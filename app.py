from flask import Flask, render_template, request, make_response, redirect, url_for
from datetime import datetime
import json

app = Flask(__name__)

@app.route("/")
def home():
    with open('./data/projects.json') as f:
        project_list = json.load(f)
        theme = request.cookies.get("theme", "light-mode")
        current_date = datetime.now().strftime("%B %Y")
        if not theme:
            prefers_dark = "dark" in request.headers.get("User-Agent", "").lower()
            theme = "dark-mode" if prefers_dark else "light-mode"
    return render_template("index.html", projects=project_list, date=current_date, theme=theme)

@app.route("/toggle_theme", methods=["GET", "POST"])
def toggle_theme():
    current_theme = request.cookies.get("theme", "light-mode")
    new_theme = "dark-mode" if current_theme == "light-mode" else "light-mode"
    response = make_response(redirect(url_for("home")))
    response.set_cookie("theme", new_theme)
    return response

if __name__ == "__main__":
    app.run(debug=True)

