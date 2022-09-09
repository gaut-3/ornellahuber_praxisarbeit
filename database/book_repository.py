import psycopg2


def load_user_ratings(username, conn):
    sql = """SELECT * FROM books WHERE fk_username = %s """

    cur = conn.cursor()
    cur.execute(sql, (username,))
    books = cur.fetchall()

    cur.close()

    books_as_objects = _map_books(books)

    return books_as_objects

def load_all_ratings(conn):
   
    cur = conn.cursor()
    cur.execute("SELECT * FROM books ")
    books = cur.fetchall()

    cur.close()

    books_as_objects = _map_books(books)

    return books_as_objects


def insert_new_rating_user(username, book_name, rating, conn):

    sql = """INSERT INTO books(title, rating, fk_username) VALUES(%s, %s, %s)"""

    cur = conn.cursor()
    cur.execute(sql, (book_name, rating, username))

    conn.commit()

    cur.close()


def _map_books(books):
    books_as_objects = []

    for book in books:
        book_id = book[0]
        book_title = book[1]
        book_rating = book[2]
        username = book[3]

        book_as_object = {
            'book_id': book_id,
            'book_title': book_title,
            'rating': book_rating,
            'username': username
        }
        books_as_objects.append(book_as_object)

    return books_as_objects
