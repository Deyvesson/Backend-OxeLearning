from flask import jsonify, request
from models.chatpdf import upload_file_chatpdf, get_response_chatpdf
from models.firebase import initialize_firebase

#iniciando conexão com o firebase
firebase = initialize_firebase()
db = firebase.database()

#Função que realiza o upload dos arquivos para o ChatPDF
def upload_file():
  # Verifica se um arquivo foi enviado na requisição
  if 'file' not in request.files or request.files['file'].filename == '':
    return jsonify({"message": "Nenhum arquivo enviado"}), 400

  if 'name' not in request.form:
    return jsonify({"message": "Nome do arquivo não enviado"}), 400

  file = request.files['file']

  # Realiza o upload do arquivo para o ChatPDF
  files = [('file', ('file', file, 'application/octet-stream'))]

  response = upload_file_chatpdf(files)
  print(response.json())

  if response.status_code == 200:
    db.push({"name": request.form.get('name'), "sourceID": response.json()['sourceId']})
    return jsonify({
      "message": "Arquivo enviado com sucesso",
      "file": file.filename,
      "sourceId": response.json()['sourceId']
    }), 201
  else:
    print('Status:', response.status_code)
    print('Error:', response.text)
    return jsonify(
      {"message":
       f"Erro ao realizar o Upload do arquivo: {response.text}"}), 500


#Função para obter resposta para pergunta do usuário
def chat_message():
  data = request.get_json()
  if data.get('message') and data.get('sourceId'):
    
    response = get_response_chatpdf(
      data.get('sourceId'), 
      data.get('message'), 
      data.get('assistent')
    )

    if response.status_code == 200:
      return jsonify(
        {
          "message": "Resposta Obtida com sucesso",
          "response": response.json()['content']
        }
      ), 200
    else:
      return jsonify(
        {
          "message": f"Erro ao enviar mensagem: {response.text}"
        }
      ), 500
  else:
    return jsonify(
      {
        "message": "mensagem ou sourceId do arquivo não enviados"
      }
    ), 400

def list_files():
  try:
    files = db.get()
    #print(files.val())
    array_files = []
    for file in files.each():
      array_files.append(file.val())
    return jsonify({
        "message": "lista de arquivos obtida",
        "files": array_files
      }), 200
  except Exception as e:
    return jsonify({'message': f"Erro ao obter lista de arquivos: {e}"}), 500

def delete_file():
  try:
    data = request.get_json()
    if(data.get('sourceID')):
      #Obtendo identificador do registro no firebase
      firebase_iten = db.order_by_child("sourceID").equal_to(data.get('sourceID')).get() 
      print(firebase_iten[0].key())
      #Deletando registro no firebase
      db.child(firebase_iten[0].key()).remove()
      return jsonify({
        "message": "Arquivo removido com sucesso",
        "sourceID": data.get('sourceID')
      }), 200
    else:
      return jsonify({
        "message": "sourceID não enviado"
      }), 400
  except Exception as e:
    return jsonify({'message': f"Erro ao remover arquivo: {e}"}), 500