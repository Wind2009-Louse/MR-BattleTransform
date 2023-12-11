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
    1020 : "[[佐鸟笼目]]",
    1021 : "[[红晴结菜]]",
    1022 : "[[煌里光]]",
    1023 : "[[笠音青]]",
    1024 : "[[大庭树里]]",
    1025 : "[[时女静香]]",
    1026 : "[[广江千春]]",
    1027 : "[[土岐沙绪]]",
    1028 : "[[蓝家姬奈]]",
    1029 : "[[宫尾时雨]]",
    1030 : "[[安积育梦]]",
    1031 : "[[神乐灿]]",
    1032 : "[[游狩美由利]]",
    1033 : "[[冰室拉比]]",
    1034 : "[[三浦旭]]",
    1035 : "[[栗栖亚历山德拉]]",
    1036 : "[[有爱丽]]",
    1037 : "[[里见那由他]]",
    1038 : "[[八云御影]]",
    1039 : "[[佐和月出里]]",
    1040 : "[[篠目夜鹤]]",
    1041 : "[[莉薇娅·梅黛洛斯]]",
    1042 : "[[小丘比]]",
    1043 : "[[黑江]]",
    1044 : "[[濑奈命]]",
    1045 : "[[水名露]]",
    1046 : "[[千鹤]]",
    1047 : "[[小黑]]",
    1048 : "[[埃博妮]]",
    1049 : "[[奥尔加]]",
    1050 : "[[冈希尔德]]",
    1051 : "[[赫露迦]]",
    1052 : "[[台与]]",
    1053 : "[[阿玛琉莉丝]]",
    1101 : "[[环伊吕波（泳装ver.）]]",
    1102 : "[[八千代·美冬（起始ver.）]]",
    1103 : "[[谣鹤乃]]",
    1104 : "[[谣莎奈]]",
    1105 : "[[小菲莉希亚]]",
    1106 : "[[梓美冬（童话ver.）]]",
    1107 : "[[灯花·音梦（圣夜ver.）]]",
    1108 : "[[圣阿莉娜]]",
    1109 : "[[小玲奈（偶像ver.）]]",
    1110 : "[[十咎桃子（修女ver.）]]",
    1112 : "[[花凛·阿莉娜（万圣ver.）]]",
    1116 : "[[和泉十七夜（吸血鬼ver.）]]",
    1117 : "[[八云御魂（晴着ver.）]]",
    1118 : "[[天音姐妹（泳装ver.）]]",
    1120 : "[[佐鸟笼目（百鬼夜行ver.）]]",
    1121 : "[[结菜·树里（吸血鬼ver.）]]",
    1125 : "[[时女静香（元旦日出ver.）]]",
    1133 : "[[冰室拉比（心魔ver.）]]",
    1137 : "[[那由他·御影（圣诞ver.）]]",
    1139 : "[[佐和月出里（情人节ver.）]]",
    1143 : "[[黑江（泳装ver.）]]",
    1201 : "[[小伊吕波]]",
    1202 : "[[七海八千代（七夕ver.）]]",
    1203 : "[[鹤乃·菲莉希亚（快递ver.）]]",
    1208 : "[[圣阿莉娜]]",
    1209 : "[[玲奈·枫（泳装ver.）]]",
    1210 : "[[桃子·御魂（人鱼ver.）]]",
    1216 : "[[和泉十七夜（常暗ver.）]]",
    1217 : "[[八云御魂（常暗ver.）]]",
    1301 : "[[伊吕波·八千代（决战ver.）]]",
    1302 : "[[七海八千代（动画ver.）]]",
    1303 : "[[谣鹤乃（动画ver.）]]",
    1309 : "[[水波玲奈（动画ver.）]]",
    1401 : "[[伊吕波·忧（巫女ver.）]]",
    1402 : "[[七海八千代（童话ver.）]]",
    1501 : "[[环伊吕波（动画ver.）]]",
    1601 : "[[∞伊吕波]]",
    1701 : "[[无限大小伊吕波]]",
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
    2103 : "[[究极小圆前辈]]",
    2104 : "[[圆·伊吕波]]",
    2105 : "[[鹿目圆（scene0 ver.）]]",
    2106 : "[[鹿目圆（泳装ver.）]]",
    2201 : "[[恶魔小焰]]",
    2202 : "[[恶魔焰]]",
    2203 : "[[晓美焰（晴着ver.）]]",
    2300 : "[[晓美焰（泳装ver.）]]",
    2301 : "[[晓美焰（scene0 ver.）]]",
    2400 : "[[美树沙耶香（晴着ver.）]]",
    2401 : "[[美树沙耶香（冲浪ver.）]]",
    2402 : "[[美树沙耶香（scene0 ver.）]]",
    2500 : "[[圣麻美]]",
    2501 : "[[巴麻美（泳装ver.）]]",
    2502 : "[[圣麻美（动画ver.）]]",
    2600 : "[[佐仓杏子（泳装ver.）]]",
    2601 : "[[佐仓杏子（scene0 ver.）]]",
    2602 : "[[佐仓杏子（魔女化身ver.）]]",
    2700 : "[[百江渚（情人节ver.）]]",
    2701 : "[[百江渚（泳装ver.）]]",
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
    3017 : "[[七濑幸佳]]",
    3018 : "[[更纱帆奈]]",
    3019 : "[[毬子彩花]]",
    3020 : "[[真尾日美香]]",
    3021 : "[[铃鹿朔夜]]",
    3022 : "[[伊并满]]",
    3023 : "[[江利爱实]]",
    3024 : "[[若菜纺]]",
    3025 : "[[五十铃怜]]",
    3026 : "[[静海木叶]]",
    3027 : "[[游佐叶月]]",
    3028 : "[[三栗菖蒲]]",
    3029 : "[[加贺见真良]]",
    3030 : "[[春名木乃美]]",
    3031 : "[[绫野梨花]]",
    3032 : "[[梢麻友]]",
    3033 : "[[史乃沙优希]]",
    3034 : "[[惠萌花]]",
    3035 : "[[千秋理子]]",
    3036 : "[[由贵真里爱]]",
    3037 : "[[安名梅露]]",
    3038 : "[[古町美仓]]",
    3039 : "[[三穗野星罗]]",
    3040 : "[[吉良手鞠]]",
    3041 : "[[柚希步鸟]]",
    3042 : "[[枇枇木巡]]",
    3043 : "[[万年樱之谣]]",
    3044 : "[[智珠兰华]]",
    3045 : "[[柚希理音]]",
    3046 : "[[观鸟令]]",
    3047 : "[[青叶知花]]",
    3048 : "[[由良萤]]",
    3049 : "[[雪野加奈惠]]",
    3050 : "[[香春优奈]]",
    3051 : "[[饰利润]]",
    3052 : "[[阿什莉·泰勒]]",
    3053 : "[[牧野郁美]]",
    3054 : "[[三轮光音]]",
    3055 : "[[桐野纱枝]]",
    3056 : "[[水树垒]]",
    3057 : "[[真井灯]]",
    3058 : "[[南津凉子]]",
    3059 : "[[入名库什]]",
    3501 : "[[梨花·怜（圣诞ver.）]]",
    3502 : "[[万年樱之谣（泳装ver.）]]",
    3503 : "[[木叶·叶月]]",
    3504 : "[[真良·心（花嫁ver.）]]",
    3900 : "[[黑]]",
    4001 : "[[美国织莉子]]",
    4002 : "[[吴纪里香]]",
    4003 : "[[千岁由麻]]",
    4004 : "[[美国织莉子（ver.Final）]]",
    4011 : "[[和美]]",
    4012 : "[[御崎海香]]",
    4013 : "[[牧薰]]",
    4014 : "[[昴和美]]",
    4021 : "[[塔鲁特]]",
    4022 : "[[莉兹]]",
    4023 : "[[梅丽莎]]",
    4024 : "[[米诺]]",
    4025 : "[[可鲁波]]",
    4026 : "[[爱丽莎]]",
    4027 : "[[拉皮努]]",
    4028 : "[[塔鲁特（Ver.Final）]]",
    4029 : "[[佩尔内勒]]",
    4121 : "[[伊莎贝拉（魔女ver.）]]",
    4122 : "[[伊莎贝拉]]",
    4031 : "[[天乃铃音]]",
    4032 : "[[日向茉莉]]",
    4033 : "[[成见亚里纱]]",
    4034 : "[[诗音千里]]",
    4035 : "[[奏遥香]]",
    4036 : "[[美琴椿]]",
    4037 : "[[日向华华莉]]",
    4041 : "[[战场原黑仪]]",
    4042 : "[[八九寺真宵]]",
    4043 : "[[神原骏河]]",
    4044 : "[[千石抚子]]",
    4045 : "[[羽川翼]]",
    4051 : "[[高町奈叶]]",
    4052 : "[[菲特]]",
    4053 : "[[八神疾风]]",
    4061 : "[[锦木千束]]",
    4062 : "[[井之上泷奈]]",

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

    6011 : "[[愉悦的蓝宝石之唇]]",
    6012 : "[[顺从的红宝石之脐]]",
    6013 : "[[振动的海蓝宝石之踵]]",
    6014 : "[[下陷的绿松石之耳]]",
    6015 : "[[健全的蛋白石之首]]",
    6016 : "[[美丽的珍珠之眼]]",
    6017 : "[[漂浮的金刚石之发]]",
    6018 : "[[停止的石榴石之小指]]",

    6101 : "[[幸福的魔女]]",
    6102 : "[[幸福魔女]]",
    6103 : "[[沙地的魔女]]",
    6104 : "[[羊之魔女]]",
    6105 : "[[屋顶的魔女]]",
    6106 : "[[保护孩子的魔女]]",
    6107 : "[[生神的魔女]]",
    6108 : "[[橡胶的魔女]]",
    6109 : "[[流浪的魔女]]",
    6110 : "[[占卜师的魔女]]",
    6112 : "[[狱门的魔女]]",
    6113 : "[[评论家的魔女]]",
    6208 : "[[象征的魔女]]",
    6211 : "[[镜之魔女]]",
    6212 : "[[镜之魔女]]",
    6214 : "[[镜之魔女]]",
    6221 : "[[象征的魔女]]",
    6223 : "[[象征的魔女]]",
    6225 : "[[象征的魔女]]",
    6227 : "[[象征的魔女]]",
    6400 : "[[班长的魔女]]",
    6401 : "[[玫瑰园的魔女]]",
    6403 : "[[零食的魔女]]",
    6404 : "[[犬之魔女]]",
    6405 : "[[舞台装置的魔女]]",
    6406 : "[[涂鸦的魔女]]",
    6407 : "[[箱之魔女]]",
    6408 : "[[黑暗的魔女]]",
    6409 : "[[影之魔女]]",
    6410 : "[[艺术家的魔女]]",
    6412 : "[[鸟笼魔女]]",
    6413 : "[[银之魔女]]",
    6414 : "[[人鱼的魔女]]",
    6416 : "[[胡桃夹子的魔女]]",
    6500 : "[[巧克力的魔女]]",
    6501 : "[[神滨圣女之谣]]",
    6502 : "[[小伊吕波|巨大伊吕波]]",

    6600 : "[[愉悦蓝宝石之唇]]",
    6601 : "？？？？？",

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
    7112 : "[[狱门的魔女的手下]]",

    7130 : "[[小猫咕噜咕噜之谣]]",
    7131 : "[[小猪皮格鲁斯之谣]]",
    7132 : "[[小牛哞太郎之谣]]",
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
    7402 : "[[玫瑰园的魔女的手下 2|玫瑰园的魔女的手下]]",
    7403 : "[[零食的魔女的手下]]",
    7404 : "[[犬之魔女的手下]]",
    7405 : "[[舞台装置的魔女的手下]]",
    7407 : "[[箱之魔女的手下]]",
    7408 : "[[黑暗的魔女的手下]]",
    7409 : "[[影之魔女的手下]]",
    7410 : "[[艺术家的魔女的手下]]",
    7412 : "[[鸟笼的魔女的手下]]",
    7413 : "[[银之魔女的手下]]",
    7414 : "[[人鱼的魔女的手下]]",
    7500 : "[[巧克力的魔女的手下]]",
    7501 : "结界入口",
    7600 : "铠甲的使魔Ⅰ",
    7601 : "铠甲的使魔Ⅱ",
    7700 : "魔法少女(二木市)",
    7701 : "魔法少女(二木市/干部)",
    7702 : "魔法少女(时女)",
    7703 : "魔法少女(时女)",
    7704 : "黑羽(新Magius)",
    7705 : "白羽(新Magius)"
}
ATTR_LIST = {"FIRE": "火",
             "TIMBER" : "木",
             "WATER": "水",
             "DARK": "暗",
             "LIGHT": "光",
             "VOID": "无"}
