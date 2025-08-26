import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import re

st.set_page_config(layout="wide")

df = pd.read_csv("D:\project\project1\imdb_2024_movies.csv")

def convert_vote_count(vote_str):
    try:
        vote_str = str(vote_str).strip().upper()
        if 'K' in vote_str:
            return float(vote_str.replace('K', '')) * 1000
        else:
            return float(vote_str)
    except:
        return None

def duration_to_minutes(duration):
    match = re.match(r'(?:(\d+)h)?\s*(?:(\d+)m)?', str(duration))
    if not match:
        return None
    hours = int(match.group(1)) if match.group(1) else 0
    minutes = int(match.group(2)) if match.group(2) else 0
    return hours * 60 + minutes

def clean_genres(g):
    if isinstance(g, list):
        return g
    elif isinstance(g, str):
        return [i.strip() for i in g.split(",")]
    else:
        return []


df['Vote Count'] = df['Vote Count'].apply(convert_vote_count)
df['Duration'] = df['Duration'].apply(duration_to_minutes)
df['Genre'] = df['Genre'].apply(clean_genres)
df = df.explode("Genre")
df = df[df['Genre'].notnull() & (df['Genre'] != "")]

st.sidebar.header(" Filter Options")

selected_genre = st.sidebar.multiselect("Select Genre(s):", sorted(df['Genre'].unique()))
selected_rating = st.sidebar.slider("Minimum IMDb Rating:", 0.0, 10.0, 0.0, 0.1)
selected_votes = st.sidebar.number_input("Minimum Vote Count:", value=0, step=1000)
selected_duration = st.sidebar.selectbox("Duration Range:", ["All", "< 120 min", "120 - 180 min", "> 180 min"])

filtered_df = df.copy()

if selected_genre:
    filtered_df = filtered_df[filtered_df['Genre'].isin(selected_genre)]

filtered_df = filtered_df[filtered_df['IMDb Rating'] >= selected_rating]
filtered_df = filtered_df[filtered_df['Vote Count'] >= selected_votes]

if selected_duration == "< 120 min":
    filtered_df = filtered_df[filtered_df['Duration'] < 120]
elif selected_duration == "120 - 180 min":
    filtered_df = filtered_df[(filtered_df['Duration'] >= 120) & (filtered_df['Duration'] <= 180)]
elif selected_duration == "> 180 min":
    filtered_df = filtered_df[filtered_df['Duration'] > 180]

st.title(" IMDb 2024 Movies Dashboard")

# 1. Top 10 Movies
st.subheader("Top 10 Movies by Rating & Votes")
top_movies = filtered_df.sort_values(by=['IMDb Rating', 'Vote Count'], ascending=[False, False]).head(10)
st.dataframe(top_movies[['Movie Name', 'Genre', 'IMDb Rating', 'Vote Count', 'Duration']])

# 2. Genre Distribution
st.subheader(" Genre Distribution")
genre_counts = filtered_df['Genre'].value_counts()
fig, ax = plt.subplots()
sns.barplot(x=genre_counts.values, y=genre_counts.index, palette='Set2', ax=ax)
ax.set_xlabel("Number of Movies")
ax.set_ylabel("Genre")
st.pyplot(fig)

# 3. Average Duration by Genre
st.subheader("Average Duration by Genre")
avg_duration = filtered_df.groupby("Genre")["Duration"].mean().sort_values()
fig, ax = plt.subplots()
sns.barplot(x=avg_duration.values, y=avg_duration.index, palette="coolwarm", ax=ax)
ax.set_xlabel("Average Duration (mins)")
st.pyplot(fig)

# 4. Voting Trends by Genre
st.subheader("Average Vote Count by Genre")
avg_votes = filtered_df.groupby("Genre")["Vote Count"].mean().sort_values(ascending=False)
fig, ax = plt.subplots()
sns.barplot(x=avg_votes.values, y=avg_votes.index, ax=ax, palette="magma")
ax.set_xlabel("Avg. Vote Count")
st.pyplot(fig)

# 5. Rating Distribution
st.subheader(" Rating Distribution")
fig, ax = plt.subplots()
sns.histplot(filtered_df['IMDb Rating'], kde=True, bins=15, color='skyblue', ax=ax)
ax.set_xlabel("IMDb Rating")
ax.set_ylabel("Frequency")
st.pyplot(fig)

# 6. Genre-Based Rating Leaders
st.subheader("Top-Rated Movie per Genre")
top_genre_movies = filtered_df.sort_values("IMDb Rating", ascending=False).drop_duplicates("Genre")
st.dataframe(top_genre_movies[['Genre', 'Movie Name', 'IMDb Rating']])

# 7. Most Popular Genres by Total Votes
st.subheader("Most Popular Genres by Total Votes")
total_votes = filtered_df.groupby("Genre")["Vote Count"].sum()
fig, ax = plt.subplots()
ax.pie(total_votes, labels=total_votes.index, autopct='%1.1f%%', startangle=140)
ax.axis('equal')
st.pyplot(fig)

# 8. Duration Extremes
st.subheader(" Duration Extremes")
shortest = filtered_df.sort_values("Duration").head(1)
longest = filtered_df.sort_values("Duration").tail(1)
st.markdown(f"**Shortest Movie:** {shortest.iloc[0]['Movie Name']} ({shortest.iloc[0]['Duration']} mins)")
st.markdown(f"**Longest Movie:** {longest.iloc[0]['Movie Name']} ({longest.iloc[0]['Duration']} mins)")

# 9. Ratings by Genre (Heatmap)
st.subheader("Heatmap of Avg Ratings by Genre")
heatmap_data = filtered_df.groupby("Genre")["IMDb Rating"].mean().to_frame()
fig, ax = plt.subplots()
sns.heatmap(heatmap_data, annot=True, cmap="YlGnBu", ax=ax)
st.pyplot(fig)

# 10. Correlation: Rating vs Votes
st.subheader("Correlation: Rating vs Vote Count")
fig, ax = plt.subplots()
sns.scatterplot(data=filtered_df, x="Vote Count", y="IMDb Rating", hue="Genre", ax=ax)
ax.set_xscale('log')
st.pyplot(fig)


st.subheader("Filtered Movies Table")
st.dataframe(filtered_df.reset_index(drop=True))