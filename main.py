import socketserver
import threading

from flask import Flask, render_template

app = Flask(__name__)

# A list to store received logs
logs = []


# Syslog UDP Handler
class SyslogUDPHandler(socketserver.BaseRequestHandler):
    def handle(self):
        message = self.request[0].decode("utf-8").replace("\x00", "")
        logs.append(f"{self.client_address[0]} : {message}")
        print(f"{self.client_address[0]} : {message}")


# Route to display logs
@app.route('/')
def index():
    return render_template('index.html', logs=logs)


def run_syslog_server():
    HOST, PORT = "0.0.0.0", 514
    server = socketserver.UDPServer((HOST, PORT), SyslogUDPHandler)
    print(f"Listening on port {PORT} for syslog messages...")
    server.serve_forever()


if __name__ == "__main__":
    # Start the syslog server in a separate thread
    syslog_thread = threading.Thread(target=run_syslog_server)
    syslog_thread.daemon = True
    syslog_thread.start()

    # Start the Flask web server
    app.run(host="0.0.0.0", port=8080)
