
from flask import Flask, render_template, jsonify, request
from pymongo import MongoClient
from flask_cors import CORS

app = Flask(__name__, static_url_path='/static', static_folder='static')
CORS(app)


@app.route('/')
def home():
    init_db()
    return render_template('index.html')


def get_db_connection():
    uri = "mongodb+srv://admin:admin@library.04ejh8i.mongodb.net/?retryWrites=true&w=majority&appName=library"
    client = MongoClient(uri)
    return client


db = get_db_connection()["library"]


def init_db():
    # Drop existing collections
    db.authors.drop()
    db.genres.drop()
    db.publishers.drop()
    db.books.drop()

    # Insert authors
    db.authors.insert_many([
        {"_id": "a1", "name": "George Orwell"},
        {"_id": "a2", "name": "Harper Lee"},
        {"_id": "a3", "name": "Jane Austen"},
        {"_id": "a4", "name": "Francesc Miralles and Hector Garcia"}
    ])

    # Insert genres
    db.genres.insert_many([
        {"_id": "g1", "name": "Fiction"},
        {"_id": "g2", "name": "Non-Fiction"},
        {"_id": "g3", "name": "Romance"},
        {"_id": "g4", "name": "Satire"},
        {"_id": "g5", "name": "Self Help"}
    ])

    # Insert publishers
    db.publishers.insert_many([
        {"_id": "p1", "name": "Penguin Books"},
        {"_id": "p2", "name": "J.B. Lippincott & Co."},
        {"_id": "p3", "name": "T. Egerton"},
        {"_id": "p4", "name": "Secker and Warburg"},
        {"_id": "p5", "name": "Penguin Life"}
    ])

    # Insert books (without state)
    db.books.insert_many([
        {
            "_id": "b1",
            "title": "1984",
            "author_id": "a1",
            "publisher_id": "p1",
            "genre_id": "g1"
        },
        {
            "_id": "b2",
            "title": "To Kill a Mockingbird",
            "author_id": "a2",
            "publisher_id": "p2",
            "genre_id": "g1"
        },
        {
            "_id": "b3",
            "title": "Pride and Prejudice",
            "author_id": "a3",
            "publisher_id": "p3",
            "genre_id": "g3"
        },
        {
            "_id": "b4",
            "title": "Animal Farm",
            "author_id": "a1",
            "publisher_id": "p4",
            "genre_id": "g4"
        },
        {
            "_id": "b5",
            "title": "Ikigai",
            "author_id": "a4",
            "publisher_id": "p5",
            "genre_id": "g5"
        }
    ])


@app.route('/api/books', methods=['GET'])
def get_books():
    try:
        db = get_db_connection()["library"]

        # Aggregation pipeline to simulate SQL joins
        pipeline = [
            {
                "$lookup": {
                    "from": "authors",
                    "localField": "author_id",
                    "foreignField": "_id",
                    "as": "author"
                }
            },
            {"$unwind": "$author"},
            {
                "$lookup": {
                    "from": "publishers",
                    "localField": "publisher_id",
                    "foreignField": "_id",
                    "as": "publisher"
                }
            },
            {"$unwind": "$publisher"},
            {
                "$lookup": {
                    "from": "genres",
                    "localField": "genre_id",
                    "foreignField": "_id",
                    "as": "genre"
                }
            },
            {"$unwind": "$genre"},
            {
                "$lookup": {
                    "from": "borrowed",
                    "localField": "_id",
                    "foreignField": "book_id",
                    "as": "borrowed"
                }
            },
            {
                "$unwind": {
                    "path": "$borrowed",
                    "preserveNullAndEmptyArrays": True
                }
            },
            {
                "$lookup": {
                    "from": "customers",
                    "localField": "borrowed.customer_id",
                    "foreignField": "_id",
                    "as": "customer"
                }
            },
            {
                "$unwind": {
                    "path": "$customer",
                    "preserveNullAndEmptyArrays": True
                }
            },
            {
                "$project": {
                    "_id": 0,
                    "book_id": "$_id",
                    "book_title": "$title",
                    "author_name": "$author.name",
                    "publisher_name": "$publisher.name",
                    "genre_name": "$genre.name",
                    "state": "$borrowed.state",
                    "borrow_date": "$borrowed.borrow_date",
                    "return_date": "$borrowed.return_date",
                    "customer_name": "$customer.name"
                }
            }
        ]

        books = list(db.books.aggregate(pipeline))
        return jsonify(books), 200

    except Exception as e:
        print("Error:", e)
        return jsonify({'error': 'Failed to fetch books, please try again later.'}), 500


@app.route('/api/borrow', methods=['POST'])
def borrow_book():
    try:
        data = request.json
        book_id = data['book_id']
        customer_name = data['customer_name']
        borrow_date = data['borrow_date']

        # Check if customer exists
        customer = db.customers.find_one({"name": customer_name})
        if not customer:
            customer_id = db.customers.insert_one(
                {"name": customer_name}).inserted_id
        else:
            customer_id = customer["_id"]

        # Insert borrow record
        db.borrowed.insert_one({
            "book_id": book_id,
            "customer_id": customer_id,
            "borrow_date": borrow_date,
            "return_date": None,
            'state': 'Borrowed'
        })

        return jsonify({'message': 'Book borrowed successfully!'}), 200

    except Exception as e:
        print(f"Exception: {e}")
        return jsonify({'error': 'Failed to borrow book, please try again later.'}), 500


@app.route('/api/return', methods=['POST'])
def return_book():
    try:
        data = request.json
        book_id = data['book_id']
        return_date = data['return_date']

        result = db.borrowed.update_one(
            {
                "book_id": book_id,
                "return_date": None
            },
            {
                "$set": {"return_date": return_date, "state": "Present"}
            }
        )

        if result.modified_count == 0:
            return jsonify({'message': 'No active borrow record found for this book.'}), 404

        return jsonify({'message': 'Book returned successfully!'}), 200

    except Exception as e:
        print(f"Exception: {e}")
        return jsonify({'error': 'Failed to return book, please try again later.'}), 500


@app.route('/api/clear', methods=['DELETE'])
def clear_all():
    try:
        db.borrowed.delete_many({})
        return jsonify({'message': 'All records cleared successfully!'}), 200
    except Exception as e:
        print(f"Exception: {e}")
        return jsonify({'error': 'Failed to clear records, please try again later.'}), 500


if __name__ == '__main__':
    app.run(debug=True)
