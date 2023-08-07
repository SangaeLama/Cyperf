import zipfile
import sys
import pandas as pd
import numpy as np

#----------------
# Change the following values of steps and duration (in seconds) as required.
rampup_steps = 12
step_duration = 30
steady_segment_duration = 180

rampup_period = rampup_steps * step_duration
#----------------

def extract_file(zip_path, file_to_extract, output_dir):
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extract(file_to_extract, path=output_dir)

# Example usage
zip_path = sys.argv[1]
throughput_file_to_extract = 'client-throughput.csv'
traffic_file_to_extract = 'client-traffic-profile.csv'
output_dir = './csvs/pytemp/'

extract_file(zip_path, throughput_file_to_extract, output_dir)
extract_file(zip_path, traffic_file_to_extract, output_dir)

csv_path = './csvs/pytemp/client-throughput.csv'
csv2_path = './csvs/pytemp/client-traffic-profile.csv'

throughputDf = pd.read_csv(csv_path, parse_dates=['Timestamp'])
trafficDf = pd.read_csv(csv2_path, parse_dates=['Timestamp'])

# Convert Timestamp to datetime type
throughputDf['Timestamp'] = pd.to_datetime(throughputDf['Timestamp'])
trafficDf['Timestamp'] = pd.to_datetime(trafficDf['Timestamp'])
# Filter the throughput DataFrame to ignore the first few entries with throughput less than 1
throughputDf = throughputDf[throughputDf['Throughput'] >= 1]

# Calculate the start time of the steady segment
steady_start = throughputDf['Timestamp'].iloc[0] + pd.Timedelta(seconds=rampup_period)
steady_end = throughputDf['Timestamp'].iloc[0] + pd.Timedelta(seconds=rampup_period+steady_segment_duration)

print(f"Steady Segment Start: {steady_start}\n")
print(f"Steady Segment End: {steady_end}\n")

# Filter the steady segment based on the start and end times
steady_segment_throughput = throughputDf.loc[
    (throughputDf['Timestamp'] >= steady_start) & (throughputDf['Timestamp'] < steady_end)].copy()

steady_segment_traffic = trafficDf.loc[
    (trafficDf['Timestamp'] >= steady_start) & (trafficDf['Timestamp'] < steady_end)].copy()
#print (f"Steady Segment Traffic Profile:\n {steady_segment_traffic}")

#-----------------
# Convert Throughput to Megabits per second (Mbps)
steady_segment_throughput['Throughput'] = steady_segment_throughput['Throughput'] / (1000**2)

#----------------------------------------------------------------------------------------------

steady_segment_throughput.to_csv('./csvs/'+zip_path+'_steady_segment_throughput.csv', index=False)
steady_segment_traffic.to_csv('./csvs/'+zip_path+'_steady_segment_traffic.csv', index=False)

#----------------------------------------------------------------------------------------------

# Calculate the minimum, maximum, and average throughput of the steady segment
minimum_throughput = steady_segment_throughput['Throughput'].min()
maximum_throughput = steady_segment_throughput['Throughput'].max()
average_throughput = steady_segment_throughput['Throughput'].mean()

#print (steady_segment)

#--------------------------

uniq_apps = trafficDf['Application'].unique()
#print(uniq_apps)
uniq_apps_count = len(uniq_apps)

first_steady_entries = steady_segment_traffic.head(uniq_apps_count)
last_steady_entries = steady_segment_traffic.tail(uniq_apps_count)

# Calculate the sum of each column for the last uniq_apps_count entries
initial_sum_of_columns = first_steady_entries.drop(columns=['Timestamp epoch ms', 'Profile', 'Application', 'Timestamp']).sum()
initial_sum_row = pd.DataFrame(initial_sum_of_columns).transpose()

Initial_Apps_Inited = first_steady_entries['Applications Initiated'].sum()
Initial_Apps_Failed = first_steady_entries['Applications Failed'].sum()
Final_Apps_Inited = last_steady_entries['Applications Initiated'].sum()
Final_Apps_Failed = last_steady_entries['Applications Failed'].sum()
Initial_Apps_Failure = Initial_Apps_Failed/Initial_Apps_Inited * 100
Final_Apps_Failure = Final_Apps_Failed/Final_Apps_Inited * 100

final_sum_of_columns = last_steady_entries.drop(columns=['Timestamp epoch ms', 'Profile', 'Application', 'Timestamp']).sum()
final_sum_row = pd.DataFrame(final_sum_of_columns).transpose()

#print(f"Initial Apps Fail Rate: {Initial_Apps_Failure}\n")
print(f"Applications Initiated: {Final_Apps_Inited}\n")
print(f"Applications Failed: {Final_Apps_Failed}\n")
print(f"Applications Failure Rate: {Final_Apps_Failure} %\n")
print(f"Steady Segment Stats of {zip_path}:\n")
print(f"Minimum throughput: {minimum_throughput} Mbps\n")
print(f"Maximum throughput: {maximum_throughput} Mbps\n")
print(f"Average throughput: {average_throughput} Mbps\n")

result = pd.concat([steady_segment_traffic, final_sum_row])
result.to_csv('./csvs/'+zip_path+'_steady_segment_traffic.csv', index=False)
#print(result.drop(columns=['Timestamp epoch ms', 'Profile', 'Application', 'Timestamp', 'Applications Succeeded','Connections Succeeded', 'Bytes Sent', 'Bytes Received']).tail(1))

# Write the statistics to a CSV file
stats_df = pd.DataFrame({
    'Metric': ['Steady Segment Start', 'Steady Segment End', 'Minimum throughput', 'Maximum throughput', 'Average throughput', 'Applications Initiated', 'Applications Failed', 'Applications Failure Rate'],
    'Value': [steady_start, steady_end, minimum_throughput, maximum_throughput, average_throughput, Final_Apps_Inited, Final_Apps_Failed, Final_Apps_Failure]
})
stats_df.to_csv('./csvs/stats/'+zip_path+'_stats.csv', index=False)
