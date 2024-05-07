from flask import Flask
import requests
from flask import render_template
from flask import g
from flask import request

app = Flask(__name__)

def get_messages():
    if not hasattr(g, 'messages'):
        g.messages = []
    return g.messages

@app.route('/')
def home():
    messages = get_messages()  # Función para obtener los mensajes de chat
    return render_template('chat.html', messages=messages)

@app.route('/send_message', methods=['POST'])
def send_message():
    user_message = request.form['message']
    # Procesar el mensaje del usuario y enviar una respuesta de Cohere
    return render_template('send_message.html')

@app.route('/chat', methods=['GET', 'POST'])
def chat():
    if not hasattr(g, 'messages'):
        g.messages = []
    if request.method == 'POST':
        # Procesar la solicitud de chat y enviar la respuesta de Cohere
        message_from_user = request.form['message']
        response_from_cohere = get_cohere_response(message_from_user)
        g.messages.append(f'Usuario: {message_from_user}')
        g.messages.append(f'Cohere: {response_from_cohere}')
    return render_template('chat.html', messages=g.messages)

COHERE_API_KEY = 'zCuY6C9JU0eL7K19BXvWi1cF2FQUvHiOMQwxmaqd'
COHERE_API_URL = 'https://api.cohere.com/command-api/v1'

def get_cohere_response(message):
    data = {
        'query': message,
        'model': 'command'
    }

    headers = {
        'Authorization': f'Bearer {COHERE_API_KEY}'
    }

    try:
        response = requests.post(COHERE_API_URL, json=data, headers=headers)
        response_data = response.json()
        print(response_data)
        return response_data['results'][0]['text']['text']
    except requests.RequestException as e:
        print(f'Error al realizar la solicitud: {e}')
        return None

if __name__ == '__main__':
    app.run()