import pygame
import math
import random
from .game_config import *


class Particle:
    """撃破時に飛び散るパーティクル"""
    def __init__(self, x, y):
        angle = random.uniform(0, math.pi * 2)
        speed = random.uniform(3, 10)
        self.x = float(x)
        self.y = float(y)
        self.vx = math.cos(angle) * speed
        self.vy = math.sin(angle) * speed
        self.life = random.randint(30, 60)
        self.max_life = self.life
        self.radius = random.randint(4, 12)
        # 色はオレンジ〜黄色系
        r = random.randint(200, 255)
        g = random.randint(80, 200)
        self.color = (r, g, 0)

    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.vy += 0.3  # 重力
        self.vx *= 0.97
        self.life -= 1

    def draw(self, screen):
        alpha = int(255 * (self.life / self.max_life))
        r = max(1, self.radius - int((1 - self.life / self.max_life) * self.radius))
        surf = pygame.Surface((r * 2, r * 2), pygame.SRCALPHA)
        pygame.draw.circle(surf, (*self.color, alpha), (r, r), r)
        screen.blit(surf, (int(self.x) - r, int(self.y) - r))

    @property
    def alive(self):
        return self.life > 0


class Monster:
    def __init__(self, monster_id, animations, name):
        self.monster_id = monster_id
        self.animations = animations
        self.name = name
        self.current_anim = "idle"
        self.frame_index = 0.0
        self.animation_speed = 0.1
        self.image = self.animations["idle"][0] if self.animations["idle"] else None

        # 位置 (画面中央)
        self.rect = self.image.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50))

        # ダメージ演出用
        self.flash_timer = 0
        self.is_dead = False
        self.alpha = 255

        # 撃破パーティクル
        self.particles = []
        self.death_flash_timer = 0  # 撃破時の白フラッシュ

    def update(self):
        # パーティクル更新
        self.particles = [p for p in self.particles if p.alive]
        for p in self.particles:
            p.update()

        if self.is_dead:
            # フェードアウト
            self.alpha = max(0, self.alpha - 8)
            if self.death_flash_timer > 0:
                self.death_flash_timer -= 1
            return

        # アニメーション更新
        anim_list = self.animations.get(self.current_anim, self.animations["idle"])
        if anim_list:
            self.frame_index += self.animation_speed
            if self.frame_index >= len(anim_list):
                self.frame_index = 0.0
            self.image = anim_list[int(self.frame_index)]

        # フラッシュタイマー更新
        if self.flash_timer > 0:
            self.flash_timer -= 1

    def draw(self, screen):
        # パーティクル描画 (モンスターの背後に出るが視認しやすい)
        for p in self.particles:
            p.draw(screen)

        if self.image and self.alpha > 0:
            temp_image = self.image.copy()

            # ダメージ時の赤フラッシュ
            if self.flash_timer > 0:
                flash_surf = pygame.Surface(temp_image.get_size()).convert_alpha()
                flash_surf.fill((255, 0, 0, 160))
                temp_image.blit(flash_surf, (0, 0), special_flags=pygame.BLEND_RGBA_ADD)

            temp_image.set_alpha(self.alpha)
            screen.blit(temp_image, self.rect)

        # 撃破直後の白フラッシュをパーティクルの手前に重ねる
        if self.death_flash_timer > 0:
            for p in self.particles:
                p.draw(screen)

    def trigger_damage(self):
        self.flash_timer = 10

    def die(self):
        self.is_dead = True
        # パーティクルを中心から大量に発生させる
        cx, cy = self.rect.center
        for _ in range(40):
            self.particles.append(Particle(cx, cy))
        self.death_flash_timer = 15
