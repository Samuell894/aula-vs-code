from flask import Flask, request, jsonify

app = Flask(__name__)

# "Banco de dados" fake
usuarios = []

# GET - listar usuários
@app.route('/usuarios', methods=['GET'])
def listar_usuarios():
    return jsonify(usuarios)

# POST - criar usuário
@app.route('/usuarios', methods=['POST'])
def criar_usuario():
    dados = request.get_json()
    usuarios.append(dados)
    return jsonify({"mensagem": "Usuário criado com sucesso!"})

# PUT - atualizar usuário
@app.route('/usuarios/<int:id>', methods=['PUT'])
def atualizar_usuario(id):
    dados = request.get_json()
    if id < len(usuarios):
        usuarios[id] = dados
        return jsonify({"mensagem": "Usuário atualizado!"})
    return jsonify({"erro": "Usuário não encontrado"}), 404

# DELETE - deletar usuário
@app.route('/usuarios/<int:id>', methods=['DELETE'])
def deletar_usuario(id):
    if id < len(usuarios):
        usuarios.pop(id)
        return jsonify({"mensagem": "Usuário deletado!"})
    return jsonify({"erro": "Usuário não encontrado"}), 404

if __name__ == '__main__':
    app.run(debug=True)