ATTR_COLOR = {"火" : "Red",
              "木" : "ForestGreen",
              "水" : "Blue",
              "暗" : "Purple",
              "光" : "Orange",
              "无" : "Black"}
BAD_LIST = {"POISON" : "毒",
            "BURN" : "烧伤",
            "CURSE" : "诅咒",
            "CHARM" : "魅惑",
            "STUN" : "眩晕",
            "RESTRAINT" : "拘束",
            "FOG" : "雾",
            "DARKNESS" : "黑暗",
            "BLINDNESS" : "幻惑",
            "BAN_SKILL" : "技能封印",
            "BAN_MAGIA" : "Magia封印",
            "INVALID_HEAL_HP" : "HP回复禁止",
            "INVALID_HEAL_MP" : "MP回复禁止",
            "DAMAGE_UP_BAD_NUM" : "虚弱",
            "DEBUFF" : "DEBUFF",
            "CONDITION_BAD": "异常状态"}
GOOD_LIST = {"AUTO_HEAL" : "自动回复",
             "AVOID" : "回避",
             "COUNTER" : "反击",
             "CRITICAL" : "暴击",
             "DAMAGE_DOWN" : "伤害削减",
             "DAMAGE_DOWN_NODISK" : "Magia伤害削减",
             "DAMAGE_DOWN_ACCEL" : "Accele伤害削减",
             "DAMAGE_DOWN_BLAST" : "Blast伤害削减",
             "DAMAGE_DOWN_CHARGE" : "Charge后伤害削减",
             "DAMAGE_DOWN_CHARGING" : "Charge盘伤害削减",
             "DAMAGE_DOWN_DARK" : "暗属性伤害削减",
             "DAMAGE_DOWN_LIGHT" : "光属性伤害削减",
             "DAMAGE_DOWN_WATER" : "水属性伤害削减",
             "DAMAGE_DOWN_FIRE" : "火属性伤害削减",
             "DAMAGE_DOWN_TIMBER" : "木属性伤害削减",
             "DAMAGE_DOWN_VOID" : "无属性伤害削减",
             "DAMAGE_UP" : "伤害上升",
             "DAMAGE_UP_BAD" : "对敌状态异常时伤害UP",
             "DEFENSE_IGNORED" : "防御无视",
             "MP_PLUS_WEAKED" : "被弱点属性攻击时MPUP",
             "MP_PLUS_DAMAGED" : "被攻击时MPUP",
             "PROTECT" : "保护",
             "PROVOKE" : "挑衅",
             "PURSUE" : "追击",
             "SKILL_QUICK" : "技能冷却加速",
             "GUTS" : "忍耐",
             "SURVIVE" : "Survive",
             "MP_PLUS_BLAST" : "Blast攻击时获得MP",
             "IMITATE_ATTRIBUTE" : "Variable",
             "NO_COST_CHARGE" : "Charge无消耗",
             "BARRIER" : "屏障",
             "REFLECT_DEBUFF" : "Debuff反射"}
