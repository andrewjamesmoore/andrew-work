from datetime import datetime
from flask import Flask, render_template, request, make_response, redirect, url_for
from contentful_client import get_all_entries, fetch_project_by_slug, fetch_experiment_by_slug
from markdown2 import markdown

app = Flask(__name__)

# Application Configuration
app.config['SESSION_COOKIE_SECURE'] = True
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'


# Reuse for Contentful markdown in body
def parse_markdown(content):
    return markdown(content or '')


# Helper function for colour theme toggle
def get_theme():
    theme = request.cookies.get("theme", "light-mode")
    opposite_theme = "dark-mode" if theme == "light-mode" else "light-mode"
    return theme, opposite_theme


# Error logging util
def log_error(context, error):
    app.logger.error(f"Error {context}: {error}")


# Helper to reduce repeating get all entries from Contentful
def fetch_entries(content_type):
    try:
        return get_all_entries(content_type)
    except Exception as e:
        log_error(f"fetching {content_type}", e)
        return []


# Global Variables
@app.context_processor
def inject_globals():
    theme, opposite_theme = get_theme()
    current_date = datetime.now().strftime("%B %Y")
    return dict(theme=theme, opposite_theme=opposite_theme, date=current_date)


# Home
@app.route("/")
def home():
    project_list = fetch_entries('projects')
    experiment_list = fetch_entries('experiments')
    return render_template("home.html", projects=project_list, experiments=experiment_list)


# Projects
@app.route("/projects")
def project_repo():
    project_list = fetch_entries('projects')
    return render_template("projects.html", projects=project_list)


@app.route("/projects/<slug>")
def project(slug):
    project_data = fetch_project_by_slug(slug)
    project_data['body_html'] = parse_markdown(project_data.get('body'))
    return render_template("project.html", project=project_data)


# Experiments
@app.route("/experiments")
def experiment_repo():
    experiment_list = fetch_entries('experiments')
    return render_template("experiments.html", experiments=experiment_list)


@app.route("/experiments/<slug>")
def experiment(slug):
    experiment_data = fetch_experiment_by_slug(slug)
    experiment_data['body_html'] = parse_markdown(experiment_data.get('body'))
    return render_template("experiment.html", experiment=experiment_data)


#Colour Theme
@app.route("/toggle_theme", methods=["GET", "POST"])
def toggle_theme():
    current_theme, new_theme = get_theme()
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