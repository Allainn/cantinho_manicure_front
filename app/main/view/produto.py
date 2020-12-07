from flask import current_app, redirect, session, url_for, flash, render_template
from ..forms import ProdutoForm
import requests
from requests.auth import HTTPBasicAuth
import json
from .verificar import verificar

headers = {
   'Content-Type': 'application/json'
}

def preencher(form):
    url_base = current_app.config.get('URL_API')
    response_tp = requests.get(url_base+"tipos_quantidade/", 
                            auth=HTTPBasicAuth(session['user']['token'], ''))
    if response_tp.ok:
        form.tipo_quantidade.choices = [(str(tp['id']), tp['sigla']) \
                        for tp in response_tp.json()['tipos_quantidade']]

def main():
    url_base = current_app.config.get('URL_API')
    form = ProdutoForm()
    preencher(form)

    response = requests.get(url_base+"produtos/", 
                            auth=HTTPBasicAuth(session['user']['token'], ''))
    if response.ok:
        if form.validate_on_submit():
            data = { 'descricao'        : form.descricao.data,
                     'quantidade'       : form.quantidade.data,
                     'tipo_quantidade'  : {
                         'id': form.tipo_quantidade.data
                     },
                     'preco_un'         : str(form.preco_un.data),
                     'observacao'       : form.observacao.data
            }
            response_pro = requests.post(url_base+"produtos/", 
                            data=json.dumps(data),
                            headers=headers,
                            auth=HTTPBasicAuth(session['user']['token'], ''))
            if response_pro.ok:
                flash('Produto cadastrado com sucesso.')
                return redirect(url_for('main.produtos'))
            flash(response_pro.json()['mensagemUsuario'])
        return render_template("produtos.html", form=form, 
                            produtos=response.json()['produtos'])
    else:
        resp = verificar(response, 'cadastrar produtos')
        if resp:
            return resp
    return redirect(url_for('main.index'))

def deletar(id):
    url_base = current_app.config.get('URL_API')
    response = requests.delete(url_base+"produtos/"+str(id), 
                                auth=HTTPBasicAuth(session['user']['token'], ''))
    if response.ok:
        flash("Produto deletado com sucesso")
    else:
        verificar(response, 'deletar produto')
    return redirect(url_for('main.produtos'))

def editar(id):
    url_base = current_app.config.get('URL_API')
    response = requests.get(url_base+"produtos/"+str(id), 
                                auth=HTTPBasicAuth(session['user']['token'], ''))
    if response.ok:
        form = ProdutoForm(tipo_quantidade = response.json()['tipo_quantidade']['id'])
        preencher(form)
        form.submit.label.text = 'Alterar'
        if form.validate_on_submit():
            data = {'descricao'        : form.descricao.data,
                    'quantidade'       : form.quantidade.data,
                    'tipo_quantidade'  : {
                        'id': form.tipo_quantidade.data
                    },
                    'preco_un'         : str(form.preco_un.data),
                    'observacao'       : form.observacao.data
            }
            response2 = requests.put(url_base+"produtos/"+str(id), 
                                    data=json.dumps(data), 
                                    headers=headers,
                                    auth=HTTPBasicAuth(session['user']['token'], ''))
            if response2.ok:
                flash('Produto alterado com sucesso.')
                return redirect(url_for('main.produtos'))
        form.descricao.data = response.json()['descricao']
        form.quantidade.data = response.json()['quantidade']
        form.preco_un.data = float(response.json()['preco_un'])
        form.observacao.data = response.json()['observacao']
        return render_template('all_edit.html', form=form, titulo='Produto')
    else:
        resp = verificar(response, 'editar produto')
        if resp:
            return resp
    return redirect(url_for('main.produtos'))