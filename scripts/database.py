import sqlite3

# Verbindung zur Datenbank herstellen
def init_db():
    conn = sqlite3.connect('data/linkedin_comments.db')  # Datenbank in 'data/' speichern
    cursor = conn.cursor()

    # Tabelle erstellen, falls sie nicht existiert
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS comments (
            post_id TEXT PRIMARY KEY,
            comment TEXT
        )
    ''')
    conn.commit()
    conn.close()

# Funktion zum Speichern eines Kommentars
def save_comment(post_id, comment):
    conn = sqlite3.connect('data/linkedin_comments.db')
    cursor = conn.cursor()
    cursor.execute('INSERT OR IGNORE INTO comments (post_id, comment) VALUES (?, ?)', (post_id, comment))
    conn.commit()
    conn.close()

# Funktion, um zu prüfen, ob ein Beitrag schon kommentiert wurde
def is_comment_saved(post_id):
    conn = sqlite3.connect('data/linkedin_comments.db')
    cursor = conn.cursor()
    cursor.execute('SELECT 1 FROM comments WHERE post_id = ?', (post_id,))
    result = cursor.fetchone()
    conn.close()
    return result is not None
