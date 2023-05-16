import pandas as pd
import os

# feeding logic equation
def give_interval(previous_interval, previous_mean_activity, new_mean_activity):
    return previous_interval * (previous_mean_activity / new_mean_activity)

def calculate_interval_and_update_table(table, datetime, mean, def_interval):
    # read the initial table, or create a new one if it doesn't exist
    try:
        df = pd.read_csv(table)
    except FileNotFoundError:
        df = pd.DataFrame(columns=["time", "mean_activity", "interval"])

    # check if the table is empty
    if df.empty:
        # if it's the first entry, create a new row with default values
        time = datetime # replace with the actual starting time
        mean_activity = mean # replace with the actual starting mean activity
        interval = def_interval # replace with the actual default interval
        df.loc[0] = [time, mean_activity, interval]
        print("Default interval:", interval)
        
    else:
        # get the previous row
        previous_row = df.iloc[-1]
        # calculate the new interval
        interval = give_interval(previous_row["interval"], previous_row["mean_activity"], mean)
        
        # create a new row with the updated values
        time = datetime
        mean_activity = mean # replace with the actual new mean activity
        df.loc[len(df)] = [time, mean_activity, interval]
        print("New interval:", interval)

    # save the updated table to disk
    df.to_csv(table, index=False)
    return interval

# set next feeding time based on time now + calculated interval
def next_feed(datetime_now, interval):
    next_time = datetime_now + pd.Timedelta(seconds=interval)
    
    # if next feeding time > 11pm, set it to 9am on the next day
    end_of_day = datetime_now.replace(hour=23, minute=0, second=0, microsecond=0)
    if next_time > end_of_day:
        # adjust the interval to start at 9am on the next day
        next_day = datetime_now + pd.Timedelta(days=1)
        next_day_9am = next_day.replace(hour=9, minute=0, second=0, microsecond=0)
        print(f"Next feeding time is at : {next_day_9am}")
        return next_day_9am
    else: 
        print(f"Next feeding time is at : {next_time}")
        return next_time

def schedule_next_feed(scheduled_time, directory):
    # Set the datetime to schedule the program
    print("scheduling...")

    # Prepare script that runs virtual environment & main.py
    activate_venv = f"source {directory}/bin/activate"
    str_sch_time = scheduled_time.strftime('%d-%m-%y_%H_%M_%S')
    script = f"export PATH=$PATH:/usr/local/bin\n{activate_venv}\npython {directory}/main.py 2>&1 | tee -a {directory}/recordings/{str_sch_time}-log.txt"
    # Write the script to a file
    with open("run_program.sh", "w") as f:
        f.write(script)

    cmd = f"{directory}/run_program.sh"

    # Schedule the script to run at the specified time using crontab
    at_time = scheduled_time.strftime("%M %H %d %m *")
    os.system(f"(crontab -l ; echo '{at_time} /bin/bash {cmd}') | crontab -")
    print("done.")

