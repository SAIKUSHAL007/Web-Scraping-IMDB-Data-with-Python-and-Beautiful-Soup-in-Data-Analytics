import requests
from bs4 import BeautifulSoup
import pandas as pd
url = "http://www.imdb.com/search/title?sort=num_votes,desc&start=1&title_type=feature&year=1950,2012"
response = requests.get(url)
if response.status_code != 200:
    print(f"Failed to retrieve the webpage. Status code: {response.status_code}")
    exit()
soup = BeautifulSoup(response.content, "html.parser")
movies = []
table = soup.find("tbody", class_="lister-list")  # Locate the table containing the movie list

for row in table.find_all("tr"):
    # Extract title
    title_column = row.find("td", class_="titleColumn")
    title = title_column.a.text.strip()
    year = title_column.span.text.strip("()")
    rating = row.find("td", class_="ratingColumn imdbRating").strong.text.strip()
    movies.append({"Title": title, "Year": year, "Rating": rating})
df = pd.DataFrame(movies)
df.to_csv("IMDb_Top_250_Movies.csv", index=False)
print(df.head())
