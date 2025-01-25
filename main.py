from datetime import datetime, timedelta


def read_log_file(file_path):
    try:
        # Open the log file in read mode with UTF-8 encoding
        with open(file_path, 'r', encoding='utf-8') as file:
            log_data = file.readlines()
        return log_data
    except FileNotFoundError:
        # Print an error message if the file is not found
        print(f"The file {file_path} does not exist.")
        return []  # Return an empty list if the file does not exist


def write_to_export_file(export_path, log_data):
    try:
        # Open the export file in write mode with UTF-8 encoding
        with open(export_path, 'w', encoding='utf-8') as file:
            # Iterate over each line in the log data
            for line in log_data:
                file.write(line)
        # Print a success message
        print(f"Log data successfully written to {export_path}")
    except Exception as e:
        # Print an error message if an exception occurs
        print(f"An error occurred while writing to the file: {e}")


def filter_last_minute_logs(log_data):
    if not log_data:
        return []

    # Get the current date and time
    current_time = datetime.now()
    # Calculate the time three hours ago from now
    one_hour_ago = current_time - timedelta(hours=1)
    # Initialize an empty list to store filtered logs
    filtered_logs = []

    # Iterate over each line in the log data
    for line in log_data:
        try:
            # Extract the timestamp from the line
            timestamp_str = line.split(' ')[0] + ' ' + line.split(' ')[1]
            # Convert the timestamp string to a datetime object
            timestamp = datetime.strptime(timestamp_str, '%Y-%m-%d %H:%M:%S.%f')
            # Check if the timestamp is within the last three hours
            if timestamp >= one_hour_ago:
                # Add the line to the filtered logs list
                filtered_logs.append(line)
        except ValueError:
            # Skip the line if there is a ValueError (e.g., incorrect timestamp format)
            continue

    return filtered_logs


def main():
    # Path to the log file
    log_file_path = '/home/lukecollins/Documents/sftp.log.txt'
    # Path to the export file
    export_file_path = '/home/lukecollins/Documents/output.log'

    # Read the contents of the log file
    log_contents = read_log_file(log_file_path)

    if log_contents:
        # Filter logs from the last three hours
        last_minute_logs = filter_last_minute_logs(log_contents)
        # Write the filtered logs to the export file
        write_to_export_file(export_file_path, last_minute_logs)
    else:
        # Write an empty list to the export file if log contents are empty
        write_to_export_file(export_file_path, [])


if __name__ == "__main__":
    # Execute the main function if the script is run directly
    main()
