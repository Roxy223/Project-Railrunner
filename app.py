from flask import Flask, render_template, request, redirect, url_for, session
from datetime import datetime, timedelta

app = Flask(__name__)
app.secret_key = "supersecretkey"  # IMPORTANT: Use env variable in production

# Full Line 33 schedule
STOPS = [
    {"name":"Oosterblok","time":"17:53"},
    {"name":"Baaier","time":"17:54"},
    {"name":"BosWater","time":"17:55"},
    {"name":"De veer QD","time":"17:55"},
    {"name":"brugstraat","time":"17:56"},
    {"name":"Komerplein","time":"17:56"},
    {"name":"Oosterbrug","time":"17:57"},
    {"name":"Oostplein","time":"17:57"},
    {"name":"Rembrand CNTRL","time":"17:58"},
    {"name":"Hoogzandweg","time":"17:59"},
    {"name":"Hogezand Strand","time":"18:00"},
    {"name":"HZ WalenbW","time":"18:01"},
    {"name":"Hoogzand Centrum","time":"18:02"},
    {"name":"Zaandams weg","time":"18:03"},
    {"name":"Bosweg","time":"18:05"},
    {"name":"Bergenlaan","time":"18:06"},
    {"name":"HVBergenlaan","time":"18:07"},
    {"name":"Zaandam Centrum","time":"18:09"},
    {"name":"HVBergenlaan","time":"18:11"},
    {"name":"Bergenlaan","time":"18:12"},
    {"name":"Bosweg","time":"18:13"},
    {"name":"Zaandams Weg","time":"18:14"},
    {"name":"HoogZand Centrum","time":"18:16"},
    {"name":"HZ WalenBW","time":"18:17"},
    {"name":"Hoogzandweg","time":"18:18"},
    {"name":"Rembrand CNTRL","time":"18:19"},
    {"name":"Oostplein","time":"18:22"},
    {"name":"De veer QD","time":"18:25"},
    {"name":"BosWater","time":"18:26"},
    {"name":"Damweg","time":"18:28"},
    {"name":"Schuurplein","time":"18:29"},
    {"name":"Oosterblok","time":"18:30"},
]


def add_minutes(time_str, minutes):
    h, m = map(int, time_str.split(":"))
    dt = datetime(2000, 1, 1, h, m) + timedelta(minutes=minutes)
    return dt.strftime("%H:%M")


@app.route("/", methods=["GET", "POST"])
def index():
    # Initialize session values
    if "delays" not in session:
        session["delays"] = [0] * len(STOPS)
    if "times" not in session:
        session["times"] = [stop["time"] for stop in STOPS]

    if request.method == "POST":

        # Reset button
        if "reset_all" in request.form:
            session["delays"] = [0] * len(STOPS)
            session["times"] = [stop["time"] for stop in STOPS]
            session.modified = True
            return redirect(url_for("index"))

        # Process updates per stop
        for i in range(len(STOPS)):

            # Add delay
            if request.form.get(f"add_delay_{i}"):
                session["delays"][i] += 1

            # Subtract delay
            if request.form.get(f"subtract_delay_{i}"):
                session["delays"][i] = max(0, session["delays"][i] - 1)

            # Manual delay input
            delay_input = request.form.get(f"delay_{i}")
            if delay_input not in (None, ""):
                try:
                    new_delay = int(delay_input)
                    session["delays"][i] = max(0, new_delay)
                except ValueError:
                    pass

            # Manual time input
            time_input = request.form.get(f"time_{i}")
            if time_input not in (None, ""):
                try:
                    datetime.strptime(time_input, "%H:%M")
                    session["times"][i] = time_input
                except ValueError:
                    pass

        session.modified = True
        return redirect(url_for("index"))

    # Prepare rendering
    stops_with_delays = []
    for i, stop in enumerate(STOPS):
        stops_with_delays.append({
            "name": stop["name"],
            "time": session["times"][i],
            "delay": session["delays"][i],
            "delayed_time": add_minutes(session["times"][i], session["delays"][i])
        })

    return render_template("index.html", stops=stops_with_delays)


import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)




