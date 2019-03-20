import time
from script import db
from script.jsonpack import *

def main():
    while(True):
        input_str = input("是否更新Battledata.json?(Y/N)")
        if (input_str == 'Y' or input_str == 'y'):
            battle_list_json = download_json(BDATA_JSON, "battleList.json")
            break
        elif (input_str == 'N' or input_str == 'n'):
            battle_list_json = read_json("battleList.json")
            break
    while(True):
        input_str = input("是否更新gift.json?(Y/N)")
        if (input_str == 'Y' or input_str == 'y'):
            gift_json = download_json(GIFT_JSON, "gift.json")
            break
        elif (input_str == 'N' or input_str == 'n'):
            gift_json = read_json("gift.json")
            break
    output_result = '{| class="wikitable" style="text-align:center; margin:0 auto;"\n! 关卡 !! 材料掉落 !! Wave !! 敌人 !! 技能\n|-\n'
    mode = 0
    while(True):
        if (mode == 0):
            id = input("输入查询关卡id(如1011011)，输入1切换模式，输入9输出当前内容，输入0退出:")
            if (id == "0"): break
            if (id == "9"):
                output_result += '|}'
                os.chdir(os.getcwd())
                dir = os.path.join(os.getcwd(),"output")
                if not os.path.exists(dir):
                    os.mkdir(dir)
                file_name = os.path.join(dir, time.strftime("%Y-%m-%d %H-%M-%S.txt", time.localtime()))
                file = open(file_name,"w",encoding="utf-8")
                file.write(output_result)
                file.close()
                output_result = '{| class="wikitable" style="text-align:center; margin:0 auto;"\n! 关卡 !! 材料掉落 !! Wave !! 敌人 !! 技能\n|-\n'
                print("成功输出！")
                continue
            if (id == '1'):
                mode = 1
                continue
            quest_json = jsonjudge_auto(id)
            if (quest_json == []):
                print("没有找到该关卡！")
                deletejson(id)
                continue
            total_enemy, return_str = db.get_battle_enemy(quest_json)
            str_header = db.get_quest_header(id, battle_list_json, gift_json, total_enemy)
            print_str = str_header + return_str
            output_result += print_str
        else:
            id = input("输入查询关卡组id(如101101)，输入1切换模式，输入9输出当前内容，输入0退出:")
            if (id == "0"): break
            if (id == "9"):
                output_result += '|}'
                os.chdir(os.getcwd())
                dir = os.path.join(os.getcwd(),"output")
                if not os.path.exists(dir):
                    os.mkdir(dir)
                file_name = os.path.join(dir, time.strftime("%Y-%m-%d %H-%M-%S.txt", time.localtime()))
                file = open(file_name,"w",encoding="utf-8")
                file.write(output_result)
                file.close()
                output_result = '{| class="wikitable" style="text-align:center; margin:0 auto;"\n! 关卡 !! 材料掉落 !! Wave !! 敌人 !! 技能\n|-\n'
                print("成功输出！")
                continue
            if (id == "1"):
                mode = 0
                continue
            if id not in battle_list_json["uQuestBattleList"].keys():
                print("没有找到该关卡组！")
                continue
            keys = battle_list_json["uQuestBattleList"][id].keys()
            for battle_id in keys:
                quest_json = jsonjudge_auto(battle_id)
                if (quest_json == []):
                    print("没有找到该关卡！")
                    deletejson(battle_id)
                    continue
                total_enemy, return_str = db.get_battle_enemy(quest_json)
                str_header = db.get_quest_header(battle_id, battle_list_json, gift_json, total_enemy)
                print_str = str_header + return_str
                output_result += print_str

    output_result += '|}'
    os.chdir(os.getcwd())
    dir = os.path.join(os.getcwd(),"output")
    if not os.path.exists(dir):
        os.mkdir(dir)
    if output_result != '{| class="wikitable" style="text-align:center; margin:0 auto;"\n! 关卡 !! 材料掉落 !! Wave !! 敌人 !! 技能\n|-\n|}':
        file_name = os.path.join(dir, time.strftime("%Y-%m-%d %H-%M-%S.txt", time.localtime()))
        file = open(file_name,"w",encoding="utf-8")
        file.write(output_result)
        file.close()
    print("程序退出。")

if __name__ == '__main__':
    main()
