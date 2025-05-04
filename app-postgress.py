from flask import Flask, render_template, jsonify, request
import psycopg2
from flask_cors import CORS
from psycopg2.extras import RealDictCursor

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
        genre.name AS genre_name,
        borrowed.state AS book_state,
        borrowed.borrow_date AS borrow_date,
        borrowed.return_date AS return_date,
        customer.name AS customer_name
    FROM 
        book
    JOIN 
        author ON book.authorid = author.authorid
     JOIN 
        publishers ON book.publisherid = publishers.publisherid
    JOIN 
        genre ON book.genreid = genre.genreid
    LEFT JOIN
        borrowed ON book.bookid = borrowed.bookid
    LEFT JOIN
        customer ON borrowed.customerid = customer.customerid
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
                'genre_name': book[4],
                'state': book[5],
                'borrow_date': book[6],
                'return_date': book[7],
                'customer_name': book[8]
            }
            for book in books
        ]

        return jsonify(books), 200
    except Exception as e:
        return jsonify({'error': 'Failed to fetch books, please try again later.'}), 500


@app.route('/api/borrow', methods=['POST'])
def borrow_book():
    try:
        # Parse JSON data
        data = request.json
        book_id = data['book_id']
        customer_name = data['customer_name']
        borrow_date = data['borrow_date']

        customer_id = None

        # Establish a new database connection
        conn = get_db_connection()

        # Use RealDictCursor to get column names with the result
        cursor = conn.cursor(cursor_factory=RealDictCursor)

        # Check for existing customer
        cursor.execute(
            'SELECT * FROM customer WHERE name = %s', (customer_name,))
        customer = cursor.fetchone()

        if not customer:
            # Insert new customer if they do not exist
            cursor.execute(
                'INSERT INTO customer (name) VALUES (%s) RETURNING customerid', (customer_name,))
            customer_id = cursor.fetchone()['customerid']
        else:
            customer_id = customer['customerid']

        # Insert borrow record
        cursor.execute('''
    INSERT INTO borrowed (bookid, customerid, state, borrow_date)
    VALUES (%s, %s, 'Borrowed', %s)
''', (book_id, customer_id, borrow_date))

        # Commit the transaction
        conn.commit()

        # Close the connection
        cursor.close()
        conn.close()

        return jsonify({'message': 'Book borrowed successfully!'}), 200

    except Exception as e:
        # Log the exception for debugging
        print(f"Exception: {e}")
        return jsonify({'error': 'Failed to borrow book, please try again later.'}), 500


@app.route('/api/return', methods=['POST'])
def return_book():
    try:
        # Parse JSON data
        data = request.json
        book_id = data['book_id']
        return_date = data['return_date']

        # Establish a new database connection
        conn = get_db_connection()

        # Use RealDictCursor to get column names with the result
        cursor = conn.cursor(cursor_factory=RealDictCursor)

        # update borrow record
        cursor.execute('''
    UPDATE borrowed
    SET return_date = %s,
        state = %s
    WHERE bookid = %s
      AND state = 'Borrowed'
      AND return_date IS NULL
''', (return_date, "Present", book_id))

        # Commit the transaction
        conn.commit()

        # Close the connection
        cursor.close()
        conn.close()

        return jsonify({'message': 'Book returned successfully!'}), 200

    except Exception as e:
        # Log the exception for debugging
        print(f"Exception: {e}")
        return jsonify({'error': 'Failed to borrow book, please try again later.'}), 500


@app.route('/api/clear', methods=['DELETE'])
def clear_all():
    try:
        # Establish a new database connection
        conn = get_db_connection()

        # Use RealDictCursor to get column names with the result
        cursor = conn.cursor(cursor_factory=RealDictCursor)

        # Clear all records from the borrowed table
        cursor.execute('''
    TRUNCATE TABLE borrowed;
''')

        # Commit the transaction
        conn.commit()

        # Close the connection
        cursor.close()
        conn.close()

        return jsonify({'message': 'All records cleared successfully!'}), 200

    except Exception as e:
        # Log the exception for debugging
        print(f"Exception: {e}")
        return jsonify({'error': 'Failed to clear records, please try again later.'}), 500


if __name__ == '__main__':
    app.run(debug=True)
