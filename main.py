import logging
import sys
import time
from datetime import datetime, timedelta
from logging.handlers import TimedRotatingFileHandler
from pathlib import Path
from socketserver import BaseRequestHandler, UDPServer
from threading import Thread

from flask import Flask, render_template, redirect
from flask_socketio import SocketIO

app = Flask(__name__)
socketio = SocketIO(app)

logs = []  # A list to store received logs


def log_namer(default_name: str) -> str:
    base_filename, ext, date = default_name.split(".")
    return f"{base_filename}.{date}.{ext}"


def setup_logging() -> None:
    # Create a custom base_logger
    base_logger = logging.getLogger()
    base_logger.setLevel(logging.DEBUG)

    # Create folder for file logs.
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)
    log_file = log_dir / "runtime.log"

    # Create handlers
    file_handler = TimedRotatingFileHandler(log_file, when='midnight', interval=1, backupCount=7, encoding='utf-8')
    file_handler.namer = log_namer
    file_handler.setLevel(logging.DEBUG)
    console_handler = logging.StreamHandler(stream=sys.stdout)
    console_handler.setLevel(logging.INFO)

    log_file_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(log_file_format)

    # Add handlers to the base_logger
    base_logger.addHandler(file_handler)
    base_logger.addHandler(console_handler)


class SyslogUDPHandler(BaseRequestHandler):
    """
    Syslog UDP Handler
    """

    def handle(self) -> None:
        message = self.request[0].decode("utf-8").replace("\x00", "")
        message = message[4:] if message.startswith('<') else message  # remove logger level numbers from message
        new_log = f"{self.client_address[0]} : {message}"
        logs.append(new_log)

        # Emit the new log message to all connected WebSocket clients
        socketio.emit('new_log', {'log': new_log})


@app.route('/')
def index():
    """
    Route to display logs
    """
    return render_template("index.html", logs=logs)


@app.route('/', methods=['POST'])
def clear_logs_button():
    """
    Route to clear logs and reload page
    """
    clear_logs()
    return redirect('/')


def clear_logs() -> None:
    logs.clear()
    logging.warning("Logs cleared")


def schedule_daily_tasks(target_hr: int = 12) -> None:
    while True:
        now = datetime.now().replace(microsecond=0)
        target_time = now.replace(hour=target_hr, minute=0, second=0)
        if now == target_time:
            # ----- Tasks -----
            clear_logs()
            time.sleep(1)
        else:
            remaining_time = target_time - now
            if remaining_time < timedelta():
                remaining_time = remaining_time + timedelta(days=1)
            time.sleep(remaining_time.total_seconds())


def run_syslog_server(port: int = 1514) -> None:
    with UDPServer(("0.0.0.0", port), SyslogUDPHandler) as server:
        logging.info(f"Listening on port {port} for syslog messages...")
        server.serve_forever()


def run_server(port: int = 9000) -> None:
    setup_logging()
    logging.info("Logging Started")
    try:
        Thread(target=run_syslog_server, daemon=True).start()  # Start the syslog server in a separate thread
        Thread(target=schedule_daily_tasks, daemon=True).start()  # Start the daily task scheduler in a separate thread
        socketio.run(app, host="0.0.0.0", port=port, allow_unsafe_werkzeug=True)  # Start Flask web server with SocketIO
    except Exception as error:
        logging.error("An error occurred while the server was running.")
        logging.exception(error)
    logging.debug("Logging Ended\n\n")


if __name__ == "__main__":
    run_server()
