import pygame
import sys
import random
from src.game_config import *
from src.asset_loader import AssetLoader
from src.monster import Monster
from src.typing_manager import TypingManager

class Game:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("IT Typing RPG")
        self.clock = pygame.time.Clock()

        self.assets = AssetLoader()
        self.assets.load_all()

        self.typing = TypingManager()

        self.state = "TITLE" # TITLE, BATTLE, RESULT
        self.monster = None
        self.monster_queue = ["slime", "kobold", "zombie", "dragon"] * 2
        self.current_monster_idx = 0
        self.used_terms = set()

        # 画面フラッシュ用
        self.screen_flash_timer = 0
        self.transition_timer = 0

        # ミス演出のクールダウン (1.0秒 = 60フレーム)
        self.miss_cooldown = 60

        # リザルトデータ
        self.results = None

        # 背景画像
        self.current_bg = None
        if self.assets.backgrounds:
            self.current_bg = random.choice(list(self.assets.backgrounds.values()))

    def start_battle(self):
        if self.current_monster_idx < len(self.monster_queue):
            m_id = self.monster_queue[self.current_monster_idx]
            m_info = MONSTER_TYPES[m_id]
            self.monster = Monster(m_id, self.assets.monster_sprites[m_id], m_info["name"])

            # 文章の選択
            difficulty = m_info["difficulty"]

            # まだ使われていない文章を抽出
            available_data = [d for d in TYPING_DATA[difficulty] if d[0] not in self.used_terms]
            if not available_data:
                # 全て使い切ってしまった場合はリセット（念のため）
                available_data = TYPING_DATA[difficulty]
                self.used_terms.clear()

            term, ja, romaji = random.choice(available_data)
            self.used_terms.add(term)
            self.typing.start_sentence(term, ja, romaji)

            if self.current_monster_idx == 0:
                self.assets.play_bgm("bgm_battle")

            self.transition_timer = 0
        else:
            self.state = "RESULT"
            self.typing.finish_game()
            self.results = self.typing.get_results()
            self.assets.play_se("win")

    def handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if self.state == "TITLE":
                    if event.key == pygame.K_SPACE:
                        self.state = "BATTLE"
                        self.current_monster_idx = 0
                        self.used_terms = set()
                        self.start_battle()

                elif self.state == "BATTLE" and self.transition_timer == 0:
                    if event.unicode and event.unicode.isprintable():
                        result = self.typing.check_key(event.unicode)
                        if result == "correct":
                            self.assets.play_se("type")
                        elif result == "miss":
                            if self.miss_cooldown == 0:
                                self.assets.play_se("miss")
                                self.screen_flash_timer = 5
                                self.monster.trigger_damage()
                                self.miss_cooldown = 60  # 1秒クールダウン
                        elif result == "complete":
                            self.assets.play_se("damage")
                            self.monster.die()
                            self.transition_timer = 75  # 1.25秒待つ（エフェクト鑑賞用）

                elif self.state == "RESULT":
                    if event.key == pygame.K_SPACE:
                        # タイトルへ戻る（リトライ）
                        self.state = "TITLE"
                        self.current_monster_idx = 0
                        self.typing = TypingManager() # リセット

                        # 背景を新しく選択
                        if self.assets.backgrounds:
                            self.current_bg = random.choice(list(self.assets.backgrounds.values()))

    def update(self):
        if self.state == "BATTLE" and self.monster:
            self.monster.update()

        if self.screen_flash_timer > 0:
            self.screen_flash_timer -= 1

        if self.miss_cooldown > 0:
            self.miss_cooldown -= 1

        if self.transition_timer > 0:
            self.transition_timer -= 1
            if self.transition_timer == 1:
                self.current_monster_idx += 1
                self.start_battle()

    def draw(self):
        # 背景描画
        if self.current_bg:
            self.screen.blit(self.current_bg, (0, 0))
        elif "forest1" in self.assets.backgrounds: # フォールバック
            self.screen.blit(self.assets.backgrounds["forest1"], (0, 0))
        else:
            self.screen.fill(BLACK)

        if self.state == "TITLE":
            self.draw_text("Typing RPG", self.assets.fonts["en_large"], BLACK, SCREEN_WIDTH//2, SCREEN_HEIGHT//2 - 50)
            self.draw_text("IT知識をタイピングしてモンスターを倒せ！", self.assets.fonts["jp_medium"], RED, SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 50)
            self.draw_text("Press SPACE to Start", self.assets.fonts["en_medium"], RED, SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 150)

        elif self.state == "BATTLE":
            if self.monster:
                self.monster.draw(self.screen)

                # ─── モンスター名 (左上) ───
                self.draw_text(
                    f"Enemy: {self.monster.name}",
                    self.assets.fonts["jp_small"], YELLOW, 200, 40)

                # ─── 下部パネル背景 ───
                panel_h = 260
                panel_surf = pygame.Surface((SCREEN_WIDTH, panel_h), pygame.SRCALPHA)
                panel_surf.fill((0, 0, 0, 180))
                self.screen.blit(panel_surf, (0, SCREEN_HEIGHT - panel_h))

                # ─── 用語名 (大きく中央) ───
                term_y = SCREEN_HEIGHT - panel_h + 36
                self.draw_text(
                    self.typing.current_term,
                    self.assets.fonts["jp_large"], YELLOW, SCREEN_WIDTH // 2, term_y)

                # 仕切り線
                pygame.draw.line(
                    self.screen, (180, 60, 60),
                    (80, term_y + 32), (SCREEN_WIDTH - 80, term_y + 32), 2)

                # ─── 日本語説明文 ───
                ja_y = term_y + 64
                self.draw_text(
                    self.typing.current_ja,
                    self.assets.fonts["jp_medium"], (220, 200, 200), SCREEN_WIDTH // 2, ja_y)

                # ─── ローマ字 (入力済み / 残り) ───
                typed, remaining = self.typing.get_progress()
                full_romaji = typed + remaining
                total_surf = self.assets.fonts["en_medium"].render(full_romaji, True, RED)
                start_x = SCREEN_WIDTH // 2 - total_surf.get_width() // 2
                romaji_y = ja_y + 52

                typed_surf = self.assets.fonts["en_medium"].render(typed, True, DARK_RED)
                remain_surf = self.assets.fonts["en_medium"].render(remaining, True, BRIGHT_RED)
                self.screen.blit(typed_surf, (start_x, romaji_y))
                self.screen.blit(remain_surf, (start_x + typed_surf.get_width(), romaji_y))

                # ─── 進捗バー ───
                bar_y = romaji_y + 52
                bar_w = SCREEN_WIDTH - 200
                bar_x = 100
                pygame.draw.rect(self.screen, (60, 20, 20), (bar_x, bar_y, bar_w, 10), border_radius=5)
                progress = self.typing.typed_index / max(len(self.typing.canonical_romaji), 1)
                pygame.draw.rect(self.screen, BRIGHT_RED,
                                 (bar_x, bar_y, int(bar_w * progress), 10), border_radius=5)

        elif self.state == "RESULT":
            self.draw_text("Battle Results", self.assets.fonts["en_large"], BLACK, SCREEN_WIDTH//2, 150)
            if self.results:
                y = 250
                self.draw_text(f"正確率: {self.results['accuracy']}%", self.assets.fonts["jp_medium"], RED, SCREEN_WIDTH//2, y)
                self.draw_text(f"スピード: {self.results['wpm']} WPM", self.assets.fonts["jp_medium"], RED, SCREEN_WIDTH//2, y + 60)
                self.draw_text(f"ミス数: {self.results['miss']}回", self.assets.fonts["jp_medium"], RED, SCREEN_WIDTH//2, y + 120)
                self.draw_text(f"Rank: {self.results['rank']}", self.assets.fonts["en_large"], BLUE, SCREEN_WIDTH//2, y + 200)

            self.draw_text("Press SPACE to Title", self.assets.fonts["en_medium"], RED, SCREEN_WIDTH//2, SCREEN_HEIGHT - 100)

        # ミス時: 赤フラッシュ
        if self.screen_flash_timer > 0:
            flash_surf = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            flash_surf.fill((255, 0, 0))
            flash_surf.set_alpha(100)
            self.screen.blit(flash_surf, (0, 0))

        # 撃破時: 白フラッシュ
        if self.monster and self.monster.death_flash_timer > 0:
            alpha = int(200 * (self.monster.death_flash_timer / 15))
            flash_surf = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            flash_surf.fill((255, 255, 200))
            flash_surf.set_alpha(alpha)
            self.screen.blit(flash_surf, (0, 0))

        pygame.display.flip()

    def draw_text(self, text, font, color, x, y):
        surf = font.render(text, True, color)
        rect = surf.get_rect(center=(x, y))
        self.screen.blit(surf, rect)

    def run(self):
        while True:
            self.handle_input()
            self.update()
            self.draw()
            self.clock.tick(FPS)

if __name__ == "__main__":
    game = Game()
    game.run()
