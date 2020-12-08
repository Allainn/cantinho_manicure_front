from flask import current_app, redirect, session, url_for, flash, render_template, request
from ..forms import TipoServicoForm
import requests
from requests.auth import HTTPBasicAuth
import json
from .verificar import verificar

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

    response_equ = requests.get(url_base+"equipamentos/", 
                            auth=HTTPBasicAuth(session['user']['token'], ''))
    if response_equ.ok:
        form.equipamento_select.choices = [(str(forn['id']), forn['descricao']) \
                        for forn in response_equ.json()['equipamentos']]

def main():
    url_base = current_app.config.get('URL_API')
    form = TipoServicoForm()
    preencher(form)
    response = requests.get(url_base+"tipos_servico/", 
                                auth=HTTPBasicAuth(session['user']['token'], ''))
    if response.ok:
        if form.validate_on_submit():
            equipamentos = [{'id':equi} for equi in request.form.getlist('equi')]
            produtos = [{'id':pro} for pro in request.form.getlist('prod')]
            valor = form.preco_total.data.split('R$')
            valor = float(valor[1]) if len(valor) == 2 else float(valor[0])
            data = {
                'descricao'    : form.descricao.data,
                'tempo'        : form.tempo_total.data,
                'produtos'     : produtos,
                'equipamentos' : equipamentos,
                'valor'        : valor,
                'observacao'   : form.observacao.data
            }
            response_tps = requests.post(url_base+"tipos_servico/", 
                            data=json.dumps(data),
                            headers=headers,
                            auth=HTTPBasicAuth(session['user']['token'], ''))
            if response_tps.ok:
                flash('Tipo serviço cadastrado com sucesso.')
                return redirect(url_for('main.tipos_servico'))
            flash(response_tps.json()['mensagemUsuario'])
        return render_template("tipos_servico.html", form=form, url_base=url_base,
                                tipos_servico=response.json()['tipos_servico'])
    else:
        resp = verificar(response, 'cadastrar tipo servico')
        if resp:
            return resp
    return redirect(url_for('main.index'))

def deletar(id):
    url_base = current_app.config.get('URL_API')
    response = requests.delete(url_base+"tipos_servico/"+str(id), 
                                auth=HTTPBasicAuth(session['user']['token'], ''))
    if response.ok:
        flash("Tipo serviço deletado com sucesso")
    else:
        verificar(response, 'deletar tipo serviço')
    return redirect(url_for('main.tipos_servico'))

def editar(id):
    url_base = current_app.config.get('URL_API')
    response = requests.get(url_base+"tipos_servico/"+str(id), 
                                auth=HTTPBasicAuth(session['user']['token'], ''))
    if response.ok:
        form = TipoServicoForm()
        preencher(form)
        form.submit.label.text = 'Alterar'
        if form.validate_on_submit():
            equipamentos = [{'id':equi} for equi in request.form.getlist('equi')]
            produtos = [{'id':pro} for pro in request.form.getlist('prod')]
            valor = form.preco_total.data.split('R$')
            valor = float(valor[1]) if len(valor) == 2 else float(valor[0])
            data = {
                'descricao'    : form.descricao.data,
                'tempo'        : form.tempo_total.data,
                'produtos'     : produtos,
                'equipamentos' : equipamentos,
                'valor'        : valor,
                'observacao'   : form.observacao.data
            }
            response_tps = requests.put(url_base+"tipos_servico/"+str(id), 
                                    data=json.dumps(data), 
                                    headers=headers,
                                    auth=HTTPBasicAuth(session['user']['token'], ''))
            if response_tps.ok:
                flash('Tipo serviço alterado com sucesso.')
                return redirect(url_for('main.tipos_servico'))
        form.descricao.data = response.json()['descricao']
        form.preco_total.data = 'R$ '+response.json()['valor']
        form.tempo_total.data = response.json()['tempo']
        form.observacao.data = response.json()['observacao']
        return render_template('tipos_servico_edit.html', form=form, 
                                    produtos=response.json()['produtos'], 
                                    equipamentos=response.json()['equipamentos'])
    else:
        resp = verificar(response, 'editar tipo servico')
        if resp:
            return resp
    return redirect(url_for('main.tipos_servico'))