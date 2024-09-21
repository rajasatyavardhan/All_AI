import sqlite3
from flask import Flask, render_template, request
from fuzzywuzzy import fuzz, process

app = Flask(__name__)

# Create or connect to a database
conn = sqlite3.connect('searches.db', check_same_thread=False)
c = conn.cursor()

# Create a table for search logs
c.execute('''CREATE TABLE IF NOT EXISTS search_logs
             (query TEXT, timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)''')
conn.commit()

# Function to log user searches
def log_search(query):
    c.execute("INSERT INTO search_logs (query) VALUES (?)", (query,))
    conn.commit()

# Hardcoded list of AI tools
ai_tools = {
    "presentation": [
        {"name": "Beautiful.ai", "url": "https://www.beautiful.ai/"},
        {"name": "Tome", "url": "https://tome.app/"},
        {"name": "SlidesAI", "url": "https://slidesai.io/"}
    ],
    "writing": [
        {"name": "Grammarly", "url": "https://www.grammarly.com/"},
        {"name": "ChatGPT", "url": "https://chat.openai.com/"},
        {"name": "Writesonic", "url": "https://writesonic.com/"}
    ],
    "image editing": [
        {"name": "DALL·E", "url": "https://openai.com/dall-e"},
        {"name": "Runway", "url": "https://runwayml.com/"},
        {"name": "Remove.bg", "url": "https://www.remove.bg/"}
    ],
}

def find_best_match(query):
    # Find the category that best matches the user's query
    categories = ai_tools.keys()
    best_match = process.extractOne(query, categories)
    if best_match and best_match[1] > 60:  # Set a threshold for match confidence
        return ai_tools[best_match[0]]
    return None

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/search')
def search():
    query = request.args.get('query').lower()
    log_search(query)  # Log each search
    tools_found = find_best_match(query)
    return render_template('home.html', tools=tools_found, query=query)

if __name__ == '__main__':
    app.run(debug=True)
