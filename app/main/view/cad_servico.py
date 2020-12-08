from flask import current_app, redirect, session, url_for, flash, render_template, request
from ..forms import ServicoForm
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
    response_cli = requests.get(url_base+"clientes/", 
                            auth=HTTPBasicAuth(session['user']['token'], ''))
    if response_cli.ok:
        form.cliente.choices = [(str(cli['id']), cli['nome']) \
                    for cli in response_cli.json()['clientes']]

    response_tps = requests.get(url_base+"tipos_servico/", 
                            auth=HTTPBasicAuth(session['user']['token'], ''))
    if response_tps.ok:
        form.tipo_servico.choices = [(str(tps['id']), tps['descricao']) \
                    for tps in response_tps.json()['tipos_servico']]

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

    return response_tps.json()['tipos_servico']

def main():
    url_base = current_app.config.get('URL_API')
    form = ServicoForm()
    tipos_servico = preencher(form)
    response = requests.get(url_base+"servicos/", 
                            auth=HTTPBasicAuth(session['user']['token'], ''))
    if response.ok:
        if form.validate_on_submit():
            equipamentos = [{'id':equi} for equi in request.form.getlist('equi')]
            produtos = [{'id':pro} for pro in request.form.getlist('prod')]
            tps_servico = [{'id':tps} for tps in request.form.getlist('tp_serv')]
            valor = form.preco_total.data.split('R$')
            valor = float(valor[1]) if len(valor) == 2 else float(valor[0])
            data_ser = form.data.data
            if data_ser:
                data_ser = data_ser.strftime("%Y-%m-%d")
            data = {
                'cliente'       : {'id' : form.cliente.data},
                'tipos_servico' : tps_servico,
                'produtos'      : produtos,
                'equipamentos'  : equipamentos,
                'valor'         : valor,
                'tempo'         : form.tempo_total.data,
                'data'          : data_ser,
                'hora'          : form.hora.data,
                'observacao'    : form.observacao.data
            }
            response_ser = requests.post(url_base+"servicos/", 
                            data=json.dumps(data),
                            headers=headers,
                            auth=HTTPBasicAuth(session['user']['token'], ''))
            if response_ser.ok:
                flash('Serviço cadastrado com sucesso.')
                return redirect(url_for('main.cad_servicos'))
            flash(response_ser.json()['mensagemUsuario'])
        return render_template("cad_servicos.html", form=form, url_base=url_base, 
                tipos_servico=tipos_servico, servicos=response.json()['servicos'])
    else:
        resp = verificar(response, 'cadastrar serviço')
        if resp:
            return resp
    return redirect(url_for('main.index'))

def deletar(id):
    url_base = current_app.config.get('URL_API')
    response = requests.delete(url_base+"servicos/"+str(id), 
                                auth=HTTPBasicAuth(session['user']['token'], ''))
    if response.ok:
        flash("Serviço deletado com sucesso")
    else:
        verificar(response, 'deletar serviço')
    return redirect(url_for('main.cad_servicos'))

def editar(id):
    url_base = current_app.config.get('URL_API')
    response = requests.get(url_base+"servicos/"+str(id), 
                                auth=HTTPBasicAuth(session['user']['token'], ''))
    if response.ok:
        form = ServicoForm()
        tipos_servico = preencher(form)
        form.submit.label.text = 'Alterar'
        if form.validate_on_submit():
            equipamentos = [{'id':equi} for equi in request.form.getlist('equi')]
            produtos = [{'id':pro} for pro in request.form.getlist('prod')]
            tps_servico = [{'id':tps} for tps in request.form.getlist('tp_serv')]
            valor = form.preco_total.data.split('R$')
            valor = float(valor[1]) if len(valor) == 2 else float(valor[0])
            data_ser = form.data.data
            if data_ser:
                data_ser = data_ser.strftime("%Y-%m-%d")
            data = {
                'cliente'       : {'id' : form.cliente.data},
                'tipos_servico' : tps_servico,
                'produtos'      : produtos,
                'equipamentos'  : equipamentos,
                'valor'         : valor,
                'tempo'         : form.tempo_total.data,
                'data'          : data_ser,
                'hora'          : form.hora.data,
                'observacao'    : form.observacao.data
            }
            print(data)
            response_ser = requests.put(url_base+"servicos/"+str(id), 
                                    data=json.dumps(data), 
                                    headers=headers,
                                    auth=HTTPBasicAuth(session['user']['token'], ''))
            if response_ser.ok:
                flash('Serviço alterado com sucesso.')
                return redirect(url_for('main.cad_servicos'))
        data = response.json()['data'].split('/')
        try:
            data = dt(int(data[2]), int(data[1]), int(data[0]))
        except:
            data = None     
        form.data.data = data
        form.hora.data = response.json()['hora']
        form.preco_total.data = 'R$ '+response.json()['valor']
        form.tempo_total.data = response.json()['tempo']
        form.observacao.data = response.json()['observacao']
        return render_template('cad_servico_edit.html', form=form, 
                                    produtos=response.json()['produtos'], 
                                    equipamentos=response.json()['equipamentos'],
                                    tps_servico=tipos_servico,
                                    tipos_servico=response.json()['tipos_servico'])
    else:
        resp = verificar(response, 'editar tipo servico')
        if resp:
            return resp
    return redirect(url_for('main.cad_servicos'))