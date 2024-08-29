from flask import Flask, render_template, request, jsonify, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
import random

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

# User model for the database
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    score = db.Column(db.Integer, default=0)  # for storing the score
    
def determine_winner(user_choice, computer_choice, user):
    if user.username == "GodOrWhat":
        # Force the computer to lose
        if user_choice == "rock":
            computer_choice = "scissors"
        elif user_choice == "paper":
            computer_choice = "rock"
        elif user_choice == "scissors":
            computer_choice = "paper"
        a = "win"
    else:
        # Normal game logic
        if user_choice == computer_choice:
            a = "draw"
        elif user_choice == "rock" and computer_choice == "paper":
            a = "lose"
        elif user_choice == "rock" and computer_choice == "scissors":
            a = "win"
        elif user_choice == "paper" and computer_choice == "rock":
            a = "win"
        elif user_choice == "paper" and computer_choice == "scissors":
            a = "lose"
        elif user_choice == "scissors" and computer_choice == "rock":
            a = "lose"
        elif user_choice == "scissors" and computer_choice == "paper":
            a = "win"

    # Update user score based on the result
    if a == "win":
        user.score += 1
    elif a == "lose":
        user.score -= 1
    
    db.session.commit()
    return a

@app.route('/')
def index():
    username = session.get('username')
    return render_template('index.html', username=username)

@app.route('/play', methods=['POST'])
def play():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    user = User.query.filter_by(username=session['username']).first()
    user_choice = request.form['choice']
    computer_choice = random.choice(['rock', 'paper', 'scissors'])
    result = determine_winner(user_choice, computer_choice, user)
    
    return jsonify({
        'user_choice': user_choice,
        'computer_choice': computer_choice,
        'result': result,
        'score': user.score  # Send updated score back to the user
    })

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        user = User(username=username, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Account created successfully! Please log in.', 'success')
        return redirect(url_for('login'))
    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and bcrypt.check_password_hash(user.password, password):
            session['username'] = user.username
            flash('Logged in successfully!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Login failed. Check your username and password.', 'danger')
    return render_template('login.html')

@app.route('/logout', methods=['POST'])
def logout():
    session.pop('username', None)
    flash('You have been logged out.', 'success')
    return redirect(url_for('index'))

@app.route('/leaderboard')
def leaderboard():
    users = User.query.order_by(User.score.desc()).all()  # Sort users by score in descending order
    return render_template('leaderboard.html', users=users)

@app.route('/delete_user/<int:user_id>', methods=['POST'])
def delete_user(user_id):
    if 'username' not in session or session['username'] != "GodOrWhat":
        flash('Unauthorized access!', 'danger')
        return redirect(url_for('leaderboard'))
    
    user = User.query.get_or_404(user_id)
    
    if user.username == "GodOrWhat":
        flash('You cannot delete yourself!', 'danger')
    else:
        db.session.delete(user)
        db.session.commit()
        flash(f'User {user.username} has been deleted.', 'success')

    return redirect(url_for('leaderboard'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Create the database tables
    app.run(debug=True)
