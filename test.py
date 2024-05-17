import cv2
import mediapipe as mp
import numpy as np
import math

LEFT_IRIS = [474, 475, 476, 477]
LEFT_EYE = [362, 382, 381, 380, 374, 373, 390, 249, 263, 466, 388, 387, 386, 385, 384, 398]
L_UP = [159]
L_DOWN = [145]
R_UP = [386]
R_DOWN = [374]
L_R = [263]
L_L = [362]
R_R = [33]
R_L = [133]
RIGHT_IRIS = [469, 470, 471, 472]
RIGHT_EYE = [33, 7, 163, 144, 145, 153, 154, 155, 133, 173, 157, 158, 159, 160, 161, 246]


class Process:
    def __init__(self) -> None:
        self.b = 0.15
        self.c = 0.27
        self.flag = False                   
        self.counter = 4
        self.mpDraw = mp.solutions.drawing_utils
        self.mpFaceMesh = mp.solutions.face_mesh
        self.faceMesh = self.mpFaceMesh.FaceMesh(max_num_faces=1, refine_landmarks=True)
        self.drawSpec = self.mpDraw.DrawingSpec(thickness=1, circle_radius=1, color=(0, 255, 0))

    def dis(self,p1, p2):
        x1, y1 = p1.ravel()
        x2, y2 = p2.ravel()
        return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)


    def pos(self,lpoint, rpoint, upoint, dpoint):
        l2r = self.dis(lpoint, rpoint)
        u2d = self.dis(upoint, dpoint)
        r = u2d / l2r
        return r

    def ProcessImage(self,vid):
        res="0"
        # print(self.k)
        img = cv2.flip(vid, 1)
        imgRGB = cv2.cvtColor(vid, cv2.COLOR_BGR2RGB)
        img_h, img_w = img.shape[:2]
        results = self.faceMesh.process(imgRGB)
        if results.multi_face_landmarks:
            facelms = results.multi_face_landmarks[0]
            meshPoints = np.array([[int(p.x * img_w), int(p.y * img_h)] for p in facelms.landmark])

            r = (self.pos(meshPoints[R_R], meshPoints[R_L], meshPoints[R_UP], meshPoints[R_DOWN],)
                    + self.pos(meshPoints[L_R], meshPoints[L_L], meshPoints[L_UP], meshPoints[L_DOWN],)) / 2
            print(r)
            if r >= self.c:
                self.flag = False
                self.k = 0
                pass
            elif r >= self.b:
                # self.k += 1
                if self.flag:
                    if self.k == self.counter:
                        self.flag = False
                        res="1"
                        self.k=0
                        self.flag=False
                    else:
                        pass
                        self.k += 1
                else:
                    self.flag = True
                    self.k = 1
            else:
                self.k = 0
                self.flag = False
                pass
        else:
            self.k = 0
            self.flag = False
            pass
        if res=="1": 
            print("===============================================Cheater===============================================")
        return res
