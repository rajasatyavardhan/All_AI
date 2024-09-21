from flask import Flask, render_template, request
from fuzzywuzzy import fuzz, process

app = Flask(__name__)

# Hardcoded list of AI tools
ai_tools = {
    "presentation": ["Beautiful.ai", "Tome", "SlidesAI"],
    "writing": ["Grammarly", "ChatGPT", "Writesonic"],
    "image editing": ["DALL·E", "Runway", "Remove.bg"],
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
    tools_found = find_best_match(query)
    if tools_found:
        return render_template('home.html', tools=tools_found, query=query)
    else:
        return render_template('home.html', tools=None, query=query)

if __name__ == '__main__':
    app.run(debug=True)
