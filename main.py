#start up
import datetime
from SshUtils import *
from RecordUtils import *
from DetectTrackUtils import *
from GraphUtils import *
from TimeUtils import *

#input parameters
vid_directory = "/Users/yapginehann/Desktop/codes"
yolo_model = f"{vid_directory}/train/results/weights/best.pt"

host = "192.168.0.101"  #Raspberry Pi's IP address
stream_port = "*" 
username = "*"
password = "*"
rpi_servo_filepath = "/home/gh/stepper.py"

datetime_now = datetime.datetime.now()
date = datetime_now.strftime('%d-%m-%y')
date_time = datetime_now.strftime('%d-%m-%y_%H_%M_%S')

print(f"Time now is : {datetime_now}")

#feed fishes
ssh_rpi(host, username, password, rpi_servo_filepath)

#RPi stream coming in, VLC download stream
vid_duration = "00:02:00" #change to default of 00:02:00

record_stream(f"http://{host}:{stream_port}", date_time, vid_directory, vid_duration)

#access stream, record for 2 mins
result_files = f"{vid_directory}/recordings/{date_time}/{date_time}"
streamed_vid = f"{result_files}.mp4"
output_vid = f"{result_files}-result.mp4"
output_table = f"{result_files}-result.csv"
output_graph = f"{result_files}-result.png"

#detect and track fishes with YOLO & BOT-Sort
fish_detector_tracker(streamed_vid, output_vid, output_table, yolo_model)

#generate graph, output mean_activity
mean_activity = generate_graph_and_mean(output_table, date_time, output_graph)

# run feeder logic on mean_activity, output time until next feeding
feed_table = f"{vid_directory}/recordings/feed_table.csv"
default_feed_interval = 21600 #change to default of 6 * 60 * 60 (6hrs)

result_interval = calculate_interval_and_update_table(feed_table, datetime_now, mean_activity, default_feed_interval)
next_feed_time = next_feed(datetime_now, result_interval)

# based on that, create a bash file that runs this python file again at that time.
schedule_next_feed(next_feed_time, vid_directory)