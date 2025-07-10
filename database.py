import pandas as pd
from sqlalchemy import create_engine
import re

# Fix file path (use raw string to avoid escape issues)
df = pd.read_csv(r"C:\Users\prati\OneDrive\Desktop\project1\imdb_2024_movies.csv")

#  Convert Vote Count
def convert_vote_count(vote_str):
    try:
        vote_str = str(vote_str).strip().upper()
        if 'K' in vote_str:
            return float(vote_str.replace('K', '')) * 1000
        else:
            return float(vote_str)
    except:
        return None

df['Vote Count'] = df['Vote Count'].apply(convert_vote_count)

#  Convert Duration
def duration_to_minutes(duration):
    match = re.match(r'(?:(\d+)h)?\s*(?:(\d+)m)?', str(duration))
    if not match:
        return None
    hours = int(match.group(1)) if match.group(1) else 0
    minutes = int(match.group(2)) if match.group(2) else 0
    return hours * 60 + minutes

df['Duration'] = df['Duration'].apply(duration_to_minutes)

#  Save to SQLite DB
engine = create_engine("sqlite:///./imdb.db", echo=True)
df.to_sql("imdb_movies_2024", con=engine, if_exists="replace", index=False)

print(" DB created and table loaded successfully!")





