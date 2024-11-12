import os
import sys
import pygame as pg
import math
import random
import time

# 実行ファイルのディレクトリに移動
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# グローバル変数を宣言(ステータス)
MeLevel = 20
MeHP = 100
EnemyHP = 100
WIDTH, HEIGHT = 680, 784  # 幅を200ピクセル増加
kk_img = pg.transform.rotozoom(pg.image.load("fig/hart.png"), 0, 0.72)  # キャラクター画像
en_img = pg.transform.rotozoom(pg.image.load("fig/koukaton.png"), 0, 0.72)
kk_rct = kk_img.get_rect()  # キャラクターの矩形を取得
kk_rct.center = int(320 * 0.8), int(590 * 0.8)  # キャラクターの初期位置を設定
screen = pg.display.set_mode((WIDTH, HEIGHT))  # 指定した寸法で画面を作成
items = ["Potion, 回復", "Ether, MP回復", "Elixir, 全回復"]
timing_width = 0
timing_x = 0
timing_color = 0
tmp_tmr = 0

menu_index = 0
item_index = 0
enter_menu = 9999
tmr = 0  # タイマーの初期化
tmp_tmr_F = 0
enemy_bullets = []  # 攻撃弾の設定
enemy_obstacles = []  # 新しい攻撃の障害物
draw_message_No = 0

# グローバル宣言(フラグ)
EnemyAttac = False
debug_EnemyAttac = False
GameOver = False
tmp_tmr_F = False
DebugMode = False
auto_attack = False  # 自動攻撃のフラグ
attack_timer = time.time()  # 攻撃タイマー
current_attack_pattern = None

# 色の定義
WHITE = (255, 255, 255)  # 白
BLACK = (0, 0, 0)        # 黒
GRAY = (200, 200, 200)   # グレー
RED = (255, 0, 0)        #赤

