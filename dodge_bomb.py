import pygame as pg
import sys
import random


def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((1600, 900))
    clock = pg.time.Clock()
    bg_img = pg.image.load("ex02/fig/pg_bg.jpg")
    kk_img = pg.image.load("ex02/fig/3.png")
    kk_img = pg.transform.rotozoom(kk_img, 0, 2.0)
    kk_rect = kk_img.get_rect()
    kk_rect.center = (900, 400)
    # キー毎の移動量
    kk_move_assign = {
        pg.K_UP: (0, -1),
        pg.K_DOWN: (0, 1),
        pg.K_LEFT: (-1, 0),
        pg.K_RIGHT: (1, 0),
    }
    # 爆弾
    bomb_img = pg.Surface((20, 20))
    pg.draw.circle(bomb_img, (255, 0, 0), (10, 10), 10)
    bomb_img.set_colorkey((0, 0, 0))
    bomb_rect = bomb_img.get_rect()
    bomb_rect.center = (
        random.randint(0, 1600),
        random.randint(0, 900)
    )

    tmr = 0

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return 0
        key_lst = pg.key.get_pressed()
        for key in kk_move_assign.keys():
            if key_lst[key]:
                kk_rect.move_ip(kk_move_assign[key])

        tmr += 1
        screen.blit(bg_img, [0, 0])
        screen.blit(kk_img, kk_rect)
        screen.blit(bomb_img, bomb_rect)
        bomb_rect.move_ip(1, 1)

        pg.display.update()
        clock.tick(1000)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
