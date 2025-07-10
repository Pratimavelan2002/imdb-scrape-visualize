# IMDb 2024 Movies Analysis & Visualization

This project focuses on **data extraction**, **transformation**, and **interactive visualization** of IMDb movie data from 2024. It involves scraping IMDb using **Selenium**, cleaning and storing data using **Pandas & SQLite**, and presenting it interactively using **Streamlit**.

#  Project Overview

# 1. Web Scraping (Selenium)

* The `selenium.ipynb` notebook scrapes movie data from IMDb for 2024.
* Extracted attributes include: `Movie Name`, `IMDb Rating`, `Genre`, `Duration`, and `Vote Count`.
* Data is saved into a CSV file (`imdb_2024_movies.csv`).

# 2. Data Cleaning & Database Loading

* `database.py` cleans the CSV data:

  * Converts vote counts like "12K" into numbers (e.g., 12000).
  * Transforms duration from "2h 10m" to minutes.
* Then stores the cleaned dataset into an **SQLite database** (`imdb.db`) under the table `imdb_movies_2024`.

# 3. Interactive Dashboard (Streamlit)

* `visualization.py` creates a **Streamlit dashboard** with various visual insights:

  * Top 10 Movies by Rating & Votes
  * Genre Distribution
  * Average Duration by Genre
  * Voting Trends by Genre
  * IMDb Rating Distribution
  * Top-Rated Movies per Genre
  * Popular Genres by Total Votes
  * Duration Extremes (Shortest & Longest)
  * Heatmap of Ratings
  * Correlation: Rating vs Vote Count
    
## requirements
* pandas
* sqlalchemy
* streamlit
* matplotlib
* seaborn
* re
* selenium
* notebook
  
## Tech Stack
* **Python**
* **Selenium** – for web scraping
* **Pandas & Regex** – for data transformation
* **SQLite (SQLAlchemy)** – for database storage
* **Streamlit, Seaborn, Matplotlib** – for data visualization

## How to Run

1. Clone the repo:

   ```bash
   git clone https://github.com/yourusername/imdb-2024-analysis.git
   cd imdb-2024-analysis
   ```

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Run data extraction (optional):

   * Open and run `selenium.ipynb` to scrape IMDb and generate the CSV file.

4. Load data into database:

   ```bash
   python database.py
   ```

5. Launch dashboard:

   ```bash
   streamlit run visualization.py
   ```

## Files

| File                   | Description                |
| ---------------------- | -------------------------- |
| `selenium.ipynb`       | Web scraping script        |
| `imdb_2024_movies.csv` | Raw scraped data           |
| `database.py`          | Data cleaning & DB storage |
| `imdb.db`              | SQLite database            |
| `visualization.py`     | Streamlit dashboard        |
| `requirements.txt`     | Required Python packages   |


## Sample Visuals

*(You can add screenshots here once the dashboard is live)*

## Author

* **Pratima Velan**
* 📍 Based in Coimbatore
* Passionate about data science, visualization, and automation
