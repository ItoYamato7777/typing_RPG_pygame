import time
from .game_config import *

# ローマ字の複数入力対応テーブル
# 同じ文字に対して、複数のローマ字を許容する
# key: 正規ローマ字, value: 受け入れる代替ローマ字リスト (正規も含む)
ROMAJI_ALTS = {
    # さ行
    "sa": ["sa"],
    "si": ["si", "shi", "ci"],
    "shi": ["si", "shi", "ci"],
    "su": ["su"],
    "se": ["se", "ce"],
    "so": ["so"],
    # た行
    "ta": ["ta"],
    "ti": ["ti", "chi"],
    "chi": ["ti", "chi"],
    "tu": ["tu", "tsu"],
    "tsu": ["tu", "tsu"],
    "te": ["te"],
    "to": ["to"],
    # じ
    "zi": ["zi", "ji"],
    "ji": ["zi", "ji"],
    # ず
    "zu": ["zu", "du"],
    "du": ["zu", "du"],
    # ぢ
    "di": ["di", "dzi"],
    # ふ
    "hu": ["hu", "fu"],
    "fu": ["hu", "fu"],
    # じゃ行
    "zya": ["zya", "jya", "ja", "zixya", "zilya", "jixya", "jilya"],
    "jya": ["zya", "jya", "ja", "zixya", "zilya", "jixya", "jilya"],
    "ja": ["zya", "jya", "ja", "zixya", "zilya", "jixya", "jilya"],
    # じゅ行
    "zyu": ["zyu", "jyu", "ju", "zixyu", "zilyu", "jixyu", "jilyu"],
    "jyu": ["zyu", "jyu", "ju", "zixyu", "zilyu", "jixyu", "jilyu"],
    "ju": ["zyu", "jyu", "ju", "zixyu", "zilyu", "jixyu", "jilyu"],
    # じょ行
    "zyo": ["zyo", "jyo", "jo", "zixyo", "zilyo", "jixyo", "jilyo"],
    "jyo": ["zyo", "jyo", "jo", "zixyo", "zilyo", "jixyo", "jilyo"],
    "jo": ["zyo", "jyo", "jo", "zixyo", "zilyo", "jixyo", "jilyo"],
    # しゃ行
    "sya": ["sya", "sha", "sixya", "silya", "shixya", "shilya"],
    "sha": ["sya", "sha", "sixya", "silya", "shixya", "shilya"],
    # しゅ行
    "syu": ["syu", "shu", "sixyu", "silyu", "shixyu", "shilyu"],
    "shu": ["syu", "shu", "sixyu", "silyu", "shixyu", "shilyu"],
    # しょ行
    "syo": ["syo", "sho", "sixyo", "silyo", "shixyo", "shilyo"],
    "sho": ["syo", "sho", "sixyo", "silyo", "shixyo", "shilyo"],
    # ちゃ行
    "tya": ["tya", "cha", "cya", "tixya", "tilya", "chixya", "chilya"],
    "cha": ["tya", "cha", "cya", "tixya", "tilya", "chixya", "chilya"],
    # ちゅ行
    "tyu": ["tyu", "chu", "cyu", "tixyu", "tilyu", "chixyu", "chilyu"],
    "chu": ["tyu", "chu", "cyu", "tixyu", "tilyu", "chixyu", "chilyu"],
    # ちょ行
    "tyo": ["tyo", "cho", "cyo", "tixyo", "tilyo", "chixyo", "chilyo"],
    "cho": ["tyo", "cho", "cyo", "tixyo", "tilyo", "chixyo", "chilyo"],
    # ぢゃ・ぢゅ・ぢょ
    "dya": ["dya", "dja", "dixya", "dilya"],
    "dyu": ["dyu", "dju", "dixyu", "dilyu"],
    "dyo": ["dyo", "djo", "dixyo", "dilyo"],
    # づ
    "dzu": ["dzu", "zu"],
    # ん
    "nn": ["nn", "n", "xn"],
    # か、き、く、け、こ
    "ka": ["ka", "ca"],
    "ku": ["ku", "cu", "qu"],
    "ko": ["ko", "co"],
    # ぎゃ、ぎゅ、ぎょ
    "gya": ["gya", "gixya", "gilya"],
    "gyu": ["gyu", "gixyu", "gilyu"],
    "gyo": ["gyo", "gixyo", "gilyo"],
    # にゃ、にゅ、にょ
    "nya": ["nya", "nixya", "nilya"],
    "nyu": ["nyu", "nixyu", "nilyu"],
    "nyo": ["nyo", "nixyo", "nilyo"],
    # ひゃ、ひゅ、ひょ
    "hya": ["hya", "hixya", "hilya"],
    "hyu": ["hyu", "hixyu", "hilyu"],
    "hyo": ["hyo", "hixyo", "hilyo"],
    # びゃ、びゅ、びょ
    "bya": ["bya", "bixya", "bilya"],
    "byu": ["byu", "bixyu", "bilyu"],
    "byo": ["byo", "bixyo", "bilyo"],
    # ぴゃ、ぴゅ、ぴょ
    "pya": ["pya", "pixya", "pilya"],
    "pyu": ["pyu", "pixyu", "pilyu"],
    "pyo": ["pyo", "pixyo", "pilyo"],
    # みゃ、みゅ、みょ
    "mya": ["mya", "mixya", "milya"],
    "myu": ["myu", "mixyu", "milyu"],
    "myo": ["myo", "mixyo", "milyo"],
    # りゃ、りゅ、りょ
    "rya": ["rya", "rixya", "rilya"],
    "ryu": ["ryu", "rixyu", "rilyu"],
    "ryo": ["ryo", "rixyo", "rilyo"],
    # ふぁ、ふぃ、ふぇ、ふぉ
    "fa": ["fa", "hwa", "huxa", "hula", "fuxa", "fula"],
    "fi": ["fi", "hwi", "huxi", "huli", "fuxi", "fuli"],
    "fe": ["fe", "hwe", "huxe", "hule", "fuxe", "fule"],
    "fo": ["fo", "hwo", "huxo", "hulo", "fuxo", "fulo"],
    # てぃ
    "thi": ["thi", "texi", "teli"],
    # でぃ
    "dhi": ["dhi", "dexi", "deli"],
    # うぇ
    "we": ["we", "uxe", "ule"],
    # うぉ
    "wo": ["wo", "uxo", "ulo"],
    # ー (長音符)
    "-": ["-"],
}

