import cv2
import pathlib
import time
import pandas
from datetime import datetime


first_frame = None
status_list = [None, None]
times = []
df = pandas.DataFrame(columns=['Start', 'End'])

# Check if folder exists else create it
pathlib.Path('./captured_images').mkdir(parents=True, exist_ok=True)

video_capture = cv2.VideoCapture(0)
time.sleep(1)

while True:
    success, frame = video_capture.read()
    status = 0

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (51, 51), 0)

    if first_frame is None:
        first_frame = gray
        continue

    delta_frame = cv2.absdiff(first_frame, gray)
    thresh_frame = cv2.threshold(delta_frame, 10, 255, cv2.THRESH_BINARY)[1]
    thresh_frame = cv2.dilate(thresh_frame, None, iterations=2)

    (cnts, _) = cv2.findContours(thresh_frame,
                                 cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    for contour in cnts:
        if cv2.contourArea(contour) < 20000:
            continue
        status = 1
        (x, y, w, h) = cv2.boundingRect(contour)
        cv2.drawContours(frame, contour, -1, (0, 255, 0), 2)

        # Image capturing when detect moving object
        cv2.imwrite(
            f'captured_images/image_captured{datetime.now()}.png', frame)

    status_list.append(status)
    status_list = status_list[-2:]

    if status_list[-1] == 1 and status_list[-2] == 0:
        times.append(datetime.now())
    if status_list[-1] == 0 and status_list[-2] == 1:
        times.append(datetime.now())

    cv2.imshow('Color Frame', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        if status == 1:
            times.append(datetime.now())
        break

for i in range(0, len(times), 2):
    df = df.append({"Start": times[i], "End": times[i+1]}, ignore_index=True)
df.to_csv("times.csv")

video_capture.release()
cv2.destroyAllWindows()
