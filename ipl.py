import requests
from bs4 import BeautifulSoup
import pandas as pd

# Step 1: Define the URL
url = "http://www.imdb.com/search/title?sort=num_votes,desc&start=1&title_type=feature&year=1950,2012"

# Step 2: Send a GET request to the URL
response = requests.get(url)
if response.status_code != 200:
    print(f"Failed to retrieve the webpage. Status code: {response.status_code}")
    exit()

# Step 3: Parse the webpage content
soup = BeautifulSoup(response.content, "html.parser")

# Step 4: Extract relevant data
movies = []
table = soup.find("tbody", class_="lister-list")  # Locate the table containing the movie list

for row in table.find_all("tr"):
    # Extract title
    title_column = row.find("td", class_="titleColumn")
    title = title_column.a.text.strip()
    
    # Extract year
    year = title_column.span.text.strip("()")
    
    # Extract rating
    rating = row.find("td", class_="ratingColumn imdbRating").strong.text.strip()
    
    # Append to movies list
    movies.append({"Title": title, "Year": year, "Rating": rating})

# Step 5: Save the data to a DataFrame
df = pd.DataFrame(movies)

# Step 6: Export to CSV (optional)
df.to_csv("IMDb_Top_250_Movies.csv", index=False)

# Step 7: Display results
print(df.head())