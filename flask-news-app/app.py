from flask import Flask, render_template, request, jsonify
from markupsafe import escape
import os
import requests
from datetime import datetime
import logging
import sys
from functools import wraps
import time

app = Flask(__name__)

# Environment validation
def validate_environment():
    """Validate required environment variables"""
    required_vars = []  # No required vars since we provide defaults
    missing_vars = [var for var in required_vars if not os.environ.get(var)]

    if missing_vars:
        logging.error(f"Missing required environment variables: {', '.join(missing_vars)}")
        sys.exit(1)

# Validate environment on startup
validate_environment()

# Configuration
app.secret_key = os.environ.get("SECRET_KEY", "some_default_secret")

NEWS_API_KEY = os.environ.get("NEWS_API_KEY", "d91b0e6c6c8a4cb5a650552269fba7da")
if not NEWS_API_KEY:
    logging.error("NEWS_API_KEY environment variable is not set")

NEWS_API_URL = "https://newsapi.org/v2/top-headlines"
SEARCH_API_URL = "https://newsapi.org/v2/everything"

request_history = {}
RATE_LIMIT_PER_HOUR = 100

def rate_limit(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        client_ip = request.remote_addr
        current_time = time.time()

        if client_ip in request_history:
            request_history[client_ip] = [
                req_time for req_time in request_history[client_ip]
                if current_time - req_time < 3600
            ]
        else:
            request_history[client_ip] = []

        if len(request_history[client_ip]) >= RATE_LIMIT_PER_HOUR:
            return jsonify({"error": "Rate limit exceeded"}), 429

        request_history[client_ip].append(current_time)
        return f(*args, **kwargs)
    return decorated_function

def validate_news_params(country=None, category=None, language=None, page_size=None):
    valid_countries = ['us', 'gb', 'ca', 'au', 'in', 'de', 'fr', 'it', 'jp', 'kr', 'cn', 'br', 'mx', 'ar', 'eg', 'ng', 'za', 'ru', 'pk']
    valid_categories = ['general', 'business', 'entertainment', 'health', 'science', 'sports', 'technology']
    valid_languages = ['ar', 'de', 'en', 'es', 'fr', 'he', 'it', 'nl', 'no', 'pt', 'ru', 'se', 'zh']

    if country and country not in valid_countries:
        country = 'us'
    if category and category not in valid_categories:
        category = 'general'
    if language and language not in valid_languages:
        language = 'en'
    if page_size:
        try:
            page_size = int(page_size)
            page_size = min(max(1, page_size), 100)
        except (ValueError, TypeError):
            page_size = 20

    return country or 'us', category or 'general', language or 'en', page_size or 20

def fetch_news(country="us", category="general", language="en", page_size=20):
    country, category, language, page_size = validate_news_params(country, category, language, page_size)
    params = {
        "apiKey": NEWS_API_KEY,
        "pageSize": page_size,
        "sortBy": "publishedAt",
        "language": language,
        "country": country,
        "category": category
    }
    headers = {'User-Agent': 'WorldNewsHub/1.0'}
    try:
        response = requests.get(NEWS_API_URL, params=params, headers=headers, timeout=5)
        response.raise_for_status()
        data = response.json()
        if data.get("status") != "ok":
            return {"status": "error", "articles": [], "message": data.get("message", "Unknown API error")}
        articles = [
            article for article in data.get("articles", [])
            if article.get("title") and article.get("url") and article.get("title") != "[Removed]" and article.get("source", {}).get("name")
        ]
        return {"status": "ok", "articles": articles, "totalResults": len(articles)}
    except Exception as e:
        logging.error(f"Error fetching news: {e}")
        return {"status": "error", "articles": [], "message": str(e)}

def search_news(query, language="en", page_size=20):
    if not query or not isinstance(query, str):
        return {"status": "error", "articles": [], "message": "Invalid search query"}

    query = query.strip()[:500]
    _, _, language, page_size = validate_news_params(language=language, page_size=page_size)
    params = {
        "apiKey": NEWS_API_KEY,
        "q": query,
        "sortBy": "publishedAt",
        "language": language,
        "pageSize": page_size
    }
    headers = {'User-Agent': 'WorldNewsHub/1.0'}
    try:
        response = requests.get(SEARCH_API_URL, params=params, headers=headers, timeout=5)
        response.raise_for_status()
        data = response.json()
        if data.get("status") != "ok":
            return {"status": "error", "articles": [], "message": data.get("message", "Search failed")}
        articles = [
            article for article in data.get("articles", [])
            if article.get("title") and article.get("url") and article.get("title") != "[Removed]" and article.get("source", {}).get("name")
        ]
        return {"status": "ok", "articles": articles}
    except Exception as e:
        logging.error(f"Search error: {e}")
        return {"status": "error", "articles": [], "message": str(e)}

def format_date(date_string):
    try:
        dt = datetime.fromisoformat(date_string.replace("Z", "+00:00"))
        return dt.strftime("%B %d, %Y %I:%M %p")
    except Exception:
        return date_string or "Unknown date"

def sanitize_for_js(text):
    if not text:
        return ""
    text = str(text).replace("\\", "\\\\").replace("'", "\\'").replace('"', '\\"')
    return text.replace("\n", "\\n").replace("\r", "\\r")

@app.route("/")
@rate_limit
def index():
    search_query = request.args.get("search", "").strip()
    if search_query and len(search_query) > 500:
        search_query = search_query[:500]

    news_data = {
        "general_news": [],
        "search_results": [],
        "search_query": search_query if search_query else None,
        "api_error": None,
    }

    try:
        if search_query:
            results = search_news(search_query, language="en")
            news_data["search_results"] = results.get("articles", [])
            if results.get("status") != "ok":
                news_data["api_error"] = results.get("message")
        else:
            results = fetch_news()
            news_data["general_news"] = results.get("articles", [])
            if results.get("status") != "ok":
                news_data["api_error"] = results.get("message")
    except Exception as e:
        logging.error(f"Unexpected error: {e}")
        news_data["api_error"] = "An unexpected error occurred"

    return render_template("index.html", format_date=format_date, sanitize_for_js=sanitize_for_js, **news_data)

@app.errorhandler(404)
def not_found(error):
    return "<h1>404 - Page Not Found</h1>", 404

@app.errorhandler(500)
def internal_error(error):
    return "<h1>500 - Internal Server Error</h1>", 500

@app.errorhandler(429)
def rate_limit_error(error):
    return jsonify({"error": "Rate limit exceeded. Please try again later."}), 429

@app.route("/health")
def health_check():
    return jsonify({"status": "healthy", "timestamp": datetime.now().isoformat()})

@app.route("/api/news")
@rate_limit
def api_news():
    search_query = request.args.get("q", "").strip()
    country = request.args.get("country", "us")
    category = request.args.get("category", "general")
    language = request.args.get("language", "en")
    page_size = request.args.get("pageSize", 20)
    try:
        if search_query:
            return jsonify(search_news(search_query, language, page_size))
        return jsonify(fetch_news(country, category, language, page_size))
    except Exception as e:
        logging.error(f"API error: {e}")
        return jsonify({"status": "error", "message": "Internal server error"}), 500

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    debug_mode = os.environ.get("FLASK_ENV") == "development"
    app.run(debug=debug_mode, host="0.0.0.0", port=5000)
