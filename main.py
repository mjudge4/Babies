from flask import Flask, render_template, flash, request

from oauth2client.client import flow_from_clientsecrets, FlowExchangeError
import httplib2
import json
from flask import make_response
import requests

from flask import session as login_session
import random
import string

CLIENT_ID = json.loads(open('client_secrets.json', 'r').read())['web']['client_id']

app = Flask(__name__)

# @reference http://https://classroom.udacity.com/courses/ud330/lessons/3967218625/concepts/39636486150923

# Create anti-forgery state token
@app.route('/login')
def showLogin():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits) for x in xrange(32))
    login_session['state'] = state
    #Render Login Template return "The current session state is %s" % login_session['state']
    return render_template('login.html', STATE=state)


# Validate the state token
@app.route('/gconnect', methods=['POST'])
def gconnect():
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Acquire authorisation code
    code = request.data


    try:
        # Upgrade auth code into a credentials object
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(json.dumps('Failed to upgrade the authorisation code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response


    # Check token is valid
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s' % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])

    # Abort if there was an error in access token info
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Confirm access token is for the correct user
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(json.dumps("User ID does not match Token ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Confirm the access token is correct for this app
    if result['issued_to'] != CLIENT_ID:
        response = make_response(json.dumps("Token ID does not match to application"), 401)
        print "Token ID does not match to application"
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check to see if the user is already logged in
    stored_access_token = login_session.get('access_token')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_access_token is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps('User is already logged in'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store access token in the session
    login_session['access_token'] = credentials.access_token
    login_session['gplus_id'] = gplus_id

    # Get the user's info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)
    data = answer.json()

    # Store user data to  create a response
    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 300px; height: 300px;border-radius: 150px;-webkit-border-radius: 150px;-moz-border-radius: 150px;"> '
    flash("you are now logged in as %s" % login_session['username'])
    print "done!"
    return output

# Disconnect by revoking user's access token

@app.route('/gdisconnect')
def gdisconnect():
    # Only disconnect connected user
    access_token = login_session.get('access_token')

    if access_token is None:
        response = make_response(json.dumps('Current User is not connected'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Enact HTTP GET request to revoke current token
    
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % login_session['access_token']
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]

    if result['status'] == '200':
        # Reset the user session
        del login_session['access_token']
        del login_session['gplus_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']

        response = make_response(json.dumps('User disconnected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    else:
        # If for some reason the token is invalid
        response = make_response(json.dumps('Token revoke for current user failed'), 400)
        response.headers['Content-Type'] = 'application/json'
        return response

@app.route('/')
@app.route('/hello')
def hello_world():
    return 'Hello World!'

if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
