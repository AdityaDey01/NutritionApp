# 🥗 NutriSmart AI — Intelligent Food & Health Assistant

> **Award-winning hackathon project** combining AI personalization, behavioral analytics, and nutrition intelligence to help individuals make smarter food choices and build lasting healthy habits.

[![Python](https://img.shields.io/badge/Python-3.11-blue)](https://python.org)
[![Flask](https://img.shields.io/badge/Flask-3.0-green)](https://flask.palletsprojects.com)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow)](LICENSE)

---

## 🚀 Problem Statement

Over **60% of chronic diseases** are linked to poor dietary choices. Despite abundant food apps, people still struggle with:
- Making real-time, contextual food decisions
- Getting personalized (not generic) nutrition guidance
- Building consistent healthy eating habits long-term
- Understanding the true health impact of their food choices

## 💡 Solution Innovation

NutriSmart AI combines **rule-based AI**, **behavioral insights**, and **gamification** to create a unified intelligent nutrition companion. Instead of just logging meals, it:

1. **Scores every food** using our proprietary Smart Food Score algorithm
2. **Recommends contextually** — based on mood, weather, workout status, stress
3. **Builds habits** through gamification and behavioral psychology
4. **Coaches proactively** via a 24/7 AI nutrition coach

## ✨ Unique Value Proposition

> *"NutriSmart AI is not just a food tracker — it's an intelligent behavioral health system that learns your patterns and nudges you toward better choices every single day."*

---

## 🏗️ Architecture

```
nutrismart-ai/
├── app/
│   ├── routes/          # Flask blueprints (9 modules)
│   │   ├── main.py      # Landing page
│   │   ├── dashboard.py # Health dashboard
│   │   ├── recommender.py # AI food recommender
│   │   ├── tracker.py   # Meal journal
│   │   ├── habits.py    # Habit + gamification
│   │   ├── grocery.py   # Meal plan + shopping
│   │   ├── coach.py     # AI chat coach
│   │   ├── profile.py   # User profile
│   │   └── insights.py  # Analytics + restaurants
│   ├── models/
│   │   └── ai_engine.py # Core AI & recommendation engine
│   ├── data/
│   │   ├── food_database.json   # 25 foods with full nutrition
│   │   └── user_profiles.json  # User, habits, challenges, leaderboard
│   ├── templates/       # Jinja2 HTML templates
│   └── static/          # CSS design system + JS
├── tests/test_app.py    # Pytest test suite
├── app.py               # Entry point
├── requirements.txt
├── Dockerfile
└── Procfile
```

---

## 🤖 AI Features

### Smart Food Score Algorithm
Scores meals 0–100 based on:
- Protein content (+25 pts)
- Fiber content (+20 pts)
- Sugar content (penalty)
- Calorie density
- Processing level (1=whole food, 5=ultra-processed)
- Baseline health impact

### Recommendation Engine
Context inputs:
- Meal query, diet preference, health goal
- Budget, meal time, stress level, workout day
- Mood, weather

### AI Nutrition Coach
Rule-based intent detection for: protein, weight loss, energy, gut health, sleep, hydration

---

## 📱 Pages

| Page | URL | Description |
|------|-----|-------------|
| Landing | `/` | Hero + features showcase |
| Dashboard | `/dashboard/` | Health score, habits, streaks, leaderboard |
| AI Recommender | `/recommender/` | Food recommendations, mood/weather engine, meal scanner |
| Meal Tracker | `/tracker/` | 7-day food journal, log meals |
| Habit Builder | `/habits/` | Habits, challenges, badges, leaderboard |
| Grocery Planner | `/grocery/` | Weekly meal plans, shopping lists |
| AI Coach | `/coach/` | Chat with NutriBot |
| Insights | `/insights/` | Charts, behavioral analytics, restaurant finder |
| Profile | `/profile/` | Settings, targets, future roadmap |

---

## ⚡ Quick Start

```bash
# Clone / navigate to project
cd "Health App"

# Install dependencies
pip install -r requirements.txt

# Run development server
python app.py
```

Open **http://127.0.0.1:5000** in your browser.

---

## 🧪 Testing

```bash
pip install pytest
pytest tests/ -v
```

---

## 🐳 Docker

```bash
docker build -t nutrismart-ai .
docker run -p 5000:5000 nutrismart-ai
```

---

## 🚀 Deployment (Render / Railway / Heroku)

The `Procfile` is included for one-click deployment:
```
web: gunicorn app:app
```

---

## 🔮 Future Roadmap

- **Computer Vision** — Photo-based meal recognition (OpenAI Vision)
- **LLM Nutrition Agent** — GPT-4 powered deep coaching
- **Voice Coach** — Whisper ASR + TTS for hands-free guidance
- **Wearable Integration** — Fitbit, Apple Watch, Garmin
- **Health API Integrations** — MyFitnessPal, Cronometer
- **Social Features** — Team challenges, friend nutrition sharing

---

## 🏆 Why This Wins Hackathons

1. **Complete product** — 9 pages, 7 modules, real working AI
2. **Beautiful UI** — Premium dark mode health-tech design
3. **Real AI logic** — Scoring engine, recommendation engine, coach
4. **Behavioral science** — Gamification, streaks, social proof
5. **Scalable architecture** — Clean blueprint structure, SQLite→PostgreSQL ready
6. **Clear impact** — Addresses a real, widespread health problem

---

*Built with ❤️ for the Health AI Hackathon 2026 | NutriSmart AI Team*
