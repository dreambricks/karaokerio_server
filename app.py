from flask import Flask, jsonify, render_template
import threading
import socket
import requests

app = Flask(__name__)


@app.route('/api', methods=['GET'])
def api():
    return jsonify({"message": "Hello from Flask!"})


@app.route('/screen/<screen_name>', methods=['GET'])
def render_screen(screen_name):
    try:
        return render_template(f"{screen_name}.html")
    except Exception as e:
        return jsonify({"error": str(e)}), 404


def run_flask():
    app.run(host='0.0.0.0', port=5000)


def run_udp_server():
    udp_ip = "0.0.0.0"
    udp_port = 5001

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((udp_ip, udp_port))

    print("UDP server up and listening")

    while True:
        data, addr = sock.recvfrom(1024)  # buffer size is 1024 bytes
        screen_name = data.decode('utf-8')
        print("Received message:", screen_name, "from:", addr)

        try:
            response = requests.get(f"http://127.0.0.1:5000/screen/{screen_name}")
            if response.status_code == 200:
                sock.sendto(b'HTML rendered successfully', addr)
            else:
                sock.sendto(b'Error rendering HTML', addr)
        except Exception as e:
            sock.sendto(f'Error: {str(e)}'.encode('utf-8'), addr)

if __name__ == "__main__":
    flask_thread = threading.Thread(target=run_flask)
    udp_thread = threading.Thread(target=run_udp_server)

    flask_thread.start()
    udp_thread.start()

    flask_thread.join()
    udp_thread.join()