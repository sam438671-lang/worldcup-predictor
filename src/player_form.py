# -*- coding: utf-8 -*-
"""48 隊完整球員資料庫 + 近期狀態（每位球員皆有數據）
格式: {球隊: [(姓名, 位置, 基礎評分, 近期狀態, 近5場進球, 近5場助攻, 上場%, 聯賽強度), ...]}"""

import random

# 聯賽強度
LIGA = {"英超":10,"西甲":9,"義甲":9,"德甲":8,"法甲":7,"荷甲":6,"葡超":6,"比甲":5,"巴甲":6,"阿甲":6,"MLS":5,"沙聯":4,"土超":5,"蘇超":5,"奧超":5,"瑞超":5,"捷甲":5,"克甲":4,"丹超":5,"挪超":4,"希超":4,"塞超":4,"日職":4,"K聯賽":4,"中超":3,"澳超":3,"墨超":5,"卡聯":3,"阿聯":3,"其他":3}

POS = {"FW":(75,95,1.2),"MF":(70,92,0.5),"DF":(65,90,0.2),"GK":(65,90,0.0)}

def _gen_form(base, pos, league_lvl, seed):
    """自動生成合理的近期狀態"""
    r = random.Random(seed)
    pos_range = POS.get(pos, (70,92,0.5))
    form = base + r.randint(-12, 8)
    form = max(pos_range[0]-5, min(pos_range[1]+5, form))
    goals = max(0, int(r.randint(0,5) * pos_range[2]))
    assists = max(0, int(r.randint(0,4) * pos_range[2] * 0.7))
    mins = r.randint(50, 98)
    return (base, form, goals, assists, mins, league_lvl)

