import requests
from bs4 import BeautifulSoup
import pandas as pd


url = "https://www.billboard.com/charts/hot-100/"
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.text, 'html.parser')
title = soup.title
# print(soup.prettify())

date_of_chart = soup.find('p', class_='u-font-size-11@mobile-max').text.strip()
date_of_chart = date_of_chart[8:]


# Grabs all rankings
rankings = []
all_rankings = soup.find_all('span', class_='u-letter-spacing-0080@tablet')
for rank in all_rankings:
    ranking_text = rank.text.strip()
    rankings.append(int(ranking_text))

# Grabs all album covers
target_divs = soup.find_all('div', class_='a-crop-67x100@mobile-max')
album_covers = []
for div in target_divs:
    img_tag = div.find('img', class_='lrv-u-height-auto')
    if img_tag:
        album_covers.append(img_tag['data-lazy-src'])


# Grabs all song titles
song_array = []
song_titles = soup.find_all('h3', class_='lrv-u-font-size-18@tablet')
# Grabs #1 ranked song (special class)
song_array.append(soup.find('h3', class_='a-font-primary-bold-m@mobile-max').text.strip())
# Grabs rest of songs
for song in song_titles:
    song_text = song.text.strip()
    song_array.append(song_text)

# Grabs all song authors
authors = []
all_authors = soup.find_all('span', class_='lrv-u-font-size-14@mobile-max')
for author in all_authors:
    author_text = author.text.strip()
    authors.append(author_text)


# Grabs all statsistics
target_lis = soup.find_all('li', class_='lrv-u-flex-grow-1')
stats = []
for li in target_lis:
    span_tag = li.find('span', class_='lrv-u-padding-tb-050@mobile-max')
    if span_tag:
        stats.append(span_tag.text.strip())

# Splits statistics into corresponding array
last_week_pos = []
peak_pos = []
weeks_on_chart = []
for i in range(1, 301):
    if i%3 == 1: 
        last_week_pos.append(stats[i-1])
    elif i%3 == 2:
        peak_pos.append(stats[i-1])
    else:
        weeks_on_chart.append(stats[i-1])




data = {'Title': title, 'Date': date_of_chart, 'Ranking': rankings, 'Cover Art': album_covers, 'Song Titles': song_array,'Authors': authors, 'Last Week Position': last_week_pos, 'Peak Position': peak_pos, 'Weeks On Chart': weeks_on_chart}
df = pd.DataFrame(data)
df.to_excel(f'Billboard_Top_100_Songs_{date_of_chart}.xlsx', index=False)
df.to_csv(f'Billboard_Top_100_Songs_{date_of_chart}.csv', index=False)


