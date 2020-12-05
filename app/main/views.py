from . import main
from flask_login import login_required
from .view import index as ind
from .view import usuario as usr
from .view import cliente as cli
from .view import servico as ser
from .view import funcionario as fun

headers = {
   'Content-Type': 'application/json'
}

@main.route('/')
def index():
   return ind.index()

@main.route('/servicos')
def servicos():
   return ser.servicos()
   
@main.route('/usuarios', methods=['GET', 'POST'])
@login_required
def usuarios():
   return usr.usuarios()

@main.route('/usuarios/d/<int:id>', methods = ['POST','GET'])
@login_required
def del_usuario(id):
   return usr.del_usuario(id)

@main.route('/usuarios/e/<int:id>', methods = ['POST','GET'])
@login_required
def edit_usuario(id):
   return usr.edit_usuario(id)

@main.route('/clientes', methods=['GET', 'POST'])
@login_required
def clientes():
   return cli.clientes()

@main.route('/clientes/d/<int:id>', methods = ['POST','GET'])
@login_required
def del_cliente(id):
   return cli.del_cliente(id)

@main.route('/clientes/e/<int:id>', methods = ['POST','GET'])
@login_required
def edit_cliente(id):
   return cli.edit_cliente(id)

@main.route('/funcionarios', methods=['GET', 'POST'])
@login_required
def funcionarios():
   return fun.funcionarios()

@main.route('/funcionarios/d/<int:id>', methods = ['POST','GET'])
@login_required
def del_funcionario(id):
   return fun.del_funcionario(id)

@main.route('/funcionarios/e/<int:id>', methods = ['POST','GET'])
@login_required
def edit_funcionario(id):
   return fun.edit_funcionario(id)