# ===== 48 隊完整陣容 =====
SQUADS = {
    # ===== GROUP A =====
    "墨西哥": [
        ("G. Ochoa","GK",82),( "C. Montes","DF",80),( "J. Vasquez","DF",80),( "J. Sanchez","DF",79),( "J. Gallardo","DF",78),
        ("E. Alvarez","MF",84),( "L. Chavez","MF",82),( "O. Pineda","MF",80),( "L. Romo","MF",78),
        ("S. Gimenez","FW",85),( "H. Lozano","FW",82),( "R. Jimenez","FW",80),( "A. Vega","FW",78),
    ],
    "南非": [
        ("R. Goss","GK",75),( "R. Williams","DF",76),( "T. Mokoena","DF",77),( "S. Xulu","DF",74),( "A. Modiba","DF",73),
        ("T. Zwane","MF",78),( "S. Mthethwa","MF",76),( "M. Mvala","MF",75),( "T. Monare","MF",74),
        ("P. Tau","FW",79),( "L. Foster","FW",78),( "B. Tshabangu","FW",76),( "E. Makgopa","FW",75),
    ],
    "南韓": [
        ("Kim Seung-gyu","GK",80),( "Kim Min-jae","DF",86),( "Kim Young-gwon","DF",80),( "Seol Young-woo","DF",79),( "Lee Ki-je","DF",78),
        ("Lee Kang-in","MF",84),( "Hwang In-beom","MF",81),( ("Park Yong-woo","MF",79)),( "Lee Jae-sung","MF",80),( "Jung Woo-young","MF",78),
        ("Son Heung-min","FW",88),( "Hwang Hee-chan","FW",83),( "Cho Gue-sung","FW",80),( "Oh Hyeon-gyu","FW",78),
    ],
    "捷克": [
        ("M. Kovar","GK",79),( "V. Coufal","DF",81),( "T. Holes","DF",80),( "J. Zima","DF",78),( "D. Jurasek","DF",77),
        ("T. Soucek","MF",84),( "A. Barak","MF",81),( ("M. Sadilek","MF",80)),( "L. Provod","MF",79),( "O. Lingr","MF",78),
        ("P. Schick","FW",84),( "A. Hlozek","FW",80),( ("M. Chytil","FW",78)),( "V. Cerny","FW",77),
    ],
    # ===== GROUP B =====
    "加拿大": [
        ("M. Crepeau","GK",78),( "A. Davies","DF",87),( "A. Johnston","DF",80),( "D. Cornelius","DF",78),( ("S. Adekugbe","DF",77)),
        ("S. Eustaquio","MF",82),( "I. Kone","MF",79),( "J. Osorio","MF",78),( ("S. Piette","MF",77)),
        ("J. David","FW",85),( ("C. Larin","FW",80)),( "T. Buchanan","FW",80),( "L. Cavallini","FW",76),
    ],
    "波赫": [
        ("I. Sehic","GK",77),( "A. Hadziahmetovic","DF",78),( "S. Prevljak","DF",79),( "E. Civic","DF",76),( "S. Sanicanin","DF",75),
        ("M. Pjanic","MF",80),( ("R. Krunic","MF",79)),( "G. Cimirot","MF",77),( "A. Gojak","MF",76),
        ("E. Dzeko","FW",82),( "E. Demirovic","FW",80),( "S. Prevljak","FW",79),( "L. Menalo","FW",76),
    ],
    "卡達": [
        ("M. Barsham","GK",76),( "B. Khoukhi","DF",77),( "T. Salman","DF",76),( "H. Ahmed","DF",75),( "A. Hassan","DF",74),
        ("A. Afif","MF",80),( "A. Al-Haydos","MF",78),( "K. Boudiaf","MF",76),( ("A. Madibo","MF",75)),
        ("A. Ali","FW",80),( "M. Muntari","FW",78),( "A. Alaaeldin","FW",76),( "Y. Abdurisag","FW",75),
    ],
    "瑞士": [
        ("Y. Sommer","GK",85),( "M. Akanji","DF",85),( "F. Schar","DF",81),( "N. Elvedi","DF",80),( "R. Rodriguez","DF",80),( "S. Widmer","DF",79),
        ("G. Xhaka","MF",86),( "R. Freuler","MF",81),( "D. Zakaria","MF",81),( "M. Aebischer","MF",79),( "X. Shaqiri","MF",80),
        ("B. Embolo","FW",82),( "R. Vargas","FW",80),( "Z. Amdouni","FW",79),
    ],
    # ===== GROUP C =====
    "巴西": [
        ("Alisson","GK",88),( "Ederson","GK",86),
        ("Marquinhos","DF",86),( "E. Militao","DF",85),( "G. Magalhaes","DF",84),( "Danilo","DF",82),( "Bremer","DF",83),( "G. Arana","DF",81),
        ("Vinicius Jr","FW",92),( "Neymar","FW",90),( "Rodrygo","FW",87),( "Raphinha","FW",86),( "Endrick","FW",82),
        ("B. Guimaraes","MF",86),( "L. Paqueta","MF",84),( "Gerson","MF",82),( "Andre","MF",81),
    ],
    "摩洛哥": [
        ("Y. Bounou","GK",85),( "A. Hakimi","DF",87),( "N. Mazraoui","DF",83),( "N. Aguerd","DF",82),( "R. Saiss","DF",80),( "J. El Yamiq","DF",78),
        ("S. Amrabat","MF",82),( "A. Ounahi","MF",81),( "B. Diaz","MF",85),( "S. Amallah","MF",79),( "B. El Khannouss","MF",80),
        ("Y. En-Nesyri","FW",82),( "H. Ziyech","FW",82),( "A. Adli","FW",80),( "I. Abde","FW",79),
    ],
    "海地": [
        ("J. Duverger","GK",70),( "R. Ade","DF",71),( "C. Arcus","DF",69),( "A. Christian","DF",68),( "S. Lambese","DF",67),
        ("D. Etienne","MF",72),( "B. Alceus","MF",70),( "L. Francois","MF",69),( "C. Sainte","MF",73),
        ("F. Pierrot","FW",74),( "D. Jean","FW",72),( "M. Joly","FW",71),( "R. Borgelin","FW",70),
    ],
    "蘇格蘭": [
        ("A. Gunn","GK",79),( "A. Robertson","DF",84),( "K. Tierney","DF",81),( "J. Hendry","DF",79),( "R. Porteous","DF",78),( "N. Patterson","DF",77),
        ("S. McTominay","MF",83),( "J. McGinn","MF",82),( "B. Gilmour","MF",80),( "C. McGregor","MF",80),( "R. Christie","MF",79),
        ("L. Dykes","FW",78),( "C. Adams","FW",77),( "L. Shankland","FW",76),
    ],
    # ===== GROUP D =====
    "美國": [
        ("M. Turner","GK",81),( "A. Robinson","DF",82),( "S. Dest","DF",82),( "C. Richards","DF",80),( "T. Ream","DF",79),( "J. Scally","DF",78),
        ("C. Pulisic","FW",86),( "T. Weah","FW",81),( "R. Pepi","FW",82),( "F. Balogun","FW",82),( "B. Aaronson","FW",79),
        ("W. McKennie","MF",83),( "G. Reyna","MF",82),( "Y. Musah","MF",81),( "T. Adams","MF",82),( "L. de la Torre","MF",79),
    ],
    "巴拉圭": [
        ("C. Dominguez","GK",77),( "G. Gomez","DF",80),( "F. Balbuena","DF",79),( "J. Caceres","DF",77),( "S. Arzamendia","DF",76),
        ("M. Almiron","MF",83),( "R. Sanchez","MF",80),( "M. Villasanti","MF",79),( "D. Gomez","MF",78),( "B. Samudio","MF",77),
        ("J. Enciso","FW",82),( ("A. Sanabria","FW",80)),( "G. Avalos","FW",78),( "S. Salcedo","FW",76),
    ],
    "澳洲": [
        ("M. Ryan","GK",80),( "H. Souttar","DF",79),( "K. Rowles","DF",77),( "A. Behich","DF",76),( "N. Atkinson","DF",75),
        ("J. Irvine","MF",78),( "A. Hrustic","MF",77),( "R. McGree","MF",78),( ("K. Baccus","MF",76)),
        ("C. Goodwin","FW",78),( "M. Duke","FW",76),( ("N. Irankunda","FW",77)),( "B. Borello","FW",75),
    ],
    "土耳其": [
        ("M. Gunok","GK",80),( "M. Demiral","DF",82),( "C. Soyuncu","DF",80),( "F. Kadioglu","DF",81),( "Z. Celik","DF",79),( "A. Bardakci","DF",78),
        ("H. Calhanoglu","MF",85),( "A. Guler","MF",84),( ("O. Kokcu","MF",82)),( "S. Ozcan","MF",80),( "I. Yuksek","MF",79),
        ("K. Akturkoglu","FW",83),( "B. Yilmaz","FW",80),( "C. Under","FW",79),( "E. Dervisoglu","FW",77),
    ],
    # ===== GROUP E =====
    "德國": [
        ("M. Neuer","GK",86),( "M. Ter Stegen","GK",85),
        ("A. Rudiger","DF",86),( "J. Tah","DF",84),( "M. Mittelstadt","DF",82),( "B. Henrichs","DF",82),( "N. Schlotterbeck","DF",83),( "R. Raum","DF",81),
        ("J. Musiala","MF",90),( "F. Wirtz","MF",89),( "J. Kimmich","MF",88),( "L. Sane","FW",86),( "K. Havertz","FW",85),( "N. Fullkrug","FW",83),( "S. Gnabry","FW",84),
    ],
    "庫拉索": [
        ("E. Room","GK",68),( "J. Bacuna","DF",72),( "C. Martina","DF",70),( "D. Lachman","DF",69),( "S. Floranus","DF",68),
        ("L. Bacuna","MF",71),( "K. Felida","MF",69),( "G. Roemeratoe","MF",68),( ("J. Antonia","MF",67)),
        ("R. Janga","FW",70),( ("C. Benschop","FW",69)),( "J. Arias","FW",68),( ("G. van der Wielen","FW",67)),
    ],
    "象牙海岸": [
        ("Y. Fofana","GK",79),( "E. Ndicka","DF",83),( "O. Diomande","DF",82),( "W. Boly","DF",80),( "G. Konan","DF",79),( "S. Aurier","DF",80),
        ("F. Kessie","MF",84),( "S. Fofana","MF",82),( "I. Sangare","MF",81),( "J. Boga","MF",80),( "M. Gradel","MF",79),
        ("S. Adingra","FW",83),( "K. Konate","FW",81),( "S. Haller","FW",81),( "J. Bamba","FW",79),
    ],
    "厄瓜多": [
        ("H. Galindez","GK",77),( "P. Estupinan","DF",83),( "W. Pacho","DF",81),( "F. Torres","DF",79),( "A. Preciado","DF",78),( "P. Hincapie","DF",80),
        ("M. Caicedo","MF",85),( "K. Paez","MF",80),( "C. Gruezo","MF",79),( ("J. Mendez","MF",78)),( "A. Franco","MF",77),
        ("E. Valencia","FW",82),( "K. Rodriguez","FW",78),( ("J. Sarmiento","FW",77)),( "E. Lastre","FW",76),
    ],
    # ===== GROUP F =====
    "荷蘭": [
        ("B. Verbruggen","GK",82),( "V. van Dijk","DF",89),( "N. Ake","DF",84),( "J. Timber","DF",83),( "M. de Ligt","DF",83),( "D. Dumfries","DF",84),( "L. Geertruida","DF",81),
        ("F. de Jong","MF",87),( "R. Gravenberch","MF",84),( "X. Simons","MF",85),( "T. Koopmeiners","MF",83),( "J. Veerman","MF",82),
        ("C. Gakpo","FW",86),( "M. Depay","FW",84),( "D. Malen","FW",83),( "W. Weghorst","FW",80),
    ],
    "日本": [
        ("Z. Suzuki","GK",80),( "T. Tomiyasu","DF",84),( "K. Itakura","DF",81),( ("Y. Sugawara","DF",80)),( "H. Ito","DF",81),( "S. Taniguchi","DF",79),
        ("K. Mitoma","FW",86),( "T. Kubo","FW",85),( "D. Kamada","MF",83),( "W. Endo","MF",83),( "R. Doan","MF",82),( "H. Morita","MF",81),( "J. Ito","MF",80),
        ("D. Maeda","FW",80),( "A. Ueda","FW",79),
    ],
    "瑞典": [
        ("R. Olsen","GK",80),( "V. Lindelof","DF",82),( "I. Hien","DF",81),( ("L. Augustinsson","DF",79)),( "E. Holm","DF",79),( "G. Gudmundsson","DF",78),
        ("A. Isak","FW",87),( "V. Gyokeres","FW",86),( "D. Kulusevski","MF",85),( "A. Elanga","FW",81),( "M. Svanberg","MF",80),( "J. Cajuste","MF",79),( "E. Forsberg","MF",80),
        ("R. Quaison","FW",78),( ("A. Ekdal","DF",77)),
    ],
    "突尼西亞": [
        ("B. Ben Said","GK",77),( "M. Talbi","DF",78),( "Y. Meriah","DF",77),( "A. Abdi","DF",76),( "W. Kechrida","DF",75),
        ("E. Skhiri","MF",81),( "A. Laidouni","MF",79),( "H. Mejbri","MF",80),( "F. Sassi","MF",78),( "M. Ben Romdhane","MF",77),
        ("Y. Msakni","FW",78),( "T. Yassine","FW",77),( "S. Jaziri","FW",76),( "H. Khazri","FW",76),
    ],
    # ===== GROUP G =====
    "比利時": [
        ("T. Courtois","GK",89),( "W. Faes","DF",80),( "Z. Debast","DF",80),( "T. Castagne","DF",81),( "A. Theate","DF",80),( "J. Vertonghen","DF",79),
        ("K. De Bruyne","MF",91),( "A. Onana","MF",82),( "Y. Tielemans","MF",83),( ("O. Mangala","MF",80)),( "C. De Ketelaere","MF",82),
        ("R. Lukaku","FW",85),( "J. Doku","FW",84),( "L. Trossard","FW",83),( "M. Batshuayi","FW",78),
    ],
    "埃及": [
        ("M. El Shenawy","GK",79),( "A. Hegazi","DF",79),( "M. Abdelmonem","DF",78),( "A. Fotouh","DF",77),( "O. Gaber","DF",76),
        ("M. Elneny","MF",80),( "E. Ashour","MF",79),( "H. Fathy","MF",78),( "Z. Kamal","MF",77),
        ("M. Salah","FW",91),( "O. Marmoush","FW",85),( ("M. Mohamed","FW",79)),( "T. Mohamed","FW",78),( "Ahmed Hassan","FW",80),
    ],
    "伊朗": [
        ("A. Beiranvand","GK",78),( "H. Kanani","DF",78),( "S. Khalilzadeh","DF",77),( "M. Mohammadi","DF",76),( "R. Rezaeian","DF",77),
        ("S. Ghoddos","MF",79),( "A. Nourollahi","MF",78),( "M. Karimi","MF",77),( "S. Ezatolahi","MF",78),
        ("M. Taremi","FW",84),( "S. Azmoun","FW",83),( "A. Jahanbakhsh","FW",79),( "M. Mohebi","FW",77),( "R. Asadi","FW",76),
    ],
    "紐西蘭": [
        ("A. Paulsen","GK",73),( "M. Boxall","DF",74),( "T. Smith","DF",73),( "L. Cacace","DF",74),( "D. Ingham","DF",72),
        ("S. Singh","MF",76),( "M. Stamenic","MF",75),( "J. Bell","MF",74),( "C. Lewis","MF",73),
        ("C. Wood","FW",81),( ("B. Waine","FW",74)),( "M. Garbett","FW",73),( "E. Just","FW",72),
    ],
    # ===== GROUP H =====
    "西班牙": [
        ("U. Simon","GK",85),( "D. Carvajal","DF",85),( "P. Cubarsi","DF",83),( "A. Laporte","DF",84),( "A. Balde","DF",84),( ("O. Mingueza","DF",81)),
        ("Rodri","MF",91),( "Pedri","MF",88),( "Gavi","MF",86),( "D. Olmo","MF",85),( ("F. Ruiz","MF",84)),( "M. Zubimendi","MF",83),
        ("L. Yamal","FW",89),( "N. Williams","FW",87),( "A. Morata","FW",84),( "M. Oyarzabal","FW",83),
    ],
    "維德角": [
        ("D. Tavares","GK",72),( "S. Moreira","DF",73),( "L. Semedo","DF",73),( "D. Borges","DF",71),( "J. Monteiro","DF",74),
        ("R. Mendes","MF",76),( "B. Varela","MF",75),( "W. Semedo","MF",74),( ("N. Mendes","MF",73)),
        ("G. Rodrigues","FW",75),( ("Z. Sanches","FW",74)),( "D. Tavares","FW",73),( "H. Borges","FW",72),
    ],
    "沙烏地阿拉伯": [
        ("M. Al-Owais","GK",77),( "H. Tambakti","DF",77),( "A. Al-Bulaihi","DF",77),( ("Y. Al-Shahrani","DF",76)),( ("S. Al-Ghannam","DF",75)),
        ("S. Al-Dawsari","MF",80),( ("M. Kanno","MF",78)),( "A. Al-Malki","MF",77),( "N. Al-Dawsari","MF",76),
        ("F. Al-Buraikan","FW",78),( ("A. Al-Hamddan","FW",77)),( "H. Al-Aboud","FW",76),( "A. Radif","FW",75),
    ],
    "烏拉圭": [
        ("S. Rochet","GK",82),( "R. Araujo","DF",86),( "J. Gimenez","DF",84),( "M. Olivera","DF",81),( "N. Nandez","DF",81),( "G. Varela","DF",79),
        ("F. Valverde","MF",89),( "R. Bentancur","MF",83),( "M. Ugarte","MF",83),( "G. de Arrascaeta","MF",82),( "N. de la Cruz","MF",80),
        ("D. Nunez","FW",84),( "F. Pellistri","FW",80),( "M. Araujo","FW",79),( "L. Suarez","FW",82),
    ],
    # ===== GROUP I =====
    "法國": [
        ("M. Maignan","GK",87),( "W. Saliba","DF",87),( "D. Upamecano","DF",84),( "T. Hernandez","DF",86),( "J. Kounde","DF",85),( ("B. Pavard","DF",84)),( "I. Konate","DF",84),
        ("K. Mbappe","FW",93),( "O. Dembele","FW",86),( "M. Thuram","FW",84),( "R. Kolo Muani","FW",83),( "K. Coman","FW",82),
        ("A. Griezmann","MF",87),( "E. Camavinga","MF",85),( "A. Tchouameni","MF",86),( ("Y. Fofana","MF",83)),
    ],
    "塞內加爾": [
        ("E. Mendy","GK",84),( "K. Koulibaly","DF",84),( "A. Diallo","DF",80),( "M. Niakhate","DF",80),( "F. Ballo-Toure","DF",78),( "Y. Sabaly","DF",79),
        ("S. Mane","FW",86),( "N. Jackson","FW",84),( "I. Sarr","FW",82),( "B. Dieng","FW",78),( "C. Diatta","FW",77),
        ("P. M. Sarr","MF",81),( "I. Gueye","MF",82),( "L. Camara","MF",80),( "P. Ciss","MF",79),
    ],
    "伊拉克": [
        ("J. Hassan","GK",75),( "A. Adnan","DF",75),( "M. Ali","DF",76),( "A. Faez","DF",74),( "R. Sulaka","DF",74),
        ("Z. Iqbal","MF",77),( ("A. Al-Ammari","MF",76)),( "I. Bayesh","MF",75),( "A. Jasim","MF",76),
        ("A. Hussein","FW",78),( ("M. Qasim","FW",76)),( ("A. Yaseen","FW",75)),( "H. Ali","FW",75),
    ],
    "挪威": [
        ("O. Nyland","GK",80),( "K. Ajer","DF",80),( "A. Hanche-Olsen","DF",79),( ("L. Ostigard","DF",78)),( "J. Ryerson","DF",79),( ("D. Wolfe","DF",77)),
        ("E. Haaland","FW",93),( "A. Sorloth","FW",84),( "O. Bobb","FW",82),( ("J. Larsen","FW",80)),( "E. Celina","FW",78),
        ("M. Odegaard","MF",88),( "S. Berge","MF",82),( ("K. Thorstvedt","MF",80)),( "O. Solbakken","MF",79),
    ],
    # ===== GROUP J =====
    "阿根廷": [
        ("E. Martinez","GK",88),( "C. Romero","DF",86),( "N. Otamendi","DF",83),( "N. Molina","DF",82),( "N. Tagliafico","DF",81),( ("L. Martinez Quarta","DF",80)),( "G. Montiel","DF",80),
        ("L. Messi","FW",94),( "L. Martinez","FW",89),( "J. Alvarez","FW",87),( ("A. Garnacho","FW",82)),( "A. Di Maria","FW",82),
        ("E. Fernandez","MF",86),( "A. Mac Allister","MF",85),( "R. De Paul","MF",84),( ("L. Paredes","MF",82)),( "G. Lo Celso","MF",81),
    ],
    "阿爾及利亞": [
        ("A. Mandi","GK",80),( "A. Ait-Nouri","DF",82),( "R. Bensebaini","DF",80),( "M. Tougai","DF",78),( "Y. Atal","DF",78),
        ("I. Bennacer","MF",83),( "R. Cherki","MF",81),( "H. Aouar","MF",80),( "R. Zerrouki","MF",78),( "N. Bentaleb","MF",77),
        ("R. Mahrez","FW",84),( "A. Gouiri","FW",80),( "M. Amoura","FW",79),( "B. Bounedjah","FW",78),
    ],
    "奧地利": [
        ("P. Pentz","GK",80),( "D. Alaba","DF",85),( "P. Lienhart","DF",80),( "S. Posch","DF",80),( "M. Wober","DF",79),( "A. Prass","DF",79),
        ("K. Laimer","MF",83),( "M. Sabitzer","MF",83),( "C. Baumgartner","MF",82),( "N. Seiwald","MF",80),( "X. Schlager","MF",79),
        ("M. Arnautovic","FW",80),( "M. Gregoritsch","FW",79),( "J. Adamu","FW",77),( ("P. Wimmer","FW",76)),
    ],
    "約旦": [
        ("A. Lafi","GK",73),( "E. Haddad","DF",74),( "Y. Abu Arab","DF",73),( "M. Al-Dmeiri","DF",72),( "B. Yaseen","DF",72),
        ("M. Al-Taamari","MF",78),( ("N. Al-Rawabdeh","MF",75)),( "A. Olwan","MF",75),( "M. Abu Zrayq","MF",74),
        ("Y. Al-Naimat","FW",76),( ("A. Al-Mardi","FW",74)),( ("M. Samir","FW",73)),( "H. Al-Dardour","FW",73),
    ],
    # ===== GROUP K =====
    "葡萄牙": [
        ("D. Costa","GK",85),( "R. Dias","DF",88),( "N. Mendes","DF",84),( "J. Cancelo","DF",85),( "G. Inacio","DF",83),( ("A. Silva","DF",81)),
        ("C. Ronaldo","FW",90),( "R. Leao","FW",87),( "D. Jota","FW",85),( ("P. Neto","FW",83)),( "G. Ramos","FW",84),
        ("B. Fernandes","MF",88),( "B. Silva","MF",88),( "Vitinha","MF",85),( ("J. Palhinha","MF",84)),( "O. Neves","MF",83),
    ],
    "剛果民主共和國": [
        ("L. Mpasi","GK",72),( "A. Masuaku","DF",77),( "C. Mbemba","DF",78),( "G. Kilonda","DF",74),( "D. Batubinsika","DF",73),
        ("S. Moutoussamy","MF",78),( "G. Kakuta","MF",77),( ("E. Kayembe","MF",76)),( "C. Pickel","MF",75),
        ("C. Bakambu","FW",80),( "Y. Wissa","FW",82),( "M. Elia","FW",76),( ("J. Banza","FW",75)),
    ],
    "烏茲別克": [
        ("U. Yusupov","GK",75),( "A. Khusanov","DF",76),( "H. Alikulov","DF",75),( "F. Sayfiyev","DF",74),( "R. Ashurmatov","DF",73),
        ("J. Masharipov","MF",78),( ("O. Urunov","MF",77)),( "O. Shukurov","MF",76),( "A. Turgunboev","MF",75),
        ("E. Shomurodov","FW",80),( ("A. Fayzullaev","FW",77)),( "B. Abdukhalikov","FW",76),( "I. Sergeyev","FW",75),
    ],
    "哥倫比亞": [
        ("C. Vargas","GK",81),( "D. Sanchez","DF",81),( "J. Lucumi","DF",80),( "D. Munoz","DF",81),( "J. Mojica","DF",79),( "Y. Mosquera","DF",78),
        ("L. Diaz","FW",88),( "J. Duran","FW",83),( "J. Rodriguez","MF",84),( "J. Lerma","MF",82),( "R. Rios","MF",81),( ("J. Quintero","MF",80)),( "W. Barrios","MF",80),
        ("R. Borre","FW",79),( ("M. Uribe","FW",78)),
    ],
    # ===== GROUP L =====
    "英格蘭": [
        ("J. Pickford","GK",84),( "J. Stones","DF",85),( "T. Alexander-Arnold","DF",85),( "M. Guehi","DF",83),( "K. Walker","DF",84),( ("L. Colwill","DF",82)),
        ("H. Kane","FW",91),( "B. Saka","FW",88),( "P. Foden","FW",87),( "C. Palmer","MF",86),( ("O. Watkins","FW",84)),( "I. Toney","FW",82),
        ("J. Bellingham","MF",90),( "D. Rice","MF",87),( ("C. Gallagher","MF",83)),( "K. Mainoo","MF",82),
    ],
    "克羅埃西亞": [
        ("D. Livakovic","GK",83),( "J. Gvardiol","DF",87),( "J. Stanisic","DF",81),( "J. Sutalo","DF",81),( "B. Sosa","DF",80),( "M. Pongracic","DF",79),
        ("L. Modric","MF",88),( "M. Kovacic","MF",84),( "M. Brozovic","MF",83),( "M. Baturina","MF",80),( "N. Vlasic","MF",81),( ("L. Sucic","MF",78)),
        ("A. Kramaric","FW",82),( "I. Perisic","FW",82),( "B. Petkovic","FW",78),( ("M. Pasalic","FW",80)),
    ],
    "迦納": [
        ("L. Ati-Zigi","GK",76),( "M. Salisu","DF",80),( "A. Seidu","DF",78),( ("G. Mensah","DF",77)),( "T. Lamptey","DF",79),
        ("M. Kudus","MF",85),( "T. Partey","MF",82),( ("K. Ofori","MF",79)),( "M. Ashimeru","MF",78),( ("E. Owusu","MF",77)),
        ("A. Semenyo","FW",80),( "I. Osman","FW",81),( ("K. Sulemana","FW",78)),( "B. Tetteh","FW",77),
    ],
    "巴拿馬": [
        ("O. Mosquera","GK",74),( "M. Murillo","DF",76),( "A. Godoy","DF",75),( "E. Davis","DF",74),( ("C. Harvey","DF",73)),
        ("A. Carrasquilla","MF",78),( ("J. Rodriguez","MF",77)),( "C. Martinez","MF",76),( "A. Quintero","MF",75),
        ("J. Fajardo","FW",76),( ("I. Diaz","FW",75)),( "T. Barcenas","FW",74),( "A. Arroyo","FW",73),
    ],
}

