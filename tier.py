#encoding=utf-8
import json
import math

# 把记忆考虑进去
MEMO_INCLUDE = {1040: 1470}
# 自定义精神强化数值，未乘以0.6
SE_SUM = {}
DEBUG = False

allchara_file = []
with open("charaCard.json", "r", encoding="utf-8") as f:
    allchara_file_text = f.read()
    allchara_file = json.loads(allchara_file_text)
allmemo_file = []
with open("memoria.json", "r", encoding="utf-8") as f:
    allmemo_file_text = f.read()
    allmemo_file = json.loads(allmemo_file_text)

ROLL_ACCELE_MEMO_CHARA_LIST = []
ROLL_BLAST_MEMO_CHARA_LIST = []
ROLL_CHARGE_MEMO_CHARA_LIST = []
ROLL_SELF_MEMO_CHARA_LIST = []
CHARA_DICT = {}
BEST_DISC_CACHE = {}

for memo_key in allmemo_file:
    memo = allmemo_file[memo_key]
    if "charaList" not in memo or memo["charaList"] == []:
        continue
    for mlb_idx in range(5, 0, -1):
        chara_id_list = []
        for c in memo["charaList"]:
            chara_id_list.append(c["charaId"])
        mlb_key = "pieceSkill%d"%mlb_idx
        if mlb_key not in memo:
            continue
        mlb_data = memo[mlb_key]
        for art_idx in range(1, 10):
            art_key = "art%d"%art_idx
            if art_key not in mlb_data:
                break
            memo_art = mlb_data[art_key]
            if "verbCode" in memo_art and "effectCode" in memo_art and memo_art["verbCode"] == "DRAW":
                memo_eff = memo_art["effectCode"]
                if memo_eff in ["ALIGNMENT", "CHARACTER"]:
                    ROLL_SELF_MEMO_CHARA_LIST.extend(chara_id_list)
                if "AGAIN" == memo_eff:
                    for c_id in chara_id_list:
                        MEMO_INCLUDE[c_id] = memo["pieceId"]
                if "ACCEL" == memo_eff:
                    ROLL_ACCELE_MEMO_CHARA_LIST.extend(chara_id_list)
                if "BLAST" == memo_eff:
                    ROLL_BLAST_MEMO_CHARA_LIST.extend(chara_id_list)
                if "CHARGE" == memo_eff:
                    ROLL_CHARGE_MEMO_CHARA_LIST.extend(chara_id_list)
        break

disc_num_dict = {"MPUP": 1, "CHARGE": 2, "RANGE_H": 10, "RANGE_V": 11, "RANGE_S": 12, "RANGE_B": 13}
rank_power_dict = {"RANK_1":2,"RANK_2":2.2,"RANK_3":2.4,"RANK_4":2.6,"RANK_5":3}
# (HP, ATK, DEF)
grow_diff = {"BALANCE": (1,1,1), "ATTACK": (0.98, 1.03, 0.97), "DEFENSE": (0.97, 0.98, 1.05), "HP": (1.04, 0.97, 0.98), "ATKDEF": (0.99, 1.02, 1.01), "ATKHP": (1.02, 1.01, 0.99), "DEFHP": (1.01, 0.99, 1.02)}
ATTRIBUTE = {"FIRE":"{{属性|火}}","WATER":"{{属性|水}}","TIMBER":"{{属性|木}}","LIGHT":"{{属性|光}}","DARK":"{{属性|暗}}","VOID":"{{属性|无}}"}
CHARA_NAME = {1001: "环伊吕波",1002: "七海八千代",1003: "由比鹤乃",1004: "二叶莎奈",1005: "深月菲莉希亚",1006: "梓美冬",1007: "里见灯花",1008: "阿莉娜·格雷",1009: "水波玲奈",1010: "十咎桃子",1011: "秋野枫",1012: "御园花凛",1013: "龙城明日香",1014: "柊音梦",1015: "环忧",1016: "和泉十七夜",1017: "八云御魂",1018: "天音月夜",1019: "天音月咲",1022: "煌里光",1023: "笠音青",1024: "大庭树里",1025: "时女静香",1026: "广江千春",1027: "土岐沙绪",1029: "宫尾时雨",1030: "安积育梦",1038: "八云御影",1039: "佐和月出里",1040: "篠目夜鹤",1041: "莉薇娅·梅黛洛斯",1042: "小丘比",1101: "环伊吕波（泳装ver.）",1102: "八千代·美冬（起始ver.）",1103: "谣鹤乃",1104: "谣莎奈",1105: "小菲莉希亚",1107: "灯花·音梦（圣夜ver.）",1108: "圣阿莉娜",1109: "小玲奈（偶像ver.）",1110: "十咎桃子（修女ver.）",1116: "和泉十七夜（吸血鬼ver.）",1117: "八云御魂（晴着ver.）",1118: "天音姐妹（泳装ver.）",1201: "小伊吕波",1203: "鹤乃·菲莉希亚（快递ver.）",1209: "玲奈·枫（泳装ver.）",1301: "伊吕波·八千代（决战ver.）",1401: "伊吕波·忧（巫女ver.）",2001: "鹿目圆",2002: "晓美焰",2003: "晓美焰（眼镜ver.）",2004: "美树沙耶香",2005: "巴麻美",2006: "佐仓杏子",2007: "百江渚",2100: "鹿目圆（晴着ver.）",2101: "圆神",2102: "小圆前辈",2300: "晓美焰（泳装ver.）",2400: "美树沙耶香（晴着ver.）",2500: "圣麻美",2501: "巴麻美（泳装ver.）",2600: "佐仓杏子（泳装ver.）",2700: "百江渚（情人节ver.）",3001: "矢宵鹿乃子",3002: "空穗夏希",3003: "都雏乃",3004: "美凪纱纱罗",3005: "常盘七夏",3006: "木崎衣美里",3007: "保澄雫",3008: "志伸晶",3009: "胡桃爱香",3010: "阿见莉爱",3011: "夏目佳子",3012: "纯美雨",3013: "伊吹丽良",3014: "桑水清佳",3015: "相野未都",3016: "粟根心",3017: "七濑幸佳",3018: "更纱帆奈",3019: "毬子彩花",3020: "真尾日美香",3021: "铃鹿朔夜",3023: "江利爱实",3024: "若菜纺",3025: "五十铃怜",3026: "静海木叶",3027: "游佐叶月",3028: "三栗菖蒲",3029: "加贺见真良",3030: "春名木乃美",3031: "绫野梨花",3032: "梢麻友",3033: "史乃沙优希",3034: "惠萌花",3035: "千秋理子",3036: "由贵真里爱",3037: "安名梅露",3038: "古町美仓",3039: "三穗野星罗",3040: "吉良手鞠",3041: "柚希步鸟",3042: "枇枇木巡",3043: "万年樱之谣",3044: "智珠兰华",3045: "柚希理音",3046: "观鸟令",3047: "青叶知花",3049: "雪野加奈惠",3050: "香春优奈",3051: "饰利润",3052: "阿什莉·泰勒",3053: "牧野郁美",3056: "水树垒",3058: "南津凉子",3501: "梨花·怜（圣诞ver.）",3502: "万年樱之谣（泳装ver.）",3900: "黑",4001: "美国织莉子",4002: "吴纪里香",4003: "千岁由麻",4011: "和美",4012: "御崎海香",4013: "牧薰",4021: "塔鲁特",4022: "莉兹",4023: "梅丽莎",4025: "可鲁波",4026: "爱丽莎",4027: "拉皮努",4028: "塔鲁特（ver.Final）",4031: "天乃铃音",4032: "日向茉莉",4033: "成见亚里纱",4034: "诗音千里",4035: "奏遥香",4036:"美琴椿", 4041: "战场原黑仪",4042: "八九寺真宵",4043: "神原骏河",4044: "千石抚子",4045: "羽川翼",4046: "忍野忍",4051: "高町奈叶",4052: "菲特",4053: "八神疾风"}
CHARGE_DMG_DICT = {1: {0: 1, 1: 1.1, 2: 1.2}, 2: {0: 1, 1: 1.4, 2: 1.7}, 3:{0: 1, 1: 1, 2: 1}}
'''[盘][位置][是否首A]'''
DISC_MP_DICT = {1:{0: {0: 7, 1: 10}, 1: {0: 10.5, 1: 13.5}, 2: {0: 14, 1: 17}}, 2:{0: {0: 0, 1: 0}, 1: {0: 0, 1: 3}, 2:{0: 0, 1: 3}}, 3: {0: {0: 2, 1: 2}, 1: {0: 3, 1: 6}, 2: {0: 4, 1: 7}}}
MAX_SINGLE_DMG = 9999999
MAX_MP = 150

