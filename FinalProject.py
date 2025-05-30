# Script Name: Final-Project.py
# Author: Allison Losso 
# Date: 4/5/2025
# Description: The Bookbag is a application that allows the user to track their books.
# Usage: python3 Final-Project.py
# Version: 4.0
# Credits: This script is based on the original Final-Project.py script by Allison Losso with the help of ChatGPT.

from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///books.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Database model
class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    status = db.Column(db.String(20), nullable=False, default='Currently Reading')
    rating = db.Column(db.Integer, nullable=True)  # Rating from 1 to 5
    favorite = db.Column(db.Boolean, default=False)  # Mark as favorite

    def __repr__(self):
        return f'<Book {self.title}>'

# Home page with list of books categorized by status
@app.route('/')
def index():
    currently_reading = Book.query.filter_by(status='Currently Reading').all()
    finished = Book.query.filter_by(status='Finished').all()
    dnf = Book.query.filter_by(status='DNF').all()
    favorites = Book.query.filter_by(favorite=True).all()
    return render_template('index.html', currently_reading=currently_reading, finished=finished, dnf=dnf, favorites=favorites)

# Add a new book
@app.route('/add', methods=['POST'])
def add_book():
    title = request.form['title']
    author = request.form['author']
    status = request.form['status']
    rating = request.form.get('rating')
    favorite = 'favorite' in request.form
    rating = int(rating) if rating and status == 'Finished' else None
    new_book = Book(title=title, author=author, status=status, rating=rating, favorite=favorite)
    db.session.add(new_book)
    db.session.commit()
    return redirect(url_for('index'))

# Update book status, rating, or favorite
@app.route('/update/<int:book_id>', methods=['POST'])
def update_book(book_id):
    book = Book.query.get_or_404(book_id)
    book.status = request.form['status']
    rating = request.form.get('rating')
    book.rating = int(rating) if rating and book.status == 'Finished' else None
    book.favorite = 'favorite' in request.form
    db.session.commit()
    return redirect(url_for('index'))

# Delete a book
@app.route('/delete/<int:book_id>', methods=['POST'])
def delete_book(book_id):
    book = Book.query.get_or_404(book_id)
    db.session.delete(book)
    db.session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)

