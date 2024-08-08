from flask import Flask, render_template, request, send_from_directory, abort, send_file
from flask_socketio import SocketIO, emit
from udp_sender import UDPSender
from qrcodeaux import generate_qr_code
import os
from apscheduler.schedulers.background import BackgroundScheduler
import parameters as pm
from pathlib import Path
import obswebsocket
from obswebsocket import obsws, requests
import time
import random

app = Flask(__name__)

socketio = SocketIO(app)

udp_sender = UDPSender()


def remove_old_files():
    current_time = time.time()
    directory = 'static/videos'
    minutes = 10

    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)

        if os.path.isfile(file_path):

            creation_time = os.path.getctime(file_path)

            time_difference = (current_time - creation_time) / 60

            if time_difference > minutes:

                os.remove(file_path)
                print(f'{filename} foi excluído.')
            else:
                print(f'{filename} foi criado há menos de {minutes} minutos.')


scheduler = BackgroundScheduler()
scheduler.add_job(remove_old_files, 'interval', minutes=2)
scheduler.start()


@app.route('/sing')
def index():
    return render_template('tablet/cantar.html')


@socketio.on('message')
def handle_message(message):
    print('Recebida mensagem: ' + message)
    emit('response', {'data': 'Mensagem recebida!'})


@app.route('/send_music_test', methods=['GET'])
def send_music_test():
    message = "start,BetterPlace_TrollsBandTogether"
    udp_sender.send(message)
    return "Message sent!"


@app.route('/send_music/<music>', methods=['GET'])
def send_music(music):
    message = "start," + music
    udp_sender.send(message)
    return "Message sent!"


@app.route('/render_terms')
def test_html():
    socketio.emit('render_terms')
    return "Render terms.html em todos os clientes!"


@app.route('/music-list')
def render_test_html():
    musics = []
    try:
        with open('static/music_list/musics.txt', 'r') as arquivo:
            for linha in arquivo:
                musics.append(linha.strip())
    except FileNotFoundError:
        return None
    print(musics)

    return render_template('tablet/music-list.html', musics=musics)


@app.route('/terms')
def terms_page():
    return render_template('tablet/termos.html')


@app.route('/qr')
def get_qrcode_score():
    video_id = get_most_recent_file()
    qr_image = generate_qr_code(pm.BASE_URL + '/download_video_page/' + video_id)
    return send_file(qr_image, mimetype='image/png')


def get_most_recent_file():
    directory = 'static/videos'
    if not os.path.isdir(directory):
        raise FileNotFoundError(f"O diretório {directory} não foi encontrado.")

    files = [f for f in Path(directory).iterdir() if f.is_file()]

    if not files:
        raise FileNotFoundError("Não há arquivos no diretório.")

    most_recent_file = max(files, key=os.path.getmtime)

    random_number = random.randint(10000, 99999)

    new_name = f'estrelas_da_casa_{random_number}{most_recent_file.suffix}'

    new_path = most_recent_file.parent / new_name

    os.rename(most_recent_file, new_path)

    return new_path.name


@app.route('/download_video_page/<filename>')
def download_video_page(filename):
    try:
        with open(f'static/videos/{filename}', 'rb') as f:
            pass
        return render_template('download.html', filename=filename)
    except FileNotFoundError:
        return render_template('error.html', message="File not found"), 404


@app.route('/download_video/<filename>')
def download_video(filename):
    try:
        return send_from_directory('static/videos', filename, as_attachment=True)
    except FileNotFoundError:
        abort(404, description="File not found")


@app.route('/save_video')
def save_video():
    try:
        ws = obsws('localhost', 4444, 'your_password')
        ws.connect()
        print("Conectado ao OBS WebSocket")

        ws.call(requests.StartRecording())
        print("Gravação iniciada")

        time.sleep(15)
        ws.call(requests.StopRecording())
        print("Gravação parada")

        ws.disconnect()
        print("Desconectado do OBS WebSocket")

    except obswebsocket.exceptions.ConnectionFailure as e:
        print(f"Falha na conexão: {e}")
    except Exception as e:
        print(f"Ocorreu um erro: {e}")
    return "Video Salvo"


if __name__ == '__main__':
    socketio.run(app, debug=True, host='0.0.0.0', allow_unsafe_werkzeug=True)
