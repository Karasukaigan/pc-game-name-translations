import csv
import difflib

# 从CSV文件读取数据
def read_csv(file_name):
    with open(file_name, 'r', encoding='utf-8') as csvfile:
        return [row for row in csv.DictReader(csvfile)]
game_data = read_csv('game_names_merged.csv')

# 获取用户输入
user_input = input("请输入关键词：")

# 计算相似度并排序
def similarity(a, b):
    return difflib.SequenceMatcher(None, a.lower(), b.lower()).ratio()
similar_games = sorted(game_data, key=lambda x: (similarity(user_input, x['en_name']),
                                                 similarity(user_input, x['zh_name']),
                                                 similarity(user_input, x['ja_name'])), reverse=True)

# 输出查询结果
print("查询结果：")
for game in similar_games:
    sim = [similarity(user_input, game[key]) for key in ['en_name', 'zh_name', 'ja_name']]
    # 如果相似度大于0.8或用户输入包含在游戏名称中，则输出该游戏名称
    if max(sim) > 0.8 or any(user_input in game[key] for key in ['en_name', 'zh_name', 'ja_name']):
        game_name = game['zh_name'] or game['en_name'] or game['ja_name']
        if game['en_name'] and game['en_name'] != game_name:
            game_name += f" ({game['en_name']})"
        if game['ja_name'] and game['ja_name'] != game_name:
            game_name += f" ({game['ja_name']})"
        print(game_name)