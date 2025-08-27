# Unwashed Dishes Monitor
A home automation system that detects unwashed dishes in the sink, identifies who left them, and sends notifications to get them cleaned.
Overview
This project combines computer vision with facial recognition to solve a common household problem. The system monitors the kitchen sink, detects when dishes are left unwashed, identifies the person responsible using facial recognition, and sends them a notification.

<img width="824" height="624" alt="uwdm_drawing" src="https://github.com/user-attachments/assets/25d5b4f1-35dd-4a27-a11e-cb8fb639b740" />


![2025-08-25_19-47-07_anand](https://github.com/user-attachments/assets/54eb2bb6-6a23-4ddb-a3a0-ceef2bd9e92a)




<img width="522" height="263" alt="uwdm_case" src="https://github.com/user-attachments/assets/3d129565-2592-4850-8df5-a601915abb57" />

# How it Works

The system activates when motion is detected near the sink. A camera captures images which are processed using computer vision to identify if dishes are present. If dishes are found, facial recognition identifies the last person in the area and sends them a notification. The system continues monitoring until the dishes are cleaned.

# Hardware Components

The device runs on a Raspberry Pi 4B with a camera module for image capture and motion sensors for activation. All components are housed in a custom 3D-printed case designed to fit naturally in a kitchen environment. Wi-Fi connectivity enables remote notifications.
Software Stack
The main application is written in Python, using OpenCV for computer vision and dish detection algorithms. Facial recognition libraries handle person identification, while a web interface provides configuration and monitoring capabilities.

# Key Features

The system provides real-time dish detection with facial recognition to identify household members. It sends email and mobile notifications when dishes are detected and includes a web dashboard for system monitoring. The custom hardware enclosure integrates all components seamlessly.

# Technical Implementation

Computer vision algorithms analyze images from the sink area to detect the presence of dishes. When dishes are identified, the system cross-references facial recognition data to determine who was last in the kitchen area. The notification system then targets that specific person with reminders.
