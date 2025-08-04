import os
import json
import csv
from datetime import datetime
from sqlalchemy import create_engine, Table, Column, MetaData, Integer, String, Date, ForeignKey
from sqlalchemy.orm import sessionmaker

# Database connection
engine = create_engine('postgresql://postgres:new_password@localhost/joy_of_painting')
metadata = MetaData()
Session = sessionmaker(bind=engine)
session = Session()

# Reflect tables
episodes = Table('episodes', metadata, autoload_with=engine)
colors = Table('colors', metadata, autoload_with=engine)
subjects = Table('subjects', metadata, autoload_with=engine)
episode_colors = Table('episode_colors', metadata, autoload_with=engine)
episode_subjects = Table('episode_subjects', metadata, autoload_with=engine)

def clean_name(name):
    return name.strip().title()

def process_dataset(file_path, format):
    with open(file_path, 'r') as f:
        if format == 'csv':
            data = list(csv.DictReader(f))
        else:
            raise ValueError("Unsupported format")

        for item in data:
            # Extract episode data
            title = clean_name(item['title'])
            date = datetime.strptime(item['date'], '%Y-%m-%d').date()
            
            # Insert episode
            episode = session.execute(
                episodes.insert().returning(episodes.c.id),
                {'title': title, 'broadcast_date': date}
            ).fetchone()
            episode_id = episode[0]

            # Process colors
            for color_name in item['colors'].split(','):
                color_name = clean_name(color_name)
                color = session.execute(
                    colors.select().where(colors.c.name == color_name)
                ).fetchone()
                if not color:
                    color = session.execute(
                        colors.insert().returning(colors.c.id),
                        {'name': color_name}
                    ).fetchone()
                session.execute(
                    episode_colors.insert(),
                    {'episode_id': episode_id, 'color_id': color[0]}
                )

            # Process subjects
            for subject_name in item['subjects'].split(','):
                subject_name = clean_name(subject_name)
                subject = session.execute(
                    subjects.select().where(subjects.c.name == subject_name)
                ).fetchone()
                if not subject:
                    subject = session.execute(
                        subjects.insert().returning(subjects.c.id),
                        {'name': subject_name}
                    ).fetchone()
                session.execute(
                    episode_subjects.insert(),
                    {'episode_id': episode_id, 'subject_id': subject[0]}
                )
        session.commit()

# Process all datasets
datasets = [
    ('data/dataset1.csv', 'csv'),
    ('data/dataset2.csv', 'csv'),
    ('data/dataset3.csv', 'csv')
]

for path, format in datasets:
    process_dataset(path, format)