def convert_to_dict(obj):
    '''把Object对象转换成Dict对象'''
    dict = {}
    dict.update(obj.__dict__)
    return dict

def get_from_dict(d_ict, key, default=None):
    '''从dict中根据key取值，取不到返回default'''
    if key not in d_ict:
        return default
    return d_ict[key]

class CharaData(object):
    '''烧酒数据'''
    def __init__(self):
        super()
        self.max_hp = 0
        self.max_atk = 0
        self.max_def = 0
        self.rank = 0
        self.element = ""
        self.discs = []
        self.is_void = False
        self.accele_disc = 0
        self.blast_disc = 0
        self.charge_disc = 0
        self.same_3b = False
        self.connect = []
        self.magia = []
        self.doppel = []
        self.enhance_art = []
        self.atk_mp = 0
        self.def_mp = 0
        self.accele_dmgup = 0
        self.blast_dmgup = 0
        self.charge_dmgup = 0

def all_check(id):
    '''输出所有效果类型'''
    data = read_from_chara_id(id)
    all_art = []
    all_art.extend(data.connect)
    all_art.extend(data.magia)
    all_art.extend(data.doppel)
    all_art.extend(data.enhance_art)
    all_data = set()
    for art in all_art:
        verb_code = get_from_dict(art, "verbCode")
        eff = get_from_dict(art, "effectCode")
        all_data.add("%s-%s"%(verb_code, eff))
    return all_data

def get_most_dmg_disc(disc_list):
    '''根据给定的发牌，得到最大伤害的出牌'''
    if len(disc_list) < 3:
        print("不够盘！")
        return []
    disc_count = [0, 0, 0, 0]
    for disc in disc_list:
        disc_count[disc] += 1
    # BBB
    if disc_count[2] >= 3:
        return [2, 2, 2]
    if disc_count[3] >= 2:
        # CCB
        if disc_count[2] > 0:
            return [3, 3, 2]
        # CCA
        if disc_count[1] > 0:
            return [3, 3, 1]
        # CCC
        return [3, 3, 3]
    if disc_count[3] == 1:
        # CBB
        if disc_count[2] > 1:
            return [3, 2, 2]
        # ACB
        if disc_count[2] == 1:
            return [1, 3, 2]
    # ABB
    if disc_count[2] == 2:
        return [1, 2, 2]
    # AAB
    if disc_count[2] == 1:
        return [1, 1, 2]
    if disc_count[3] == 1:
        return [1, 3, 1]
    # AAA
    return [1, 1, 1]
    
def get_most_mp_disc(disc_list):
    '''根据给定的发牌，得到最大MP的出牌'''
    if len(disc_list) < 3:
        print("不够盘！")
        return []
    disc_count = [0, 0, 0, 0]
    for disc in disc_list:
        disc_count[disc] += 1
    # AAA
    if disc_count[1] == 3:
        return [1, 1, 1]
    if disc_count[1] == 2:
        # ACA
        if disc_count[3] > 0:
            return [1, 3, 1]
        # ABA
        if disc_count[2] > 0:
            return [1, 2, 1]
    if disc_count[1] == 1:
        # CCA
        if disc_count[3] > 1:
            return [3, 3, 1]
        # ABB
        if disc_count[3] == 0 and disc_count[2] > 1:
            return [1, 2, 2]
        # ACB
        return [1, 3, 2]
    # CCC
    if disc_count[3] > 2:
        return [3, 3, 3]
    # CCB
    if disc_count[3] > 1:
        return [3, 3, 2]
    # CBB
    if disc_count[3] > 0:
        return [3, 2, 2]
    # BBB
    return [2, 2, 2]

