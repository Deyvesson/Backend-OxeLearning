import json, os, json
import urllib.request as urlRequest
from flask import jsonify, request
from models.firebase import initialize_firebase

#iniciando conexão com o firebase
firebase = initialize_firebase()
auth = firebase.auth()


def login():
  if request.form.get('user') and request.form.get('password'):
    try:
      # Autentica o usuário com email e senha
      user = auth.sign_in_with_email_and_password(request.form.get('user'),
                                                  request.form.get('password'))
      return jsonify({
        "message": "Usuário logado com sucesso",
        "user": user
      }), 200
    except Exception as e:
      error_data = json.loads(e.args[1])
      #Se o erro for de usuário ou senha incorretos
      if error_data['error']['message'] == 'EMAIL_NOT_FOUND' or error_data[
          'error']['message'] == 'INVALID_PASSWORD':
        return jsonify({'message': 'Usuário ou Senha incorretos.'}), 401
      else:
        return jsonify({'message': f"Erro desconhecido: {e}"}), 500
  else:
    return jsonify({"message": "User ou Password não enviados"}), 400


def signup():
  if request.form.get('user') and request.form.get('password'):
    try:
      # Cria o usuário com email e senha
      user = auth.create_user_with_email_and_password(
        request.form.get('user'), request.form.get('password'))
      return jsonify({
        "message": "Login criado com sucesso",
        "user": user
      }), 201
    except Exception as e:
      error_data = json.loads(e.args[1])
      # Se o erro for de Usuário já existente
      if error_data['error']['message'] == 'EMAIL_EXISTS':
        return jsonify({"message": "Usuário já cadastrado"}), 400
      else:
        return jsonify({"message": f"Erro desconhecido: {e}"}), 500
  else:
    return jsonify({"message": "User ou Password não enviados"}), 400


def redifinirSenha():
  data = request.get_json()
  try:
    auth.send_password_reset_email(data.get('email'))
    return jsonify({
      "message": "Email enviado com sucesso!",
    }), 200
  except Exception as e:
    error_data = json.loads(e.args[1])
    #Se o erro for de usuário ou senha incorretos
    if error_data['error']['message'] == 'EMAIL_NOT_FOUND':
      return jsonify({'message': 'Email não cadastrado!'}), 401
    else:
      return jsonify({'message': f"Erro desconhecido: {e}"}), 500


def changePassword():
  data = request.get_json()
  # Substitua YOUR_API_KEY pelo seu chave de API do Firebase
  apiKey = os.environ['API_KEY']
  idToken = data.get('token')
  newPassword = data.get('new_password')

  url = f"https://identitytoolkit.googleapis.com/v1/accounts:update?key={apiKey}"
  headers = {'Content-Type': 'application/json'}

  payload = {
    "idToken": idToken,
    "password": newPassword,
  }
  data = json.dumps(payload).encode('utf-8')
  retorno = urlRequest.Request(url, data=data, headers=headers, method='POST')

  with urlRequest.urlopen(retorno) as response:
    response_data = response.read().decode(
      'utf-8')  # Decodificando a resposta em texto
    return jsonify({
      "message": "Senha atualizada com sucesso!",
      "response": response_data
    }), 200
