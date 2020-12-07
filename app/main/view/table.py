# import things
from flask_table import Table, Col

# Declare your table
class ItemTable(Table):
    classes = ['table', 'table-striped', 'table-bordered']
    table_id = 'tabela2'
    id = Col('ID')
    descricao = Col('Descrição')
    acao = Col('Ação')

# Get some objects
class Item(object):
    def __init__(self, id, descricao, acao):
        self.id = id
        self.descricao = descricao
        self.acao = acao