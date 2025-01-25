# Log Time Slicer

Log Time Slicer is a tool designed to process log files by extracting log lines with timestamps and outputting a truncated version based on a specified number of hours to look back. This application is particularly useful for scenarios where there is a need to parse log files with PRTG's file sensor, which cannot tail a logfile or read back a logfile to a point specified by a timestamp. Although it was designed to solve a limitation with PRTG, it is free for use for any similar purpose.

## Features

- Extracts log lines based on timestamps.
- Outputs a truncated version of the log file.
- Configurable number of hours to look back.
- Cross-platform compatibility (Windows and Linux).

## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/lukejcollins/log-time-slicer.git
    cd log-time-slicer
    ```

2. Install the required dependencies:
    ```sh
    pip install -r requirements.txt
    ```

## Usage

To use Log Time Slicer, run the following command:

```sh
python main.py --log_file_path <path_to_log_file> --export_file_path <path_to_export_file> --log_output_path <path_to_log_output_file> --regex_pattern <timestamp_regex> --timestamp_format <timestamp_format> --hours <number_of_hours>
```

### Arguments

- `--log_file_path`: Path to the log file.
- `--export_file_path`: Path to the export file.
- `--log_output_path`: Path to the log output file.
- `--regex_pattern`: Regex pattern for the timestamp.
- `--timestamp_format`: Timestamp format for parsing.
- `--hours`: Number of hours to look back.

### Example

```sh
python main.py --log_file_path logs/application.log --export_file_path logs/filtered.log --log_output_path logs/output.log --regex_pattern "\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}" --timestamp_format "%Y-%m-%d %H:%M:%S" --hours 1
```

## GitHub Actions

This repository includes a GitHub Actions workflow to build and release the application as Windows and Linux x86/64 binaries. The workflow is triggered when a new release is created.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.

## License

This project is licensed under the MIT License. See the LICENSE file for details.