def disclist_to_key(disc_list):
    '''将出牌list转成key'''
    if len(disc_list) != 3:
        print("盘型不对！：", disc_list)
        return 0
    return disc_list[0] * 100 + disc_list[1] * 10 + disc_list[2]

def key_to_disclist(key):
    '''将key转成出牌list'''
    first = key // 100
    key -= first * 100
    second = key // 10
    key -= second * 10
    return [first, second, key]

def get_best_disc_list(data : CharaData, get_mp=False):
    '''获得烧酒的各种发牌情况下三连的最大伤害/最大MP出牌类型'''
    cache_idx = data.accele_disc * 100 + data.blast_disc * 10 + data.charge_disc * 1
    if cache_idx in BEST_DISC_CACHE:
        return BEST_DISC_CACHE[cache_idx]
    all_disc = []
    accele_disc = [1] * data.accele_disc
    blast_disc = [2] * data.blast_disc
    charge_disc = [3] * data.charge_disc
    all_disc.extend(accele_disc)
    all_disc.extend(blast_disc)
    all_disc.extend(charge_disc)
    func = get_most_dmg_disc
    if get_mp:
        func = get_most_mp_disc

    result = {}
    # 5选3
    five_best_key = disclist_to_key(func(all_disc))
    result[five_best_key] = 1
    # 4选3
    for remove_idx in range(0, 5):
        four_disc = all_disc.copy()
        del four_disc[remove_idx]
        key = disclist_to_key(func(four_disc))
        if key not in result:
            result[key] = 0
        result[key] += 1
    # 3选3
    for first_idx in range(0, 3):
        for second_idx in range(first_idx + 1, 4):
            for third_idx in range(second_idx + 1, 5):
                three_disc = [all_disc[first_idx], all_disc[second_idx], all_disc[third_idx]]
                key = disclist_to_key(func(three_disc))
                if key not in result:
                    result[key] = 0
                result[key] += 1
    return result

def read_from_chara_id(id):
    '''根据ID获得烧酒数据'''
    global allchara_file
    if get_from_dict(CHARA_DICT, id) is not None:
        return get_from_dict(CHARA_DICT, id)
    result = CharaData()
    id_key = "%d"%id
    if id_key not in allchara_file:
        print("%d不在数据中！"%id)
        return result
    data = allchara_file[id_key]
    for evo_idx in range(5, 0, -1):
        evo_key = "evolutionCard%d"%evo_idx
        if evo_key in data or evo_idx == 1:
            if evo_key not in data:
                max_data = data["defaultCard"]
            else:
                max_data = data[evo_key]
            result.element = get_from_dict(max_data,"attributeId")
            result.is_void = get_from_dict(max_data,"attributeId") == "VOID"
            result.rank = int(max_data["rank"][-1])
            result.atk_mp = get_from_dict(max_data, "rateGainMpAtk") / 1000
            result.def_mp = get_from_dict(max_data, "rateGainMpDef") / 1000
            grow_df = grow_diff[max_data["growthType"]]
            result.max_hp = max_data["hp"] + max_data["hp"] * grow_df[0] * rank_power_dict[max_data["rank"]]
            result.max_atk = max_data["attack"] + max_data["attack"] * grow_df[1] * rank_power_dict[max_data["rank"]]
            result.max_def = max_data["defense"] + max_data["defense"] * grow_df[2] * rank_power_dict[max_data["rank"]]
            # 盘
            last_blast = None
            for disc_idx in range(1, 10):
                disc_key = "commandType%d"%disc_idx
                if disc_key not in max_data:
                    break
                disc_num = disc_num_dict[max_data[disc_key]]
                if disc_num == 1:
                    result.accele_disc += 1
                elif disc_num == 2:
                    result.charge_disc += 1
                else:
                    result.blast_disc += 1
                    if last_blast is None:
                        last_blast = disc_num
                    elif last_blast != disc_num:
                        last_blast = 999
                result.discs.append(disc_num)
            if result.blast_disc >= 3 and (last_blast is not None and last_blast != 999):
                result.same_3b = True
            
            # connect
            if "cardSkill" in max_data:
                connect_data = max_data["cardSkill"]
                for art_idx in range(1, 10):
                    art_key = "art%d"%art_idx
                    if art_key not in connect_data:
                        break
                    result.connect.append(connect_data[art_key])
            
            # Magia
            if "cardMagia" in max_data:
                magia_data = max_data["cardMagia"]
                for art_idx in range(1, 10):
                    art_key = "art%d"%art_idx
                    if art_key not in magia_data:
                        break
                    art = magia_data[art_key]
                    if "growPoint" in art and "effectValue" in art:
                        art["effectValue"] += art["growPoint"] * 4
                    result.magia.append(art)
            
            # Doppel
            if "doppelCardMagia" in max_data:
                doppel_data = max_data["doppelCardMagia"]
                for art_idx in range(1, 10):
                    art_key = "art%d"%art_idx
                    if art_key not in doppel_data:
                        break
                    art = doppel_data[art_key]
                    if "growPoint" in art and "effectValue" in art:
                        art["effectValue"] += art["growPoint"] * 4
                    result.doppel.append(art)
            
            # EX
            if "maxPieceSkillList" in max_data:
                ex_data_list = max_data["maxPieceSkillList"]
                for ex_data in ex_data_list:
                    for art_idx in range(1, 10):
                        art_key = "art%d"%art_idx
                        if art_key not in ex_data:
                            break
                        result.enhance_art.append(ex_data[art_key])
            
            # 觉醒
            if "cardCustomize" in max_data:
                awaken_data = max_data["cardCustomize"]
                for awaken_idx in range(1, 10):
                    code_key = "bonusCode%d"%awaken_idx
                    num_key = "bonusNum%d"%awaken_idx
                    if code_key not in awaken_data or num_key not in awaken_data:
                        continue
                    if awaken_data[code_key] == "HP":
                        result.max_hp *= (1 + awaken_data[num_key] / 1000)
                    if awaken_data[code_key] == "ATTACK":
                        result.max_atk *= (1 + awaken_data[num_key] / 1000)
                    if awaken_data[code_key] == "DEFENSE":
                        result.max_def *= (1 + awaken_data[num_key] / 1000)
                    if awaken_data[code_key] == "ACCELE":
                        result.accele_dmgup += awaken_data[num_key] / 10
                    if awaken_data[code_key] == "BLAST":
                        result.blast_dmgup += awaken_data[num_key] / 10
                    if awaken_data[code_key] == "CHARGE":
                        result.charge_dmgup += awaken_data[num_key] / 10
            break

    # 精神强化
    if "enhancementCellList" in data:
        enhance_hp = 0
        enhance_atk = 0
        enhance_def = 0
        enhance_list = data["enhancementCellList"]
        for enhance_cell in enhance_list:
            if enhance_cell["enhancementType"] == "HP":
                enhance_hp += enhance_cell["effectValue"]
            elif enhance_cell["enhancementType"] == "ATTACK":
                enhance_atk += enhance_cell["effectValue"]
            elif enhance_cell["enhancementType"] == "DEFENSE":
                enhance_def += enhance_cell["effectValue"]
            elif enhance_cell["enhancementType"] == "DISK_ACCELE":
                result.accele_dmgup += enhance_cell["effectValue"] / 10
            elif enhance_cell["enhancementType"] == "DISK_BLAST":
                result.blast_dmgup += enhance_cell["effectValue"] / 10
            elif enhance_cell["enhancementType"] == "DISK_CHARGE":
                result.charge_dmgup += enhance_cell["effectValue"] / 10
            elif enhance_cell["enhancementType"] == "SKILL":
                enhance_skill = enhance_cell["emotionSkill"]
                cd_turn = get_from_dict(enhance_skill, "intervalTurn", 0)
                for art_idx in range(1, 10):
                    art_key = "art%d"%art_idx
                    if art_key not in enhance_skill:
                        break
                    if cd_turn > 0:
                        enhance_skill[art_key]["intervalTurn"] = cd_turn
                    result.enhance_art.append(enhance_skill[art_key])
        if id in SE_SUM:
            enhance_hp = SE_SUM[id][0]
            enhance_atk = SE_SUM[id][1]
            enhance_def = SE_SUM[id][2]
        result.max_hp += enhance_hp * 0.6
        result.max_atk += enhance_atk * 0.6
        result.max_def += enhance_def * 0.6

    # 记忆
    if id in MEMO_INCLUDE:
        memo = allmemo_file["%d"%MEMO_INCLUDE[id]]
        for mlb_idx in range(5, 0, -1):
            mlb_key = "pieceSkill%d"%mlb_idx
            if mlb_key not in memo:
                continue
            mlb_data = memo[mlb_key]
            for art_idx in range(1, 10):
                art_key = "art%d"%art_idx
                if art_key not in mlb_data:
                    break
                result.enhance_art.append(mlb_data[art_key])
            break

    CHARA_DICT[id] = result
    return result