CHANCE_GOOD_LIST = ["AVOID","COUNTER","CRITICAL","DAMAGE_DOWN","DAMAGE_UP",
                    "DEFENSE_IGNORED","PROVOKE","PROTECT","PURSUE","INVALID_HEAL_HP",
                    "SKILL_QUICK"]
WORDS_TRANS = {"ATTACK" : "攻击力",
               "DEF" : "防御力",
               "DEFENSE" : "防御力",
               "MP_GAIN" : "MP获得量",
               "MP_GAIN_OVER100" : "MP100以上时MP获得量",
               "RESIST" : "异常状态耐性",
               "ACCEL" : "Accele MP",
               "BLAST" : "Blast伤害",
               "CHARGE" : "Charge后伤害",
               "CHARGING" : "Charge盘伤害",
               "MAGIA" : "Magia伤害",
               "DOPPEL" : "DOPPEL伤害",
               "DAMAGE" : "造成伤害",
               "WEAK_BLAST" : "Blast伤害",
               "WEAK_CHARGE_DONE" : "Charge后伤害",
               "WEAK_FIRE" : "火属性伤害",
               "WEAK_WATER" : "水属性伤害",
               "WEAK_TIMBER" : "木属性伤害",
               "WEAK_DARK" : "暗属性伤害",
               "WEAK_LIGHT" : "光属性伤害",
               "ATTACK_FIRE" : "火属性攻击力",
               "ATTACK_TIMBER" : "木属性攻击力",
               "ATTACK_WATER" : "水属性攻击力",
               "ATTACK_LIGHT" : "光属性攻击力",
               "ATTACK_DARK" : "暗属性攻击力"}
