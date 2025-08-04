from flask import Flask, request, jsonify
from sqlalchemy import create_engine, func, or_, and_
from sqlalchemy.orm import sessionmaker, aliased
from sqlalchemy.ext.declarative import declarative_base

app = Flask(__name__)
engine = create_engine('postgresql://user:password@localhost/joy_of_painting')
Session = sessionmaker(bind=engine)
Base = declarative_base()

# Define models
class Episode(Base):
    __tablename__ = 'episodes'
    id = Column(Integer, primary_key=True)
    title = Column(String)
    broadcast_date = Column(Date)

class Color(Base):
    __tablename__ = 'colors'
    id = Column(Integer, primary_key=True)
    name = Column(String)

class Subject(Base):
    __tablename__ = 'subjects'
    id = Column(Integer, primary_key=True)
    name = Column(String)

@app.route('/episodes', methods=['GET'])
def get_episodes():
    session = Session()
    try:
        # Get query parameters
        month = request.args.get('month', type=int)
        colors = request.args.getlist('color')
        subjects = request.args.getlist('subject')
        match = request.args.get('match', default='all')

        # Base query
        query = session.query(Episode)

        # Apply filters
        conditions = []
        if month:
            conditions.append(func.extract('month', Episode.broadcast_date) == month)
        if colors:
            color_subq = session.query(Episode.id).join(episode_colors).join(Color)
            color_subq = color_subq.filter(Color.name.in_(colors)).subquery()
            conditions.append(Episode.id.in_(color_subq))
        if subjects:
            subject_subq = session.query(Episode.id).join(episode_subjects).join(Subject)
            subject_subq = subject_subq.filter(Subject.name.in_(subjects)).subquery()
            conditions.append(Episode.id.in_(subject_subq))

        # Combine conditions
        if conditions:
            if match == 'any':
                query = query.filter(or_(*conditions))
            else:
                query = query.filter(and_(*conditions))

        # Execute query
        episodes = query.all()
        return jsonify([{
            'id': e.id,
            'title': e.title,
            'broadcast_date': e.broadcast_date.isoformat()
        } for e in episodes])
    finally:
        session.close()

if __name__ == '__main__':
    app.run(debug=True)