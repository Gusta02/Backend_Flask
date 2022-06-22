from flask import Blueprint, render_template,current_app, jsonify, request
import os


from config import TEMPLATE_FOLDER


login = Blueprint("autenticacao",__name__, 
        template_folder=os.path.join(TEMPLATE_FOLDER, "resources", "templates"), 
        static_folder=os.path.join(TEMPLATE_FOLDER, "resources", "static"))
    


@login.route("/login", methods=["GET","POST"])
def login_usuario():
    return render_template("login.html")


@login.route("/cadastro", methods=["GET","POST"])
def cadastro():
    return render_template("cadastro.html")


@login.route("/recuperarsenha", methods=["GET","POST"])
def recuperar_senha():
    return render_template("recuperarsenha.html")