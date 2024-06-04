import time
import pynput.mouse as mouse
import pynput.keyboard as keyb
import objects as cl
import threading as thr


def doing(poses):
    global isDoing
    t = time.time()
    mCon = mouse.Controller()
    for i in poses:
        if isDoing:
            i.do(mCon)
    print(f'Doing took {time.time() - t} s')
    isDoing = False


def keyHandler():
    print('KeyHandler started')

    def onPress(key):
        global isRecording, recordingThr, result, isRecordingFinished, isRecordingPaused, isDoing, poses, run
        print('Key pressed')
        if key == keyb.Key.shift_r and not isRecordingFinished:
            isRecording = not isRecording
            isRecordingPaused = False
            if isRecording:
                recordingThr = thr.Thread(target=recording, daemon=True)
                recordingThr.start()
            else:
                while not recordingThr.is_alive():
                    continue
                recordingThr.join()
                result = recordingThr.result
                isRecordingFinished = True
        elif key == keyb.Key.ctrl_r:
            isRecordingPaused = not isRecordingPaused
        elif key == keyb.Key.insert:
            isDoing = True
            doingThr = thr.Thread(target=doing, daemon=True, args=(poses,))
            doingThr.start()
        elif key == keyb.Key.end:
            run = False

    kLis = keyb.Listener(on_press=onPress)
    kLis.start()


def recording():
    global isRecording, curTime, isRecordingPaused

    recorded = []

    curTime = time.time()

    def logMove(x, y):
        global curTime
        if not isRecording:
            return False
        if isRecordingPaused:
            curTime = time.time()
            pass
        elif isRecording:
            print('Move!')
            recorded.append(
                cl.MouseEvent(delayB=time.time() - curTime, isPress=False, isRelease=False, local=False, x=x, y=y))
            curTime = time.time()

    def logClick(x, y, button, pressed):
        global curTime
        if not isRecording:
            return False
        if isRecordingPaused:
            curTime = time.time()
            pass
        elif isRecording:
            print('Click!')
            recorded.append(
                cl.MouseEvent(delayB=time.time() - curTime, isPress=pressed, isRelease=not pressed, button=button))
            curTime = time.time()

    mLis = mouse.Listener(
        on_move=logMove,
        on_click=logClick)
    mLis.start()
    while isRecording:
        if isRecordingPaused:
            curTime = time.time()
    mLis.stop()
    mLis.join()

    print(recorded)
    thr.current_thread().result = recorded


def main():
    global isRecording, isRecordingFinished, result, isRecordingPaused, poses, run

    poses = [cl.MouseEvent(delayB=95)]

    isRecording = False

    keyHandlerThr = thr.Thread(target=keyHandler, daemon=True)

    keyHandlerThr.start()

    isRecordingFinished = False
    isRecordingPaused = False

    run = True
    while run:
        if isRecordingFinished:
            poses = result

            isRecordingFinished = False
            print('Recording was finished')

        time.sleep(1 / 60)


if __name__ == '__main__':
    main()
