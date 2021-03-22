import time
import re
from script.jsonpack import *

def main():
    while(True):
        input_str = input("是否更新Battledata.json?(Y/N)")
        if (input_str == "Y" or input_str == "y"):
            battle_list_json = download_json(BDATA_JSON, "battleList.json")
            break
        elif (input_str == "N" or input_str == "n"):
            battle_list_json = read_json("battleList.json")
            break
    plus_str = input("请输入加成分隔，用半角逗号分开： ")
    plus_str_list = plus_str.split(",")
    plus_int_list = []
    for ps in plus_str_list:
        plus_int_list.append(int(ps))
    result_map = {}
    while(True):
        input_str = input("请输入要查询的关卡号，输入0退出：")
        if input_str == "0":
            break
        for qb in battle_list_json["uQuestBattleList"].values():
            k_list = qb.keys()
            if input_str not in k_list:
                continue
            quest_data = qb[input_str]
            if "addDropLotArr" not in quest_data:
                print("关卡[%s]没有掉落List！"%input_str)
                break
            cost_ap = quest_data["ap"]
            drop_lot_array = quest_data["addDropLotArr"].split(",")
            plus_drop_list = []
            # 计算不同加成下的掉落
            for plus in plus_int_list:
                total_drop = 0
                for drop_count in range(len(drop_lot_array)):
                    real_drop_plus = drop_count + plus
                    drop_pos = int(drop_lot_array[drop_count])
                    total_drop += real_drop_plus * drop_pos / 1000
                total_drop /= cost_ap
                plus_drop_list.append(total_drop)
            result_map[input_str] = plus_drop_list
            print("关卡[%s]记录成功！"%input_str)
            break
    with open("drop.csv", "w") as f:
        f.write("关卡,")
        for plus in plus_int_list:
            f.write("加成%d,"%plus)
        f.write("\n")
        for k, v in result_map.items():
            f.write("%s,"%k)
            for plus in v:
                f.write("%.2f,"%plus)
            f.write("\n")


if __name__ == "__main__":
    main()