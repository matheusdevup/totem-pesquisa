from flask import Blueprint, render_template, request, redirect, url_for, session
from datetime import datetime
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
            caminho = os.path.join("static", "img", nome_imagem)
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

    # 1. Pega os parâmetros passados via URL
    termo_busca = request.args.get("busca", "").strip().lower()
    filtro_status = request.args.get("status", "todos").strip().lower()

    # 2. Busca todas as pesquisas no BD
    todas_pesquisas = consultar_pesquisas() or []

    # 3. Contadores gerais para os Cards (calculados sobre o total real)
    total = len(todas_pesquisas)
    ativas = 0
    programadas = 0
    encerradas = 0

    for p in todas_pesquisas:
        # Tenta identificar o status no banco (seja tupla, lista ou dicionário)
        if isinstance(p, (tuple, list)):
            # Se a tupla tiver status em algum índice superior ou assume 'ativa' por padrão
            st = str(p[7]).lower() if len(p) > 7 and p[7] else "ativa"
        else:
            st = str(getattr(p, 'status', 'ativa')).lower()

        if st in ['ativa', 'disponivel', 'publicada']:
            ativas += 1
        elif st in ['programada', 'rascunho']:
            programadas += 1
        elif st in ['encerrada', 'respondida']:
            encerradas += 1

    stats = {
        'total': total,
        'ativas': ativas,
        'programadas': programadas,
        'encerradas': encerradas
    }

    # 4. Aplica os Filtros de Busca e Status na lista da tabela
    pesquisas_filtradas = []
    for p in todas_pesquisas:
        if isinstance(p, (tuple, list)):
            titulo = str(p[1]).lower() if len(p) > 1 else ""
            descricao = str(p[2]).lower() if len(p) > 2 else ""
            # Pega o status real se existir no índice 7, senão define como 'ativa'
            st_item = str(p[7]).lower() if len(p) > 7 and p[7] else "ativa"
        else:
            titulo = str(getattr(p, 'titulo', '')).lower()
            descricao = str(getattr(p, 'descricao', '')).lower()
            st_item = str(getattr(p, 'status', 'ativa')).lower()

        # Condição de busca textual (no título ou na descrição)
        match_busca = (termo_busca in titulo) or (termo_busca in descricao) if termo_busca else True

        # Condição de status
        match_status = True
        if filtro_status != 'todos':
            if filtro_status in ['ativa', 'publicada']:
                match_status = st_item in ['ativa', 'disponivel', 'publicada']
            else:
                match_status = (filtro_status in st_item)

        if match_busca and match_status:
            pesquisas_filtradas.append(p)

    # 5. Paginação sobre a lista filtrada
    PER_PAGE = 5
    page = request.args.get('page', 1, type=int)
    inicio = (page - 1) * PER_PAGE
    fim = inicio + PER_PAGE
    pesquisas_pagina = pesquisas_filtradas[inicio:fim]

    return render_template(
        "admin/lista_pesquisa.html",
        pesquisas=pesquisas_pagina,
        stats=stats,
        total_pesquisas=len(pesquisas_filtradas),
        per_page=PER_PAGE,
        page=page,
        termo_busca=request.args.get("busca", ""),
        filtro_status=filtro_status
    )