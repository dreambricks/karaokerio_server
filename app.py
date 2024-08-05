from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit
from udp_sender import UDPSender
from qrcodeaux import generate_qr_code
import io
import base64

app = Flask(__name__)

socketio = SocketIO(app)

udp_sender = UDPSender()


@app.route('/')
def index():
    return render_template('index.html')


@socketio.on('message')
def handle_message(message):
    print('Recebida mensagem: ' + message)
    emit('response', {'data': 'Mensagem recebida!'})


@app.route('/send_music', methods=['POST'])
def test_udp():
    message = request.form['message']
    udp_sender.send(message)
    return "Message sent!"


@app.route('/render_music_list')
def test_html():
    socketio.emit('render_list')
    return "Render music-list.html em todos os clientes!"


@app.route('/music-list.html')
def render_test_html():
    return render_template('music-list.html')


@app.route('/qrcode_video/<id>')
def qrcode_video(id):
    qr_code_image = generate_qr_code(id)

    img_buffer = io.BytesIO()
    qr_code_image.save(img_buffer, format="PNG")

    img_str = base64.b64encode(img_buffer.getvalue()).decode()

    return render_template('qr-code-video.html', qrcode=img_str)


if __name__ == '__main__':
    socketio.run(app, debug=True, host='0.0.0.0', allow_unsafe_werkzeug=True)
