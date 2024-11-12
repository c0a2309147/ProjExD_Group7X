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
items=["Potion, 回復","Ether, MP回復","Elixir, 全回復"]
timing_width = 0
timing_x = 0
timing_color = 0
tmp_tmr = 0

menu_index = 0
item_index = 0
enter_menu = 9999
tmr = 0  # タイマーの初期化
tmp_tmr_F = 0
enemy_bullets = [] # 攻撃弾の設定
enemy_obstacles = [] # 新しい攻撃の障害物
draw_message_No = 0
effect_timer = 0  
effect_duration = 30

# グローバル宣言(フラグ)
EnemyAttac = False
debug_EnemyAttac = False
GameOver = False
tmp_tmr_F = False
DebugMode = False
auto_attack = False  # 自動攻撃のフラグ
attack_timer = time.time()  # 攻撃タイマー
current_attack_pattern = None
effect_active = False
tmp = False

# 色の定義
WHITE = (255, 255, 255)  # 白
BLACK = (0, 0, 0)        # 黒
GRAY = (200, 200, 200)   # グレー
RED = (255, 0, 0)        #赤

# エフェクトの表示処理
def draw_enemy_effect():
    global effect_active, effect_timer, tmp
    if effect_active:

        font = pg.font.SysFont("Arial", 80)
        miss_text = font.render("Miss", True, (255, 0, 255))  
        screen.blit(miss_text, (WIDTH / 2 - miss_text.get_width()  / 2, HEIGHT / 2 - 300)) 

        if effect_timer > effect_duration + 10:
            effect_active = False
            effect_timer = 0  
        else:
            effect_timer += 1  

