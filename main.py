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

# グローバル宣言(フラグ)
EnemyAttac = False
debug_EnemyAttac = False
GameOver = False
tmp_tmr_F = False
DebugMode = False

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

    # タイミングバーの設定：毎回リセット
    if tmp_tmr_F == False:
        timing_x = bar_x  # 初期位置を設定
        timing_width = 20  # 初期のバー幅
        timing_color = (0, 255, 0)  # 初期色
        tmp_tmr_F = True

    # タイミングバーの進行
    if enter_menu == 0:  # 攻撃メニューにいるときのみ進行
        timing_x += 4  # 進行速度を調整（2は適当な例）
        if timing_x >= bar_x + bar_width:
            timing_x = bar_x  # バーの終わりに達したら最初に戻る

    # 判定ゾーンの設定（成功範囲）
    judge_zone_start = bar_x + 160
    judge_zone_end = bar_x + 320
    judge_zone_color = (255, 255, 0)

    # バー全体の枠
    pg.draw.rect(screen, WHITE, (bar_x, bar_y, bar_width, bar_height), 2)

    # 判定ゾーンを描画
    pg.draw.rect(screen, judge_zone_color, (judge_zone_start, bar_y, judge_zone_end - judge_zone_start, bar_height))

    # タイミングバーを描画
    pg.draw.rect(screen, timing_color, (timing_x, bar_y, timing_width, bar_height))

    # プレイヤーの入力待ちと判定処理
    if enter_menu == 0:
        if tmp_tmr_F == False:
            tmp_tmr = tmr
            tmp_tmr_F = True
################################################################################
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
    """攻撃をリセットする関数"""
    global enter_menu, tmp_tmr_F, tmp_tmr, enemy_bullets, enemy_obstacles, timing_width, timing_x, timing_color, tmr
    enter_menu = 9999
    tmp_tmr = 0
    tmp_tmr_F = False
    enemy_bullets.clear()
    enemy_obstacles.clear()
    # timing_width = 0
    # timing_x = 0
    # timing_color = 0
    tmr = 0  # タイマーをリセット


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
            print("asdfghjkjfdfgeefwgsdahjgfiuasbdfkjasgfijkagvdfkjasjkfhdioua")
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
            print("saughdfiahfuiosaghi")
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
    global draw_message_No
    serect = ["こうかとんがあらわれた！!", "こうかとんはあなたをにらみつけている"]

    if EnemyAttac == False and enter_menu > 2 and debug_EnemyAttac == False:
        for i, text in enumerate(serect[draw_message_No]):
            menu_surface = font.render(text, True, WHITE)
            screen.blit(menu_surface, (145, 350 + i * 40))

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

def handle_enemy_obstacles():
    global MeHP, GameOver

    if debug_EnemyAttac and tmr % 60 == 0:  # 障害物の生成頻度を高める
        # 障害物の生成位置（上部と下部の両方）
        y = random.choice([random.randint(340, 595), random.randint(340, 595)])  # y座標を340～595の範囲に制限
        width = random.randint(10, 30)
        height = random.randint(60, 90)
        speed = random.randint(3, 6)

        # 上部の場合、y座標を負の値にすることで、画面上に配置
        if y < 470:  # 画面上部に配置される場合
            enemy_obstacles.append({"rect": pg.Rect(WIDTH, y - height, width, height), "speed": -speed})
        else:  # 画面下部に配置される場合
            enemy_obstacles.append({"rect": pg.Rect(0, y, width, height), "speed": speed})

    # 障害物の更新
    for obstacle in enemy_obstacles[:]:
        obstacle["rect"].x += obstacle["speed"]

        # 画面外に出た障害物を削除
        if obstacle["rect"].right < 0 or obstacle["rect"].left > WIDTH:
            enemy_obstacles.remove(obstacle)
            continue

        # 障害物が画面内に収まるように制限
        if obstacle["rect"].top < 340:
            obstacle["rect"].top = 340  # 上限
        if obstacle["rect"].bottom > 595:
            obstacle["rect"].bottom = 595  # 下限dfghjk

        # 障害物を描画
        pg.draw.rect(screen, (0, 255, 0), obstacle["rect"])

        # 障害物とプレイヤーの衝突判定
        if kk_rct.colliderect(obstacle["rect"]):
            MeHP -= 15
            enemy_obstacles.remove(obstacle)
            if MeHP <= 0:
                GameOver = True


def main():
    global MeLevel, MeHP, EnemyHP, GameOver, kk_rct, screen, menu_index, enter_menu, tmr, EnemyAttac, debug_EnemyAttac

    pg.display.set_caption("逃げろ！こうかとん")
    # font_path = "/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc"
    # font = pg.font.Font(font_path, int(40 * 0.5))
    font = pg.font.Font(None, int(60 * 0.5))
    clock = pg.time.Clock()
    
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_RSHIFT:
                    # `EnemyAttac` トグルするが、`debug_EnemyAttac` が有効なら無効化
                    EnemyAttac = not EnemyAttac
                    if debug_EnemyAttac:
                        EnemyAttac = False
                    reset_attack()  # 攻撃開始時にリセット
                if event.key == pg.K_LSHIFT:
                    # `debug_EnemyAttac` トグルするが、`EnemyAttac` が有効なら無効化
                    debug_EnemyAttac = not debug_EnemyAttac
                    if EnemyAttac:
                        EnemyAttac = False
                    reset_attack()  # デバッグ攻撃開始時にリセット
                if not EnemyAttac and not debug_EnemyAttac:
                    # メニュー操作の処理
                    if event.key == pg.K_RIGHT:
                        menu_index = (menu_index + 1) % 3
                    elif event.key == pg.K_LEFT:
                        menu_index = (menu_index - 1) % 3
                    elif event.key == pg.K_RETURN:
                        enter_menu = menu_index
                        if enter_menu == 0:  # 攻撃メニューに入るときにリセット
                            #reset_attack()
                            pass

        screen.fill(BLACK)
        draw_status(font)
        draw_menu(font, event, tmr)
        move_hart()
        draw_enemy()
        draw_message(font)

        # `EnemyAttac` が有効なときは通常の弾攻撃を実行
        if EnemyAttac:
            handle_enemy_bullets()
        # `debug_EnemyAttac` が有効なときは障害物攻撃を実行
        elif debug_EnemyAttac:
            handle_enemy_obstacles()

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