// DOM Elements
const chatMessages = document.getElementById('chat-messages');
const messageInput = document.getElementById('message-input');
const sendButton = document.getElementById('send-button');
const typingIndicator = document.getElementById('typing-indicator');

// Function to add message to chat
function addMessage(text, isUser) {
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${isUser ? 'user' : 'bot'}`;
    
    const bubbleDiv = document.createElement('div');
    bubbleDiv.className = 'message-bubble';
    bubbleDiv.textContent = text;
    
    messageDiv.appendChild(bubbleDiv);
    chatMessages.appendChild(messageDiv);
    
    // Scroll to bottom
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

// Function to show typing indicator
function showTyping() {
    typingIndicator.style.display = 'block';
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

// Function to hide typing indicator
function hideTyping() {
    typingIndicator.style.display = 'none';
}

// Function to send message
async function sendMessage() {
    const message = messageInput.value.trim();
    
    if (!message) return;
    
    // Add user message to chat
    addMessage(message, true);
    messageInput.value = '';
    
    // Show typing indicator
    showTyping();
    
    try {
        // Send message to backend
        const response = await fetch('/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ message: message })
        });
        
        const data = await response.json();
        
        // Hide typing indicator
        hideTyping();
        
        if (data.status === 'success') {
            addMessage(data.response, false);
        } else {
            addMessage('Sorry, I encountered an error. Please try again.', false);
        }
        
    } catch (error) {
        hideTyping();
        addMessage('Sorry, there was a connection error. Please check your internet.', false);
    }
}

// Function to handle Enter key press
function handleKeyPress(event) {
    if (event.key === 'Enter') {
        sendMessage();
    }
}

// Function to initialize the chat
function initializeChat() {
    // Focus input on load
    messageInput.focus();
    
    // Add welcome message after a short delay
    setTimeout(() => {
        addMessage("Hello! I'm your AI assistant. How can I help you today?", false);
    }, 500);
}

// Event listeners
document.addEventListener('DOMContentLoaded', function() {
    sendButton.addEventListener('click', sendMessage);
    messageInput.addEventListener('keypress', handleKeyPress);
    initializeChat();
});

// Export functions for potential module use (if needed)
if (typeof module !== 'undefined' && module.exports) {
    module.exports = { addMessage, sendMessage };
}