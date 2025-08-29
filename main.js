document.addEventListener('DOMContentLoaded', () => {
    const messageInput = document.getElementById('message-input');
    const sendButton = document.getElementById('send-button');
    const micButton = document.getElementById('mic-button');
    const chatBox = document.getElementById('chat-box');
    const feedback = document.getElementById('feedback');
    const suggestionButtons = document.querySelectorAll('.suggestion-btn');

    function sendMessage(message) {
        if (message.trim() !== '') {
            appendMessage('You', message, 'user');
            messageInput.value = '';
            feedback.innerHTML = 'Darek is thinking...';

            fetch('/chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ message: message })
            })
            .then(response => response.json())
            .then(data => {
                const message = data.message || data.error || 'Sorry, I could not process your request.';
                appendMessage('Darek', message, 'bot');
                
                // Add text-to-speech for bot responses
                if (window.speechManager) {
                    window.speechManager.speak(message);
                }
                
                feedback.innerHTML = '';
            })
            .catch(error => {
                console.error('Error:', error);
                appendMessage('Darek', 'Sorry, there was an error processing your request.', 'bot');
                feedback.innerHTML = '';
            });
        }
    }

    function appendMessage(sender, message, type) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${type}-message`;
        
        const messageContent = document.createElement('div');
        messageContent.className = 'message-content';
        messageContent.innerHTML = message.replace(/\n/g, '<br>');
        
        messageDiv.appendChild(messageContent);
        chatBox.appendChild(messageDiv);
        chatBox.scrollTop = chatBox.scrollHeight;
    }

    if (sendButton) {
        sendButton.addEventListener('click', () => {
            sendMessage(messageInput.value);
        });
    }

    if (messageInput) {
        messageInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                sendMessage(messageInput.value);
            }
        });
    }

    if (micButton) {
        micButton.addEventListener('click', () => {
            alert('Voice input feature coming soon!');
        });
    }

    // Suggestion buttons functionality
    suggestionButtons.forEach(button => {
        button.addEventListener('click', () => {
            const suggestion = button.textContent;
            if (messageInput) {
                messageInput.value = suggestion;
                messageInput.focus();
            }
        });
    });

    // Feature buttons functionality
    const featureButtons = document.querySelectorAll('.feature-btn');
    featureButtons.forEach(button => {
        button.addEventListener('click', (e) => {
            const feature = e.currentTarget.getAttribute('data-feature');
            handleFeatureClick(feature);
        });
    });

    // Sidebar navigation functionality
    const navItems = document.querySelectorAll('.nav-item[data-feature]');
    navItems.forEach(item => {
        item.addEventListener('click', (e) => {
            e.preventDefault();
            const feature = e.currentTarget.getAttribute('data-feature');
            handleFeatureClick(feature);
        });
    });

    function handleFeatureClick(feature) {
        const featureMessages = {
            'search': 'Search for artificial intelligence',
            'reminders': 'Set a reminder in 10 minutes to check emails',
            'timers': 'Start a 5 minute timer',
            'calendar': 'What\'s on my calendar today?',
            'notes': 'Create a note about meeting with team tomorrow',
            'todo': 'Add finish presentation to my to-do list',
            'shopping': 'Add bread and eggs to my shopping list',
            'habits': 'Track my daily water intake',
            'weather': 'What\'s the weather like in London?',
            'news': 'Give me the latest news headlines',
            'calculator': 'Calculate 15 + 25 * 2',
            'translator': 'Translate hello to Spanish',
            'music': 'Play some relaxing music',
            'jokes': 'Tell me a funny joke',
            'trivia': 'Ask me a trivia question'
        };

        const message = featureMessages[feature] || `Help me with ${feature}`;
        
        // Auto-fill the input with the feature message
        if (messageInput) {
            messageInput.value = message;
            messageInput.focus();
        }
    }

    // Weather functionality with card display
    function loadWeather() {
        fetch('/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                message: 'weather in London'
            })
        })
        .then(response => response.json())
        .then(data => {
            if (data.response && data.response.includes('°')) {
                // Parse weather data and create card
                createWeatherCard(data.response);
            } else {
                document.getElementById('weather-content').innerHTML = data.response || '<p>Unable to load weather</p>';
            }
        })
        .catch(error => {
            console.error('Error loading weather:', error);
            document.getElementById('weather-content').innerHTML = '<p>Unable to load weather</p>';
        });
    }

    function createWeatherCard(weatherText) {
        const weatherContainer = document.getElementById('weather-content');
        if (!weatherContainer) return;

        // Extract temperature and description from response
        const tempMatch = weatherText.match(/(\d+)°/);
        const descMatch = weatherText.match(/with (.+?)\./);
        
        const temp = tempMatch ? tempMatch[1] : '--';
        const desc = descMatch ? descMatch[1] : 'Clear';
        
        weatherContainer.innerHTML = `
            <div class="weather-card">
                <div class="card-header">
                    <i class="fas fa-cloud-sun card-icon"></i>
                    <h3 class="card-title">Current Weather</h3>
                </div>
                <div class="weather-info">
                    <div class="weather-main">
                        <div class="weather-temp">${temp}°</div>
                        <div class="weather-desc">${desc}</div>
                    </div>
                    <div class="weather-details">
                        <div class="weather-detail">London, UK</div>
                        <div class="weather-detail">Updated now</div>
                    </div>
                </div>
            </div>
        `;
    }

    // Music card functionality
    function createMusicCard() {
        const musicContainer = document.getElementById('music-content');
        if (!musicContainer) return;

        musicContainer.innerHTML = `
            <div class="music-card">
                <div class="card-header">
                    <i class="fas fa-music card-icon"></i>
                    <h3 class="card-title">Music Player</h3>
                </div>
                <div class="music-info">
                    <div class="music-title">Relaxing Ambient</div>
                    <div class="music-artist">Nature Sounds</div>
                </div>
                <div class="music-progress">
                    <div class="music-progress-bar" id="progress-bar"></div>
                </div>
                <div class="music-controls">
                    <button class="music-btn" onclick="previousTrack()">
                        <i class="fas fa-step-backward"></i>
                    </button>
                    <button class="music-btn play" onclick="togglePlay()" id="play-btn">
                        <i class="fas fa-play"></i>
                    </button>
                    <button class="music-btn" onclick="nextTrack()">
                        <i class="fas fa-step-forward"></i>
                    </button>
                </div>
            </div>
        `;
    }

    // Music control functions
    window.isPlaying = false;
    window.progress = 0;

    window.togglePlay = function() {
        const playBtn = document.getElementById('play-btn');
        const progressBar = document.getElementById('progress-bar');
        
        window.isPlaying = !window.isPlaying;
        
        if (window.isPlaying) {
            playBtn.innerHTML = '<i class="fas fa-pause"></i>';
            startProgress();
        } else {
            playBtn.innerHTML = '<i class="fas fa-play"></i>';
            stopProgress();
        }
    }

    function startProgress() {
        const progressBar = document.getElementById('progress-bar');
        const interval = setInterval(() => {
            if (!window.isPlaying) {
                clearInterval(interval);
                return;
            }
            window.progress += 0.5;
            if (window.progress >= 100) {
                window.progress = 0;
                window.togglePlay();
            }
            if (progressBar) {
                progressBar.style.width = window.progress + '%';
            }
        }, 100);
    }

    function stopProgress() {
        // Progress stops automatically when isPlaying is false
    }

    window.previousTrack = function() {
        window.progress = 0;
        document.getElementById('progress-bar').style.width = '0%';
    }

});

// Feature buttons functionality
const featureButtons = document.querySelectorAll('.feature-btn');
featureButtons.forEach(button => {
    button.addEventListener('click', (e) => {
        const feature = e.currentTarget.getAttribute('data-feature');
        handleFeatureClick(feature);
    });
});

// Sidebar navigation functionality
const navItems = document.querySelectorAll('.nav-item[data-feature]');
navItems.forEach(item => {
    item.addEventListener('click', (e) => {
        e.preventDefault();
        const feature = e.currentTarget.getAttribute('data-feature');
        handleFeatureClick(feature);
    });
});

function handleFeatureClick(feature) {
    const featureMessages = {
        'search': 'Search for artificial intelligence',
        'reminders': 'Set a reminder in 10 minutes to check emails',
        'timers': 'Start a 5 minute timer',
        'calendar': 'What\'s on my calendar today?',
        'notes': 'Create a note about meeting with team tomorrow',
        'todo': 'Add finish presentation to my to-do list',
        'shopping': 'Add bread and eggs to my shopping list',
        'habits': 'Track my daily water intake',
        'weather': 'What\'s the weather like in London?',
        'news': 'Give me the latest news headlines',
        'calculator': 'Calculate 15 + 25 * 2',
        'translator': 'Translate hello to Spanish',
        'music': 'Play some relaxing music',
        'jokes': 'Tell me a funny joke',
        'trivia': 'Ask me a trivia question'
    };

    const message = featureMessages[feature] || `Help me with ${feature}`;
    
    // Auto-fill the input with the feature message
    if (messageInput) {
        messageInput.value = message;
        messageInput.focus();
    }
}

// Weather functionality with card display
function loadWeather() {
    fetch('/chat', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            message: 'weather in London'
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.response && data.response.includes('°')) {
            // Parse weather data and create card
            createWeatherCard(data.response);
        } else {
            document.getElementById('weather-content').innerHTML = data.response || '<p>Unable to load weather</p>';
        }
    })
    .catch(error => {
        console.error('Error loading weather:', error);
        document.getElementById('weather-content').innerHTML = '<p>Unable to load weather</p>';
    });
}

function createWeatherCard(weatherText) {
    const weatherContainer = document.getElementById('weather-content');
    if (!weatherContainer) return;

    // Extract temperature and description from response
    const tempMatch = weatherText.match(/(\d+)°/);
    const descMatch = weatherText.match(/with (.+?)\./);
    
    const temp = tempMatch ? tempMatch[1] : '--';
    const desc = descMatch ? descMatch[1] : 'Clear';
    
    weatherContainer.innerHTML = `
        <div class="weather-card">
            <div class="card-header">
                <i class="fas fa-cloud-sun card-icon"></i>
                <h3 class="card-title">Current Weather</h3>
            </div>
            <div class="weather-info">
                <div class="weather-main">
                    <div class="weather-temp">${temp}°</div>
                    <div class="weather-desc">${desc}</div>
                </div>
                <div class="weather-details">
                    <div class="weather-detail">London, UK</div>
                    <div class="weather-detail">Updated now</div>
                </div>
            </div>
        </div>
    `;
}

// Music card functionality
function createMusicCard() {
    const musicContainer = document.getElementById('music-content');
    if (!musicContainer) return;

    musicContainer.innerHTML = `
        <div class="music-card">
            <div class="card-header">
                <i class="fas fa-music card-icon"></i>
                <h3 class="card-title">Music Player</h3>
            </div>
            <div class="music-info">
                <div class="music-title">Relaxing Ambient</div>
                <div class="music-artist">Nature Sounds</div>
            </div>
            <div class="music-progress">
                <div class="music-progress-bar" id="progress-bar"></div>
            </div>
            <div class="music-controls">
                <button class="music-btn" onclick="previousTrack()">
                    <i class="fas fa-step-backward"></i>
                </button>
                <button class="music-btn play" onclick="togglePlay()" id="play-btn">
                    <i class="fas fa-play"></i>
                </button>
                <button class="music-btn" onclick="nextTrack()">
                    <i class="fas fa-step-forward"></i>
                </button>
            </div>
        </div>
    `;
}

// Music control functions
window.isPlaying = false;
window.progress = 0;

window.togglePlay = function() {
    const playBtn = document.getElementById('play-btn');
    const progressBar = document.getElementById('progress-bar');
    
    window.isPlaying = !window.isPlaying;
    
    if (window.isPlaying) {
        playBtn.innerHTML = '<i class="fas fa-pause"></i>';
        startProgress();
    } else {
        playBtn.innerHTML = '<i class="fas fa-play"></i>';
        stopProgress();
    }
}

function startProgress() {
    const progressBar = document.getElementById('progress-bar');
    const interval = setInterval(() => {
        if (!window.isPlaying) {
            clearInterval(interval);
            return;
        }
        window.progress += 0.5;
        if (window.progress >= 100) {
            window.progress = 0;
            window.togglePlay();
        }
        if (progressBar) {
            progressBar.style.width = window.progress + '%';
        }
    }, 100);
}

function stopProgress() {
    // Progress stops automatically when isPlaying is false
}

window.previousTrack = function() {
    window.progress = 0;
    document.getElementById('progress-bar').style.width = '0%';
}

window.nextTrack = function() {
    window.progress = 0;
    document.getElementById('progress-bar').style.width = '0%';
}

// Theme toggle functionality
const themeToggle = document.getElementById('theme-toggle');
const themeIcon = document.getElementById('theme-icon');
const themeText = document.getElementById('theme-text');
    
// Load saved theme or default to light
const savedTheme = localStorage.getItem('theme') || 'light';
document.documentElement.setAttribute('data-theme', savedTheme);
updateThemeButton(savedTheme);
    
if (themeToggle) {
    themeToggle.addEventListener('click', () => {
        const currentTheme = document.documentElement.getAttribute('data-theme');
        const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
        
        // Add transition class for smooth animation
        document.body.style.transition = 'all 0.5s cubic-bezier(0.4, 0, 0.2, 1)';
        
        // Update theme
        document.documentElement.setAttribute('data-theme', newTheme);
        localStorage.setItem('theme', newTheme);
        updateThemeButton(newTheme);
        
        // Remove transition after animation
        setTimeout(() => {
            document.body.style.transition = '';
        }, 500);
    });
}
    
function updateThemeButton(theme) {
    if (themeIcon && themeText) {
        if (theme === 'dark') {
            themeIcon.className = 'fas fa-sun';
            themeText.textContent = 'Light Mode';
        } else {
            themeIcon.className = 'fas fa-moon';
            themeText.textContent = 'Dark Mode';
        }
    }
}

// Load weather on page load
if (window.location.pathname === '/dashboard') {
    loadWeather();
}

if (document.getElementById('weather-content')) {
    loadWeather();
}
    
if (document.getElementById('music-content')) {
    createMusicCard();
}
