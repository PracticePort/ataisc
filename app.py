from flask import Flask, render_template, request, send_from_directory
import pandas as pd
import openai
import time

# Initialize the OpenAI API client
openai.api_key = 'YOUR_OPENAI_API_KEY'

# Load the CSV data into memory
df = pd.read_csv('/workspace/ataisc/CSV/ata62223(1).csv)

# Initialize the Flask application
app = Flask(__name__)

# Store the chat session details
chat_sessions = {}

# Landing page of your web app where users can initiate a chat with the chatbot
@app.route('/')
def home():
    return render_template('index.html')  # Render the HTML template for the chat interface

# Endpoint that handles the user's input and returns the chatbot's response
@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.form['user_input']  # Retrieve the user's input from the form data

    session_id = request.form['session_id']  # Retrieve the session ID

    # Check if the session ID is already in progress
    if session_id in chat_sessions:
        session = chat_sessions[session_id]

        # Check if the session is still within the time limit
        if time.time() - session['start_time'] > 1800:
            # Session has expired, remove it from the active sessions
            del chat_sessions[session_id]
            response = "Sorry, the chat session has expired. Please start a new session."
        else:
            # Check if the maximum API call limit has been reached
            if session['api_calls'] >= 30:
                response = "Sorry, you have reached the maximum API call limit for this session."
            else:
                # Generate the chatbot's response
                response = generate_chatbot_response(user_input)

                # Increment the API call count for the session
                session['api_calls'] += 1

    else:
        # New session, require manual approval before starting
        response = "Your chat request is pending approval. Please wait for confirmation."

        # Save the session details for manual approval
        chat_sessions[session_id] = {
            'start_time': time.time(),
            'api_calls': 0
        }

        # TODO: Send notification to your phone or email for approval

    # Return the response to the user
    return response

def generate_chatbot_response(user_input):
    # Define the persona of the chatbot
    persona = """
    My name is ChatGPT. I'm an AI assistant trained to help you with your queries.
    I'm here to provide you with information and recommendations on various tools.
    """

    # Define a series of prompts or a prompt chain for the chatbot
    # Adjust the prompts based on your desired conversation flow
    prompts = [
        "You: " + user_input,
        "ChatGPT: ",
        persona
    ]
    
    # Generate the chatbot's response using the GPT-3.5 API
    response = openai.Completion.create(
        engine='text-davinci-003',
        prompt= '\n'.join(prompts),
        max_tokens=100,
        n=1,
        stop=None,
        temperature=0.7
    )

    # Extract the generated response from the API response object
    generated_response = response.choices[0].text.strip()

    # Use the loaded CSV data to enhance the chatbot's responses
    matching_data = df[df['User Query'] == user_input]
    if not matching_data.empty:
        relevant_info = matching_data['Information'].values[0]
        generated_response += " " + relevant_info

    return generated_response


# Endpoint to serve static files like CSS stylesheets or JavaScript files
@app.route('/static/<path:filename>')
def serve_static(filename):
    return send_from_directory('static', filename)

if __name__ == '__main__':
    app.run()
