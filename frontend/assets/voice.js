class VoiceManager {
    constructor() {
        this.synth = window.speechSynthesis;
        // Default to true unless explicitly turned off
        this.enabled = localStorage.getItem('voice_enabled') !== 'false';
        this.voices = [];
        this.pendingText = null;

        const loadVoices = () => {
            this.voices = this.synth.getVoices();
        };

        if (this.synth.onvoiceschanged !== undefined) {
            this.synth.onvoiceschanged = loadVoices;
        }
        loadVoices();


        // Fallback for browser autoplay restrictions: trigger pending speech on first interaction
        const triggerPending = () => {
            if (this.pendingText) {
                console.log("User interacted, playing pending speech:", this.pendingText);
                this.speak(this.pendingText);
                this.pendingText = null;
            }
        };

        ['click', 'mousedown', 'keydown', 'touchstart', 'scroll'].forEach(event => {
            window.addEventListener(event, triggerPending, { once: true });
        });
    }

    enable() {
        this.enabled = true;
        localStorage.setItem('voice_enabled', 'true');
        console.log("Voice Assistant Enabled");
    }

    disable() {
        this.enabled = false;
        localStorage.setItem('voice_enabled', 'false');
        console.log("Voice Assistant Disabled");
    }

    speak(text) {
        if (!this.enabled) {
            console.log("Speech skipped: Voice Assistant disabled in settings.");
            return;
        }
        if (!text) return;

        // If synth is not ready or blocked, store it for first interaction
        if (this.synth.speaking) {
            this.synth.cancel();
        }

        const utterance = new SpeechSynthesisUtterance(text);
        const preferredVoice = this.voices.find(v => v.name.includes('Google US English') || v.name.includes('Female') || v.name.includes('Samantha'));
        if (preferredVoice) utterance.voice = preferredVoice;

        // Modern browsers might block this until user interacts
        try {
            this.synth.speak(utterance);

            // If it didn't start speaking immediately (likely blocked), save for later
            setTimeout(() => {
                if (!this.synth.speaking && !this.synth.pending) {
                    console.log("Speech blocked by browser, waiting for user interaction...");
                    this.pendingText = text;
                }
            }, 100);
        } catch (e) {
            console.error("Speech error:", e);
            this.pendingText = text;
        }
    }

    startListening(callback) {
        if (!('webkitSpeechRecognition' in window)) {
            alert("Speech recognition not supported in this browser.");
            return;
        }

        if (this.recognition) {
            this.recognition.stop();
        }

        this.recognition = new webkitSpeechRecognition();
        this.recognition.continuous = false;
        this.recognition.interimResults = false;
        this.recognition.lang = 'en-US';

        this.recognition.onstart = () => {
            console.log("Voice listening started...");
        };

        this.recognition.onresult = (event) => {
            const text = event.results[0][0].transcript;
            console.log("Heard:", text);
            if (callback) callback(text);
        };

        this.recognition.onerror = (event) => {
            console.error("Speech recognition error", event.error);
        };

        this.recognition.onend = () => {
            console.log("Voice listening ended.");
        };

        this.recognition.start();
    }

    stopListening() {
        if (this.recognition) {
            this.recognition.stop();
        }
    }

    getGreeting() {
        const hour = new Date().getHours();
        if (hour < 12) return "Good morning!";
        if (hour < 18) return "Good afternoon!";
        return "Good evening!";
    }

    explainApp() {
        const greeting = this.getGreeting();
        const text = `${greeting} Welcome to Gig Finder. We help you find local student helpers. If you need help, click Find a Helper. If you want to earn money, click Earn Money.`;
        this.speak(text);
    }

    guideRegistration() {
        this.speak("Please enter your details to create an account. You can upload a profile picture and provide your phone number. Your phone number will be kept secure.");
    }

    guideLogin() {
        this.speak("Welcome back. Please enter your email and password to log in.");
    }
}

const voiceAssistant = new VoiceManager();
window.voiceAssistant = voiceAssistant;
