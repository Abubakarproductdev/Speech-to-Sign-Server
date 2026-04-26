import spacy
from flask import Flask, request, jsonify

app = Flask(__name__)

# Load the English NLP model
nlp = spacy.load("en_core_web_sm")

# REPLACE THESE with your exact 30 root words (video filenames minus the .mp4)
AVAILABLE_SIGNS = {
    "boss", "call", "client", "come", "day", "female",
    "give", "i", "idea", "love", "meet", "plan",
    "project", "read", "report", "this", "time",
    "today", "want", "you"
}

@app.route('/speech-to-sign', methods=['POST'])
def speech_to_sign():
    data = request.get_json()
    
    if not data or 'text' not in data:
        return jsonify({"error": "Text payload missing"}), 400

    raw_text = data['text']
    doc = nlp(raw_text)
    
    sequence = []

    for token in doc:
        # Convert the word to its root (e.g., "went" -> "go", "running" -> "run")
        lemma = token.lemma_.lower()
        raw_word = token.text.lower()
        
        # Only add the word to the sequence if we actually have a video for it
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