from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask import make_response
import requests, json

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Offering, Tag, Comment

app = Flask(__name__)

engine = create_engine('sqlite:///offerings.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


app = Flask(__name__)

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