def get_score(id):
    '''总评分'''
    d = read_from_chara_id(id)

    # d_json = json.dumps(convert_to_dict(d))
    # print(d_json)

    # 基础分数
    d_total_power = (d.max_hp + d.max_atk + d.max_def / 3)
    # 周回
    d_loop_power = get_loop_score(d)
    # 镜层 TODO
    d_mirror_power = 0
    # 辅助
    d_support_power = get_support_score(d)
    # 高难普攻
    d_oneturn_dmg = get_normal_damage(d, False, True)
    d_normal_dmg = get_normal_damage(d, False)
    d_normal_dmg_duo = get_normal_damage(d, True)
    d_normal_dmg_avg = d_oneturn_dmg * 0.4 + d_normal_dmg * 0.2 + d_normal_dmg_duo * 0.4
    d_normal_dmg_diff = d_normal_dmg_duo - d_normal_dmg
    # 高难Magia
    d_magia_power = get_magia_score(d)
    # 心魔输出
    d_kimochi_dmg_list = get_kimochi_score(d)
    # 功能性
    d_func = get_function_score(d)

    result_str = "%d\t%s\t%d\t%s\t\
%.2f\t%.2f\t%.2f\t%.2f\t\
%.2f\t%.2f\t%.2f\t\
%.2f%%\t%.2f\t%.2f\t\
%.2f\t%.2f\t%.2f\t\
%.2f\t%.2f\t%.2f\t\
%.2f"%(
        id, get_from_dict(CHARA_NAME, id), d.rank, ATTRIBUTE[d.element], 
        d_total_power, d_loop_power, d_mirror_power, d_support_power, 
        d_oneturn_dmg, d_normal_dmg, d_normal_dmg_diff,
        d_normal_dmg_diff * 100 / d_normal_dmg, d_normal_dmg_duo, d_normal_dmg_avg,
        d_magia_power[0], d_magia_power[1], d_magia_power[2], 
        d_kimochi_dmg_list[0], d_kimochi_dmg_list[1], d_kimochi_dmg_list[2],
        d_func)
    print(result_str)

def get_loop_score(data : CharaData):
    '''周回评分'''
    base_score = data.blast_disc
    if base_score >= 3 and data.same_3b:
        base_score += 0.5
    return base_score

