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
    M = UrlAnalysis()
    if url:
        is_phishing = M.is_phishing(url=url)

    response = {
        'is_phishing': is_phishing
    }
    print(response)
    print(url)
    return jsonify(response)

@app.route('/check-email', methods=['POST'])
def check_email():

    data = request.get_json()
    email_message = data.get('email_message')
    # Check if all required fields are present
    M = EmailDetection()
    is_phishing = M.is_phishing(url)

    print(email_message)
    print(response)
    response = {
        'is_phishing': is_phishing,
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
