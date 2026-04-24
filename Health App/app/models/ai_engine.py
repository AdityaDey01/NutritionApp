import json
import math
import random
from datetime import datetime, timedelta
from pathlib import Path

DATA_DIR = Path(__file__).parent.parent / "data"

def load_food_db():
    with open(DATA_DIR / "food_database.json", encoding="utf-8") as f:
        return json.load(f)

def load_user_profiles():
    with open(DATA_DIR / "user_profiles.json", encoding="utf-8") as f:
        return json.load(f)

# ─────────────────────────────────────────────
#  SMART FOOD SCORING ENGINE
# ─────────────────────────────────────────────

def calculate_food_score(food: dict) -> dict:
    """
    Compute a 0-100 Smart Food Score based on:
    protein, fiber, sugar, calories, processing level, health impact.
    """
    score = 0

    # 1. Protein bonus (max 25 pts)
    protein = food.get("protein", 0)
    score += min(protein * 0.8, 25)

    # 2. Fiber bonus (max 20 pts)
    fiber = food.get("fiber", 0)
    score += min(fiber * 2, 20)

    # 3. Sugar penalty (max -20 pts)
    sugar = food.get("sugar", 0)
    score -= min(sugar * 0.5, 20)

    # 4. Calorie balance (max 20 pts)
    calories = food.get("calories", 0)
    if calories <= 300:
        score += 20
    elif calories <= 500:
        score += 12
    elif calories <= 700:
        score += 5
    else:
        score -= 5

    # 5. Processing level penalty (max -25 pts)
    proc = food.get("processing_level", 3)
    proc_penalty = {1: 0, 2: -5, 3: -12, 4: -20, 5: -30}
    score += proc_penalty.get(proc, -15)

    # 6. Health impact bonus (max 15 pts)
    base_health = food.get("health_score", 50)
    score += (base_health / 100) * 15

    # Clamp to 0-100
    final_score = max(0, min(100, round(score)))

    grade = "A+" if final_score >= 90 else \
            "A"  if final_score >= 80 else \
            "B"  if final_score >= 65 else \
            "C"  if final_score >= 50 else \
            "D"  if final_score >= 35 else "F"

    color = "#00C896" if final_score >= 80 else \
            "#F5A623" if final_score >= 60 else \
            "#E8445A"

    return {"score": final_score, "grade": grade, "color": color}


# ─────────────────────────────────────────────
#  RECOMMENDATION ENGINE
# ─────────────────────────────────────────────

def get_recommendations(meal_query: str, diet_pref: str, health_goal: str,
                         budget: str, meal_time: str, stress_level: str = "normal",
                         workout_day: bool = False) -> dict:
    db = load_food_db()
    foods = db["foods"]

    scored = []
    query_lower = meal_query.lower()

    for food in foods:
        match_score = 0

        # Diet filter
        if diet_pref and diet_pref != "any":
            if diet_pref in food.get("diet_types", []):
                match_score += 30

        # Budget filter
        budget_map = {"low": ["low"], "medium": ["low", "medium"], "high": ["low", "medium", "high"]}
        if food.get("budget_level") in budget_map.get(budget, ["low", "medium", "high"]):
            match_score += 15

        # Meal time
        if meal_time and meal_time in food.get("meal_time", []):
            match_score += 20

        # Goal alignment
        goal_rules = {
            "weight_loss": lambda f: f["calories"] < 350 and f["protein"] > 15,
            "muscle_gain": lambda f: f["protein"] > 20,
            "heart_health": lambda f: f["fat"] < 10 and f["fiber"] > 4,
            "energy_boost": lambda f: f["carbs"] > 20 and f["fiber"] > 3,
            "gut_health": lambda f: f["fiber"] > 5
        }
        if health_goal in goal_rules and goal_rules[health_goal](food):
            match_score += 25

        # Workout day: boost protein foods
        if workout_day and food["protein"] > 20:
            match_score += 10

        # Stress: boost comfort + low-sugar
        if stress_level == "high" and "comfort" in food.get("tags", []):
            match_score += 10
        if stress_level == "high" and food["sugar"] < 5:
            match_score += 5

        # Health score base
        match_score += food.get("health_score", 50) * 0.3

        scored.append({**food, "match_score": round(match_score)})

    # Sort by match score then health_score
    scored.sort(key=lambda x: (x["match_score"], x["health_score"]), reverse=True)
    top = scored[:5]

    # Attach smart food score
    for item in top:
        item["smart_score"] = calculate_food_score(item)

    # Contextual insight
    time_map = {
        "breakfast": "Starting your day with high-fiber and protein keeps energy stable.",
        "lunch": "A balanced lunch prevents afternoon energy crashes.",
        "dinner": "Light dinners support better sleep and fat metabolism.",
        "snack": "Smart snacking keeps metabolism active between meals."
    }
    insight = time_map.get(meal_time, "Balanced nutrition is key at every meal.")

    if workout_day:
        insight += " Post-workout: prioritize protein within 30 minutes."

    return {
        "recommendations": top,
        "insight": insight,
        "query": meal_query,
        "context": {
            "meal_time": meal_time,
            "diet": diet_pref,
            "goal": health_goal,
            "workout_day": workout_day,
            "stress_level": stress_level
        }
    }


