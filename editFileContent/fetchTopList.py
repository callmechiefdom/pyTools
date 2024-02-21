import json
import re
import sys

def extract_songs(file_content):
    # 正则表达式匹配每个歌曲的模式
    pattern = re.compile(r'^(\d+)\s*\n\n(.*?)\n(.*?)\n', re.M | re.S)
    
    song_list = []
    for match in pattern.finditer(file_content):
        song_id = match.group(1).strip()
        song_name = match.group(2).strip()
        song_artist = match.group(3).strip()
        song = {
            'id': int(song_id),
            'songName': song_name,
            'auth': song_artist
        }
        song_list.append(song)
    
    return song_list

def save_to_json(file_path, song_data):
    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(song_data, file, indent=4, ensure_ascii=False)

def main(input_file, output_file):
    try:
        # 读取文件内容
        with open(input_file, 'r', encoding='utf-8') as file:
            content = file.read()

        # 提取歌曲信息
        songs = extract_songs(content)

        # 保存为JSON文件
        save_to_json(output_file, songs)

        print(f"提取的歌曲信息已保存到 '{output_file}'.")
    except Exception as e:
        print(f"处理过程中发生错误：{e}")

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("使用方法: python script.py 输入文件名 输出文件名")
    else:
        input_file = sys.argv[1]
        output_file = sys.argv[2]
        main(input_file, output_file)


# python fetchTopList.py topList.txt topList_extracted.json









# 你是资深架构师，精通前后端框架设计和编程，拥有极其丰富的技术栈。python大师。现在帮我写个工具，
# 从文件中提取出里面指定的内容，并用json格式保存文件。需要提取出歌名，歌手等信息。
# 提取的结构类似下面的结果：
# {
# 	{
# 		"id": 1,
# 		"songName": "Dance You Outta My Head",
# 		"auth": "Cat Janice"
# 	}, {
# 		"id": 2,
# 		"songName": "Little Life",
# 		"auth": "Cordelia"
# 	}
# }
# 以下是待提取的文件中的内容：
