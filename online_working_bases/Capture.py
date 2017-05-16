import numpy as np
import cv2

cap = cv2.VideoCapture(0)
blank_image = np.zeros((500,500,3), np.uint8)

while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()
    try:
    # Display the resulting frame
        cv2.imshow('frame',frame)
    except:
        frame = blank_image
        cv2.imshow('frame',frame)
    cv2.moveWindow("frame",-15,528)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
