# Flask Log Streamer

A simple Flask app that streams merged log files on the fly.

## Usage

To start the server:
```
python -m venv venv
source venv/bin/activate        # On Windows: venv\Scripts\activate
pip install -r requirements.txt

python app.py
```

To test:
```
curl -OJ "http://localhost:12001/logs?start=10&end=23"
```