SUPPORT_SCORE_LIST = {
    "BUFF" : {
        # Accele MPUP
        "ACCEL"         : 0.0015,
        # Blast UP
        "BLAST"         : 0.001,
        # Charge UP
        "CHARGE"        : 0.00075,
        # Charge盘UP
        "CHARGING"      : 0.0005,
        # MP获得量UP
        "MP_GAIN"       : 0.00125,
        # ATTACK UP
        "ATTACK"        : 0.005,
        "ATTACK_FIRE"   : 0.005,
        "ATTACK_WATER"  : 0.005,
        "ATTACK_TIMBER" : 0.005,
        "ATTACK_LIGHT"  : 0.005,
        "ATTACK_DARK"   : 0.005,
        "ATTACK_VOID"   : 0.005,
        # 伤害UP
        "DAMAGE"        : 0.005,
        # Magia UP
        "MAGIA"         : 0.002,
        # DEF UP
        "DEFENSE"       : 0.001,
        # 耐性 UP
        "RESIST"        : 0.0001
    },
    "CONDITION_GOOD" : {
        # 伤害UP
        "DAMAGE_UP"            : 0.005,
        # 异常状态伤害UP
        "DAMAGE_UP_BAD"        : 0.00025,
        # 伤害削减
        "DAMAGE_DOWN"          : 0.001,
        "DAMAGE_DOWN_FIRE"     : 0.0001,
        "DAMAGE_DOWN_WATER"    : 0.0001,
        "DAMAGE_DOWN_TIMBER"   : 0.0001,
        "DAMAGE_DOWN_LIGHT"    : 0.0001,
        "DAMAGE_DOWN_DARK"     : 0.0001,
        "DAMAGE_DOWN_VOID"     : 0.0001,
        "DAMAGE_DOWN_NODISK"   : 0.0001,
        "DAMAGE_DOWN_ACCEL"    : 0.0001,
        "DAMAGE_DOWN_BLAST"    : 0.0001,
        "DAMAGE_DOWN_CHARGE"   : 0.0001,
        "DAMAGE_DOWN_CHARGING" : 0.0001,
        # 自动回复
        "AUTO_HEAL"            : 0.0025
    },
    "REVOKE" : {
        # Debuff解除
        "DEBUFF" : 0.1,
        # 异常状态解除
        "BAD"    : 0.1
    },
    "HEAL" : {
        # 回复HP
        "HP" : 0.0075,
        # 回复MP
        "MP" : 0.03
    },
    "RESURRECT" : {
        # 苏生
        "None" : 0.02
    }
}

def get_support_score(data: CharaData):
    '''辅助评分'''
    all_art = []
    all_art.extend(data.connect)
    all_art.extend(data.magia)
    all_art.extend(data.enhance_art)
    def get_support_score_from_list(art_list):
        base_score = 0
        for art in art_list:
            target_count = 0
            target_id = get_from_dict(art, "targetId")
            if target_id == "ALL":
                target_count = 2.5
            elif target_id in ["CONNECT", "TARGET", "ONE"]:
                target_count = 1
            else:
                continue

            enable_turn = 1
            if get_from_dict(art, "enableTurn") == 0:
                enable_turn = 3.5
            elif "enableTurn" in art:
                enable_turn = art["enableTurn"]
                if enable_turn > 3:
                    enable_turn = 3.5

            power = 0
            verbCode = get_from_dict(art, "verbCode", "None")
            effectCode = get_from_dict(art, "effectCode", "None")
            power = get_from_dict(
                get_from_dict(SUPPORT_SCORE_LIST, verbCode, {}),
                effectCode,
                0
            )

            if verbCode == "CONDITION_GOOD" and effectCode == "AUTO_HEAL" and get_from_dict(art, "genericValue") == "MP":
                power = 0.015

            effectValue = get_from_dict(art, "effectValue")
            if effectValue is None:
                effectValue = 10
            poss = get_from_dict(art, "probability")
            if poss is not None:
                effectValue *= poss / 1000
            
            art_score = target_count * enable_turn * power * effectValue / 10
            base_score += art_score
            if art_score > 0 and DEBUG:
                print(art)
                print(target_count, enable_turn, power, effectValue, art_score)
        return base_score
    total_score = get_support_score_from_list(data.enhance_art) * 4
    total_score += get_support_score_from_list(data.connect) * 3
    total_score += get_support_score_from_list(data.magia) * 2
    total_score += get_support_score_from_list(data.doppel)
    return total_score

def get_normal_damage(data: CharaData, use_connect : bool, ignore_enableTurn=False):
    '''通常伤害评分'''

    all_poss_disc = get_best_disc_list(data)
    disc_divide = sum(all_poss_disc.values())
    
    base_atk = data.max_atk
    disc_dmg_stat = [1, 1 + data.accele_dmgup / 100, 1 + data.blast_dmgup / 100, 1 + data.charge_dmgup / 100]
    blastup_stat = 0
    chargingup_stat = 0
    chargeup_stat = 0
    atkup_stat = 0
    dmgup_stat = 1
    critical_poss = 0
    ignore_def_poss = 0
    use_art = data.enhance_art.copy()
    if use_connect:
        connect_art = data.connect.copy()
        for art in connect_art:
            art.pop("enableTurn", 0)
        use_art.extend(connect_art)
    for art in use_art:
        # 不算有回合限制的效果
        if (not ignore_enableTurn) and "enableTurn" in art and art["enableTurn"] < 5:
            continue
        if "limitedValue" in art:
            continue
        verbCode = get_from_dict(art, "verbCode")
        effectCode = get_from_dict(art, "effectCode")
        effectValue = get_from_dict(art, "effectValue")
        poss = get_from_dict(art, "probability")
        
        if verbCode == "BUFF":
            # BlastUP
            if effectCode == "BLAST":
                blastup_stat += effectValue / 1000
            # Charge盘UP
            elif effectCode == "CHARGING":
                chargingup_stat += effectValue / 1000
            # Charge后伤害UP
            elif effectCode == "CHARGE":
                chargeup_stat += effectValue
            # ATKUP
            elif effectCode == "ATTACK":
                atkup_stat += effectValue
            # 伤害UP
            elif effectCode == "DAMAGE":
                dmgup_stat += effectValue / 1000
        if verbCode == "CONDITION_GOOD":
            # 伤害UP
            if effectCode == "DAMAGE":
                dmgup_stat += effectValue / 1000
            # 概率暴击
            elif effectCode == "CRITICAL":
                critical_poss = max(critical_poss, poss / 1000)
            # 概率无视防御
            elif effectCode == "DEFENSE_IGNORED":
                ignore_def_poss = max(ignore_def_poss, poss / 1000)
    blastup_stat = min(1, blastup_stat)
    chargeup_stat = min(2, 1 + chargeup_stat / 1000)
    atkup_stat = min(2, 1 + atkup_stat / 1000)
    base_atk *= atkup_stat
    # 模拟打6kDEF
    base_dmg = (base_atk - 2000) * (1 - ignore_def_poss) + base_atk * ignore_def_poss
    average_dmg = 0
    def get_dmg_from_disc(use_disc):
        total_dmg = 0
        current_charging = 0
        for disc_idx in range(0, 3):
            disc = use_disc[disc_idx]
            # 基本盘型系数
            base_disc_factor = 1.2
            if disc == 2:
                base_disc_factor = 0.9
            # 盘型加成
            disc_factor = disc_dmg_stat[disc]
            # 克制系数，默认打克制
            element_plus = 2
            if data.is_void:
                element_plus = 1
            # B系数
            blast_disc_place = 1
            if disc == 2:
                blast_disc_place += disc_idx * 0.1
            # C系数
            charge_plus = CHARGE_DMG_DICT[disc][current_charging]
            if disc != 3:
                charge_plus = min(5.5, charge_plus * chargeup_stat) 
            # 伤害系数
            base_dmg_factor = dmgup_stat
            if disc == 2:
                base_dmg_factor += blastup_stat
            if disc == 3:
                base_dmg_factor += chargingup_stat
            base_dmg_factor = min(3, base_dmg_factor)
            # 暴击
            base_dmg_factor = base_dmg_factor * (1 - critical_poss) + (base_dmg_factor + 1) * critical_poss
            dmg = base_dmg * base_disc_factor * disc_factor * element_plus * blast_disc_place * charge_plus * base_dmg_factor
            if disc == 3:
                current_charging += 1
            else:
                current_charging = 0
            if disc == 2:
                dmg *= 2
            total_dmg += dmg
            
        return total_dmg
    for disc_key in all_poss_disc.keys():
        disc_list = key_to_disclist(disc_key)
        dmg = get_dmg_from_disc(disc_list)
        dmg *= all_poss_disc[disc_key] / disc_divide
        average_dmg += dmg
    return average_dmg

