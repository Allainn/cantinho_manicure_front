from flask import current_app, redirect, session, url_for, flash, render_template
from ..forms import ClienteForm
import requests
from requests.auth import HTTPBasicAuth
import json
from .verificar import verificar
from datetime import datetime as dt

headers = {
   'Content-Type': 'application/json'
}

def alterar_tipo_usuario(id_user, id_tp, desc):
   url_base = current_app.config.get('URL_API')
   response_usr = requests.get(url_base+"usuarios/"+str(id_user), 
                     auth=HTTPBasicAuth(session['user']['token'], ''))
   if response_usr.ok:
      usr = response_usr.json()['login']
      tp_usr = response_usr.json()['tipo_usuario']['descricao'].upper()
      if tp_usr == 'USUARIO' or tp_usr == 'CLIENTE':
         data_user = {
            'tipo_usuario' : {
               'id' : id_tp
            }
         }
         response_user = requests.put(url_base+"usuarios/"+str(id_user), 
                        data=json.dumps(data_user), 
                        headers=headers,
                        auth=HTTPBasicAuth(session['user']['token'], ''))
         if response_user.ok:
            flash("Usuário {} foi alterado para {}".format(usr, desc))

def pre_clientes(form):
   url_base = current_app.config.get('URL_API')
   id_bairro = id_end = None
   id_cidade = form.cidade.data
   id_user = form.usuario.data
   bairro = form.bairro.data
   rua = form.rua.data
   comp = form.complemento.data
   data_nas = form.dataNascimento.data
   
   # Verificar Bairro, senão tem cadastre
   response_bai = requests.get(url_base+"bairros/"+id_cidade+"/"+bairro,
                     auth=HTTPBasicAuth(session['user']['token'], ''))
   if response_bai.ok:
      id_bairro = response_bai.json()['id']
   else:
      data_bairro = {
         'descricao' : bairro,
         'cidade'    : {
            'id' : id_cidade
         }
      }
      response_bai = requests.post(url_base+"bairros/",
                        data=json.dumps(data_bairro),
                        headers=headers,
                        auth=HTTPBasicAuth(session['user']['token'], ''))
      if response_bai.ok:
         id_bairro = response_bai.json()['id']
         flash('Bairro cadastrado com sucesso.')
      else:
         flash(response_bai.json()['mensagemUsuario'])

   # Verificar Endereço, senão tem cadastre
   response_end = requests.get(url_base+"enderecos/"+str(id_bairro)+"/"+rua+"/"+\
                                (comp if comp else ' '),
                            auth=HTTPBasicAuth(session['user']['token'], ''))
   if response_end.ok:
      id_end = response_end.json()['id']
   else:
      data_end = {
         'rua'         : form.rua.data,
         'complemento' : form.complemento.data,
         'bairro'      : {
            'id' : id_bairro
         }
      }
      response_end = requests.post(url_base+"enderecos/",
                           data=json.dumps(data_end),
                           headers=headers,
                           auth=HTTPBasicAuth(session['user']['token'], ''))
      if response_end.ok:
         id_end = response_end.json()['id']
         flash('Endereço cadastrado com sucesso.')
      else:
         flash(response_bai.json()['mensagemUsuario'])
   
   # Cadastrar Cliente
   if data_nas:
      data_nas = data_nas.strftime("%Y-%m-%d")
   data_cli = {
      'nome'            : form.nome.data,
      'endereco'        : {
                           'id' : id_end
                        },
      'numero'          : form.numero.data,
      'telefone1'       : form.telefone1.data,
      'telefone2'       : form.telefone2.data,
      'data_nascimento' : data_nas,
      'instagram'       : form.instagram.data,
      'facebook'        : form.facebook.data
   }

   if id_user != '0':
      alterar_tipo_usuario(id_user, 2, "cliente")
      data_cli['usuario'] = {
         'id' : id_user
      }

   return data_cli

