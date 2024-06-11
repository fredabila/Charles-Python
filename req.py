import urllib.request
import json
from dotenv import load_dotenv
import os

load_dotenv()

# Initialize chat history
chat_history = []

def send_message(message, chat_history):
    try:
        url = "https://v1.api.buzzchat.site/charles/"

        hdr = {
            # Request headers
            'Content-Type': 'application/json',
            'Cache-Control': 'no-cache',
            'B-Key': os.environ['B_Key'],
        }

        # Append the new message to the chat history
        chat_history.append(f"User: {message}")

        # Combine the chat history into a single string
        combined_history = "\n".join(chat_history)

        # Request body with combined chat history
        data = {"content": combined_history}
        data = json.dumps(data)
        req = urllib.request.Request(url, headers=hdr, data=bytes(data.encode("utf-8")))

        req.get_method = lambda: 'POST'
        response = urllib.request.urlopen(req)
        response_data = json.loads(response.read().decode('utf-8'))

        # Get the AI response
        ai_response = response_data.get('message', 'No message field in response')

        # Append the AI response to the chat history
        chat_history.append(f"Charles: {ai_response}")

        return ai_response
    except Exception as e:
        return str(e)

# Start a conversation
while True:
    user_input = input("You: ")
    if user_input.lower() in ['exit', 'quit']:
        print("Ending conversation.")
        break
    response_message = send_message(user_input, chat_history)
    print(f"Charles: {response_message}")
