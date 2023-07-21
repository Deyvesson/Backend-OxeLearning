from flask import jsonify, request
from models.chatpdf import upload_file_chatpdf, get_response_chatpdf

#Função que realiza o upload dos arquivos para o ChatPDF
def upload_file():
  # Verifica se um arquivo foi enviado na requisição

  if 'file' not in request.files or request.files['file'].filename == '':
    return jsonify({"message": "Nenhum arquivo enviado"}), 400

  file = request.files['file']

  # Realiza o upload do arquivo para o ChatPDF
  files = [('file', ('file', file, 'application/octet-stream'))]

  response = upload_file_chatpdf(files)
  print(response)

  if response.status_code == 200:
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
  if request.form.get('message') and request.form.get('sourceId'):
    
    response = get_response_chatpdf(
      request.form.get('sourceId'), 
      request.form.get('message'), 
      request.form.get('assistent')
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