def get_magia_score(data : CharaData):
    base_atk = data.max_atk
    magia_factor = 0
    magia_range = ""
    atkup_stat = 1
    element_atkup_stat = 0
    element_weak_stat = 1
    dmg_stat = 1
    accele_mp_stat = 1
    mp_gain_stat = 1
    mp_gain_hit_stat = 1
    init_mp = 0
    gain_mp = 0
    magia_stat = 1
    blast_mp = 0
    use_art = data.enhance_art.copy()
    use_art.extend(data.magia)
    for art in use_art:
        verbCode = get_from_dict(art, "verbCode")
        effectCode = get_from_dict(art, "effectCode")
        effectValue = get_from_dict(art, "effectValue")
        if verbCode == "ATTACK" and effectCode != "DUMMY":
            magia_range = get_from_dict(art, "targetId")
            magia_factor = get_from_dict(art, "effectValue") / 1000
            if not data.is_void:
                magia_factor *= 1.5
            if effectCode == "ALIGNMENT":
                magia_factor *= 2
        if verbCode == "BUFF":
            # Accele MPUP
            if effectCode == "ACCEL":
                accele_mp_stat += effectValue / 1000
            # MPUP
            if effectCode == "MP_GAIN":
                mp_gain_stat += effectValue / 1000
            # ATKUP
            if effectCode == "ATTACK":
                atkup_stat += effectValue / 1000
            # 伤害UP
            if effectCode == "DAMAGE":
                dmg_stat += effectValue / 1000
            # Magia UP
            if effectCode == "MAGIA":
                magia_stat += effectValue / 1000
        if verbCode == "CONDITION_GOOD":
            # 伤害UP
            if effectCode == "DAMAGE":
                dmg_stat += effectValue / 1000
            # 被攻击时MPUP
            if effectCode == "MP_PLUS_DAMAGED":
                mp_gain_hit_stat += effectValue / 10
            # 被弱点属性攻击时MPUP
            if effectCode == "MP_PLUS_WEAKED" and not data.is_void:
                mp_gain_hit_stat += effectValue / 10
            # Blast MP
            if effectCode == "MP_PLUS_BLAST":
                blast_mp += effectValue / 10
        # 属性增伤
        if verbCode == "DEBUFF" and effectCode in ["WEAK_FIRE", "WEAK_WATER", "WEAK_TIMBER", "WEAK_LIGHT", "WEAK_DARK", "WEAK_VOID"]:
            effectValue = get_from_dict(art, "effectValue") / 1000
            element_weak_stat += effectValue
        # 属性ATK
        if verbCode == "BUFF" and effectCode in ["ATTACK_FIRE", "ATTACK_WATER", "ATTACK_TIMBER", "ATTACK_LIGHT", "ATTACK_DARK", "ATTACK_VOID"]:
            effectValue = get_from_dict(art, "effectValue") / 1000
            element_atkup_stat += effectValue
        # MP回复
        if verbCode == "HEAL" and effectCode == "MP":
            effectValue = get_from_dict(art, "effectValue") / 10
            gain_mp += effectValue
        # MP自回
        if verbCode == "CONDITION_GOOD" and effectCode == "AUTO_HEAL" and get_from_dict(art, "genericValue") == "MP":
            effectValue = get_from_dict(art, "effectValue") / 10
            poss = get_from_dict(art, "probability", 1000) / 1000
            gain_mp += effectValue * poss
        # 初始MP
        if verbCode == "INITIAL" and effectCode == "MP":
            effectValue = get_from_dict(art, "effectValue") / 1000 * MAX_MP
            init_mp += effectValue
    
    init_mp += gain_mp * mp_gain_stat

    all_poss_disc = get_best_disc_list(data, True)
    disc_divide = sum(all_poss_disc.values())

    # 攻击MP
    for disc_key in all_poss_disc.keys():
        disc_list = key_to_disclist(disc_key)
        current_mp = 0
        current_charge = 0
        first_a = 0
        if disc_list[0] == 1:
            first_a = 1
        if disc_key == 111:
            current_mp = 20
        for disc_idx in range(0, 3):
            disc = disc_list[disc_idx]
            disc_mp = DISC_MP_DICT[disc][disc_idx][first_a]
            if disc == 1:
                # Charge MP
                disc_mp *= (1 + 0.3 * current_charge)
                # Accele MPUP
                disc_mp *= accele_mp_stat
            if disc == 2:
                # Blast MP
                disc_mp += blast_mp * 2
            # MPUP
            disc_mp *= mp_gain_stat
            # 攻击修正
            disc_mp *= data.atk_mp
            if disc == 3:
                current_charge += 1
            else:
                current_charge = 0
            current_mp += int(disc_mp * 10) / 10
        current_mp *= all_poss_disc[disc_key] / disc_divide
        init_mp += current_mp

    # 受击MP
    hit_mp = int((4 * data.def_mp + mp_gain_hit_stat) * mp_gain_stat * 30) / 10
    init_mp += hit_mp

    magia_dmg = 0
    magia_count = 0
    single_point_dmg = min(MAX_SINGLE_DMG, base_atk * (min(3, atkup_stat) + element_atkup_stat) * magia_factor * min(3, dmg_stat) * magia_stat * element_weak_stat)
    # 随机伤害
    if magia_range[0:6] == "RANDOM":
        magia_count = int(magia_range[-1])
    else:
        # 范围伤害
        magia_count = 1
        if magia_range in ["HORIZONTAL", "VERTICAL"]:
            magia_count = 3
        elif magia_range == "ALL":
            magia_count = 5
    magia_dmg = single_point_dmg * magia_count
    magia_log = 1
    if magia_dmg > 0:
        magia_log = math.log(magia_dmg, 10)
    return (magia_dmg, init_mp, magia_log * (init_mp / MAX_MP))

