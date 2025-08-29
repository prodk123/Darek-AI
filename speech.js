// Text-to-Speech functionality for Darek AI
class SpeechManager {
    constructor() {
        this.synth = window.speechSynthesis;
        this.voices = [];
        this.currentVoice = null;
        this.isEnabled = true;
        this.loadVoices();
    }

    loadVoices() {
        this.voices = this.synth.getVoices();
        
        // Find a good English voice
        this.currentVoice = this.voices.find(voice => 
            voice.lang.startsWith('en') && voice.name.includes('Google')
        ) || this.voices.find(voice => 
            voice.lang.startsWith('en')
        ) || this.voices[0];

        // Reload voices when they become available
        if (this.voices.length === 0) {
            this.synth.onvoiceschanged = () => {
                this.loadVoices();
            };
        }
    }

    speak(text) {
        if (!this.isEnabled || !text) return;

        // Stop any current speech
        this.synth.cancel();

        // Clean text for speech
        const cleanText = text
            .replace(/🌤️|🔍|📖|⚠️|❌|🌐|🔑|💬|🧠|😊|🌟|💫|👋|😄|🧮|📝|⏰|📰|📅|📊|🎵|🌐|🤖/g, '')
            .replace(/\*\*/g, '')
            .replace(/\n\n/g, '. ')
            .replace(/\n/g, '. ')
            .replace(/•/g, '')
            .trim();

        if (cleanText.length > 0) {
            // Split long text into chunks to prevent cutoff
            const maxLength = 200; // Chrome has limits on utterance length
            const sentences = cleanText.split('. ');
            let currentChunk = '';
            const chunks = [];

            sentences.forEach(sentence => {
                if ((currentChunk + sentence).length < maxLength) {
                    currentChunk += (currentChunk ? '. ' : '') + sentence;
                } else {
                    if (currentChunk) chunks.push(currentChunk);
                    currentChunk = sentence;
                }
            });
            
            if (currentChunk) chunks.push(currentChunk);

            // Speak each chunk with a small delay
            this.speakChunks(chunks, 0);
        }
    }

    speakChunks(chunks, index) {
        if (index >= chunks.length || !this.isEnabled) return;

        const utterance = new SpeechSynthesisUtterance(chunks[index]);
        
        if (this.currentVoice) {
            utterance.voice = this.currentVoice;
        }
        
        utterance.rate = 0.9;
        utterance.pitch = 1.0;
        utterance.volume = 0.8;

        utterance.onend = () => {
            // Small delay before next chunk to prevent browser issues
            setTimeout(() => {
                this.speakChunks(chunks, index + 1);
            }, 100);
        };

        utterance.onerror = (event) => {
            console.log('Speech error:', event.error);
            // Try next chunk even if current one fails
            setTimeout(() => {
                this.speakChunks(chunks, index + 1);
            }, 100);
        };

        this.synth.speak(utterance);
    }

    toggle() {
        this.isEnabled = !this.isEnabled;
        if (!this.isEnabled) {
            this.synth.cancel();
        }
        return this.isEnabled;
    }

    stop() {
        this.synth.cancel();
    }
}

// Initialize speech manager
window.speechManager = new SpeechManager();

// Add speech toggle button functionality
document.addEventListener('DOMContentLoaded', () => {
    // Create speech toggle button
    const speechToggle = document.createElement('button');
    speechToggle.id = 'speech-toggle';
    speechToggle.className = 'speech-toggle-btn';
    speechToggle.innerHTML = '<i class="fas fa-volume-up"></i>';
    speechToggle.title = 'Toggle Text-to-Speech';
    
    // Add to chat interface
    const chatContainer = document.querySelector('.chat-container');
    if (chatContainer) {
        chatContainer.appendChild(speechToggle);
    }

    speechToggle.addEventListener('click', () => {
        const isEnabled = window.speechManager.toggle();
        speechToggle.innerHTML = isEnabled ? 
            '<i class="fas fa-volume-up"></i>' : 
            '<i class="fas fa-volume-mute"></i>';
        speechToggle.title = isEnabled ? 
            'Disable Text-to-Speech' : 
            'Enable Text-to-Speech';
    });
});
