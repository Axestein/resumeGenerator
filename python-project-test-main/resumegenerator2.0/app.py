from flask import Flask, request, jsonify, render_template
import google.generativeai as genai
import logging
import json

# Initialize Flask app
app = Flask(__name__)

# Setup logging
logging.basicConfig(level=logging.DEBUG)

# Set API key directly
API_KEY = "AIzaSyDklOoZrYueeVgySMymMbG_gzX2LEc3ocw"
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate_resume', methods=['POST'])
def generate_resume():
    try:
        data = request.get_json()

        # Create prompt for Gemini
        prompt = (
            "Generate an ATS-friendly resume with the following characteristics:\n"
            "Format: Use a professional format with clear headings for each section.\n"
            "        Use bullet points to list responsibilities for each job experience and skills.\n"
            "        Do not use tables, avoid complex formatting. Make it easily parsable by ATS.\n"
            "        Include:\n"
            "           1. Personal Summary\n"
            "           2. Experience (job title, company, dates, and responsibility)\n"
            "           3. Education (degree, university, dates)\n"
            "           4. Skills (technical and soft skills).\n"
            "Length: Limit the resume to a single page.\n"
            "Tone: Professional and concise.\n"
            f"Here is the data provided for the resume:\n\n"
            f"Personal Summary: {data['personal_summary']}\n"
            f"Experience: {json.dumps(data['experience'])}\n"
            f"Education: {json.dumps(data['education'])}\n"
            f"Skills: {json.dumps(data['skills'])}\n"
        )

        # Generate the resume
        response = model.generate_content(prompt)

        # Return the result
        return jsonify({
            'status': 'success',
            'resume': response.text
        })

    except Exception as e:
        logging.error(f"Error generating resume: {str(e)}")
        return jsonify({
            'status': 'error',
            'error': str(e)
        }), 500

if __name__ == '__main__':
    print("Starting Flask application...")
    app.run(debug=True)
