import random
import sys
import math

import pygame as pg

def sign(value: int) -> int:
    """
    値の符号を返す関数
    引数1: 符号を判定したいint変数
    返り値: 符号（負=-1, ゼロ=0, 正=1）
    """
    if (value < 0):
        return -1
    if (value is 0):
        return 0
    return 1

def length(pos1: tuple, pos2: tuple) -> float:
    """
    ベクトルの長さを返す関数
    引数1: ベクトル1 (タプル)
    引数2: ベクトル2（タプル）
    返り値: 長さ
    """
    return math.sqrt((pos1[0] - pos2[0]) ** 2 + (pos1[1] - pos2[1]) ** 2)

def change_length(lst: list, after_length: int):
    """
    ベクトルの長さを変更する関数
    引数1: 長さを変更したりベクトル
    引数2: 変更後の長さ
    """
    l = length((0, 0), tuple(lst))
    rst = [0, 0]
    rst[0] = lst[0] / l * after_length
    rst[1] = lst[1] / l * after_length
    return rst

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
    is_gameover = False
    tmr = 0
    gameover_tmr = 0

    # 背景
    bg_img = pg.image.load("ex02/fig/pg_bg.jpg")

    # こうかとん
    kk_img = pg.image.load("ex02/fig/3.png")
    kk_img = pg.transform.rotozoom(kk_img, 0, 2.0)
    kk_img_flip = pg.transform.flip(kk_img, True, False)
    kk_gameover_img = pg.image.load("ex02/fig/6.png")
    kk_gameover_img = pg.transform.rotozoom(kk_gameover_img, -90, 2.0)
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
    bomb_accs = [a for a in range(1, 11)]
    bomb_imgs = []
    for r in range(1, 11):
        img = pg.Surface((20 * r, 20 * r))
        pg.draw.circle(img, (255, 0, 0), (10 * r, 10 * r), 10 * r)
        img.set_colorkey((0, 0, 0))
        bomb_imgs.append(img)
    bomb_velocity_normalized = change_length([1, 1], 1)

    while True:
        tmr += 1
        # イベントの受け取り
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return 0

        # 背景の描画
        screen.blit(bg_img, [0, 0])

        # ゲームオーバー時処理
        if is_gameover:
            screen.blit(kk_gameover_img, kk_rect)
            if tmr - gameover_tmr >= 3000:
                return
            pg.display.update()
            clock.tick(1000)
            continue

        # こうかとんの移動方向決定
        kk_velo = [0, 0]
        for key in kk_move_assign.keys():
            pos = kk_rect.center
            if pg.key.get_pressed()[key]:
                kk_velo[0] += kk_move_assign[key][0]
                kk_velo[1] += kk_move_assign[key][1]

        # こうかとんの表示画像の決定
        if tuple(kk_velo) in kk_imgs.keys():
            kk_img = kk_imgs[tuple(kk_velo)]

        # こうかとん移動&描画
        kk_rect.move_ip(kk_velo)
        bound = check_bound(screen, kk_rect)
        if (not bound[0]) or (not bound[1]):
            kk_rect.center = pos

        # 爆弾移動ベクトル決定
        bomb_velocity = [0.0, 0.0]
        if length(kk_rect.center, bomb_rect.center) >= 500:
            sabun = [
                kk_rect.center[0] - bomb_rect.center[0],
                kk_rect.center[1] - bomb_rect.center[1]
            ]
            bomb_velocity_normalized = change_length(sabun, 1)

        bomb_velocity[0] = round(bomb_velocity_normalized[0] * bomb_accs[min(tmr // 1000, 9)])
        bomb_velocity[1] = round(bomb_velocity_normalized[1] * bomb_accs[min(tmr // 1000, 9)])

        # 爆弾移動＆描画
        bomb_rect.move_ip(bomb_velocity)
        bound = check_bound(screen, bomb_rect)
        if (not bound[0]):
            bomb_velocity_normalized[0] *= -1
        if not bound[1]:
            bomb_velocity_normalized[1] *= -1
        screen.blit(bomb_imgs[min(tmr // 1000, 9)], bomb_rect)

        # ゲームオーバー判定
        if kk_rect.colliderect(bomb_rect):
            screen.blit(kk_gameover_img, kk_rect)
            is_gameover = True
            gameover_tmr = tmr
        else:
            screen.blit(kk_img, kk_rect)

        # 更新処理
        pg.display.update()
        clock.tick(1000)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
