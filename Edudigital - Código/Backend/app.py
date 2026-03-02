from flask import Flask, request, jsonify
from flask_cors import CORS  # Essencial para conectar com o Frontend
import sqlite3

app = Flask(__name__)
CORS(app)  # Libera o acesso para o seu Frontend

# 🔹 Conexão com o banco (usando contexto 'with' para maior segurança)
def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

# 🔹 Criar tabela automaticamente ao iniciar
def criar_tabela():
    with get_db_connection() as conn:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS usuarios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                email TEXT NOT NULL
            )
        ''')
        conn.commit()

criar_tabela()

# 🔹 Rota inicial
@app.route('/')
def home():
    return jsonify({"status": "online", "mensagem": "API Flask com SQLite rodando com sucesso! 🚀"})

# 🔹 Criar usuário (POST)
@app.route('/usuarios', methods=['POST'])
def criar_usuario():
    dados = request.get_json()
    
    # Validação básica de entrada
    if not dados or 'nome' not in dados or 'email' not in dados:
        return jsonify({"erro": "Dados obrigatórios: nome e email"}), 400

    nome = dados['nome']
    email = dados['email']

    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('INSERT INTO usuarios (nome, email) VALUES (?, ?)', (nome, email))
        conn.commit()
        novo_id = cursor.lastrowid

    return jsonify({"id": novo_id, "mensagem": "Usuário criado com sucesso"}), 201

# 🔹 Listar todos os usuários (GET)
@app.route('/usuarios', methods=['GET'])
def listar_usuarios():
    with get_db_connection() as conn:
        usuarios = conn.execute('SELECT * FROM usuarios').fetchall()
    
    return jsonify([dict(u) for u in usuarios])

# 🔹 Buscar usuário por ID (GET)
@app.route('/usuarios/<int:id>', methods=['GET'])
def buscar_usuario(id):
    with get_db_connection() as conn:
        usuario = conn.execute('SELECT * FROM usuarios WHERE id = ?', (id,)).fetchone()
    
    if usuario is None:
        return jsonify({"erro": f"Usuário com ID {id} não encontrado"}), 404

    return jsonify(dict(usuario))

# 🔹 Atualizar usuário (PUT)
@app.route('/usuarios/<int:id>', methods=['PUT'])
def atualizar_usuario(id):
    dados = request.get_json()
    
    with get_db_connection() as conn:
        # Verifica se existe antes de tentar atualizar
        usuario_existe = conn.execute('SELECT id FROM usuarios WHERE id = ?', (id,)).fetchone()
        if not usuario_existe:
            return jsonify({"erro": "Usuário não encontrado para atualização"}), 404

        conn.execute('UPDATE usuarios SET nome = ?, email = ? WHERE id = ?', 
                     (dados['nome'], dados['email'], id))
        conn.commit()

    return jsonify({"mensagem": "Usuário atualizado com sucesso"})

# 🔹 Deletar usuário (DELETE)
@app.route('/usuarios/<int:id>', methods=['DELETE'])
def deletar_usuario(id):
    with get_db_connection() as conn:
        # Verifica se existe antes de tentar deletar
        usuario_existe = conn.execute('SELECT id FROM usuarios WHERE id = ?', (id,)).fetchone()
        if not usuario_existe:
            return jsonify({"erro": "Não foi possível deletar: ID não encontrado"}), 404

        conn.execute('DELETE FROM usuarios WHERE id = ?', (id,))
        conn.commit()

    return jsonify({"mensagem": "Usuário deletado com sucesso"})

# 🔹 Rodar servidor
if __name__ == '__main__':
    app.run(debug=True)
