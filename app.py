from flask import Flask, request, jsonify
from flask_cors import CORS
import simplemma
import re

app = Flask(__name__)
CORS(app) 

AVAILABLE_SIGNS = {
    "boss", "call", "client", "come", "day", "female",
    "give", "i", "idea", "love", "meet", "plan",
    "project", "read", "report", "this", "time",
    "today", "want", "you","help","job","make","male"
}

@app.route('/speech-to-sign', methods=['POST'])
def speech_to_sign():
    data = request.get_json()
    
    if not data or 'text' not in data:
        return jsonify({"error": "Text payload missing"}), 400

    raw_text = data['text']
    
    clean_text = re.sub(r'[^\w\s]', '', raw_text)
    tokens = clean_text.split()
    
    sequence = []

    for word in tokens:
        raw_word = word.lower()
        
        lemma = simplemma.lemmatize(raw_word, lang='en')
        
        if lemma in AVAILABLE_SIGNS:
            sequence.append(lemma)
        elif raw_word in AVAILABLE_SIGNS and lemma not in AVAILABLE_SIGNS:
            sequence.append(raw_word)

    return jsonify({
        "original_text": raw_text,
        "video_sequence": sequence
    }), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=5000)