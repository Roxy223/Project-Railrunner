from flask import Flask, render_template, request, redirect, url_for, session
from datetime import datetime, timedelta

app = Flask(__name__)
app.secret_key = "supersecretkey"  # replace with env var in production

# Stops (base scheduled times)
STOPS = [
    {"name":"Amsterdam Centraal","time":"16:42"},
    {"name":"Amsterdam Amstel","time":"16:46"},
    {"name":"Amsterdam Bijlmer Arena","time":"16:50"},
    {"name":"Maarssen":"17:57"},
    {"name":"Utrecht Centraal","time":"18:00"},
]

# uploaded image local path (will be converted by your environment)
SAMPLE_IMAGE = "/mnt/data/48b3c56f-2692-49b6-9e22-bf2e1af7218a.png"

def add_minutes(time_str, minutes):
    """Add (or subtract) minutes to HH:MM string and return HH:MM (wraps past midnight)."""
    h, m = map(int, time_str.split(":"))
    dt = datetime(2000,1,1,h,m) + timedelta(minutes=minutes)
    return dt.strftime("%H:%M")

@app.route("/", methods=["GET", "POST"])
def index():
    # initialize session values
    if "times" not in session:
        session["times"] = [stop["time"] for stop in STOPS]
    if "delays" not in session:
        session["delays"] = [0 for _ in STOPS]

    if request.method == "POST":
        # check each stop for updates or +/- clicks
        for i, _ in enumerate(STOPS):
            # +/- buttons: names like add_0, sub_0
            if f"add_{i}" in request.form:
                session["delays"][i] = session["delays"][i] + 1
            if f"sub_{i}" in request.form:
                session["delays"][i] = session["delays"][i] - 1  # allow negative for early

            # time input
            tkey = f"time_{i}"
            if tkey in request.form:
                val = request.form.get(tkey, "").strip()
                try:
                    datetime.strptime(val, "%H:%M")
                    session["times"][i] = val
                except Exception:
                    pass

            # delay numeric input (editable)
            dkey = f"delay_{i}"
            if dkey in request.form:
                val = request.form.get(dkey, "").strip()
                try:
                    newd = int(float(val))
                    session["delays"][i] = newd
                except Exception:
                    pass

        # Reset
        if "reset_all" in request.form:
            session["times"] = [stop["time"] for stop in STOPS]
            session["delays"] = [0 for _ in STOPS]

        session.modified = True
        return redirect(url_for("index"))

    # prepare stops
    stops_render = []
    for i, stop in enumerate(STOPS):
        base_time = session["times"][i]
        delay = session["delays"][i]
        updated_time = add_minutes(base_time, delay)
        stops_render.append({
            "name": stop["name"],
            "base_time": base_time,
            "delay": delay,
            "updated_time": updated_time,
            "is_delayed": delay != 0
        })

    return render_template("index.html",
                           stops=stops_render,
                           title="RE6 Naar Utrect Centraal",
                           sample_image=SAMPLE_IMAGE)

if __name__ == "__main__":
    app.run(debug=True)
