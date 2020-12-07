from flask import current_app, redirect, session, url_for, flash, render_template, request
from ..forms import CompraForm
from .table import ItemTable
import requests
from requests.auth import HTTPBasicAuth
import json
from .verificar import verificar
from datetime import datetime as dt

headers = {
   'Content-Type': 'application/json'
}

def preencher(form):
    url_base = current_app.config.get('URL_API')
    response_pro = requests.get(url_base+"produtos/", 
                            auth=HTTPBasicAuth(session['user']['token'], ''))
    if response_pro.ok:
        form.produto_select.choices = [(str(pro['id']), pro['descricao']) \
                        for pro in response_pro.json()['produtos']]
    response_forn = requests.get(url_base+"fornecedores/", 
                            auth=HTTPBasicAuth(session['user']['token'], ''))
    if response_forn.ok:
        form.fornecedor.choices = [(str(forn['id']), forn['nome']) \
                        for forn in response_forn.json()['fornecedores']]

def main():
    url_base = current_app.config.get('URL_API')
    form = CompraForm()
    preencher(form)
    response = requests.get(url_base+"compras/", 
                                auth=HTTPBasicAuth(session['user']['token'], ''))
    if response.ok:
        if form.validate_on_submit():
            data_com = form.data.data
            produtos = [{'id':pro} for pro in request.form.getlist('prod')]
            valor = form.preco_total.data.split('R$')
            valor = float(valor[1]) if len(valor) == 2 else float(valor[0])
            if data_com:
                data_com = data_com.strftime("%Y-%m-%d")
            data = {
                'data'       : data_com,
                'fornecedor' : {'id': form.fornecedor.data},
                'produtos'   : produtos,
                'valor'      : valor,
                'observacao' : form.observacao.data
            }
            response_com = requests.post(url_base+"compras/", 
                            data=json.dumps(data),
                            headers=headers,
                            auth=HTTPBasicAuth(session['user']['token'], ''))
            if response_com.ok:
                flash('Compra cadastrado com sucesso.')
                return redirect(url_for('main.compras'))
            flash(response_com.json()['mensagemUsuario'])
        return render_template("compras.html", form=form, url_base=url_base,
                                compras=response.json()['compras'])
    else:
        resp = verificar(response, 'cadastrar compra')
        if resp:
            return resp
    return redirect(url_for('main.index'))

def deletar(id):
    url_base = current_app.config.get('URL_API')
    response = requests.delete(url_base+"compras/"+str(id), 
                                auth=HTTPBasicAuth(session['user']['token'], ''))
    if response.ok:
        flash("Compra deletado com sucesso")
    else:
        verificar(response, 'deletar compra')
    return redirect(url_for('main.compras'))

def editar(id):
    url_base = current_app.config.get('URL_API')
    response = requests.get(url_base+"compras/"+str(id), 
                                auth=HTTPBasicAuth(session['user']['token'], ''))
    if response.ok:
        form = CompraForm(fornecedor = response.json()['fornecedor']['id'])
        preencher(form)
        form.submit.label.text = 'Alterar'
        if form.validate_on_submit():
            data_com = form.data.data
            produtos = [{'id':pro} for pro in request.form.getlist('id')]
            valor = form.preco_total.data.split('R$')
            valor = float(valor[1]) if len(valor) == 2 else float(valor[0])
            if data_com:
                data_com = data_com.strftime("%Y-%m-%d")
            data = {
                'data'       : data_com,
                'fornecedor' : {'id': form.fornecedor.data},
                'produtos'   : produtos,
                'valor'      : valor,
                'observacao' : form.observacao.data
            }
            response_com = requests.put(url_base+"compras/"+str(id), 
                                    data=json.dumps(data), 
                                    headers=headers,
                                    auth=HTTPBasicAuth(session['user']['token'], ''))
            if response_com.ok:
                flash('Compra alterado com sucesso.')
                return redirect(url_for('main.compras'))
        form.preco_total.data = 'R$ '+response.json()['valor']
        data = response.json()['data'].split('/')
        try:
            data = dt(int(data[2]), int(data[1]), int(data[0]))
        except:
            data = None     
        form.data.data = data
        form.observacao.data = response.json()['observacao']
        return render_template('compra_edit.html', form=form, 
                                    produtos=response.json()['produtos'])
    else:
        resp = verificar(response, 'editar compra')
        if resp:
            return resp
    return redirect(url_for('main.compras'))