REVOKE_TYPES = {"BUFF" : "Buff解除",
                "DEBUFF" : "Debuff解除",
                "BAD" : "状态异常解除",
                "GOOD" : "赋予效果解除"}
CODE_MAP = {"BUFF" : "%sUP",
            "BUFF_DYING" : "濒死时%sUP",
            "BUFF_HPMAX" : "HP最大时%sUP",
            "BUFF_PARTY_DIE" : "同伴死亡时%sUP",
            "BUFF_DIE" : "死亡时同伴%sUP"}
TYPE_WILL_ON_ENEMY = {"CONDITION_BAD","DEBUFF"}
LIMIT_TARGET = {"WITCH":"魔女","RUMOR":"谣","HUMAN":"魔法少女","EMOTION":"心魔"}
FIELD_SIDE_LIST = {"PLAYER" : "己方", "ENEMY": "敌方"}
COST_TRANS = {"みたま特製エナジードリンク" : "饮料",
              "色鉛筆" : "铅笔",
              "料金分の愛情が入ったパフェ" : "帕菲",
              "記憶の頁" : "记忆之页",
              "回数券" : "回数券",
              "ブラックカード" : "黑卡",
              "フォーチュンペーパー" : "幸运纸",
              "メモリーピン":"记忆大头针",
              "練習カレンダー":"练习日历本",
              "珊瑚礁":"珊瑚礁",
              "始まりの焚火":"篝火",
              "サンタのひげ":"圣诞胡子",
              "秋の七草":"秋之七草",
              "宇宙一のレシピ":"食谱",
              "まどかPからの連絡":"联络",
              "乙女の秘密":"少女的秘密",
              "アクアリウムへの招待状":"请柬",
              "いたずら駄菓子":"糖果",
              "白紙の便箋":"便笺",
              "ヒイラギの葉":"柊树叶",
              "大凧":"风筝",
              "絡まりリボン":"缎带",
              "疑惑の写真":"写真",
              "キレイな川魚":"河鱼",
              "七夕飾り":"装饰",
              "想い結ぶシュシュ":"发圈",
              "サークルリスト":"名单",
              "憧憬の烙印":"烙印",
              "マギウスの指令書":"指令书",
              "ハワイ行のチケット":"奖券",
              "仮面":"假面",
              "なかよし手帳":"手册",
              "群印":"群印",
              "商店街の福引券":"抽奖券"}
