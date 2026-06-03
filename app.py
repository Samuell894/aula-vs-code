from flask import Flask, request, jsonify

app = Flask(__name__)

# Simulando um banco de dados com dicionários para ter IDs fixos
usuarios = [
    {"id": 0, "nome": "Admin", "email": "admin@email.com"}
]

# GET - listar usuários
@app.route('/usuarios', methods=['GET'])
def listar_usuarios():
    return jsonify(usuarios), 200

# POST - criar usuário
@app.route('/usuarios', methods=['POST'])
def criar_usuario():
    dados = request.get_json()
    
    # Gerar um novo ID baseado no último da lista
    novo_id = usuarios[-1]['id'] + 1 if usuarios else 0
    dados['id'] = novo_id
    
    usuarios.append(dados)
    return jsonify({"mensagem": "Usuário criado!", "usuario": dados}), 201

# PUT - atualizar usuário
@app.route('/usuarios/<int:id>', methods=['PUT'])
def atualizar_usuario(id):
    dados = request.get_json()
    
    # Procura o usuário pelo ID real, não pela posição na lista
    for usuario in usuarios:
        if usuario['id'] == id:
            usuario.update(dados)
            return jsonify({"mensagem": "Atualizado com sucesso!", "usuario": usuario}), 200
            
    return jsonify({"erro": "Usuário não encontrado"}), 404

# DELETE - deletar usuário
@app.route('/usuarios/<int:id>', methods=['DELETE'])
def deletar_usuario(id):
    global usuarios
    # Filtra a lista mantendo apenas quem NÃO tem o ID informado
    usuarios_filtrados = [u for u in usuarios if u['id'] != id]
    
    if len(usuarios_filtrados) < len(usuarios):
        usuarios = usuarios_filtrados
        return jsonify({"mensagem": "Usuário deletado!"}), 200
    
    return jsonify({"erro": "Usuário não encontrado"}), 404

if __name__ == '__main__':
    app.run(debug=True)