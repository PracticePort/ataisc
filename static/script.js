// Function to add a chat message to the chat log
function addMessage(message, isUser) {
    const chatLog = document.querySelector('.chat-log');
    const messageClass = isUser ? 'user-message' : 'chatbot-message';
    const messageElement = document.createElement('div');
    messageElement.classList.add('chat-message', messageClass);
    messageElement.textContent = message;
    chatLog.appendChild(messageElement);
    chatLog.scrollTop = chatLog.scrollHeight;
}

// Event listener for the chat form submission
document.querySelector('.chat-form').addEventListener('submit', function(event) {
    event.preventDefault();
    const userInput = event.target.user_input.value;
    addMessage(userInput, true); // Add the user's message to the chat log
    event.target.user_input.value = ''; // Clear the input field

    // TODO: Send the user input to the chat endpoint and handle the chatbot's response
    // Replace the code below with the API call or processing logic
    const chatbotResponse = 'This is the response from the chatbot.';
    addMessage(chatbotResponse, false); // Add the chatbot's response to the chat log
});
