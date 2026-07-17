from flask import Blueprint, render_template, request, redirect, url_for, session
from models.pesquisa import cadastrar_pesquisa

admin = Blueprint("admin", __name__)

@admin.route("/admin/nova-pesquisa", methods=["GET", "POST"])
def nova_pesquisa():

    if "user_cpf" not in session:
        return redirect(url_for("home"))

    if session.get("user_role") != "admin":
        return redirect(url_for("pesquisas"))

    if request.method == "POST":

        titulo = request.form["titulo"]
        descricao = request.form["descricao"]
        imagem = request.form["imagem"]
        data_inicio = request.form["data_inicio"]
        data_fim = request.form["data_fim"]

        cadastrar_pesquisa(
            titulo,
            descricao,
            imagem,
            data_inicio,
            data_fim
        )

        return redirect(url_for("pesquisas"))

    return render_template("admin/nova_pesquisa.html")