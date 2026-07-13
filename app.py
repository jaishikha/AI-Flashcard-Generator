import os
from flask import Flask, render_template, request, jsonify
from pypdf import PdfReader  
from google import genai
from google.genai import types
from google.genai.errors import APIError

app = Flask(__name__)
client = genai.Client()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate_flashcards():
    if 'pdf' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400
        
    file = request.files['pdf']
    num_cards = request.form.get('count', '5') 
    
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    try:
        reader = PdfReader(file)
        extracted_text = ""
        
        for page in reader.pages:
            text = page.extract_text()
            if text:
                extracted_text += text + "\n"

        if not extracted_text.strip():
            return jsonify({"error": "Could not extract any readable text from this PDF."}), 400

        prompt = (
            f"You are an expert educator. Generate a concise list of exactly {num_cards} high-utility flashcards "
            "based strictly on the following text. Provide the output in a clean JSON format, "
            "where the root is an array named 'flashcards', and each item has a 'front' key "
            "(the question or concept) and a 'back' key (the brief answer or explanation).\n\n"
            f"Source Text:\n{extracted_text}"
        )

        response = client.models.generate_content(
            model='gemini-3.1-flash-lite',
            contents=prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json"
            )
        )

        return response.text, 200, {'Content-Type': 'application/json'}

    except APIError as e:
        print(f"!!! Google API Error: {str(e)}")
        return jsonify({"error": "Our AI service is currently facing a heavy traffic spike. Please wait a minute and try again!"}), 500
        
    except Exception as e:
        print(f"!!! System Crash: {str(e)}")
        return jsonify({"error": "Oops! Something went wrong on our end while processing your PDF. Please try again."}), 500
if __name__ == '__main__':
    app.run(debug=True)