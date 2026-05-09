import pygame
import os
import glob
import random
from .game_config import *

class AssetLoader:
    def __init__(self):
        self.backgrounds = {}
        self.monster_sprites = {}
        self.sounds = {}
        self.fonts = {}
        self.bgm_list = []  # BGMファイルパスのリスト

    def load_all(self):
        # 背景の読み込み
        bg_files = glob.glob(os.path.join(BG_DIR, "*.jpg")) + glob.glob(os.path.join(BG_DIR, "*.png"))
        for f in bg_files:
            name = os.path.splitext(os.path.basename(f))[0]
            try:
                img = pygame.image.load(f).convert()
                self.backgrounds[name] = pygame.transform.scale(img, (SCREEN_WIDTH, SCREEN_HEIGHT))
            except Exception as e:
                print(f"Error loading background {f}: {e}")

        # フォントの読み込み
        try:
            self.fonts["jp_large"] = pygame.font.Font(JAPANESE_FONT_PATH, 48)
            self.fonts["jp_medium"] = pygame.font.Font(JAPANESE_FONT_PATH, 32)
            self.fonts["jp_small"] = pygame.font.Font(JAPANESE_FONT_PATH, 24)
            self.fonts["en_large"] = pygame.font.Font(None, 64)
            self.fonts["en_medium"] = pygame.font.Font(None, 40)
        except:
            print("Warning: Could not load Japanese font. Using default.")
            self.fonts["jp_large"] = pygame.font.Font(None, 48)
            self.fonts["jp_medium"] = pygame.font.Font(None, 32)
            self.fonts["jp_small"] = pygame.font.Font(None, 24)
            self.fonts["en_large"] = pygame.font.Font(None, 64)
            self.fonts["en_medium"] = pygame.font.Font(None, 40)

        # サウンドの読み込み
        # SE
        se_files = {
            "type": "maou_se_system49.mp3", # タイピング成功
            "miss": "maou_se_8bit14.mp3",   # ミス
            "damage": "maou_se_battle_explosion06.mp3", # ダメージ/撃破
            "win": "maou_se_jingle03.mp3"    # クリア
        }
        for key, filename in se_files.items():
            path = os.path.join(SOUNDS_DIR, filename)
            if os.path.exists(path):
                sound = pygame.mixer.Sound(path)
                sound.set_volume(0.5)  # SE音量を半分に設定
                self.sounds[key] = sound
        
        # BGM (bgm_ で始まるファイルをすべてロード)
        bgm_files = sorted(glob.glob(os.path.join(SOUNDS_DIR, "maou_bgm_*.mp3")))
        self.bgm_list = bgm_files
        if self.bgm_list:
            self.sounds["bgm_battle"] = self.bgm_list[0]  # 代表キー（互換用）

        # モンスターのスプライト読み込み
        for m_id, m_info in MONSTER_TYPES.items():
            self.monster_sprites[m_id] = self._load_monster_animation(m_info["sprite_path"])

    def _load_monster_animation(self, path):
        animations = {"idle": [], "attack": [], "move": []}
        
        # 待機モーション (A_待機...)
        idle_files = sorted(glob.glob(os.path.join(path, "*A_待機*.png")))
        for f in idle_files:
            img = pygame.image.load(f).convert_alpha()
            # スプライトが小さいので3倍に拡大
            scaled_img = pygame.transform.scale(img, (img.get_width() * 4, img.get_height() * 4))
            animations["idle"].append(scaled_img)
            
        # 攻撃モーション
        attack_files = sorted(glob.glob(os.path.join(path, "*A_攻撃*.png")))
        for f in attack_files:
            img = pygame.image.load(f).convert_alpha()
            scaled_img = pygame.transform.scale(img, (img.get_width() * 4, img.get_height() * 4))
            animations["attack"].append(scaled_img)

        # もし待機モーションが空なら一番最初の画像を入れる
        if not animations["idle"]:
            all_pngs = sorted(glob.glob(os.path.join(path, "*.png")))
            if all_pngs:
                img = pygame.image.load(all_pngs[0]).convert_alpha()
                scaled_img = pygame.transform.scale(img, (img.get_width() * 4, img.get_height() * 4))
                animations["idle"].append(scaled_img)

        return animations

    def play_bgm(self, key):
        # BGMリストからランダムに選択して再生
        if self.bgm_list:
            chosen = random.choice(self.bgm_list)
            pygame.mixer.music.load(chosen)
            pygame.mixer.music.set_volume(0.5 / 3)  # 音量を1/3に設定
            pygame.mixer.music.play(-1)

    def play_se(self, key):
        if key in self.sounds and isinstance(self.sounds[key], pygame.mixer.Sound):
            self.sounds[key].play()
