import cv2 
import numpy as np
import mediapipe as mp
import serial
import time
import requests
import sys
import ipaddress



# Задаем адрес ESP32 в режиме точки доступа
ipEsp = input("Write ip esp32,not space\n")

def is_valid_ip(ip):
    try:
        ipaddress.ip_address(ip)
        return True
    except ValueError:
        print('Неправильный ip')
        sys.exit(1)
        
is_valid_ip (ipEsp)   

url = 'http://'+ipEsp+'/data'  # Замените IP-адресом вашего ESP32




data={'gestures':''}


try:
    response = requests.post(url, data=data)
    # Обрабатываем ответ от сервера
except requests.exceptions.ConnectionError as e:
    print('Ошибка подключения:', e)
    sys.exit(1)

    
if response.status_code == 200:
    print("Данные успешно отправлены на ESP32")
else:
    print("Ошибка при отправке данных на ESP32")
    sys.exit(1)



# 10.10.16.41

# arduino=serial.Serial('COM8', 115200)
#time.sleep(2)

cap = cv2.VideoCapture(0)

hands = mp.solutions.hands.Hands(static_image_mode=False,
                                 max_num_hands=1,
                                 min_tracking_confidence = 0.5,
                                 min_detection_confidence= 0.5)

if not cap.isOpened():
    print("Cannot open camera")
    exit()

mpDraw = mp.solutions.drawing_utils


# def writetoSerial(gestures):
#     if(gestures):
#         arduino.write(gestures.encode())
#         print(gestures)  



prev_finger_x = 0
prev_finger_z = 0


prev_finger_x_8 = 0
prev_finger_x_4 = 0

