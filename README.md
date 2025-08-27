Unwashed Dishes Monitor
A home automation system that detects unwashed dishes in the sink, identifies who left them, and sends notifications to get them cleaned.
Overview
This project combines computer vision with facial recognition to solve a common household problem. The system monitors the kitchen sink, detects when dishes are left unwashed, identifies the person responsible using facial recognition, and sends them a notification.

<img width="824" height="624" alt="uwdm_drawing" src="https://github.com/user-attachments/assets/25d5b4f1-35dd-4a27-a11e-cb8fb639b740" />


![2025-08-25_19-47-07_anand](https://github.com/user-attachments/assets/54eb2bb6-6a23-4ddb-a3a0-ceef2bd9e92a)




<img width="522" height="263" alt="uwdm_case" src="https://github.com/user-attachments/assets/3d129565-2592-4850-8df5-a601915abb57" />

How it Works

Motion sensor detects activity near the sink
Camera captures images when motion is detected
Computer vision identifies if dishes are present
Facial recognition identifies the last person in the area
System sends notification to that person
Monitors until dishes are cleaned

Hardware

Raspberry Pi 4B
Camera module for image capture
Motion sensors
Custom 3D-printed case
Wi-Fi connectivity for notifications

Software

Python for the main application
OpenCV for computer vision and dish detection
Face recognition libraries for person identification
Web interface for configuration and monitoring

Features

Real-time dish detection
Facial recognition to identify household members
Email and mobile notifications
Web dashboard for monitoring
Custom hardware enclosure

Technical Details
The system uses computer vision algorithms to detect dishes in the sink area. When dishes are detected, it cross-references with facial recognition data to determine who was last in the kitchen. The custom 3D-printed case houses all components and is designed to blend into a kitchen environment.
