#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""自動更新 2026 世界盃賽果與球隊狀態 — GitHub Actions 每日執行"""

import json, os, re, random
from datetime import datetime, timedelta
from collections import Counter

# ===== 48 隊 Elo 基礎值 =====
ELO_BASE = {
    "阿根廷":2135,"法國":2120,"巴西":2110,"英格蘭":2085,"西班牙":2070,"德國":2050,
    "葡萄牙":2040,"荷蘭":2020,"比利時":1990,"克羅埃西亞":1970,"美國":1960,
    "摩洛哥":1940,"烏拉圭":1935,"日本":1930,"哥倫比亞":1925,"墨西哥":1920,
    "瑞士":1910,"塞內加爾":1900,"瑞典":1870,"奧地利":1860,"挪威":1855,
    "象牙海岸":1850,"丹麥":1845,"加拿大":1840,"土耳其":1835,"捷克":1830,
    "厄瓜多":1830,"埃及":1830,"波蘭":1820,"蘇格蘭":1815,"伊朗":1810,
    "阿爾及利亞":1800,"巴拉圭":1790,"澳洲":1780,"迦納":1770,"突尼西亞":1755,
    "南非":1750,"沙烏地阿拉伯":1740,"卡達":1730,"波赫":1720,"伊拉克":1710,
    "剛果民主共和國":1700,"烏茲別克":1690,"巴拿馬":1680,"維德角":1660,
    "約旦":1650,"紐西蘭":1640,"海地":1620,"庫拉索":1580,"南韓":1880,
}

def update_elo(winner_elo, loser_elo, draw=False, k=32):
    """更新 Elo 積分"""
    if draw:
        e = 1 / (1 + 10**((loser_elo - winner_elo)/400))
        return winner_elo + k*(0.5 - e), loser_elo + k*(0.5 - (1-e))
    e = 1 / (1 + 10**((loser_elo - winner_elo)/400))
    return winner_elo + k*(1 - e), loser_elo + k*(0 - (1-e))

