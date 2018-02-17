from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Base, Offering, Tag, Comment

engine = create_engine('mysql://root:password@localhost/mydatabase')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
session = DBSession()

offering1 = Offering(title="Godchild", date="October")

session.add(offering1)
session.commit()

tag1 = Tag(tag_name="Babygrow", offering=offering1)
session.add(tag1)
session.commit()

tag2 = Tag(tag_name="Novelty", offering=offering1)
session.add(tag2)
session.commit()

comment1 = Comment(body="That looks great", offering=offering1)
session.add(comment1)
session.commit()

offering2 = Offering(title="BabyTed", date="November")

session.add(offering2)
session.commit()

tag1 = Tag(tag_name="Babygrow", offering=offering2)
session.add(tag1)
session.commit()

tag2 = Tag(tag_name="Novelty", offering=offering2)
session.add(tag2)
session.commit()

comment2 = Comment(body="Cool", offering=offering2)
session.add(comment2)
session.commit()

print "Offerings added"