🤖 Darek AI Assistant

A comprehensive AI-powered virtual assistant built with Flask that provides intelligent conversation, productivity tools, and real-time information services.

## ✨ Features

### 🧠 **Core AI Capabilities**
- **Natural Language Processing** - Understands and responds to conversational queries
- **Multi-language Translation** - Supports 12 languages (Spanish, French, German, Italian, Portuguese, Dutch, Russian, Japanese, Chinese, Korean, Hindi, Arabic)
- **Web Search Integration** - Real-time information retrieval using DuckDuckGo API
- **Text-to-Speech** - Voice output for AI responses with chunked reading

### 🌤️ **Information Services**
- **Weather Reports** - Live weather data for any city worldwide via OpenWeatherMap API
- **News Headlines** - Latest news updates with News API integration
- **Wikipedia Search** - Quick access to encyclopedia information

### 📋 **Productivity Tools**
- **Smart Reminders** - Time-based reminders with natural language parsing
- **Todo Lists** - Task management with completion tracking
- **Shopping Lists** - Multi-item shopping list management
- **Notes System** - Personal note creation and storage
- **Timers** - Countdown timers with notifications

### 🧮 **Utilities**
- **Advanced Calculator** - Mathematical operations, percentages, complex expressions
- **Entertainment** - Jokes, trivia questions, and fun interactions
- **Habit Tracking** - Personal habit monitoring capabilities

### 🔐 **User Management**
- **Secure Authentication** - Login/registration with password hashing
- **Session Persistence** - 7-day session management
- **Personal Dashboard** - Comprehensive overview of user data

## 🚀 Quick Start

### Prerequisites
- Python 3.7+
- pip package manager


## 🔑 API Keys Setup

### OpenWeatherMap API (Required for Weather)
1. Visit [OpenWeatherMap](https://openweathermap.org/api)
2. Sign up for a free account
3. Get your API key from the dashboard
4. Add to `.env` file as `WEATHER_API_KEY`

### News API (Optional for News Features)
1. Visit [NewsAPI](https://newsapi.org/)
2. Register for a free account
3. Get your API key
4. Add to `.env` file as `NEWS_API_KEY`

## 💬 Usage Examples

### Basic Conversation
- "Hi Darek, how are you?"
- "What can you help me with?"
- "Tell me a joke"

### Weather Queries
- "What's the weather in London?"
- "Weather forecast for Tokyo"
- "Is it raining in Paris?"

### Productivity Commands
- "Set a reminder to call mom in 30 minutes"
- "Add finish presentation to my todo list"
- "Add bread and milk to shopping list"
- "Start a 5 minute timer"

### Translation Requests
- "Translate hello to Spanish"
- "Translate thank you to Japanese"
- "Translate good morning to German"

### Calculations
- "Calculate 15% of 200"
- "What's 25 + 30 * 2?"
- "Math: (100 + 50) / 3"

### Information Searches
- "Search for artificial intelligence"
- "Tell me about quantum computing"
- "What is machine learning?"

## 🏗️ Architecture

### Backend
- **Flask** - Web framework
- **SQLite** - Database for user data and persistence
- **Python 3.13** - Compatible with latest Python version

### Frontend
- **Vanilla JavaScript** - No framework dependencies
- **Modern CSS** - Glassmorphism design with animations
- **Responsive Design** - Mobile and desktop compatible

### APIs & Services
- **OpenWeatherMap** - Weather data
- **DuckDuckGo** - Web search results
- **News API** - Latest headlines
- **Web Speech API** - Text-to-speech functionality

## 📁 Project Structure

```
darek-ai-assistant/
├── app.py                 # Main Flask application
├── darek_core.py         # AI logic and command processing
├── init_db.py            # Database initialization
├── requirements.txt      # Python dependencies
├── .env                  # Environment variables (create this)
├── README.md            # This file
├── static/
│   ├── css/
│   │   ├── enhanced_style.css      # Main stylesheet
│   │   └── weather_music_cards.css # Card components
│   └── js/
│       ├── main.js      # Frontend JavaScript
│       └── speech.js    # Text-to-speech functionality
├── templates/
│   ├── base.html        # Base template
│   ├── index.html       # Chat interface
│   ├── dashboard.html   # User dashboard
│   ├── login.html       # Login page
│   └── signup.html    # Registration page
└── instance/
    └── darek_ai.db      # SQLite database (auto-created)
```


### Database Schema
The application uses SQLite with the following tables:
- `users` - User authentication and profiles
- `reminders` - Time-based reminders
- `todo_item` - Todo list items
- `shopping_item` - Shopping list items
- `notes` - User notes
- `timers` - Active timers

## 🔒 Security Features

- Session-based authentication
- CSRF protection ready
- Environment variable configuration

## 🌐 Browser Compatibility

- Chrome 80+
- Firefox 75+
- Safari 13+
- Edge 80+


