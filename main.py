import argparse
import logging
from datetime import datetime, timedelta


def read_log_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            log_data = file.readlines()
        return log_data
    except FileNotFoundError as e:
        logging.error("The file %s does not exist.", file_path)
        raise SystemExit(f"The file {file_path} does not exist.") from e


def write_to_export_file(export_path, log_data):
    try:
        with open(export_path, 'w', encoding='utf-8') as file:
            for line in log_data:
                file.write(line)
        logging.info("Log data successfully written to %s", export_path)
    except Exception as e:
        logging.error("An error occurred while writing to the file: %s", e)


def filter_last_minute_logs(log_data):
    if not log_data:
        return []

    current_time = datetime.now()
    one_hour_ago = current_time - timedelta(hours=1)
    filtered_logs = []

    for line in log_data:
        try:
            timestamp_str = line.split(' ')[0] + ' ' + line.split(' ')[1]
            timestamp = datetime.strptime(timestamp_str, '%Y-%m-%d %H:%M:%S.%f')
            if timestamp >= one_hour_ago:
                filtered_logs.append(line)
        except ValueError:
            continue

    return filtered_logs


def main(log_file_path, export_file_path):
    log_contents = read_log_file(log_file_path)

    if log_contents:
        last_minute_logs = filter_last_minute_logs(log_contents)
        write_to_export_file(export_file_path, last_minute_logs)
    else:
        write_to_export_file(export_file_path, [])


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process log files.")
    parser.add_argument('log_file_path', type=str, help="Path to the log file")
    parser.add_argument('export_file_path', type=str, help="Path to the export file")
    parser.add_argument('log_output_path', type=str, help="Path to the log output file")
    args = parser.parse_args()

    logging.basicConfig(filename=args.log_output_path, level=logging.INFO,
                        format='%(asctime)s - %(levelname)s - %(message)s')

    main(args.log_file_path, args.export_file_path)
