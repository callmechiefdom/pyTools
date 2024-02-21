import csv, re
import requests
from bs4 import BeautifulSoup

def parse_song_info(line):
    match = re.match(r'(\d+)\.\s*(.*?)\s*-\s*(.*)', line)
    if match:
        rank, song, artist = match.groups()
        return rank.strip(), song.strip(), artist.strip()
    else:
        print(f"Unable to parse line: {line}")
        return None

def read_text_file(file_path):
    # with open(file_path, 'r', encoding='utf-8') as file:
    #     lines = file.readlines()
    # return [parse_song_info(line) for line in lines]
    song_data = []
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()
        for line in lines:
            parsed_info = parse_song_info(line)
            if parsed_info:
                song_data.append(parsed_info)
    return song_data

def search_song(song):
    search_url = 'https://www.tencymusic.com/catalog.php?mquery='
    response = requests.get(search_url + requests.utils.requote_uri(song))
    if response.status_code != 200:
        response.raise_for_status()
    return response.text

def find_matching_song(html, song, artist):
    soup = BeautifulSoup(html, 'html.parser')
    for tr in soup.find_all('tr', attrs={'song-id': True}):
        song_elem = tr.find('td').find_next_sibling('td').find('a')
        artist_elem = tr.find('td').find_next_sibling('td').find_next_sibling('td')
        if song_elem and artist_elem:
            if (song_elem.text.strip().lower() == song.lower() and
                artist_elem.text.strip().split('&')[0].split('(*)')[0].strip().lower() == artist.lower()):
                return 'https://www.tencymusic.com' + song_elem.get('href').strip()
    return None

def save_to_csv(filename, data):
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Rank', 'Physical', 'Artist', 'Url'])
        writer.writerows(data)

def run_crawler(input_txt, output_csv):
    song_data = read_text_file(input_txt)
    matched_songs = []
    for rank, song, artist in song_data:
        print(f"Processing rank: {rank}")  # Helpful for debugging
        html = search_song(song)
        song_url = find_matching_song(html, song, artist)
        if song_url:
            matched_songs.append([rank, song, artist, song_url])
    save_to_csv(output_csv, matched_songs)
    print(f"{len(matched_songs)} songs have been saved to {output_csv}")

if __name__ == '__main__':
    input_txt_path = '90list.txt'
    output_csv_path = '90s_songs_with_urls.csv'
    run_crawler(input_txt_path, output_csv_path)
