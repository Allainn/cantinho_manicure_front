from flask import render_template, redirect, request, url_for, flash, session, current_app
from flask_login import login_user, logout_user, login_required
from . import auth
from .forms import LoginForm, RegistrationForm
import requests
from requests.auth import HTTPBasicAuth
from ..models import User
import json


@auth.route('/login', methods=['GET', 'POST'])
def login():
    url_base = current_app.config.get('URL_API')
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data.lower()
        password = form.password.data
        response = requests.post(url_base+"tokens/", auth=HTTPBasicAuth(email, password))
        if response.ok:
            token = response.json()['token']
            response2 = requests.get(url_base+"usuarios/"+email, auth=HTTPBasicAuth(email, password))
            login = response2.json()['login']
            tp_user = response2.json()['tipo_usuario']['descricao']
            user = User(email, token, login, tp_user)
            session['user'] = {
                'login':login,
                'email':email,
                'token':token,
                'tp_user':tp_user
            }
            next = request.args.get('next')
            login_user(user, form.remember_me.data)
            if next is None or not next.startswith('/'):
                next = url_for('main.index')
            flash('Você entrou com sucesso.')
            return redirect(next)
        #message = response.json()['message']
        flash('Email ou senha invalido.')
    return render_template('auth/login.html', form=form)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    del(session['user'])
    flash('Você saiu com sucesso.')
    return redirect(url_for('main.index'))

@auth.route('/registrar', methods=['GET', 'POST'])
def register():
    url_base = current_app.config.get('URL_API')
    form = RegistrationForm()
    if form.validate_on_submit():
        data = {'login'        : form.login.data,
                'email'        : form.email.data.lower(), 
                'senha_hash'   : form.password.data,
                'tipo_usuario' : { 
                    'id' : 1 
                }
        }
        headers = {
            'Content-Type': 'application/json'
        }
        response = requests.post(url_base+"usuarios/", 
                                data=json.dumps(data), 
                                headers=headers)

        if response.ok:
            flash('Você pode entrar agora.')
            return redirect(url_for('auth.login'))
        flash(response.json()['mensagemUsuario'])
    return render_template('auth/register.html', form=form)