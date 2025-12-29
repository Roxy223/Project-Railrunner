from flask import Flask, render_template, request, redirect, url_for, session
from datetime import datetime, timedelta

app = Flask(__name__)
app.secret_key = "supersecretkey"  # IMPORTANT: Use env variable in production

# Full Line 33 schedule
STOPS = [
  {"name":"Den Helder","time":"01:37"},
  {"name":"Den Helder Zuid","time":"01:40"},
  {"name":"Anna Palowona","time":"01:43"},
  {"name":"Schagen","time":"01:46"},
  {"name":"Heeruhugowaard","time":"01:49"},
  {"name":"Alkmaar Noord","time":"01:53"},
  {"name":"Alkmaar","time":"01:56"},
  {"name":"Heiloo","time":"02:00"},
  {"name":"Castricem","time":"02:04"},
  {"name":"Uitgeest","time":"02:07"},
  {"name":"AssenDelft","time":"02:10"},
  {"name":"Wormerveer","time":"02:12"},
  {"name":"Zaanse Schans","time":"02:16"},
  {"name":"Kooz .a . Zaan","time":"02:19"},
  {"name":"Zaandam","time":"02:23"},
  {"name":"Amsterdam Sloterdijk","time":"02:27"},
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












