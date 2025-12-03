from flask import Flask, render_template, request, redirect, url_for, session
from datetime import datetime, timedelta
import os

app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET", "dev-key")

STOPS = [
    {"name": "Amsterdam Centraal", "time": "16:42"},
    {"name": "Amsterdam Amstel", "time": "16:46"},
    {"name": "Duivendrecht", "time": "16:48"},
    {"name": "Amsterdam Bijlmer Arena", "time": "16:50"},
    {"name": "Abcoude Station", "time": "17:53"},
    {"name": "Breukelen Station", "time": "17:57"},
]

SAMPLE_IMAGE = ""

def add_minutes(t, mins):
    h, m = map(int, t.split(":"))
    dt = datetime(2000, 1, 1, h, m) + timedelta(minutes=mins)
    return dt.strftime("%H:%M")

@app.route("/", methods=["GET", "POST"])
def index():
    if "times" not in session:
        session["times"] = [stop["time"] for stop in STOPS]
    if "delays" not in session:
        session["delays"] = [0] * len(STOPS)

    if request.method == "POST":

        for i in range(len(STOPS)):

            if f"add_{i}" in request.form:
                session["delays"][i] += 1

            if f"sub_{i}" in request.form:
                session["delays"][i] -= 1

            time_val = request.form.get(f"time_{i}")
            if time_val:
                try:
                    datetime.strptime(time_val, "%H:%M")
                    session["times"][i] = time_val
                except:
                    pass

            delay_val = request.form.get(f"delay_{i}")
            if delay_val:
                try:
                    session["delays"][i] = int(float(delay_val))
                except:
                    pass

        if "reset_all" in request.form:
            session["times"] = [stop["time"] for stop in STOPS]
            session["delays"] = [0 for _ in STOPS]

        session.modified = True
        return redirect(url_for("index"))

    stops_out = []
    for i, stop in enumerate(STOPS):
        base = session["times"][i]
        delay = session["delays"][i]
        stops_out.append({
            "name": stop["name"],
            "base_time": base,
            "delay": delay,
            "updated_time": add_minutes(base, delay),
            "is_delayed": delay != 0
        })

    return render_template("index.html",
                           stops=stops_out,
                           title="IC Naar Utrecht Centraal",
                           sample_image=SAMPLE_IMAGE)

if __name__ == "__main__":
    # Render-compatible host + port binding
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
