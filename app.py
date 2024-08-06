from flask import Flask, render_template, request, send_from_directory, abort,send_file
from flask_socketio import SocketIO, emit
from udp_sender import UDPSender
from qrcodeaux import generate_qr_code
import os
import time
from apscheduler.schedulers.background import BackgroundScheduler
import parameters as pm


app = Flask(__name__)

socketio = SocketIO(app)

udp_sender = UDPSender()


def remove_old_files():
    current_time = time.time()
    directory = 'static/videos'
    minutes = 5

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


@app.route('/')
def index():
    return render_template('index.html')


@socketio.on('message')
def handle_message(message):
    print('Recebida mensagem: ' + message)
    emit('response', {'data': 'Mensagem recebida!'})


@app.route('/send_music', methods=['GET'])
def test_udp():
    message = "start Evanescence-Bring-Me-to-Life"
    udp_sender.send(message)
    return "Message sent!"


@app.route('/render_music_list')
def test_html():
    socketio.emit('render_list')
    return "Render music-list.html em todos os clientes!"


@app.route('/music-list.html')
def render_test_html():
    return render_template('music-list.html')


@app.route('/qr/<video_id>')
def get_qrcode_score(video_id):
    qr_image = generate_qr_code(pm.BASE_URL + '/download_video_page/' + video_id + '.mp4')
    return send_file(qr_image, mimetype='image/png')


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


if __name__ == '__main__':
    socketio.run(app, debug=True, host='0.0.0.0', allow_unsafe_werkzeug=True)
