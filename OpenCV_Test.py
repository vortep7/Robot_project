import cv2

camera = cv2.VideoCapture(0)

while True:
    success, frame = camera.read()

    if success:
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        binary = cv2.inRange(hsv, (55, 0, 90), (160, 255, 255))

        roi = cv2.bitwise_and(frame, frame, mask=binary)  # за счет полученной маски можно выделить найденный объект из общего кадра
        contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

        if len(contours) != 0:
            maxc = max(contours, key=cv2.contourArea)
            moments = cv2.moments(maxc)

            if moments["m00"] > 20:
                cx = int(moments["m10"] / moments["m00"])
                cy = int(moments["m01"] / moments["m00"])

    cv2.imshow('frame', frame)  # выводим все кадры на экран
    cv2.imshow('binary', binary)
    cv2.imshow('roi', roi)

    if cv2.waitKey(1) == ord('q'):
        break