# fyp
A MV pipeline that automates feeding of fishes by detecting, tracking, classify satiety (via feeding velocity) and scheduling feeding interval. 

It uses YOLOv8 to detect fishes, 
Bot-SORT to track them, 
extract feeding velocity before 
scheduling the next feeding interval. 

requirements:
python = 3.9.16
ultralytics = 8.0.51
supervision = 0.3.0
