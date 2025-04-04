// script.js
document.addEventListener('DOMContentLoaded', () => {
    const chatBox = document.getElementById('chat-box');
    const userInput = document.getElementById('user-input');
    const sendButton = document.getElementById('send-button');

    // Function to add a message to the chatbox
    function addMessage(message, sender) {
        const messageElement = document.createElement('div');
        messageElement.classList.add('message', `${sender}-message`); // e.g., 'user-message' or 'bot-message'

        const paragraph = document.createElement('p');
        paragraph.textContent = message;
        messageElement.appendChild(paragraph);

        chatBox.appendChild(messageElement);

        // Scroll to the bottom of the chatbox
        chatBox.scrollTop = chatBox.scrollHeight;
    }

    // Function to handle sending message
    async function handleSendMessage() {
        const messageText = userInput.value.trim();
        if (messageText === '') return; // Don't send empty messages

        // Display user's message
        addMessage(messageText, 'user');
        userInput.value = ''; // Clear input field
        userInput.focus(); // Keep focus on input

        // --- Send message to backend and get reply ---
        try {
            // Optional: Add a "Bot is typing..." indicator
            addMessage("...", 'bot'); // Placeholder typing indicator
            const typingIndicator = chatBox.lastChild; // Get reference to typing indicator

            const response = await fetch('/chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ message: messageText }),
            });

            // Remove the "typing..." indicator
            chatBox.removeChild(typingIndicator);

            if (!response.ok) {
                console.error("Error fetching chat response:", response.statusText);
                addMessage("Sorry, I couldn't connect to the server.", 'bot');
                return;
            }

            const data = await response.json();
            const botReply = data.reply;

            // Display bot's reply
            addMessage(botReply, 'bot');

        } catch (error) {
             // Remove the "typing..." indicator even if there's an error
            if (chatBox.lastChild && chatBox.lastChild.textContent === "...") {
                chatBox.removeChild(chatBox.lastChild);
            }
            console.error("Error during chat communication:", error);
            addMessage("An error occurred. Please try again later.", 'bot');
        }
    }

    // Event Listeners
    sendButton.addEventListener('click', handleSendMessage);

    userInput.addEventListener('keypress', (event) => {
        // Check if Enter key was pressed (and not Shift+Enter)
        if (event.key === 'Enter' && !event.shiftKey) {
            event.preventDefault(); // Prevent default form submission/newline
            handleSendMessage();
        }
    });

    // Optional: Add initial focus to input
    userInput.focus();

}); // End DOMContentLoaded