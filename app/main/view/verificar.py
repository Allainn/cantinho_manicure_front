def verificar(response, mensagem):
   if response.status_code == 401:
      flash('Sessão expirada.')
      return redirect(url_for('auth.logout'))
   elif response.status_code == 403:
      flash("Você não tem permissão de acessar esta área.")
   else:
      flash("Falha ao {}.".format(mensagem))