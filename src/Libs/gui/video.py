import cv2
from PIL import ImageTk, Image

def video():
    cap = cv2.VideoCapture(0)

    _, frame = cap.read()
    cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
    cv2image = cv2.resize(cv2image,(0,0), fx = 0.4, fy = 0.4, interpolation = cv2.INTER_CUBIC)
    img = Image.fromarray(cv2image) #Bis hier ist es auf dem Flugzeug
    img = img.resize((320,240))
    imgbytes = img.tobytes()
    return imgbytes

if __name__ == "__main__":
    pass
