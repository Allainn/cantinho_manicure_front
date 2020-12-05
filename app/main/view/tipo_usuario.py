from flask import current_app, session, flash
import requests
from requests.auth import HTTPBasicAuth
import json

headers = {
   'Content-Type': 'application/json'
}

def alterar_tipo_usuario(id_user, id_tp, desc):
   url_base = current_app.config.get('URL_API')
   response_usr = requests.get(url_base+"usuarios/"+str(id_user), 
                     auth=HTTPBasicAuth(session['user']['token'], ''))
   if response_usr.ok:
      usr = response_usr.json()['login']
      tp_usr = response_usr.json()['tipo_usuario']['descricao'].upper()
      print(tp_usr)
      print(id_tp)
      if (tp_usr == 'USUARIO' and id_tp != 1) or \
            (tp_usr == 'CLIENTE' and id_tp != 2) or \
            (tp_usr == 'FUNCIONARIO' and id_tp != 3):
         data_user = {
            'tipo_usuario' : {
               'id' : id_tp
            }
         }
         response_user = requests.put(url_base+"usuarios/"+str(id_user), 
                        data=json.dumps(data_user), 
                        headers=headers,
                        auth=HTTPBasicAuth(session['user']['token'], ''))
         if response_user.ok:
            flash("Usuário {} foi alterado para {}".format(usr, desc))