# 促音 (っ) の動的追加
for c in "bcdfghjklmpqrstvwxyz":
    if c != 'n':
        ROMAJI_ALTS[c + c] = [c + c, "xtsu" + c, "ltsu" + c, "xtu" + c, "ltu" + c]

def _build_trie(alternatives):
    """
    全ての代替ローマ字からTrieを構築して、
    一文字ずつ入力チェックできるようにする。
    """
    trie = {}
    for alt in alternatives:
        node = trie
        for c in alt:
            if c not in node:
                node[c] = {}
            node = node[c]
        node["$"] = True  # 終端マーク
    return trie

class TypingManager:
    def __init__(self):
        self.current_term = ""   # 表示用の用語
        self.current_ja = ""     # 日本語の説明文
        self.canonical_romaji = ""  # 正規ローマ字（表示用）
        self.tokens = []           # 各音節ごとのTrie (複数入力対応)
        self.typed_index = 0       # canonicalの何文字目まで入力済みか（進捗バー用）
        
        self.completed_typed_string = "" # 完了したトークンまでの実際の入力文字列
        
        self._token_index = 0      # tokensの何番目の音節か
        self._node = {}            # 現在のTrie上のノード
        self._token_typed = ""     # 現在の音節で入力した文字列
        
        # 統計
        self.total_keys = 0
        self.miss_keys = 0
        self.start_time = None
        self.end_time = None
        
        self.is_active = False

    def start_sentence(self, term, ja, canonical_romaji):
        self.current_term = term
        self.current_ja = ja
        self.canonical_romaji = canonical_romaji
        self.tokens = _tokenize_romaji(canonical_romaji)
        self.typed_index = 0
        self.completed_typed_string = ""
        self._token_index = 0
        self._node = self.tokens[0] if self.tokens else {}
        self._token_typed = ""
        self.is_active = True
        if self.start_time is None:
            self.start_time = time.time()

    def _advance_token(self):
        """現在のトークンを完了し、次のトークンへ進める"""
        self.completed_typed_string += self._token_typed
        self._token_typed = ""  # ここでリセットする
        self._token_index += 1
        self.typed_index += self.tokens[self._token_index - 1].get("_canonical_len", 1)
        if self._token_index >= len(self.tokens):
            self.is_active = False
            return "complete"
        self._node = self.tokens[self._token_index]
        return None

    def check_key(self, char):
        if not self.is_active or not self.tokens:
            return None

        self.total_keys += 1
        
        # 1. 優先して現在のトークン内でさらにマッチするかチェック
        if char in self._node:
            self._node = self._node[char]
            self._token_typed += char
            
            # 現在のノードが $ (終端) を持ち、かつ他に遷移先がない場合は即座に次へ進む
            if "$" in self._node and len(self._node) == 1:
                res = self._advance_token()
                if res == "complete":
                    return "complete"
            # 最後のトークンで、かつ既に完了可能な場合 ($がある場合)、即座に完了とする
            elif "$" in self._node and self._token_index == len(self.tokens) - 1:
                res = self._advance_token()
                if res == "complete":
                    return "complete"
            return "correct"
            
        else:
            # 2. 現在のノードに char がない場合
            # もし現在のノードが既に $ (完了可能) を持っているなら、
            # 現在のトークンをここで完了扱いにして、次トークンで char を評価する
            if "$" in self._node:
                res = self._advance_token()
                if res == "complete":
                    return "complete"
                # 再度 check_key を呼んで評価
                self.total_keys -= 1 # 1回減らす（再帰先で増えるから）
                return self.check_key(char)
                
            self.miss_keys += 1
            return "miss"

    def get_progress(self):
        """入力済み文字列と残り文字列を動的に返す"""
        typed = self.completed_typed_string + self._token_typed
        
        # 現在のトークンの残りの文字列（最短パス）
        remaining_current = _get_shortest_completion(self._node) if self.is_active and self.tokens else ""
        
        # 未入力のトークンの文字列
        remaining_future = ""
        if self.is_active and self.tokens:
            for i in range(self._token_index + 1, len(self.tokens)):
                remaining_future += self.tokens[i].get("_canonical_chunk", "")
                
        remaining = remaining_current + remaining_future
        return typed, remaining

    def finish_game(self):
        self.end_time = time.time()

    def get_results(self):
        duration = self.end_time - self.start_time if self.end_time and self.start_time else 1
        wpm = (self.total_keys / 5) / (duration / 60)
        accuracy = (1 - (self.miss_keys / self.total_keys)) * 100 if self.total_keys > 0 else 0
        
        rank = "C"
        if accuracy > 95 and wpm > 40: rank = "S"
        elif accuracy > 90 and wpm > 30: rank = "A"
        elif accuracy > 80 and wpm > 20: rank = "B"
        
        return {
            "wpm": round(wpm, 1),
            "accuracy": round(accuracy, 1),
            "rank": rank,
            "miss": self.miss_keys,
            "time": round(duration, 1)
        }


