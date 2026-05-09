import os

# 画面設定
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
FPS = 60

# カラー
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (220, 60, 60)
BRIGHT_RED = (255, 80, 80)
DARK_RED = (120, 30, 30)
GREEN = (80, 220, 80)
YELLOW = (255, 220, 60)
BLUE = (60, 60, 220)

# フォント設定
JAPANESE_FONT_PATH = "C:\\Windows\\Fonts\\msgothic.ttc"

import sys

# パス設定
if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
    # PyInstallerの実行ファイルから起動された場合のパス
    BASE_DIR = sys._MEIPASS
else:
    # 通常のPythonスクリプトから起動された場合のパス
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ASSETS_DIR = os.path.join(BASE_DIR, "assets")
BG_DIR = os.path.join(ASSETS_DIR, "bg")
SPRITES_DIR = os.path.join(ASSETS_DIR, "sprites")
SOUNDS_DIR = os.path.join(ASSETS_DIR, "sounds")

# モンスター設定
MONSTER_TYPES = {
    "slime": {
        "name": "スライム",
        "sprite_path": os.path.join(SPRITES_DIR, "スライム"),
        "difficulty": "easy"
    },
    "kobold": {
        "name": "コボルト",
        "sprite_path": os.path.join(SPRITES_DIR, "コボルト"),
        "difficulty": "easy"
    },
    "zombie": {
        "name": "ゾンビ",
        "sprite_path": os.path.join(SPRITES_DIR, "ゾンビ"),
        "difficulty": "medium"
    },
    "dragon": {
        "name": "ドラゴン",
        "sprite_path": os.path.join(SPRITES_DIR, "ドラゴン"),
        "difficulty": "hard"
    }
}

