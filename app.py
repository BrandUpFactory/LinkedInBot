from flask import Flask, render_template, request, redirect
from scripts.scraper import (
    initialize_driver,
    remove_full_height,
    manage_buffer,
    reload_feed,
    cleanup_driver,
)
import time

app = Flask(__name__)
buffer = []

@app.route("/")
def index():
    global buffer
    driver = initialize_driver()
    remove_full_height()

    if len(buffer) < 5:  # Puffer erhöhen
        buffer.extend(manage_buffer(5))
        if len(buffer) < 5:
            reload_feed()
            buffer.extend(manage_buffer(5))

    if not buffer:
        return "Keine weiteren Beiträge zum Überprüfen."

    post = buffer.pop(0)
    return render_template("review.html", post=post)

@app.route("/submit", methods=["POST"])
def submit():
    global buffer
    action = request.form["action"]
    print(f"Aktion: {action}")
    time.sleep(0.5)  # Kürzere Ladeanimation
    return redirect("/")

@app.teardown_appcontext
def teardown_driver(exception):
    cleanup_driver()

if __name__ == "__main__":
    print("Starte die App...")
    app.run(debug=True, use_reloader=False)
