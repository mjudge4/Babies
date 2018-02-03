from flask import Flask

from flask import session as login_session
import random
import string

app = Flask(__name__)

# @reference http://https://classroom.udacity.com/courses/ud330/lessons/3967218625/concepts/39636486150923
#Create a state token for forgery prevention and store in session for later validation
@app.route('/login')
def showLogin():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits) for x in xrange(32))
    login_session['state'] = state
    return "The current session state is %s" % login_session['state']

@app.route('/')
def hello_world():
    return 'Hello World!'

if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
