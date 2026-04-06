# send_dummy_image.py
import socketio
import cv2
import numpy as np
import base64
import time
import threading

# Socket.IO 클라이언트 생성
sio = socketio.Client()

@sio.event
def connect():
    print("✅ Node.js 서버에 연결 성공!")

@sio.event
def disconnect():
    print("❌ 연결이 끊어졌습니다.")

# 더미 이미지 생성 (YOLO 결과처럼 보이게)
def create_dummy_image():
    # 빈 이미지 만들기
    img = np.zeros((480, 640, 3), dtype=np.uint8)
    
    # 배경에 텍스트 그리기 (YOLO 느낌)
    cv2.putText(img, "YOLO Detection Test", (80, 150), 
                cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 255, 0), 3)
    cv2.putText(img, "Person detected", (120, 250), 
                cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 0, 255), 2)
    cv2.putText(img, "Confidence: 0.92", (120, 300), 
                cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 255, 0), 2)
    
    # 빨간 사각형 (바운딩박스 느낌)
    cv2.rectangle(img, (200, 180), (450, 380), (0, 0, 255), 4)
    
    # JPG로 인코딩 → base64
    _, buffer = cv2.imencode('.jpg', img)
    return base64.b64encode(buffer).decode('utf-8')

# 이미지 전송 루프 (별도 스레드)
def image_sender():
    while True:
        base64_img = create_dummy_image()
        sio.emit('image', {
            'image': base64_img,
            'info': 'Dummy YOLO result from Python'
        })
        print(f"📤 더미 이미지 전송 완료 ({time.strftime('%H:%M:%S')})")
        time.sleep(2)  # 2초마다 전송 (테스트용)

if __name__ == "__main__":
    try:
        sio.connect('http://localhost:3000')
        
        # 이미지 전송 스레드 시작
        threading.Thread(target=image_sender, daemon=True).start()
        
        # 프로그램 유지
        sio.wait()
        
    except Exception as e:
        print("❌ 연결 실패:", e)
