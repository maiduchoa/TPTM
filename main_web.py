from flask import Flask, render_template, Response
import cv2
import mediapipe as mp
import serial
import time

app = Flask(__name__)

# ==========================================
# CẤU HÌNH ARDUINO (Sửa lại đúng cổng COM của bạn)
# ==========================================
PORT_ARDUINO = 'COM3' 
try:
    arduino = serial.Serial(port=PORT_ARDUINO, baudrate=9600, timeout=1)
    time.sleep(2)
    print("Đã kết nối thành công với Arduino!")
except:
    print("Không thể kết nối với Arduino. Chạy chế độ giả lập không mạch.")
    arduino = None

# Khởi tạo MediaPipe
mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils
hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7)

# Khởi tạo Camera
cap = cv2.VideoCapture(0)

def gen_frames():
    trang_thai_truoc = -1
    while True:
        success, frame = cap.read()
        if not success:
            break
        else:
            frame = cv2.flip(frame, 1)
            img_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = hands.process(img_rgb)
            system_status = "TAT"

            if results.multi_hand_landmarks:
                for hand_landmarks in results.multi_hand_landmarks:
                    mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
                    
                    landmarks = hand_landmarks.landmark
                    ngon_tro_up = landmarks[8].y < landmarks[6].y
                    ngon_giua_up = landmarks[12].y < landmarks[10].y
                    ngon_nhan_up = landmarks[16].y < landmarks[14].y
                    ngon_ut_up = landmarks[20].y < landmarks[18].y

                    tong_ngon_xoe = sum([ngon_tro_up, ngon_giua_up, ngon_nhan_up, ngon_ut_up])

                    if tong_ngon_xoe >= 3:
                        system_status = "BAT"
                        if trang_thai_truoc != 1:
                            if arduino: arduino.write(b'1')
                            trang_thai_truoc = 1
                            print("--> Lệnh Web: BẬT")
                    else:
                        system_status = "TAT"
                        if trang_thai_truoc != 0:
                            if arduino: arduino.write(b'0')
                            trang_thai_truoc = 0
                            print("--> Lệnh Web: TẮT")

            # Vẽ chữ trạng thái lên khung hình video để đưa lên web
            mau_sac = (0, 255, 0) if system_status == "BAT" else (0, 0, 255)
            cv2.putText(frame, f"May bom: {system_status}", (10, 50), 
                        cv2.FONT_HERSHEY_SIMPLEX, 1, mau_sac, 2)

            # Nén khung hình thành định dạng JPEG để truyền lên web
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            
            # Trả dữ liệu luồng video liên tục về giao diện web
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

# Route chính để hiển thị trang web
@app.route('/')
def index():
    return render_template('index.html')

# Route để truyền luồng video từ camera vào thẻ <img> trong HTML
@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    # Chạy server web tại địa chỉ cục bộ cổng 5000
    app.run(host='0.0.0.0', port=5000, debug=False)
