from flask import current_app, redirect, session, url_for, flash, render_template
from ..forms import RegistrationForm
import requests
from requests.auth import HTTPBasicAuth
import json
from .verificar import verificar

headers = {
   'Content-Type': 'application/json'
}

def usuarios():
   url_base = current_app.config.get('URL_API')
   form = RegistrationForm()
   tp_user = []
   response_tp = requests.get(url_base+"tipos_usuario/", 
                            auth=HTTPBasicAuth(session['user']['token'], ''))
   if response_tp.ok:
      for tp in response_tp.json()['tipos_usuario']:
         tp_user.append((str(tp['id']), tp['descricao']))
   form.tipo_usuario.choices = tp_user

   response = requests.get(url_base+"usuarios/", 
                            auth=HTTPBasicAuth(session['user']['token'], ''))
   
   if response.ok:
      if form.validate_on_submit():
         data = { 'login'        : form.login.data,
                  'email'        : form.email.data.lower(), 
                  'senha_hash'   : form.password.data,
                  'tipo_usuario' : { 
                     'id' : form.tipo_usuario.data
                  }
         }
         response2 = requests.post(url_base+"usuarios/", 
                            data=json.dumps(data), 
                            headers=headers,
                            auth=HTTPBasicAuth(session['user']['token'], ''))
         if response2.ok:
            flash('Usuário cadastrado com sucesso.')
            return redirect(url_for('main.usuarios'))
         flash(response2.json()['mensagemUsuario'])
      return render_template("usuarios.html", form=form, 
                            usuarios=response.json()['usuarios'])
   else:
      resp = verificar(response, 'cadastrar usuário')
      if resp:
         return resp
   return redirect(url_for('main.index'))

def del_usuario(id):
   url_base = current_app.config.get('URL_API')
   response = requests.delete(url_base+"usuarios/"+str(id), 
                            auth=HTTPBasicAuth(session['user']['token'], ''))
   if response.ok:
      flash("Usuário deletado com sucesso")
   else:
      verificar(response, 'deletar usuário')
   return redirect(url_for('main.usuarios'))

def edit_usuario(id):
   url_base = current_app.config.get('URL_API')
   response = requests.get(url_base+"usuarios/"+str(id), 
                              auth=HTTPBasicAuth(session['user']['token'], ''))
   if response.ok:
      form = RegistrationForm(tipo_usuario = response.json()['tipo_usuario']['id'])
      tp_user = []
      response_tp = requests.get(url_base+"tipos_usuario/", 
                              auth=HTTPBasicAuth(session['user']['token'], ''))
      for tp in response_tp.json()['tipos_usuario']:
         tp_user.append((str(tp['id']), tp['descricao']))
      form.tipo_usuario.choices = tp_user
      form.submit.label.text = 'Alterar'
      del(form.password)
      del(form.password2)
      if form.validate_on_submit():
         data = { 'login'        : form.login.data,
                  'email'        : form.email.data.lower(),
                  'tipo_usuario' : { 
                     'id' : form.tipo_usuario.data
                  }
         }
         response2 = requests.put(url_base+"usuarios/"+str(id), 
                                data=json.dumps(data), 
                                headers=headers,
                                auth=HTTPBasicAuth(session['user']['token'], ''))
         if response2.ok:
            flash('Usuário alterado com sucesso.')
            return redirect(url_for('main.usuarios'))
      form.email.data = response.json()['email']
      form.login.data = response.json()['login']
      return render_template('usuario_edit.html', usuario = response.json(), 
                            form=form)
   else:
      resp = verificar(response, 'editar usuário')
      if resp:
         return resp
   return redirect(url_for('main.usuarios'))
