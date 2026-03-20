from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3

app = Flask(__name__)
CORS(app)

DATABASE = "database.db"

# ---------------------------------
# CONEXÃO COM BANCO
# ---------------------------------

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


# ---------------------------------
# CRIAR TABELAS
# ---------------------------------

def criar_tabelas():

    with get_db_connection() as conn:

        conn.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            senha TEXT NOT NULL
        )
        """)

        conn.execute("""
        CREATE TABLE IF NOT EXISTS licoes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo TEXT NOT NULL
        )
        """)

        conn.execute("""
        CREATE TABLE IF NOT EXISTS exercicios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            pergunta TEXT NOT NULL,
            resposta TEXT NOT NULL,
            licao_id INTEGER,
            FOREIGN KEY (licao_id) REFERENCES licoes(id)
        )
        """)

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
# ROTA TESTE
# ---------------------------------

@app.route("/")
def home():
    return jsonify({"mensagem": "API Flask rodando 🚀"})


# ---------------------------------
# CRIAR USUÁRIO
# ---------------------------------

@app.route("/usuarios", methods=["POST"])
def criar_usuario():

    dados = request.get_json()

    if not dados:
        return jsonify({"erro": "Dados não enviados"}), 400

    nome = dados.get("nome")
    email = dados.get("email")
    senha = dados.get("senha")

    if not nome or not email or not senha:
        return jsonify({"erro": "Nome, email e senha são obrigatórios"}), 400

    with get_db_connection() as conn:

        usuario_existente = conn.execute(
            "SELECT * FROM usuarios WHERE email = ?",
            (email,)
        ).fetchone()

        if usuario_existente:
            return jsonify({"erro": "Email já cadastrado"}), 400

        cursor = conn.cursor()

        cursor.execute(
            "INSERT INTO usuarios (nome, email, senha) VALUES (?, ?, ?)",
            (nome, email, senha)
        )

        conn.commit()

    return jsonify({"mensagem": "Usuário criado com sucesso"}), 201


# ---------------------------------
# LISTAR USUÁRIOS
# ---------------------------------

@app.route("/usuarios", methods=["GET"])
def listar_usuarios():

    with get_db_connection() as conn:

        usuarios = conn.execute(
            "SELECT id, nome, email FROM usuarios"
        ).fetchall()

    return jsonify([dict(u) for u in usuarios])


# ---------------------------------
# BUSCAR USUÁRIO
# ---------------------------------

@app.route("/usuarios/<int:id>", methods=["GET"])
def buscar_usuario(id):

    with get_db_connection() as conn:

        usuario = conn.execute(
            "SELECT id, nome, email FROM usuarios WHERE id = ?",
            (id,)
        ).fetchone()

    if usuario is None:
        return jsonify({"erro": "Usuário não encontrado"}), 404

    return jsonify(dict(usuario))


# ---------------------------------
# ATUALIZAR USUÁRIO
# ---------------------------------

@app.route("/usuarios/<int:id>", methods=["PUT"])
def atualizar_usuario(id):

    dados = request.get_json()

    nome = dados.get("nome")
    email = dados.get("email")
    senha = dados.get("senha")

    if not nome or not email or not senha:
        return jsonify({"erro": "Dados incompletos"}), 400

    with get_db_connection() as conn:

        usuario = conn.execute(
            "SELECT * FROM usuarios WHERE id = ?",
            (id,)
        ).fetchone()

        if not usuario:
            return jsonify({"erro": "Usuário não encontrado"}), 404
        
        user = dict(usuario)
        
        usuarios = conn.execute(
            "SELECT * FROM usuarios"
            ).fetchall()

        email_existente = conn.execute(
            "SELECT * FROM usuarios WHERE email = ? AND id != ?",
            (email, id)
        ).fetchone()

        if email_existente:
            return jsonify({"erro": "Email já cadastrado"}), 400

        conn.execute(
            "UPDATE usuarios SET nome = ?, email = ?, senha = ? WHERE id = ?",
            (nome, email, senha, id)
        )

        conn.commit()

    return jsonify({"mensagem": "Usuário atualizado"})


# ---------------------------------
# DELETAR USUÁRIO
# ---------------------------------

@app.route("/usuarios/<int:id>", methods=["DELETE"])
def deletar_usuario(id):

    with get_db_connection() as conn:

        usuario = conn.execute(
            "SELECT * FROM usuarios WHERE id = ?",
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
# LOGIN
# ---------------------------------

@app.route("/login", methods=["POST"])
def login():

    dados = request.get_json()

    email = dados.get("email")
    senha = dados.get("senha")

    if not email or not senha:
        return jsonify({"erro": "Email e senha são obrigatórios"}), 400

    with get_db_connection() as conn:

        usuario = conn.execute(
            "SELECT * FROM usuarios WHERE email = ?",
            (email,)
        ).fetchone()

    if usuario is None:
        return jsonify({"erro": "Usuário não encontrado"}), 404

    if senha != usuario["senha"]:
        return jsonify({"erro": "Senha incorreta"}), 401

    return jsonify({
        "id": usuario["id"],
        "usuario": usuario["nome"],
        "mensagem": "Login realizado com sucesso"
    })


# ---------------------------------
# INICIAR SERVIDOR
# ---------------------------------

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)
