import random
import sys
import pygame as pg


WIDTH, HEIGHT = 1600, 900


def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("ex02/fig/pg_bg.jpg")
    kk_img = pg.image.load("ex02/fig/3.png")
    kk_img = pg.transform.rotozoom(kk_img, 0, 2.0)
    bb_img = pg.Surface((20, 20))  # 練習1 透明なSurfaceを作る
    pg.draw.circle(bb_img, (255, 0, 0), (10, 10), 10)  # 練習1 半径10の赤い円を描く
    bb_img.set_colorkey((0, 0, 0))
    bb_rct = bb_img.get_rect() # 練習1 
    bb_rct.centerx = random.randint(0, WIDTH)
    bb_rct.centery = random.randint(0, HEIGHT)
    
    clock = pg.time.Clock()
    tmr = 0
    vx, vy = +5, +5

    while True:

        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return

        screen.blit(bg_img, [0, 0])
        screen.blit(kk_img, [900, 400])
        bb_rct.move_ip(vx, vy)
        screen.blit(bb_img, bb_rct)

        pg.display.update()
        tmr += 1
        clock.tick(10)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()