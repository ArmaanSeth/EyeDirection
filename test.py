import cv2
import mediapipe as mp
import numpy as np
import math

LEFT_IRIS = [474, 475, 476, 477]
LEFT_EYE = [
    362,
    382,
    381,
    380,
    374,
    373,
    390,
    249,
    263,
    466,
    388,
    387,
    386,
    385,
    384,
    398,
]
L_UP = [159]
L_DOWN = [145]
R_UP = [386]
R_DOWN = [374]
L_R = [263]
L_L = [362]
R_R = [33]
R_L = [133]
RIGHT_IRIS = [469, 470, 471, 472]
RIGHT_EYE = [
    33,
    7,
    163,
    144,
    145,
    153,
    154,
    155,
    133,
    173,
    157,
    158,
    159,
    160,
    161,
    246,
]


# counter=5
# flag=False
# k=0
# b=-1
# c=-1
# f1=0
# f2=False
# ls=[]
def dis(p1, p2):
    x1, y1 = p1.ravel()
    x2, y2 = p2.ravel()
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)


def pos(lpoint, rpoint, upoint, dpoint):
    l2r = dis(lpoint, rpoint)
    u2d = dis(upoint, dpoint)
    r = u2d / l2r
    return r


mpDraw = mp.solutions.drawing_utils
mpFaceMesh = mp.solutions.face_mesh
faceMesh = mpFaceMesh.FaceMesh(max_num_faces=1, refine_landmarks=True)
drawSpec = mpDraw.DrawingSpec(thickness=1, circle_radius=1, color=(0, 255, 0))


def processOutput(vid):
    counter = 5
    flag = False
    k = 0
    b = -1
    c = -1
    f1 = 0
    f2 = False
    ls = []
    # cap = cv2.VideoCapture(vid);
    # s, img= cap.read()
    img = cv2.flip(vid, 1)
    imgRGB = cv2.cvtColor(vid, cv2.COLOR_BGR2RGB)
    img_h, img_w = img.shape[:2]
    results = faceMesh.process(imgRGB)
    if results.multi_face_landmarks:
        facelms = results.multi_face_landmarks[0]
        meshPoints = np.array(
            [
                np.multiply([p.x, p.y], [img_w, img_h]).astype(int)
                for p in facelms.landmark
            ]
        )
        (l_cx, L_cy), l_radius = cv2.minEnclosingCircle(meshPoints[LEFT_IRIS])
        (r_cx, r_cy), r_radius = cv2.minEnclosingCircle(meshPoints[RIGHT_IRIS])
        center_left = np.array([l_cx, L_cy], dtype=np.int32)
        center_right = np.array([r_cx, r_cy], dtype=np.int32)
        cv2.circle(img, center_left, int(l_radius), (255, 0, 255), 1, cv2.LINE_AA)
        cv2.circle(img, meshPoints[R_UP][0], 2, (255, 255, 255), -1, cv2.LINE_AA)
        cv2.circle(img, meshPoints[R_DOWN][0], 2, (255, 255, 255), -1, cv2.LINE_AA)
        if f2:
            cv2.putText(
                img,
                f"Bottom: {b:.2f}",
                (50, img_h - 100),
                cv2.FONT_HERSHEY_COMPLEX,
                1,
                (255, 0, 0),
                2,
                cv2.LINE_AA,
            )
            cv2.putText(
                img,
                f"Space: {c:.2f}",
                (400, img_h - 100),
                cv2.FONT_HERSHEY_COMPLEX,
                1,
                (255, 0, 0),
                2,
                cv2.LINE_AA,
            )
            res = (
                pos(
                    meshPoints[R_R],
                    meshPoints[R_L],
                    meshPoints[R_UP],
                    meshPoints[R_DOWN],
                )
                + pos(
                    meshPoints[L_R],
                    meshPoints[L_L],
                    meshPoints[L_UP],
                    meshPoints[L_DOWN],
                )
            ) / 2
            cv2.putText(
                img,
                f"{res:.2f}",
                (150, 50),
                cv2.FONT_HERSHEY_COMPLEX,
                1,
                (255, 0, 0),
                2,
                cv2.LINE_AA,
            )
            if res >= b:
                flag = False
                k = 0
            elif res >= c:
                if flag:
                    if k == counter:
                        flag = False
                        cv2.putText(
                            img,
                            "Cheater",
                            (0, 500),
                            cv2.FONT_HERSHEY_COMPLEX,
                            5,
                            (0, 0, 255),
                            3,
                            cv2.LINE_AA,
                        )
                        print("CHEATER")
                    else:
                        k += 1
                else:
                    flag = True
                    k = 1
            else:
                k = 0
                flag = False
                print("BLINK")
                cv2.putText(
                    img,
                    "Blink",
                    (0, 500),
                    cv2.FONT_HERSHEY_COMPLEX,
                    3,
                    (0, 255, 0),
                    3,
                    cv2.LINE_AA,
                )
        else:
            if f1 == 1:
                cv2.putText(
                    img,
                    "look at the last row of keys, press k to start and stop",
                    (0, 50),
                    cv2.FONT_HERSHEY_COMPLEX,
                    1,
                    (255, 0, 0),
                    2,
                    cv2.LINE_AA,
                )
                ls = (
                    pos(
                        meshPoints[R_R],
                        meshPoints[R_L],
                        meshPoints[R_UP],
                        meshPoints[R_DOWN],
                    )
                    + pos(
                        meshPoints[L_R],
                        meshPoints[L_L],
                        meshPoints[L_UP],
                        meshPoints[L_DOWN],
                    )
                ) / 2
                cv2.putText(
                    img,
                    f"{ls:.2f}",
                    (0, img_h),
                    cv2.FONT_HERSHEY_COMPLEX,
                    1,
                    (0, 0, 255),
                    2,
                    cv2.LINE_AA,
                )
                if b == -1:
                    b = ls
                b = min(b, ls)
            elif f1 == 2:
                cv2.putText(
                    img,
                    "press k to stop",
                    (0, 50),
                    cv2.FONT_HERSHEY_COMPLEX,
                    1,
                    (255, 0, 0),
                    2,
                    cv2.LINE_AA,
                )
                ls = (
                    pos(
                        meshPoints[R_R],
                        meshPoints[R_L],
                        meshPoints[R_UP],
                        meshPoints[R_DOWN],
                    )
                    + pos(
                        meshPoints[L_R],
                        meshPoints[L_L],
                        meshPoints[L_UP],
                        meshPoints[L_DOWN],
                    )
                ) / 2
                cv2.putText(
                    img,
                    f"{ls:.2f}",
                    (0, img_h),
                    cv2.FONT_HERSHEY_COMPLEX,
                    1,
                    (0, 0, 255),
                    2,
                    cv2.LINE_AA,
                )
                if c == -1:
                    c = ls
                c = min(c, ls)
            else:
                cv2.putText(
                    img,
                    "Press K to start",
                    (0, 50),
                    cv2.FONT_HERSHEY_COMPLEX,
                    1,
                    (255, 0, 0),
                    2,
                    cv2.LINE_AA,
                )

        cv2.imshow("Video", img)
        pressedKey = cv2.waitKey(1) & 0xFF
        if pressedKey == ord("k"):
            if f1 < 2:
                f1 += 1
            else:
                f2 = True
        elif pressedKey == ord("s"):
            f2 = False
            f1 = 0
            b = c = -1
            k = 0

        elif pressedKey == ord("q"):
            cv2.destroyAllWindows()