SPECIAL_MEMORY_NAME = ["!","…","、","！","？","災"]

POSITION_TRANSFORM = {1:3, 2:6, 3:9, 4:2, 5:5, 6:8, 7:1, 8:4, 9:7}

def char_idtostr(id,origin_str):
    if (type(id) != int): id = int(id)
    return_str = ""
    if origin_str == "幸福な魔女の手下" or origin_str == "幸福の魔女の手下":
        return "[[幸福的魔女的手下]]"
    if origin_str == "FM神浜のウワサ":
        return "[[绝交阶梯之谣|FM神滨之谣]]"
    if origin_str == "神浜レアリティースターのウワサ":
        return "神滨稀有度之星之谣"
    if origin_str == "記憶キュゥレーターのウワサ":
        return "[[记忆馆长之谣|记忆Q长之谣]]"
    if id % 10 == 9:
        return_str += "镜"
    real_id = math.floor(id / 100)
    if real_id in CHAR_ID_LIST:
        return_str += CHAR_ID_LIST[real_id]
    else:
        return_str += origin_str
    return return_str

def item_idtostr(id, json_data):
    '''将掉落转换为字符串'''
    new_id = re.sub(r"GIFT_(\d*)_\d*",r"\1", id)
    if (id == new_id): return ""
    new_id = int(new_id)
    for i in json_data["giftList"]:
        if i["id"] == new_id:
            return "{{素材|%s}}" % i["name"]
    return ""