def update_html():
    """根據 LATEST_RESULTS 更新 HTML 中的資料"""
    html_path = os.path.join(os.path.dirname(__file__), 'index.html')
    if not os.path.exists(html_path):
        html_path = os.path.join(os.path.dirname(__file__), 'WorldCup2026_Predictor.html')
    with open(html_path, 'r', encoding='utf-8') as f:
        html = f.read()

    today = datetime.now().strftime('%Y-%m-%d')
    print(f"Update date: {today}")

    # ===== 手動維護區：在此新增每日最新賽果 =====
    # 格式: (日期, 組別, 主隊, 客隊, 比數)  比數=None表示尚未開賽
    LATEST_RESULTS = [
        # 已賽結果 (截至 6/24)
        ("2026-06-11","A","墨西哥","南非","2-0"),
        ("2026-06-11","A","南韓","捷克","2-1"),
        ("2026-06-12","B","加拿大","波赫","1-1"),
        ("2026-06-12","D","美國","巴拉圭","4-1"),
        ("2026-06-13","B","卡達","瑞士","1-1"),
        ("2026-06-13","C","巴西","摩洛哥","1-1"),
        ("2026-06-13","C","蘇格蘭","海地","1-0"),
        ("2026-06-14","D","澳洲","土耳其","2-0"),
        ("2026-06-14","E","德國","庫拉索","7-1"),
        ("2026-06-14","F","荷蘭","日本","2-2"),
        ("2026-06-14","E","象牙海岸","厄瓜多","1-0"),
        ("2026-06-14","F","瑞典","突尼西亞","5-1"),
        ("2026-06-15","H","西班牙","維德角","0-0"),
        ("2026-06-15","G","比利時","埃及","1-1"),
        ("2026-06-15","H","沙烏地阿拉伯","烏拉圭","1-1"),
        ("2026-06-15","G","伊朗","紐西蘭","2-2"),
        ("2026-06-16","I","法國","塞內加爾","3-1"),
        ("2026-06-16","I","挪威","伊拉克","4-1"),
        ("2026-06-16","J","阿根廷","阿爾及利亞","3-0"),
        ("2026-06-17","J","奧地利","約旦","3-1"),
        ("2026-06-17","K","葡萄牙","剛果民主共和國","1-1"),
        ("2026-06-17","L","英格蘭","克羅埃西亞","4-2"),
        ("2026-06-17","L","迦納","巴拿馬","1-0"),
        ("2026-06-17","K","哥倫比亞","烏茲別克","3-1"),
        ("2026-06-18","A","捷克","南非","1-1"),
        ("2026-06-18","B","瑞士","波赫","4-1"),
        ("2026-06-18","B","加拿大","卡達","6-0"),
        ("2026-06-18","A","墨西哥","南韓","1-0"),
        ("2026-06-19","D","美國","澳洲","2-0"),
        ("2026-06-19","C","摩洛哥","蘇格蘭","1-0"),
        ("2026-06-19","C","巴西","海地","3-0"),
        ("2026-06-19","D","巴拉圭","土耳其","1-0"),
        ("2026-06-20","F","荷蘭","瑞典","5-1"),
        ("2026-06-20","E","德國","象牙海岸","2-1"),
        ("2026-06-20","E","厄瓜多","庫拉索","0-0"),
        ("2026-06-21","F","日本","突尼西亞","4-0"),
        ("2026-06-21","H","西班牙","沙烏地阿拉伯","4-0"),
        ("2026-06-21","G","比利時","伊朗","0-0"),
        ("2026-06-21","H","烏拉圭","維德角","2-2"),
        ("2026-06-21","G","埃及","紐西蘭","3-1"),
        ("2026-06-22","J","阿根廷","奧地利","2-0"),
        ("2026-06-22","I","法國","伊拉克","3-0"),
        ("2026-06-22","I","挪威","塞內加爾","3-2"),
        ("2026-06-22","J","約旦","阿爾及利亞","1-2"),
        # 6/23 賽果
        ("2026-06-23","K","葡萄牙","烏茲別克","4-0"),
        ("2026-06-23","L","英格蘭","迦納","2-0"),
        ("2026-06-23","L","巴拿馬","克羅埃西亞","0-3"),
        ("2026-06-23","K","哥倫比亞","剛果民主共和國","2-0"),
        # 6/24 賽果 - 今日
        ("2026-06-24","B","瑞士","加拿大",None),
        ("2026-06-24","B","波赫","卡達",None),
        ("2026-06-24","C","蘇格蘭","巴西",None),
        ("2026-06-24","C","摩洛哥","海地",None),
        ("2026-06-24","A","南非","南韓",None),
        ("2026-06-24","A","捷克","墨西哥",None),
        # 6/25
        ("2026-06-25","E","庫拉索","象牙海岸",None),
        ("2026-06-25","E","厄瓜多","德國",None),
        ("2026-06-25","F","日本","瑞典",None),
        ("2026-06-25","F","突尼西亞","荷蘭",None),
        ("2026-06-25","D","巴拉圭","澳洲",None),
        ("2026-06-25","D","土耳其","美國",None),
        # 6/26
        ("2026-06-26","I","挪威","法國",None),
        ("2026-06-26","I","塞內加爾","伊拉克",None),
        ("2026-06-26","H","烏拉圭","西班牙",None),
        ("2026-06-26","H","維德角","沙烏地阿拉伯",None),
        ("2026-06-26","G","埃及","伊朗",None),
        ("2026-06-26","G","紐西蘭","比利時",None),
        # 6/27
        ("2026-06-27","L","巴拿馬","英格蘭",None),
        ("2026-06-27","L","克羅埃西亞","迦納",None),
        ("2026-06-27","K","哥倫比亞","葡萄牙",None),
        ("2026-06-27","K","剛果民主共和國","烏茲別克",None),
        ("2026-06-27","J","約旦","阿根廷",None),
        ("2026-06-27","J","阿爾及利亞","奧地利",None),
    ]

    # 更新 Elo
    elo = dict(ELO_BASE)
    for m in LATEST_RESULTS:
        if m[4] is None: continue
        try:
            ga, gb = map(int, m[4].split('-'))
            if m[2] in elo and m[3] in elo:
                if ga > gb:
                    elo[m[2]], elo[m[3]] = update_elo(elo[m[2]], elo[m[3]])
                elif gb > ga:
                    elo[m[3]], elo[m[2]] = update_elo(elo[m[3]], elo[m[2]])
                else:
                    elo[m[2]], elo[m[3]] = update_elo(elo[m[2]], elo[m[3]], draw=True)
        except: pass

    # 計算近期狀態 (近5場)
    team_results = {t: [] for t in elo}
    for m in LATEST_RESULTS:
        if m[4] is None: continue
        try:
            ga, gb = map(int, m[4].split('-'))
            team_results[m[2]].append((ga, gb, elo.get(m[3],1800)))
            team_results[m[3]].append((gb, ga, elo.get(m[2],1800)))
        except: pass

    form_scores = {}
    for team, results in team_results.items():
        recent = results[-5:]
        if not recent: form_scores[team] = 0; continue
        pts = sum(3 if g[0]>g[1] else 1 if g[0]==g[1] else 0 for g in recent)
        gf = sum(g[0] for g in recent)
        ga = sum(g[1] for g in recent)
        pts_pct = pts / max(len(recent)*3, 1)
        gd = gf - ga
        form_scores[team] = round((pts_pct - 0.5)*5 + gd*0.3, 1)

    # 生成 JavaScript 的 MATCHES 陣列
    matches_js = "const MATCHES=[\n"
    for m in LATEST_RESULTS:
        result_str = f'"{m[4]}"' if m[4] else 'null'
        matches_js += f'["{m[0]}","{m[1]}","{m[2]}","{m[3]}",{result_str}],'
    matches_js += "\n];"

    # 更新 HTML 中的 MATCHES
    html = re.sub(r'const MATCHES=\[[\s\S]*?\];', matches_js, html)

    # 更新 TEAMS 中的 elo (e) 和 form (f)
    for team, e_val in elo.items():
        new_e = int(e_val)
        new_f = form_scores.get(team, 0)
        # Update TEAMS dict in JS
        pattern = rf'"{team}":\{{g:"([^"]*)",r:(\d+),a:(\d+),d:(\d+),m:(\d+),e:(\d+),f:([-\d.]+)\}}'
        repl = rf'"{team}":{{g:"\1",r:\2,a:\3,d:\4,m:\5,e:{new_e},f:{new_f}}}'
        html = re.sub(pattern, repl, html)

    # 重新整理 MATCHES 格式 (加入換行)
    html = re.sub(r'const MATCHES=\[([^\]]+)\];',
                  lambda m: 'const MATCHES=[\n' + re.sub(r'\],\"', '],\n\"', m.group(1)) + '\n];', html)

    # 寫回
    for fname in ['index.html', 'WorldCup2026_Predictor.html']:
        path = os.path.join(os.path.dirname(__file__), fname)
        if os.path.exists(path):
            with open(path, 'w', encoding='utf-8') as f:
                f.write(html)
            print(f"Updated: {fname}")

    print(f"Teams updated: {len(elo)}")
    print(f"Matches: {len(LATEST_RESULTS)}")
    return True

if __name__ == '__main__':
    update_html()
