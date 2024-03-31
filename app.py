import cv2
import mediapipe as mp
import numpy as np
import math

LEFT_IRIS = [474, 475, 476, 477]
LEFT_EYE =[ 362, 382, 381, 380, 374, 373, 390, 249, 263, 466, 388, 387, 386, 385,384, 398 ]
L_H_UP=[159]
L_H_DOWN=[145]
R_H_UP=[386]
R_H_DOWN=[374]
RIGHT_IRIS = [469, 470, 471, 472]
RIGHT_EYE=[ 33, 7, 163, 144, 145, 153, 154, 155, 133, 173, 157, 158, 159, 160, 161 , 246 ] 

counter=3
flag=False
k=0

def dis(p1, p2):
    x1, y1 =p1.ravel()
    x2, y2=p2.ravel()
    return math.sqrt((x2-x1)**2 + (y2-y1)**2)

def pos(center, upoint, dpoint):
    c2d=dis(center, dpoint)
    u2d=dis(upoint, dpoint)
    r=c2d/u2d 
    if r<8:
        return 'UP'
    elif r<10:
        return 'FRONT'
    elif r<14: 
        return 'DOWN'
    else:
        return '==================================================================BLINK'

mpDraw=mp.solutions.drawing_utils
mpFaceMesh=mp.solutions.face_mesh
faceMesh=mpFaceMesh.FaceMesh(max_num_faces=1,refine_landmarks=True)
drawSpec=mpDraw.DrawingSpec(thickness=1,circle_radius=1,color=(0,255,0))
cap=cv2.VideoCapture(0)

while(True):
    s, img= cap.read()
    img=cv2.flip(img, 1)
    imgRGB=cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
    img_h, img_w =img.shape[:2]
    results=faceMesh.process(imgRGB)
    if results.multi_face_landmarks:
        facelms=results.multi_face_landmarks[0]
        meshPoints=np.array([np.multiply([p.x, p.y], [img_w, img_h]).astype(int) for p in facelms.landmark])
        # cv2.polylines(img, [meshPoints[LEFT_EYE]], True, (0, 255, 0), 1, cv2.LINE_AA)
        # cv2.polylines(img, [meshPoints[LEFT_IRIS]], True, (0, 255, 0), 1, cv2.LINE_AA)
        # cv2.polylines(img, [meshPoints[RIGHT_EYE]], True, (0, 255, 0), 1, cv2.LINE_AA)
        # cv2.polylines(img, [meshPoints[RIGHT_IRIS]], True, (0, 255, 0), 1, cv2.LINE_AA)
        # mpDraw.draw_landmarks(img,facelms,mpFaceMesh.FACEMESH_CONTOURS,drawSpec,drawSpec)
        (l_cx, L_cy), l_radius = cv2.minEnclosingCircle(meshPoints [LEFT_IRIS])
        (r_cx, r_cy), r_radius = cv2.minEnclosingCircle(meshPoints [RIGHT_IRIS])
        center_left = np.array([l_cx, L_cy], dtype=np.int32)
        center_right = np.array([r_cx, r_cy], dtype=np. int32)
        cv2. circle(img, center_left, int(l_radius), (255, 0, 255), 1, cv2. LINE_AA)
        cv2. circle(img, center_right, int(r_radius), (255, 0, 255), 1, cv2.LINE_AA)
        cv2. circle(img, meshPoints[R_H_UP][0], 2, (255, 255, 255), -1, cv2 .LINE_AA)
        cv2.circle(img, meshPoints[R_H_DOWN][0], 2, (255, 255, 255), -1, cv2.LINE_AA)
        res=pos(center_right, meshPoints[R_H_UP], meshPoints[R_H_DOWN])
        if res in ['UP', 'FRONT']:
            flag=False
            k=0
        
        elif res=='DOWN':
            if k==counter:
                print("CHEATER")
            elif not flag:
                k+=1
            else: 
                k+=1
        else:
            print(res)
            flag=False
            k=0
        # print(res)
        # for id,lm in enumerate(facelms.landmark):
        #     print(lm)
        #     h,w,c=img.shape
        #     x,y=int(lm.x*w),int(lm.y*h)
        #     print(id,x,y)

    cv2.imshow("Video", img)
    if cv2.waitKey(1) & 0xff == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