def get_healthier_alternatives(food_id: int) -> list:
    db = load_food_db()
    alt_map = db.get("meal_alternatives", {})
    foods_by_id = {f["id"]: f for f in db["foods"]}
    alt_ids = alt_map.get(str(food_id), [])
    return [foods_by_id[i] for i in alt_ids if i in foods_by_id]


def get_mood_suggestions(mood: str) -> list:
    db = load_food_db()
    mood_map = db.get("mood_food_map", {})
    foods_by_id = {f["id"]: f for f in db["foods"]}
    ids = mood_map.get(mood, [])
    suggestions = [foods_by_id[i] for i in ids if i in foods_by_id]
    for s in suggestions:
        s["smart_score"] = calculate_food_score(s)
    return suggestions


def get_weather_suggestions(weather: str) -> list:
    db = load_food_db()
    weather_map = db.get("weather_food_map", {})
    foods_by_id = {f["id"]: f for f in db["foods"]}
    ids = weather_map.get(weather, [])
    suggestions = [foods_by_id[i] for i in ids if i in foods_by_id]
    for s in suggestions:
        s["smart_score"] = calculate_food_score(s)
    return suggestions


# ─────────────────────────────────────────────
#  MEAL LOG ENGINE
# ─────────────────────────────────────────────

_journal_cache = None

def generate_weekly_journal():
    """Simulate 7 days of meal logs."""
    global _journal_cache
    if _journal_cache is not None:
        return _journal_cache

    days = []
    food_db = load_food_db()
    foods = food_db["foods"]
    healthy = [f for f in foods if f["health_score"] >= 75]
    all_foods = foods

    for i in range(7):
        date = (datetime.now() - timedelta(days=6 - i)).strftime("%Y-%m-%d")
        weekday = (datetime.now() - timedelta(days=6 - i)).strftime("%A")
        breakfast = random.choice([f for f in healthy if "breakfast" in f["meal_time"]])
        lunch = random.choice([f for f in all_foods if "lunch" in f["meal_time"]])
        dinner = random.choice([f for f in all_foods if "dinner" in f["meal_time"]])
        snack = random.choice([f for f in foods if "snack" in f["meal_time"]])

        total_cal = breakfast["calories"] + lunch["calories"] + dinner["calories"] + snack["calories"]
        total_protein = breakfast["protein"] + lunch["protein"] + dinner["protein"]
        avg_score = round((breakfast["health_score"] + lunch["health_score"] + dinner["health_score"]) / 3)
        water = random.randint(4, 10)

        days.append({
            "date": date,
            "weekday": weekday,
            "meals": {
                "breakfast": breakfast,
                "lunch": lunch,
                "dinner": dinner,
                "snack": snack
            },
            "totals": {
                "calories": total_cal,
                "protein": total_protein,
                "water_glasses": water,
                "health_score": avg_score
            }
        })

    _journal_cache = days
    return days


def get_weekly_insights(journal: list) -> dict:
    """Aggregate insights from the weekly journal."""
    avg_cal = round(sum(d["totals"]["calories"] for d in journal) / len(journal))
    avg_protein = round(sum(d["totals"]["protein"] for d in journal) / len(journal))
    avg_water = round(sum(d["totals"]["water_glasses"] for d in journal) / len(journal), 1)
    avg_score = round(sum(d["totals"]["health_score"] for d in journal) / len(journal))

    best_day = max(journal, key=lambda d: d["totals"]["health_score"])
    worst_day = min(journal, key=lambda d: d["totals"]["health_score"])

    return {
        "avg_calories": avg_cal,
        "avg_protein": avg_protein,
        "avg_water": avg_water,
        "avg_health_score": avg_score,
        "best_day": best_day["weekday"],
        "worst_day": worst_day["weekday"],
        "trend": "improving" if journal[-1]["totals"]["health_score"] > journal[0]["totals"]["health_score"] else "declining"
    }


