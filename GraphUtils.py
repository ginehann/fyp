import matplotlib.pyplot as plt
import pandas as pd

def generate_graph_and_mean(table, datetime, output_graph):
    df = pd.read_csv(table)
    
    # plot a graph with x= time, y= aggregate velocity
    plt.plot(df['Time'], df['Aggregate Velocity'], color='red', label='Velocity (Rolling)')
    plt.legend()
    plt.xlabel('Time (seconds)')
    plt.ylabel('Velocity (pixels per second)')
    plt.title(f"Fishes' velocity when fed at {datetime}")
    plt.ylim(None, 1500)
    
    # save it into a file
    plt.savefig(output_graph) 

    # also return mean velocity
    mean_activity = df['Aggregate Velocity'].mean()
    return mean_activity 
