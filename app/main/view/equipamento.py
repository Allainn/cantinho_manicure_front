from flask import current_app, redirect, session, url_for, flash, render_template
from ..forms import EquipamentoForm
import requests
from requests.auth import HTTPBasicAuth
import json
from .verificar import verificar

headers = {
   'Content-Type': 'application/json'
}

def main():
    url_base = current_app.config.get('URL_API')
    form = EquipamentoForm()

    response = requests.get(url_base+"equipamentos/", 
                            auth=HTTPBasicAuth(session['user']['token'], ''))
    if response.ok:
        if form.validate_on_submit():
            data = { 'descricao'   : form.descricao.data,
                     'tempo'       : form.tempo.data,
                     'preco_tempo' : str(form.preco_tempo.data),
                     'observacao'  : form.observacao.data
            }
            response_equi = requests.post(url_base+"equipamentos/", 
                            data=json.dumps(data),
                            headers=headers,
                            auth=HTTPBasicAuth(session['user']['token'], ''))
            if response_equi.ok:
                flash('Equipamento cadastrado com sucesso.')
                return redirect(url_for('main.equipamentos'))
            flash(response_equi.json()['mensagemUsuario'])
        return render_template("equipamentos.html", form=form, 
                            equipamentos=response.json()['equipamentos'])
    else:
        resp = verificar(response, 'cadastrar equipamentos')
        if resp:
            return resp
    return redirect(url_for('main.index'))

def deletar(id):
    url_base = current_app.config.get('URL_API')
    response = requests.delete(url_base+"equipamentos/"+str(id), 
                                auth=HTTPBasicAuth(session['user']['token'], ''))
    if response.ok:
        flash("Equipamento deletado com sucesso")
    else:
        verificar(response, 'deletar equipamentos')
    return redirect(url_for('main.equipamentos'))

def editar(id):
    url_base = current_app.config.get('URL_API')
    response = requests.get(url_base+"equipamentos/"+str(id), 
                                auth=HTTPBasicAuth(session['user']['token'], ''))
    if response.ok:
        form = EquipamentoForm()
        form.submit.label.text = 'Alterar'
        if form.validate_on_submit():
            data = { 'descricao'   : form.descricao.data,
                     'tempo'       : form.tempo.data,
                     'preco_tempo' : str(form.preco_tempo.data),
                     'observacao'  : form.observacao.data
            }
            response2 = requests.put(url_base+"equipamentos/"+str(id), 
                                    data=json.dumps(data), 
                                    headers=headers,
                                    auth=HTTPBasicAuth(session['user']['token'], ''))
            if response2.ok:
                flash('Equipamento alterado com sucesso.')
                return redirect(url_for('main.equipamentos'))
        form.descricao.data = response.json()['descricao']
        form.tempo.data = response.json()['tempo']
        form.preco_tempo.data = float(response.json()['preco_tempo'])
        form.observacao.data = response.json()['observacao']
        return render_template('all_edit.html', form=form, titulo='Equipamento')
    else:
        resp = verificar(response, 'editar equipamento')
        if resp:
            return resp
    return redirect(url_for('main.equipamentos'))