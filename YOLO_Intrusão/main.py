import cv2
from ultralytics import YOLO
import winsound
import threading

video = cv2.VideoCapture("ex01.mp4")
modelo = YOLO('yolov8n.pt')

area = [510,230,910,700]

alarmeCtl = False
def alarme():
    for _ in range(5):
        global alarmeCtl
        winsound.Beep(2500,500)
        alarmeCtl = False

while True:
    check, img = video.read()
    img = cv2.resize(img, (1270, 720))
    img2 = img.copy()
    cv2.rectangle(img2, (area[0],area[1]),(area[2],area[3]), (0,255,0), -1)
    resultado = modelo(img)

    for objectos in resultado:
        obj = objectos.boxes
        for dados in obj:
            x,y,w,h = dados.xyxy[0]
            x,y,w,h = int(x), int(y), int(w), int(h)
            cls = int(dados.cls[0])
            cx, cy =(x+w)//2,(y+h)//2
           #cv2.circle(img, (cx,cy), 5, (0,0,0), 2)
            if cls == 0:
                cv2.rectangle(img, (x,y),(w,h), (255,0,0), 2)
                if cx >= area[0] and cx <= area [2] and cy>=area[1] and cy <= area[3]:
                    cv2.rectangle(img2, (area[0],area[1]),(area[2],area[3]), (0,0,255), -1)
                    cv2.rectangle(img, (100,30), (470,80), (0,0,255), -1)
                    cv2.putText(img, 'INVASOR DETECTADO', (105,65), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 3)
                    if not alarmeCtl:
                        alarmeCtl = True
                        threading.Thread(target=alarme).start()
            


    #print(resultado)
    imgFinal = cv2.addWeighted(img2,0.5,img,0.5,0)
    cv2.imshow('img', imgFinal)
    cv2.waitKey(1)