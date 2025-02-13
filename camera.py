import cv2
import face_recognition

camera_in = cv2.VideoCapture(0)  # Kirish kamerasini ulash
camera_out = cv2.VideoCapture(1) # Chiqish kamerasini ulash

def process_frame(video_capture):
    ret, frame = video_capture.read()
    if not ret:
        return None
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    face_locations = face_recognition.face_locations(rgb_frame)
    return face_locations

while True:
    faces_in = process_frame(camera_in)
    faces_out = process_frame(camera_out)
    print(f"Kirish: {len(faces_in)} ta yuz | Chiqish: {len(faces_out)} ta yuz")

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

camera_in.release()
camera_out.release()
cv2.destroyAllWindows()
