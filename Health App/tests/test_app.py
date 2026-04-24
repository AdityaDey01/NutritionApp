import pytest
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from app import create_app

@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True
    with app.test_client() as c:
        yield c

def test_landing(client):
    r = client.get('/')
    assert r.status_code == 200

def test_dashboard(client):
    r = client.get('/dashboard/')
    assert r.status_code == 200

def test_recommender_page(client):
    r = client.get('/recommender/')
    assert r.status_code == 200

def test_recommender_api(client):
    r = client.post('/recommender/search', json={
        'meal_query': 'something healthy',
        'diet_pref': 'balanced',
        'health_goal': 'weight_loss',
        'budget': 'medium',
        'meal_time': 'lunch',
        'stress_level': 'normal',
        'workout_day': False
    })
    assert r.status_code == 200
    data = r.get_json()
    assert 'recommendations' in data
    assert len(data['recommendations']) > 0

def test_coach_chat(client):
    r = client.post('/coach/chat', json={'message': 'How do I get more protein?'})
    assert r.status_code == 200
    data = r.get_json()
    assert 'response' in data

def test_mood_suggestions(client):
    r = client.post('/recommender/mood', json={'mood': 'happy'})
    assert r.status_code == 200
    data = r.get_json()
    assert 'suggestions' in data

def test_grocery_plan(client):
    r = client.get('/grocery/?diet=vegan')
    assert r.status_code == 200

def test_tracker(client):
    r = client.get('/tracker/')
    assert r.status_code == 200

def test_habits(client):
    r = client.get('/habits/')
    assert r.status_code == 200

def test_insights(client):
    r = client.get('/insights/')
    assert r.status_code == 200

def test_profile(client):
    r = client.get('/profile/')
    assert r.status_code == 200
