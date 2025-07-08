🌍 World News Hub
A modern, responsive Flask web application for browsing and searching world news with a beautiful UI and read-later functionality.

🚀 Features
🌟 Core
Real-time News – Get the latest headlines from around the world.

Search Functionality – Find news by topics, keywords, or specific terms.

Read Later – Save articles (stored in session memory) for later reading.

Responsive Design – Mobile-friendly, modern interface.

PDF Export – Save or print articles as PDFs.

Rate Limiting – API rate limiting for performance and stability.

🎨 UI/UX
Gradient-based modern design with smooth animations.

Hover effects and interactive elements.

Keyboard navigation (e.g., Ctrl/Cmd + K to focus search).

Scroll animations for a seamless experience.

Error handling with user-friendly feedback.

Loading states and toast notifications.

📰 News Options
Categories: General, Business, Entertainment, Health, Science, Sports, Technology.

Supports multiple countries and languages.

Fallback images for missing media.

Source and publish date attribution.

Responsive grid layout for browsing.

🧰 Tech Stack
Backend: Flask (Python)

Frontend: HTML5, CSS3, JavaScript (ES6+)

Styling: Custom CSS (modern patterns)

Icons: Font Awesome 6.0

API: NewsAPI.org

Deployment: Works on any Flask-compatible host

⚙️ Installation
Prerequisites
Python 3.7+

pip

News API key from newsapi.org

Steps
Clone Repository

git clone <repository-url>
cd world-news-hub
Create Virtual Environment

python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
Install Dependencies

pip install -r requirements.txt
Set Environment Variables
Create a .env file:

NEWS_API_KEY=your_news_api_key
SECRET_KEY=your_secret_key
FLASK_ENV=development
Run the App

python app.py
View in Browser
Visit: http://localhost:5000

🔧 Configuration
Environment Variables
Variable	Required	Default	Description
NEWS_API_KEY	✅ Yes	—	NewsAPI key
SECRET_KEY	❌ No	Auto-generated	Flask session security key
FLASK_ENV	❌ No	production	Use development for debug mode

🌐 API Usage
Endpoints
GET /api/news?q=query&country=us&category=general&language=en&pageSize=20

GET /health – Health check endpoint

🔍 Search System
Real-time filtering across articles

Filters by relevance, popularity, or date

Supports advanced queries

Caching for performance improvement

🔖 Read Later
Stored in session memory (no database needed)

Persistent during the session

Easy to remove saved items

📱 Responsive Design
Mobile-first layout

Tablet and desktop optimization

Touch-friendly UI

Smooth transitions and interactions

🛡️ Error Handling & Security
Friendly API error messages

Rate limiting (100 requests/hour/IP)

404 & 500 error pages

Input validation & sanitization

CSRF & XSS protection

Secure environment variable usage

🐳 Deployment
Local

export FLASK_ENV=development
python app.py
Gunicorn (Production)

pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
Docker
dockerfile

FROM python:3.9-slim
WORKDIR /app
 requirements.txt .
RUN pip install -r requirements.txt

EXPOSE 5000
CMD ["python", "app.py"]
🌐 Supported
Countries:
US, GB, CA, AU, IN, DE, FR, IT, JP, KR, CN, BR, MX, AR, EG, NG, ZA, RU, PK

Languages:
Arabic, German, English, Spanish, French, Hebrew, Italian, Dutch, Norwegian, Portuguese, Russian, Swedish, Chinese

📊 API Rate Limits
Plan	Limit
Free	1,000 requests/month
Developer	50,000 requests/month
Business	500,000 requests/month

Client-side rate limiting is enforced: 100 requests/hour per IP.

✅ Browser Support
Chrome 80+

Firefox 78+

Safari 14+

Edge 80+

Major mobile browsers (iOS, Android)

🤝 Contributing
Fork the repo

Create a new feature branch

Make your changes

Add relevant tests

Submit a pull request

📄 License
MIT License – see LICENSE for details.

🆘 Support
Check the built-in documentation

Browse or open GitHub issues

Submit detailed bug reports or feature requests

📦 Changelog
v1.0.0
Initial release

Headline search & filtering

Read Later

Responsive design

Rate limiting

Author: MARYAM FATIMA
Contact: maryamfatima6766@gmail.com
Project: World News Hub
