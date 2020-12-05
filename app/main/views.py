from . import main
from flask_login import login_required
from .view import index as ind
from .view import usuario as usr
from .view import cliente as cli
from .view import servico as ser
from .view import funcionario as fun
from .view import fornecedor as forn
from .view import tipo_quantidade as tpq
from .view import produto as pro

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
   return usr.main()

@main.route('/usuarios/d/<int:id>', methods = ['POST','GET'])
@login_required
def del_usuario(id):
   return usr.deletar(id)

@main.route('/usuarios/e/<int:id>', methods = ['POST','GET'])
@login_required
def edit_usuario(id):
   return usr.editar(id)

@main.route('/clientes', methods=['GET', 'POST'])
@login_required
def clientes():
   return cli.main()

@main.route('/clientes/d/<int:id>', methods = ['POST','GET'])
@login_required
def del_cliente(id):
   return cli.deletar(id)

@main.route('/clientes/e/<int:id>', methods = ['POST','GET'])
@login_required
def edit_cliente(id):
   return cli.editar(id)

@main.route('/funcionarios', methods=['GET', 'POST'])
@login_required
def funcionarios():
   return fun.main()

@main.route('/funcionarios/d/<int:id>', methods = ['POST','GET'])
@login_required
def del_funcionario(id):
   return fun.deletar(id)

@main.route('/funcionarios/e/<int:id>', methods = ['POST','GET'])
@login_required
def edit_funcionario(id):
   return fun.editar(id)

@main.route('/fornecedores', methods=['GET', 'POST'])
@login_required
def fornecedores():
   return forn.main()

@main.route('/fornecedores/d/<int:id>', methods = ['POST','GET'])
@login_required
def del_fornecedor(id):
   return forn.deletar(id)

@main.route('/fornecedores/e/<int:id>', methods = ['POST','GET'])
@login_required
def edit_fornecedor(id):
   return forn.editar(id)

@main.route('/tipos_quantidade', methods=['GET', 'POST'])
@login_required
def tipos_quantidade():
   return tpq.main()

@main.route('/tipos_quantidade/d/<int:id>', methods = ['POST','GET'])
@login_required
def del_tipos_quantidade(id):
   return tpq.deletar(id)

@main.route('/tipos_quantidade/e/<int:id>', methods = ['POST','GET'])
@login_required
def edit_tipos_quantidade(id):
   return tpq.editar(id)

@main.route('/produtos', methods=['GET', 'POST'])
@login_required
def produtos():
   return pro.main()

@main.route('/produtos/d/<int:id>', methods = ['POST','GET'])
@login_required
def del_produto(id):
   return pro.deletar(id)

@main.route('/produtos/e/<int:id>', methods = ['POST','GET'])
@login_required
def edit_produto(id):
   return pro.editar(id)