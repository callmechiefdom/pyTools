'''
Author: Chiefdom
Date: 2023-08-15 15:27:41
Description: search from setting : customMade
'''
import os, json
from PIL import Image

# pip freeze > requirements.txt
# from t_cover import cover_files

# from os import chdir, path as p
# chdir(p.dirname(p.abspath(__file__)))
# sys.path.append("conf")

def copy_dir(src_path, target_path, srcSuffix, targetSuffix):
    result = []
    if os.path.isdir(src_path) and os.path.isdir(target_path):
        filelist_src = os.listdir(src_path)
        for file in filelist_src:
            path = os.path.join(os.path.abspath(src_path), file)
            if os.path.isdir(path):
                path1 = os.path.join(os.path.abspath(target_path), file)	
                if not os.path.exists(path1):						
                    os.mkdir(path1)
                result.extend(copy_dir(path,path1))
            else:
                path1 = os.path.join(target_path, file)
                if os.path.isfile(path) and (("." + srcSuffix) in path):
                    image = Image.open(path)
                    png_file = path1.split(srcSuffix)[0] + targetSuffix
                    image.save(png_file)
                    result.append(png_file)
        return result

if __name__ == "__main__":
    confPath = "./config.json"

    with open(confPath, 'r') as genFile:
        config = json.load(genFile)

    print(" ----------- check path && conf ------------")

    srcSuffix = config.get('srcType')
    targetSuffix = config.get('targetType')

    # 对路径配置进行检测
    if not os.path.exists(config.get('InputPath')):
        print(" ----------------- ERROR : InputPath DoesNot ESIST -----------------")
        print(f" ----------------- {config.get('InputPath')} -----------------")
        print(" ----------------- ERROR : InputPath DoesNot ESIST -----------------")
        os._exit(0)

    if not os.path.exists(config.get('OutputPath')):
        print(" ----------------- ERROR : OutputPath DoesNot ESIST -----------------")
        print(f" ----------------- {config.get('OutputPath')} -----------------")
        print(" ----------------- ERROR : OutputPath DoesNot ESIST -----------------")
        os._exit(0)

    outputPath = config.get('OutputPath') + config.get('OutputName')
    if not os.path.exists(outputPath):
        os.mkdir(outputPath)

    # 将目标目录文件进行转换
    print(" ----------- copy files ------------")
    pngList = copy_dir(config.get('InputPath'), outputPath, srcSuffix, targetSuffix)
    print(" ----------- copy FINISHED ------------")
    print("ALL work is DONE!!!")
    pass


# D:/server/pyTools/png-tga.trans/Input
# D:/server/pyTools/png-tga.trans/Output