def art_to_str(this_art):
    '''将art转换为字符串'''
    this_mem_str = ""
    if this_art["code"] == "ENCHANT":
        sub_state = BAD_LIST[this_art["sub"]]
        if this_art["rate"] < 1000:
            this_mem_str += '<span title="%.1f%%">攻击时概率赋予%s(%dT)状态</span>' % (this_art["rate"] / 10 ,sub_state, this_art["turn"])
        elif this_art["rate"] == 1000:
            this_mem_str += "攻击时必定赋予%s(%dT)状态" % (sub_state, this_art["turn"])
        elif this_art["rate"] > 1000:
            this_mem_str += '<span title="%.1f%%">攻击时必定赋予%s(%dT)状态</span>' % (this_art["rate"] / 10 ,sub_state, this_art["turn"])
    elif this_art["code"] == "CONDITION_GOOD":
        this_mem_str += rate_append(this_art["sub"], this_art["rate"])
        this_art_str = GOOD_LIST[this_art["sub"]]
        effect_not_used = True
        if this_art_str == "反击" and this_art["effect"] > 800:
            this_art_str = '<span title="%.1f%%">交叉反击</span>'%(this_art["effect"] / 10)
        elif this_art_str == "自动回复":
            if "genericValue" in this_art.keys() and this_art["genericValue"] == "MP":
                this_art_str = "MP自动回复"
                this_art_str = "%s(%d)" % (this_art_str, this_art["effect"] / 10)
            else:
                this_art_str = "HP自动回复"
                this_art_str = "%s(%d%%)" % (this_art_str, this_art["effect"] / 10)
        elif this_art_str == "保护" and this_art["target"] == "DYING":
            this_art_str = "保护濒死的同伴"
        elif this_art_str == "Survive":
            this_art_str = '<span title="%.1f%%">Survive</span>'%(this_art["effect"] / 10)
        elif this_art_str == "屏障":
            this_art_str = '屏障(%d)'%(this_art["effect"])
        elif this_art_str == "Debuff反射":
            this_art_str = 'Debuff反射%d回'%(this_art["effect"])
        else:
            effect_not_used = False
        if this_art_str == "保护" and "param" in this_art.keys():
            this_art_str += "(必定保护%s)"%char_idtostr(this_art["param"]*100,"NULL")
        if not effect_not_used and "effect" in this_art:
            this_mem_str += '<span title="%.1f%%">%s</span>' % (this_art["effect"] / 10, this_art_str)
        else:
            this_mem_str += this_art_str
    elif this_art["code"] == "CONDITION_BAD":
        this_mem_str += rate_append(this_art["sub"], this_art["rate"])
        this_art_str = BAD_LIST[this_art["sub"]]
        if this_art_str == "毒" and this_art["effect"] > 100:
            this_art_str = "强化毒"
        if this_art_str == "诅咒" and this_art["effect"] > 200:
            this_art_str = "强化诅咒"
        if "effect" in this_art:
            this_mem_str += '<span title="%.1f%%">%s</span>' % (this_art["effect"] / 10, this_art_str)
        else:
            this_mem_str += this_art_str
    elif this_art["code"] == "IGNORE":
        this_mem_str += rate_append(this_art["sub"], this_art["rate"])
        if this_art["sub"] in GOOD_LIST.keys():
            this_mem_str += "%s无效" % (GOOD_LIST[this_art["sub"]])
        elif this_art["sub"] in BAD_LIST.keys():
            this_mem_str += "%s无效" % (BAD_LIST[this_art["sub"]])
        else:
            print("CODE IGNORE新SUB:%s" % this_art["sub"])
    elif this_art["code"] == "HEAL":
        if this_art["sub"] == "HP":
            this_mem_str += "HP回复"
        elif this_art["sub"] == "MP_DAMAGE":
            this_mem_str += "MP伤害"
        elif this_art["sub"] == "MP":
            this_mem_str += "MP回复"
        else:
            print("HEAL新sub:", this_art["sub"])
    elif this_art["code"] == "REVOKE":
        if this_art["sub"] in REVOKE_TYPES.keys():
            this_mem_str += REVOKE_TYPES[this_art["sub"]]
        else:
            print("REVOKE新sub: ",this_art["sub"])
    elif this_art["code"] == "LIMITED_ENEMY_TYPE":
        target_name = WORDS_TRANS[this_art["genericValue"]]
        if "effect" in this_art:
            this_mem_str += '<span title="%.1f%%">对%s%s</span>' % (this_art["effect"] / 10, target_name, GOOD_LIST[this_art["sub"]])
        else:
            this_mem_str += "对%s%s" % (target_name,GOOD_LIST[this_art["sub"]])
    elif this_art["code"] == "DEBUFF":
        if "effect" in this_art:
            if "WEAK" in this_art["sub"]:
                this_mem_str += '<span title="%.1f%%">%s耐性DOWN</span>' % (this_art["effect"] / 10, WORDS_TRANS[this_art["sub"]])
            else:
                this_mem_str += '<span title="%.1f%%">%sDOWN</span>' % (this_art["effect"] / 10, WORDS_TRANS[this_art["sub"]])
        else:
            this_mem_str += "%sDOWN" % (WORDS_TRANS[this_art["sub"]])
    elif this_art["code"] == "INITIAL" and this_art["sub"] == "MP":
        this_mem_str += "初始%dMP" % (this_art["effect"] / 10)
    elif this_art["code"] == "RESURRECT":
        this_mem_str += "苏生"
    elif this_art["code"] == "ATTACK":
        sub_str = ""
        if "sub" in this_art:
            if this_art["sub"] == "DAMAGE_UP_BADS":
                sub_str += "异常增伤"
            elif this_art["sub"] == "LINKED_DAMAGE":
                sub_str += "低HP威力UP"
            elif this_art["sub"] == "ALIGNMENT":
                sub_str += "属性强化"
            elif this_art["sub"] == "DUMMY":
                return "DUMMY"
        if this_art["target"] == "TARGET":
            this_mem_str += "对敌方单体%s伤害"%sub_str
        elif this_art["target"] == "ALL":
            this_mem_str += "对敌方全体%s伤害"%sub_str
        elif this_art["target"][0:6] == "RANDOM":
            this_mem_str += "随机%s次 %s伤害"%(this_art["target"][-1],sub_str)
        elif this_art["target"] == "HORIZONTAL":
            this_mem_str += "横方向%s伤害"%sub_str
        elif this_art["target"] == "VERTICAL":
            this_mem_str += "纵方向%s伤害"%sub_str
        else:
            print("新攻击：%s",str(this_art))
        if "effect" in this_art:
            this_mem_str = '<span title="%.1f%%">%s</span>'%(this_art["effect"] / 10, this_mem_str)
    elif this_art["code"] == "TURN_ALLY" or this_art["code"] == "TURN_ENEMY":
        if this_art["sub"] == "BUFF":
            this_mem_str += "Buff延长"
        elif this_art["sub"] == "DEBUFF":
            this_mem_str += "Debuff延长"
    else:
        if this_art["code"] in CODE_MAP:
            temp_str = CODE_MAP[this_art["code"]]
            if "effect" in this_art:
                temp_str = '<span title="%.1f%%">' + temp_str + "</span>"
                this_mem_str += temp_str % (this_art["effect"] / 10, WORDS_TRANS[this_art["sub"]])
            else:
                this_mem_str += temp_str % (WORDS_TRANS[this_art["sub"]])
        else:
            print("ART新CODE:", this_art["code"])
    return this_mem_str

