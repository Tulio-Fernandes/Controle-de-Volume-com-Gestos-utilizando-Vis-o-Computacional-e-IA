import cv2
import numpy as np
import mediapipe as mp
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
import math
import time

# Iniciar o mediapipe
mpHands = mp.solutions.hands
hands = mpHands.Hands()
mpDraw = mp.solutions.drawing_utils

# Inicializar pycaw
device = AudioUtilities.GetSpeakers()
interface = device.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))

volRange = volume.GetVolumeRange()
minVol = volRange[0]
maxVol = volRange[1]

# Estado de mute
is_muted = volume.GetMute()

# Timer para cooldown de mute
last_mute_time = 0
cooldown = 1  # segundos

# Webcam
cap = cv2.VideoCapture(0)

while True:
    success, img = cap.read()
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(imgRGB)

    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks:
            lmList = []
            for id, lm in enumerate(handLms.landmark):
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                lmList.append([cx, cy])

            if len(lmList) >= 21:
                # Coordenadas do dedo indicador e polegar
                x1, y1 = lmList[4]
                x2, y2 = lmList[8]

                # Desenhar círculos e linhas para volume
                cv2.circle(img, (x1, y1), 10, (255, 0, 0), cv2.FILLED)
                cv2.circle(img, (x2, y2), 10, (255, 0, 0), cv2.FILLED)
                cv2.line(img, (x1, y1), (x2, y2), (255, 0, 0), 2)

                # Calcular distância para controle de volume
                length = math.hypot(x2 - x1, y2 - y1)
                vol = np.interp(length, [20, 150], [minVol, maxVol])
                volume.SetMasterVolumeLevel(vol, None)
                vol_percent = int(np.interp(length, [20, 150], [0, 100]))

                # Mostrar volume
                cv2.putText(img, f'Volume: {vol_percent}%', (10, 50),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

                # Detectar mão aberta ou fechada
                fingers = []

                # Polegar (opcional: pode adaptar para mão esquerda/direita)
                if lmList[4][0] < lmList[3][0]:
                    fingers.append(1)
                else:
                    fingers.append(0)

                # Outros dedos (índice, médio, anelar, mindinho)
                for tipId, pipId in zip([8, 12, 16, 20], [6, 10, 14, 18]):
                    if lmList[tipId][1] < lmList[pipId][1]:
                        fingers.append(1)
                    else:
                        fingers.append(0)

                totalFingers = fingers.count(1)

                # Mute se mão estiver fechada (0 dedos levantados), desmute se aberta (5 dedos)
                current_time = time.time()
                if totalFingers == 0 and not is_muted and current_time - last_mute_time > cooldown:
                    volume.SetMute(1, None)
                    is_muted = True
                    last_mute_time = current_time
                elif totalFingers == 5 and is_muted and current_time - last_mute_time > cooldown:
                    volume.SetMute(0, None)
                    is_muted = False
                    last_mute_time = current_time

                # Exibir estado de mute
                mute_text = "MUTADO" if is_muted else "SOM ATIVO"
                cv2.putText(img, mute_text, (10, 90),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7,
                            (0, 0, 255) if is_muted else (0, 255, 0), 2)

            mpDraw.draw_landmarks(img, handLms, mpHands.HAND_CONNECTIONS)

    cv2.imshow("Controle de Volume com a Mão", img)
    if cv2.waitKey(1) & 0xFF == 27:  # Tecla ESC para sair
        break

cap.release()
cv2.destroyAllWindows()
