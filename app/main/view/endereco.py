from flask import current_app, session, flash
import requests
from requests.auth import HTTPBasicAuth
import json

headers = {
   'Content-Type': 'application/json'
}

def verificar_bairro_endereco(id_cidade, bairro, rua, comp):
    url_base = current_app.config.get('URL_API')
    # Verificar Bairro, senão tem cadastre
    response_bai = requests.get(url_base+"bairros/"+id_cidade+"/"+bairro,
                        auth=HTTPBasicAuth(session['user']['token'], ''))
    if response_bai.ok:
        id_bairro = response_bai.json()['id']
    else:
        data_bairro = {
            'descricao' : bairro,
            'cidade'    : {
                'id' : id_cidade
            }
        }
        response_bai = requests.post(url_base+"bairros/",
                            data=json.dumps(data_bairro),
                            headers=headers,
                            auth=HTTPBasicAuth(session['user']['token'], ''))
        if response_bai.ok:
            id_bairro = response_bai.json()['id']
            flash('Bairro cadastrado com sucesso.')
        else:
            flash(response_bai.json()['mensagemUsuario'])

    # Verificar Endereço, senão tem cadastre
    response_end = requests.get(url_base+"enderecos/"+str(id_bairro)+"/"+rua+"/"+\
                                    (comp if comp else ' '),
                                auth=HTTPBasicAuth(session['user']['token'], ''))
    if response_end.ok:
        id_end = response_end.json()['id']
    else:
        data_end = {
            'rua'         : rua,
            'complemento' : comp,
            'bairro'      : {
                'id' : id_bairro
            }
        }
        response_end = requests.post(url_base+"enderecos/",
                            data=json.dumps(data_end),
                            headers=headers,
                            auth=HTTPBasicAuth(session['user']['token'], ''))
        if response_end.ok:
            id_end = response_end.json()['id']
            flash('Endereço cadastrado com sucesso.')
        else:
            flash(response_bai.json()['mensagemUsuario'])
            return ''
    return id_end

