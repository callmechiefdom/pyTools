import csv
import requests
from bs4 import BeautifulSoup

# Read CSV file and convert to list of dictionaries
def read_csv_file(file_path):
    with open(file_path, mode='r', encoding='utf-8-sig') as file:
        csv_reader = csv.DictReader(file)
        return list(csv_reader)

# Send HTTP request to search for the song
def search_song_by_name(song_name):
    search_url = 'https://www.tencymusic.com/catalog.php?mquery=' + requests.utils.requote_uri(song_name)
    response = requests.get(search_url)
    if response.status_code == 200:
        return response.content
    else:
        response.raise_for_status()

# Extract matching song information from the HTML response
def extract_song_info(html_content, song_name, artist):
    soup = BeautifulSoup(html_content, 'html.parser')
    for tr in soup.find_all('tr', attrs={'song-id': True}):
        song_title_elem = tr.find('td').find_next_sibling('td').find('a')
        artist_elem = tr.find('td').find_next_sibling('td').find_next_sibling('td')
        if song_title_elem and artist_elem:
            extracted_song = song_title_elem.text.strip().split('(*)')[0].strip()
            extracted_artist = artist_elem.text.strip().split('&')[0].split('(*)')[0].strip()
            if extracted_song.lower() == song_name.lower() and extracted_artist.lower() == artist.lower():
                href = song_title_elem.get('href').strip()
                return 'https://www.tencymusic.com' + href
    return None

# Save the results to a CSV file
def save_csv(file_path, data):
    with open(file_path, mode='w', encoding='utf-8', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=['Rank', 'Song', 'Artist', 'Url'])
        writer.writeheader()
        for record in data:
            writer.writerow(record)

# Main program
def run_crawler(input_csv, output_csv):
    records = read_csv_file(input_csv)
    results = []

    for record in records:
        print(f"Processing record: {record}")  # Helpful for debugging
        html_content = search_song_by_name(record['Song'])
        song_url = extract_song_info(html_content, record['Song'], record['Artist'])
        if song_url:
            results.append({
                'Rank': record['Rank'],
                'Song': record['Song'],
                'Artist': record['Artist'],
                'Url': song_url
            })

    # Save matched results to a new CSV file
    save_csv(output_csv, results)
    print(f"Matched information saved into '{output_csv}'")

if __name__ == '__main__':
    input_csv_path = '80list.csv'
    output_csv_path = '80list_with_urls.csv'
    run_crawler(input_csv_path, output_csv_path)