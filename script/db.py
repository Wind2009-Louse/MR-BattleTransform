import math
import re
CHAR_ID_LIST = {
    1001 : "[[环伊吕波]]",
    1002 : "[[七海八千代]]",
    1003 : "[[由比鹤乃]]",
    1004 : "[[二叶莎奈]]",
    1005 : "[[深月菲莉希亚]]",
    1006 : "[[梓美冬]]",
    1007 : "[[里见灯花]]",
    1008 : "[[阿莉娜·格雷]]",
    1009 : "[[水波玲奈]]",
    1010 : "[[十咎桃子]]",
    1011 : "[[秋野枫]]",
    1012 : "[[御园花凛]]",
    1013 : "[[龙城明日香]]",
    1014 : "[[柊音梦]]",
    1015 : "[[环忧]]",
    1016 : "[[和泉十七夜]]",
    1017 : "[[八云御魂]]",
    1018 : "[[天音月夜]]",
    1019 : "[[天音月咲]]",
    1101 : "[[环伊吕波（泳装ver.）]]",
    1103 : "[[谣鹤乃]]",
    1108 : "[[圣阿莉娜]]",
    1117 : "[[八云御魂（晴着ver.）]]",
    2001 : "[[鹿目圆]]",
    2002 : "[[晓美焰]]",
    2003 : "[[晓美焰（眼镜ver.）]]",
    2004 : "[[美树沙耶香]]",
    2005 : "[[巴麻美]]",
    2006 : "[[佐仓杏子]]",
    2007 : "[[百江渚]]",
    2100 : "[[鹿目圆（晴着ver.）]]",
    2101 : "[[圆神]]",
    2102 : "[[小圆前辈]]",
    2300 : "[[晓美焰（泳装ver.）]]",
    2500 : "[[圣麻美]]",
    3001 : "[[矢宵鹿乃子]]",
    3002 : "[[空穗夏希]]",
    3003 : "[[都雏乃]]",
    3004 : "[[美凪纱纱罗]]",
    3005 : "[[常盘七夏]]",
    3006 : "[[木崎衣美里]]",
    3007 : "[[保澄雫]]",
    3008 : "[[志伸晶]]",
    3009 : "[[胡桃爱香]]",
    3010 : "[[阿见莉爱]]",
    3011 : "[[夏目佳子]]",
    3012 : "[[纯美雨]]",
    3013 : "[[伊吹丽良]]",
    3014 : "[[桑水清佳]]",
    3015 : "[[相野未都]]",
    3016 : "[[粟根心]]",
    3019 : "[[毬子彩花]]",
    3020 : "[[真尾日美香]]",
    3023 : "[[江利爱实]]",
    3025 : "[[五十铃怜]]",
    3026 : "[[静海木叶]]",
    3027 : "[[游佐叶月]]",
    3028 : "[[三栗菖蒲]]",
    3029 : "[[加贺见真良]]",
    3030 : "[[春名木乃美]]",
    3031 : "[[绫野梨花]]",
    3032 : "[[梢麻友]]",
    3033 : "[[史乃沙优希]]",
    3035 : "[[千秋理子]]",
    3037 : "[[安名梅露]]",
    3043 : "[[逢良花音]]",
    3046 : "[[观鸟令]]",
    3049 : "[[雪野加奈惠]]",
    3053 : "[[牧野郁美]]",
    3900 : "[[黑]]",
    4001 : "[[美国织莉子]]",
    4002 : "[[吴纪里香]]",
    4003 : "[[千岁由麻]]",
    4011 : "[[和美]]",
    4012 : "[[御崎海香]]",
    4013 : "[[牧薰]]",
    4021 : "[[塔鲁特]]",
    4022 : "[[莉兹]]",
    4023 : "[[梅丽莎]]",
    4025 : "[[可鲁波]]",
    4031 : "[[天乃铃音]]",
    4032 : "[[日向茉莉]]",
    4033 : "[[成见亚里纱]]",
    4034 : "[[诗音千里]]",
    4035 : "[[奏遥香]]",
    4041 : "[[战场原黑仪]]",
    4042 : "[[八九寺真宵]]",
    4043 : "[[神原骏河]]",
    4044 : "[[千石抚子]]",
    4045 : "[[羽川翼]]",
    4046 : "[[忍野忍]]",
    6000 : "[[钟摆的魔女]]",
    6001 : "[[立耳的魔女]]",
    6002 : "[[绝交阶梯之谣]]",
    6003 : "[[待人马之谣]]",
    6004 : "[[不幸角杯之谣]]",
    6005 : "[[无名人工智能之谣]]",
    6006 : "[[记忆馆长之谣]]",
    6007 : "[[螯合大摩天轮之谣]]",
    6008 : "[[Flower Speaker之谣]]",
    6009 : "[[兵熊之谣]]",
    6010 : "[[熊后之谣]]",
    6101 : "幸福的魔女",
    6103 : "[[沙地的魔女]]",
    6104 : "[[羊之魔女]]",
    6105 : "[[屋顶的魔女]]",
    6106 : "[[保护孩子的魔女]]",
    6107 : "[[生神的魔女]]",
    6108 : "[[橡胶的魔女]]",
    6109 : "[[流浪的魔女]]",
    6400 : "[[班长的魔女]]",
    6401 : "[[玫瑰园的魔女]]",
    6403 : "[[零食的魔女]]",
    6404 : "[[犬之魔女]]",
    6500 : "[[巧克力的魔女]]",
    6501 : "[[神滨圣女之谣]]",
    7000 : "[[钟摆的魔女的手下]]",
    7001 : "[[立耳的魔女的手下]]",
    7002 : "[[绝交挂锁之谣]]",
    7003 : "[[通灵绘马之谣]]",
    7004 : "[[不幸猫头鹰之谣]]",
    7005 : "[[无名邮件之谣]]",
    7006 : "[[记忆职员之谣]]",
    7007 : "[[螯合吉祥物之谣]]",
    7009 : "[[工熊之谣]]",
    7101 : "[[？？？魔女的手下]]",
    7102 : "[[镜之魔女的手下Ⅳ]]",
    7103 : "[[沙地的魔女的手下]]",
    7104 : "[[羊之魔女的手下]]",
    7105 : "[[屋顶的魔女的手下]]",
    7106 : "[[保护孩子的魔女的手下]]",
    7107 : "[[生神的魔女的手下]]",
    7108 : "[[橡胶的魔女的手下]]",
    7109 : "[[流浪的魔女的手下]]",
    7150 : "黑羽",
    7151 : "白羽",
    7201 : "[[象征的魔女的手下Ⅰ]]",
    7202 : "[[象征的魔女的手下Ⅱ]]",
    7203 : "[[象征的魔女的手下Ⅲ]]",
    7204 : "[[象征的魔女的手下Ⅳ]]",
    7211 : "[[镜之魔女的手下Ⅰ]]",
    7212 : "[[镜之魔女的手下Ⅱ]]",
    7213 : "[[镜之魔女的手下Ⅲ]]",
    7400 : "[[班长的魔女的手下]]",
    7401 : "[[玫瑰园的魔女的手下]]",
    7403 : "[[零食的魔女的手下]]",
    7404 : "[[犬之魔女的手下]]",
    7500 : "[[巧克力的魔女的手下]]",
    7600 : "[[铠甲的使魔Ⅰ]]",
    7601 : "[[铠甲的使魔Ⅱ]]"
}
ATTR_LIST = {"FIRE": "火",
             "TIMBER" : "木",
             "WATER": "水",
             "DARK": "暗",
             "LIGHT": "光",
             "VOID": "无"}
