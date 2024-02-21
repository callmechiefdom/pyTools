import json
import requests
from bs4 import BeautifulSoup

# 读取topList.json文件
def read_json_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    return data

# 查询歌曲信息
def search_song(query):
    base_url = 'https://www.tencymusic.com/catalog.php?mquery='
    response = requests.get(base_url + query)
    print(f'response.status_code: {response.status_code}')
    if response.status_code == 200:
        return response.text
    else:
        response.raise_for_status()

# 解析响应内容并提取信息
def extract_info(html_content, song_name, auth):
    soup = BeautifulSoup(html_content, 'html.parser')
    rows = soup.find_all('tr', attrs={'song-id': True})
    # print(f"row: {rows}")
    for row in rows:
        anchor_tag = row.find('td').find_next_sibling('td').find('a')
        author_tag = row.find('td').find_next_sibling('td').find_next_sibling('td')
        if anchor_tag and author_tag:
            extracted_song_name = anchor_tag.text.strip().split('(*)')[0].strip()
            extracted_auth = author_tag.text.strip().split('&')[0].split('(*)')[0].strip()
            print(f" ################## ")
            print(f"extracted_song_name: {extracted_song_name}")
            print(f"extracted_auth: {extracted_auth}")
            if extracted_song_name == song_name and extracted_auth == auth:
                href = anchor_tag['href']
                song_url = 'https://www.tencymusic.com' + href
                return song_url
    return None

# 保存信息到新的JSON文件
def save_to_json(fetch_list, file_path='fetchList.json'):
    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(fetch_list, file, ensure_ascii=False, indent=4)

# 主执行函数
def run_crawler():
    top_list = read_json_file('topList.json')
    fetch_list = []
    
    for item in top_list:
        song_name = item.get('songName')
        auth = item.get('auth')
        id = item.get('id')
        print(f"-------------- {id} ---------------")
        print(f'songName: {song_name}')
        print(f'auth: {auth}')
        if song_name and auth:
            html_content = search_song(song_name)
            url = extract_info(html_content, song_name, auth)
            if url:
                fetch_list.append({
                    "id": item.get('id'),
                    "songName": song_name,
                    "auth": auth,
                    "url": url
                })

    save_to_json(fetch_list)

if __name__ == "__main__":
    run_crawler()