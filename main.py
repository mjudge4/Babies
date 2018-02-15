from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask import make_response
import requests, json
import os
import MySQLdb

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Offering, Tag, Comment

# These environment variables are configured in app.yaml.
CLOUDSQL_CONNECTION_NAME = os.environ.get('pycharm-194111:europe-west2:babiesgrowdatabase')
CLOUDSQL_USER = os.environ.get('root')
CLOUDSQL_PASSWORD = os.environ.get('OLkkD03xAb31IIv1')



app = Flask(__name__)

engine = create_engine('sqlite:///offerings.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


app = Flask(__name__)


def connect_to_cloudsql():
    # When deployed to App Engine, the `SERVER_SOFTWARE` environment variable
    # will be set to 'Google App Engine/version'.
    if os.getenv('SERVER_SOFTWARE', '').startswith('Google App Engine/'):
        # Connect using the unix socket located at
        # /cloudsql/cloudsql-connection-name.
        cloudsql_unix_socket = os.path.join(
            '/cloudsql', pycharm-194111:europe-west2:babiesgrowdatabase)

        db = MySQLdb.connect(
            unix_socket=cloudsql_unix_socket,
            user=root,
            passwd=OLkkD03xAb31IIv1)

    # If the unix socket is unavailable, then try to connect using TCP. This
    # will work if you're running a local MySQL server or using the Cloud SQL
    # proxy, for example:
    #
    #   $ cloud_sql_proxy -instances=your-connection-name=tcp:3306
    #
    else:
        db = MySQLdb.connect(
            host='127.0.0.1', user=root, passwd=OLkkD03xAb31IIv1)

    return db

# @reference http://https://classroom.udacity.com/courses/ud330/lessons/3967218625/concepts/39636486150923

# Create anti-forgery state token


@app.route('/')
@app.route('/offerings/')
def offering():
    offerings = session.query(Offering).all()

    return render_template('offerings.html', offerings=offerings)

@app.route('/offerings/JSON')
def offeringJSON():
    offerings = session.query(Offering).all()
    return jsonify(offerings=[i.serialize for i in offerings])



@app.route('/offerings/<int:offering_id>/')
def offeringDetail(offering_id):
    offering = session.query(Offering).filter_by(id=offering_id).one()
    tags = session.query(Tag).filter_by(offering_id=offering_id).all()
    comments = session.query(Comment).filter_by(offering_id=offering_id).all()
    return render_template('offeringDetail.html', offering=offering, tags=tags,
                           comments=comments, offering_id=offering_id)



@app.route('/offerings/<int:offering_id>/JSON')
def offeringDetailJSON(offering_id):
    offering = session.query(Offering).filter_by(id=offering_id).one()
    tags = session.query(Tag).filter_by(offering_id=offering_id).all()
    comments = session.query(Comment).filter_by(offering_id=offering_id).all()
    return jsonify(offering=offering.serialize, Tags=[i.serialize for i in tags], Comment=[j.serialize for j in comments])


@app.route('/offerings/new/', methods=['GET', 'POST'])
def newOffering():
    if request.method == 'POST':
        newOffering = Offering(title=request.form['title'], date=request.form['date'])
        session.add(newOffering)
        session.commit()
        flash("New Offering added")
        return redirect(url_for('offering'))
    else:
        return render_template('newoffering.html')

@app.route('/offerings/<int:offering_id>/edit/', methods=['GET', 'POST'])
def editOffering(offering_id):
    editedOffering = session.query(Offering).filter_by(id=offering_id).one()
    if request.method == 'POST':
        if request.form['title']:
            editedOffering.title = request.form['title']
            flash("Offering updated")
            return redirect(url_for('offering'))
    else:
        return render_template('editoffering.html', offering=editedOffering)

@app.route('/offerings/<int:offering_id>/delete/', methods=['GET', 'POST'])
def deleteOffering(offering_id):
    offeringToDelete = session.query(Offering).filter_by(id=offering_id).one()
    if request.method == 'POST':
        session.delete(offeringToDelete)
        session.commit()
        flash("Offering deleted")
        return redirect(url_for('offering', offering_id=offering_id))
    else:
        return render_template('deleteoffering.html', offering = offeringToDelete)


if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