# ─────────────────────────────────────────────
#  GROCERY PLANNER ENGINE
# ─────────────────────────────────────────────

WEEKLY_MEAL_PLANS = {
    "balanced": {
        "name": "Balanced Nutrition Plan",
        "description": "A well-rounded plan covering all macros",
        "days": [
            {"breakfast": "Oatmeal with Berries", "lunch": "Quinoa Bowl", "dinner": "Grilled Chicken Breast", "snack": "Mixed Nuts"},
            {"breakfast": "Egg White Omelette", "lunch": "Turkey & Veggie Wrap", "dinner": "Salmon Fillet", "snack": "Greek Yogurt Parfait"},
            {"breakfast": "Avocado Toast", "lunch": "Veggie Stir Fry", "dinner": "Brown Rice & Lentils", "snack": "Fruit Salad"},
            {"breakfast": "Greek Yogurt Parfait", "lunch": "Caesar Salad with Chicken", "dinner": "Chickpea Curry", "snack": "Mixed Nuts"},
            {"breakfast": "Oatmeal with Berries", "lunch": "Sweet Potato & Black Bean Bowl", "dinner": "Grilled Tofu Salad", "snack": "Protein Smoothie"},
            {"breakfast": "Chocolate Smoothie Bowl", "lunch": "Whole Grain Pasta Primavera", "dinner": "Salmon Fillet", "snack": "Fruit Salad"},
            {"breakfast": "Egg White Omelette", "lunch": "Quinoa Bowl", "dinner": "Tempeh Steak", "snack": "Greek Yogurt Parfait"}
        ]
    },
    "vegan": {
        "name": "Plant-Powered Plan",
        "description": "100% plant-based meals full of nutrients",
        "days": [
            {"breakfast": "Oatmeal with Berries", "lunch": "Quinoa Bowl", "dinner": "Chickpea Curry", "snack": "Mixed Nuts"},
            {"breakfast": "Avocado Toast", "lunch": "Sweet Potato & Black Bean Bowl", "dinner": "Veggie Stir Fry", "snack": "Fruit Salad"},
            {"breakfast": "Chocolate Smoothie Bowl", "lunch": "Grilled Tofu Salad", "dinner": "Brown Rice & Lentils", "snack": "Mixed Nuts"},
            {"breakfast": "Acai Bowl", "lunch": "Veggie Stir Fry", "dinner": "Tempeh Steak", "snack": "Fruit Salad"},
            {"breakfast": "Oatmeal with Berries", "lunch": "Quinoa Bowl", "dinner": "Chickpea Curry", "snack": "Mixed Nuts"},
            {"breakfast": "Avocado Toast", "lunch": "Sweet Potato & Black Bean Bowl", "dinner": "Grilled Tofu Salad", "snack": "Protein Smoothie"},
            {"breakfast": "Chocolate Smoothie Bowl", "lunch": "Brown Rice & Lentils", "dinner": "Veggie Stir Fry", "snack": "Fruit Salad"}
        ]
    },
    "keto": {
        "name": "Keto Performance Plan",
        "description": "Low-carb, high-fat for ketosis and fat burning",
        "days": [
            {"breakfast": "Egg White Omelette", "lunch": "Caesar Salad with Chicken", "dinner": "Salmon Fillet", "snack": "Mixed Nuts"},
            {"breakfast": "Egg White Omelette", "lunch": "Grilled Chicken Breast", "dinner": "Tempeh Steak", "snack": "Mixed Nuts"},
            {"breakfast": "Egg White Omelette", "lunch": "Grilled Tofu Salad", "dinner": "Salmon Fillet", "snack": "Bone Broth Soup"},
            {"breakfast": "Egg White Omelette", "lunch": "Caesar Salad with Chicken", "dinner": "Grilled Chicken Breast", "snack": "Mixed Nuts"},
            {"breakfast": "Egg White Omelette", "lunch": "Salmon Fillet", "dinner": "Tempeh Steak", "snack": "Bone Broth Soup"},
            {"breakfast": "Egg White Omelette", "lunch": "Grilled Chicken Breast", "dinner": "Grilled Tofu Salad", "snack": "Mixed Nuts"},
            {"breakfast": "Egg White Omelette", "lunch": "Caesar Salad with Chicken", "dinner": "Salmon Fillet", "snack": "Bone Broth Soup"}
        ]
    }
}

