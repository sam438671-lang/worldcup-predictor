# -*- coding: utf-8 -*-
"""2026 世界盃 - 運彩分析模擬引擎
蒙地卡羅模擬 + Poisson 分布 + Elo 評分
支援：勝負、讓分、大小、正確比數、BTTS、半全場"""

import random, math, statistics
from collections import Counter
from .team_data import TEAMS
from .player_form import get_team_form_boost
from .team_form import get_team_form, RED_CARD_PROB, PENALTY_PROB

random.seed()

# ===== Elo 評分系統 =====
def _expected_score(elo_a, elo_b):
    return 1.0 / (1.0 + 10 ** ((elo_b - elo_a) / 400.0))

def _team_strength(team_name):
    """計算球隊綜合戰力 (0-100)"""
    t = TEAMS.get(team_name, {})
    if not t: return 50
    att, def_, mid = t.get("att",70), t.get("def",70), t.get("mid",70)
    return (att * 0.35 + def_ * 0.30 + mid * 0.35)

def _team_form_boost(team_name):
    """球隊近期戰績加成 (-5 ~ +5)"""
    return get_team_form(team_name)

# ===== Poisson 分布模擬 =====
def _poisson_lambda(team_name, opponent_name, is_home=True):
    """計算球隊預期進球數 λ (lambda) — 整合 8 大類因素"""
    t = TEAMS.get(team_name, {"att":70,"def":70,"mid":70,"elo":1800})
    o = TEAMS.get(opponent_name, {"att":70,"def":70,"mid":70,"elo":1800})

    # 1️⃣ 球隊基本實力
    attack_power = t.get("att", 70) / 100.0
    opp_defense = o.get("def", 70) / 100.0
    elo_diff = (t.get("elo", 1800) - o.get("elo", 1800)) / 400.0

    # 2️⃣ 近期狀態 (近5場)
    form = _team_form_boost(team_name) * 0.06
    opp_form = _team_form_boost(opponent_name) * 0.04

    # 3️⃣ 球員全隊狀態
    star = get_team_form_boost(team_name) * 0.08
    opp_star = get_team_form_boost(opponent_name) * 0.04

    # 4️⃣ 主場優勢
    home_boost = 0.15 if is_home else 0.0

    # 5️⃣ 基礎 λ
    base = 1.4

    # 綜合計算
    lam = (base * attack_power / max(opp_defense, 0.6) + elo_diff * 0.35 +
           form - opp_form + star - opp_star + home_boost)

    return max(0.25, min(3.8, lam))

def _simulate_goals(lam):
    """Poisson 分布隨機生成進球數"""
    # Knuth's algorithm for Poisson
    L = math.exp(-lam)
    k = 0; p = 1.0
    while p > L:
        k += 1
        p *= random.random()
    return k - 1

