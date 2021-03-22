import time
import re
from script.jsonpack import *

def main():
    while(True):
        input_str = input("是否更新CharaCard.json?(Y/N)")
        if (input_str == 'Y' or input_str == 'y'):
            chara_json = download_json("https://stat.magireco.moe/data/charaCard.json", "CharaCard.json")
            break
        elif (input_str == 'N' or input_str == 'n'):
            chara_json = read_json("CharaCard.json")
            break
    for per_chara in chara_json.values():
        if 'enhancementCellList' not in per_chara:
            continue
        enhance_list = per_chara['enhancementCellList']
        if len(enhance_list) == 0:
            continue
        print("%d\t%d"%(per_chara['id'], per_chara['enhancementCellList'][0]['groupId']))

if __name__ == '__main__':
    main()