GROCERY_LISTS = {
    "balanced": {
        "produce": ["Spinach (1 bag)", "Broccoli (2 heads)", "Sweet potatoes (4)", "Avocados (3)", "Mixed berries (2 cups)", "Bananas (6)", "Cherry tomatoes (1 pint)", "Bell peppers (3)"],
        "protein": ["Chicken breast (1.5 kg)", "Salmon fillets (4 pieces)", "Eggs (1 dozen)", "Greek yogurt (500g)", "Black beans (2 cans)"],
        "grains": ["Rolled oats (500g)", "Quinoa (400g)", "Whole grain bread (1 loaf)", "Brown rice (500g)", "Whole grain pasta (400g)"],
        "pantry": ["Olive oil (1 bottle)", "Almond butter (1 jar)", "Mixed nuts (200g)", "Chickpeas (2 cans)", "Lentils (500g)"],
        "estimated_cost": "$85-$105"
    },
    "vegan": {
        "produce": ["Spinach (2 bags)", "Kale (1 bunch)", "Sweet potatoes (6)", "Avocados (4)", "Mixed berries (3 cups)", "Broccoli (2 heads)", "Zucchini (3)", "Mushrooms (400g)"],
        "protein": ["Firm tofu (600g)", "Tempeh (400g)", "Black beans (3 cans)", "Lentils (500g)", "Chickpeas (3 cans)"],
        "grains": ["Rolled oats (500g)", "Quinoa (500g)", "Brown rice (500g)", "Whole grain bread (1 loaf)"],
        "pantry": ["Coconut oil (1 jar)", "Nutritional yeast (200g)", "Mixed nuts (300g)", "Tahini (1 jar)", "Soy sauce (1 bottle)"],
        "estimated_cost": "$70-$90"
    },
    "keto": {
        "produce": ["Spinach (2 bags)", "Avocados (6)", "Broccoli (3 heads)", "Cauliflower (1 head)", "Zucchini (4)", "Bell peppers (4)", "Mushrooms (400g)"],
        "protein": ["Chicken breast (2 kg)", "Salmon fillets (6 pieces)", "Eggs (2 dozen)", "Ground turkey (500g)", "Tuna (4 cans)"],
        "grains": ["Almond flour (500g)", "Flaxseed meal (200g)"],
        "pantry": ["Olive oil (1 large bottle)", "Coconut oil (1 jar)", "Mixed nuts (400g)", "Butter (250g)", "Bone broth (4 cups)"],
        "estimated_cost": "$95-$120"
    }
}


def get_meal_plan(diet_type: str = "balanced") -> dict:
    plan = WEEKLY_MEAL_PLANS.get(diet_type, WEEKLY_MEAL_PLANS["balanced"])
    grocery = GROCERY_LISTS.get(diet_type, GROCERY_LISTS["balanced"])
    return {"meal_plan": plan, "grocery_list": grocery}


# ─────────────────────────────────────────────
#  AI COACH ENGINE
# ─────────────────────────────────────────────

