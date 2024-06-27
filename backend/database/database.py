import sqlite3

# Function to initialize the database
def initialize_database():
    conn = sqlite3.connect('phishing.db')
    c = conn.cursor()

    # Create table if not exists
    c.execute('''CREATE TABLE IF NOT EXISTS phishing_results
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  username TEXT,
                  url TEXT,
                  is_phishing BOOLEAN)''')

    conn.commit()
    conn.close()

# Function to insert phishing detection result into database
def insert_detection_result(username, url, is_phishing):
    conn = sqlite3.connect('phishing.db')
    c = conn.cursor()

    c.execute('''INSERT INTO phishing_results (username, url, is_phishing)
                 VALUES (?, ?, ?)''', (username, url, is_phishing))

    conn.commit()
    conn.close()
