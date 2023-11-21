import requests
from bs4 import BeautifulSoup
import csv

# Send a GET request to the website
url = 'https://www.boxofficemojo.com/year/world/'
response = requests.get(url)

# Parse the HTML content using BeautifulSoup
soup = BeautifulSoup(response.content, 'html.parser')

# Find the table containing movie data
table = soup.find('table', )

# Extract table headers
headers = [header.text.strip() for header in table.find_all('th')]

# Extract table rows
rows = []
for row in table.find_all('tr'):
    rows.append([val.text.strip() for val in row.find_all('td')])

# Remove empty rows
rows = [row for row in rows if row]

# Save data to a CSV file
csv_filename = 'top_grossing_movies_world_2023.csv'
with open(csv_filename, 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(headers)
    writer.writerows(rows)

print(f"Table successfully scraped and saved as '{csv_filename}'")