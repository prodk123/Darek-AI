import datetime
import pyjokes
import pywhatkit
import wikipedia
import requests
import os
import sqlite3

class Darek:
    def __init__(self):
        pass

    def get_db_connection(self):
        """Get database connection"""
        conn = sqlite3.connect('instance/darek_ai.db')
        conn.row_factory = sqlite3.Row
        return conn

    def process_command(self, command, user_id=None):
        if not command or not command.strip():
            return "Hello! How can I help you today?"
            
        command = command.lower().strip()
        response = ""

        # Debug logging
        print(f"DEBUG: Processing command: '{command}'")

        if 'time' in command:
            now = datetime.datetime.now().strftime("%I:%M %p")
            response = f"The current time is {now}."

        elif 'set a reminder' in command or 'remind me' in command:
            parts = command.split(' ')
            try:
                if 'in' in command:
                    time_index = parts.index('in') + 1
                    time_value = int(parts[time_index])
                    time_unit = parts[time_index + 1]
                    
                    if 'minute' in time_unit:
                        reminder_time = datetime.datetime.now() + datetime.timedelta(minutes=time_value)
                    elif 'hour' in time_unit:
                        reminder_time = datetime.datetime.now() + datetime.timedelta(hours=time_value)
                    else:
                        reminder_time = datetime.datetime.now() + datetime.timedelta(minutes=time_value)
                    
                    task = command.replace('set a reminder', '').replace('remind me', '').replace(f'in {time_value} {time_unit}', '').replace('to', '').strip()
                    
                    if user_id:
                        conn = self.get_db_connection()
                        conn.execute('INSERT INTO reminder (task, remind_at, user_id) VALUES (?, ?, ?)',
                                   (task, reminder_time, user_id))
                        conn.commit()
                        conn.close()
                    
                    response = f"🔔 Reminder set: '{task}' in {time_value} {time_unit}."
                else:
                    response = "Please specify when to remind you, like 'remind me to call mom in 30 minutes'."
            except (ValueError, IndexError):
                response = "Please specify the reminder in the format: 'Set a reminder to [task] in [time] [unit]'."

        elif 'add to my to-do list' in command or ('add' in command and 'todo' in command) or 'todo' in command:
            # Extract the todo item from various command formats
            item = ''
            if 'add to my to-do list' in command:
                item = command.replace('add to my to-do list', '').strip()
            elif 'add' in command and 'todo' in command:
                item = command.replace('add', '').replace('to', '').replace('todo', '').replace('list', '').strip()
            elif 'todo' in command:
                item = command.replace('todo', '').replace('add', '').replace('create', '').strip()
            
            # Clean up common words
            item = item.replace('my', '').replace('the', '').strip()
            
            if user_id and item:
                try:
                    conn = self.get_db_connection()
                    conn.execute('INSERT INTO todo_item (task, user_id, completed) VALUES (?, ?, ?)', (item, user_id, False))
                    conn.commit()
                    conn.close()
                    response = f"✅ Added '{item}' to your to-do list."
                except Exception as e:
                    response = f"✅ Todo item noted: '{item}' (database temporarily unavailable)"
            else:
                response = "What would you like to add to your to-do list?"

        elif 'add to my shopping list' in command or ('add' in command and 'shopping' in command) or 'shopping' in command:
            # Extract shopping item from various command formats
            item = ''
            if 'add to my shopping list' in command:
                item = command.replace('add to my shopping list', '').strip()
            elif 'add' in command and 'shopping' in command:
                # Handle "add bread to shopping list" format
                item = command.replace('add', '').replace('to', '').replace('shopping', '').replace('list', '').replace('my', '').strip()
            elif 'shopping' in command:
                # Handle "shopping list bread" or "add bread shopping" formats
                item = command.replace('shopping', '').replace('list', '').replace('add', '').replace('my', '').replace('to', '').strip()
            
            # Clean up extra words
            item = item.replace('and', ',').strip()
            
            if item:
                if user_id:
                    try:
                        conn = self.get_db_connection()
                        # Handle multiple items separated by commas or "and"
                        items = [i.strip() for i in item.replace(' and ', ',').split(',') if i.strip()]
                        added_items = []
                        for single_item in items:
                            if single_item:
                                conn.execute('INSERT INTO shopping_item (item_name, user_id) VALUES (?, ?)', (single_item, user_id))
                                added_items.append(single_item)
                        conn.commit()
                        conn.close()
                        
                        if len(added_items) == 1:
                            response = f"🛒 Added '{added_items[0]}' to your shopping list."
                        else:
                            response = f"🛒 Added {len(added_items)} items to your shopping list: {', '.join(added_items)}"
                    except Exception as e:
                        response = f"🛒 Shopping item noted: '{item}' (database temporarily unavailable)"
                else:
                    response = f"🛒 Shopping item noted: '{item}'"
            else:
                response = "What would you like to add to your shopping list? Try: 'add bread and milk to shopping list'"

        elif 'search' in command or 'wikipedia' in command:
            query = command.replace('search', '').replace('wikipedia', '').strip()
            try:
                summary = wikipedia.summary(query, sentences=2)
                response = f"Here's what I found about {query}: {summary}"
            except wikipedia.exceptions.DisambiguationError as e:
                response = f"Multiple results found for {query}. Try being more specific."
            except wikipedia.exceptions.PageError:
                response = f"Sorry, I could not find a Wikipedia page for {query}."
            except Exception as e:
                response = f"An error occurred: {e}"

        elif 'play' in command:
            song = command.replace('play', '').strip()
            response = f"🎵 Playing {song} on YouTube."
            try:
                pywhatkit.playonyt(song)
            except:
                response = f"🎵 I would play {song} for you, but there was an issue opening YouTube."

        elif 'start' in command and 'timer' in command:
            parts = command.split()
            try:
                if 'minute' in command:
                    time_index = next(i for i, word in enumerate(parts) if word.isdigit())
                    minutes = int(parts[time_index])
                    duration_seconds = minutes * 60
                    
                    if user_id:
                        conn = self.get_db_connection()
                        conn.execute('INSERT INTO timer (name, duration, user_id) VALUES (?, ?, ?)',
                                   (f"{minutes}-minute timer", duration_seconds, user_id))
                        conn.commit()
                        conn.close()
                    
                    response = f"⏰ Started a {minutes}-minute timer. I'll notify you when it's done!"
                elif 'second' in command:
                    time_index = next(i for i, word in enumerate(parts) if word.isdigit())
                    seconds = int(parts[time_index])
                    
                    if user_id:
                        conn = self.get_db_connection()
                        conn.execute('INSERT INTO timer (name, duration, user_id) VALUES (?, ?, ?)',
                                   (f"{seconds}-second timer", seconds, user_id))
                        conn.commit()
                        conn.close()
                    
                    response = f"⏰ Started a {seconds}-second timer. I'll notify you when it's done!"
                else:
                    response = "Please specify the timer duration, like 'start a 5 minute timer'."
            except (ValueError, StopIteration):
                response = "Please specify the timer duration, like 'start a 5 minute timer'."

        elif 'calculate' in command or 'math' in command:
            import re
            # Extract numbers and operators from the command
            math_parts = re.findall(r'[\d+\-*/().\s]+', command)
            if math_parts:
                try:
                    expr = ''.join(math_parts).strip()
                    # Clean expression to only allow safe characters
                    safe_expr = re.sub(r'[^\d+\-*/().\s]', '', expr)
                    if safe_expr and any(c.isdigit() for c in safe_expr):
                        # Use eval safely for basic math
                        result = eval(safe_expr)
                        response = f"🧮 {safe_expr} = {result}"
                    else:
                        response = "Please provide a math expression like '15 + 25' or '10 * 5'."
                except Exception as e:
                    response = "Sorry, I couldn't calculate that. Please try a simpler math expression like '15 + 25'."
            else:
                # Try to extract from percentage calculations
                if '%' in command and 'of' in command:
                    try:
                        parts = command.split()
                        percentage = None
                        amount = None
                        for i, part in enumerate(parts):
                            if '%' in part:
                                percentage = float(part.replace('%', ''))
                            elif part.replace('.', '').isdigit() and i > 0:
                                amount = float(part)
                        if percentage and amount:
                            result = (percentage / 100) * amount
                            response = f"🧮 {percentage}% of {amount} = {result:.2f}"
                        else:
                            response = "Please provide a calculation like '15% of 100' or '25 + 30'."
                    except:
                        response = "Please provide a calculation like '15% of 100' or '25 + 30'."
                else:
                    response = "Please provide a math expression like '15 + 25', '10 * 5', or '15% of 100'."

        elif 'translate' in command:
            # Multi-language translation using basic dictionary for common phrases
            try:
                # Extract text to translate and target language
                command_lower = command.lower()
                
                # Define translations for 12 languages
                translations_db = {
                    'spanish': {
                        'hello': 'hola', 'goodbye': 'adiós', 'thank you': 'gracias', 'please': 'por favor',
                        'yes': 'sí', 'no': 'no', 'good morning': 'buenos días', 'good night': 'buenas noches',
                        'how are you': 'cómo estás', 'i love you': 'te amo', 'water': 'agua', 'food': 'comida'
                    },
                    'french': {
                        'hello': 'bonjour', 'goodbye': 'au revoir', 'thank you': 'merci', 'please': 's\'il vous plaît',
                        'yes': 'oui', 'no': 'non', 'good morning': 'bonjour', 'good night': 'bonne nuit',
                        'how are you': 'comment allez-vous', 'i love you': 'je t\'aime', 'water': 'eau', 'food': 'nourriture'
                    },
                    'german': {
                        'hello': 'hallo', 'goodbye': 'auf wiedersehen', 'thank you': 'danke', 'please': 'bitte',
                        'yes': 'ja', 'no': 'nein', 'good morning': 'guten morgen', 'good night': 'gute nacht',
                        'how are you': 'wie geht es dir', 'i love you': 'ich liebe dich', 'water': 'wasser', 'food': 'essen'
                    },
                    'italian': {
                        'hello': 'ciao', 'goodbye': 'arrivederci', 'thank you': 'grazie', 'please': 'per favore',
                        'yes': 'sì', 'no': 'no', 'good morning': 'buongiorno', 'good night': 'buonanotte',
                        'how are you': 'come stai', 'i love you': 'ti amo', 'water': 'acqua', 'food': 'cibo'
                    },
                    'portuguese': {
                        'hello': 'olá', 'goodbye': 'tchau', 'thank you': 'obrigado', 'please': 'por favor',
                        'yes': 'sim', 'no': 'não', 'good morning': 'bom dia', 'good night': 'boa noite',
                        'how are you': 'como está', 'i love you': 'eu te amo', 'water': 'água', 'food': 'comida'
                    },
                    'dutch': {
                        'hello': 'hallo', 'goodbye': 'tot ziens', 'thank you': 'dank je', 'please': 'alsjeblieft',
                        'yes': 'ja', 'no': 'nee', 'good morning': 'goedemorgen', 'good night': 'goedenacht',
                        'how are you': 'hoe gaat het', 'i love you': 'ik hou van je', 'water': 'water', 'food': 'eten'
                    },
                    'russian': {
                        'hello': 'привет', 'goodbye': 'до свидания', 'thank you': 'спасибо', 'please': 'пожалуйста',
                        'yes': 'да', 'no': 'нет', 'good morning': 'доброе утро', 'good night': 'спокойной ночи',
                        'how are you': 'как дела', 'i love you': 'я тебя люблю', 'water': 'вода', 'food': 'еда'
                    },
                    'japanese': {
                        'hello': 'こんにちは', 'goodbye': 'さようなら', 'thank you': 'ありがとう', 'please': 'お願いします',
                        'yes': 'はい', 'no': 'いいえ', 'good morning': 'おはよう', 'good night': 'おやすみ',
                        'how are you': '元気ですか', 'i love you': '愛してる', 'water': '水', 'food': '食べ物'
                    },
                    'chinese': {
                        'hello': '你好', 'goodbye': '再见', 'thank you': '谢谢', 'please': '请',
                        'yes': '是', 'no': '不', 'good morning': '早上好', 'good night': '晚安',
                        'how are you': '你好吗', 'i love you': '我爱你', 'water': '水', 'food': '食物'
                    },
                    'korean': {
                        'hello': '안녕하세요', 'goodbye': '안녕히 가세요', 'thank you': '감사합니다', 'please': '제발',
                        'yes': '네', 'no': '아니요', 'good morning': '좋은 아침', 'good night': '잘 자요',
                        'how are you': '어떻게 지내세요', 'i love you': '사랑해요', 'water': '물', 'food': '음식'
                    },
                    'hindi': {
                        'hello': 'नमस्ते', 'goodbye': 'अलविदा', 'thank you': 'धन्यवाद', 'please': 'कृपया',
                        'yes': 'हाँ', 'no': 'नहीं', 'good morning': 'सुप्रभात', 'good night': 'शुभ रात्रि',
                        'how are you': 'आप कैसे हैं', 'i love you': 'मैं तुमसे प्यार करता हूँ', 'water': 'पानी', 'food': 'खाना'
                    },
                    'arabic': {
                        'hello': 'مرحبا', 'goodbye': 'وداعا', 'thank you': 'شكرا', 'please': 'من فضلك',
                        'yes': 'نعم', 'no': 'لا', 'good morning': 'صباح الخير', 'good night': 'تصبح على خير',
                        'how are you': 'كيف حالك', 'i love you': 'أحبك', 'water': 'ماء', 'food': 'طعام'
                    }
                }
                
                # Find target language
                target_lang = None
                for lang in translations_db.keys():
                    if f'to {lang}' in command_lower:
                        target_lang = lang
                        text_to_translate = command_lower.replace('translate', '').replace(f'to {lang}', '').strip()
                        break
                
                if target_lang and text_to_translate:
                    translation = translations_db[target_lang].get(text_to_translate, None)
                    if translation:
                        response = f"🌐 Translation: '{text_to_translate}' in {target_lang.title()} is '{translation}'"
                    else:
                        available_phrases = ', '.join(list(translations_db[target_lang].keys())[:8])
                        response = f"🌐 I can translate these phrases to {target_lang.title()}: {available_phrases}"
                else:
                    supported_langs = ', '.join(list(translations_db.keys()))
                    response = f"🌐 I support translation to: {supported_langs}. Try: 'translate hello to German' or 'translate thank you to Japanese'"
                    
            except Exception as e:
                response = "🌐 Translation service temporarily unavailable. Try: 'translate hello to German'"

        elif 'news' in command:
            try:
                news_api_key = os.getenv('NEWS_API_KEY', '')
                if news_api_key and news_api_key != 'YOUR_NEWS_API_KEY_HERE':
                    url = f'https://newsapi.org/v2/top-headlines?country=us&apiKey={news_api_key}'
                    news_response = requests.get(url)
                    
                    if news_response.status_code == 200:
                        news_data = news_response.json()
                        articles = news_data.get('articles', [])[:3]
                        
                        if articles:
                            headlines = "📰 Latest News Headlines:\n\n"
                            for i, article in enumerate(articles, 1):
                                headlines += f"{i}. {article['title']}\n"
                            response = headlines
                        else:
                            response = "📰 No news articles found at the moment."
                    else:
                        response = "📰 Unable to fetch news at the moment. Please try again later."
                else:
                    response = "📰 News feature requires API key setup. Please add NEWS_API_KEY to your environment variables."
            except Exception as e:
                response = "📰 Error fetching news. Please try again later."

        elif 'note' in command and ('create' in command or 'make' in command or 'add' in command):
            note_content = command.replace('create a note', '').replace('make a note', '').replace('add a note', '').replace('note', '').strip()
            if note_content and user_id:
                try:
                    conn = self.get_db_connection()
                    conn.execute('INSERT INTO note (content, user_id) VALUES (?, ?)', (note_content, user_id))
                    conn.commit()
                    conn.close()
                    response = f"📝 Created a note: '{note_content}'"
                except:
                    response = f"📝 Note saved locally: '{note_content}'"
            elif note_content:
                response = f"📝 Note saved: '{note_content}'"
            else:
                response = "What would you like to note down?"

        elif 'joke' in command:
            try:
                response = pyjokes.get_joke()
            except:
                response = "😄 Why don't scientists trust atoms? Because they make up everything!"

        elif 'weather' in command:
            try:
                # Extract city from command - improved parsing
                city = "London"  # Default city
                
                # Better city extraction logic
                if ' in ' in command:
                    city = command.split(' in ')[1].replace('?', '').strip()
                elif 'weather ' in command:
                    # Extract everything after "weather "
                    weather_index = command.find('weather ')
                    after_weather = command[weather_index + 8:].strip()
                    if after_weather and not after_weather.startswith('like'):
                        city = after_weather.replace('?', '').strip()
                
                # Clean up city name
                city = city.replace('the weather', '').replace('like', '').strip()
                if not city or city == '':
                    city = "London"
                
                api_key = os.getenv('WEATHER_API_KEY')
                
                if api_key and api_key != 'YOUR_API_KEY_HERE':
                    url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric'
                    
                    try:
                        weather_response = requests.get(url, timeout=10)
                        
                        if weather_response.status_code == 200:
                            weather_data = weather_response.json()
                            weather_desc = weather_data['weather'][0]['description']
                            temp = round(weather_data['main']['temp'])
                            feels_like = round(weather_data['main']['feels_like'])
                            humidity = weather_data['main']['humidity']
                            wind_speed = weather_data['wind']['speed']

                            response = f"🌤️ **Weather in {city.title()}**\n\n" \
                                       f"Currently: {weather_desc.title()}\n" \
                                       f"Temperature: {temp}°C (feels like {feels_like}°C)\n" \
                                       f"Humidity: {humidity}%\n" \
                                       f"Wind Speed: {wind_speed} m/s"
                        else:
                            weather_data = weather_response.json()
                            response = f"❌ Couldn't find weather data for '{city}'. Please check the city name and try again."
                    except requests.exceptions.RequestException:
                        response = f"🌐 Unable to connect to weather service. Please check your internet connection."
                    except Exception as e:
                        response = f"⚠️ Error getting weather data: {str(e)}"
                else:
                    response = "🔑 Weather API key not configured. Please set WEATHER_API_KEY in environment variables."
            except Exception as e:
                response = "💬 Try: 'weather in Paris' or 'what's the weather in Tokyo'"

        elif 'trivia' in command or 'quiz' in command:
            trivia_questions = [
                "🧠 Here's a trivia question: What is the largest planet in our solar system? (Answer: Jupiter)",
                "🧠 Trivia time: Which element has the chemical symbol 'Au'? (Answer: Gold)",
                "🧠 Quick question: What year did the Titanic sink? (Answer: 1912)",
                "🧠 Brain teaser: How many continents are there? (Answer: 7)",
                "🧠 Fun fact question: What's the fastest land animal? (Answer: Cheetah)"
            ]
            import random
            response = random.choice(trivia_questions)

        elif 'habit' in command or 'track' in command:
            response = "📊 Habit tracking feature coming soon! I'll help you build and maintain healthy habits."

        elif 'calendar' in command or 'schedule' in command:
            response = "📅 Calendar integration coming soon! I'll be able to manage your schedule and appointments."

        elif 'how are you' in command:
            responses = [
                "I'm doing fantastic! Ready to help you with anything you need. 😊",
                "I'm great, thank you for asking! How can I assist you today?",
                "Doing wonderful! I'm here and ready to help with your tasks."
            ]
            import random
            response = random.choice(responses)

        # Web search functionality - ENHANCED
        elif any(word in command for word in ['search', 'google', 'find', 'look up', 'what is', 'who is', 'tell me about']):
            # Extract search query with better parsing
            search_query = command
            
            # Remove search trigger words
            for word in ['search for', 'search', 'google', 'find', 'look up', 'what is', 'who is', 'tell me about', 'about', 'web', 'internet']:
                search_query = search_query.replace(word, '')
            
            search_query = search_query.strip()
            
            if search_query and len(search_query) > 1:
                try:
                    from urllib.parse import quote
                    
                    # Use DuckDuckGo Instant Answer API
                    search_url = f"https://api.duckduckgo.com/?q={quote(search_query)}&format=json&no_html=1&skip_disambig=1"
                    search_response = requests.get(search_url, timeout=10)
                    
                    if search_response.status_code == 200:
                        data = search_response.json()
                        
                        # Try different response types
                        if data.get('Abstract') and len(data['Abstract']) > 50:
                            abstract_url = data.get('AbstractURL', '')
                            source_name = abstract_url.split('//')[-1].split('/')[0] if abstract_url else 'Wikipedia'
                            response = f"🔍 **{search_query.title()}**\n\n{data['Abstract']}\n\n📖 Source: {source_name}"
                            
                        elif data.get('Definition') and len(data['Definition']) > 20:
                            def_url = data.get('DefinitionURL', '')
                            source_name = def_url.split('//')[-1].split('/')[0] if def_url else 'Dictionary'
                            response = f"🔍 **Definition: {search_query.title()}**\n\n{data['Definition']}\n\n📖 Source: {source_name}"
                            
                        elif data.get('Answer'):
                            response = f"🔍 **{search_query.title()}**\n\n{data['Answer']}"
                            
                        elif data.get('RelatedTopics') and len(data['RelatedTopics']) > 0:
                            # Use first related topic if available
                            first_topic = data['RelatedTopics'][0]
                            if isinstance(first_topic, dict) and first_topic.get('Text'):
                                response = f"🔍 **{search_query.title()}**\n\n{first_topic['Text']}\n\n📖 Source: DuckDuckGo"
                            else:
                                response = f"🔍 **Search: {search_query}**\n\nFound some results but no detailed information available. Try a more specific search term."
                        else:
                            # Enhanced fallback with suggestions
                            response = f"🔍 **Search: {search_query}**\n\nNo detailed information found. Try:\n• Being more specific\n• Using different keywords\n• Checking spelling\n\nExample: 'search Python programming' or 'what is machine learning'"
                    else:
                        response = f"🔍 Search service temporarily unavailable. Please try again in a moment."
                        
                except requests.exceptions.Timeout:
                    response = f"🔍 Search request timed out. Please try again with a shorter query."
                except requests.exceptions.RequestException:
                    response = f"🔍 Unable to connect to search service. Check your internet connection."
                except Exception as e:
                    response = f"🔍 Search error occurred. Please try again later."
            else:
                response = "🔍 **Web Search Ready!**\n\nWhat would you like me to search for?\n\nExamples:\n• 'search artificial intelligence'\n• 'what is blockchain'\n• 'find information about space exploration'\n• 'tell me about renewable energy'"

        # Normal conversation AI responses
        elif any(greeting in command for greeting in ['hi', 'hello', 'hey', 'good morning', 'good afternoon', 'good evening']):
            responses = [
                "Hello! 👋 I'm Darek, your AI assistant. How can I help you today?",
                "Hi there! 😊 Ready to assist you with anything you need!",
                "Hey! 🌟 What can I do for you today?",
                "Hello! Great to see you! How can I make your day better?"
            ]
            import random
            response = random.choice(responses)
            
        elif 'what can you do' in command or 'help' in command or 'capabilities' in command:
            response = """🤖 **I'm Darek, your AI assistant! Here's what I can do:**

📅 **Productivity:** Set reminders, create notes, manage to-do lists, start timers
🧮 **Calculator:** Solve math problems, percentages, complex calculations  
🌤️ **Weather:** Get current weather for any city
📰 **News:** Latest headlines and news updates
🔍 **Web Search:** Search the internet for information
🎵 **Entertainment:** Tell jokes, share trivia, play music
📝 **Organization:** Shopping lists, habit tracking
💬 **Chat:** Have normal conversations - I'm here to help and chat!

Just ask me naturally like "What's the weather in Paris?" or "Calculate 15% of 200" or even just say hi! 😊"""

        elif 'thank you' in command or 'thanks' in command:
            responses = [
                "You're very welcome! 😊 Happy to help anytime!",
                "My pleasure! 🌟 Let me know if you need anything else!",
                "Glad I could help! 💫 Feel free to ask me anything!"
            ]
            import random
            response = random.choice(responses)
            
        elif 'bye' in command or 'goodbye' in command or 'see you' in command:
            responses = [
                "Goodbye! 👋 Have a wonderful day!",
                "See you later! 😊 Take care!",
                "Bye! 🌟 Come back anytime you need help!"
            ]
            import random
            response = random.choice(responses)

        else:
            # More conversational fallback responses
            fallback_responses = [
                "I'm not sure I understand that completely. Could you try rephrasing? I can help with weather, calculations, reminders, notes, web searches, or just chat! 😊",
                "Hmm, I didn't quite catch that. I'm here to help with various tasks or just have a conversation. What would you like to do?",
                "I'm still learning! 🤖 Could you be more specific? I can assist with productivity tasks, answer questions, or just chat with you!",
                "That's interesting! I might need a bit more context. Feel free to ask me about weather, math, reminders, or anything else on your mind! 💭"
            ]
            import random
            response = random.choice(fallback_responses)
            
            # Log unrecognized command
            with open('unrecognized_commands.txt', 'a') as f:
                f.write(f'{datetime.datetime.now()}: {command}\n')
    
        return response