COACH_RESPONSES = {
    "protein": {
        "keywords": ["protein", "muscle", "strength", "building"],
        "response": "🥩 **Protein Power!** Aim for 1.6-2.2g of protein per kg of body weight daily. Great sources include chicken breast, salmon, eggs, Greek yogurt, lentils, and tofu. Spread protein across all meals for optimal muscle protein synthesis.",
        "tip": "Try adding a protein shake post-workout — within 30 minutes is the golden window! 💪"
    },
    "weight_loss": {
        "keywords": ["lose weight", "weight loss", "fat", "slim", "diet", "cutting"],
        "response": "⚖️ **Smart Weight Loss Strategy!** Create a 300-500 calorie deficit through a combination of diet and exercise. Focus on high-protein, high-fiber foods that keep you satiated. Avoid extreme restriction — sustainability is key!",
        "tip": "Eat 80% of your meals at home. You'll control ingredients and portions much better! 🏠"
    },
    "energy": {
        "keywords": ["energy", "tired", "fatigue", "sluggish", "afternoon crash"],
        "response": "⚡ **Boost Your Energy!** Stable blood sugar is your best friend. Eat complex carbs + protein at every meal. Avoid high-sugar foods that cause crashes. Stay hydrated — even 2% dehydration reduces energy by 20%!",
        "tip": "Try eating smaller meals every 3-4 hours instead of 3 large meals for consistent energy. 🔋"
    },
    "gut": {
        "keywords": ["gut", "digestion", "bloating", "stomach", "probiotic", "fiber"],
        "response": "🦠 **Gut Health is Foundation Health!** Your gut microbiome affects immunity, mood, and metabolism. Eat fermented foods (yogurt, kimchi, kefir), high-fiber vegetables, and prebiotic foods (garlic, onions, bananas).",
        "tip": "Aim for 30 different plant foods per week — this dramatically improves gut diversity! 🌿"
    },
    "sleep": {
        "keywords": ["sleep", "insomnia", "rest", "night"],
        "response": "😴 **Nutrition for Better Sleep!** Avoid heavy meals 3 hours before bed. Foods rich in tryptophan (turkey, milk, oats) support melatonin production. Limit caffeine after 2pm and alcohol before sleep.",
        "tip": "A small handful of almonds or a banana before bed can actually help you sleep better! 🌙"
    },
    "hydration": {
        "keywords": ["water", "hydration", "drink", "thirsty"],
        "response": "💧 **Hydration is Everything!** Aim for 35ml per kg of body weight daily. Drink a large glass of water first thing in the morning. Herbal teas count! Food also provides ~20% of daily fluid intake.",
        "tip": "Keep a water bottle visible at your desk — you'll drink 30% more just by seeing it! 🫗"
    },
    "general": {
        "keywords": [],
        "response": "🤖 **NutriSmart AI Coach here!** I'm designed to give you personalized nutrition guidance. Some key principles for healthy eating:\n\n1. **Eat the rainbow** — diverse colors mean diverse nutrients\n2. **Prioritize whole foods** — minimize ultra-processed items\n3. **Stay hydrated** — often hunger is actually thirst\n4. **Plan ahead** — meal prep is your superpower\n5. **Progress, not perfection** — consistency beats intensity!",
        "tip": "What specific nutrition goal can I help you with today? 🎯"
    }
}

def get_coach_response(message: str) -> dict:
    message_lower = message.lower()

    for topic, data in COACH_RESPONSES.items():
        if any(kw in message_lower for kw in data["keywords"]):
            return {
                "response": data["response"],
                "tip": data["tip"],
                "topic": topic
            }

    return {
        "response": COACH_RESPONSES["general"]["response"],
        "tip": COACH_RESPONSES["general"]["tip"],
        "topic": "general"
    }


# ─────────────────────────────────────────────
#  DASHBOARD AGGREGATOR
# ─────────────────────────────────────────────

def get_dashboard_data(user_id: str = "demo_user") -> dict:
    profiles = load_user_profiles()
    user = profiles.get(user_id, profiles["demo_user"])
    habits = profiles.get("habits", [])
    challenges = profiles.get("challenges", [])
    leaderboard = profiles.get("leaderboard", [])

    now = datetime.now()
    hour = now.hour

    if 5 <= hour < 12:
        meal_time = "breakfast"
        greeting = "Good Morning"
    elif 12 <= hour < 17:
        meal_time = "lunch"
        greeting = "Good Afternoon"
    elif 17 <= hour < 21:
        meal_time = "dinner"
        greeting = "Good Evening"
    else:
        meal_time = "snack"
        greeting = "Good Night"

    # Simulated today's intake
    today_calories = 1340
    today_protein = 98
    today_water = 6
    today_fiber = 18

    return {
        "user": user,
        "greeting": greeting,
        "meal_time": meal_time,
        "today": {
            "calories_consumed": today_calories,
            "calories_remaining": user["daily_calorie_target"] - today_calories,
            "protein_g": today_protein,
            "water_glasses": today_water,
            "fiber_g": today_fiber,
            "health_score": user["health_score"]
        },
        "habits": habits,
        "challenges": challenges[:3],
        "leaderboard": leaderboard,
        "streak": user["streak_days"],
        "points": user["points"],
        "level": user["level"],
        "badges": user["badges"]
    }
