# -*- coding: utf-8 -*-
"""2026 世界盃預測系統 - GUI"""

import customtkinter as ctk
from tkinter import messagebox
import threading
from .simulator import simulate_match, get_all_teams, get_team_info
from .match_schedule import get_matches_by_date, get_all_dates, BETTING_TYPES

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

BG = "#0F172A"; CARD = "#1E293B"; ACCENT = "#3B82F6"
GREEN = "#10B981"; RED = "#EF4444"; YELLOW = "#F59E0B"
TEXT = "#E2E8F0"; SUBTEXT = "#94A3B8"; BORDER = "#334155"


class WorldCupApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("2026 世界盃預測分析系統")
        self.geometry("1100x800"); self.minsize(900, 650)
        self.configure(fg_color=BG)
        self.dates = get_all_dates()
        self._build_main()

    def _build_main(self):
        for w in self.winfo_children(): w.destroy()

        # Header
        h = ctk.CTkFrame(self, fg_color="#1E3A5F", corner_radius=0, height=70)
        h.pack(fill="x"); h.pack_propagate(False)
        ctk.CTkLabel(h, text="2026 FIFA 世界盃 預測分析系統",
            font=ctk.CTkFont(size=22, weight="bold"), text_color="white").pack(pady=(12,2))
        ctk.CTkLabel(h, text="蒙地卡羅模擬 × Poisson 分布 × 運彩分析  |  48 隊完整資料庫",
            font=ctk.CTkFont(size=11), text_color="#94A3B8").pack()

        # Main content
        main = ctk.CTkFrame(self, fg_color="transparent")
        main.pack(fill="both", expand=True, padx=20, pady=15)

        # === Left Panel ===
        left = ctk.CTkFrame(main, fg_color="transparent", width=320)
        left.pack(side="left", fill="y", padx=(0,15))
        left.pack_propagate(False)

        # Date
        ctk.CTkLabel(left, text="比賽日期", font=ctk.CTkFont(size=12, weight="bold"),
            text_color=TEXT).pack(anchor="w", pady=(0,3))
        self.date_var = ctk.StringVar(value=self.dates[0] if self.dates else "")
        self.date_menu = ctk.CTkOptionMenu(left, values=self.dates, variable=self.date_var,
            font=ctk.CTkFont(size=12), fg_color=CARD, button_color=ACCENT, text_color=TEXT,
            dropdown_fg_color=CARD, dropdown_text_color=TEXT, height=36,
            command=lambda _: self._load_matches())
        self.date_menu.pack(fill="x")

        # Match list
        ctk.CTkLabel(left, text="選擇對戰組合", font=ctk.CTkFont(size=12, weight="bold"),
            text_color=TEXT).pack(anchor="w", pady=(15,3))
        self.match_frame = ctk.CTkScrollableFrame(left, fg_color=CARD, corner_radius=8, height=180)
        self.match_frame.pack(fill="x", pady=(0,10))
        self.match_btns = []
        self.selected_match = None

        # Bet type
        ctk.CTkLabel(left, text="運彩玩法", font=ctk.CTkFont(size=12, weight="bold"),
            text_color=TEXT).pack(anchor="w", pady=(5,3))
        self.bet_var = ctk.StringVar(value=BETTING_TYPES[-1])
        ctk.CTkOptionMenu(left, values=BETTING_TYPES, variable=self.bet_var,
            font=ctk.CTkFont(size=12), fg_color=CARD, button_color=ACCENT, text_color=TEXT,
            dropdown_fg_color=CARD, dropdown_text_color=TEXT, height=36).pack(fill="x", pady=(0,5))

        # Sim count
        ctk.CTkLabel(left, text="模擬次數", font=ctk.CTkFont(size=12, weight="bold"),
            text_color=TEXT).pack(anchor="w", pady=(10,3))
        sim_frame = ctk.CTkFrame(left, fg_color="transparent")
        sim_frame.pack(fill="x")
        self.sim_var = ctk.IntVar(value=200)
        for v, label in [(50,"50"),(100,"100"),(200,"200"),(500,"500")]:
            ctk.CTkRadioButton(sim_frame, text=label, variable=self.sim_var, value=v,
                font=ctk.CTkFont(size=11), fg_color=ACCENT, text_color=TEXT,
                border_color=BORDER).pack(side="left", padx=(0,8))

        # Buttons
        ctk.CTkButton(left, text="開始分析預測", command=self._run_simulation,
            font=ctk.CTkFont(size=15, weight="bold"), fg_color=ACCENT,
            hover_color="#2563EB", height=48, corner_radius=10).pack(fill="x", pady=(15,5))

        # === Right Panel (Results) ===
        self.result_frame = ctk.CTkScrollableFrame(main, fg_color=CARD, corner_radius=12)
        self.result_frame.pack(side="right", fill="both", expand=True)
        self._show_welcome()

        # Load matches
        self._load_matches()

    def _load_matches(self):
        for b in self.match_btns: b.destroy()
        self.match_btns = []
        date = self.date_var.get()
        matches = get_matches_by_date(date)
        from datetime import date as dt
        today = dt.today().isoformat()
        if not matches:
            ctk.CTkLabel(self.match_frame, text="本日無比賽",
                font=ctk.CTkFont(size=12), text_color=SUBTEXT).pack(pady=20)
            return
        for m in matches:
            is_today = " TODAY" if m["date"] == today else ""
            if m.get("result"):
                txt = f"[{m['group']}組] {m['team_a']} {m['result']} {m['team_b']} (已賽)"
                clr = SUBTEXT
            else:
                txt = f"[{m['group']}組] {m['team_a']} vs {m['team_b']}{is_today}"
                clr = GREEN if is_today else TEXT
            btn = ctk.CTkButton(self.match_frame, text=txt, font=ctk.CTkFont(size=11),
                fg_color="transparent", hover_color=BORDER, text_color=clr,
                anchor="w", height=34, corner_radius=4,
                command=lambda ma=m["team_a"], mb=m["team_b"]: self._select_match(ma, mb))
            btn.pack(fill="x", pady=1)
            self.match_btns.append(btn)
        # Auto-select first match
        if matches:
            self._select_match(matches[0]["team_a"], matches[0]["team_b"])

    def _select_match(self, team_a, team_b):
        self.selected_match = (team_a, team_b)
        for b in self.match_btns:
            b.configure(fg_color="transparent")
            if team_a in b.cget("text") and team_b in b.cget("text"):
                b.configure(fg_color=BORDER)

    def _show_welcome(self):
        for w in self.result_frame.winfo_children(): w.destroy()
        ctk.CTkLabel(self.result_frame, text="歡迎使用 2026 世界盃預測系統",
            font=ctk.CTkFont(size=18, weight="bold"), text_color=TEXT).pack(pady=(80,8))
        ctk.CTkLabel(self.result_frame, text="選擇日期 → 選擇對戰 → 選運彩玩法 → 開始分析",
            font=ctk.CTkFont(size=12), text_color=SUBTEXT).pack()
        ctk.CTkLabel(self.result_frame, text="系統使用蒙地卡羅模擬 + Poisson 分布 + Elo 評分",
            font=ctk.CTkFont(size=11), text_color=SUBTEXT).pack(pady=5)

    def _run_simulation(self):
        if not self.selected_match:
            messagebox.showwarning("提示","請先選擇對戰組合"); return
        team_a, team_b = self.selected_match
        num_sims = self.sim_var.get()
        bet_type = self.bet_var.get()

        # Loading
        for w in self.result_frame.winfo_children(): w.destroy()
        ctk.CTkLabel(self.result_frame, text="正在模擬分析...",
            font=ctk.CTkFont(size=14), text_color=TEXT).pack(pady=(80,5))
        bar = ctk.CTkProgressBar(self.result_frame, width=300, height=10, fg_color=BORDER, progress_color=ACCENT)
        bar.pack(); bar.start()

        def do():
            result = simulate_match(team_a, team_b, num_sims=num_sims)
            self.after(0, lambda: self._show_result(result, bet_type))
        threading.Thread(target=do, daemon=True).start()

    def _show_result(self, r, bet_type):
        for w in self.result_frame.winfo_children(): w.destroy()
        if not r: return

        a, b = r["team_a"], r["team_b"]
        wp = r["win_pct"]

        # Title
        ctk.CTkLabel(self.result_frame,
            text=f"{a} vs {b}  ({r['num_sims']}次模擬)",
            font=ctk.CTkFont(size=18, weight="bold"), text_color=TEXT).pack(pady=(12,3))

        # Strength + Form
        sf = ctk.CTkFrame(self.result_frame, fg_color="transparent")
        sf.pack(fill="x", padx=15, pady=5)
        ctk.CTkLabel(sf, text=f"戰力 {a}: {r['strength_a']} (近期狀態 {r['form_a']:+.1f})  |  {b}: {r['strength_b']} (近期狀態 {r['form_b']:+.1f})",
            font=ctk.CTkFont(size=10), text_color=SUBTEXT).pack()
        # Events
        ev = r.get('events', {})
        if ev:
            ctk.CTkLabel(sf, text=f"紅牌率: {ev['avg_red_cards']}/場  點球率: {ev['avg_penalties']}/場",
                font=ctk.CTkFont(size=9), text_color=SUBTEXT).pack()

        # Win probability bars
        ctk.CTkLabel(self.result_frame, text="勝率預測",
            font=ctk.CTkFont(size=13, weight="bold"), text_color=TEXT).pack(pady=(10,2))
        pf = ctk.CTkFrame(self.result_frame, fg_color="transparent")
        pf.pack(fill="x", padx=15, pady=3)
        for label, pct, color in [(a, wp["a"], GREEN), ("平局", wp["draw"], YELLOW), (b, wp["b"], RED)]:
            row = ctk.CTkFrame(pf, fg_color="transparent"); row.pack(fill="x", pady=1)
            ctk.CTkLabel(row, text=label, font=ctk.CTkFont(size=11), text_color=TEXT, width=70).pack(side="left")
            bar_frame = ctk.CTkFrame(row, fg_color=BORDER, corner_radius=4, height=16)
            bar_frame.pack(side="left", fill="x", expand=True, padx=6)
            bar_frame.pack_propagate(False)
            inner = ctk.CTkFrame(bar_frame, fg_color=color, corner_radius=4, width=int(pct*3), height=16)
            inner.pack(side="left"); inner.pack_propagate(False)
            ctk.CTkLabel(row, text=f"{pct}%", font=ctk.CTkFont(size=11, weight="bold"), text_color=color, width=45).pack(side="right")

        # Analysis by bet type
        if "綜合" in bet_type or "勝負" in bet_type:
            self._section("全場勝負分析",
                f"• {a} 勝率: {wp['a']}%  平局: {wp['draw']}%  {b} 勝率: {wp['b']}%\n"
                f"• 最佳正確比數: {r['best_score'][0]}:{r['best_score'][1]} ({r['best_score'][2]}%)")

        if "綜合" in bet_type or "讓分" in bet_type:
            txt = "• 亞洲讓分盤分析:\n"
            for h in ["-1.5","-1.0","-0.5","+0.5","+1.0","+1.5"]:
                k = f"a{h}"
                if k in r["handicaps"]:
                    txt += f"  {a} 讓 {h} 球: 過盤率 {r['handicaps'][k]['cover']}%\n"
            self._section("讓分盤分析", txt)

        if "綜合" in bet_type or "大小" in bet_type:
            ou = r["over_under"]
            self._section("大小球分析",
                f"• 大 1.5 球: {ou['over15']}%\n"
                f"• 大 2.5 球: {ou['over25']}%  小 2.5 球: {ou['under25']}%\n"
                f"• 大 3.5 球: {ou['over35']}%\n"
                f"• 平均總進球: {r['total_goals']['avg']} 球")

        if "綜合" in bet_type or "正確比數" in bet_type:
            txt = "\n".join([f"• {s} ({p}%)" for s,p in r["top_scores"]])
            self._section("正確比數 TOP 3", txt)

        if "綜合" in bet_type or "BTTS" in bet_type:
            bt = r["btts"]
            self._section("兩隊都進球 (BTTS)", f"• 是: {bt['yes']}%  否: {bt['no']}%")

        if "綜合" in bet_type or "半場" in bet_type:
            txt = "\n".join([f"• {s}: {p}%" for s,p in r["ht_ft"]])
            self._section("半場/全場 TOP 3", txt)

        if "綜合" in bet_type or "總進球" in bet_type:
            tg = r["total_goals"]
            items = [f"{k}球: {v}次" for k,v in tg["dist"].items()]
            self._section("總進球數分布", "  ".join(items))

        # Recommendations
        if r["recommendations"]:
            rec_text = "\n".join(r["recommendations"])
            self._section("推薦運彩策略", rec_text, color=YELLOW)

        self._disclaimer()

    def _section(self, title, text, color=TEXT):
        f = ctk.CTkFrame(self.result_frame, fg_color=CARD, border_color=BORDER, border_width=1, corner_radius=8)
        f.pack(fill="x", padx=12, pady=3)
        ctk.CTkLabel(f, text=title, font=ctk.CTkFont(size=12, weight="bold"),
            text_color=color).pack(anchor="w", padx=10, pady=(8,2))
        ctk.CTkLabel(f, text=text, font=ctk.CTkFont(size=10), text_color=SUBTEXT,
            justify="left").pack(anchor="w", padx=10, pady=(0,8))

    def _disclaimer(self):
        ctk.CTkLabel(self.result_frame,
            text="⚠️ 分析僅供參考，運彩投注有風險，請理性決策。",
            font=ctk.CTkFont(size=9), text_color="#64748B").pack(pady=(15,10))

def run():
    WorldCupApp().mainloop()
