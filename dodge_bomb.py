import random
import sys
import pygame as pg


WIDTH, HEIGHT = 1600, 900

delta = {  # 練習3 押下キーと移動量の定義
    pg.K_UP: (0, -5),
    pg.K_DOWN: (0, 5),
    pg.K_LEFT: (-5, 0),
    pg.K_RIGHT: (5, 0)
}

kk_img0 = pg.transform.rotozoom(pg.image.load("ex02/fig/3.png"), 0, 2.0)
kk_img = pg.transform.flip(kk_img0, True, False)

kk_img_GO = pg.transform.rotozoom(pg.image.load("ex02/fig/8.png"), 0, 2.0)  # ゲームオーバーの画像

kk_rot_dict = {  # 演習1 移動量に対するrotozoomの角度の辞書
    # (0, 0): pg.transform.rotozoom(kk_img0, 0, 1.0) ,
    (-5, 0): pg.transform.rotozoom(kk_img0, 0, 1.0) ,
    (-5, -5): pg.transform.rotozoom(kk_img0, 310, 1.0) ,
    (0, -5): pg.transform.rotozoom(kk_img, 90, 1.0) ,
    (-5, +5): pg.transform.rotozoom(kk_img0, 45, 1.0) ,
    (+5, 0): pg.transform.rotozoom(kk_img, 0, 1.0) ,
    (+5, +5): pg.transform.rotozoom(kk_img, 310, 1.0) ,
    (0, +5): pg.transform.rotozoom(kk_img0, 90, 1.0) ,
    (+5, -5): pg.transform.rotozoom(kk_img, 45, 1.0) ,
}

accs = [a for a in range(1, 11)]
bb_imgs = []
for r in range(1, 11):
    bb_img = pg.Surface((20*r, 20*r))
    pg.draw.circle(bb_img, (255, 0, 0), (10*r, 10*r), 10*r)
    bb_img.set_colorkey((0, 0, 0))
    bb_imgs.append(bb_img)
    


def check_bound(rct: pg.Rect) -> tuple:
    """
    オブジェクトが画面内 or 画面外を判定し、真理値タプルを返す関数
    引数 rct こうかとん or 爆弾SurfaceのRect
    戻り値:横方向, 縦方向のはみ出し判定結果(画面内:True/画面外:False)
    """
    yoko, tate = True, True
    if rct.left < 0 or WIDTH < rct.right:  # 横方向はみ出し
        yoko = False
    if rct.top < 0 or HEIGHT < rct.bottom:  # 縦方向はみ出し
        tate = False
    return yoko, tate


def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("ex02/fig/pg_bg.jpg")
    kk_img = pg.image.load("ex02/fig/3.png")
    kk_img = pg.transform.rotozoom(kk_img, 0, 2.0)
    kk_rct = kk_img.get_rect()
    kk_rct.center = 900, 400 # 練習3 こうかとんの初期座標
    bb_img = pg.Surface((20, 20))  # 練習1 透明なSurfaceを作る
    pg.draw.circle(bb_img, (255, 0, 0), (10, 10), 10)  # 練習1 半径10の赤い円を描く
    bb_img.set_colorkey((0, 0, 0))
    bb_rct = bb_img.get_rect() # 練習1 
    bb_rct.centerx = random.randint(0, WIDTH)
    bb_rct.centery = random.randint(0, HEIGHT)
    
    kk_img = pg.transform.rotozoom(kk_img, 10, 1.0)
    
    clock = pg.time.Clock()
    tmr = 0
    vx, vy = +5, +5
    

    while True:

        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
            
        if kk_rct.colliderect(bb_rct):  # ゲームオーバー時の処理
            kk_img = kk_img_GO
            screen.blit(bg_img, [0, 0])
            screen.blit(kk_img, kk_rct)
            pg.display.update()
            pg.time.wait(300)
            print("Game Over")
            return
        
        key_lst = pg.key.get_pressed()
        #print(len(key_lst))
        sum_mv = [0, 0]
        for k, tpl in delta.items():
            if key_lst[k]:  # キーが押されたら
                sum_mv[0] += tpl[0]
                sum_mv[1] += tpl[1]

        screen.blit(bg_img, [0, 0])
        kk_rct.move_ip(sum_mv[0], sum_mv[1]) 
        if check_bound(kk_rct) != (True, True):
            kk_rct.move_ip(-sum_mv[0], -sum_mv[1])
        # print((sum_mv[0], sum_mv[1]))
        if (sum_mv[0], sum_mv[1]) != (0, 0):
            kk_img = kk_rot_dict[(sum_mv[0], sum_mv[1])]  # 演習1
        screen.blit(kk_img, kk_rct)
        bb_img = bb_imgs[min(tmr//500, 9)]  # リストから大きさ変更
        avx, avy = vx*accs[min(tmr//500, 9)], vy*accs[min(tmr//500, 9)]  # リストから速さ変更
        bb_rct.move_ip(avx, avy)  # 練習2
        yoko, tate = check_bound(bb_rct)
        if not yoko:
            vx *= -1
        if not tate:
            vy *= -1
        bb_rct.move_ip(vx, vy)
        screen.blit(bb_img, bb_rct)

        pg.display.update()
        tmr += 1
        clock.tick(100)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()