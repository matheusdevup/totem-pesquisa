from flask import Flask, render_template, request, redirect, url_for, session

from models.funcionarios import consultar_funcionario
from models.opcoes import consultar_opcoes
from models.pesquisa import (
    consultar_pesquisas,
    consultar_pesquisa,
    consultar_pesquisas_respondidas_usuario,
    registrar_resposta_usuario
)
from database.connection import conectar

from routes.admin import admin

app = Flask(__name__)
app.secret_key = "macpet_super_secret_key"

# Registro dos Blueprints
app.register_blueprint(admin)


# ======================================================
# PÁGINA INICIAL (RAIZ DO SITE)
# ======================================================
@app.route("/", methods=["GET", "POST"])
def home():
    # Se o usuário JÁ estiver logado, exibe a tela de pesquisas
    if "user_cpf" in session:
        cpf_logado = session.get("user_cpf")

        usuario = {
            "nome": session.get("user_nome"),
            "role": session.get("user_role")
        }

        pesquisas = consultar_pesquisas()
        respondidas_ids = consultar_pesquisas_respondidas_usuario(cpf_logado)

        return render_template(
            "pesquisas.html",
            usuario=usuario,
            pesquisas=pesquisas,
            respondidas_ids=respondidas_ids
        )

    # Se NÃO estiver logado e enviar o formulário de login (POST)
    if request.method == "POST":
        cpf = request.form.get("cpf", "")
        cpf = cpf.replace(".", "").replace("-", "")

        funcionario = consultar_funcionario(cpf)

        if funcionario:
            session["user_cpf"] = funcionario[1]
            session["user_nome"] = funcionario[2]
            session["user_role"] = funcionario[4]

            return redirect(url_for("home"))

        return render_template(
            "login.html",
            erro="CPF não encontrado."
        )

    return render_template("login.html")


# ======================================================
# ROTA: EXIBIR PERGUNTAS DA PESQUISA
# ======================================================
@app.route("/responder_pesquisa/<int:id_pesquisa>")
def responder_pesquisa(id_pesquisa):
    if "user_cpf" not in session:
        return redirect(url_for("home"))

    pesquisa = consultar_pesquisa(id_pesquisa)
    if not pesquisa:
        return redirect(url_for("home"))

    # Busca a primeira pergunta e as opções no banco de dados
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute(
        "SELECT * FROM perguntas WHERE pesquisa_id = ? ORDER BY ordem ASC LIMIT 1",
        (id_pesquisa,)
    )
    pergunta = cursor.fetchone()

    opcoes = []
    if pergunta:
        opcoes = consultar_opcoes(pergunta[0])

    conexao.close()

    return render_template(
        "responder_pesquisa.html",
        pesquisa=pesquisa,
        pergunta=pergunta,
        opcoes=opcoes,
        pergunta_atual_numero=1,
        total_perguntas=6
    )


# ======================================================
# ROTA: SALVAR RESPOSTAS DA PESQUISA
# ======================================================
@app.route("/salvar_respostas/<int:id_pesquisa>", methods=["POST"])
def salvar_respostas(id_pesquisa):
    if "user_cpf" not in session:
        return redirect(url_for("home"))

    cpf_logado = session.get("user_cpf")

    # Registra que este CPF respondeu a esta pesquisa
    registrar_resposta_usuario(id_pesquisa, cpf_logado)

    # Redireciona de volta para a Home
    return redirect(url_for("home"))


# ======================================================
# LOGOUT
# ======================================================
@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("home"))


# ======================================================
# EXECUÇÃO
# ======================================================
if __name__ == "__main__":
    app.run(debug=True)