# タイピングデータ: (用語, 日本語説明表示, タイピングさせるローマ字)
# ローマ字は pykakasi + ー→- 変換で生成
TYPING_DATA = {
    "easy": [
        ("ビット (bit)",
         "データの最小単位。０か１の状態を表す。",
         "de-tanosaisyoutanni.0ka1nojoutaiwoarawasu."),
        ("バイト (Byte)",
         "８ビットをまとめた単位。",
         "8bittowomatometatanni."),
        ("OS",
         "ハードウェアとソフトウェアを管理する基本ソフト。",
         "ha-doweatosofutoweawokanrisurukihonsofuto."),
        ("CPU",
         "計算や命令の制御を行うコンピュータの頭脳。",
         "keisannyameireinoseigyowookonaukonnpyu-tanozunou."),
        ("メモリ",
         "データを一時的に記憶する作業場所。",
         "de-tawoichijitekinikiokusurusagyoubasyo."),
        ("ストレージ",
         "電源を切ってもデータを保存できる記憶装置。",
         "denngennwokittemode-tawohozonndekirukiokusouchi."),
        ("LAN",
         "限られた範囲のネットワーク。",
         "kagiraretahanninonettowa-ku."),
        ("プロトコル",
         "通信のための取り決め事。",
         "tuusinnnotamenotorikimegoto."),
        ("IPアドレス",
         "ネットワーク上の機器を識別する番号。",
         "nettowa-kujonokikiwosikibetusurubanngou."),
        ("ブラウザ",
         "ウェブサイトを閲覧するソフト。",
         "webusaitowoetsuransurusohuto."),
        ("クラウド",
         "ネット越しにサービスを利用する仕組み。",
         "nettogoshinisa-bisuworiyousurushikumi."),
        ("マルウェア",
         "コンピュータに悪影響を与える悪意あるソフトの総称。",
         "konnpyu-taniakueikyouwoataeruakuiarusohutonosousou."),
    ],
    "medium": [
        ("2進数",
         "０と１だけで数値を表現する方法。",
         "0to1dakedesuuchiwohyougennsuruhouhou."),
        ("論理演算",
         "ＡＮＤやＯＲなどの論理的な計算。",
         "ANDyaORnadonoronritekinakeisann."),
        ("アルゴリズム",
         "問題を解くための手順や処理の流れ。",
         "mondaiwotokutamenotejunnyashorinonagare."),
        ("変数",
         "プログラム内で値を格納する箱。",
         "puroguramunaideataiwokakunousuruhako."),
        ("配列",
         "同じ型のデータを番号で管理する構造。",
         "onajikatanode-tawobanngoudekannrisurukouzou."),
        ("関数",
         "特定の処理をひとまとめにしたもの。",
         "tokuteinoshoriwohitomatomenishitamono."),
        ("データベース",
         "データを整理・蓄積し検索しやすくした仕組み。",
         "de-tawoseirichikusekishikensakushiyasukushitashikumi."),
        ("SQL",
         "リレーショナルデータベースを操作する言語。",
         "rire-shonarude-tabe-suwosousasurugenngo."),
        ("ルータ",
         "異なるネットワーク同士を接続する装置。",
         "kotonarunettowa-kudoushiwosetsuzokusurusouchi."),
        ("パケット",
         "データを分割して送受信する単位。",
         "de-tawobunnkatusitesoujusinnsurutanni."),
        ("暗号化",
         "第三者に内容が分からないようデータを変換する。",
         "daisanshaninaiyougawakaranaiyoude-tawohennkannsuru."),
        ("公開鍵暗号",
         "公開鍵と秘密鍵のペアを使う暗号化の仕組み。",
         "koukaikagitohimitsukaginopeawotsukauangoukanosikumi."),
        ("ファイアウォール",
         "外部からの不正な通信を遮断する防御システム。",
         "gaibukaranofuseinnatuusinnwosadansurubougyosisutemu."),
        ("バックアップ",
         "故障に備えてデータを別の場所に保存すること。",
         "koshounisonaetede-tawobetsunobashonihozonnsurukoto."),
        ("API",
         "ソフトウェア同士が機能を共有するための窓口。",
         "sofutoweadoushigakinouwokyouyuusurutamenomadoguchi."),
    ],
    "hard": [
        ("浮動小数点数",
         "大きな数や小さな小数を効率よく表す形式。",
         "ookinakazuyachiisanashousuuwokouritsuyokuarawasukeisiki."),
        ("スタックとキュー",
         "後入れ先出しと先入れ先出しによるデータ構造。",
         "atoiresakidasitosakiiresakidasiniyorude-takouzou."),
        ("2分探索",
         "ソート済みデータで効率よく目的のデータを探す手法。",
         "so-tosumide-tadekouritsuyokumokutekinode-tawosagasusushuhou."),
        ("計算量",
         "処理にかかる時間やメモリ量を示す指標。",
         "shorinikakarujikannyamemoriryouwoshimesushihyou."),
        ("仮想メモリ",
         "メモリ不足時にストレージの一部をメモリとして扱う技術。",
         "memorifusokujinisutore-jinoichibuwomemoritositeatukaugijutu."),
        ("キャッシュメモリ",
         "ＣＰＵと主記憶の速度差を埋める高速メモリ。",
         "CPUtoshukiokunosokudosawoumerukousokumemori."),
        ("トランザクション",
         "データベースで一連の処理を不可分の単位として扱うこと。",
         "de-tabe-sudeichirennoshoriwofukabunnotannitositeatukaukoto."),
        ("正規化",
         "データの重複をなくしテーブルを整理する手法。",
         "de-tanochoufukuwonakusite-buruwoseirisurushuhou."),
        ("DNS",
         "ドメイン名とIPアドレスを対応させる仕組み。",
         "domeinnmeitoIPadoresuwotaiousaserusikumi."),
        ("OSI参照モデル",
         "通信機能を7つの階層に分けて定義した国際標準モデル。",
         "tuusinnkinouwo7tsunokaisouniwaketeteigisitatokusaihyoujunnmoderu."),
        ("多要素認証",
         "複数の要素を組み合わせて行う認証方式。",
         "fukusuunoyousowokumiawaseteokonauninnshouhoushiki."),
        ("アジャイル開発",
         "小さな単位で開発とリリースを繰り返す手法。",
         "chiisanatannidekaihatsutoriri-suwokurikaesushuhou."),
    ],
}
