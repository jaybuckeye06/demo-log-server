from flask import Flask, Response, request, abort
import os
import random
import string

app = Flask(__name__)

LOG_DIR = "logs"
NUM_LOGS = 100
MIN_LINES = 10000
MAX_LINES = 20000


def generate_log_files():
    os.makedirs(LOG_DIR, exist_ok=True)
    for i in range(1, NUM_LOGS + 1):
        path = os.path.join(LOG_DIR, f"log{i}.log")
        if not os.path.exists(path):
            with open(path, "w") as f:
                num_lines = random.randint(MIN_LINES, MAX_LINES)
                for j in range(1, num_lines + 1):
                    content = ''.join(random.choices(string.ascii_letters + string.digits, k=80))
                    f.write(f"log{i}_line{j}: {content}\n")


def stream_logs(start, end):
    for i in range(start, end + 1):
        path = os.path.join(LOG_DIR, f"log{i}.log")
        if not os.path.exists(path):
            continue
        with open(path, "r") as f:
            yield f.read()


@app.route("/logs")
def get_logs():
    try:
        start = int(request.args.get("start"))
        end = int(request.args.get("end"))
    except (TypeError, ValueError):
        abort(400, "Invalid start or end parameter")

    if not (1 <= start <= end <= NUM_LOGS):
        abort(400, "Start and end must be between 1 and 100 and start <= end")

    return Response(stream_logs(start, end), mimetype='text/plain', headers={
        "Content-Disposition": "attachment; filename=output.log"
    })


if __name__ == '__main__':
    generate_log_files()
    app.run(debug=True, port=12001)
