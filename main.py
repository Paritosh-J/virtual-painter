import cv2
import numpy as np
import os
import handDetectionModule as hdm

def main():
    # importing pallete images
    
    folderPath = './pallete'
    picList = os.listdir(folderPath)
    overlayList = []
    imgHeight, imgWidth = 125, 1280
    for imgpath in picList:
        img = cv2.imread(f'{folderPath}/{imgpath}')
        overlayList.append(img)
    palleteHeader = overlayList[0]

    # color and eraser variables
    color = (0, 0, 255)
    colorThickness = 15
    eraserThickness = 80

    # frame varaibles
    drawFrame = np.zeros((720, 1280, 3), np.uint8) # unint8 - unsigned 8 bit values from 0 to 255
    xPrev, yPrev = 0, 0


    # turn on the camera (0) & start to capture
    video = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    # setting the captured video's dimensions
    wCam, hCam = 1280, 720
    video.set(3, wCam)
    video.set(4, hCam)

    detect = hdm.handDetector(maxHands=1, detectConfidence=0.95)

    while True:
        check, frame = video.read()
        frame = cv2.flip(frame, 1)
        # detect hands
        frame = detect.findHands(frame, draw=False)
        LmarkList = detect.findPosition(frame, draw=False)
        
        # get tip of index and middle fingers
        if len(LmarkList) != 0:
            x1, y1 = LmarkList[8][1:]
            x2, y2 = LmarkList[12][1:]

            # detect finger pointing up
            upFinger = detect.upFingers()

            # selection mode - index and middle fingers up
            if upFinger[1] and upFinger[2]:
                xPrev, yPrev = 0, 0
                # selecting color from pallete
                if y1 < 140:
                    if 250 < x1 < 450:  # red
                        palleteHeader = overlayList[0]
                        color = (0, 0, 255)
                    elif 550 < x1 < 750: # blue
                        palleteHeader = overlayList[1]
                        color = (255, 0, 0)
                    elif 800 < x1 < 950: # green
                        palleteHeader = overlayList[2]
                        color = (0, 255, 0)
                    elif 1050 < x1 < 1200: # eraser
                        palleteHeader = overlayList[3]
                        color = (0, 0, 0)
                cv2.rectangle(frame, (x1, y1 - 25), (x2, y2 + 25), color, cv2.FILLED)

            # draw mode - index finger up
            if upFinger[1] and upFinger[2] == False:
                cv2.circle(frame, (x1, y1), 15, color, cv2.FILLED)
                if xPrev == 0 and yPrev == 0:
                    xPrev, yPrev = x1, y1

                # if eraser chosen
                if color == (0, 0, 0):
                    cv2.line(frame, (xPrev, yPrev), (x1, y1), color, eraserThickness)
                    cv2.line(drawFrame, (xPrev, yPrev), (x1, y1), color, eraserThickness)

                # draw on frame from preveous to current coordinate
                else :
                    cv2.line(frame, (xPrev, yPrev), (x1, y1), color, colorThickness)
                    cv2.line(drawFrame, (xPrev, yPrev), (x1, y1), color, colorThickness)

                # update coordinate
                xPrev, yPrev = x1, y1

        grayImg = cv2.cvtColor(drawFrame, cv2.COLOR_BGR2GRAY) # convert frame into grayscale image
        x, inverseImg = cv2.threshold(grayImg, 50, 255, cv2.THRESH_BINARY_INV)  # convert into inverse image
        inverseImg = cv2.cvtColor(inverseImg, cv2.COLOR_GRAY2BGR) # convert grayscale image back to colored image
        frame = cv2.bitwise_and(frame, inverseImg)  # add inverse image frame to main frame
        frame = cv2.bitwise_or(frame, drawFrame)    # combine color frame with current frame (inverseImge + main frame)

        # set pallete image
        frame[0:imgHeight, 0:imgWidth] = palleteHeader
        
        cv2.putText(frame, "Press 'q' to exit", (20, 700), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
        cv2.imshow('=== Virtual Painter ===', frame)  # open window for showing the o/p

        # escape key
        if cv2.waitKey(1) == ord('q'):
            break

    # release the captured video and distroy all windows
    video.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
