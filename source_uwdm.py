import cv2
import mediapipe as mp
import face_recognition as fc  
import os 
import numpy as np
from datetime import datetime
import csv
import time
import serial
from ultralytics import YOLO

last_seen={}
arduino=serial.Serial("/dev/tty.usbserial-0001",9600)
model=YOLO("yolov11_custom.pt")

log_face=open("recognized_face.csv", mode="a", newline= "")
csv_writer=csv.writer(log_face)
if os.stat("recognized_face.csv").st_size == 0:
    csv_writer.writerow(["Timestamp","Name"])

# Initialize Mediapipe
mp_face_detection = mp.solutions.face_detection
mp_drawing = mp.solutions.drawing_utils
is_recognized = False

#Open webcam    
cap = cv2.VideoCapture(0,cv2.CAP_AVFOUNDATION)

#Get all the sample photos for the comparison
folder_path="/Users/anandkrishna/Desktop/Projects & Practice/image/APIweather/Practice.py/attachments"
image_file=[]
for i in os.listdir(folder_path):
    if i.lower().endswith(('.png', '.jpg', '.jpeg')):
        image_file.append(i)
    
#Gets the encoding of all the sample photos
known_images=[]
known_encodings=[]
known_names=[]
for i in image_file:
    image_path = os.path.join(folder_path, i)
    known_image = fc.load_image_file(image_path)
    known_encoding=fc.face_encodings(known_image)
    if len(known_encoding)>0:
        known_encodings.append(known_encoding[0])
        name=os.path.splitext(i)[0]
        name="".join([char for char in name if not char.isdigit()])
        known_names.append(name.lower())

# Function to detect bowl for 10 seconds
def detect_bowl_for_duration(duration=10):
    """
    Detects bowl for specified duration and returns True if bowl found
    Only detects bowls in lower portion of frame (sink area)
    """
    start_time = time.time()
    bowl_detected = False
    
    print(f"Starting bowl detection for {duration} seconds...")
    
    while time.time() - start_time < duration:
        ret, frame = cap.read()
        if not ret:
            continue
        
        frame_height, frame_width = frame.shape[:2]
        
        # Only look at bottom 60% of frame (where sink should be)
        roi_frame = frame[int(frame_height * 0.4):, :]  # Bottom 60% of frame
            
        # Run prediction without showing window
        results = model.predict(roi_frame, show=False, save=False, conf=0.8, save_crop=False)
        
        # Process results
        for result in results:
            for box in result.boxes:
                class_id = int(box.cls[0])
                class_name = model.names[class_id]
                
                if class_name.lower() == "bowl":
                    print(f"Bowl detected in sink area!")
                    bowl_detected = True
                    
                    # Optional: Show the detection visually for debugging
                    annotated_frame = result.plot()
                    # Add ROI back to full frame for display
                    display_frame = frame.copy()
                    display_frame[int(frame_height * 0.4):, :] = annotated_frame
                    cv2.rectangle(display_frame, (0, int(frame_height * 0.4)), (frame_width, frame_height), (0, 255, 0), 2)
                    cv2.putText(display_frame, "SINK DETECTION ZONE", (10, int(frame_height * 0.4) - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
                    cv2.imshow('Bowl Detection', display_frame)
                    cv2.waitKey(1)
                    
                    # Exit immediately when bowl found
                    break
        
        # Exit immediately if bowl found
        if bowl_detected:
            break
            
        # Small delay to prevent excessive CPU usage
        time.sleep(0.1)
    
    # Close any detection windows
    cv2.destroyWindow('Bowl Detection')
    print(f"Bowl detection finished. Bowl found: {bowl_detected}")
    return bowl_detected

# Create FaceDetection instance
with mp_face_detection.FaceDetection(min_detection_confidence=0.5) as face_detection:
    while cap.isOpened():
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

        ret, frame = cap.read()
        if not ret:
            continue

        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = face_detection.process(frame_rgb)
        face_locations=fc.face_locations(frame_rgb)
        face_encodings=fc.face_encodings(frame_rgb, face_locations)
        frame_height, frame_width, _ = frame.shape
        
        for (top,right,bottom, left), face_encoding in zip(face_locations,face_encodings):
            distances=fc.face_distance(known_encodings, face_encoding)
            name="Unknown"
            color=(0,0,255)
            
            if len(distances)>0:
                min_distance_index=np.argmin(distances) 
                if distances[min_distance_index] < 0.6:
                    name = known_names[min_distance_index]
                    color=(0,255,0)
                    current_time = time.time()
                    last_time = last_seen.get(name, 0)
                   
                    if current_time - last_time > 30:
                        last_seen[name] = current_time
                        
                        print(f"Face recognized: {name}. Starting bowl detection sequence...")
                        
                        # Pan camera to sink (180 degrees)
                        print("Panning camera to sink...")
                        angle = 180
                        arduino.write(f"{angle}\n".encode())
                        arduino.flush()  # Make sure command is sent
                        time.sleep(4)  # Wait longer for camera to pan
                        
                        # Detect bowl for 10 seconds
                        bowl_found = detect_bowl_for_duration(10)
                        
                        if bowl_found:
                            print(f"Bowl detected! {name} left a bowl unwashed.")
                        
                        else:
                            print(f"No bowl detected. {name} is all good!")
                        
                        # Pan camera back to original position (0 degrees)
                        print("Panning camera back to face detection position...")
                        angle = 0
                        arduino.write(f"{angle}\n".encode())
                        arduino.flush()  # Make sure command is sent
                        time.sleep(4)  # Wait longer for camera to return
                        
                        print("Ready for next person...")

           
            cv2.rectangle(frame,(left,top),(right,bottom), color,2)
            cv2.putText(frame, name,(left,top-10), cv2.FONT_HERSHEY_SIMPLEX,1,color,2)
            
            # Log the detection
            timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
            folder_path_save = f"/Users/anandkrishna/Desktop/Model/Detected_Faces"
            file_name=f"{timestamp}_{name}.jpg"
            save_path = os.path.join(folder_path_save, file_name)
            cv2.imwrite(save_path, frame)
            csv_writer.writerow([timestamp, name])
            
        # Show face detection feed
        cv2.imshow('Face Detection', frame)

        if cv2.waitKey(1) == ord('q'):
            break

cap.release()
cv2.destroyAllWindows()
log_face.close()