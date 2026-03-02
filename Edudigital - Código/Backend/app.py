from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

# 🔹 Conexão com o banco
def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

# 🔹 Criar tabela automaticamente
def criar_tabela():
    conn = get_db_connection()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            email TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

criar_tabela()

# 🔹 Rota inicial
@app.route('/')
def home():
    return "API funcionando 🚀"

# 🔹 Criar usuário
@app.route('/usuarios', methods=['POST'])
def criar_usuario():
    dados = request.get_json()

    nome = dados['nome']
    email = dados['email']

    conn = get_db_connection()
    conn.execute('INSERT INTO usuarios (nome, email) VALUES (?, ?)', (nome, email))
    conn.commit()
    conn.close()

    return jsonify({"mensagem": "Usuário criado com sucesso"}), 201

# 🔹 Listar todos os usuários
@app.route('/usuarios', methods=['GET'])
def listar_usuarios():
    conn = get_db_connection()
    usuarios = conn.execute('SELECT * FROM usuarios').fetchall()
    conn.close()

    return jsonify([dict(u) for u in usuarios])

# 🔹 Buscar usuário por ID
@app.route('/usuarios/<int:id>', methods=['GET'])
def buscar_usuario(id):
    conn = get_db_connection()
    usuario = conn.execute('SELECT * FROM usuarios WHERE id = ?', (id,)).fetchone()
    conn.close()

    if usuario is None:
        return jsonify({"erro": "Usuário não encontrado"}), 404

    return jsonify(dict(usuario))

# 🔹 Atualizar usuário
@app.route('/usuarios/<int:id>', methods=['PUT'])
def atualizar_usuario(id):
    dados = request.get_json()
    nome = dados['nome']
    email = dados['email']

    conn = get_db_connection()
    conn.execute('UPDATE usuarios SET nome = ?, email = ? WHERE id = ?', (nome, email, id))
    conn.commit()
    conn.close()

    return jsonify({"mensagem": "Usuário atualizado com sucesso"})

# 🔹 Deletar usuário
@app.route('/usuarios/<int:id>', methods=['DELETE'])
def deletar_usuario(id):
    conn = get_db_connection()
    conn.execute('DELETE FROM usuarios WHERE id = ?', (id,))
    conn.commit()
    conn.close()

    return jsonify({"mensagem": "Usuário deletado com sucesso"})

# 🔹 Rodar servidor
if __name__ == '__main__':
    app.run(debug=True)