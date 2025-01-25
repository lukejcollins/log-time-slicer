import argparse
import logging
import re
from datetime import datetime, timedelta


def read_log_file(file_path, export_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            log_data = file.readlines()
        return log_data
    except FileNotFoundError as e:
        logging.error("The file %s does not exist.", file_path)
        # Clear the contents of the output file
        with open(export_path, 'w', encoding='utf-8') as file:
            file.write('')
        raise SystemExit(f"The file {file_path} does not exist.") from e


def write_to_export_file(export_path, log_data):
    try:
        with open(export_path, 'w', encoding='utf-8') as file:
            for line in log_data:
                file.write(line)
        logging.info("Log data successfully written to %s", export_path)
    except Exception as e:
        logging.error("An error occurred while writing to the file: %s", e)


def filter_logs_by_timestamp(log_data, regex_pattern, timestamp_format):
    if not log_data:
        return []

    current_time = datetime.now()
    one_hour_ago = current_time - timedelta(hours=1)
    filtered_logs = []

    for line in log_data:
        try:
            # Search for the timestamp pattern anywhere using the provided regex pattern
            match = re.search(regex_pattern, line)
            if match:
                timestamp_str = match.group(0)
                # Convert the timestamp string to a datetime object
                timestamp = datetime.strptime(timestamp_str, timestamp_format)
                # Check if the timestamp is within the last hour
                if timestamp >= one_hour_ago:
                    filtered_logs.append(line)
        except ValueError:
            continue

    return filtered_logs


def main(log_file_path, export_file_path, regex_pattern, timestamp_format):
    log_contents = read_log_file(log_file_path, export_file_path)

    if log_contents:
        filtered_logs = filter_logs_by_timestamp(log_contents, regex_pattern,
                                                 timestamp_format)
        write_to_export_file(export_file_path, filtered_logs)
    else:
        write_to_export_file(export_file_path, [])


if __name__ == "__main__":
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
    args = parser.parse_args()

    logging.basicConfig(
        filename=args.log_output_path, level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )

    main(args.log_file_path, args.export_file_path, args.regex_pattern,
         args.timestamp_format)