# ===== 蒙地卡羅模擬 =====
def simulate_match(team_a, team_b, num_sims=100, neutral=True):
    """
    模擬兩隊對戰
    回傳完整分析 dict
    """
    if team_a not in TEAMS or team_b not in TEAMS:
        return None

    results = {"a_wins":0, "draw":0, "b_wins":0}
    scores = []
    ht_scores = []
    events_log = {"red_cards": 0, "penalties": 0, "red_affected": 0}

    for _ in range(num_sims):
        # 全場模擬
        lam_a = _poisson_lambda(team_a, team_b, is_home=(not neutral))
        lam_b = _poisson_lambda(team_b, team_a, is_home=False)

        # 🔥 比賽事件: 紅牌 (降低受罰方 λ 30%)
        red_a = 1 if random.random() < RED_CARD_PROB * 0.5 else 0
        red_b = 1 if random.random() < RED_CARD_PROB * 0.5 else 0
        if red_a: lam_a *= 0.7; events_log["red_cards"] += 1
        if red_b: lam_b *= 0.7; events_log["red_cards"] += 1

        # 🔥 比賽事件: 點球 (+0.8 預期進球)
        pen_a = 1 if random.random() < PENALTY_PROB * 0.5 else 0
        pen_b = 1 if random.random() < PENALTY_PROB * 0.5 else 0

        goals_a = _simulate_goals(lam_a) + pen_a
        goals_b = _simulate_goals(lam_b) + pen_b
        if pen_a + pen_b > 0: events_log["penalties"] += 1
        scores.append((goals_a, goals_b))

        if goals_a > goals_b: results["a_wins"] += 1
        elif goals_a == goals_b: results["draw"] += 1
        else: results["b_wins"] += 1

        # 半場模擬 (全場 λ 的一半)
        ht_a = _simulate_goals(lam_a * 0.45)
        ht_b = _simulate_goals(lam_b * 0.40)
        ht_scores.append((ht_a, ht_b))

    total = num_sims

    # === 全場勝負 ===
    a_win_pct = results["a_wins"] / total * 100
    draw_pct = results["draw"] / total * 100
    b_win_pct = results["b_wins"] / total * 100

    # === 正確比數 TOP 10 ===
    score_counts = Counter(scores)
    top_scores = score_counts.most_common(10)

    # === 大小球分析 (2.5 球) ===
    over25 = sum(1 for a,b in scores if a+b > 2.5) / total * 100
    under25 = 100 - over25

    # 各門檻
    over15 = sum(1 for a,b in scores if a+b > 1.5) / total * 100
    over35 = sum(1 for a,b in scores if a+b > 3.5) / total * 100

    # === BTTS (Both Teams To Score) ===
    btts_yes = sum(1 for a,b in scores if a>0 and b>0) / total * 100

    # === 半全場 ===
    ht_ft = Counter()
    for (ht_a, ht_b), (ft_a, ft_b) in zip(ht_scores, scores):
        if ht_a > ht_b and ft_a > ft_b: ht_ft["主/主"] += 1
        elif ht_a > ht_b and ft_a == ft_b: ht_ft["主/和"] += 1
        elif ht_a > ht_b and ft_a < ft_b: ht_ft["主/客"] += 1
        elif ht_a == ht_b and ft_a > ft_b: ht_ft["和/主"] += 1
        elif ht_a == ht_b and ft_a == ft_b: ht_ft["和/和"] += 1
        elif ht_a == ht_b and ft_a < ft_b: ht_ft["和/客"] += 1
        elif ht_a < ht_b and ft_a > ft_b: ht_ft["客/主"] += 1
        elif ht_a < ht_b and ft_a == ft_b: ht_ft["客/和"] += 1
        elif ht_a < ht_b and ft_a < ft_b: ht_ft["客/客"] += 1

    # === 總進球數分布 ===
    total_goals = [a+b for a,b in scores]
    avg_goals = statistics.mean(total_goals)
    median_goals = statistics.median(total_goals)
    goal_dist = Counter(total_goals)

    # === 亞洲讓分盤分析 ===
    # 計算各種讓分盤口的勝率
    handicaps = {}
    for h in [-2.0, -1.5, -1.0, -0.5, 0.0, 0.5, 1.0, 1.5, 2.0]:
        # team_a 讓 h 球
        a_cover = sum(1 for a,b in scores if a - b > h) / total * 100
        push = sum(1 for a,b in scores if abs((a - b) - h) < 0.01) / total * 100
        b_cover = 100 - a_cover - push
        handicaps[f"a{h:+.1f}"] = {"cover": round(a_cover,1), "push": round(push,1)}

    # === 推薦運彩策略 ===
    recommendations = []
    if a_win_pct > 55:
        recommendations.append(f"【高信心】{team_a} 勝 (信心度 {a_win_pct:.0f}%)")
    if b_win_pct > 55:
        recommendations.append(f"【高信心】{team_b} 勝 (信心度 {b_win_pct:.0f}%)")
    if over25 > 60:
        recommendations.append(f"【高信心】大 2.5 球 (機率 {over25:.0f}%)")
    if under25 > 60:
        recommendations.append(f"【高信心】小 2.5 球 (機率 {under25:.0f}%)")
    if btts_yes > 60:
        recommendations.append(f"【高信心】兩隊都進球-是 (機率 {btts_yes:.0f}%)")
    if btts_yes < 35:
        recommendations.append(f"【高信心】兩隊都進球-否 (機率 {100-btts_yes:.0f}%)")
    if draw_pct > 30:
        recommendations.append(f"【注意】平局機率偏高 ({draw_pct:.0f}%)，可考慮受讓")

    # 最佳正確比數
    best_score = top_scores[0] if top_scores else ((0,0),0)

    # 兩隊戰力對比
    str_a = _team_strength(team_a)
    str_b = _team_strength(team_b)

    return {
        "team_a": team_a, "team_b": team_b,
        "num_sims": num_sims,
        "strength_a": round(str_a, 1), "strength_b": round(str_b, 1),
        "form_a": round(_team_form_boost(team_a),1), "form_b": round(_team_form_boost(team_b),1),
        "events": {"avg_red_cards": round(events_log["red_cards"]/num_sims,2),
                   "avg_penalties": round(events_log["penalties"]/num_sims,2)},

        # 勝負
        "win_pct": {"a": round(a_win_pct,1), "draw": round(draw_pct,1), "b": round(b_win_pct,1)},

        # 大小球
        "over_under": {
            "over15": round(over15,1), "over25": round(over25,1), "over35": round(over35,1),
            "under25": round(under25,1),
        },

        # BTTS
        "btts": {"yes": round(btts_yes,1), "no": round(100-btts_yes,1)},

        # 正確比數 TOP 3
        "top_scores": [(f"{a}:{b}", round(cnt/total*100,1)) for (a,b), cnt in top_scores[:3]],

        # 半全場 TOP 5
        "ht_ft": [(k, round(v/total*100,1)) for k,v in ht_ft.most_common(5)],

        # 總進球
        "total_goals": {"avg": round(avg_goals,2), "median": int(median_goals),
                        "dist": {str(k):v for k,v in sorted(goal_dist.items())[:8]}},

        # 讓分盤
        "handicaps": handicaps,

        # 推薦
        "recommendations": recommendations,

        # 最佳正確比數
        "best_score": (best_score[0][0], best_score[0][1], round(best_score[1]/total*100, 1)),
    }

def get_all_teams():
    """回傳所有 48 隊名稱列表（依組別排序）"""
    groups = {}
    for name, data in TEAMS.items():
        g = data["group"]
        if g not in groups: groups[g] = []
        groups[g].append(name)
    result = []
    for g in sorted(groups.keys()):
        result.extend(sorted(groups[g]))
    return result

def get_team_info(team_name):
    """回傳單一球隊詳細資訊"""
    t = TEAMS.get(team_name, {})
    stars = STAR_PLAYERS.get(team_name, [])
    return {
        "name": team_name,
        "group": t.get("group","?"),
        "fifa_rank": t.get("fifa","?"),
        "confederation": t.get("conf","?"),
        "strength": round(_team_strength(team_name),1),
        "attack": t.get("att",0), "defense": t.get("def",0), "midfield": t.get("mid",0),
        "elo": t.get("elo",0),
        "star_boost": round(_star_boost(team_name),1),
        "star_players": [f"{n} ({r})" for n,r in stars[:3]],
    }
