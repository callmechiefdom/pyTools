import re

def process_file(filename):
    # 尝试打开并读取文件
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            lines = file.readlines()
    except FileNotFoundError:
        print(f'Error: File {filename} not found.')
        return
    except IOError as e:
        print(f'An I/O error occurred: {e}')
        return

    # 处理文件的每一行
    processed_lines = [re.sub(r'\s*@.*', '', line) for line in lines]

    # 创建新的文件名并写入处理后的内容
    new_filename = 'processed_' + filename
    try:
        with open(new_filename, 'w', encoding='utf-8') as new_file:
            new_file.writelines(processed_lines)
    except IOError as e:
        print(f'An I/O error occurred while writing to {new_filename}: {e}')
        return

    print(f"Processed data has been written to {new_filename}")

if __name__ == '__main__':
    print("Please enter the filename (with extension) you'd like to process:")
    filename = input().strip()
    process_file(filename)
