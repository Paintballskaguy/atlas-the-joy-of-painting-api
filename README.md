# The Joy of Painting API 🎨
﻿<a href="https://imgflip.com/i/8ypabe](https://d7hftxdivxxvm.cloudfront.net/?height=1440&quality=80&resize_to=fit&src=https%3A%2F%2Fartsy-media-uploads.s3.amazonaws.com%2FxsvTijg8O01pLjzquMcfqA%252FBob%2BRoss-2.jpg&width=1440)"><img src="https://d7hftxdivxxvm.cloudfront.net/?height=1440&quality=80&resize_to=fit&src=https%3A%2F%2Fartsy-media-uploads.s3.amazonaws.com%2FxsvTijg8O01pLjzquMcfqA%252FBob%2BRoss-2.jpg&width=1440" title="made at imgflip.com"/></a><div></a></div>
A comprehensive API for exploring Bob Ross's iconic painting episodes with advanced filtering capabilities

## About the Developer
John Wilson

Systems Architect → Full-Stack Engineer

With 6+ years building HIPAA-compliant infrastructure in healthcare/energy sectors, I now craft developer tools that blend system-level efficiency with intuitive UX. Passionate about creating terminal experiences that reduce cognitive load through thoughtful design.

## Project Description
The Joy of Painting API provides a comprehensive database and query interface for all 403 episodes of Bob Ross's iconic painting instructional series. This API allows users to filter episodes based on multiple criteria including broadcast month, subject matter, and color palette, with flexible matching options to create personalized viewing experiences.

Unlike simple media databases, this project involved complex data integration from multiple disparate sources, sophisticated ETL processes, and a thoughtfully designed API that handles complex filtering logic while maintaining performance and usability.

## Development Story
### The Challenge
The project began with three distinct datasets collected by different individuals, each with unique storage formats and inconsistencies. The primary challenge was transforming this heterogeneous data into a coherent, queryable database that could power a filtering system for public broadcasting station viewers.

### Data Integration Journey
The most intricate part of the project was designing an ETL pipeline that could:

- Handle CSV files with different schemas and formats

- Resolve data inconsistencies and duplicates

- Establish proper relational connections between datasets

- Transform date formats and boolean values consistently

I implemented a multi-phase approach:

- Database Design: Created a normalized schema with proper relationships

- ETL Development: Built custom Python scripts with SQLAlchemy for data loading

- API Construction: Developed a Flask-based API with complex filtering capabilities

### Technical Breakthroughs
The most satisfying moment came when solving the complex filtering requirements. Implementing the "match any" vs "match all" logic required careful query construction to handle multiple filter combinations while maintaining performance across 403 episodes with numerous attributes.

## Features
Implemented
Multi-source Data Integration: Combined three different dataset formats into a unified database

### Advanced Filtering System:

- Filter by broadcast month (1-12)

- Filter by subject matter (65+ categories including mountains, lakes, cabins, etc.)

- Filter by color palette (18 different paint colors)

- Combined filters with "match all" or "match any" logic

- RESTful API: Clean JSON responses with episode metadata

- Data Validation: Comprehensive error handling and data type conversion

- Performance Optimization: Efficient database queries with proper indexing

### API Endpoints
- GET /episodes/filter?month=1&subject=mountain&color=blue&match=all

Returns filtered episodes in JSON format with complete metadata

### To Be Implemented
- User authentication and personalized episode collections

- Advanced search with partial string matching

- Pagination for large result sets

- Rate limiting and API usage analytics

- Caching layer for improved performance

- Web interface for visual exploration of episodes

### Technical Challenges
Data Heterogeneity
The three source datasets had completely different structures:

Dataset 1: Episode metadata with colors and tags

Dataset 2: Boolean features for subject matter (65+ columns)

Dataset 3: Air dates with special guest information

Integrating these required careful schema design and complex ETL logic.

### Database Design Complexity
Creating a schema that maintained relationships while enabling efficient filtering was challenging. The final design uses:

- A main episodes table with core metadata

- An episode_details table with boolean subject columns

- An episode_airdates table with broadcast information

### Filter Implementation
The most complex technical challenge was implementing the filtering system that allows:

- Multiple values for each filter type (e.g., multiple colors)

- Different matching strategies ("all" vs "any")

- Efficient database queries that join multiple tables

The solution uses SQLAlchemy's expression language to dynamically construct queries based on filter parameters.

### Date Format Inconsistencies
The original data stored dates in different formats ("January 11, 1983" vs "1983-01-11"). The ETL process needed to detect and normalize these formats before database insertion.

## Technical Stack
Backend: Python, Flask, SQLAlchemy

Database: PostgreSQL with optimized schema design

Data Processing: Custom ETL scripts with pandas-like functionality

API Design: RESTful principles with JSON responses

### Installation & Usage
```
bash
Clone the repository
git clone https://github.com/johnwilson/atlas-the-joy-of-painting-api.git
```

### Set up database
```
createdb joy_of_painting
psql -U your_username -d joy_of_painting -f database/create_tables.sql
```

### Run ETL process
```
cd etl
python3 load_data.py
```

### Start API server
```
cd ../api
python3 app.py
Example Queries
bash
# Get episodes aired in January
curl "http://localhost:5000/episodes/filter?month=1"
```

### Get episodes featuring mountains and lakes
```
curl "http://localhost:5000/episodes/filter?subject=mountain&subject=lake&match=all"
```

### Get episodes using blue or green paints
```
curl "http://localhost:5000/episodes/filter?color=blue&color=green&match=any"
```

# Complex combination (episodes from January featuring mountains OR using red paint)
```
curl "http://localhost:5000/episodes/filter?month=1&subject=mountain&color=red&match=any"
```
### Future Enhancements
This project lays the foundation for several interesting expansions:

Machine learning recommendations based on painting preferences

Social features for sharing curated episode collections

Integration with streaming services for direct episode access

Visual analysis of color palette trends across seasons

Mobile application with personalized viewing schedules

This project was developed as part of the Atlas School curriculum, demonstrating full-stack development skills from database design to API implementation.
