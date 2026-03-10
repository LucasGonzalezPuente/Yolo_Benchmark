import cv2
import os
import numpy as np
import time
from ultralytics import YOLO


DEVICE = 'cuda' # o 'cpu'

model = YOLO('yolov8s-pose.pt')

cap = cv2.VideoCapture(0)
modo_camara = False

print(f"--- SISTEMA INICIADO EN: {DEVICE.upper()} ---")
print("Controles: [V] Cámara | [C] Cambiar a CPU | [G] Cambiar a GPU | [Q] Salir")

while True:
    t_inicio_ciclo = time.time() 

    if modo_camara:
        
        t0 = time.time()
        ret, frame = cap.read()
        t_captura = (time.time() - t0) * 1000 # ms
        
        if not ret: break
        
        
        t0 = time.time()
        results = model.predict(frame, conf=0.5, device=DEVICE, verbose=False)
        t_inferencia = (time.time() - t0) * 1000
        
        
        t0 = time.time()
        annotated_frame = results[0].plot()
        t_dibujado = (time.time() - t0) * 1000
        
        
        t_total_ciclo = time.time() - t_inicio_ciclo
        fps = 1 / t_total_ciclo if t_total_ciclo > 0 else 0

        
        cv2.putText(annotated_frame, f"FPS: {fps:.1f} | Dev: {DEVICE}", (20, 40), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        
        print(f"[{DEVICE}] Cap: {t_captura:.1f}ms | Inf: {t_inferencia:.1f}ms | Draw: {t_dibujado:.1f}ms", end='\r')
        
        cv2.imshow('Benchmark YOLO Pose', annotated_frame)
    else:
        img_standby = np.zeros((480, 640, 3), np.uint8)
        cv2.putText(img_standby, f"MODO ESPERA ({DEVICE}) - Pulsa 'V'", (150, 240), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 1)
        cv2.imshow('Benchmark YOLO Pose', img_standby)

    key = cv2.waitKey(1) & 0xFF
    if key == ord('v'):
        modo_camara = not modo_camara
    elif key == ord('c'):
        DEVICE = 'cpu'
        print(f"\nCambiando a CPU...")
    elif key == ord('g'):
        DEVICE = 'cuda'
        print(f"\nCambiando a GPU...")
    elif key == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()