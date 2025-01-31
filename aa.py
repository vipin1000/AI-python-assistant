import requests
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Define the Hugging Face API URL and your API key
HUGGINGFACE_API_URL = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.3"  # The model URL
API_KEY = "xxxxxxxxxxxxxxxxxxxxx"  # Replace with your Hugging Face API key

def get_chatbot_response(prompt):
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    query = f'''You are a Python programming expert with great communication skills. You are highly skilled in Python development and software engineering, capable of explaining complex coding concepts clearly and concisely. When users ask you questions, you should:

1. **Provide clear and concise answers**, offering simple and effective explanations, code examples.
2. **Break down complex concepts** in an easy-to-understand manner, ensuring the user learns from the conversation.
3. **Offer advice on best practices** in Python programming, including code optimization, readability, and efficient problem-solving.
4. **Respond confidently and professionally**, with a helpful and friendly tone, keeping the conversation educational yet approachable.
5. **Help debug and solve coding problems** when users share error messages or describe issues in their code.
6. **only generate response for python related problems** if you find that the user input a query that does not seem like related to python just generate "can only generate response for python related queries"
7.** Add ssome emoji to make it a fun conversation**
For example:
- If the user asks how to handle file I/O in Python, you would explain how to read and write files in Python, provide an example of code, and explain each step of the process.
- If the user asks for help with a Python bug, you would help debug the issue, explaining what went wrong and how to fix it.

Your goal is to help the user write Python code effectively, offering practical advice while ensuring the user learns and understands the solution.
---
Generated response: ""{prompt}""
'''

    payload = {
        "inputs": query,  # Text input for the model
        "options": {"use_cache": False}  # Optional settings
    }

    try:
        response = requests.post(HUGGINGFACE_API_URL, json=payload, headers=headers)
        print(f"API Response Status: {response.status_code}")
        print(f"API Response Text: {response.text}")  # Log the response text for debugging
        
        if response.status_code == 200:
            response_data = response.json()
            
            # Access the first item of the response (it's a list)
            generated_text = response_data[0].get("generated_text", "")
            
            # Slice the response after the '--' part
            if '--' in generated_text:
                result = generated_text.split('Generated response:')[1].strip()  # Return the part after '--'
            else:
                result = generated_text.strip()  # If no '--', just return the full response
            
            return result  # Return the relevant part of the response
            
        else:
            raise Exception(f"Hugging Face API Error: {response.status_code} - {response.text}")
 
    except Exception as e:
        print(f"Error: {e}")
        return str(e)

# Flask route to render the homepage
@app.route('/')
def index():
    return render_template('index.html')

# Flask route to handle form submissions and API interaction
@app.route('/ask', methods=['POST'])
def ask():
    try:
        user_input = request.form['user_input']
        if not user_input:
            raise ValueError("User input is empty.")

        chatbot_response = get_chatbot_response(user_input)
        return jsonify({'response': chatbot_response})

    except Exception as e:
        # Log the error message to the console
        print(f"Error: {e}")

        # Return a JSON response with the error message
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=7001)
