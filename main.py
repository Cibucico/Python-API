from flask import Flask, request, jsonify
from flask import render_template
import sqlite3

app = Flask(__name__)

# Create a SQLite database and a 'books' table
conn = sqlite3.connect('books.db')
cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS books (
        id INTEGER PRIMARY KEY,
        author TEXT,
        language TEXT,
        title TEXT
    )
''')

# Insert 10 books into the 'books' table
books_data = [
    ("Hans Christian Andersen", "Danish", "Fairy Tales"),
    ("J.K. Rowling", "English", "Harry Potter and the Sorcerer's Stone"),
    ("Gabriel Garcia Marquez", "Spanish", "One Hundred Years of Solitude"),
    ("Jane Austen", "English", "Pride and Prejudice"),
    ("George Orwell", "English", "1984"),
    ("Leo Tolstoy", "Russian", "War and Peace"),
    ("J.R.R. Tolkien", "English", "The Lord of the Rings"),
    ("Mark Twain", "English", "The Adventures of Huckleberry Finn"),
    ("Agatha Christie", "English", "Murder on the Orient Express"),
    ("Harper Lee", "English", "To Kill a Mockingbird"),
]

cursor.executemany('''
    INSERT INTO books (author, language, title)
    VALUES (?, ?, ?)
''', books_data)

conn.commit()
conn.close()

@app.route('/', methods=['GET'])
def index():
    conn = sqlite3.connect('books.db')
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM books')
    books_data = cursor.fetchall()
    books_list = [{
        'id': book[0],
        'author': book[1],
        'language': book[2],
        'title': book[3],
    } for book in books_data]

    conn.close()
    return render_template('index.html', books=books_list)

@app.route('/books', methods=['GET', 'POST'])
def get_or_add_books():
    conn = sqlite3.connect('books.db')
    cursor = conn.cursor()

    if request.method == 'GET':
        cursor.execute('SELECT * FROM books')
        books_data = cursor.fetchall()
        books_list = []
        for book in books_data:
            books_list.append({
                'id': book[0],
                'author': book[1],
                'language': book[2],
                'title': book[3],
            })
        conn.close()
        return jsonify(books_list)

    elif request.method == 'POST':
        new_author = request.form['author']
        new_lang = request.form['language']
        new_title = request.form['title']

        cursor.execute('''
            INSERT INTO books (author, language, title)
            VALUES (?, ?, ?)
        ''', (new_author, new_lang, new_title))

        conn.commit()
        conn.close()

        return 'Book added successfully', 201

@app.route('/books/<int:book_id>', methods=['GET', 'PUT', 'DELETE'])
def get_update_delete_book(book_id):
    conn = sqlite3.connect('books.db')
    cursor = conn.cursor()

    if request.method == 'GET':
        cursor.execute('SELECT * FROM books WHERE id = ?', (book_id,))
        book = cursor.fetchone()
        if book:
            book_data = {
                'id': book[0],
                'author': book[1],
                'language': book[2],
                'title': book[3],
            }
            conn.close()
            return jsonify(book_data)
        else:
            conn.close()
            return 'Book not found', 404

    elif request.method == 'PUT':
        cursor.execute('SELECT * FROM books WHERE id = ?', (book_id,))
        existing_book = cursor.fetchone()

        if existing_book:
            updated_author = request.form.get('author', existing_book[1])
            updated_lang = request.form.get('language', existing_book[2])
            updated_title = request.form.get('title', existing_book[3])

            cursor.execute('''
                UPDATE books
                SET author=?, language=?, title=?
                WHERE id=?
            ''', (updated_author, updated_lang, updated_title, book_id))

            conn.commit()
            conn.close()
            return 'Book updated successfully'
        else:
            conn.close()
            return 'Book not found', 404

    elif request.method == 'DELETE':
        cursor.execute('SELECT * FROM books WHERE id = ?', (book_id,))
        book = cursor.fetchone()

        if book:
            cursor.execute('DELETE FROM books WHERE id = ?', (book_id,))
            conn.commit()
            conn.close()
            return 'Book deleted successfully'
        else:
            conn.close()
            return 'Book not found', 404

if __name__ == '__main__':
    app.run(debug=True) 