def _tokenize_romaji(canonical_romaji):
    """
    正規ローマ字をトークン分割し、各トークンに対してTrieを構築する。
    例: "koukaikagi..." -> ["k","o","u","k","a","i","k","a","g","i"...] に分割し
        各音節に対して ROMAJI_ALTS を参照してTrie生成。
    
    簡易実装：長い順に代替マッチを試み、1〜3文字の音節に分割する。
    """
    tokens = []
    i = 0
    s = canonical_romaji
    while i < len(s):
        matched = False
        # 3文字, 2文字, 1文字の順で代替テーブルを検索
        for length in [3, 2, 1]:
            chunk = s[i:i+length]
            if chunk in ROMAJI_ALTS:
                alts = ROMAJI_ALTS[chunk]
                trie = _build_trie(alts)
                trie["_canonical_len"] = len(chunk)
                trie["_canonical_chunk"] = chunk
                tokens.append(trie)
                i += length
                matched = True
                break
        if not matched:
            # 代替なし（記号、数字など）: そのまま1文字のトークン
            trie = _build_trie([s[i]])
            trie["_canonical_len"] = 1
            trie["_canonical_chunk"] = s[i]
            tokens.append(trie)
            i += 1
    return tokens

def _get_shortest_completion(node):
    if "$" in node:
        return ""
    # 見つかった最初の経路を返す (辞書順などの保証はないが有効なパス)
    for k, v in node.items():
        if k != "$" and not k.startswith("_"):
            return k + _get_shortest_completion(v)
    return ""
