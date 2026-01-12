from flask import Flask, render_template, request, redirect, url_for, session
from datetime import datetime, timedelta

app = Flask(__name__)
app.secret_key = "supersecretkey"  # IMPORTANT: Use env variable in production

# Full Line 33 schedule
stops = [
    {"name": "Oosterblok", "time": "20:53"},
    {"name": "BosWater", "time": "20:55"},
    {"name": "De veer QD", "time": "20:55"},
    {"name": "brugstraat", "time": "20:56"},
    {"name": "Komerplein", "time": "20:56"},
    {"name": "Oosterbrug", "time": "20:57"},
    {"name": "Oostplein", "time": "20:57"},
    {"name": "Rembrand CNTRL", "time": "20:58"},
    {"name": "Hoogzandweg", "time": "20:59"},
    {"name": "Hogezand Strand", "time": "21:00"},
    {"name": "HZ WalenbW", "time": "21:01"},
    {"name": "Hoogzand Centrum", "time": "21:02"},
    {"name": "Zaandams weg", "time": "21:03"}
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























