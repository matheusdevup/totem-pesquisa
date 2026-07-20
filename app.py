from flask import Flask, render_template, request, redirect, url_for, session

from models.funcionarios import consultar_funcionario
from models.pesquisa import consultar_pesquisas

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
    # Se o usuário JÁ estiver logado, exibe a tela de pesquisas direto na raiz '/'
    if "user_cpf" in session:
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

    # Se NÃO estiver logado e enviar o formulário de login (POST)
    if request.method == "POST":
        cpf = request.form.get("cpf", "")
        cpf = cpf.replace(".", "").replace("-", "")

        funcionario = consultar_funcionario(cpf)

        if funcionario:
            session["user_cpf"] = funcionario[1]
            session["user_nome"] = funcionario[2]
            session["user_role"] = funcionario[4]

            # Recarrega a própria raiz '/', que agora vai cair no bloco de usuário logado acima
            return redirect(url_for("home"))

        return render_template(
            "login.html",
            erro="CPF não encontrado."
        )

    # Se NÃO estiver logado e apenas acessar a página (GET), mostra a tela de login
    return render_template("login.html")


# ======================================================
# LOGOUT
# ======================================================
@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("home"))  # Volta para a raiz (tela de login)


# ======================================================
# EXECUÇÃO
# ======================================================
if __name__ == "__main__":
    app.run(debug=True)