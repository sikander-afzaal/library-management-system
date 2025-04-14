from flask import Flask, render_template, jsonify, request
import psycopg2
from flask_cors import CORS

app = Flask(__name__, static_url_path='/static', static_folder='static')
CORS(app)


@app.route('/')
def home():
    return render_template('index.html')


def get_db_connection():
    conn = psycopg2.connect(
        dbname='mydatabase',
        user='admin',
        password='admin',
        host='localhost',
        port='5432'
    )
    return conn


@app.route('/api/books', methods=['GET'])
def get_books():
    try:
        print('books')
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
    SELECT 
        book.bookid AS book_id,
        book.title AS book_title,
        author.name AS author_name,
        publishers.name AS publisher_name,
        genre.name AS genre_name
    FROM 
        book
    JOIN 
        author ON book.authorid = author.authorid
     JOIN 
        publishers ON book.publisherid = publishers.publisherid
    JOIN 
        genre ON book.genreid = genre.genreid
    
''')
        books = cursor.fetchall()
        cursor.close()
        conn.close()

        # Convert the result to a list of dictionaries
        books = [
            {
                'book_id': book[0],
                'book_title': book[1],
                'author_name': book[2],
                'publisher_name': book[3],
                'genre_name': book[4]
            }
            for book in books
        ]

        return jsonify(books), 200
    except Exception as e:
        return jsonify({'error': 'Failed to fetch books, please try again later.'}), 500


if __name__ == '__main__':
    app.run(debug=True)
