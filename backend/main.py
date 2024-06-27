from flask import Flask, request, jsonify, abort
from database import initialize_database, insert_detection_result
from ML.EmailDetection import EmailDetection
from ML.UrlAnalysis import UrlAnalysis

app = Flask(__name__)

    # Initialize the database
initialize_database()

@app.route('/check', methods=['POST'])
def check():

    data = request.get_json()
    email_message = data.get('email_message')
    url = data.get('url')
    username = data.get('username')
    # Check if all required fields are present
    if not username:
        abort(400, description="Bad Request: Missing required fields (username, email_message, url)")

    is_phishing = False

        # Perform URL phishing analysis
    if url:
        if UrlAnalysis.is_phishing(url):
            is_phishing = True
            insert_detection_result(username, url, True)
            
    if email_message:
        # Perform email phishing analysis
        if EmailDetection.is_phishing(email_message):
            is_phishing = True
            insert_detection_result(username, 'Email message', True)

    response = {
        'is_phishing': is_phishing,
        'success': True
    }

    return jsonify(response)

# Error handler for 400 Bad Request
@app.errorhandler(400)
def bad_request(error):
    return jsonify({
        'error': 'Bad Request',
        'message': error.description,
    }), 400

if __name__ == '__main__':
    app.run(debug=True)
