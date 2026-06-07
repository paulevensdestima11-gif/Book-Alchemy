from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Author(db.Model):
    """
    Represents an author in the library system.

    Attributes:
        id (int): Primary key.
        name (str): Author name.
        birth_date (date): Optional birthdate.
        date_of_death (date): Optional death date.
        books (relationship): One-to-many relationship with Book.
    """

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    birth_date = db.Column(db.Date, nullable=True)
    date_of_death = db.Column(db.Date, nullable=True)

    books = db.relationship(
        "Book",
        backref="author",
        cascade="all, delete",
        lazy=True
    )


class Book(db.Model):
    """
    Represents a book in the library system.

    Attributes:
        id (int): Primary key.
        isbn (str): Unique ISBN identifier.
        title (str): Book title.
        publication_year (int): Year published.
        author_id (int): Foreign key linking to Author.
    """

    id = db.Column(db.Integer, primary_key=True)
    isbn = db.Column(db.String(20), unique=True, nullable=False)
    title = db.Column(db.String(200), nullable=False)
    publication_year = db.Column(db.Integer, nullable=True)

    author_id = db.Column(
        db.Integer,
        db.ForeignKey('author.id'),
        nullable=False
    )