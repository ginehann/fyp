import matplotlib.pyplot as plt
import pandas as pd

def generate_graph_and_mean(table, datetime, output_graph):
    df = pd.read_csv(table)

    plt.plot(df['Time'], df['Aggregate Velocity'], color='red', label='Velocity (Rolling)')
    plt.legend()
    plt.xlabel('Time (seconds)')
    plt.ylabel('Velocity (pixels per second)')
    plt.title(f"Fishes' velocity when fed at {datetime}")
    plt.ylim(None, 1500)
    plt.savefig(output_graph) 

    mean_activity = df['Aggregate Velocity'].mean()
    return mean_activity 