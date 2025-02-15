import argparse
import logging
import re
import os
from datetime import datetime, timedelta


# Function to read the log file
def read_log_file(file_path, export_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            log_data = file.readlines()
        return log_data
    except FileNotFoundError as e:
        logging.error("The file %s does not exist.", file_path)
        # Clear the contents of the output file if the log file does not exist
        with open(export_path, 'w', encoding='utf-8') as file:
            file.write('')
        raise SystemExit(f"The file {file_path} does not exist.") from e


# Function to write filtered log data to the export file
def write_to_export_file(export_path, log_data):
    try:
        with open(export_path, 'w', encoding='utf-8') as file:
            for line in log_data:
                file.write(line)
        logging.info("Log data successfully written to %s", export_path)
    except Exception as e:
        logging.error("An error occurred while writing to the file: %s", e)


# Function to filter logs based on timestamp
def filter_logs_by_timestamp(log_data, regex_pattern, timestamp_format, hours):
    if not log_data:
        return []

    current_time = datetime.now()
    time_threshold = current_time - timedelta(hours=hours)
    filtered_logs = []

    for line in log_data:
        try:
            # Search for the timestamp pattern using the provided regex pattern
            match = re.search(regex_pattern, line)
            if match:
                timestamp_str = match.group(0)
                # Convert the timestamp string to a datetime object
                timestamp = datetime.strptime(timestamp_str, timestamp_format)
                # Check if the timestamp is within the specified time range
                if timestamp >= time_threshold:
                    filtered_logs.append(line)
        except ValueError:
            continue

    return filtered_logs


# Main function to process the log file
def main(log_file_path, export_file_path, regex_pattern, timestamp_format, hours):
    # Normalize file paths for cross-platform compatibility
    log_file_path = os.path.normpath(log_file_path)
    export_file_path = os.path.normpath(export_file_path)

    # Read the log file
    log_contents = read_log_file(log_file_path, export_file_path)

    if log_contents:
        # Filter logs based on the timestamp
        filtered_logs = filter_logs_by_timestamp(log_contents, regex_pattern,
                                                 timestamp_format, hours)
        # Write filtered logs to the export file
        write_to_export_file(export_file_path, filtered_logs)
    else:
        # Write an empty list to the export file if no log contents
        write_to_export_file(export_file_path, [])


if __name__ == "__main__":
    # Set up argument parsing
    parser = argparse.ArgumentParser(description="Process log files.")
    parser.add_argument(
        '--log_file_path', type=str, required=True, help="Path to the log file"
    )
    parser.add_argument(
        '--export_file_path', type=str, required=True, help="Path to the export file"
    )
    parser.add_argument(
        '--log_output_path', type=str, required=True, help="Path to the log output file"
    )
    parser.add_argument(
        '--regex_pattern', type=str, required=True, help="Regex for the timestamp"
    )
    parser.add_argument(
        '--timestamp_format', type=str, required=True, help="Timestamp format parsing"
    )
    parser.add_argument(
        '--hours', type=int, required=True, help="Number of hours to look back"
    )
    args = parser.parse_args()

    # Set up logging configuration
    logging.basicConfig(
        filename=os.path.normpath(args.log_output_path), level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )

    # Run the main function with parsed arguments
    main(args.log_file_path, args.export_file_path, args.regex_pattern,
         args.timestamp_format, args.hours)
