from flask import Flask, render_template, request, redirect, url_for, session

from models.funcionarios import consultar_funcionario
from models.pesquisa import consultar_pesquisas

from routes.admin import admin

app = Flask(__name__)
app.secret_key = "macpet_super_secret_key"

# Registro dos Blueprints
app.register_blueprint(admin)


# ======================================================
# LOGIN
# ======================================================

@app.route("/", methods=["GET", "POST"])
def home():

    # Se já estiver logado, vai direto para pesquisas
    if "user_cpf" in session:
        return redirect(url_for("pesquisas"))

    if request.method == "POST":

        cpf = request.form.get("cpf", "")
        cpf = cpf.replace(".", "").replace("-", "")

        funcionario = consultar_funcionario(cpf)

        if funcionario:

            session["user_cpf"] = funcionario[1]
            session["user_nome"] = funcionario[2]
            session["user_role"] = funcionario[4]

            return redirect(url_for("pesquisas"))

        return render_template(
            "login.html",
            erro="CPF não encontrado."
        )

    return render_template("login.html")


# ======================================================
# LISTA DE PESQUISAS
# ======================================================

@app.route("/pesquisas")
def pesquisas():

    if "user_cpf" not in session:
        return redirect(url_for("home"))

    usuario = {
        "nome": session.get("user_nome"),
        "role": session.get("user_role")
    }

    pesquisas = consultar_pesquisas()

    return render_template(
        "pesquisas.html",
        usuario=usuario,
        pesquisas=pesquisas
    )


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