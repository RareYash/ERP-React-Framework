// Initialize Streamlit component communication
Streamlit.setComponentReady();

// DOM elements
const fab = document.getElementById('chatbot-fab');
const window = document.getElementById('chatbot-window');
const closeBtn = document.getElementById('chatbot-close');
const sendBtn = document.getElementById('chatbot-send');
const input = document.getElementById('chatbot-input');
const messagesContainer = document.getElementById('chatbot-messages');

// Toggle chatbot window
fab.addEventListener('click', () => {
    window.classList.toggle('hidden');
});

closeBtn.addEventListener('click', () => {
    window.classList.add('hidden');
});

// Send message
function sendMessage() {
    const messageText = input.value.trim();
    if (messageText) {
        // Send message to Streamlit via URL query parameter
        const url = new URL(window.parent.location);
        url.searchParams.set('chatbot_query', encodeURIComponent(messageText));
        window.parent.history.pushState({}, '', url); // Update URL without reloading

        input.value = '';
    }
}

sendBtn.addEventListener('click', sendMessage);
input.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') {
        sendMessage();
    }
});

// Add a message to the chat window
function addMessage(text, className) {
    const messageElement = document.createElement('div');
    messageElement.className = `message ${className}`;
    messageElement.innerHTML = text; // Use innerHTML to render HTML content
    messagesContainer.appendChild(messageElement);
    messagesContainer.scrollTop = messagesContainer.scrollHeight;
}

// Render chat history on load
window.addEventListener('load', function() {
    messagesContainer.innerHTML = ''; // Clear existing messages
    chatHistory.forEach(msg => {
        addMessage(msg.content, msg.role === 'user' ? 'user-message' : 'bot-message');
    });
});
