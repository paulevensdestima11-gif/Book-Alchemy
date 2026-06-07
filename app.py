from flask import Flask, render_template, request, redirect, url_for, flash
import os

from data_models import db, Author, Book

app = Flask(__name__)

# ----------------------
# CONFIG
# ----------------------
basedir = os.path.abspath(os.path.dirname(__file__))

app.config['SQLALCHEMY_DATABASE_URI'] = (
    f"sqlite:///{os.path.join(basedir, 'data/library.sqlite')}"
)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = "dev-key"

db.init_app(app)


# ----------------------
# HOME + SEARCH
# ----------------------
@app.route("/")
def home():
    """
    Displays all books or filtered books based on search query.
    """

    query = request.args.get("q")

    if query:
        books = Book.query.filter(
            Book.title.ilike(f"%{query}%")
        ).all()
    else:
        books = Book.query.all()

    return render_template("home.html", books=books, query=query)


# ----------------------
# ADD AUTHOR (FIXED FOR GIVEN HTML)
# ----------------------
@app.route("/add_author", methods=["GET", "POST"])
def add_author():
    """
    Creates a new author in the database.
    Handles form field mismatch from provided HTML.
    """

    if request.method == "GET":
        return render_template("add_author.html")

    name = request.form.get("name")

    # IMPORTANT: matches HTML field "birthdate"
    birth_date = request.form.get("birthdate")

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


# ----------------------
# DELETE BOOK
# ----------------------
@app.route("/book/<int:book_id>/delete", methods=["POST"])
def delete_book(book_id):
    """
    Deletes a single book.
    """

    book = Book.query.get_or_404(book_id)

    db.session.delete(book)
    db.session.commit()

    flash("Book deleted successfully")
    return redirect(url_for("home"))


# ----------------------
# DELETE AUTHOR
# ----------------------
@app.route("/author/<int:author_id>/delete", methods=["POST"])
def delete_author(author_id):
    """
    Deletes an author and all related books (cascade handled in model).
    """

    author = Author.query.get_or_404(author_id)

    db.session.delete(author)
    db.session.commit()

    flash("Author and all related books deleted successfully")
    return redirect(url_for("home"))


# ----------------------
# DB INIT
# ----------------------
with app.app_context():
    db.create_all()