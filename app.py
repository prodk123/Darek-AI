from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
import sqlite3
import hashlib
import os
import datetime
import requests
from dotenv import load_dotenv
from darek_core import Darek

# Load environment variables with explicit path
try:
    load_dotenv(dotenv_path='.env')
except:
    # Fallback if dotenv fails
    pass

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'darek-ai-super-secret-key-2024-production')
app.config['PERMANENT_SESSION_LIFETIME'] = datetime.timedelta(days=7)

# Initialize Darek AI
darek = Darek()

def get_db_connection():
    """Get database connection"""
    conn = sqlite3.connect('instance/darek_ai.db')
    conn.row_factory = sqlite3.Row
    return conn

def hash_password(password):
    """Hash password using SHA256"""
    return hashlib.sha256(password.encode()).hexdigest()

def verify_password(password, hashed):
    """Verify password against hash"""
    return hash_password(password) == hashed

@app.route('/')
def index():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return render_template('index.html')

@app.route('/chat')
def chat_page():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        try:
            email = request.form['email']
            password = request.form['password']
            remember = 'remember' in request.form
            
            conn = get_db_connection()
            user = conn.execute('SELECT * FROM user WHERE email = ?', (email,)).fetchone()
            conn.close()
            
            if user and verify_password(password, user['password_hash']):
                session['user_id'] = user['id']
                session['username'] = user['username']
                session['email'] = user['email']
                
                if remember:
                    session.permanent = True
                
                flash('Welcome back!', 'success')
                return redirect(url_for('dashboard'))
            else:
                flash('Invalid email or password. Please try again.', 'danger')
                return render_template('login.html')
                
        except Exception as e:
            flash(f'An error occurred: {str(e)}', 'danger')
            return render_template('login.html')
    
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        try:
            username = request.form['username']
            email = request.form['email']
            password = request.form['password']
            
            conn = get_db_connection()
            
            # Check if user exists
            existing_user = conn.execute('SELECT id FROM user WHERE email = ? OR username = ?', 
                                       (email, username)).fetchone()
            
            if existing_user:
                conn.close()
                flash('User already exists with that email or username', 'danger')
                return render_template('signup.html')
            
            # Create new user
            password_hash = hash_password(password)
            conn.execute('INSERT INTO user (username, email, password_hash) VALUES (?, ?, ?)',
                        (username, email, password_hash))
            conn.commit()
            conn.close()
            
            flash('Your account has been created! You can now log in.', 'success')
            return redirect(url_for('login'))
            
        except Exception as e:
            flash(f'An error occurred: {str(e)}', 'danger')
            return render_template('signup.html')
    
    return render_template('signup.html')

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    conn = get_db_connection()
    
    # Get user data
    reminders = conn.execute('SELECT * FROM reminder WHERE user_id = ? ORDER BY remind_at ASC', 
                           (session['user_id'],)).fetchall()
    todos = conn.execute('SELECT * FROM todo_item WHERE user_id = ? AND completed = 0', 
                        (session['user_id'],)).fetchall()
    shopping_items = conn.execute('SELECT * FROM shopping_item WHERE user_id = ?', 
                                (session['user_id'],)).fetchall()
    notes = conn.execute('SELECT * FROM note WHERE user_id = ? ORDER BY created_at DESC', 
                        (session['user_id'],)).fetchall()
    timers = conn.execute('SELECT * FROM timer WHERE user_id = ? ORDER BY id DESC LIMIT 5', 
                         (session['user_id'],)).fetchall()
    
    conn.close()
    
    return render_template('dashboard.html', 
                         name=session['username'],
                         reminders=reminders,
                         todos=todos,
                         shopping_items=shopping_items,
                         notes=notes,
                         timers=timers)

@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out.', 'info')
    return redirect(url_for('index'))

@app.route('/chat', methods=['POST'])
def chat():
    if 'user_id' not in session:
        return jsonify({'error': 'Not authenticated'}), 401
    
    try:
        data = request.get_json()
        if not data or 'message' not in data:
            return jsonify({'message': 'Please provide a message'}), 400
            
        user_message = data['message'].strip()
        if not user_message:
            return jsonify({'message': 'Please provide a valid message'}), 400
            
        user_id = session['user_id']
        
        # Process command with Darek AI
        response_text = darek.process_command(user_message, user_id)
        
        # Ensure we have a valid response
        if not response_text or response_text.strip() == '':
            response_text = "I'm not sure how to help with that. Try asking me about weather, reminders, or other tasks!"
        
        # Log command history
        try:
            conn = get_db_connection()
            conn.execute('INSERT INTO command_history (command, user_id, success) VALUES (?, ?, ?)',
                        (user_message, user_id, True))
            conn.commit()
            conn.close()
        except:
            pass  # Continue even if logging fails
        
        return jsonify({'message': response_text})
        
    except Exception as e:
        return jsonify({'message': f"Sorry, I encountered an error: {str(e)}"}), 500

@app.route('/weather')
def get_weather():
    if 'user_id' not in session:
        return jsonify({'error': 'Not authenticated'}), 401
    
    city = request.args.get('city', 'London')
    api_key = os.getenv('WEATHER_API_KEY')
    
    if not api_key or api_key == 'YOUR_API_KEY_HERE':
        return jsonify({'error': 'Weather API key not configured'}), 500
    
    try:
        url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric'
        response = requests.get(url)
        data = response.json()
        
        if response.status_code == 200:
            weather_info = {
                'city': data['name'],
                'temperature': data['main']['temp'],
                'description': data['weather'][0]['description'],
                'humidity': data['main']['humidity'],
                'wind_speed': data['wind']['speed']
            }
            return jsonify(weather_info)
        else:
            return jsonify({'error': 'Weather data not found'}), 404
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/news')
def get_news():
    if 'user_id' not in session:
        return jsonify({'error': 'Not authenticated'}), 401
    
    api_key = os.getenv('NEWS_API_KEY')
    
    if not api_key or api_key == 'YOUR_NEWS_API_KEY_HERE':
        return jsonify({'error': 'News API key not configured'}), 500
    
    try:
        url = f'https://newsapi.org/v2/top-headlines?country=us&apiKey={api_key}'
        response = requests.get(url)
        data = response.json()
        
        if response.status_code == 200:
            articles = data.get('articles', [])[:5]
            news_items = []
            for article in articles:
                news_items.append({
                    'title': article['title'],
                    'description': article['description'],
                    'url': article['url']
                })
            return jsonify({'articles': news_items})
        else:
            return jsonify({'error': 'News data not found'}), 404
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    # Ensure instance directory exists
    os.makedirs('instance', exist_ok=True)
    
    print("🚀 Starting Darek AI Assistant...")
    print("🌐 Server will be available at: http://localhost:5000")
    print("📱 Press Ctrl+C to stop")
    
    # Run the app
    app.run(debug=True, port=5000, host='0.0.0.0')
