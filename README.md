# Final Year Project codes
A MV pipeline that automates feeding of fishes by detecting, tracking, classify satiety (via feeding velocity) and scheduling feeding interval. 

It uses 
- MotionEye to stream footages from camera connected to Raspberry Pi
- Use SSH to toggle feeding 
- YOLOv8 to detect fishes, 
- Bot-SORT to track them, 
- extract feeding velocity from the tracked results before 
- using it scheduling the next feeding interval. 

requirements:
- python = 3.9.16
- ultralytics = 8.0.51
- supervision = 0.3.0
