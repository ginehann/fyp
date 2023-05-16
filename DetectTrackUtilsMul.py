import cv2
from ultralytics import YOLO
import supervision as sv
import numpy as np
import pandas as pd

# same as DetectTrackUtils.py, except generate an extra video with moving dots of detected fishes
def fish_detector_tracker(streamed_vid, detected_vid, dot_vid, output_table ,MODEL): # file path to streamed_vid, detected_vid, etc.

    print("Running Object Detection & Tracking software...")

    # fuse model to YOLO
    model = YOLO(MODEL)
    model.fuse()

    # box annotator parameters
    box_annotator = sv.BoxAnnotator(
        thickness=1,
        text_thickness=1,
        text_scale=0.5
    )

    # video parameters
    cap = cv2.VideoCapture(streamed_vid)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = float(cap.get(cv2.CAP_PROP_FPS))
    fourcc = int(cap.get(cv2.CAP_PROP_FOURCC))
    out = cv2.VideoWriter(detected_vid, fourcc, fps, (width, height), isColor=True)
    out2 = cv2.VideoWriter(dot_vid, fourcc, fps, (width, height), isColor=True)

    previous_coords = {}
    velocity_whole_video = []

    # detect & track using one line.
    for result in model.track(source=streamed_vid, show=False, stream=True, agnostic_nms=True):
        
        frame = result.orig_img
        detections = sv.Detections.from_yolov8(result)

        if result.boxes.id is not None:
            detections.tracker_id = result.boxes.id.cpu().numpy().astype(int)

        # Extract the tracker ids from the detections
        tracker_ids = [d[-1] for d in detections if d[-1] is not None]

        # Filter out detections with no tracker id
        detections = [d for d in detections if d[-1] is not None]

        # initialise 
        labels = []
        velocity_in_frame = []
        
        # create empty frame
        empty_frame = np.full((480, 640, 3), 255, dtype = np.uint8)

        # loop over each detections in a single frame
        for i, (xyxy, confidence, class_id, tracker_id) in enumerate(detections):
        
        # extract and write centre coordinates
            x1, y1, x2, y2 = xyxy.astype(int)
            c_x = int((x1 + x2)/2)
            c_y = int((y1 + y2)/2)
            empty_frame = cv2.circle(empty_frame, (c_x, c_y), radius=3, color=(0,0,255), thickness=-1)
        
            # if tracker id is same, calculate and update velocity. 
            prev_vel = [0]
            prefTime = [0]
            if tracker_id in previous_coords:
                prev_c_x, prev_c_y, prefTime, prev_vel= previous_coords[tracker_id]

                # calculate rolling velocity
                dist = np.sqrt((c_x - prev_c_x)**2 + (c_y - prev_c_y)**2)
                latestVel = prev_vel[-100:]
                latestTime = prefTime[-100:]
                for j in range(len(latestTime)):
                    dist += latestTime[j] * latestVel[j]

                # rolling velocity = total dist/ total time for last 100 records
                velocity = dist / (np.sum(latestTime) + 1/fps)
                velocity_in_frame.append(velocity)
                prefTime.append(1/fps)
                prev_vel.append(velocity)
            
            # input labels.
            previous_coords[tracker_id] = (c_x, c_y, prefTime, prev_vel)
            labels.append(f"#{tracker_id} {confidence:0.2f} {int(prev_vel[-1])}p/s")

        # sum up the velocities in a single frame, then append to a list
        total_velocity_in_frame = np.sum(velocity_in_frame)
        velocity_whole_video.append(total_velocity_in_frame)

        frame = box_annotator.annotate(
            scene=frame, 
            detections=detections,
            labels=labels
        )

        # write both videos.
        out.write(frame)
        out2.write(empty_frame)
    
    out.release()
    out2.release()
    cv2.destroyAllWindows()

    # create a dataframe with time & aggregate velocity as columns
    frame_timings = np.round(np.arange(len(velocity_whole_video)) / fps, 3)
    df = pd.DataFrame({'Time': frame_timings, 'Aggregate Velocity': velocity_whole_video})
  
    # save dataframe to a csv file
    df.to_csv(output_table, index=False)

    print("Finished Object Detection & Tracking.")
