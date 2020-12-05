from flask import current_app, redirect, session, url_for, flash, render_template
from ..forms import TipoQuantidadeForm
import requests
from requests.auth import HTTPBasicAuth
import json
from .verificar import verificar

headers = {
   'Content-Type': 'application/json'
}

def main():
    url_base = current_app.config.get('URL_API')
    form = TipoQuantidadeForm()

    response = requests.get(url_base+"tipos_quantidade/", 
                            auth=HTTPBasicAuth(session['user']['token'], ''))
    if response.ok:
        if form.validate_on_submit():
            data = { 'descricao'    : form.descricao.data,
                     'sigla'        : form.sigla.data
            }
            response_tp = requests.post(url_base+"tipos_quantidade/", 
                            data=json.dumps(data), 
                            headers=headers,
                            auth=HTTPBasicAuth(session['user']['token'], ''))
            if response_tp.ok:
                flash('Tipo quantidade cadastrado com sucesso.')
                return redirect(url_for('main.tipos_quantidade'))
            flash(response_tp.json()['mensagemUsuario'])
        return render_template("tipos_quantidade.html", form=form, 
                            tipos_quantidade=response.json()['tipos_quantidade'])
    else:
        resp = verificar(response, 'cadastrar tipo quantidade')
        if resp:
            return resp
    return redirect(url_for('main.index'))

def deletar(id):
   url_base = current_app.config.get('URL_API')
   response = requests.delete(url_base+"tipos_quantidade/"+str(id), 
                            auth=HTTPBasicAuth(session['user']['token'], ''))
   if response.ok:
      flash("Tipo quantidade deletado com sucesso")
   else:
      verificar(response, 'deletar tipo quantidade')
   return redirect(url_for('main.tipos_quantidade'))

def editar(id):
   url_base = current_app.config.get('URL_API')
   response = requests.get(url_base+"tipos_quantidade/"+str(id), 
                              auth=HTTPBasicAuth(session['user']['token'], ''))
   if response.ok:
      form = TipoQuantidadeForm()
      form.submit.label.text = 'Alterar'
      if form.validate_on_submit():
         data = { 'descricao' : form.descricao.data,
                  'sigla'     : form.sigla.data.lower(),
         }
         response_tp = requests.put(url_base+"tipos_quantidade/"+str(id), 
                                data=json.dumps(data), 
                                headers=headers,
                                auth=HTTPBasicAuth(session['user']['token'], ''))
         if response_tp.ok:
            flash('Tipo quantidade alterado com sucesso.')
            return redirect(url_for('main.tipos_quantidade'))
      form.descricao.data = response.json()['descricao']
      form.sigla.data = response.json()['sigla']
      return render_template('all_edit.html', form=form, titulo='Tipo Quantidade')
   else:
      resp = verificar(response, 'editar tipo quantidade')
      if resp:
         return resp
   return redirect(url_for('main.tipos_quantidade'))
