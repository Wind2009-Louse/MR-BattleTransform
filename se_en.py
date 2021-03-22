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
    header_2 = "Skill No.,Skill Name,Description,Type,Effect Verb,Effect Name,Effect Value,Effect Probability\n"
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
                skillid = cell['effectValue']
                skillname = cell['emotionSkill']['name']
                skilldesp = cell['emotionSkill']['shortDescription']
                if cell['emotionSkill']["type"] == "ABILITY":
                    skilltype = "Passive"
                elif cell['emotionSkill']["type"] == "STARTUP":
                    skilltype = "Startup"
                else:
                    skilltype = "Active CD%d"%cell['emotionSkill']['intervalTurn']
                skill_sumup.append("%d,%s,%s,%s,"%(skillid, skillname, skilldesp, skilltype))
                
                for count in range(1, 11):
                    if 'art%d'%count in cell['emotionSkill']:
                        art = cell['emotionSkill']['art%d'%count]
                        art_name = art["effectCode"]

                        if 'verbCode' in art:
                            art_verb = art['verbCode']
                        else:
                            art_verb = "N/A"

                        if 'effectValue' in art:
                            if art_name in ["MP_DAMAGE"]:
                                art_value = "%.1f"%art['effectValue']
                            else:
                                art_value = "%.1f%%"%(art['effectValue']/10)
                        else:
                            art_value = "N/A"
                        
                        if 'genericValue' in art:
                            art_name += " %s"%(art['genericValue'])

                        if 'probability' in art:
                            art_poss = "%.1f%%"%(art['probability']/10)
                        else:
                            art_poss = "N/A"
                        
                        if 'art%d'%(count+1) in cell['emotionSkill']:
                            skill_sumup.append("%s,%s,%s,%s\n,,,,"%(art_verb, art_name, art_value, art_poss))
                        else:
                            skill_sumup.append("%s,%s,%s,%s\n"%(art_verb, art_name, art_value, art_poss))
            else:
                pass

        chara_name = per_chara['name']
        if 'title' in per_chara:
            chara_name += "（%s）"%per_chara['title']

        output_str += header
        output_str += "%d,%s,%d,%d,%d,%d%%,%d%%,%d%%\n"%(per_chara['id'], chara_name, 
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