def get_kimochi_score(data: CharaData):
    '''心魔评分'''
    total_dmg = 0

    base_atk = data.max_atk
    doppel_factor = 0
    doppel_range = ""
    magia_up = 1
    mp_gain = 0
    mp_rate = 1
    atk_up = 2
    element_atk_up = 0
    element_weak = 1
    dmg_up = 2
    dmg_up_weak = 0

    dmg_art_list = data.doppel
    if data.doppel == []:
        dmg_art_list = data.magia
    # 计算Magia/Doppel效果
    for dmg_art in dmg_art_list:
        verbCode = get_from_dict(dmg_art, "verbCode")
        effectCode = get_from_dict(dmg_art, "effectCode")
        # 伤害
        if verbCode == "ATTACK" and effectCode != "DUMMY":
            doppel_range = get_from_dict(dmg_art, "targetId")
            doppel_factor = get_from_dict(dmg_art, "effectValue") / 1000
            if not data.is_void:
                doppel_factor *= 1.5
                # 属性强化
                if effectCode == "ALIGNMENT":
                    doppel_factor *= 2
        # MP自回
        if verbCode == "CONDITION_GOOD" and effectCode == "AUTO_HEAL":
            if get_from_dict(dmg_art, "genericValue") == "MP":
                mp_value = get_from_dict(dmg_art, "effectValue") / 10
                mp_value *= get_from_dict(dmg_art, "enableTurn")
                mp_value *= get_from_dict(dmg_art, "probability") / 1000
                mp_gain += mp_value
        # MP速回
        if verbCode == "HEAL" and effectCode == "MP":
            mp_value = get_from_dict(dmg_art, "effectValue") / 10
            mp_gain += mp_value
    for art in data.enhance_art:
        verbCode = get_from_dict(art, "verbCode")
        effectCode = get_from_dict(art, "effectCode")
        # MP自回
        if verbCode == "CONDITION_GOOD" and effectCode == "AUTO_HEAL":
            if get_from_dict(art, "genericValue") == "MP":
                mp_value = get_from_dict(art, "effectValue") / 10
                enable_turn = get_from_dict(art, "enableTurn")
                if enable_turn is None:
                    enable_turn = 4
                mp_value *= enable_turn
                mp_value *= get_from_dict(art, "probability") / 1000
                mp_gain += mp_value
        # MP速回
        if verbCode == "HEAL" and effectCode == "MP":
            mp_value = get_from_dict(art, "effectValue") / 10
            mp_gain += mp_value
        # MP获得量UP
        if verbCode == "BUFF" and effectCode == "MP_GAIN":
            mp_rate += get_from_dict(art, "effectValue") / 1000
        # Magia UP
        if verbCode == "BUFF" and effectCode == "MAGIA":
            magia_up += get_from_dict(art, "effectValue") / 1000
        # 增伤
        if verbCode == "CONDITION_GOOD" and effectCode == "DAMAGE_UP":
            dmg_up += get_from_dict(art, "effectValue") / 1000
        # 异常增伤
        if verbCode == "CONDITION_GOOD" and effectCode == "DAMAGE_UP_BAD":
            dmg_up_weak += get_from_dict(art, "effectValue") / 1000
        # 属性增伤
        if verbCode == "DEBUFF" and effectCode in ["WEAK_FIRE", "WEAK_WATER", "WEAK_TIMBER", "WEAK_LIGHT", "WEAK_DARK", "WEAK_VOID"]:
            effectValue = get_from_dict(art, "effectValue") / 1000
            element_weak += effectValue
        # 属性ATK
        if verbCode == "BUFF" and effectCode in ["ATTACK_FIRE", "ATTACK_WATER", "ATTACK_TIMBER", "ATTACK_LIGHT", "ATTACK_DARK", "ATTACK_VOID"]:
            effectValue = get_from_dict(art, "effectValue") / 1000
            element_atk_up += effectValue

    mp_gain *= mp_rate
    magia_up = min(2, magia_up)

    # 随机伤害
    if doppel_range[0:6] == "RANDOM":
        random_times = int(doppel_range[-1])
        doppel_dmg_up_weak = min(3, dmg_up + dmg_up_weak)
        doppel_factor_weak = doppel_factor
        if not data.is_void:
            doppel_factor_weak *= 1.2
        single_point_dmg = min(MAX_SINGLE_DMG, base_atk * min(3, atk_up + element_atk_up) * doppel_factor * dmg_up * magia_up * element_weak)
        single_point_dmg_weak = min(MAX_SINGLE_DMG, base_atk * min(3, atk_up + element_atk_up) * doppel_factor_weak * doppel_dmg_up_weak * magia_up * element_weak)
        single_dmg = single_point_dmg * 0.8 + single_point_dmg_weak * 0.2
        total_dmg = single_dmg * random_times
    else:
        # 范围伤害
        dmg_point_count = 1
        if doppel_range in ["HORIZONTAL", "VERTICAL"]:
            dmg_point_count = 3
        elif doppel_range == "ALL":
            dmg_point_count = 5
        
        # 异常点伤害
        bad_doppel_factor = doppel_factor
        if not data.is_void:
            bad_doppel_factor *= 1.2
        bad_point_dmg = min(MAX_SINGLE_DMG, base_atk * min(3, atk_up + element_atk_up) * bad_doppel_factor * min(3, dmg_up + dmg_up_weak) * magia_up * element_weak)
        normal_point_dmg = min(MAX_SINGLE_DMG, base_atk * min(3, atk_up + element_atk_up) * doppel_factor * min(3, dmg_up) * magia_up * element_weak)
        total_dmg = bad_point_dmg + normal_point_dmg * (dmg_point_count - 1)
    return (total_dmg, mp_gain, (total_dmg * (1 + mp_gain / MAX_MP)))

