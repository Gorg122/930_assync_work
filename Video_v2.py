import os

import cv2
import time

def Video():
    cap = cv2.VideoCapture(0)

    # Get the Default resolutions
    frame_width = int(cap.get(3))
    frame_height = int(cap.get(4))
    cur_dir = os.getcwd()
    print(cur_dir)

    files = "video_timing.txt"
    timing = open(files)
    time_rest = timing.readline()
    print(time_rest)
    timing.close()

    tik = time.time()
    print(tik)

    # Define the codec and filename.
    fourcc = cv2.VideoWriter_fourcc(*'MP4V')
    #out = cv2.VideoWriter('output.mp4',cv2.VideoWriter_fourcc('M','J','P','G'), 10, (frame_width,frame_height))
    out = cv2.VideoWriter('output.mp4', fourcc, 20.0, (frame_width, frame_height))



    while(cap.isOpened() ):
        ret, frame = cap.read()
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
    cap.release()
    out.release()
    cv2.destroyAllWindows()
    time.sleep(4)
    files_2 = "video_done.txt"
    done_chek = open(files_2, "w")
    done_chek.write("done")
    done_chek.close()
#if __name__ == '__main__':
Video()