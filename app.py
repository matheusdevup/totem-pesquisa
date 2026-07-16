from flask import Flask, render_template, request, redirect, url_for, session
from models.funcionarios import consultar_funcionario
from models.pesquisa import consultar_pesquisas
import os

app = Flask(__name__)
app.secret_key = "macpet_super_secret_key"  # Mantém a sessão segura

@app.route("/", methods=["GET", "POST"])
def home():
    # Se o usuário já estiver logado, redireciona direto para as pesquisas
    if "user_cpf" in session:
        return redirect(url_for("pesquisas"))

    if request.method == "POST":
        cpf_enviado = request.form.get("cpf")
        if cpf_enviado:
            cpf_limpo = cpf_enviado.replace(".", "").replace("-", "")
            funcionario = consultar_funcionario(cpf_limpo)
            print(funcionario)
            # Validação do Usuário
            funcionario = consultar_funcionario(cpf_limpo)

            if funcionario:
                session["user_cpf"] = funcionario[1]
                session["user_nome"] = funcionario[2]

                # Por enquanto vamos definir o perfil manualmente
                session["user_role"] = funcionario[4]

                return redirect(url_for("pesquisas"))
            else:
                print("CPF não cadastrado no sistema!")

    return render_template("login.html")


@app.route("/pesquisas")
def pesquisas():

    # Impede acessar a página sem login
    if "user_cpf" not in session:
        return redirect(url_for("home"))

    # Busca as pesquisas no banco
    pesquisas = consultar_pesquisas()

    # Dados do usuário logado
    usuario = {
        "nome": session.get("user_nome"),
        "role": session.get("user_role")
    }

    return render_template(
        "pesquisas.html",
        usuario=usuario,
        pesquisas=pesquisas
    )


@app.route("/logout")
def logout():
    session.clear()  # Limpa o login do navegador
    return redirect(url_for("home"))


if __name__ == "__main__":
    app.run(debug=True)