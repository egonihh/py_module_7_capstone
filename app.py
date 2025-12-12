from flask import Flask, jsonify, send_from_directory
from models import init_db, Session, Device, UsageEntry
from recommendations import generate_recommendations

app = Flask(__name__, static_folder='static')
init_db()

@app.route('/')
def index():
    return send_from_directory('static', 'index.html')

@app.route('/api/summary')
def summary():
    s = Session()
    devices = s.query(Device).all()
    out = []
    for d in devices:
        total = sum(u.seconds for u in d.usage)
        by_app = {}
        for u in d.usage:
            by_app[u.app_name] = by_app.get(u.app_name,0)+u.seconds
        out.append({'device': d.name, 'total_seconds': total, 'by_app': by_app})
    s.close()
    return jsonify(out)

@app.route('/api/recommendations')
def recs():
    s = Session()
    devices = s.query(Device).all()
    data = []
    for d in devices:
        entries = [{'app': u.app_name, 'seconds': u.seconds, 'background': u.background} for u in d.usage]
        data.append({'device': d.name, 'entries': entries})
    s.close()
    return jsonify(generate_recommendations(data))

if __name__ == '__main__':
    app.run(debug=True)