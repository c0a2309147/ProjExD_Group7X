import os
import sys
import pygame as pg

# グローバル変数を宣言(ステータス)
MeLevel = 20
MeHP = 100
EnemyHP = 100

# グローバル宣言(ステータス)
EnemyAttac = False
GameOver = False

# 画面の寸法を定義
WIDTH, HEIGHT = 650, 900
# 実行ファイルのディレクトリに移動
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# 色の定義
WHITE = (255, 255, 255)  # 白
BLACK = (0, 0, 0)        # 黒
GRAY = (200, 200, 200)   # グレー

def draw_menu(screen, font):
    global EnemyAttac
    # 画面下部にメニューオプションを描画する
    menu_texts = ["FIGHT", "ACT", "ITEM"]  # メニュー項目
    for i, text in enumerate(menu_texts):
        menu_surface = font.render(text, True, WHITE)  # テキストを描画可能なサーフェスに変換
        screen.blit(menu_surface, (90 + i * 200, HEIGHT - 75))  # 画面に描画

def draw_status(screen, font):
    global MeLevel, MeHP, EnemyHP, EnemyAttac  # グローバル変数を使用
    
    # ステータスボックスを描画するための矩形
    pg.draw.rect(screen, WHITE, (60, 410, 530, 350), 0)  # ステータスボックスの背景を白で描画
    pg.draw.rect(screen, BLACK, (75, 425, 500, 320), 0)
    
    lv_text = font.render(f"LV {MeLevel}", True, WHITE)  # レベルテキストを描画
    hp_text = font.render(f"HP {MeHP}/{MeHP}", True, WHITE)  # HPテキストを描画

    # デバッグ用の透明な矩形を描画
    debug_rect = pg.Surface((200, 50))  # 矩形のサイズを指定
    debug_rect.fill(BLACK)  # 矩形の背景色を黒に設定
    debug_rect.set_colorkey(BLACK)  # 黒を透明に設定

    screen.blit(lv_text, (25, 770))  # レベルを画面に描画
    screen.blit(hp_text, (110, 770))  # HPを画面に描画

def main():
    global MeLevel, MeHP, EnemyHP, GameOver  # グローバル変数を使用

    # pygameを初期化し、画面をセットアップする
    pg.display.set_caption("逃げろ！こうかとん")  # ウィンドウタイトルを設定
    screen = pg.display.set_mode((WIDTH, HEIGHT))  # 指定した寸法で画面を作成
    font = pg.font.Font(None, 40)  # フォントの設定
    
    # キャラクターの画像を読み込む
    kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 0.9)  # キャラクター画像
    kk_rct = kk_img.get_rect()  # キャラクターの矩形を取得
    kk_rct.center = 300, 200  # キャラクターの初期位置を設定
    
    clock = pg.time.Clock()  # 時間管理のためのクロックを作成
    tmr = 0  # タイマーの初期化
    
    # メインゲームループ
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:  # ウィンドウが閉じられた場合
                return

        screen.fill(BLACK)  # 画面を黒で塗りつぶす
        draw_status(screen, font)  # ステータスボックスを描画
        draw_menu(screen, font)  # メニューオプションを描画
        
        # キャラクターの移動
        key_lst = pg.key.get_pressed()  # 現在のキーの状態を取得
        sum_mv = [0, 0]  # 移動量の初期化
        if key_lst[pg.K_UP]:  # 上キーが押されたら
            sum_mv[1] -= 5  # 上方向に移動
        if key_lst[pg.K_DOWN]:  # 下キーが押されたら
            sum_mv[1] += 5  # 下方向に移動
        if key_lst[pg.K_LEFT]:  # 左キーが押されたら
            sum_mv[0] -= 5  # 左方向に移動
        if key_lst[pg.K_RIGHT]:  # 右キーが押されたら
            sum_mv[0] += 5  # 右方向に移動
        kk_rct.move_ip(sum_mv)  # キャラクターを移動させる
        
        # キャラクターが画面内に収まるように制限
        if kk_rct.left < 75: kk_rct.left = 75  # 左端で制限
        if kk_rct.right > 575: kk_rct.right = 575  # 右端で制限
        if kk_rct.top < 425: kk_rct.top = 425  # 上端で制限
        if kk_rct.bottom > 755: kk_rct.bottom = 755  # 下端で制限
        
        screen.blit(kk_img, kk_rct)  # キャラクターを描画
        pg.display.update()  # 画面を更新
        
        # フレーム制御
        tmr += 1  # タイマーを更新
        clock.tick(50)  # フレームレートを50FPSに設定

if __name__ == "__main__":
    pg.init()  # pygameを初期化
    main()  # メイン関数を呼び出し
    pg.quit()  # pygameを終了
    sys.exit()  # プログラムを終了