def get_all_players(team):
    """取得隊伍所有球員 (含自動生成的近期狀態)"""
    squad = SQUADS.get(team, [])
    players = []
    for i, p in enumerate(squad):
        name = p[0]; pos = p[1]; base = p[2]
        form = _gen_form(base, pos, LIGA.get("其他",3), hash(f"{team}{name}{i}") % 10000)
        players.append((name, pos, form[0], form[1], form[2], form[3], form[4], form[5]))
    return players

def get_team_form_boost(team):
    """計算整隊近期狀態加成（全員加權）"""
    players = get_all_players(team)
    if not players: return 0
    weighted = []
    for p in players:
        wr = calculate_weighted_rating(p[2], p[3], p[4], p[5], p[6], p[7])
        weighted.append(wr)
    # 取前11人（先發陣容）
    top11 = sorted(weighted, reverse=True)[:11]
    avg_top11 = sum(top11) / 11
    return max(0, (avg_top11 - 55) / 8)  # 55→0, 95→5

def calculate_weighted_rating(base_rating, form, goals, assists, minutes_pct, league_lvl):
    """加權計算球員實際戰力 (0-100)"""
    goal_bonus = min(goals * 2.5, 12)
    assist_bonus = min(assists * 2, 10)
    minute_bonus = (minutes_pct - 50) / 5
    LEAGUE_STRENGTH = {10:1.0,9:0.97,8:0.94,7:0.90,6:0.87,5:0.84,4:0.81,3:0.78,2:0.75}
    league_mult = LEAGUE_STRENGTH.get(league_lvl, 0.85)
    # 調整公式讓加權分數維持在 60-95 範圍
    weighted = (base_rating * 0.55 + form * 0.25 + (goal_bonus + assist_bonus) * 1.2 +
               minute_bonus * 0.3) * league_mult + 5  # +5 基數修正
    return round(weighted, 1)
