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
    output_str = ""
    header = "ID,Name,Enhanced HP,Enhanced ATK,Enhanced DEF,Enhanced Accele,Enhanced Blast,Enhanced Charge\n"
    header_2 = "Skill No.,Skill Name,Description,Type,,Effect 1 Name,Effect 1 Value,Effect 1 Probability,,Effect 2 Name,Effect 2 Value,Effect 2 Probability\n"
    split_str = "\t\t\t\t\t\t\t\t\t\t\t\n"
    for per_chara in chara_json.values():
        if 'enhancementCellList' not in per_chara:
            continue
        enhance_list = per_chara['enhancementCellList']
        if len(enhance_list) == 0:
            continue
        sumup = {"ATTACK":0,"DEFENSE":0,"HP":0,"DISK_ACCELE":0,"DISK_BLAST":0,"DISK_CHARGE":0}
        skill_sumup = []

        for idx in range(len(enhance_list)):
            cell = enhance_list[idx]
            # 类型
            type_str = cell['enhancementType']
            # 基本类型
            if type_str in ['HP','ATTACK','DEFENSE']:
                sumup[type_str] += cell['effectValue']
            # 盘型
            elif type_str[0:5] == "DISK_":
                sumup[type_str] += cell['effectValue']/10
            # 技能
            elif type_str == "SKILL":
                for count in range(1, 11):
                    if 'art%d'%count in cell['emotionSkill']:
                        pass
                skillid = cell['effectValue']
                skillname = cell['emotionSkill']['name']
                skilldesp = cell['emotionSkill']['shortDescription']
                if cell['emotionSkill']["type"] == "ABILITY":
                    skilltype = "Passive"
                else:
                    skilltype = "Active CD%d"%cell['emotionSkill']['intervalTurn']
                art_1 = cell['emotionSkill']['art1']
                art_1_name = art_1["effectCode"]
                if 'effectValue' in art_1:
                    if art_1_name in ["MP_DAMAGE"]:
                        art_1_value = "%.1f"%art_1['effectValue']
                    else:
                        art_1_value = "%.1f%%"%(art_1['effectValue']/10)
                else:
                    art_1_value = "N/A"
                if 'probability' in art_1:
                    art_1_poss = "%.1f%%"%(art_1['probability']/10)
                else:
                    art_1_poss = "N/A"

                if 'art2' not in cell['emotionSkill']:
                    art_2_name = ""
                    art_2_value = ""
                    art_2_poss = ""
                else:
                    art_2 = cell['emotionSkill']['art2']
                    art_2_name = art_2["effectCode"]
                    if 'effectValue' in art_2:
                        if art_2_name in ["MP_DAMAGE"]:
                            art_2_value = "%.1f"%art_2['effectValue']
                        else:
                            art_2_value = "%.1f%%"%(art_2['effectValue']/10)
                    else:
                        art_2_value = "N/A"
                    if 'probability' in art_2:
                        art_2_poss = "%.1f%%"%(art_2['probability']/10)
                    else:
                        art_2_poss = "N/A"
                    if 'art3' in cell['emotionSkill']:
                        print("art 3 exists.")
                
                skill_sumup.append("%d,%s,%s,%s,,%s,%s,%s,,%s,%s,%s\n"%(skillid, skillname, skilldesp, skilltype,
                art_1_name, art_1_value, art_1_poss, art_2_name, art_2_value, art_2_poss))

            else:
                pass

        output_str += header
        output_str += "%d,%s,%d,%d,%d,%d%%,%d%%,%d%%\n"%(per_chara['id'], per_chara['name'], 
            sumup["HP"], sumup["ATTACK"], sumup["DEFENSE"],
            sumup["DISK_ACCELE"], sumup["DISK_BLAST"], sumup["DISK_CHARGE"])
        output_str += split_str
        output_str += header_2
        for s in skill_sumup:
            output_str += s
        output_str += split_str
        output_str += split_str
    with open("enhancement.csv", 'w', encoding="utf-8-sig") as f:
        f.write("\n")
        f.write(output_str)


if __name__ == '__main__':
    main()
