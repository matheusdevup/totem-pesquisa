from flask import Blueprint, render_template, request, redirect, url_for, session

import os
from werkzeug.utils import secure_filename

from models.pesquisa import (
    cadastrar_pesquisa,
    consultar_pesquisas
)


admin = Blueprint("admin", __name__)

@admin.route("/admin/nova_pesquisa", methods=["GET", "POST"])
def nova_pesquisa():

    if "user_cpf" not in session:
        return redirect(url_for("home"))

    if session.get("user_role") != "admin":
        return redirect(url_for("home"))

    if request.method == "POST":

        titulo = request.form["titulo"]
        descricao = request.form["descricao"]
        banner = request.files["banner"]
        data_inicio = request.form["data_inicio"]
        data_fim = request.form["data_fim"]

        nome_imagem = ""

        if banner and banner.filename != "":
            nome_imagem = secure_filename(banner.filename)

            caminho = os.path.join(
                "static",
                "img",
                nome_imagem
            )

            banner.save(caminho)

        cadastrar_pesquisa(
            titulo,
            descricao,
            nome_imagem,
            data_inicio,
            data_fim
        )

        return redirect(url_for("admin.lista_pesquisas"))




    return render_template("admin/nova_pesquisa.html")

@admin.route("/lista_pesquisas")
def lista_pesquisas():

    if "user_cpf" not in session:
        return redirect(url_for("home"))

    if session.get("user_role") != "admin":
        return redirect(url_for("home"))

    pesquisas = consultar_pesquisas()

    return render_template(
        "admin/lista_pesquisa.html",
        pesquisas=pesquisas
    )
