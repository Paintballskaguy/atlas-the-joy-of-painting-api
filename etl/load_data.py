import csv
from datetime import datetime
from sqlalchemy import create_engine, Table, Column, MetaData, Integer, String, Date, Text, Boolean
from sqlalchemy.orm import sessionmaker
from sqlalchemy.dialects.postgresql import insert

# Database connection
engine = create_engine('postgresql://johnwilson:new_password@localhost/joy_of_painting')
metadata = MetaData()
Session = sessionmaker(bind=engine)
session = Session()

# Define tables to match your CSV structure
episodes = Table('episodes', metadata,
    Column('id', Integer, primary_key=True),
    Column('painting_index', Integer),
    Column('img_src', String(255)),
    Column('painting_title', String(255)),
    Column('season', Integer),
    Column('episode', Integer),
    Column('num_colors', Integer),
    Column('youtube_src', String(255)),
    Column('colors', Text),
    Column('color_hex', Text),
    Column('tags', Text)
)

episode_details = Table('episode_details', metadata,
    Column('episode_id', Integer, primary_key=True),
    Column('season', Integer),
    Column('episode', Integer),
    Column('title', String(255)),
    # Include all boolean columns from dataset2.csv
    Column('apple_frame', Boolean),
    Column('aurora_borealis', Boolean),
    Column('barn', Boolean),
    Column('beach', Boolean),
    Column('boat', Boolean),
    Column('bridge', Boolean),
    Column('building', Boolean),
    Column('bushes', Boolean),
    Column('cabin', Boolean),
    Column('cactus', Boolean),
    Column('circle_frame', Boolean),
    Column('cirrus', Boolean),
    Column('cliff', Boolean),
    Column('clouds', Boolean),
    Column('conifer', Boolean),
    Column('cumulus', Boolean),
    Column('deciduous', Boolean),
    Column('diane_andre', Boolean),
    Column('dock', Boolean),
    Column('double_oval_frame', Boolean),
    Column('farm', Boolean),
    Column('fence', Boolean),
    Column('fire', Boolean),
    Column('florida_frame', Boolean),
    Column('flowers', Boolean),
    Column('fog', Boolean),
    Column('framed', Boolean),
    Column('grass', Boolean),
    Column('guest', Boolean),
    Column('half_circle_frame', Boolean),
    Column('half_oval_frame', Boolean),
    Column('hills', Boolean),
    Column('lake', Boolean),
    Column('lakes', Boolean),
    Column('lighthouse', Boolean),
    Column('mill', Boolean),
    Column('moon', Boolean),
    Column('mountain', Boolean),
    Column('mountains', Boolean),
    Column('night', Boolean),
    Column('ocean', Boolean),
    Column('oval_frame', Boolean),
    Column('palm_trees', Boolean),
    Column('path', Boolean),
    Column('person', Boolean),
    Column('portrait', Boolean),
    Column('rectangle_3d_frame', Boolean),
    Column('rectangular_frame', Boolean),
    Column('river', Boolean),
    Column('rocks', Boolean),
    Column('seashell_frame', Boolean),
    Column('snow', Boolean),
    Column('snowy_mountain', Boolean),
    Column('split_frame', Boolean),
    Column('steve_ross', Boolean),
    Column('structure', Boolean),
    Column('sun', Boolean),
    Column('tomb_frame', Boolean),
    Column('tree', Boolean),
    Column('trees', Boolean),
    Column('triple_frame', Boolean),
    Column('waterfall', Boolean),
    Column('waves', Boolean),
    Column('windmill', Boolean),
    Column('window_frame', Boolean),
    Column('winter', Boolean),
    Column('wood_framed', Boolean)
)

episode_airdates = Table('episode_airdates', metadata,
    Column('painting_title', String(255), primary_key=True),
    Column('air_date', Date),
    Column('special_guest', String(255))
)

def load_datasets():
    try:
        # Clear all data
        session.execute(episode_airdates.delete())
        session.execute(episode_details.delete())
        session.execute(episodes.delete())
        session.commit()

        # Load dataset3 (air dates)
        with open('../data/dataset3.csv', 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                air_date = datetime.strptime(row['Air Date'], '%B %d, %Y').date()
                stmt = insert(episode_airdates).values(
                    painting_title=row['painting_title'],
                    air_date=air_date,
                    special_guest=row.get('Special_Guest') or None
                ).on_conflict_do_update(
                    index_elements=['painting_title'],
                    set_={
                        'air_date': air_date,
                        'special_guest': row.get('Special_Guest') or None
                    }
                )
                session.execute(stmt)

        # Load dataset1 (episodes)
        with open('../data/dataset1.csv', 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                stmt = insert(episodes).values(
                    id=int(row['id']),
                    painting_index=int(row['painting_index']),
                    img_src=row['img_src'],
                    painting_title=row['painting_title'],
                    season=int(row['season']),
                    episode=int(row['episode']),
                    num_colors=int(row['num_colors']),
                    youtube_src=row['youtube_src'],
                    colors=row['colors'],
                    color_hex=row['color_hex'],
                    tags=row['tags']
                ).on_conflict_do_update(
                    index_elements=['id'],
                    set_={
                        'painting_title': row['painting_title'],
                        'season': int(row['season']),
                        'episode': int(row['episode']),
                        'num_colors': int(row['num_colors']),
                        'colors': row['colors'],
                        'tags': row['tags']
                    }
                )
                session.execute(stmt)

        # Load dataset2 (details)
        with open('../data/dataset2.csv', 'r') as f:
            reader = csv.DictReader(f)
            boolean_columns = [col for col in reader.fieldnames if col not in ['id', 'season', 'episode', 'title']]
            
            for row in reader:
                values = {
                    'episode_id': int(row['id']),
                    'season': int(row['season']),
                    'episode': int(row['episode']),
                    'title': row['title']
                }
                # Add all boolean columns
                for col in boolean_columns:
                    values[col] = bool(int(row[col]))
                
                stmt = insert(episode_details).values(
                    **values
                ).on_conflict_do_update(
                    index_elements=['episode_id'],
                    set_=values
                )
                session.execute(stmt)

        session.commit()
        print("Data loaded successfully!")
    except Exception as e:
        session.rollback()
        print(f"Error loading data: {str(e)}")
        raise
    finally:
        session.close()

if __name__ == '__main__':
    load_datasets()