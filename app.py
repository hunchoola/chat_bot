from flask import Flask, render_template, request, jsonify, send_from_directory
from langchain_groq import ChatGroq
from langgraph.prebuilt import create_react_agent
from dotenv import load_dotenv
import os

# Get absolute paths
current_dir = os.path.dirname(os.path.abspath(__file__))
template_dir = os.path.join(current_dir, 'templates')
static_dir = os.path.join(current_dir, 'static')

print(f"Current directory: {current_dir}")
print(f"Template directory: {template_dir}")
print(f"Static directory: {static_dir}")

# Check if directories exist
print(f"Templates exist: {os.path.exists(template_dir)}")
print(f"Static exist: {os.path.exists(static_dir)}")

load_dotenv()

app = Flask(__name__,
            template_folder=template_dir,
            static_folder=static_dir
            )

# Initialize chatbot
model = ChatGroq(
    model="llama-3.1-8b-instant",
    temperature=0.3,
    api_key=os.getenv("Your API Key")
)
tools = []
agent_executor = create_react_agent(model, tools)

# Manual static file routes to ensure they work


@app.route('/static/css/<path:filename>')
def serve_css(filename):
    return send_from_directory(os.path.join(static_dir, 'css'), filename)


@app.route('/static/js/<path:filename>')
def serve_js(filename):
    return send_from_directory(os.path.join(static_dir, 'js'), filename)


@app.route('/')
def home():
    return render_template('chat.html')


@app.route('/chat', methods=['POST'])
def chat():
    try:
        user_message = request.json['message']

        system_prompt = "Keep your response very short and concise. Answer in 1-2 sentences maximum. Be direct and to the point."

        full_response = ""
        for chunk in agent_executor.stream(
            {
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_message}
                ]
            },
            config={"configurable": {"thread_id": "123"}}
        ):
            if "agent" in chunk:
                for message in chunk["agent"].get("messages", []):
                    if hasattr(message, 'content') and message.content:
                        full_response += message.content

        return jsonify({'response': full_response, 'status': 'success'})

    except Exception as e:
        return jsonify({'response': f"Error: {str(e)}", 'status': 'error'})


@app.route('/debug')
def debug():
    """Debug page to check if static files are loading"""
    return '''
    <html>
    <head>
        <title>Debug Static Files</title>
        <link rel="stylesheet" href="/static/css/style.css">
    </head>
    <body>
        <h1>Static File Debug</h1>
        <p>Check if CSS and JS are loading properly.</p>
        <button onclick="testJS()">Test JavaScript</button>
        <script src="/static/js/script.js"></script>
        <script>
            function testJS() {
                alert('JavaScript is working!');
            }
        </script>
    </body>
    </html>
    '''


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
