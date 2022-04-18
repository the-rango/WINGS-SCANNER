import cv2
import numpy as np

# define a video capture object
vid = cv2.VideoCapture(0)

while(True):
    # Capture the video frame
    # by frame
    ret, frame = vid.read()

    # Converts images from BGR to HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    upper_blue = np.array([121,100,188])
    lower_blue = np.array([50,0,0])

    # Here we are defining range of bluecolor in HSV
    # This creates a mask of blue coloured
    # objects found in the frame.
    mask = cv2.inRange(hsv, lower_blue, upper_blue)

    # The bitwise and of the frame and mask is done so
    # that only the blue coloured objects are highlighted
    # and stored in res
    res = cv2.bitwise_and(frame,frame, mask= mask)
    # cv2.imshow('mask',mask)
    cv2.imshow('res',res)

    thresh_img = cv2.threshold(mask, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]

    cnts = cv2.findContours(thresh_img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if len(cnts) == 2 else cnts[1]

    ticket = []

    for cnt in cnts:
        approx = cv2.contourArea(cnt)
        if approx > 57000 :
            ticket.append(cnt)
            print(approx)

    cv2.drawContours(frame, ticket, -1, (0,255,0), 3)

    if len(ticket) > 0:
        (x,y,w,h) = cv2.boundingRect(ticket[0])
        crop = res[y:y+h,x:x+w]
        cv2.imshow("crop", crop)
        break


    # Display the resulting frame
    cv2.imshow('frame', frame)

    # the 'q' button is set as the
    # quitting button you may use any
    # desired button of your choice
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.imwrite('t1.png',crop)

# After the loop release the cap object
vid.release()
# Destroy all the windows
cv2.destroyAllWindows()
