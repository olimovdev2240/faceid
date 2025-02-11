import cv2
import face_recognition
import mysql.connector
import datetime
import requests

# 📌 MySQL bazaga ulanish (OpenServer uchun, parolsiz)
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",  # Root parolsiz ishlaydi
    database="faceid"
)
cursor = db.cursor()

# 📌 Telegram bot sozlamalari (Sening tokening)
TELEGRAM_BOT_TOKEN = "8081302753:AAEha2MufUxxU9AXObrhIRSVOY3vRgIX78I"
CHAT_ID = "687511965"  # O'z Telegram ID'ngni qo'y

# 📌 Ro‘yxatga olingan yuzlarni yuklash (test qilish uchun)
known_faces = []
known_names = []

# 🔹 Odamlarning suratlarini yuklash (Fayllarni "ali.jpg", "vali.jpg" nomida saqlagin)
ali_image = face_recognition.load_image_file("ali.jpg")
ali_encoding = face_recognition.face_encodings(ali_image)[0]

vali_image = face_recognition.load_image_file("vali.jpg")
vali_encoding = face_recognition.face_encodings(vali_image)[0]

known_faces.extend([ali_encoding, vali_encoding])
known_names.extend(["Ali Valiyev", "Vali Karimov"])

# 📌 USB Kamera (IP-kamera yo‘q holat uchun)
camera_in = cv2.VideoCapture(0)  # Kompyuterning o‘z kamerasidan foydalanamiz
camera_out = cv2.VideoCapture(0)  # Chiqish uchun ham vaqtincha shu ishlaydi

def process_frame(video_capture, direction):
    ret, frame = video_capture.read()
    if not ret:
        return

    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    face_locations = face_recognition.face_locations(rgb_frame)
    face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

    for face_encoding in face_encodings:
        matches = face_recognition.compare_faces(known_faces, face_encoding)
        name = "Noma’lum"

        if True in matches:
            first_match_index = matches.index(True)
            name = known_names[first_match_index]

            # 📌 MySQL bazaga yozish
            event_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            sql = "INSERT INTO logs (name, direction, time) VALUES (%s, %s, %s)"
            cursor.execute(sql, (name, direction, event_time))
            db.commit()

            # 📌 Telegram botga xabar yuborish
            message = f"✅ {name} {'kirdi' if direction == 'IN' else 'chiqdi'}! 🕒 {event_time}"
            requests.get(f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage?chat_id={CHAT_ID}&text={message}")

        # 📌 Ekranda ismni chiqarish
        cv2.putText(frame, name, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    cv2.imshow(f"Face Control - {direction}", frame)

# 📌 Asosiy sikl - ikki kamerani parallel ishlatish
while True:
    process_frame(camera_in, "IN")   # Kirish kamerasini tekshirish
    process_frame(camera_out, "OUT") # Chiqish kamerasini tekshirish

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

camera_in.release()
camera_out.release()
cv2.destroyAllWindows()
db.close()
