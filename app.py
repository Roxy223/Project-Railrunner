from flask import Flask, render_template, request, redirect, url_for, session
from datetime import datetime, timedelta
import os

app = Flask(__name__)
app.secret_key = "supersecretkey"  # use env var in production

STOPS = [
    {"name":"Oosterblok","time":"23:53"},
    {"name":"BosWater","time":"23:55"},
    {"name":"De veer QD","time":"23:55"},
    {"name":"brugstraat","time":"23:56"},
    {"name":"Komerplein","time":"23:56"},
    {"name":"Oosterbrug","time":"23:57"},
    {"name":"Oostplein","time":"23:57"},
    {"name":"Rembrand CNTRL","time":"23:58"},
    {"name":"Hoogzandweg","time":"23:59"},
    {"name":"Hogezand Strand","time":"00:00"},
    {"name":"HZ WalenbW","time":"00:01"},
    {"name":"Hoogzand Centrum","time":"00:02"},
    {"name":"Zaandams weg","time":"00:03"},
    {"name":"Bosweg","time":"00:05"},
    {"name":"Bergenlaan","time":"00:06"},
    {"name":"HVBergenlaan","time":"00:07"},
    {"name":"Zaandam Centrum","time":"00:09"},
    {"name":"HVBergenlaan","time":"00:11"},
    {"name":"Bergenlaan","time":"00:12"},
    {"name":"Bosweg","time":"00:13"},
    {"name":"Zaandams Weg","time":"00:14"},
    {"name":"HoogZand Centrum","time":"00:16"},
    {"name":"HZ WalenBW","time":"00:17"},
    {"name":"Hoogzandweg","time":"00:18"},
    {"name":"Rembrand CNTRL","time":"00:19"},
    {"name":"Oostplein","time":"00:22"},
    {"name":"De veer QD","time":"00:25"},
    {"name":"Oosterblok","time":"00:30"},
]

def add_minutes(time_str, minutes):
    h, m = map(int, time_str.split(":"))
    dt = datetime(2000, 1, 1, h, m) + timedelta(minutes=minutes)
    return dt.strftime("%H:%M")

@app.route("/", methods=["GET", "POST"])
def index():
    if "delays" not in session:
        session["delays"] = [0] * len(STOPS)
    if "times" not in session:
        session["times"] = [s["time"] for s in STOPS]

    if request.method == "POST":

        if "reset_all" in request.form:
            session["delays"] = [0] * len(STOPS)
            session["times"] = [s["time"] for s in STOPS]
            session.modified = True
            return redirect(url_for("index"))

        for i in range(len(STOPS)):

            if request.form.get(f"add_delay_{i}"):
                session["delays"][i] += 1

            if request.form.get(f"subtract_delay_{i}"):
                session["delays"][i] -= 1

            delay_input = request.form.get(f"delay_{i}")
            if delay_input not in (None, ""):
                try:
                    session["delays"][i] = int(delay_input)
                except ValueError:
                    pass

            time_input = request.form.get(f"time_{i}")
            if time_input not in (None, ""):
                try:
                    datetime.strptime(time_input, "%H:%M")
                    session["times"][i] = time_input
                except ValueError:
                    pass

        session.modified = True
        return redirect(url_for("index"))

    stops_with_delays = []
    for i, stop in enumerate(STOPS):
        stops_with_delays.append({
            "name": stop["name"],
            "time": session["times"][i],
            "delay": session["delays"][i],
            "delayed_time": add_minutes(session["times"][i], session["delays"][i])
        })

    return render_template(
        "index.html",
        title="Line 33 – Night Service",
        sample_image="/static/route.png",
        stops=stops_with_delays
    )

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
