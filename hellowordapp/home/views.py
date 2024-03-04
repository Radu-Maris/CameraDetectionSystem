import threading

import cv2
from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators import gzip
from django.http import StreamingHttpResponse

@gzip.gzip_page
def index(request):
    try:
        cam = VideoCamera()
        return StreamingHttpResponse(gen(cam), content_type="multipart/x-mixed-replace;boundary=frame")
    except:
        pass
    return render(request, 'CameraInput.html')


class VideoCamera(object):
    static_back = None
    gray = None

    def __init__(self):
        self.video = cv2.VideoCapture(0)

    def __del__(self):
        self.video.release()

    def get_frame(self):
        check, frame = self.video.read()
        motion = 0
        # transforms the camera input to grayscale values
        self.gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)

        if self.static_back is None:
            self.static_back = self.gray

        # generate the difference frame
        diff_frame = cv2.absdiff(self.static_back, self.gray)

        # If change between static background and current frame greater than
        # threshold it becomes white
        threshold = cv2.threshold(diff_frame, 30, 255, cv2.THRESH_BINARY)[1]

        # Finding contour of moving object
        contours, aux = cv2.findContours(threshold.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
        contours2, aux2 = cv2.findContours(self.gray.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

        for contour in contours:
            if cv2.contourArea(contour) < 10000:
                continue
            # draws a rectangle around the object
            (x, y, w, h) = cv2.boundingRect(contour)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 5)

            for contour2 in contours2:
                (x2, y2, w2, h2) = cv2.boundingRect(contour2)
                cv2.rectangle(frame, (x2, y2), (x2 + w2, y2 + h2), (0, 0, 255), 5)

        ret, jpeg = cv2.imencode('.jpg', frame)
        return jpeg.tobytes()

    def update(self):
        while True:
            (self.grabbed, self.frame) = self.video.read()


def gen(camera):
    while True:
        video = camera.get_frame()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + video + b'\r\n\r\n')
