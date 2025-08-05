from flask import Flask, jsonify, request
from sqlalchemy import create_engine, and_, or_, extract, func, Column, Integer, String, Date, Text, Boolean
from sqlalchemy.orm import sessionmaker, declarative_base
import json

app = Flask(__name__)
engine = create_engine('postgresql://johnwilson:new_password@localhost/joy_of_painting')
Session = sessionmaker(bind=engine)
Base = declarative_base()

# Define models
class Episode(Base):
    __tablename__ = 'episodes'
    id = Column(Integer, primary_key=True)
    painting_index = Column(Integer)
    img_src = Column(String)
    painting_title = Column(String)
    season = Column(Integer)
    episode = Column(Integer)
    num_colors = Column(Integer)
    youtube_src = Column(String)
    colors = Column(Text)
    color_hex = Column(Text)
    tags = Column(Text)

class EpisodeAirdate(Base):
    __tablename__ = 'episode_airdates'
    painting_title = Column(String, primary_key=True)
    air_date = Column(Date)
    special_guest = Column(String)

class EpisodeDetail(Base):
    __tablename__ = 'episode_details'
    episode_id = Column(Integer, primary_key=True)
    season = Column(Integer)
    episode = Column(Integer)
    title = Column(String)
    apple_frame = Column(Boolean)
    aurora_borealis = Column(Boolean)
    barn = Column(Boolean)
    beach = Column(Boolean)
    boat = Column(Boolean)
    bridge = Column(Boolean)
    building = Column(Boolean)
    bushes = Column(Boolean)
    cabin = Column(Boolean)
    cactus = Column(Boolean)
    circle_frame = Column(Boolean)
    cirrus = Column(Boolean)
    cliff = Column(Boolean)
    clouds = Column(Boolean)
    conifer = Column(Boolean)
    cumulus = Column(Boolean)
    deciduous = Column(Boolean)
    diane_andre = Column(Boolean)
    dock = Column(Boolean)
    double_oval_frame = Column(Boolean)
    farm = Column(Boolean)
    fence = Column(Boolean)
    fire = Column(Boolean)
    florida_frame = Column(Boolean)
    flowers = Column(Boolean)
    fog = Column(Boolean)
    framed = Column(Boolean)
    grass = Column(Boolean)
    guest = Column(Boolean)
    half_circle_frame = Column(Boolean)
    half_oval_frame = Column(Boolean)
    hills = Column(Boolean)
    lake = Column(Boolean)
    lakes = Column(Boolean)
    lighthouse = Column(Boolean)
    mill = Column(Boolean)
    moon = Column(Boolean)
    mountain = Column(Boolean)
    mountains = Column(Boolean)
    night = Column(Boolean)
    ocean = Column(Boolean)
    oval_frame = Column(Boolean)
    palm_trees = Column(Boolean)
    path = Column(Boolean)
    person = Column(Boolean)
    portrait = Column(Boolean)
    rectangle_3d_frame = Column(Boolean)
    rectangular_frame = Column(Boolean)
    river = Column(Boolean)
    rocks = Column(Boolean)
    seashell_frame = Column(Boolean)
    snow = Column(Boolean)
    snowy_mountain = Column(Boolean)
    split_frame = Column(Boolean)
    steve_ross = Column(Boolean)
    structure = Column(Boolean)
    sun = Column(Boolean)
    tomb_frame = Column(Boolean)
    tree = Column(Boolean)
    trees = Column(Boolean)
    triple_frame = Column(Boolean)
    waterfall = Column(Boolean)
    waves = Column(Boolean)
    windmill = Column(Boolean)
    window_frame = Column(Boolean)
    winter = Column(Boolean)
    wood_framed = Column(Boolean)

@app.route('/episodes/filter', methods=['GET'])
def filter_episodes():
    session = Session()
    try:
        # Get query parameters
        months = [int(m) for m in request.args.getlist('month')] if 'month' in request.args else []
        subjects = request.args.getlist('subject')
        colors = request.args.getlist('color')
        match = request.args.get('match', 'all')  # 'all' or 'any'
        
        # Base query
        query = session.query(
            Episode.id,
            Episode.painting_title,
            Episode.season,
            Episode.episode,
            EpisodeAirdate.air_date,
            Episode.youtube_src,
            Episode.colors
        ).join(
            EpisodeAirdate, Episode.painting_title == EpisodeAirdate.painting_title
        )
        
        # Join episode_details for subject filtering
        if subjects:
            query = query.join(EpisodeDetail, Episode.id == EpisodeDetail.episode_id)
        
        # Build filter conditions
        conditions = []
        
        # Month filter (extract month from air_date)
        if months:
            month_conditions = [extract('month', EpisodeAirdate.air_date) == m for m in months]
            conditions.append(or_(*month_conditions))
        
        # Subject filter (check boolean columns)
        if subjects:
            subject_conditions = [getattr(EpisodeDetail, subject).is_(True) for subject in subjects]
            conditions.append(or_(*subject_conditions))
        
        # Color filter (check if color appears in colors string)
        if colors:
            color_conditions = [func.lower(Episode.colors).contains(func.lower(color)) for color in colors]
            conditions.append(or_(*color_conditions))
        
        # Apply filters based on match type
        if conditions:
            if match == 'all':
                for condition in conditions:
                    query = query.filter(condition)
            else:  # 'any'
                query = query.filter(or_(*conditions))
        
        # Execute query
        results = query.distinct().all()
        
        # Format results
        episodes = []
        for row in results:
            # Convert colors string to list
            try:
                colors_list = json.loads(row.colors.replace("'", '"'))
            except json.JSONDecodeError:
                colors_list = []
            
            episodes.append({
                'id': row.id,
                'title': row.painting_title,
                'season': row.season,
                'episode': row.episode,
                'air_date': row.air_date.isoformat() if row.air_date else None,
                'youtube_src': row.youtube_src,
                'colors': colors_list
            })
        
        return jsonify(episodes)
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        session.close()

if __name__ == '__main__':
    app.run(debug=True)