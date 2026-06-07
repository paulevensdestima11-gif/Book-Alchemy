from flask import Flask, render_template, request, redirect, url_for, flash
import os

from data_models import db, Author, Book

app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))

app.config['SQLALCHEMY_DATABASE_URI'] = (
    f"sqlite:///{os.path.join(basedir, 'data/library.sqlite')}"
)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = "dev-key"

db.init_app(app)


@app.route("/")
def home():
    """
    Home page route.

    Displays all books in the library.
    If a search query is provided, filters books by title using case-insensitive partial matching.

    Returns:
        Rendered home.html template with:
        - books (list of Book objects)
        - query (optional search string)
    """

    query = request.args.get("q")

    if query:
        books = Book.query.filter(
            Book.title.ilike(f"%{query}%")
        ).all()
    else:
        books = Book.query.all()

    return render_template("home.html", books=books, query=query)


@app.route("/add_author", methods=["GET", "POST"])
def add_author():
    """
    Add a new author to the database.

    GET:
        Renders the author creation form.

    POST:
        Validates input and creates a new Author record.
        Stores optional birth and death dates if provided.

    Returns:
        Redirects to /add_author with flash message on success or error.
    """

    if request.method == "GET":
        return render_template("add_author.html")

    name = request.form.get("name")
    birth_date = request.form.get("birth_date")
    date_of_death = request.form.get("date_of_death")

    if not name:
        flash("Name is required")
        return redirect(url_for("add_author"))

    author = Author(
        name=name,
        birth_date=birth_date if birth_date else None,
        date_of_death=date_of_death if date_of_death else None
    )

    db.session.add(author)
    db.session.commit()

    flash("Author successfully added")
    return redirect(url_for("add_author"))


@app.route("/book/<int:book_id>/delete", methods=["POST"])
def delete_book(book_id):
    """
    Delete a specific book from the database.

    Args:
        book_id (int): ID of the book to delete.

    Returns:
        Redirects to home page with success message.
    """

    book = Book.query.get_or_404(book_id)

    db.session.delete(book)
    db.session.commit()

    flash("Book deleted successfully")
    return redirect(url_for("home"))


@app.route("/author/<int:author_id>/delete", methods=["POST"])
def delete_author(author_id):
    """
    Delete an author and all associated books from the database.

    Args:
        author_id (int): ID of the author to delete.

    Returns:
        Redirects to home page with success message.
    """

    author = Author.query.get_or_404(author_id)

    db.session.delete(author)
    db.session.commit()

    flash("Author and all related books deleted successfully")
    return redirect(url_for("home"))


with app.app_context():
    db.create_all()


if __name__=="__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)