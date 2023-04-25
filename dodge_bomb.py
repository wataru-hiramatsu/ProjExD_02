import random
import sys

import pygame as pg


def check_bound(screen: pg.Surface, obj_rect:pg.Rect):
    """
    オブジェクトが画面内or画面外を判定し、真偽値タプルを返す変数
    引数1: 画面Surface
    引数2: 判定したいSurfaceのRect
    返り値: 横方向、縦方向のはみ出し結果（画面内=True）
    """
    width = 0 <= obj_rect.left and obj_rect.right <= screen.get_width()
    height = 0 <= obj_rect.top and obj_rect.bottom <= screen.get_height()
    return (width, height)

def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((1600, 900))
    clock = pg.time.Clock()
    bg_img = pg.image.load("ex02/fig/pg_bg.jpg")
    kk_img = pg.image.load("ex02/fig/3.png")
    kk_img = pg.transform.rotozoom(kk_img, 0, 2.0)
    kk_img_flip = pg.transform.flip(kk_img, True, False)
    kk_rect = kk_img.get_rect()
    kk_rect.center = (900, 400)
    # キー毎の移動量
    kk_move_assign = {
        pg.K_UP: (0, -1),
        pg.K_DOWN: (0, 1),
        pg.K_LEFT: (-1, 0),
        pg.K_RIGHT: (1, 0),
    }
    kk_imgs = {
        (-1, 0): kk_img,
        (-1, -1): pg.transform.rotozoom(kk_img, -45, 1),
        (-1, 1): pg.transform.rotozoom(kk_img, 45, 1),
        (0, -1): pg.transform.rotozoom(kk_img_flip, 90, 1),
        (1, 0): kk_img_flip,
        (1, -1): pg.transform.rotozoom(kk_img_flip, 45, 1),
        (0, 1): pg.transform.rotozoom(kk_img_flip, -90, 1),
        (1, 1): pg.transform.rotozoom(kk_img_flip, -45, 1),
    }
    # 爆弾
    bomb_img = pg.Surface((20, 20))
    pg.draw.circle(bomb_img, (255, 0, 0), (10, 10), 10)
    bomb_img.set_colorkey((0, 0, 0))
    bomb_rect = bomb_img.get_rect()
    bomb_rect.center = (
        random.randint(0 + bomb_rect.width / 2, screen.get_width() - bomb_rect.width / 2),
        random.randint(0 + bomb_rect.height / 2, screen.get_height() - bomb_rect.height / 2)
    )
    bomb_velocity = [1, 1]

    tmr = 0

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return 0
        key_lst = pg.key.get_pressed()
        kk_velo = [0, 0]
        for key in kk_move_assign.keys():
            pos = kk_rect.center
            if key_lst[key]:
                kk_velo[0] += kk_move_assign[key][0]
                kk_velo[1] += kk_move_assign[key][1]

        if tuple(kk_velo) in kk_imgs.keys():
            kk_img = kk_imgs[tuple(kk_velo)]
        kk_rect.move_ip(kk_velo)
        bound = check_bound(screen, kk_rect)
        if (not bound[0]) or (not bound[1]):
            kk_rect.center = pos

        tmr += 1
        screen.blit(bg_img, [0, 0])
        screen.blit(kk_img, kk_rect)

        bomb_rect.move_ip(bomb_velocity)
        bound = check_bound(screen, bomb_rect)
        if (not bound[0]) or (not bound[1]):
            bomb_velocity[0] *= -1
            bomb_velocity[1] *= -1
        screen.blit(bomb_img, bomb_rect)

        if kk_rect.colliderect(bomb_rect):
            return

        pg.display.update()
        clock.tick(1000)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
