from script.names import *

def get_quest_header(id_str, json_data, item_data, height=1):
    '''获得关卡内容(名字、难度、AP、掉落)'''
    return_str = ""
    battle_ap = 0
    battle_diff = 0
    battle_cost = "AP"
    battle_drop = ""
    battle_drop_list = []
    for i in json_data["uQuestBattleList"].keys(): # 比如101101
        for data_key in json_data["uQuestBattleList"][i].keys(): # 比如1011011
            if (id_str == data_key):
                if ("ap" in json_data["uSectionList"][i]):
                    battle_ap = json_data["uSectionList"][i]["ap"]
                    battle_diff = json_data["uSectionList"][i]["difficulty"]
                data = json_data["uQuestBattleList"][i][data_key]
                if "title" in data.keys():
                    battle_title = data["title"]
                    battle_title = re.sub("エクストラ", "Extra", battle_title)
                elif json_data["uSectionList"][i]["questType"] == "ACCOMPLISH":
                    temp_id = (data["sectionId"] % 100)
                    if (temp_id > 10):
                        temp_id -= 10
                    temp_id = (temp_id - 1) * 5 + data["sectionIndex"]
                    battle_title = "BATTLE %d" % temp_id
                else:
                    battle_title = "BATTLE %d"%data["sectionIndex"]
                if json_data["uSectionList"][i]["questType"] == "REG_ACC":
                    if "parameterMap" in data:
                        regParam = data["parameterMap"]
                        if "FLOOR" in regParam:
                            battle_title = "第%s阶段"%regParam["FLOOR"]

                if "needItemNum" in data.keys():
                    battle_ap = data["needItemNum"]
                elif "ap" in data.keys():
                    battle_ap = data["ap"]
                if "difficulty" in data.keys():
                    battle_diff = data["difficulty"]
                if "useItem" in data.keys():
                    use_Item = data["useItem"]["name"]
                    if use_Item in COST_TRANS.keys():
                        battle_cost = COST_TRANS[use_Item]
                    else:
                        print("新消耗物品:%s"%use_Item)
                if "consumeType" in data.keys() and data["consumeType"] == "RAID":
                    battle_cost = "RP"
                    battle_ap = 1

                dropItem = 1
                while(True):
                    keys_1 = "dropItem%d"%dropItem
                    if (keys_1 in data):
                        rewardCode = 1
                        while(True):
                            keys_2 = "rewardCode%d"%rewardCode
                            if (keys_2 in data[keys_1]):
                                gift_id = data[keys_1][keys_2]
                                gift_name = item_idtostr(gift_id, item_data)
                                if gift_name != "":
                                    if gift_name not in battle_drop_list:
                                        battle_drop_list.append(gift_name)
                                rewardCode += 1
                            else:
                                break
                        dropItem += 1
                    else:
                        break

                if len(battle_drop_list) == 0:
                    battle_drop = "无"
                else:
                    for item in battle_drop_list:
                        if (battle_drop != ""): battle_drop += "<br />"
                        battle_drop += item

                if json_data["uSectionList"][i]["questType"] == "ACCOMPLISH":
                    if ("effectAdjusterList" in data):
                        battle_drop="HP回复量%d%%<br />MP回复量%d%%"%(data["effectAdjusterList"][0]["value"]/10,data["effectAdjusterList"][0]["value"]/10)
                        pass
                    else:
                        battle_drop = "无"
                    pass

                battle_drop = re.sub(r"＋",r"+",battle_drop)
                # make str
                return_str += '| colspan="5" |\n|-\n'
                if (height == 1):
                    return_str += "| %s<br />难度 %d<br />消耗%s %d\n"%(battle_title, battle_diff, battle_cost, battle_ap)
                    return_str += "| %s\n"%battle_drop
                else:
                    return_str += '| rowspan = "%d" | %s<br />难度 %d<br />消耗%s %d\n' % (height, battle_title, battle_diff, battle_cost, battle_ap)
                    return_str += '| rowspan = "%d" |  %s\n' % (height, battle_drop)
                return return_str
    print("没有找到关卡%d！"%id_str)
    return return_str