BAD_STATUS_LIST = {
    # 毒
    "POISON"    : 0.0002,
    # 烧伤
    "BURN"      : 0.0003,
    # 诅咒
    "CURSE"     : 0.0004,
    # 魅惑
    "CHARM"     : 0.0005,
    # 眩晕
    "STUN"      : 0.0006,
    # 拘束
    "RESTRAINT" : 0.0007,
    # 雾
    "FOG"       : 0.0002,
    # 黑暗
    "DARKNESS"  : 0.0003,
    # 幻惑
    "BLINDNESS" : 0.0004,
    # 技能封印
    "BAN_SKILL" : 0.0005,
    # Magia封印
    "BAN_MAGIA" : 0.0005
}
FUNCTION_SCORE_LIST = {
    "CONDITION_BAD" : BAD_STATUS_LIST,
    "ENCHANT" : BAD_STATUS_LIST,
    "CONDITION_GOOD" : {
        # 闪避
        "AVOID"             : 0.0005,
        # Charge Combo+
        "C_COMBO_PLUS"      : 0.0001,
        # 反击
        "COUNTER"           : 0.00025,
        # 暴击
        "CRITICAL"          : 0.00025,
        # 无视防御
        "DEFENSE_IGNORED"   : 0.0005,
        # 忍耐
        "GUTS"              : 0.00025,
        # VARIABLE
        "IMITATE_ATTRIBUTE" : 0.001,
        # Charge不消耗
        "NO_COST_CHARGE"    : 0.001,
        # 保护
        "PROTECT"           : 0.0006,
        # 挑衅
        "PROVOKE"           : 0.0005,
        # 追击
        "PURSUE"            : 0.00025,
        # 加速
        "SKILL_QUICK"       : 0.00075,
        # Survive
        "SURVIVE"           : 0.001
    },
    "REVOKE" : {
        # Buff解除
        "BUFF" : 0.00075,
        # 赋予效果解除
        "GOOD" : 0.00075
    },
    "DRAW" : {
        "AGAIN" : 0.00075
    },
    "IGNORE" : {
        "AVOID"         : 0.0005,
        "DEBUFF"        : 0.001,
        "CONDITION_BAD" : 0.001,
        "POISON"        : 0.00025,
        "BURN"          : 0.00025,
        "CURSE"         : 0.00025,
        "CHARM"         : 0.00025,
        "STUN"          : 0.00025,
        "RESTRAINT"     : 0.00025,
        "FOG"           : 0.00025,
        "DARKNESS"      : 0.00025,
        "BLINDNESS"     : 0.00025,
        "BAN_SKILL"     : 0.00025,
        "BAN_MAGIA"     : 0.00025
    }, 
    "HEAL" : {
        "MP_DAMAGE" : 0.00075
    }
}

def get_function_score(data: CharaData):
    '''功能性评分'''
    def get_function_score_from_list(art_list):
        base_score = 0
        for art in art_list:
            target_count = 0
            target_id = get_from_dict(art, "targetId")
            if target_id == "ALL":
                target_count = 2.5
            elif target_id in ["CONNECT", "TARGET", "ONE", "SELF"]:
                target_count = 1
            else:
                continue

            enable_turn = 1
            if get_from_dict(art, "enableTurn") == 0:
                enable_turn = 3.5
            elif "enableTurn" in art:
                enable_turn = art["enableTurn"]
                if enable_turn > 3:
                    enable_turn = 3.5

            power = 0
            verbCode = get_from_dict(art, "verbCode")
            effectCode = get_from_dict(art, "effectCode", "None")
            effectValue = get_from_dict(art, "effectValue", 1000)
            power = get_from_dict(
                get_from_dict(FUNCTION_SCORE_LIST, verbCode, {}),
                effectCode,
                0
            )

            # 赋予异常状态
            if verbCode == "CONDITION_BAD" or verbCode == "ENCHANT":
                effectValue = 1000
                if verbCode == "CONDITION_BAD" and target_id == "SELF":
                    effectValue = 0
            # Debuff/异常状态无效
            elif verbCode == "IGNORE" and effectCode in ["DEBUFF", "CONDITION_BAD"]:
                enable_turn = 1
            # 洗牌
            elif verbCode == "DRAW":
                power = 0.00075

            poss = get_from_dict(art, "probability")
            if poss is not None:
                effectValue *= poss / 1000
            
            art_score = target_count * enable_turn * power * effectValue / 10
            cd_turn = get_from_dict(art, "intervalTurn", 0)
            if cd_turn > 0:
                art_score *= (cd_turn + 1)
                art_score /= cd_turn

            base_score += art_score
            if art_score > 0 and DEBUG:
                print(art)
                print(target_count, enable_turn, power, effectValue, art_score)
        return base_score
    se_score = get_function_score_from_list(data.enhance_art) * 4
    connect_score = get_function_score_from_list(data.connect) * 3
    magia_score = get_function_score_from_list(data.magia) * 2
    doppel_score = get_function_score_from_list(data.doppel) * 1
    return se_score + connect_score + magia_score + doppel_score

def calu():
    print("编号\t中文名\t最高稀有度\t属性\t基础数值\t周回表现\t镜层表现\t辅助\t单T普攻\t高难普攻\t连携增幅值\t连携增幅比\t二人普攻\t普攻综合\tMagia伤害\tMP效率\tMagia系数\t心魔伤害\t心魔回流\t心魔系数\t功能性")
    while(True):
        id = int(input())
        if id == 0:
            break
        get_score(id)

def main():
    calu()
    # get_verb()

def get_verb():
    verb_set = set()
    for id in allchara_file.keys():
        id = int(id)
        verb_set = verb_set.union(all_check(id))
    print(verb_set)

if __name__ == "__main__":
    main()