import os
import requests


from flask import Flask, session, jsonify, render_template, request, redirect

from flask import url_for

from flask_session import Session

from flask_socketio import SocketIO, emit




app = Flask(__name__)

app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")




# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"

Session(app)

socketio = SocketIO(app)

votes = {"yes": 0, "no": 0, "maybe": 0}



@app.route("/" , methods=["POST","GET"])
def index():

	# Get Username for session
	user_logged = ""


	try:

		user_logged = session['username']
		user_logged_value = 1

	except :

		user_logged = "No User Logged in"
		user_logged_value = 0


	# If method is POST 
	if request.method == "GET" and user_logged_value == 1: 

		
		# Render template search.html and return books query result
		return render_template("index.html", user_logged = user_logged , votes=votes)



	elif request.method == "GET" and user_logged_value == 0:


		error_log = "Please Log in here"


		return render_template("login.html" , error_log = error_log )




@socketio.on("submit vote")

def vote(data):

    selection = data["selection"]

    votes[selection] += 1

    emit("vote totals", votes, broadcast=True)



   

# User Authentication

@app.route("/loguser", methods = ["POST"])

def loguser():

	

	if request.method == "POST":


		# Get username and user password from form after is Posted 
		name = request.form.get("username")

		password = request.form.get("userpassword")

		

	    # If the usernamane and password are correct

	    

	    #if name is not None and password is not None: 

		existence = 1

		
		# if the statement is True redirect to index
		if existence == 1: 

			# Store UserName 
			session['username'] = name

			return redirect (url_for("index"))

			

		else:

			# Return a message if the username or password is incorrect
			error_log = "The username or password is incorrect"

			return render_template("login.html" , error_log = error_log )



# User Login Route/Function

@app.route("/login" )
def login():

	error_log = "Please Log in here"

	session.pop('username', None)

	# render template login.html
	return render_template("login.html" ,error_log = error_log)



# User Log out Route/Function

@app.route("/logout")

def logout():

   # Remove the username from the session if it is there one
   session.pop('username', None)

   # Use redirect 
   return redirect(url_for("index"))