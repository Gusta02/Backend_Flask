from flask import Blueprint, redirect, render_template,current_app, jsonify, request,session
import os
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from sqlalchemy.ext.declarative import declarative_base
from flask_admin.model import typefmt

from config import TEMPLATE_FOLDER



from ..models.produtos import ProdutoBasico,ProdutoDetalhe,MarcaProduto


  

admin_app = Blueprint("adminapp",__name__, 
        template_folder=os.path.join(TEMPLATE_FOLDER, "resources","templates","admin"), 
        static_folder=os.path.join(TEMPLATE_FOLDER, "resources", "static"))
    
Base = declarative_base()

current_app.config['FLASK_ADMIN_SWATCH'] = 'cosmo'


admin = Admin(current_app, name='HauszAdmin', template_mode='bootstrap3')



class BasicoView(ModelView):
    column_list = ('NomeProduto', 'EAN', 'DataInserido','EstoqueAtual','SaldoAtual')


#admin.add_view(BasicoView(ProdutoBasico, ))
#admin.add_view(BasicoView(ProdutoDetalhe, ))
#admin.add_view(BasicoView(MarcaProduto,))

@admin_app.route("/indexadmin", methods=["GET","POST"])
def home():
    return redirect("/admin")