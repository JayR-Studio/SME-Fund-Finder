import os
from flask import Flask, render_template, abort, request
import pandas as pd
import json

# 1. Absolute Path Discovery
# This finds the EXACT folder where index.py lives
api_dir = os.path.dirname(os.path.abspath(__file__))
# This goes up one level to the root
project_root = os.path.abspath(os.path.join(api_dir, ".."))
# This points specifically to your templates
template_dir = os.path.join(project_root, 'templates')

app = Flask(__name__, template_folder=template_dir)


def load_grant_data():
    """Loads CSV using the absolute project root path"""
    data_path = os.path.join(project_root, 'data', 'grants.csv')
    if os.path.exists(data_path):
        return pd.read_csv(data_path)
    return pd.DataFrame()


@app.route('/')
def home():
    """Single-page logic for directory and search results."""
    query = request.args.get('q', '').strip().lower()
    df = load_grant_data()

    if df.empty:
        return "System initializing... please wait."

    if query:
        # Filter: looks through grant names, states, and industries
        mask = (
                df['grant_name'].str.lower().str.contains(query) |
                df['state'].str.lower().str.contains(query) |
                df['industry'].str.lower().str.contains(query)
        )
        results = df[mask].to_dict('records')
        section_title = f"Search Results for '{query}'"
    else:
        # Default: show first 20 for the directory view
        results = df.head(20).to_dict('records')
        section_title = "Featured Funding Opportunities"

    return render_template('index.html', grants=results, title=section_title)


@app.route('/grant/<slug>')
def grant_detail(slug):
    df = load_grant_data()
    grant_match = df[df['slug'] == slug].to_dict('records')
    if not grant_match:
        abort(404)
    return render_template('grant_page.html', data=grant_match[0])


def load_articles():
    """Helper to read our article library from JSON."""
    json_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'articles.json')
    with open(json_path, 'r') as f:
        return json.load(f)


@app.route('/resources/<slug>')
def view_article(slug):
    """Dynamic route for the 20 authority articles."""
    all_articles = load_articles()
    article = all_articles.get(slug)

    if not article:
        abort(404)

    return render_template('articles.html',
                           title=article['title'],
                           content=article['content'])


@app.route('/resources')
def resources_directory():
    all_articles = load_articles() # Reuses your existing JSON loader
    return render_template('resources.html', articles=all_articles)


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/privacy-policy')
def privacy():
    return render_template('privacy.html')


@app.route('/terms')
def terms():
    return render_template('terms.html')


@app.route('/contact')
def contact():
    return render_template('contact.html')


# Required for Vercel
app = app

if __name__ == "__main__":
    app.run(debug=True)
