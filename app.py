from flask import Flask, render_template
import json

app = Flask(__name__)

@app.route("/")
def home():
    with open('./data/projects.json') as f:
        project_list = json.load(f)
    return render_template("index.html", projects=project_list)

@app.route("/about")
def about():
    return render_template("about.html")

if __name__ == "__main__":
    app.run(debug=True)