BAD_LIST = {'POISON':"毒",
            "BURN":"烧伤",
            "CURSE": "诅咒",
            "CHARM": "魅惑",
            "STUN": "眩晕",
            "RESTRAINT": "拘束",
            "FOG": "雾",
            "DARKNESS": "黑暗",
            "BLINDNESS": "幻惑",
            "BAN_SKILL": "技能封印",
            "BAN_MAGIA": "Magia封印",
            "INVALID_HEAL_HP": "HP回复禁止"}
GOOD_LIST = {"AUTO_HEAL":"自动回复",
             "AVOID":"回避",
             "COUNTER":"反击",
             "CRITICAL":"暴击",
             "DAMAGE_DOWN":"伤害削减",
             "DAMAGE_UP":"伤害上升",
             "DAMAGE_UP_BAD":"敌方状态异常时伤害UP",
             "DEFENSE_IGNORED":"防御无视",
             "MP_PLUS_WEAKED":"被弱点属性攻击时MPUP",
             "PROTECT":"保护",
             "PROVOKE":"挑衅",
             "PURSUE":"追击",
             "SKILL_QUICK":"技能冷却加速",
             "GUTS": "忍耐",
             "SURVIVE":"survive"}
CHANCE_GOOD_LIST = ["AVOID","COUNTER","CRITICAL","DAMAGE_DOWN","DAMAGE_UP",
                    "DEFENSE_IGNORED","PROVOKE","PROTECT","PURSUE","INVALID_HEAL_HP",
                    "SKILL_QUICK"]