def preencher_form_cliente(form):
   url_base = current_app.config.get('URL_API')
   response_es = requests.get(url_base+"estados/", 
                              auth=HTTPBasicAuth(session['user']['token'], ''))
   if response_es.ok:
      form.estado.choices = [(str(es['id']), es['uf']) \
                                 for es in response_es.json()['estados']]
   response_user = requests.get(url_base+"usuarios/", 
                              auth=HTTPBasicAuth(session['user']['token'], ''))
   if response_user.ok:
      form.usuario.choices = [("0","")]+[(str(user['id']), user['login']) \
                                 for user in response_user.json()['usuarios']]

def clientes():
   url_base = current_app.config.get('URL_API')
   form = ClienteForm()
   preencher_form_cliente(form)

   response = requests.get(url_base+"clientes/", 
                              auth=HTTPBasicAuth(session['user']['token'], ''))
   if response.ok:
      if form.validate_on_submit():
         data_cli = pre_clientes(form)
         
         response_cli = requests.post(url_base+"clientes/", 
                              data=json.dumps(data_cli), 
                              headers=headers,
                              auth=HTTPBasicAuth(session['user']['token'], ''))
         if response_cli.ok:
            flash('Cliente cadastrado com sucesso.')
            return redirect(url_for('main.clientes'))
         flash(response_cli.json()['mensagemUsuario'])
      return render_template("clientes.html", url_base=url_base, form=form, 
                              clientes=response.json()['clientes'])
   else:
      resp = verificar(response, 'cadastrar cliente')
      if resp:
         return resp
   return redirect(url_for('main.index'))

def del_cliente(id):
   url_base = current_app.config.get('URL_API')
   response = requests.delete(url_base+"clientes/"+str(id), 
                              auth=HTTPBasicAuth(session['user']['token'], ''))
   if response.ok:
      try:
         id_usr = response.json()['usuario']['id']
         alterar_tipo_usuario(id_usr, 1, 'usuário')
      except:
         pass

      flash("Cliente deletado com sucesso")
   else:
      resp = verificar(response, 'deletar cliente')
      if resp:
         return resp
   return redirect(url_for('main.clientes'))

def edit_cliente(id):
   url_base = current_app.config.get('URL_API')
   response = requests.get(url_base+"clientes/"+str(id), 
                              auth=HTTPBasicAuth(session['user']['token'], ''))
   if response.ok:
      cliente = response.json() 
      estado = cliente['endereco']['bairro']['cidade']['estado']['id']
      cidade = cliente['endereco']['bairro']['cidade']['id']
      try:
         usuario = cliente['usuario']['id']
      except:
         usuario = '0'
      form = ClienteForm(estado = estado, cidade = cidade, usuario=usuario)
      preencher_form_cliente(form)
      response_cid = requests.get(url_base+"cidades/uf/"+str(estado), 
                              auth=HTTPBasicAuth(session['user']['token'], ''))
      if response_cid.ok:
         form.cidade.choices = [(str(cid['id']), cid['descricao']) \
                        for cid in response_cid.json()['cidades']]
      form.submit.label.text = 'Alterar'
      if form.validate_on_submit():
         data_cli = pre_clientes(form)
         response_cli = requests.put(url_base+"clientes/"+str(id), 
                              data=json.dumps(data_cli), 
                              headers=headers,
                              auth=HTTPBasicAuth(session['user']['token'], ''))
         if response_cli.ok:
            flash('Cliente alterado com sucesso.')
            return redirect(url_for('main.clientes'))
      form.nome.data = cliente['nome']
      form.bairro.data = cliente['endereco']['bairro']['descricao']
      form.rua.data = cliente['endereco']['rua']
      form.complemento.data = cliente['endereco']['complemento']
      form.numero.data = cliente['numero']
      form.telefone1.data = cliente['telefone1']
      form.telefone2.data = cliente['telefone2']
      form.telefone1.data = cliente['telefone1']
      data_nas = cliente['data_nascimento'].split('/')
      try:
         data_nas = dt(int(data_nas[2]), int(data_nas[1]), int(data_nas[0]))
      except:
         data_nas = None     
      form.dataNascimento.data = data_nas
      form.instagram.data = cliente['instagram']
      form.facebook.data = cliente['facebook']
      return render_template('cliente_edit.html', form=form, url_base=url_base)
   else:
      resp = verificar(response, 'editar cliente')
      if resp:
         return resp
   return redirect(url_for('main.clientes'))