import pandas as pd

# Load the logs
real_time_log = pd.read_csv('real_time_color_detection.log', sep=' - ', engine='python', names=['timestamp', 'data'])
knn_log = pd.read_csv('k_nearest_real_time_color_detection.log', sep=' - ', engine='python', names=['timestamp', 'data'])

# Function to extract color name and RGB values from log data
def parse_log(data):
    parts = data.split()
    color_name = ' '.join(parts[:-3])
    r = int(parts[-3].split('=')[1])
    g = int(parts[-2].split('=')[1])
    b = int(parts[-1].split('=')[1])
    return color_name, r, g, b

# Compare logs
comparison_results = []

for rt_entry, knn_entry in zip(real_time_log['data'], knn_log['data']):
    rt_color_name, rt_r, rt_g, rt_b = parse_log(rt_entry)
    knn_color_name, knn_r, knn_g, knn_b = parse_log(knn_entry)
    
    comparison_results.append({
        'Real Time Color Name': rt_color_name,
        'Real Time RGB': (rt_r, rt_g, rt_b),
        'k-NN Color Name': knn_color_name,
        'k-NN RGB': (knn_r, knn_g, knn_b),
        'Match': rt_color_name == knn_color_name
    })

# Create a DataFrame to display results
comparison_df = pd.DataFrame(comparison_results)

# Display the comparison results
print(comparison_df)