WORDS_TRANS = {"ATTACK":"攻击力",
               "DEF":"防御力",
               "DEFENSE":"防御力",
               "MP_GAIN":"MP获得量",
               "RESIST":"异常状态耐性",
               "ACCEL":"Accele MP",
               "BLAST":"Blast伤害",
               "CHARGE": "Charge后伤害",
               "MAGIA":"Magia伤害",
               "DAMAGE":"造成伤害"}
REVOKE_TYPES = {"BUFF":"Buff解除",
                "DEBUFF":"Debuff解除",
                "BAD":"状态异常解除",
                "GOOD":"赋予效果解除"}
TYPE_WILL_ON_ENEMY = {"CONDITION_BAD","DEBUFF"}
COST_TRANS = {'みたま特製エナジードリンク':"饮料",
              "色鉛筆":"铅笔",
              "記憶の頁":"记忆之页",
              "回数券":"回数券",
              "ブラックカード":"黑卡",
              "フォーチュンペーパー":"幸运纸"}
SPECIAL_MEMORY_NAME = ["!","…","、","！","？"]

def char_idtostr(id,origin_str):
    if (type(id) != int): id = int(id)
    return_str = ""
    if origin_str == "幸福な魔女の手下":
        return "[[？？？魔女的手下|幸福的魔女的手下]]"
    if id % 10 == 9:
        return_str += "镜"
    real_id = math.floor(id / 100)
    if real_id in CHAR_ID_LIST:
        return_str += CHAR_ID_LIST[real_id]
    else:
        return_str += origin_str
    return return_str

def item_idtostr(id, json_data):
    new_id = re.sub(r'GIFT_(\d*)_\d*',r'\1', id)
    if (id == new_id): return ""
    new_id = int(new_id)
    for i in json_data['giftList']:
        if i['id'] == new_id:
            return "{{素材|%s}}" % i['name']
    return ""

