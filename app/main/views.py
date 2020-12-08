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
from .view import equipamento as equ
from .view import compra as com
from .view import tipos_servico as tps
from .view import cad_servico as cser
from .view import agendar as age

headers = {
   'Content-Type': 'application/json'
}

@main.route('/')
def index():
   return ind.index()

@main.route('/agendar')
def agendar():
   return age.main()

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

@main.route('/equipamentos', methods=['GET', 'POST'])
@login_required
def equipamentos():
   return equ.main()

@main.route('/equipamentos/d/<int:id>', methods = ['POST','GET'])
@login_required
def del_equipamento(id):
   return equ.deletar(id)

@main.route('/equipamentos/e/<int:id>', methods = ['POST','GET'])
@login_required
def edit_equipamento(id):
   return equ.editar(id)

@main.route('/compras', methods=['GET', 'POST'])
@login_required
def compras():
   return com.main()

@main.route('/compras/d/<int:id>', methods = ['POST','GET'])
@login_required
def del_compra(id):
   return com.deletar(id)

@main.route('/compras/e/<int:id>', methods = ['POST','GET'])
@login_required
def edit_compra(id):
   return com.editar(id)

@main.route('/tipos_servico', methods=['GET', 'POST'])
@login_required
def tipos_servico():
   return tps.main()

@main.route('/tipos_servico/d/<int:id>', methods = ['POST','GET'])
@login_required
def del_tipo_servico(id):
   return tps.deletar(id)

@main.route('/tipos_servico/e/<int:id>', methods = ['POST','GET'])
@login_required
def edit_tipo_servico(id):
   return tps.editar(id)

@main.route('/cad_servicos', methods=['GET', 'POST'])
@login_required
def cad_servicos():
   return cser.main()

@main.route('/cad_servicos/d/<int:id>', methods = ['POST','GET'])
@login_required
def del_cad_servico(id):
   return cser.deletar(id)

@main.route('/cad_servicos/e/<int:id>', methods = ['POST','GET'])
@login_required
def edit_cad_servico(id):
   return cser.editar(id)