# Compatible with Windows – tested and running successfully.

import os
os.environ["GLOG_minloglevel"]="2"
os.environ["TF_CPP_MIN_LOG_LEVEL"]="3"

import cv2, mediapipe as mp, pyautogui, time, math, numpy as np

cam=0
a=0.35
cdth=0.055
cuth=0.085
cdeb=0.25
sth=50

sw,sh=pyautogui.size()

mph=mp.solutions.hands
mpd=mp.solutions.drawing_utils
hnd=mph.Hands(max_num_hands=1,min_detection_confidence=0.6,min_tracking_confidence=0.5)

mfm=mp.solutions.face_mesh
fms=mfm.FaceMesh(static_image_mode=False,max_num_faces=1,refine_landmarks=False,
                 min_detection_confidence=0.6,min_tracking_confidence=0.5)
oval=mfm.FACEMESH_FACE_OVAL

cap=cv2.VideoCapture(cam)
if not cap.isOpened(): raise SystemExit

ex=ey=None
clk=False
t0=0.0

while True:
    ok,frm=cap.read()
    if not ok: break
    frm=cv2.flip(frm,1)
    h,w=frm.shape[:2]
    rgb=cv2.cvtColor(frm,cv2.COLOR_BGR2RGB)

    r=hnd.process(rgb)
    if r.multi_hand_landmarks:
        lm=r.multi_hand_landmarks[0]
        i=lm.landmark[8]; t=lm.landmark[4]; m=lm.landmark[12]
        mx=int(i.x*sw); my=int(i.y*sh)
        if ex is None: ex,ey=mx,my
        else:
            ex=(1-a)*ex+a*mx
            ey=(1-a)*ey+a*my
        pyautogui.moveTo(int(ex),int(ey),duration=0)
        d=math.hypot(t.x-i.x,t.y-i.y); now=time.time()
        if (not clk) and d<=cdth and (now-t0)>=cdeb:
            pyautogui.click(); clk=True; t0=now
        elif clk and d>=cuth: clk=False
        dy=(m.y-i.y)*h
        if abs(dy)>sth: pyautogui.scroll(-100 if dy>0 else 100)
        mpd.draw_landmarks(frm,lm,mph.HAND_CONNECTIONS)

    fr=fms.process(rgb)
    if fr.multi_face_landmarks:
        fl=fr.multi_face_landmarks[0]
        idx=set()
        for a1,b1 in oval: idx.add(a1); idx.add(b1)
        pts=np.array([[int(fl.landmark[k].x*w),int(fl.landmark[k].y*h)] for k in idx],dtype=np.int32)
        if len(pts)>=8:
            xmin,xmax=pts[:,0].min(),pts[:,0].max()
            ymin,ymax=pts[:,1].min(),pts[:,1].max()
            fh=ymax-ymin
            off=int(0.08*fh)

            L=pts[pts[:,0].argmin()]
            R=pts[pts[:,0].argmax()]
            T=pts[pts[:,1].argmin()]
            B=pts[pts[:,1].argmax()]
            TL=pts[(pts[:,0]+pts[:,1]).argmin()]
            TR=pts[(pts[:,1]-pts[:,0]).argmin()]
            BL=pts[(pts[:,0]-pts[:,1]).argmin()]
            BR=pts[(pts[:,0]+pts[:,1]).argmax()]

            for p in (T,TL,TR):
                p[1]=max(0,p[1]-off)

            for p in (tuple(L),tuple(R),tuple(T),tuple(B),tuple(TL),tuple(TR),tuple(BL),tuple(BR)):
                cv2.circle(frm,p,12,(0,255,255),-1)

            poly=np.array([T,TR,R,BR,B,BL,L,TL],dtype=np.int32).reshape((-1,1,2))
            cv2.polylines(frm,[poly],True,(0,255,255),2)

    cv2.imshow("H",frm)
    if cv2.waitKey(1)&0xFF==ord('q'): break

cap.release(); cv2.destroyAllWindows()

