from flask import Flask, jsonify

from controllers.user_controller import login, signup
from controllers.chatpdf_controller import upload_file, chat_message

app = Flask(__name__)

@app.route('/')
def index():
  return jsonify({"response": "Backend Oxe Learning"}), 200

# Rota de Cadastro de usuário
app.add_url_rule('/signUp', 'signup', signup, methods=['POST'])

# Rota de Login
app.add_url_rule('/login', 'login', login, methods=['POST'])

# Endpoint para upload de arquivos
app.add_url_rule('/uploadFile', 'uploadFile', upload_file, methods=['POST'])

# Endpoint para Enviar perguntas
app.add_url_rule('/chatMessage', 'chatMessage', chat_message, methods=['POST'])

# Inicia a API
app.run(host='0.0.0.0')
