from flask import Flask, render_template, jsonify
from models import Session, Device, UsageEntry

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/data")
def data():
    s = Session()
    devices = s.query(Device).all()
    output = {}
    for d in devices:
        total_sec = sum(u.seconds for u in d.usages)
        total_pickups = sum(u.pickups for u in d.usages)
        apps = {}
        for u in d.usages:
            apps[u.app_name] = {"time": u.seconds, "pickups": u.pickups}
        output[d.name] = {
            "total_seconds": total_sec,
            "pickups": total_pickups,
            "apps": apps
        }
    return jsonify(output)

if __name__ == "__main__":
    app.run(debug=True)
