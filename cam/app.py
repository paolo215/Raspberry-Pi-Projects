from flask import Flask
from flask import render_template
from flask import Response
from gevent.pywsgi import WSGIServer

from usb_opencv import USB_OpenCV

from threading import Thread
import cv2

app = Flask(__name__, static_url_path="/static")

@app.route("/")
def index():
    return render_template("index.html")

def get_frame(camera):
    while True:
        if camera.isOpened():
            return_value, frame = camera.get_frame()
            if return_value:
                return_value, frame = cv2.imencode(".jpg", frame)
                frame = frame.tobytes() 
                yield (b" --frame\r\n" \
                    b"Content-Type: image/jpeg\r\n\r\n" + frame + b"\r\n\r\n")

@app.route("/video_feed")
def video_feed():
    return Response(get_frame(camera), mimetype="multipart/x-mixed-replace; boundary=frame")

if __name__ == "__main__":
    global camera
    port = 5000
    camera = USB_OpenCV("app", (640, 480))
    if camera.isOpened():
        t1 = Thread(target=camera.start_record, args=(60*5,))
        t1.daemon = True
        t1.start()

        server = WSGIServer(("", port), app) 
        
        print("Starting: " + str(port))
        server.serve_forever()
    else:
        print("Camera not found")


