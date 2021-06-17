import cv2
import time
import datetime

def gstreamer_pipeline(
    capture_width=600,
    capture_height=400,
    display_width=600,
    display_height=400,
    framerate=60,
    flip_method=0,
):
    return (
        "nvarguscamerasrc ! "
        "video/x-raw(memory:NVMM), "
        "width=(int)%d, height=(int)%d, "
        "format=(string)NV12, framerate=(fraction)%d/1 ! "
        "nvvidconv flip-method=%d ! "
        "video/x-raw, width=(int)%d, height=(int)%d, format=(string)BGRx ! "
        "videoconvert ! "
        "video/x-raw, format=(string)BGR ! appsink"
        % (
            capture_width,
            capture_height,
            framerate,
            flip_method,
            display_width,
            display_height,
        )
    )
count=0
cap = cv2.VideoCapture(gstreamer_pipeline(), cv2.CAP_GSTREAMER)
while (cap.isOpened):
	ret, img = cap.read()
	img = cv2.cvtColor(img, cv2.IMREAD_COLOR)
	cv2.imwrite(f"./data/background/{time.strftime('%Y-%m-%d-%h-%m-%s', time.localtime(time.time()))}.png", img, params=[cv2.IMWRITE_PNG_COMPRESSION, 0])
	time.sleep(1)
	print(count)
	count += 1
cap.release()
cv2.destroyAllWindows()