def enemy_initial():
    '''初始化敌人信息，含：\n\nname, HP, ATK, DEF, ATTR, MEM, Magia, Doppel, position'''
    result = {"name": "",
              "HP": 0,
              "ATK": 0,
              "DEF": 0,
              "ATTR": set(),
              "MEM":set(),
              "Magia": 0,
              "Doppel": 0,
              "position":0}
    return result

def get_battle_enemy(json_data, battle_id=0):
    '''输出敌人信息'''
    return_str = ""
    enemy_count = 0
    wave_state = []
    # 加载敌人信息
    this_wave_index = 0
    for this_wave in json_data["waveList"]:
        this_wave_index += 1
        this_wave_state = {
            "begin":this_wave_index,
            "end":this_wave_index,
            "enemies":[],
            "positions":[],
            "allgirls":True
        }
        for this_enemy in this_wave["enemyList"]:
            # 如果是大型敌人，则记录其位置
            if "enemySizeType" in this_enemy.keys() and this_enemy["enemySizeType"] == "BIG":
                this_wave_state["positions"].append(this_enemy["pos"])
            new_enemy = enemy_initial()
            # 判断是否全为少女
            if type(this_enemy["miniCharId"]) != int:
                enemy_id = int(this_enemy["miniCharId"])
            else:
                enemy_id = this_enemy["miniCharId"]
            if (enemy_id >= 500000 and (enemy_id // 100) not in [7150,7151,7700,7701]) or enemy_id % 10 == 9:
                this_wave_state["allgirls"] = False
            # 读取
            new_enemy["HP"] = this_enemy["hp"]
            if new_enemy["HP"] == 0:
                continue
            new_enemy["name"] = char_idtostr(this_enemy["miniCharId"], this_enemy["name"])
            new_enemy["ATK"] = this_enemy["attack"]
            new_enemy["ATTR"].add(ATTR_LIST[this_enemy["align"]])
            new_enemy["DEF"] = this_enemy["defence"]
            if "pos" in this_enemy.keys():
                new_enemy["position"] = [this_enemy["pos"]]
            for mem_id in this_enemy["memoriaList"]:
                if mem_id not in new_enemy["MEM"]:
                    new_enemy["MEM"].add(mem_id)
            if "magiaId" in this_enemy:
                new_enemy["Magia"] = this_enemy["magiaId"]
            if "doppelId" in this_enemy:
                new_enemy["Doppel"] = this_enemy["doppelId"]
            # 判断是否存在相同的敌人
            have_same_enemy = False
            for enemy_before in this_wave_state["enemies"]:
                if enemy_before["name"] == new_enemy["name"] \
                and enemy_before["ATK"] == new_enemy["ATK"] \
                and enemy_before["DEF"] == new_enemy["DEF"] \
                and enemy_before["MEM"] == new_enemy["MEM"] \
                and enemy_before["Magia"] == new_enemy["Magia"] \
                and enemy_before["Doppel"] == new_enemy["Doppel"] :
                    have_same_enemy = True
                    # 相同属性自动省略
                    enemy_before["ATTR"].add(ATTR_LIST[this_enemy["align"]])
                    enemy_before["position"].append(this_enemy["pos"])
                    break
            if not have_same_enemy:
                this_wave_state["enemies"].append(new_enemy)
        # 清除标记
        if not this_wave_state["allgirls"]:
            for this_enemy in this_wave_state["enemies"]:
                this_enemy["position"] = 0
        # 判断是否和上一Wave重复
        if len(wave_state) > 0:
            last_wave = wave_state[len(wave_state)-1]
            isAllSame = True
            for enemy_this_wave in this_wave_state["enemies"]:
                if enemy_this_wave not in last_wave["enemies"]:
                    isAllSame = False
                    break
            for enemy_last_wave in last_wave["enemies"]:
                if enemy_last_wave not in this_wave_state["enemies"]:
                    isAllSame = False
                    break
            # 如果重复，则修改wave index
            if isAllSame:
                wave_state[len(wave_state) - 1]["end"] = this_wave_index
            else:
                wave_state.append(this_wave_state)
        else:
            wave_state.append(this_wave_state)
    
    # 开始转为字符串
    for wave_index in range(len(wave_state)):
        # 关卡基本信息
        this_wave = wave_state[wave_index]
        this_enemy_count = len(this_wave["enemies"])
        enemy_count += this_enemy_count
        if this_wave["begin"] == this_wave["end"]:
            wave_str = "%s"%this_wave["begin"]
        else:
            wave_str = "%s-%s"%(this_wave["begin"],this_wave["end"])
        return_str += '| rowspan = "%d" | W%s\n'%(this_enemy_count,wave_str)
        # 判断是否为大型敌人
        positions_str = ""
        if len(this_wave["positions"]) > 0:
            positions_str = "{{阵形"
            attr_color = ATTR_COLOR[list(this_wave["enemies"][0]["ATTR"])[0]]
            for pos in [7,4,1,8,5,2,9,6,3]:
                positions_str += "|"
                if pos in this_wave["positions"]:
                    positions_str += attr_color
            positions_str += "}}"
        # 每个敌人
        total_mem_str = ""
        for enemy in this_wave["enemies"]:
            attr_list = ""
            for each_attr in enemy["ATTR"]:
                attr_list += each_attr
            if this_wave["allgirls"]:
                attr_color = ATTR_COLOR[list(enemy["ATTR"])[0]]
                positions_str = ""
                if len(enemy["position"]) == 1:
                    positions_str = "{{阵形|%d=%s}}"%(POSITION_TRANSFORM[enemy["position"][0]],attr_color)
            return_str += '| %s<span title="ATK:%d&#10;DEF:%d">%s(%d/%s)</span> || '%(positions_str,enemy["ATK"],enemy["DEF"],enemy["name"],enemy["HP"],attr_list)
            # 敌人技能，按照能力型-技能型排序
            ability_memory = []
            skill_memory = []
            total_mem_str = ""
            for mem in json_data["memoriaList"]:
                if mem["memoriaId"] in enemy["MEM"]:
                    if mem["cost"] > 0:
                        skill_memory.append(mem)
                    else:
                        ability_memory.append(mem)
            # 能力型
            for abi_mem in ability_memory:
                this_mem_str = ""
                # 获取效果
                this_art_list = []
                for art_id in abi_mem["artList"]:
                    for art in json_data["artList"]:
                        if art["artId"] == art_id:
                            this_art_list.append(art)
                            break
                # 将效果输出
                for art_id in range(len(this_art_list)):
                    if art_id > 0:
                        this_mem_str += "&"
                    this_art = this_art_list[art_id]
                    this_mem_str += art_to_str(this_art)
                    # 判断是否需要输出效果范围(和下一个效果相同则不输出)
                    this_range = range_to_str(this_art)
                    if (art_id != len(this_art_list)-1):
                        next_range = range_to_str(this_art_list[art_id+1])
                    else:
                        next_range = ""
                    if this_range != next_range:
                        this_mem_str += this_range
                # 是否标记效果名
                if "name" in abi_mem.keys():
                    need_add_skillname = False
                    for char in SPECIAL_MEMORY_NAME:
                        if char in abi_mem["name"]:
                            need_add_skillname = True
                            break
                    if need_add_skillname:
                        this_mem_str = "{{Ruby|1=%s|2=%s}}"%(this_mem_str,abi_mem["name"])
                if (total_mem_str != ""):
                    total_mem_str += "<br />"
                # 战斗开始时附加状态的能力型记忆
                if "type" in abi_mem.keys() and abi_mem["type"] == "STARTUP":
                    this_mem_str = "战斗开始时获得" + this_mem_str
                total_mem_str += this_mem_str

            # 技能型
            for skill_mem in skill_memory:
                this_mem_str = ""
                # 获取效果
                this_art_list = []
                for art_id in skill_mem["artList"]:
                    for art in json_data["artList"]:
                        if art["artId"] == art_id:
                            this_art_list.append(art)
                            break
                # 将效果输出
                for art_id in range(len(this_art_list)):
                    if art_id > 0:
                        this_mem_str += "&"
                    this_art = this_art_list[art_id]
                    this_mem_str += art_to_str(this_art)
                    # 判断是否需要输出效果范围(和下一个效果相同则不输出)
                    this_range = range_to_str(this_art)
                    if (art_id != len(this_art_list)-1):
                        next_range = range_to_str(this_art_list[art_id+1])
                    else:
                        next_range = ""
                    if this_range != next_range:
                        this_mem_str += this_range

                this_mem_str = "%s[%dT]" % (this_mem_str, skill_mem["cost"])
                if "name" in skill_mem.keys():
                    need_add_skillname = False
                    for char in SPECIAL_MEMORY_NAME:
                        if char in skill_mem["name"]:
                            need_add_skillname = True
                            break
                    if need_add_skillname:
                        this_mem_str = "{{Ruby|1=%s|2=%s}}"%(this_mem_str,skill_mem["name"])
                if (total_mem_str != ""):
                    total_mem_str += "<br />"
                total_mem_str += this_mem_str
            
            # Magia
            if enemy["Magia"] != 0:
                this_mem_str = '<span class="mw-customtoggle-m%d-%d" style="background:LightGrey;">\
Magia</span><div class="mw-collapsible mw-collapsed" id="mw-customcollapsible-m%d-%d">'%(
battle_id, enemy["Magia"], battle_id, enemy["Magia"])
                # 获取效果
                this_art_list = []
                for magia in json_data["magiaList"]:
                    if magia["magiaId"] == enemy["Magia"]:
                        for art_id in magia["artList"]:
                            for art in json_data["artList"]:
                                if art["artId"] == art_id:
                                    this_art_list.append(art)
                                    break

                # 将效果输出
                is_dummy = False
                for art_id in range(len(this_art_list)):
                    if art_id > 0 and not (art_id == 1 and is_dummy):
                        this_mem_str += "&"
                    this_art = this_art_list[art_id]
                    art_str = art_to_str(this_art)
                    if art_str == "DUMMY":
                        is_dummy = True
                    else:
                        this_mem_str += art_to_str(this_art)
                    # 判断是否需要输出效果范围(和下一个效果相同则不输出)
                    this_range = range_to_str(this_art)
                    if (art_id != len(this_art_list)-1):
                        next_range = range_to_str(this_art_list[art_id+1])
                    else:
                        next_range = ""
                    if this_range != next_range:
                        this_mem_str += this_range
                this_mem_str += "</div>"
                if total_mem_str != "":
                    total_mem_str += "<br />"
                total_mem_str += this_mem_str

            # Doppel
            if enemy["Doppel"] != 0:
                this_mem_str = '<span class="mw-customtoggle-d%d-%d" style="background:Silver;">\
Doppel</span><div class="mw-collapsible mw-collapsed" id="mw-customcollapsible-d%d-%d">'%(
battle_id, enemy["Doppel"], battle_id, enemy["Doppel"])
                # 获取效果
                this_art_list = []
                for doppel in json_data["doppelList"]:
                    if doppel["doppelId"] == enemy["Doppel"]:
                        for art_id in doppel["artList"]:
                            for art in json_data["artList"]:
                                if art["artId"] == art_id:
                                    this_art_list.append(art)
                                    break
                # 将效果输出
                is_dummy = False
                for art_id in range(len(this_art_list)):
                    if art_id > 0 and not (art_id == 1 and is_dummy):
                        this_mem_str += "&"
                    this_art = this_art_list[art_id]
                    art_str = art_to_str(this_art)
                    if art_str == "DUMMY":
                        is_dummy = True
                    else:
                        this_mem_str += art_to_str(this_art)
                    # 判断是否需要输出效果范围(和下一个效果相同则不输出)
                    this_range = range_to_str(this_art)
                    if (art_id != len(this_art_list)-1):
                        next_range = range_to_str(this_art_list[art_id+1])
                    else:
                        next_range = ""
                    if this_range != next_range:
                        this_mem_str += this_range
                this_mem_str += "</div>"
                if total_mem_str != "" and enemy["Magia"] == 0:
                    total_mem_str += "<br />"
                total_mem_str += this_mem_str

            return_str += (total_mem_str + "\n|-\n")
    return enemy_count,return_str
