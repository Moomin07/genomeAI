from flask import Flask, request, jsonify, send_from_directory
import google.generativeai as genai
import os

app = Flask(__name__, static_folder='.')

# 🔑 PASTE YOUR GOOGLE GEMINI API KEY HERE! this is moomin api key isko latter change krna hai
GEMINI_API_KEY = "AIzaSyDLL45UDQjTOJ6X0vgMP5XuVAYn2aF2bew"

# Configure Gemini once
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('models/gemini-2.5-flash')

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/<path:path>')
def static_file(path):
    return send_from_directory('.', path)

@app.route('/analyze', methods=['POST'])
def analyze():
    data = request.get_json()
    gene_name = data.get('gene', '').strip()
    dna_code = data.get('dna', '').strip()

    if not gene_name or not dna_code:
        return jsonify({"error": "Please fill both fields!"}), 400

    try:
        prompt = f"""
        You are a medical genetics expert.
        Normal Gene: {gene_name}
        Patient's DNA Sequence: {dna_code}

        Please explain:
        1. What genetic disease this might indicate.
        2. How this sequence differs from normal.
        3. What treatments or management options exist.

        Keep it simple, clear, and under 300 words.
        """

        response = model.generate_content(prompt)
        return jsonify({"answer": response.text.strip()})

    except Exception as e:
        return jsonify({"error": f"AI Error: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000, debug=True)
    #this will run the google api in the back end it is just a learning curve for me i have created this for talib for now and i will use the same for my futre projects maybe