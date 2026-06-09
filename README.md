<div align="center">
  <h1>🌱 SMART PUMP ECO-SYSTEM</h1>
  <p><b>Hệ thống giám sát và điều khiển máy bơm nước thông minh qua cử chỉ tay ứng dụng Trí tuệ nhân tạo (AI Computer Vision) và IoT Web Dashboard</b></p>
</div>

## 📌 Tổng quan dự án
* **Mô tả ngắn:** Hệ thống nhúng thông minh kết hợp mạng học sâu cho phép nhận diện hành vi, cử chỉ bàn tay của con người thông qua camera thời gian thực để đóng ngắt rơ-le điều khiển máy bơm nước và điều khiển cơ cấu van xả (Servo) từ xa mà không cần tiếp xúc vật lý.
* **Môi trường thử nghiệm:** Phòng thí nghiệm, hệ thống nhúng cục bộ (Localhost Server).
* **Công nghệ cốt lõi:**
    * **AI & Computer Vision:** Google MediaPipe Hands (Nhận diện 21 điểm landmark cấu trúc xương bàn tay), OpenCV.
    * **Mạch điều khiển trung tâm:** Arduino UNO R3 (Vi điều khiển ATmega328P).
    * **Giao diện (Web Dashboard):** Flask Framework (Backend Python), HTML5, CSS3 (Thiết kế High-End Tech Dark Mode).
    * **Giao tiếp hệ thống:** Thư viện PySerial qua giao thức UART (USB Serial) tốc độ 9600 bps.

<table align="center" width="100%" style="border-collapse: collapse; border: none;">
  <tr style="border: none;">
    <td align="center" width="33.33%" style="border: none; padding: 10px;">
      <img src="https://img.shields.io/badge/Arduino-00979D?style=for-the-badge&logo=Arduino&logoColor=white" alt="Arduino">
    </td>
    <td align="center" width="33.33%" style="border: none; padding: 10px;">
      <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python">
    </td>
    <td align="center" width="33.33%" style="border: none; padding: 10px;">
      <img src="https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white" alt="Flask">
    </td>
  </tr>
</table>

## ✨ Tính năng nổi bật
* ⚡ **Xử lý thị giác thời gian thực (Real-time tracking):** Trích xuất ma trận tọa độ không gian 3 chiều của bàn tay với độ trễ xử lý ảnh cực thấp (~15ms).
* 🔒 **Điều khiển không tiếp xúc (Contactless Control):** Tự động dịch mã số lượng ngón tay mở để kích hoạt hệ thống, triệt tiêu hoàn toàn nguy cơ mất an toàn về điện trong môi trường ẩm ướt.
* 📂 **Bộ lọc trạng thái chống lặp dữ liệu:** Thuật toán chỉ gửi tín hiệu xuống phần cứng duy nhất một lần khi có sự chuyển dịch cử chỉ, ngăn chặn hiện tượng thắt nút cổ chai và spam bộ đệm Serial.
* 🔍 **Dashboard tích hợp đa luồng (Multi-threading):** Truyền tải trực tiếp luồng video camera đã xử lý ma trận AI lên giao diện web mà không gây giật lag hệ thống.

## 🔄 Quy trình hoạt động

<table width="100%" style="border-collapse: collapse; border: none;">
  <tr style="border: none;">
    <td width="50%" valign="top" style="border: none; padding: 15px; background: #0f172a; color: #f8fafc; border-radius: 8px;">
      <h3>1. Thu thập hình ảnh (AI Vision)</h3>
      <p>Camera thu thập chuỗi khung hình thô &rarr; Module MediaPipe quét phân tích và định vị vị trí các khớp ngón tay.</p>
    </td>
    <td width="50%" valign="top" style="border: none; padding: 15px; background: #0f172a; color: #f8fafc; border-radius: 8px;">
      <h3>2. Đóng gói lệnh & Chuyển tiếp</h3>
      <p>Thuật toán đếm ngón tay xòe xác định trạng thái logic &rarr; PySerial đóng gói lệnh thành mã byte truyền xuống Arduino.</p>
    </td>
  </tr>
  <tr style="border: none;">
    <td width="50%" valign="top" style="border: none; padding: 15px; background: #0f172a; color: #f8fafc; border-radius: 8px;">
      <h3>3. Đồng bộ hóa Dashboard</h3>
      <p>Server Flask kết xuất hình ảnh camera kèm dòng trạng thái đồ họa (BẬT/TẮT) đồng thời lên trình duyệt web (Cổng 5000).</p>
    </td>
    <td width="50%" valign="top" style="border: none; padding: 15px; background: #0f172a; color: #f8fafc; border-radius: 8px;">
      <h3>4. Thực thi thiết bị chấp hành</h3>
      <p>Arduino giải mã byte lệnh &rarr; Kích đóng/ngắt mạch cách ly Relay và điều khiển Servo xoay gạt chính xác góc 0° - 180°.</p>
    </td>
  </tr>
</table>

## 📐 Kiến trúc đấu nối phần cứng
Để đảm bảo hệ thống vận hành ổn định, không bị sụt áp nguồn do dòng khởi động của động cơ bước, sơ đồ mạch được thiết kế phân tách dòng động lực qua thanh bus bar của Breadboard:
* **Chân IN (Relay)** &rarr; Kết nối chân **Digital Pin 8** trên Arduino.
* **Chân Tín hiệu (Servo)** &rarr; Kết nối chân cấp xung **Digital Pin 9 (PWM)** trên Arduino.
* **Chân Nguồn tải Đỏ (Servo)** &rarr; Kết nối qua cổng **NO (Normally Open)** của Relay để đóng ngắt nguồn cấp.
* **Hệ thống GND** &rarr; Tất cả các chân đất (Arduino, Relay, Servo) được đấu nối chung hàng mass trên Breadboard.

## 🏆 Thành tựu đạt được
* ✅ **Đáp ứng thời gian thực vượt trội:** Tổng độ trễ truyền tin từ lúc nhận diện cử chỉ đến khi thiết bị vật lý hoàn thành hành trình chỉ xấp xỉ **120ms**.
* ✅ **Giải quyết bài toán sụt áp:** Ứng dụng thành công mạch chia nguồn song song giúp Servo SG90 hoạt động ổn định mà không làm reset vi điều khiển.
* ✅ **Giao diện UI/UX tối ưu:** Thiết kế trang Dashboard phong cách Tech Dark Mode tối giản, hiển thị luồng streaming camera ổn định ở mức **28-30 FPS**.

---
*Đồ án nghiên cứu Hệ thống nhúng tương tác thông minh ứng dụng Thị giác máy tính © 2026*
