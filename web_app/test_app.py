import os
import tempfile
import pytest
from app import app
from database import init_db, get_db_connection
import sqlite3

@pytest.fixture
def client():
    # Configure the app for testing
    app.config['TESTING'] = True
    
    # We use the existing database logic, but could be directed to a test.db if modified.
    # For simplicity, we test the endpoints directly.
    with app.test_client() as client:
        yield client

def test_login_page_loads(client):
    """Test that the login page loads correctly."""
    response = client.get('/')
    assert response.status_code == 200
    assert b'Hospital Login' in response.data

def test_valid_login(client):
    """Test login with valid credentials."""
    response = client.post('/', data=dict(
        username='admin',
        password='admin123'
    ), follow_redirects=True)
    
    assert response.status_code == 200
    assert b'Patient List' in response.data

def test_invalid_login(client):
    """Test login with invalid credentials."""
    response = client.post('/', data=dict(
        username='wrong',
        password='user'
    ), follow_redirects=True)
    
    assert response.status_code == 200
    assert b'Invalid Username or Password' in response.data

def test_dashboard_access_without_login(client):
    """Test that accessing dashboard without login redirects to login."""
    response = client.get('/dashboard', follow_redirects=True)
    assert b'Hospital Login' in response.data

def test_add_patient(client):
    """Test adding a patient after logging in."""
    # Login first
    client.post('/', data=dict(username='admin', password='admin123'))
    
    # Add patient
    response = client.post('/add', data=dict(
        name='Test Patient',
        age='30',
        gender='Male',
        disease='Flu'
    ), follow_redirects=True)
    
    assert response.status_code == 200
    assert b'Patient Added Successfully' in response.data
    assert b'Test Patient' in response.data
