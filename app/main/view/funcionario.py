from flask import current_app, redirect, session, url_for, flash, render_template
from ..forms import ClienteForm
import requests
from requests.auth import HTTPBasicAuth
import json
from .verificar import verificar
from datetime import datetime as dt
from .endereco import verificar_bairro_endereco
from .tipo_usuario import alterar_tipo_usuario
from .cliente import preencher_form

headers = {
   'Content-Type': 'application/json'
}

def pre_funcionarios(form):
   id_cidade = form.cidade.data
   id_user = form.usuario.data
   bairro = form.bairro.data
   rua = form.rua.data
   comp = form.complemento.data
   data_nas = form.dataNascimento.data
   
   id_end = verificar_bairro_endereco(id_cidade, bairro, rua, comp)

   # Cadastrar Funcionario
   if data_nas:
      data_nas = data_nas.strftime("%Y-%m-%d")
   data_fun = {
      'nome'            : form.nome.data,
      'endereco'        : {
                           'id' : id_end
                        },
      'numero'          : form.numero.data,
      'telefone1'       : form.telefone1.data,
      'telefone2'       : form.telefone2.data,
      'data_nascimento' : data_nas,
   }

   if id_user != '0':
      alterar_tipo_usuario(id_user, 3, "funcionário")
      data_fun['usuario'] = {
         'id' : id_user
      }

   return data_fun

def main():
    url_base = current_app.config.get('URL_API')
    form = ClienteForm(estado = '31', cidade = '3118007')
    del(form.facebook)
    del(form.instagram)
    preencher_form(form)
    form.usuario.choices.pop(0)

    response = requests.get(url_base+"funcionarios/", 
                                auth=HTTPBasicAuth(session['user']['token'], ''))
    if response.ok:
        if form.validate_on_submit():
            data_fun = pre_funcionarios(form)
            
            response_fun = requests.post(url_base+"funcionarios/", 
                                data=json.dumps(data_fun), 
                                headers=headers,
                                auth=HTTPBasicAuth(session['user']['token'], ''))
            if response_fun.ok:
                flash('Funcionário cadastrado com sucesso.')
                return redirect(url_for('main.funcionarios'))
            flash(response_fun.json()['mensagemUsuario'])
        preencher_form(form, cidade=True, estado=form.estado.data, default=False, usuario=False)
        return render_template("funcionarios.html", url_base=url_base, form=form, 
                                funcionarios=response.json()['funcionarios'])
    else:
        resp = verificar(response, 'cadastrar funcionário')
        if resp:
            return resp
    return redirect(url_for('main.index'))

def deletar(id):
    url_base = current_app.config.get('URL_API')
    response = requests.delete(url_base+"funcionarios/"+str(id), 
                                auth=HTTPBasicAuth(session['user']['token'], ''))
    if response.ok:
        try:
            id_usr = response.json()['usuario']['id']
            alterar_tipo_usuario(id_usr, 1, 'usuário')
        except:
            pass

        flash("Funcionário deletado com sucesso")
    else:
        resp = verificar(response, 'deletar funcionário')
        if resp:
            return resp
    return redirect(url_for('main.funcionarios'))

def editar(id):
    url_base = current_app.config.get('URL_API')
    response = requests.get(url_base+"funcionarios/"+str(id), 
                                auth=HTTPBasicAuth(session['user']['token'], ''))
    if response.ok:
        funcionario = response.json() 
        estado = funcionario['endereco']['bairro']['cidade']['estado']['id']
        cidade = funcionario['endereco']['bairro']['cidade']['id']
        try:
            usuario = funcionario['usuario']['id']
        except:
            usuario = '0'
        form = ClienteForm(estado = estado, cidade = cidade, usuario=usuario)
        del(form.facebook)
        del(form.instagram)
        preencher_form(form, cidade=True, estado=estado)
        form.usuario.choices.pop(0)
        form.submit.label.text = 'Alterar'
        if form.validate_on_submit():
            data_cli = pre_funcionarios(form)
            response_cli = requests.put(url_base+"funcionarios/"+str(id), 
                                data=json.dumps(data_cli), 
                                headers=headers,
                                auth=HTTPBasicAuth(session['user']['token'], ''))
            if response_cli.ok:
                flash('Funcionário alterado com sucesso.')
                return redirect(url_for('main.funcionarios'))
        form.nome.data = funcionario['nome']
        form.bairro.data = funcionario['endereco']['bairro']['descricao']
        form.rua.data = funcionario['endereco']['rua']
        form.complemento.data = funcionario['endereco']['complemento']
        form.numero.data = funcionario['numero']
        form.telefone1.data = funcionario['telefone1']
        form.telefone2.data = funcionario['telefone2']
        data_nas = funcionario['data_nascimento'].split('/')
        try:
            data_nas = dt(int(data_nas[2]), int(data_nas[1]), int(data_nas[0]))
        except:
            data_nas = None     
        form.dataNascimento.data = data_nas
        return render_template('all_edit.html', form=form, titulo='Funcionário', 
                                url_base=url_base)
    else:
        resp = verificar(response, 'editar funcionário')
        if resp:
            return resp
    return redirect(url_for('main.funcionarios'))