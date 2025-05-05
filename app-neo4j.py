import atexit
from flask import Flask, render_template, jsonify, request
from neo4j import GraphDatabase
from flask_cors import CORS

app = Flask(__name__, static_url_path='/static', static_folder='static')
CORS(app)


@app.route('/')
def home():
    return render_template('index.html')


def get_db_connection():
    uri = "bolt://localhost:7687"
    username = "neo4j"
    password = "Sevensis2@"
    driver = GraphDatabase.driver(uri, auth=(username, password))
    return driver


driver = get_db_connection()


@app.route('/api/books', methods=['GET'])
def get_books():
    with driver.session() as session:
        result = session.run('''
            MATCH (b:Book)-[:WROTE]-(a:Author),
                  (b)-[:PUBLISHED_BY]-(p:Publisher),
                  (b)-[:BELONGS_TO]-(g:Genre)
            OPTIONAL MATCH (b)-[r:BORROWED]-(c:Customer)
            RETURN b.title AS book_title,
                   a.name AS author_name,
                   p.name AS publisher_name,
                   g.name AS genre_name,
                   r.state AS book_state,
                   r.borrow_date AS borrow_date,
                   r.return_date AS return_date,
                   c.name AS customer_name
            ''')
        books = []
        for record in result:
            books.append({
                "book_id": len(books) + 1,
                "book_title": record["book_title"],
                "author_name": record["author_name"],
                "publisher_name": record["publisher_name"],
                "genre_name": record["genre_name"],
                "state": record.get("book_state"),
                "borrow_date": str(record.get("borrow_date")) if record.get("borrow_date") else None,
                "return_date": str(record.get("return_date")) if record.get("return_date") else None,
                "customer_name": record.get("customer_name")
            })
        return jsonify(books)


@app.route('/api/borrow', methods=['POST'])
def borrow_book():
    try:
        # Parse JSON data
        data = request.json
        book_title = data['book_id']
        customer_name = data['customer_name']
        borrow_date = data['borrow_date']

        with driver.session() as session:
            # Check for existing customer
            result = session.run(
                "MATCH (c:Customer {name: $name}) RETURN c", name=customer_name)
            customer = result.single()

            if not customer:
                # Create new customer if they do not exist
                session.run(
                    "CREATE (c:Customer {name: $name})", name=customer_name)

            # Insert borrow record
            session.run('''
                MATCH (b:Book {title: $title}), (c:Customer {name: $cname})
                CREATE (c)-[:BORROWED {state: 'Borrowed', borrow_date: date($bdate)}]->(b)
                ''', title=book_title, cname=customer_name, bdate=borrow_date)

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
        book_title = data['book_id']
        return_date = data['return_date']

        with driver.session() as session:
            # Update borrow record
            session.run('''
                MATCH (c:Customer)-[r:BORROWED]->(b:Book {title: $title})
                WHERE r.state = 'Borrowed' AND r.return_date IS NULL
                SET r.return_date = date($rdate), r.state = 'Present'
                ''', title=book_title, rdate=return_date)

        return jsonify({'message': 'Book returned successfully!'}), 200

    except Exception as e:
        # Log the exception for debugging
        print(f"Exception: {e}")
        return jsonify({'error': 'Failed to return book, please try again later.'}), 500


@app.route('/api/clear', methods=['DELETE'])
def clear_all():
    try:
        with driver.session() as session:
            # Clear all BORROWED relationships
            session.run('MATCH ()-[r:BORROWED]->() DELETE r')

        return jsonify({'message': 'All records cleared successfully!'}), 200

    except Exception as e:
        # Log the exception for debugging
        print(f"Exception: {e}")
        return jsonify({'error': 'Failed to clear records, please try again later.'}), 500


if __name__ == '__main__':
    app.run(debug=True)

atexit.register(driver.close)