def get_quest_header(id_str, json_data, item_data, height=1):
    return_str = ""
    battle_ap = 0
    battle_diff = 0
    battle_cost = "AP"
    battle_drop = ""
    battle_drop_list = []
    for i in json_data['uQuestBattleList'].keys(): # 比如101101
        for data_key in json_data['uQuestBattleList'][i].keys(): # 比如1011011
            if (id_str == data_key):
                if ('ap' in json_data['uSectionList'][i]):
                    battle_ap = json_data['uSectionList'][i]['ap']
                    battle_diff = json_data['uSectionList'][i]['difficulty']
                data = json_data['uQuestBattleList'][i][data_key]
                if 'title' in data.keys():
                    battle_title = data['title']
                    battle_title = re.sub('エクストラ', 'Extra', battle_title)
                elif json_data['uSectionList'][i]['questType'] == 'ACCOMPLISH':
                    temp_id = (data['sectionId'] % 100)
                    if (temp_id > 10):
                        temp_id -= 10
                    temp_id = (temp_id - 1) * 5 + data['sectionIndex']
                    battle_title = "BATTLE %d" % temp_id
                else:
                    battle_title = "BATTLE %d"%data['sectionIndex']
                if 'needItemNum' in data.keys():
                    battle_ap = data['needItemNum']
                elif 'ap' in data.keys():
                    battle_ap = data['ap']
                if 'difficulty' in data.keys():
                    battle_diff = data['difficulty']
                if 'useItem' in data.keys():
                    use_Item = data['useItem']['name']
                    if use_Item in COST_TRANS.keys():
                        battle_cost = COST_TRANS[use_Item]
                    else:
                        print("新消耗物品:%s"%use_Item)
                if 'consumeType' in data.keys() and data['consumeType'] == 'RAID':
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

                if json_data['uSectionList'][i]['questType'] == 'ACCOMPLISH':
                    if ('effectAdjusterList' in data):
                        battle_drop="HP回复量%d%%<br />MP回复量%d%%"%(data['effectAdjusterList'][0]['value']/10,data['effectAdjusterList'][0]['value']/10)
                        pass
                    else:
                        battle_drop = "无"
                    pass

                battle_drop = re.sub(r'＋',r'+',battle_drop)
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
    result = {"name": "",
              "HP": 0,
              "ATK": 0,
              "DEF": 0,
              "ATTR": set(),
              "MEM":set()}
    return result

def art_to_str(this_art):
    this_mem_str = ""
    if this_art['code'] == 'ENCHANT':
        sub_state = BAD_LIST[this_art['sub']]
        if this_art['rate'] != 1000:
            this_mem_str += '<span title="%.1f%%">攻击时概率赋予%s(%dT)状态</span>' % (this_art['rate'] / 10 ,sub_state, this_art['turn'])
        else:
            this_mem_str += '攻击时必定赋予%s(%dT)状态' % (sub_state, this_art['turn'])
    elif this_art['code'] == 'CONDITION_GOOD':
        this_mem_str += rate_append(this_art['sub'], this_art['rate'])
        this_art_str = GOOD_LIST[this_art['sub']]
        if this_art_str == '反击' and this_art['effect'] > 800:
            this_art_str = '交叉反击'
        elif this_art_str == '自动回复':
            if 'genericValue' in this_art.keys() and this_art['genericValue'] == 'MP':
                this_art_str = "MP自动回复"
                this_art_str = "%s(%d)" % (this_art_str, this_art['effect'] / 10)
            else:
                this_art_str = "HP自动回复"
                this_art_str = "%s(%d%%)" % (this_art_str, this_art['effect'] / 10)
        elif this_art_str == "保护" and this_art['target'] == 'DYING':
            this_art_str = "保护濒死的同伴"
        this_mem_str += this_art_str
    elif this_art['code'] == 'CONDITION_BAD':
        this_mem_str += rate_append(this_art['sub'], this_art['rate'])
        this_art_str = BAD_LIST[this_art['sub']]
        this_mem_str += this_art_str
    elif this_art['code'] == 'IGNORE':
        this_mem_str += rate_append(this_art['sub'], this_art['rate'])
        if this_art['sub'] in GOOD_LIST.keys():
            this_mem_str += "%s无效" % (GOOD_LIST[this_art['sub']])
        elif this_art['sub'] in BAD_LIST.keys():
            this_mem_str += "%s无效" % (BAD_LIST[this_art['sub']])
        else:
            print("CODE IGNORE新SUB:%s" % this_art['sub'])
    elif this_art['code'] == 'HEAL':
        if this_art['sub'] == "HP":
            this_mem_str += "HP回复"
        elif this_art['sub'] == "MP_DAMAGE":
            this_mem_str += "MP伤害"
        elif this_art['sub'] == "MP":
            this_mem_str += "MP回复"
        else:
            print("HEAL新sub:", this_art['sub'])
    elif this_art['code'] == 'REVOKE':
        if this_art['sub'] in REVOKE_TYPES.keys():
            this_mem_str += REVOKE_TYPES[this_art['sub']]
        else:
            print("REVOKE新sub: ",this_art['sub'])
    elif this_art['code'] == 'BUFF':
        this_mem_str += "%sUP" % (WORDS_TRANS[this_art['sub']])
    elif this_art['code'] == 'BUFF_DYING':
        this_mem_str += "濒死时%sUP" % (WORDS_TRANS[this_art['sub']])
    elif this_art['code'] == 'BUFF_HPMAX':
        this_mem_str += "HP最大时%sUP" % (WORDS_TRANS[this_art['sub']])
    elif this_art['code'] == 'BUFF_PARTY_DIE':
        this_mem_str += "同伴死亡时%sUP" % (WORDS_TRANS[this_art['sub']])
    elif this_art['code'] == 'DEBUFF':
        this_mem_str += "%sDOWN" % (WORDS_TRANS[this_art['sub']])
    elif this_art['code'] == 'INITIAL' and this_art['sub'] == 'MP':
        this_mem_str += "初始%d%%MP" % (this_art['effect'] / 10)
    else:
        print("ART新CODE:", this_art["code"])
    return this_mem_str

