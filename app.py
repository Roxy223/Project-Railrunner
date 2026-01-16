from flask import Flask, render_template, request, redirect, url_for, session
from datetime import datetime, timedelta

app = Flask(__name__)
app.secret_key = "supersecretkey"  # Use environment variable in production

# Full Line 33 schedule
STOPS = [
    {"name":"Oosterblok","time":"16:53"},
    {"name":"BosWater","time":"16:55"},
    {"name":"De veer QD","time":"16:55"},
    {"name":"brugstraat","time":"16:56"},
    {"name":"Komerplein","time":"16:56"},
    {"name":"Oosterbrug","time":"16:57"},
    {"name":"Oostplein","time":"16:57"},
    {"name":"Rembrand CNTRL","time":"16:58"},
    {"name":"Hoogzandweg","time":"16:59"},
    {"name":"Hogezand Strand","time":"17:00"},
    {"name":"HZ WalenbW","time":"17:01"},
    {"name":"Hoogzand Centrum","time":"17:02"},
    {"name":"Zaandams weg","time":"17:03"},
    {"name":"Bosweg","time":"17:05"},
    {"name":"Bergenlaan","time":"17:06"},
    {"name":"HVBergenlaan","time":"17:07"},
    {"name":"Zaandam Centrum","time":"17:09"},
    {"name":"HVBergenlaan","time":"17:11"},
    {"name":"Bergenlaan","time":"18:12"},
    {"name":"Bosweg","time":"17:13"},
    {"name":"Zaandams Weg","time":"17:14"},
    {"name":"HoogZand Centrum","time":"17:16"},
    {"name":"HZ WalenBW","time":"17:17"},
    {"name":"Hoogzandweg","time":"17:18"},
    {"name":"Rembrand CNTRL","time":"17:19"},
    {"name":"Oostplein","time":"17:22"},
    {"name":"De veer QD","time":"17:25"},
    {"name":"BosWater","time":"17:26"},
    {"name":"Damweg","time":"17:28"},
    {"name":"Schuurplein","time":"17:29"},
    {"name":"Oosterblok","time":"17:30"},
]

def add_minutes(time_str, minutes):
    h, m = map(int, time_str.split(":"))
    dt = datetime(2000,1,1,h,m) + timedelta(minutes=minutes)
    return dt.strftime("%H:%M")

@app.route("/", methods=["GET", "POST"])
def index():
    if "delays" not in session:
        session["delays"] = [0 for _ in STOPS]  # Start all delays at 0
    if "times" not in session:
        session["times"] = [stop["time"] for stop in STOPS]

    if request.method == "POST":
        for i, stop in enumerate(STOPS):
            # Increment / decrement delays
            if f"add_delay_{i}" in request.form:
                session["delays"][i] += 1
            if f"subtract_delay_{i}" in request.form:
                session["delays"][i] = max(0, session["delays"][i]-1)

            # Editable delay input
            if f"delay_{i}" in request.form:
                try:
                    new_delay = int(request.form[f"delay_{i}"])
                    session["delays"][i] = max(0, new_delay)
                except ValueError:
                    pass

            # Editable time input
            if f"time_{i}" in request.form:
                new_time = request.form[f"time_{i}"]
                try:
                    datetime.strptime(new_time, "%H:%M")
                    session["times"][i] = new_time
                except ValueError:
                    pass

        # Reset all button
        if "reset_all" in request.form:
            session["delays"] = [0 for _ in STOPS]
            session["times"] = [stop["time"] for stop in STOPS]

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

    return render_template("index.html", stops=stops_with_delays)

if __name__ == "__main__":
    app.run(debug=True)
