import json
import pandas as pd
from datetime import datetime


def generate_sitemap():
    # Your live URL
    base_url = "https://sme-fund-finder.vercel.app"

    # Static mandatory pages
    pages = [
        {"url": "/", "priority": "1.0"},
        {"url": "/resources", "priority": "0.9"},
        {"url": "/about", "priority": "0.5"},
        {"url": "/privacy", "priority": "0.5"},
        {"url": "/terms", "priority": "0.5"},
        {"url": "/contact", "priority": "0.5"},
    ]

    # Add 1,000 grant pages
    try:
        df = pd.read_csv('data/grants.csv')
        for slug in df['slug']:
            pages.append({"url": f"/grant/{slug}", "priority": "0.8"})
    except Exception as e:
        print(f"Error loading grants: {e}")

    # Add 20 authority articles
    try:
        with open('data/articles.json', 'r') as f:
            articles = json.load(f)
            for slug in articles.keys():
                pages.append({"url": f"/resources/{slug}", "priority": "0.7"})
    except Exception as e:
        print(f"Error loading articles: {e}")

    # Build XML
    sitemap_xml = '<?xml version="1.0" encoding="UTF-8"?>\n'
    sitemap_xml += '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'

    for page in pages:
        sitemap_xml += '  <url>\n'
        sitemap_xml += f'    <loc>{base_url}{page["url"]}</loc>\n'
        sitemap_xml += f'    <lastmod>{datetime.now().strftime("%Y-%m-%d")}</lastmod>\n'
        sitemap_xml += f'    <priority>{page["priority"]}</priority>\n'
        sitemap_xml += '  </url>\n'

    sitemap_xml += '</urlset>'

    # Save to static folder
    with open('static/sitemap.xml', 'w') as f:
        f.write(sitemap_xml)
    print("Successfully generated static/sitemap.xml!")


if __name__ == "__main__":
    generate_sitemap()