def draw_gameover_screen(font):
    """ゲームオーバー画面を描画する"""
    gameover_text = font.render("GAME OVER", True, RED)
    screen.fill(BLACK)
    screen.blit(gameover_text, (WIDTH // 2 - gameover_text.get_width() // 2, HEIGHT // 2 - 50))
    pg.display.update()

def draw_attack_bar(font, tmr):
    global enter_menu, tmp_tmr_F, tmp_tmr, timing_width, timing_x, timing_color, tmp

    bar_width = 400
    bar_height = 20
    bar_x = 140
    bar_y = HEIGHT - 150

    # タイミングバーの初期化
    if enter_menu == 0 and not tmp_tmr_F:
        timing_x = bar_x
        timing_width = 20
        timing_color = (0, 255, 0)
        tmp_tmr_F = True  # 初期化フラグを立てる

    # タイミングバーの進行
    if enter_menu == 0:
        timing_x += 4  # タイミングバーの移動速度
        if timing_x >= bar_x + bar_width - 20:
            timing_x = bar_x  # タイミングバーを最初に戻す

    # 判定ゾーンの設定
    judge_zone_start = bar_x + 160
    judge_zone_end = bar_x + 320
    judge_zone_color = (255, 255, 0)

    # 攻撃バー枠
    pg.draw.rect(screen, WHITE, (bar_x, bar_y + 30, bar_width, bar_height), 2)

    # 判定ゾーンの描画
    pg.draw.rect(screen, judge_zone_color, (judge_zone_start, bar_y + 30, judge_zone_end - judge_zone_start, bar_height))

    # タイミングバーの描画
    pg.draw.rect(screen, timing_color, (timing_x, bar_y + 30, timing_width, bar_height))

    # タイマーをリセット
    if enter_menu == 0 and tmp_tmr_F:
        tmp_tmr = tmr
        tmp_tmr_F = True

    # 判定処理
    if tmr > (tmp_tmr + 200):  # 攻撃バーが終了するまでの時間
        reset_attack()  # リセット関数を呼び出して初期化
    elif pg.key.get_pressed()[pg.K_SPACE]:
        if judge_zone_start <= timing_x <= judge_zone_end:
            reset_attack()
            tmp = True
        else:
            reset_attack()
            tmp = False
            effect_timer += 1  

    space_text = font.render("SPACE!!", True, WHITE)
    screen.blit(space_text, (bar_x + bar_width / 2 - space_text.get_width() / 2, bar_y + 60))  # 攻撃バーの下に表示


def reset_attack():
    global enter_menu, tmp_tmr_F, tmp_tmr, timing_x, timing_color, auto_attack, attack_timer, EnemyAttac, current_attack_pattern, effect_active, effect_timer, enemy_bullets, enemy_obstacles
    
    enter_menu = 9999  # メニューのリセット
    tmp_tmr = 0  # タイマーリセット
    tmp_tmr_F = False  # タイミングフラグリセット
    timing_x = 0  # タイミングバー位置のリセット
    timing_color = (0, 255, 0)  # 色リセット
    auto_attack = True  # 自動攻撃のフラグを立てる
    attack_timer = time.time()  # 攻撃タイマーのリセット
    current_attack_pattern = random.choice(["pattern1", "pattern2"])  # ランダムな攻撃パターンの選択
    print(f"敵の攻撃パターン: {current_attack_pattern} を開始")
    
    # 攻撃リストをクリア
    enemy_bullets.clear()
    enemy_obstacles.clear()

    EnemyAttac = True  # 敵の攻撃を開始

    # エフェクト開始
    effect_active = True
    effect_timer = 0  # エフェクトタイマーをリセット





def handle_enemy_bullets():
    global MeHP, GameOver
    #if tmr % 20 == 0:
    if EnemyAttac and tmr % 5 == 0:
        x = random.randint(60, 560)
        y = 80
        speed = random.randint(2, 6)
        enemy_bullets.append({"rect": pg.Rect(x, y, 10, 10), "speed": speed})
    

    for bullet in enemy_bullets[:]:
        bullet["rect"].y += bullet["speed"]
        if bullet["rect"].top > HEIGHT:
            enemy_bullets.remove(bullet)
            continue

        pg.draw.rect(screen, (255, 0, 0), bullet["rect"])

        if kk_rct.colliderect(bullet["rect"]):
            MeHP -= 10
            enemy_bullets.remove(bullet)
            if MeHP <= 0:
                GameOver = True
                


    if not EnemyAttac:
        enemy_bullets.clear()


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
            pg.draw.rect(screen, (255, 255, 0), (128, 328, 424, 280), 0)
            if tmp_tmr_F == False:
                tmp_tmr = tmr 
                tmp_tmr_F = True
            if tmr > (tmp_tmr + 100):
                enter_menu = 9999
                tmp_tmr = 0
                tmp_tmr_F = False
        elif enter_menu == 2:
            #pg.draw.rect(screen, (255, 255, 0), (128, 328, 424, 280), 0)
            #if tmp_tmr_F == False:
                #tmp_tmr = tmr 
                #tmp_tmr_F = True
            #if tmr > (tmp_tmr + 100):
                #enter_menu = 9999
                #tmp_tmr = 0
                #tmp_tmr_F = False
            draw_item_menu(font)

def draw_item_menu(font):
    """アイテムメニューを表示"""
    global item_index, screen

    for i, item in enumerate(items):
        color = (255, 255, 0) if i == item_index else WHITE
        item_surface = font.render(item, True, color)
        screen.blit(item_surface, (160, HEIGHT - 350 + i * 40))

def handle_item_selection():
    """アイテム選択の処理"""
    global MeHP, item_index, enter_menu

    selected_item = items[item_index]
    
    if selected_item == "Potion: 回復":
        MeHP = min(MeHP + 30, 100)  # HP回復
    elif selected_item == "Ether: MP回復":
        print("MPが回復しました！（ダミー処理）")
    elif selected_item == "Elixir: 全回復":
        MeHP = 100  # HP全回復

    enter_menu = 9999  # メニュー選択終了

def draw_status(font):
    global MeLevel, MeHP, EnemyHP, EnemyAttac, screen
    
    if enter_menu > 2:
        pg.draw.rect(screen, WHITE, (128, 328, 424, 280), 0)
        pg.draw.rect(screen, BLACK, (128 + 12, 340, 400, 256), 0)
    
    lv_text = font.render(f"LV {MeLevel}", True, WHITE)
    hp_text = font.render(f"HP {MeHP}/100", True, WHITE)

    screen.blit(lv_text, (168 - 28, 616))
    screen.blit(hp_text, (178 + 40, 616))
    
    # HPゲージを描画
    pg.draw.rect(screen, (255, 0, 0), (168 + 182, 623, 200, 20))
    hp_width = (MeHP / 100) * 200
    pg.draw.rect(screen, (255, 255, 0), (168 + 182, 623, hp_width, 20))

def draw_enemy():
    en_ip = [(WIDTH / 2) - 50, 80 + 5 * math.sin(tmr * 0.05)]
    screen.blit(en_img, en_ip)

def move_hart():
    if EnemyAttac == True or debug_EnemyAttac == True:
        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]
        if key_lst[pg.K_UP]:
            sum_mv[1] -= 6
        if key_lst[pg.K_DOWN]:
            sum_mv[1] += 6
        if key_lst[pg.K_LEFT]:
            sum_mv[0] -= 6
        if key_lst[pg.K_RIGHT]:
            sum_mv[0] += 6
        if debug_EnemyAttac:
            sum_mv[1] += 4
        kk_rct.move_ip(sum_mv)

        if kk_rct.left < 140: kk_rct.left = 140
        if kk_rct.right > 540: kk_rct.right = 540
        if kk_rct.top < 340: kk_rct.top = 340
        if kk_rct.bottom > 595: kk_rct.bottom = 595

        if enter_menu > 2:
            screen.blit(kk_img, kk_rct)

def draw_message(font):
    """メッセージ表示"""
    global draw_message_No
    serect = ["Koukaton appeared!", "Koukaton is glaring at you"]

    if not EnemyAttac and enter_menu > 2 and not debug_EnemyAttac:
        message_surface = font.render(serect[draw_message_No], True, WHITE)
        screen.blit(message_surface, (145, 350))

def handle_enemy_obstacles():
    global MeHP, GameOver

    if EnemyAttac and tmr % 30 == 0:  # 障害物の生成頻度を高める
        # 障害物の生成位置（上部と下部の両方）
        y = random.choice([random.randint(340, 595), random.randint(340, 595)]) 
        width = random.randint(10, 30)
        height = random.randint(60, 90)
        speed = random.randint(3, 6)
        print(width, height)

        if y < 470:  # 画面上部に配置される場合
            enemy_obstacles.append({"rect": pg.Rect(WIDTH, y - height, width, height), "speed": -speed})
        else:  # 画面下部に配置される場合
            enemy_obstacles.append({"rect": pg.Rect(0, y, width, height), "speed": speed})

    # 障害物の更新
    for obstacle in enemy_obstacles[:]:
        obstacle["rect"].x += obstacle["speed"]


        if obstacle["rect"].right < 0 or obstacle["rect"].left > WIDTH:
            enemy_obstacles.remove(obstacle)
            continue

        if obstacle["rect"].top < 340:
            obstacle["rect"].top = 340  
        if obstacle["rect"].bottom > 595:
            obstacle["rect"].bottom = 595  


        pg.draw.rect(screen, (0, 255, 0), obstacle["rect"])

        if kk_rct.colliderect(obstacle["rect"]):
            MeHP -= 15
            enemy_obstacles.remove(obstacle)
            if MeHP <= 0:
                GameOver = True
                


    if not EnemyAttac:
        enemy_bullets.clear()



def handle_enemy_attack():
    """敵の攻撃を自動制御し、パターンをランダムで選択する"""
    global EnemyAttac, auto_attack, attack_timer, current_attack_pattern

    # 自動攻撃が開始された場合、攻撃パターンをランダムで選択
    if auto_attack and (time.time() - attack_timer > 10):  # 攻撃が15秒で自動終了
        print("自動攻撃終了")
        EnemyAttac = False
        auto_attack = False
        current_attack_pattern = None  # 攻撃パターンをリセット
        effect_active = False  # エフェクト停止
        effect_timer = 0  # エフェクトタイマーをリセット
        print("次回攻撃準備完了")
    elif auto_attack and not EnemyAttac: 
        # 次の攻撃開始
        EnemyAttac = True
        current_attack_pattern = random.choice(["pattern1", "pattern2"])  # 新しいパターンをランダムで選択
        print(f"新しい攻撃パターン: {current_attack_pattern} を開始")

    if EnemyAttac:
        if current_attack_pattern == "pattern1":
            print("攻撃パターン1: 弾を生成")
            handle_enemy_bullets()  # 攻撃パターン1: 弾を生成
        elif current_attack_pattern == "pattern2":
            print("攻撃パターン2: 障害物を生成")
            handle_enemy_obstacles()  # 攻撃パターン2: 障害物を生成



def main():
    global MeLevel, MeHP, EnemyHP, GameOver, kk_rct, screen, menu_index, enter_menu, tmr, EnemyAttac, debug_EnemyAttac, auto_attack, effect_active

    pg.display.set_caption("逃げろ！こうかとん")
    font = pg.font.Font(None, int(60 * 0.5))
    clock = pg.time.Clock()

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return
            if event.type == pg.KEYDOWN:
                # if event.key == pg.K_RSHIFT:
                #     EnemyAttac = not EnemyAttac
                #     if debug_EnemyAttac:
                #         EnemyAttac = False
                #     reset_attack()
                # if event.key == pg.K_LSHIFT:
                #     debug_EnemyAttac = not debug_EnemyAttac
                #     if EnemyAttac:
                #         EnemyAttac = False
                #     reset_attack()
                if not EnemyAttac and not debug_EnemyAttac:
                    if event.key == pg.K_RIGHT:
                        menu_index = (menu_index + 1) % 3
                    elif event.key == pg.K_LEFT:
                        menu_index = (menu_index - 1) % 3
                    elif event.key == pg.K_RETURN:
                        print(f"K_RETURN が押されました。menu_index: {menu_index}")
                        enter_menu = menu_index
                        if enter_menu == 0:
                            pass
                    elif event.key == pg.K_SPACE and enter_menu == 0:
                        if timing_x >= 160 and timing_x <= 320:
                            reset_attack()
                        else:
                            reset_attack()

        screen.fill(BLACK)
        draw_status(font)
        draw_menu(font, event, tmr)
        move_hart()
        draw_enemy()
        draw_message(font)

        # エフェクトを描画
        draw_enemy_effect()
        handle_enemy_attack()

        if GameOver:
            draw_gameover_screen(font)
            time.sleep(5)
            return

        pg.display.update()
        tmr += 1
        clock.tick(60)




if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()