def rate_append(type,rate):
    if type in CHANCE_GOOD_LIST or type in BAD_LIST.keys():
        if rate > 1000:
            return '<span title="%.1f%%">必定</span>'%(rate/10)
        elif rate == 1000:
            return '必定'
        else:
            return '<span title="%.1f%%">概率</span>'%(rate/10)
    else:
        return ""

def range_to_str(this_art):
    result_str = ""
    if this_art['target'] == 'SELF':
        if this_art['code'] == 'HEAL':
            # 如 (自/10%)
            if this_art['sub'] == "MP" or this_art['sub'] == "MP_DAMAGE":
                result_str += "(自/%d)" % (this_art['effect']/10)
            else:
                result_str += "(自/%d%%)" % (this_art['effect']/10)
        elif 'turn' in this_art.keys():
            # 如 (自/3T)
            result_str += "(自/%dT)" % (this_art['turn'])
        else:
            result_str += "(自)"
    else:
        temp_str = ""
        # 敌单 敌全 单 全
        if (this_art['code'] == 'REVOKE' and (this_art['sub'] == 'BUFF' or this_art['sub'] == 'GOOD')) \
            or this_art['code'] in TYPE_WILL_ON_ENEMY \
            or (this_art['code'] == "HEAL" and this_art['sub'] == "MP_DAMAGE"):
            temp_str += "敌"

        if this_art['target'] == 'ALL':
            temp_str += '全'
        elif this_art['target'] == 'ONE' or this_art['target'] == 'TARGET':
            temp_str += '单'

        if 'turn' in this_art.keys():
            # 如 (敌单/1T)
            result_str += "(%s/%dT)" % (temp_str, this_art['turn'])
        elif this_art['code'] == "HEAL":
            # 如 (全/30%)
            if this_art['sub'] == "MP" or this_art['sub'] == "MP_DAMAGE":
                result_str += "(%s/%d)" % (temp_str,this_art['effect']/10)
            else:
                result_str += "(%s/%d%%)" % (temp_str,this_art['effect']/10)
        else:
            # 如 (敌全)
            result_str += "(%s)" % temp_str
    return result_str

