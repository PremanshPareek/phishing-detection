from flask import Flask, request, jsonify, abort
from database.database import initialize_database, insert_detection_result
from ML.EmailDetection.EmailDetection import EmailDetection
from ML.UrlAnalysis.UrlAnalysis import UrlAnalysis

app = Flask(__name__)

    # Initialize the database
initialize_database()

@app.route('/check-url', methods=['POST'])
def check_url():

    data = request.get_json()
    email_message = data.get('email_message')
    url = data.get('url')
    username = data.get('username')
    # Check if all required fields are present



    is_phishing = True
    M = UrlAnalysis
    if url:
        if M.is_phishing(url):
            is_phishing = True
            insert_detection_result(username, url, True)

    response = {
        'is_phishing': is_phishing
    }
    print(response)
    return jsonify(response)

@app.route('/check-email', methods=['POST'])
def check_email():

    data = request.get_json()
    email_message = data.get('email_message')
    url = data.get('url')
    username = data.get('username')
    # Check if all required fields are present
    if not username:
        abort(400, description="Bad Request: Missing required fields (username, email_message, url)")



    is_phishing_ = True
    M = EmailDetection
    if email_message:
        if M.is_phishing(url):
            is_phishing = True

    response = {
        'is_phishing': is_phishing_,
        'success': True
    }

    return jsonify(response)


# Error handler for 400 Bad Request
@app.errorhandler(400)
def bad_request(error):
    print(error.description)
    return jsonify({
        'error': 'Bad Request',
        'message': error.description,
    }), 400

if __name__ == '__main__':
    app.run(debug=True)
