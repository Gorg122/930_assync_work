import numpy as np
import cv2
import time

cap = cv2.VideoCapture(0)

# Get the Default resolutions
frame_width = int(cap.get(3))
frame_height = int(cap.get(4))

tik = time.time()
print(tik)
# Define the codec and filename.
out = cv2.VideoWriter('output.avi',cv2.VideoWriter_fourcc('M','J','P','G'), 20, (frame_width,frame_height))



while(cap.isOpened() ):
    ret, frame = cap.read()
    tok = time.time()
    if ret==True :
        # write the  frame
        out.write(frame)
        cv2.imshow('frame',frame)
        #if cv2.waitKey(1) & 0xFF == ord('q') & int(tok - tik) >= 30:
        if int(tok - tik) >= 40:
            break
    else:
        break

# Release everything if job is finished
cap.release()
out.release()
cv2.destroyAllWindows()
