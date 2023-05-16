# Final Year Project codes
A Machine Vision (MV) pipeline that automates feeding of fishes by detecting, tracking and scheduling feeding interval. 

It uses:
1. MotionEye to stream footages from camera connected to Raspberry Pi
- MotionEye github page: https://github.com/motioneye-project/motioneye/tree/dev
2. Use SSH to toggle feeding 
3. YOLOv8 to detect fishes, 
4. Bot-SORT to track them, 
- YOLOv8 & Bot-SORT native tracking reference: https://github.com/SkalskiP/yolov8-native-tracking

5. extract feeding velocity from the tracked results before 
6. using it scheduling the next feeding interval. 

requirements:
- python = 3.9.16
- ultralytics = 8.0.51
- supervision = 0.3.0