def rate_append(type,rate):
    if type in CHANCE_GOOD_LIST or type in BAD_LIST.keys():
        if rate > 1000:
            return '<span title="%.1f%%">必定</span>'%(rate/10)
        elif rate == 1000:
            return "必定"
        else:
            return '<span title="%.1f%%">概率</span>'%(rate/10)
    else:
        return ""

def range_to_str(this_art):
    result_str = ""
    # Magia无范围
    if this_art["code"] in ["ATTACK", "ENCHANT"]:
        return ""
    if this_art["code"] == "TURN_ALLY":
        if this_art["target"] == "SELF":
            result_str += "自"
        elif this_art["target"] == "ALL":
            result_str += "己全"
        if "effect" in this_art:
            result_str += "/%dT" % (this_art["effect"])
    elif this_art["code"] == "TURN_ENEMY":
        if this_art["target"] == "ONE":
            result_str += "敌单"
        elif this_art["target"] == "ALL":
            result_str += "敌全"
        if "effect" in this_art:
            result_str += "/%dT" % (this_art["effect"])
    elif this_art["target"] == "SELF":
        if this_art["code"] == "HEAL":
            # 如 (自/10%)
            if this_art["sub"] == "MP" or this_art["sub"] == "MP_DAMAGE":
                result_str += "自/%d" % (this_art["effect"]/10)
            else:
                result_str += "自/%d%%" % (this_art["effect"]/10)
        elif "turn" in this_art.keys():
            # 如 (自/3T)
            result_str += "自/%dT" % (this_art["turn"])
        else:
            result_str += "自"
    else:
        temp_str = ""
        # 敌单 敌全 单 全
        if (this_art["code"] == "REVOKE" and (this_art["sub"] == "BUFF" or this_art["sub"] == "GOOD")) \
            or this_art["code"] in TYPE_WILL_ON_ENEMY \
            or (this_art["code"] == "HEAL" and this_art["sub"] == "MP_DAMAGE"):
            temp_str += "敌"

        if this_art["target"] == "ALL":
            temp_str += "全"
        elif this_art["target"] == "ONE" or this_art["target"] == "TARGET":
            temp_str += "单"

        if "turn" in this_art.keys():
            # 如 (敌单/1T)
            result_str += "%s/%dT" % (temp_str, this_art["turn"])
        elif this_art["code"] == "HEAL":
            # 如 (全/30%)
            if this_art["sub"] == "MP" or this_art["sub"] == "MP_DAMAGE":
                result_str += "%s/%d" % (temp_str,this_art["effect"]/10)
            else:
                result_str += "%s/%d%%" % (temp_str,this_art["effect"]/10)
        elif this_art["code"] == "RESURRECT":
            result_str += "%s/%d%%" % (temp_str,this_art["effect"]/10)
        else:
            # 如 (敌全)
            result_str += "%s" % temp_str
    if "param" in this_art and this_art["param"] == 1:
        if len(result_str) > 0:
            result_str += "/"
        result_str += "不可解除"
    if len(result_str) > 0:
        return "(%s)"%result_str
    return ""