def Gestures(keypoints,gestures):
    global prev_finger_x
    global prev_finger_z
    global prev_finger_x_8
    global prev_finger_x_4



    if(keypoints):
        finger_x_8 = keypoints[8]['x']
        finger_x_4 = keypoints[4]['x']
        if (
        keypoints[4]['y'] < keypoints[3]['y']
        and keypoints[3]['y'] < keypoints[2]['y']
        and keypoints[8]['y'] < keypoints[7]['y']
        and keypoints[7]['y'] < keypoints[6]['y']
        and keypoints[12]['y'] < keypoints[11]['y']
        and keypoints[11]['y'] < keypoints[10]['y']
        and keypoints[16]['y'] < keypoints[15]['y']
        and keypoints[15]['y'] < keypoints[14]['y']
        and keypoints[20]['y'] < keypoints[19]['y']
        and keypoints[19]['y'] < keypoints[18]['y']
        and keypoints[0]['y'] > keypoints[1]['y']
        and keypoints[1]['y'] > keypoints[2]['y']
        and abs( keypoints[0]['x']  - keypoints[4]['x'])>abs( keypoints[12]['x']  - keypoints[0]['x'])
        and gestures != 'gestures Hand'
        ):
            gestures = 'gestures Hand'
        elif (
        keypoints[4]['y'] < keypoints[3]['y']
        and keypoints[3]['y'] < keypoints[2]['y']
        and keypoints[2]['y'] < keypoints[1]['y']
        and keypoints[5]['y'] < keypoints[9]['y']
        and keypoints[9]['y'] < keypoints[13]['y']
        and keypoints[8]['y'] < keypoints[12]['y']
        and keypoints[12]['y'] < keypoints[16]['y']
        and keypoints[16]['y'] < keypoints[20]['y']
        and keypoints[13]['y'] < keypoints[17]['y']
        and keypoints[8]['x'] > keypoints[6]['x']
        and keypoints[12]['x'] > keypoints[10]['x']
        and keypoints[16]['x'] > keypoints[14]['x'] 
        and keypoints[20]['x'] > keypoints[18]['x']
        and keypoints[8]['x']  < keypoints[0]['x']
        and keypoints[12]['x']  < keypoints[0]['x']
        and keypoints[16]['x']  < keypoints[0]['x']
        and keypoints[20]['x']  < keypoints[0]['x']
        and keypoints[0]['y']  < keypoints[20]['y']
        and gestures != 'gestures Up'
        ):
            gestures = 'gestures Up'
        elif (
            keypoints[8]['y'] < keypoints[7]['y']
            and keypoints[7]['y'] < keypoints[6]['y']
            and keypoints[6]['y'] < keypoints[5]['y']
            and keypoints[12]['y'] < keypoints[11]['y']
            and keypoints[11]['y'] < keypoints[10]['y']
            and keypoints[10]['y'] < keypoints[9]['y']
            and keypoints[4]['y'] > keypoints[6]['y']
            and abs(keypoints[4]['x'] - keypoints[10]['x']) < abs(keypoints[4]['x'] - keypoints[6]['x'])
            and keypoints[16]['y'] > keypoints[13]['y']
            and keypoints[20]['y'] > keypoints[17]['y']
            and keypoints[2]['x'] > keypoints[4]['x']
            and keypoints[4]['y'] > keypoints[8]['y']
            and gestures != 'gestures Victory'
        ):
            gestures = 'gestures Victory'
        elif (
            keypoints[20]['x'] > keypoints[16]['x']
            and keypoints[16]['x'] > keypoints[12]['x']
            and keypoints[20]['x'] > keypoints[16]['x']
            and keypoints[8]['y'] > keypoints[6]['y']
            and keypoints[0]['y'] > keypoints[1]['y']
            and keypoints[12]['y'] < keypoints[19]['y']
            and keypoints[16]['y'] < keypoints[13]['y']
            and keypoints[20]['y'] < keypoints[17]['y']
            and keypoints[12]['y'] < keypoints[11]['y']
            and keypoints[11]['y'] < keypoints[10]['y']
            and keypoints[16]['y'] < keypoints[15]['y']
            and keypoints[15]['y'] < keypoints[14]['y']
            and keypoints[20]['y'] < keypoints[19]['y']
            and keypoints[19]['y'] < keypoints[18]['y']
            and keypoints[2]['y'] > keypoints[4]['y']
            and gestures != 'gestures OK'
        ):
            gestures = 'gestures OK'
        elif (
            keypoints[4]['y'] < keypoints[3]['y']
            and keypoints[3]['y'] < keypoints[2]['y']
            and keypoints[8]['y'] < keypoints[7]['y']
            and keypoints[7]['y'] < keypoints[6]['y']
            and keypoints[5]['y'] > keypoints[6]['y']
            and keypoints[12]['y'] > keypoints[11]['y']
            and keypoints[12]['y'] > keypoints[9]['y']
            and keypoints[16]['y'] > keypoints[15]['y']
            and keypoints[16]['y'] > keypoints[13]['y']
            and keypoints[20]['y'] > keypoints[19]['y']
            and keypoints[20]['y'] > keypoints[18]['y']
            and (abs(finger_x_8 - finger_x_4)<0.08
            or abs(finger_x_8 - finger_x_4)>0.12)
        ):
            
            #if(abs(finger_x_8 - finger_x_4)<0.01):
                     
            # elif(abs(finger_x_8 - finger_x_4)>0.05):
            
            if(gestures !="Palzs right" and gestures !="Palzs left"):
                if finger_x_8 < prev_finger_x_8  and abs(finger_x_8 - prev_finger_x_8)>0.02 and finger_x_4 > prev_finger_x_4 and abs(finger_x_4 - prev_finger_x_4)>0.015 :
                    gestures = "Palzs left"   
                
                if finger_x_8 > prev_finger_x_8 and abs(finger_x_8 - prev_finger_x_8)>0.02 and finger_x_4 < prev_finger_x_4 and abs(finger_x_4 - prev_finger_x_4)>0.015:
                    gestures = "Palzs right"   
        
            prev_finger_x_8 = finger_x_8
            prev_finger_x_4 = finger_x_4

            
        # elif (
        #     keypoints[8]['y'] < keypoints[7]['y']
        #     and keypoints[12]['y'] > keypoints[9]['y']
        #     and keypoints[16]['y'] > keypoints[13]['y']
        #     and keypoints[20]['y'] > keypoints[17]['y']
        #     and keypoints[2]['x'] > keypoints[4]['x']
        #     and keypoints[4]['y'] > keypoints[8]['y']
        #     and gestures != "right"
        #     and gestures != "left"
        # ):
        #     finger_x = keypoints[8]['x']  # Координата x указательного пальца
        #     finger_z = keypoints[8]['z']  # Координата z указательного пальца

        #     if prev_finger_z - finger_z>0.01:            
        #         if finger_x < prev_finger_x and abs(finger_x - prev_finger_x)>0.03:
        #                 gestures = "right"
        #         if finger_x > prev_finger_x and abs(finger_x - prev_finger_x)>0.02:
        #                 gestures = "left"

        #     prev_finger_x = finger_x
        #     prev_finger_z = finger_z
            
    elif gestures:
        gestures = ''

    return gestures


gestures=''
bufferGetures = ''


while True:
    ret, frame = cap.read()
    RGB_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(RGB_image)
    keypoints = []

    if result.multi_hand_landmarks:
        for id,hand_landmarks in enumerate(result.multi_hand_landmarks[0].landmark):
            keypoints.append({
                'id':id,
                'x': hand_landmarks.x,
                'y': hand_landmarks.y,
                'z': hand_landmarks.z
            })
            h,w,_ = frame.shape
            cx,cy = int(hand_landmarks.x * w),int(hand_landmarks.y*h)
            cv2.circle(RGB_image,(cx,cy),3,(255,0,255))
            mpDraw.draw_landmarks(RGB_image,result.multi_hand_landmarks[0],mp.solutions.hands.HAND_CONNECTIONS)


    gestures = Gestures(keypoints,gestures)
    
    if(gestures != bufferGetures):
        bufferGetures = gestures
        # writetoSerial(bufferGetures)
        data={'gestures':gestures}
        response = requests.post(url, data=data)
        if response.status_code == 200:
            print("Данные успешно отправлены на ESP32")
        else:
            print("Ошибка при отправке данных на ESP32")

    BGR_image = cv2.cvtColor(RGB_image, cv2.COLOR_RGB2BGR)    
    cv2.imshow("Video",  BGR_image)
    if cv2.waitKey(13) & 0xFF == ord('q'):
        break


cap.release()
cv2.destroyAllWindows()
