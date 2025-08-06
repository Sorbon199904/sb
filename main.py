from flask import Flask, request, jsonify, send_from_directory
import os

app = Flask(__name__)

# Боркунии луғат
with open("tajik_dictionary.txt", "r", encoding="utf-8") as f:
    tajik_dictionary = set(f.read().splitlines())

# Имло
def check_spelling(text, dictionary):
    words = text.lower().split()
    return [word for word in words if word not in dictionary]

# Грамматика
def check_grammar(text):
    suggestions = []
    words = text.lower().split()
    if "ман" in words:
        i = words.index("ман")
        if i + 1 < len(words):
            next_word = words[i + 1]
            if not next_word.endswith("ам"):
                suggestions.append(f"Феъли '{next_word}' бо 'ман' мувофиқат намекунад. Шояд '{next_word}ам' бошад.")
    return suggestions

# API
@app.route("/check", methods=["POST"])
def check_text():
    data = request.get_json()
    text = data.get("text", "")
    spelling = check_spelling(text, tajik_dictionary)
    grammar = check_grammar(text)
    return jsonify({
        "original": text,
        "spelling_errors": spelling,
        "grammar_suggestions": grammar
    })

# Барои хизматрасонии index.html
@app.route("/")
def index():
    return send_from_directory('.', 'index.html')

if __name__ == "__main__":
    app.run(debug=True)
