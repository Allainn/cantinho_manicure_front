from flask import current_app, redirect, session, url_for, flash, render_template
from ..forms import FornecedorForm
import requests
from requests.auth import HTTPBasicAuth
import json
from .verificar import verificar
from .endereco import verificar_bairro_endereco
from .tipo_usuario import alterar_tipo_usuario
from .cliente import preencher_form

headers = {
   'Content-Type': 'application/json'
}

def pre_fornecedores(form):
    id_cidade = form.cidade.data
    bairro = form.bairro.data
    rua = form.rua.data
    comp = form.complemento.data

    id_end = verificar_bairro_endereco(id_cidade, bairro, rua, comp)

    # Cadastrar Fornecedor
    data_for = {
        'nome'            : form.nome.data,
        'email'           : form.email.data,
        'endereco'        : {
                            'id' : id_end
                        },
        'numero'          : form.numero.data,
        'telefone1'       : form.telefone1.data,
        'telefone2'       : form.telefone2.data,
        'site'            : form.site.data,
        'instagram'       : form.instagram.data,
        'facebook'        : form.facebook.data,
        'observacao'      : form.observacao.data
    }

    return data_for

def main():
    url_base = current_app.config.get('URL_API')
    form = FornecedorForm(estado = '31', cidade = '3118007')
    preencher_form(form, usuario=False)
    response = requests.get(url_base+"fornecedores/", 
                                auth=HTTPBasicAuth(session['user']['token'], ''))
    if response.ok:
        if form.validate_on_submit():
            data_for = pre_fornecedores(form)
            
            response_for = requests.post(url_base+"fornecedores/", 
                                data=json.dumps(data_for), 
                                headers=headers,
                                auth=HTTPBasicAuth(session['user']['token'], ''))
            if response_for.ok:
                flash('Fornecedor cadastrado com sucesso.')
                return redirect(url_for('main.fornecedores'))
            flash(response_for.json()['mensagemUsuario'])
        preencher_form(form, cidade=True, estado=form.estado.data, default=False, 
                        usuario=False)
        return render_template("fornecedores.html", url_base=url_base, form=form, 
                                fornecedores=response.json()['fornecedores'])
    else:
        resp = verificar(response, 'cadastrar fornecedor')
        if resp:
            return resp
    return redirect(url_for('main.index'))

def deletar(id):
   url_base = current_app.config.get('URL_API')
   response = requests.delete(url_base+"fornecedores/"+str(id), 
                              auth=HTTPBasicAuth(session['user']['token'], ''))
   if response.ok:
      try:
         id_usr = response.json()['usuario']['id']
         alterar_tipo_usuario(id_usr, 1, 'usuário')
      except:
         pass

      flash("Fornecedor deletado com sucesso")
   else:
      resp = verificar(response, 'deletar fornecedor')
      if resp:
         return resp
   return redirect(url_for('main.fornecedores'))

def editar(id):
    url_base = current_app.config.get('URL_API')
    response = requests.get(url_base+"fornecedores/"+str(id), 
                                auth=HTTPBasicAuth(session['user']['token'], ''))
    if response.ok:
        fornecedor = response.json() 
        estado = fornecedor['endereco']['bairro']['cidade']['estado']['id']
        cidade = fornecedor['endereco']['bairro']['cidade']['id']

        form = FornecedorForm(estado = estado, cidade = cidade)
        preencher_form(form, cidade=True, estado=estado, usuario=False)
        form.submit.label.text = 'Alterar'
        if form.validate_on_submit():
            data_for = pre_fornecedores(form)
            response_for = requests.put(url_base+"fornecedores/"+str(id), 
                                data=json.dumps(data_for), 
                                headers=headers,
                                auth=HTTPBasicAuth(session['user']['token'], ''))
            if response_for.ok:
                flash('Fornecedor alterado com sucesso.')
                return redirect(url_for('main.fornecedores'))
        form.nome.data = fornecedor['nome']
        form.email.data = fornecedor['email']
        form.bairro.data = fornecedor['endereco']['bairro']['descricao']
        form.rua.data = fornecedor['endereco']['rua']
        form.complemento.data = fornecedor['endereco']['complemento']
        form.numero.data = fornecedor['numero']
        form.telefone1.data = fornecedor['telefone1']
        form.telefone2.data = fornecedor['telefone2']
        form.site.data = fornecedor['site']
        form.instagram.data = fornecedor['instagram']
        form.facebook.data = fornecedor['facebook']
        form.observacao.data = fornecedor['observacao']
        return render_template('all_edit.html', form=form, titulo='Fornecedor', 
                                url_base=url_base)
    else:
        resp = verificar(response, 'editar fornecedor')
        if resp:
            return resp
    return redirect(url_for('main.fornecedores'))