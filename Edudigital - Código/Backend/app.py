from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3

app = Flask(__name__)
CORS(app)


# ---------------------------------
# CONEXÃO COM O BANCO
# ---------------------------------

def get_db_connection():
    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row
    return conn


# ---------------------------------
# CRIAR TABELAS
# ---------------------------------

def criar_tabelas():

    with get_db_connection() as conn:

        # tabela usuarios
        conn.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            email TEXT NOT NULL,
            senha TEXT NOT NULL
        )
        """)

        # tabela licoes
        conn.execute("""
        CREATE TABLE IF NOT EXISTS licoes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo TEXT NOT NULL
        )
        """)

        # tabela exercicios
        conn.execute("""
        CREATE TABLE IF NOT EXISTS exercicios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            pergunta TEXT NOT NULL,
            resposta TEXT NOT NULL,
            licao_id INTEGER,
            FOREIGN KEY (licao_id) REFERENCES licoes(id)
        )
        """)

        # tabela progresso
        conn.execute("""
        CREATE TABLE IF NOT EXISTS progresso (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario_id INTEGER,
            pontuacao INTEGER,
            FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
        )
        """)

        conn.commit()


criar_tabelas()


# ---------------------------------
# ROTA INICIAL
# ---------------------------------

@app.route("/")
def home():

    return jsonify({
        "mensagem": "API Flask rodando 🚀"
    })


# ---------------------------------
# USUÁRIOS
# ---------------------------------

@app.route("/usuarios", methods=["POST"])
def criar_usuario():

    dados = request.get_json()

    if not dados or "nome" not in dados or "email" not in dados or "senha" not in dados:
        return jsonify({"erro": "Nome, email e senha são obrigatórios"}), 400

    nome = dados["nome"]
    email = dados["email"]
    senha = dados["senha"]

    if nome == "" or email == "" or senha == "":
        return jsonify({"erro": "Nome, email e senha são obrigatórios"}), 400


    with get_db_connection() as conn:

        usuarios = conn.execute(
            "SELECT * FROM usuarios"
        ).fetchall()

    users = [dict(u) for u in usuarios]

    for i in range(len(users)):
        if email == users[i]["email"]:
            return jsonify({"erro": "Email já cadastrado"})

    with get_db_connection() as conn:

        cursor = conn.cursor()

        cursor.execute(
            "INSERT INTO usuarios (nome, email, senha) VALUES (?, ?, ?)",
            (nome, email, senha)
        )

        conn.commit()

    return jsonify({
        "mensagem": "Usuário criado com sucesso"
    }), 201

@app.route("/usuarios", methods=["GET"])
def listar_usuarios():

    with get_db_connection() as conn:

        usuarios = conn.execute(
            "SELECT * FROM usuarios"
        ).fetchall()

    return jsonify([dict(u) for u in usuarios])


@app.route("/usuarios/<int:id>", methods=["GET"])
def buscar_usuario(id):

    with get_db_connection() as conn:

        usuario = conn.execute(
                    "SELECT * FROM usuarios WHERE id = ?",
                    (id,)
                ).fetchone()

    if usuario is None:
        return jsonify({"erro": "Usuário não encontrado"}), 404

    return jsonify(dict(usuario))


@app.route("/usuarios/<int:id>", methods=["PUT"])
def atualizar_usuario(id):

    dados = request.get_json()

    with get_db_connection() as conn:

        usuario = conn.execute(
            "SELECT * FROM usuarios WHERE id = ?",
            (id,)
        ).fetchone()

        if not usuario:
            return jsonify({"erro": "Usuário não encontrado"}), 404
        
        user = dict(usuario)
        print(user)
        
        usuarios = conn.execute(
            "SELECT * FROM usuarios"
            ).fetchall()

        users = [dict(u) for u in usuarios]

        for i in range(len(users)):
            if dados["email"] == users[i]["email"] and users[i]["id"] != id:
                return jsonify({"erro": "Email já cadastrado"})

        conn.execute(
            "UPDATE usuarios SET nome = ?, email = ?, senha = ? WHERE id = ?",
            (dados["nome"], dados["email"], dados["senha"], id)
        )

        conn.commit()

    return jsonify({"mensagem": "Usuário atualizado"})


@app.route("/usuarios/<int:id>", methods=["DELETE"])
def deletar_usuario(id):

    with get_db_connection() as conn:

        usuario = conn.execute(
            "SELECT id FROM usuarios WHERE id = ?",
            (id,)
        ).fetchone()

        if not usuario:
            return jsonify({"erro": "Usuário não encontrado"}), 404

        conn.execute(
            "DELETE FROM usuarios WHERE id = ?",
            (id,)
        )

        conn.commit()

    return jsonify({"mensagem": "Usuário deletado"})


# ---------------------------------
# LIÇÕES
# ---------------------------------

@app.route("/licoes", methods=["GET"])
def listar_licoes():

    with get_db_connection() as conn:

        licoes = conn.execute(
            "SELECT * FROM licoes"
        ).fetchall()

    return jsonify([dict(l) for l in licoes])


@app.route("/licoes/<int:id>", methods=["GET"])
def exercicios_da_licao(id):

    with get_db_connection() as conn:

        exercicios = conn.execute(
            "SELECT * FROM exercicios WHERE licao_id = ?",
            (id,)
        ).fetchall()

    return jsonify([dict(e) for e in exercicios])


# ---------------------------------
# RESPONDER EXERCÍCIO
# ---------------------------------

@app.route("/responder", methods=["POST"])
def responder():

    dados = request.get_json()

    exercicio_id = dados["exercicio_id"]
    resposta_usuario = dados["resposta"]
    usuario_id = dados["usuario_id"]

    with get_db_connection() as conn:

        exercicio = conn.execute(
            "SELECT resposta FROM exercicios WHERE id = ?",
            (exercicio_id,)
        ).fetchone()

        if not exercicio:
            return jsonify({"erro": "Exercício não encontrado"}), 404

        resposta_correta = exercicio["resposta"]

        if resposta_usuario == resposta_correta:
            pontuacao = 10
            correto = True
        else:
            pontuacao = 0
            correto = False

        conn.execute(
            "INSERT INTO progresso (usuario_id, pontuacao) VALUES (?, ?)",
            (usuario_id, pontuacao)
        )

        conn.commit()

    return jsonify({
        "correto": correto,
        "pontuacao": pontuacao
    })


# ---------------------------------
# PROGRESSO DO USUÁRIO
# ---------------------------------

@app.route("/progresso/<int:usuario_id>", methods=["GET"])
def progresso(usuario_id):

    with get_db_connection() as conn:

        registros = conn.execute(
            "SELECT pontuacao FROM progresso WHERE usuario_id = ?",
            (usuario_id,)
        ).fetchall()

    total = 0

    for r in registros:
        total += r["pontuacao"]

    return jsonify({
        "pontuacao_total": total
    })


# ---------------------------------
# CRIAR LIÇÃO
# ---------------------------------

@app.route("/licoes", methods=["POST"])
def criar_licao():

    dados = request.get_json()

    titulo = dados["titulo"]

    with get_db_connection() as conn:

        cursor = conn.cursor()

        cursor.execute(
            "INSERT INTO licoes (titulo) VALUES (?)",
            (titulo,)
        )

        conn.commit()

        novo_id = cursor.lastrowid

    return jsonify({
        "id": novo_id,
        "titulo": titulo
    }), 201


# ---------------------------------
# CRIAR EXERCÍCIO
# ---------------------------------

@app.route("/exercicios", methods=["POST"])
def criar_exercicio():

    dados = request.get_json()

    pergunta = dados["pergunta"]
    resposta = dados["resposta"]
    licao_id = dados["licao_id"]

    with get_db_connection() as conn:

        cursor = conn.cursor()

        cursor.execute(
            "INSERT INTO exercicios (pergunta, resposta, licao_id) VALUES (?, ?, ?)",
            (pergunta, resposta, licao_id)
        )

        conn.commit()

        novo_id = cursor.lastrowid

    return jsonify({
        "id": novo_id,
        "pergunta": pergunta
    }), 201

# ---------------------------------
# LOGIN
# ---------------------------------

@app.route("/login", methods=["POST"])
def login():

    dados = request.get_json()

    if not dados or "email" not in dados or "senha" not in dados:
        return jsonify({"erro": "Email e senha são obrigatórios"}), 400
    
    email = dados["email"]
    senha = dados["senha"]

    if email == "" or senha == "":
        return jsonify({"erro": "Email e senha são obrigatórios"}), 400

    
    with get_db_connection() as conn:

        usuario = conn.execute(
            "SELECT * FROM usuarios WHERE email = ?",
            (email,)
        ).fetchone()

    if usuario is None:
        return jsonify({"erro": "Usuário não encontrado"}), 404
    
    user = dict(usuario)

    if dados["senha"] != user["senha"]:
        return jsonify({"erro": "Email ou senha incorretos"})
    
    return jsonify({
        "id": user["id"],
        "mensagem": "Login realizado com sucesso",
        "usuario": user["nome"]
    })


# ---------------------------------
# INICIAR SERVIDOR
# ---------------------------------

if __name__ == "__main__":
    app.run(debug=True)