def draw_gameover_screen(font):
    """ゲームオーバー画面を描画する"""
    gameover_text = font.render("GAME OVER", True, RED)
    screen.fill(BLACK)
    screen.blit(gameover_text, (WIDTH // 2 - gameover_text.get_width() // 2, HEIGHT // 2 - 50))
    pg.display.update()

def draw_attack_bar(font, tmr):
    global enter_menu, tmp_tmr_F, tmp_tmr, timing_width, timing_x, timing_color

    # 攻撃バーの設定
    bar_width = 400
    bar_height = 20
    bar_x = 140
    bar_y = HEIGHT - 150

    # タイミングバーの設定
    if not tmp_tmr_F:
        timing_x = bar_x
        timing_width = 20
        timing_color = (0, 255, 0)
        tmp_tmr_F = True

    # タイミングバーの進行
    if enter_menu == 0:
        timing_x += 4
        if timing_x >= bar_x + bar_width:
            timing_x = bar_x

    # 判定ゾーンの設定
    judge_zone_start = bar_x + 160
    judge_zone_end = bar_x + 320
    judge_zone_color = (255, 255, 0)

    # バー全体の枠
    pg.draw.rect(screen, WHITE, (bar_x, bar_y, bar_width, bar_height), 2)

    # 判定ゾーンを描画
    pg.draw.rect(screen, judge_zone_color, (judge_zone_start, bar_y, judge_zone_end - judge_zone_start, bar_height))

    # タイミングバーを描画
    pg.draw.rect(screen, timing_color, (timing_x, bar_y, timing_width, bar_height))

    if enter_menu == 0 and not tmp_tmr_F:
        tmp_tmr = tmr
        tmp_tmr_F = True

    if tmr > (tmp_tmr + 200):
        enter_menu = 9999
        tmp_tmr = 0
        tmp_tmr_F = False
    elif pg.key.get_pressed()[pg.K_SPACE]:
        if judge_zone_start <= timing_x <= judge_zone_end:
            print("成功！攻撃が当たった")
            reset_attack()
        else:
            print("失敗！攻撃が外れた")
            reset_attack()

def reset_attack():
    global enter_menu, tmp_tmr_F, tmp_tmr, enemy_bullets, enemy_obstacles, timing_width, timing_x, timing_color, tmr, auto_attack, attack_timer, EnemyAttac, current_attack_pattern
    enter_menu = 9999
    tmp_tmr = 0
    tmp_tmr_F = False
    enemy_bullets.clear()
    enemy_obstacles.clear()
    timing_x = 0  # タイミングバー位置のリセット
    timing_color = (0, 255, 0)  # 色リセット
    auto_attack = True  # 自動攻撃のフラグを立てる
    attack_timer = time.time()  # 攻撃タイマーを開始
    current_attack_pattern = random.choice(["pattern1", "pattern2"])  # 攻撃パターンをランダム選択
    print(f"敵の攻撃パターン: {current_attack_pattern} を開始")
    EnemyAttac = True  # 敵の攻撃を開始

def draw_menu(font, event, tmr):
    global EnemyAttac, screen, menu_index, enter_menu, tmp_tmr_F, tmp_tmr
    menu_texts = ["ATTACK", "ACT", "ITEM"]

    if EnemyAttac == False and debug_EnemyAttac == False:
        if enter_menu > 2:
            for i, text in enumerate(menu_texts):
                color = (255, 255, 0) if i == menu_index else WHITE
                menu_surface = font.render(text, True, color)
                screen.blit(menu_surface, (160 + i * 160, HEIGHT - 125))

        if enter_menu == 0:
            draw_attack_bar(font, tmr)
        elif enter_menu == 1:
            print("ACTメニュー選択")
            pg.draw.rect(screen, (255, 255, 0), (128, 328, 424, 280), 0)
            if tmp_tmr_F == False:
                tmp_tmr = tmr
                tmp_tmr_F = True
            if tmr > (tmp_tmr + 100):
                enter_menu = 9999
                tmp_tmr = 0
                tmp_tmr_F = False
        elif enter_menu == 2:
            draw_item_menu(font)

def draw_item_menu(font):
    """アイテムメニューを表示"""
    global item_index
    for i, item in enumerate(items):
        color = (255, 255, 0) if i == item_index else WHITE
        item_text = font.render(item, True, color)
        screen.blit(item_text, (WIDTH // 2 - item_text.get_width() // 2, 160 + i * 50))

def handle_enemy_obstacles():
    """敵の攻撃と障害物の処理"""
    global enemy_obstacles, enemy_bullets
    for bullet in enemy_bullets:
        bullet.move()
        if bullet.rect.colliderect(kk_rct):
            MeHP -= 10
            print(f"プレイヤーが攻撃を受けた！残りHP: {MeHP}")
            enemy_bullets.remove(bullet)
    for obstacle in enemy_obstacles:
        obstacle.move()
        if obstacle.rect.colliderect(kk_rct):
            MeHP -= 20
            print(f"プレイヤーが障害物に当たった！残りHP: {MeHP}")
            enemy_obstacles.remove(obstacle)

def main():
    pg.init()
    font = pg.font.Font(None, 40)

    global GameOver, EnemyAttac, enter_menu
    clock = pg.time.Clock()
    
    while not GameOver:
        tmr = pg.time.get_ticks()
        screen.fill(BLACK)

        for event in pg.event.get():
            if event.type == pg.QUIT:
                GameOver = True
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_UP:
                    menu_index = (menu_index - 1) % 3
                elif event.key == pg.K_DOWN:
                    menu_index = (menu_index + 1) % 3
                elif event.key == pg.K_RETURN:
                    if menu_index == 0:
                        enter_menu = 0
                    elif menu_index == 1:
                        enter_menu = 1
                    elif menu_index == 2:
                        enter_menu = 2

        draw_menu(font, event, tmr)
        if MeHP <= 0:
            GameOver = True
            draw_gameover_screen(font)
        pg.display.update()
        clock.tick(60)

    pg.quit()

if __name__ == "__main__":
    main()
