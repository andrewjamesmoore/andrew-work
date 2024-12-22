from datetime import datetime
from flask import Flask, render_template, request, make_response, redirect, url_for
from contentful_client import get_all_entries, fetch_project_by_slug
from markdown2 import markdown

app = Flask(__name__)

@app.context_processor
def inject_globals():
    theme = request.cookies.get("theme", "light-mode")
    opposite_theme = "dark-mode" if theme == "light-mode" else "light-mode"
    current_date = datetime.now().strftime("%B %Y")
    return dict(theme=theme, opposite_theme=opposite_theme, date=current_date)

@app.route("/")
def home():
    try:
        project_list = get_all_entries('projects')
    except Exception as e:
        print(f"Error fetching projects: {e}")
        project_list = []
    return render_template("home.html", projects=project_list)

@app.route("/projects")
def project_repo():
    try:
        project_list = get_all_entries('projects')
    except Exception as e:
        print(f"Error fetching projects: {e}")
        project_list = []
    return render_template("projects.html", projects=project_list)

@app.route("/projects/<slug>")
def project(slug):
    project_data = fetch_project_by_slug(slug)
    project_data['body_html'] = markdown(project_data.get('body', ''))
    return render_template("project.html", project=project_data)

@app.route("/toggle_theme", methods=["GET", "POST"])
def toggle_theme():
    current_theme = request.cookies.get("theme", "light-mode")
    new_theme = "dark-mode" if current_theme == "light-mode" else "light-mode"
    referer_url = request.referrer or url_for('home')
    response = make_response(redirect(referer_url))
    response.set_cookie("theme", new_theme)
    return response

@app.errorhandler(Exception)
def handle_error(error):
    app.logger.error(f'An error occurred: {error}')
    return render_template('error.html'), 500

if __name__ == "__main__":
    app.run(debug=True)