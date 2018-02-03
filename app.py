from flask import Flask, flash, redirect, render_template, request, session, abort
import os
from flask_sqlalchemy import SQLAlchemy
#from flask.ext.session import Session


app = Flask(__name__)
app.debug=True
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://vrpvhvllhyasco:febb795e614ed1c0999098b5994fbbac3279df274ef02cb1e23fe1bf059c07c8@ec2-50-16-231-2.compute-1.amazonaws.com:5432/dedpgiv3mf2l6f'
app.secret_key = 'super secret key'
db = SQLAlchemy(app)


class Users(db.Model):
    #__tablename__ = "Users"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(100), nullable = False)
    last_name = db.Column(db.String(100), nullable = False)
    email = db.Column(db.String(100), nullable = False)
    pwd = db.Column(db.String(100), nullable = False)

class Posts(db.Model):
	id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	#post_user = db.Column()
	title = db.Column(db.String(100), nullable=False)
	text = db.Column(db.String(1000), nullable=False)

@app.route('/')
@app.route('/login_signup')
def login_signup():
    return render_template('login_signup.html')

@app.route('/home')
def home():
	return render_template('home.html', user=user)

@app.route('/post')
def post():
	return render_template('post.html', user=user)

@app.route('/sessions')
def sessions():
	posts=Posts.query.all()
	return render_template('sessions.html', posts=posts, user=user)

@app.route('/conferences')
def conferences():
	return render_template('conferences.html', user=user)

@app.route('/members')
def members():
	users = Users.query.all()
	print(users)
	return render_template('members.html', users=users)

@app.route('/about')
def about_page():
	return render_template('about_page.html')

##################Signup####################
@app.route('/signup', methods=['GET','POST'])

def signup():
	
	if request.method == 'POST':
		user = Users()
		user.first_name = request.form['first_name']
		user.last_name = request.form['last_name']
		user.email = request.form['email']
		user.pwd = request.form['pwd']
		db.session.add(user)
		db.session.commit()
		return render_template('home.html', user = user)

	elif request.method == 'GET':
		return render_template('login_signup.html')

#################login######################
@app.route('/login', methods=['GET','POST'])
def login():
	if request.method == 'GET':
		return render_template('home.html', email=email, pwd=pwd)

	elif request.method == 'POST':
		user = db.session.query(Users).filter_by(email=request.form['email']).first()
		if user.pwd == request.form.get('pwd'):
			session['logged_in'] = True
			return render_template('home.html',user=user)

		else:
			flash('Wrong Password!')
			return render_template('login_signup.html')

##################Post######################
@app.route('/post', methods=['GET','POST'])
def posts():
	if request.method == 'GET':
		return render_template('post.html')

	elif request.method == 'POST':
		print(0)
		new_post = Posts()
		print(5)
		new_post.title = request.form['title']
		print(6)
		new_post.text = request.form['text']
		print(1)
		db.session.add(new_post)
		print(2)
		db.session.commit()
		print(3)
		posts = Posts.query.all()
		print(4)
		print(posts)
		return render_template('sessions.html', posts=posts)
'''
if __name__ == '__main__':
	app.secret_key = 'super secret key'
	app.config['SESSION_TYPE'] = 'filesystem'
	app.run(debug=True)
'''