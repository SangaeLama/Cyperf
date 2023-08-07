# Data Analysis Script for Traffic and Throughput Analysis

This Python script is designed to analyze network traffic and throughput data from provided CSV files. It calculates various metrics and generates insightful statistics related to network behavior during a steady segment. The script is intended for network analysis professionals and researchers using Cyperf for testing network performance on devices.

## Requirements

- Python 3.x
- Pandas
- Numpy
- zipfile

## Usage

1. Ensure you have the required dependencies installed.
2. Download or clone this repository to your local machine.
3. Place your CSV data files (client-throughput.csv and client-traffic-profile.csv) in the repository folder.
4. Open a terminal or command prompt and navigate to the repository folder.
5. Run the script using the following command:

  ``` bash
  python analyze_traffic.py <path_to_zip_file>
```
## Configuration
#Configure the steady segment
rampup_steps = 12
step_duration = 30
steady_segment_duration = 180


## Output
The script will generate the following outputs in the ./csvs directory:

- <zip_filename>_steady_segment_throughput.csv: CSV file containing the filtered throughput data during the steady segment.
- <zip_filename>_steady_segment_traffic.csv: CSV file containing the filtered traffic profile data during the steady segment.
- stats/<zip_filename>_stats.csv: CSV file containing statistics of the steady segment, including start time, end time, minimum, maximum, and average throughput, applications initiated, applications failed, and applications failure rate.

## Example
Suppose you have a zip file named data.zip containing client-throughput.csv and client-traffic-profile.csv. You can analyze the data by running:
``` python analyze_traffic.py data.zip

## License
This script is provided under the MIT License. Feel free to use and modify it according to your needs.

## Author
Author: SangaeLama
GitHub: https://github.com/SangaeLama

### Note: This script is intended for educational and research purposes. Use it responsibly and respect the terms of use for the data you analyze.