def get_battle_enemy(json_data):
    return_str = ""
    enemy_count = 0
    wave_state = []
    # 加载敌人信息
    this_wave_index = 0
    for this_wave in json_data['waveList']:
        this_wave_index += 1
        this_wave_state = {
            "begin":this_wave_index,
            "end":this_wave_index,
            "enemies":[],
            "positions":[]
        }
        for this_enemy in this_wave['enemyList']:
            if this_enemy['enemySizeType'] == "BIG":
                this_wave_state["positions"].append(this_enemy["pos"])
                pass
            new_enemy = enemy_initial()
            new_enemy["HP"] = this_enemy["hp"]
            if new_enemy["HP"] == 0:
                continue
            new_enemy["name"] = char_idtostr(this_enemy["miniCharId"], this_enemy['name'])
            new_enemy["ATK"] = this_enemy["attack"]
            new_enemy["ATTR"].add(ATTR_LIST[this_enemy['align']])
            new_enemy["DEF"] = this_enemy["defence"]
            for mem_id in this_enemy['memoriaList']:
                if mem_id not in new_enemy["MEM"]:
                    new_enemy["MEM"].add(mem_id)
            have_same_enemy = False
            for enemy_before in this_wave_state["enemies"]:
                if enemy_before["name"] == new_enemy["name"] \
                and enemy_before["ATK"] == new_enemy["ATK"] \
                and enemy_before["DEF"] == new_enemy["DEF"] \
                and enemy_before["MEM"] == new_enemy["MEM"]:
                    have_same_enemy = True
                    # 相同属性自动省略
                    enemy_before["ATTR"].add(ATTR_LIST[this_enemy['align']])
                    break
            if not have_same_enemy:
                this_wave_state["enemies"].append(new_enemy)
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
        if this_wave['begin'] == this_wave['end']:
            wave_str = "%s"%this_wave['begin']
        else:
            wave_str = "%s-%s"%(this_wave['begin'],this_wave['end'])
        return_str += '| rowspan = "%d" | W%s\n'%(this_enemy_count,wave_str)
        # 判断是否为大型敌人
        positions_str = ""
        if len(this_wave["positions"]) > 0:
            positions_str = '{{敌人站位'
            for pos in range(1,10):
                positions_str += "|"
                if pos in this_wave["positions"]:
                    positions_str += str(pos)
            positions_str += '}}'
        # 每个敌人
        total_mem_str = ""
        for enemy in this_wave["enemies"]:
            attr_list = ""
            for each_attr in enemy['ATTR']:
                attr_list += each_attr
            return_str += '| %s<span title="ATK:%d&#10;DEF:%d">%s(%d/%s)</span> || '%(positions_str,enemy["ATK"],enemy["DEF"],enemy["name"],enemy["HP"],attr_list)
            # 敌人技能，按照能力型-技能型排序
            ability_memory = []
            skill_memory = []
            total_mem_str = ""
            for mem in json_data['memoriaList']:
                if mem['memoriaId'] in enemy["MEM"]:
                    if mem['cost'] > 0:
                        skill_memory.append(mem)
                    else:
                        ability_memory.append(mem)
            # 能力型
            for abi_mem in ability_memory:
                this_mem_str = ""
                # 获取效果
                this_art_list = []
                for art_id in abi_mem['artList']:
                    for art in json_data['artList']:
                        if art['artId'] == art_id:
                            this_art_list.append(art)
                            break
                # 将效果输出
                for art_id in range(len(this_art_list)):
                    if art_id > 0:
                        this_mem_str += "&"
                    this_art = this_art_list[art_id]
                    this_mem_str += art_to_str(this_art)
                if 'name' in abi_mem.keys():
                    need_add_skillname = False
                    for char in SPECIAL_MEMORY_NAME:
                        if char in abi_mem['name']:
                            need_add_skillname = True
                            break
                    if need_add_skillname:
                        this_mem_str = "{{Ruby|%s|%s}}"%(this_mem_str,abi_mem['name'])
                if (total_mem_str != ""):
                    total_mem_str += "<br />"
                total_mem_str += this_mem_str

            for skill_mem in skill_memory:
                this_mem_str = ""
                # 获取效果
                this_art_list = []
                for art_id in skill_mem['artList']:
                    for art in json_data['artList']:
                        if art['artId'] == art_id:
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

                this_mem_str = "%s[%dT]" % (this_mem_str, skill_mem['cost'])
                if 'name' in skill_mem.keys():
                    need_add_skillname = False
                    for char in SPECIAL_MEMORY_NAME:
                        if char in skill_mem['name']:
                            need_add_skillname = True
                            break
                    if need_add_skillname:
                        this_mem_str = "{{Ruby|%s|%s}}"%(this_mem_str,skill_mem['name'])
                if (total_mem_str != ""):
                    total_mem_str += "<br />"
                total_mem_str += this_mem_str
            return_str += (total_mem_str + "\n|-\n")
    return enemy_count,return_str
