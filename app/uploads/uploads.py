from flask import Blueprint, render_template,current_app, jsonify, request, redirect, flash, url_for
import os
from werkzeug.utils import secure_filename
from flask import send_from_directory
import flask_excel as excel
from flask import abort

from ..controllers.consultascontroller import retorna_produtos_estoques
from ..uploads.factory import Produto
from config import basedir, patharquivos, ALLOWED_EXTENSIONS


UPLOAD_FOLDER = patharquivos + "\\uploadarquivos\\"

current_app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

uploads = Blueprint("uploads",__name__
        ,template_folder='templates',static_folder='static',static_url_path='/static/imagens')



def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@uploads.route('/uploads', methods=['GET', 'POST'])
def upload_file():
    try:
    #Verifica na requisição se existe algum arquivo
        if request.method == 'POST':
            try:
                if 'file' not in request.files:
                    flash('No file part')
                    return redirect(request.url)
                file = request.files['file']

                if file.filename == '':
                    flash('No selected file')
                    return redirect(request.url)
                if file and allowed_file(file.filename):
                    filename = secure_filename(file.filename)
                    file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))

                
            
                    return redirect(url_for('uploads.download_file', name=filename))
            except:
                abort(500)
        return render_template("upload.html")
    except:
        abort(500)

@uploads.route('/uploads/<name>') 
#Recebe paramento com nome do arquivo e retorna json para o layout
def download_file(name):
    try:
        brand = Produto(UPLOAD_FOLDER+name)
        dicts = brand.retorna_marca()
        print('chegou na função ~~ >',dicts)
        jsons = retorna_produtos_estoques(dicts)
        print(jsons)
    
        return render_template("informacoesestoque.html", produtos = jsons)
    except:
        abort(500)
  

@uploads.route("/exportrelatoriosaldos/<name>", methods=["GET","POST"])
def export_relatorio_saldo_produto(name):
    print(name)
    brand = Produto(UPLOAD_FOLDER+name)
    dicts = brand.retorna_marca()
    print('chegou na função ~~ >',dicts)
    jsons = retorna_produtos_estoques(dicts)
    return excel.make_response_from_array([x.items() for x in jsons], "csv",
                                          file_name="export_data")