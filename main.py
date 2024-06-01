import pygame as pg
import pynput.mouse as mouse
import screeninfo
import classes as cl
import threading as thr
import json

WINDOW_SIZE = cl.Pos(screeninfo.get_monitors()[-1].width, screeninfo.get_monitors()[-1].height)


def doing(poses):
    mCon = mouse.Controller()
    for i in poses:
        assert not ((i.pos() > WINDOW_SIZE or i.pos() < 0) and not i.local)
        i.do(mCon)


def recording() -> list[cl.MouseEvent]:
    return


def main():
    pg.init()

    config = {}

    with open('config.json') as f:
        try:
            config = json.loads(f.read())
        except json.decoder.JSONDecodeError as ex:
            if 'FPS' not in config.keys():
                config['FPS'] = 60
            if 'WIDTH' not in config.keys():
                config['WIDTH'] = WINDOW_SIZE.x
            if 'HEIGHT' not in config.keys():
                config['HEIGHT'] = WINDOW_SIZE.y
            if 'FONT' not in config.keys():
                config['FONT'] = 'Arial'
            if 'FONT_SIZE' not in config.keys():
                config['FONT_SIZE'] = 20

            with open('config.json', 'w') as f:
                f.write(json.dumps(config))

    dis = pg.display.set_mode((config['WIDTH'], config['HEIGHT']))

    clock = pg.time.Clock()

    poses = []
    doingThr = thr.Thread(target=doing, daemon=True, args=(poses,))

    run = True
    text = cl.cnvs.Text(cl.Pos(1920/2, 0), 'I am flood', pg.font.SysFont('Arial', 20), [0, 0, 0], 1, isCenteredX=True)

    while run:
        dis.fill([255, 255, 255])
        for i in pg.event.get():
            if i.type == pg.QUIT:
                run = False
            elif i.type == pg.KEYDOWN:
                if i.key == pg.K_ESCAPE:
                    run = False
        text.draw(dis)

        pg.display.update()
        clock.tick(config['FPS'])


if __name__ == '__main__':
    main()
