import os

import cv2
import time

def Video():
    #cap = cv2.VideoCapture(0)

    HIGH_VALUE = 10000
    WIDTH = HIGH_VALUE
    HEIGHT = HIGH_VALUE

    capture = cv2.VideoCapture(0)

    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    #focus = int(capture.get(cv2.CAP_PROP_AUTOFOCUS))
    capture.set(cv2.CAP_PROP_FRAME_WIDTH, WIDTH)
    capture.set(cv2.CAP_PROP_FRAME_HEIGHT, HEIGHT)
    #capture.set(cv2.CAP_PROP_FOCUS, 200)
    capture.set(cv2.CAP_PROP_AUTOFOCUS, 1)
    width = int(capture.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(capture.get(cv2.CAP_PROP_FRAME_HEIGHT))


    # Get the Default resolutions
    #frame_width = int(cap.get(3))
    #frame_height = int(cap.get(4))
    cur_dir = os.getcwd()
    #os.chdir(cur_dir)
    print(cur_dir)
    print(width)
    print(height)

    files = "video_timing.txt"
    timing = open(files)
    time_rest = timing.readline()
    print(time_rest)
    timing.close()

    tik = time.time()
    print(tik)

    # Define the codec and filename.
    #fourcc = cv2.VideoWriter_fourcc(*'MP4V')
    #out = cv2.VideoWriter('output.mp4',cv2.VideoWriter_fourcc('M','J','P','G'), 10, (frame_width,frame_height))
    out = cv2.VideoWriter('video/output.mp4', fourcc, 30.0, (width, height))



    while(capture.isOpened() ):
        ret, frame = capture.read()
        tok = time.time()
        if ret==True :
            # write the  frame
            out.write(frame)
            #cv2.imshow('frame',frame)
            #if cv2.waitKey(1) & 0xFF == ord('q') & int(tok - tik) >= 30:
            if int(tok - tik) >= int(time_rest):
                break
        else:

            break

    # Release everything if job is finished
    capture.release()
    out.release()
    cv2.destroyAllWindows()
    time.sleep(4)
    files_2 = "video_done.txt"
    done_chek = open(files_2, "w")
    done_chek.write("done")
    done_chek.close()
#if __name__ == '__main__':
Video()
