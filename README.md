# FTP Sync

A Python script that recursively downloads files from an FTP server with optional deletion of remote files. By default, the script only downloads files (safe mode). Remote file deletion is only performed when explicitly requested via command line flag.

## ⚠️ Warning

**When using the `--delete-remote` flag, this script DELETES files from the remote FTP server after downloading them.** Use with extreme caution and always test with non-critical data first. Make sure you have proper backups before running this script with the deletion flag on important data.

## Features

- **Safe by default**: Downloads files without deleting them from remote server
- **Optional deletion**: Remote file deletion only when `--delete-remote` flag is used
- Recursively processes directories and subdirectories
- Downloads files from FTP server to local directory
- Comprehensive logging of all operations
- Type-hinted Python code for better maintainability
- Command-line interface with flexible options

## Requirements

- Python 3.6 or higher
- No external dependencies (uses only standard library modules)

## Installation

1. Clone or download this repository
2. Make the script executable (optional):
   ```bash
   chmod +x ftp_sync.py
   ```

## Usage

### Basic Usage (Safe Mode - Download Only)

```bash
python3 ftp_sync.py --host ftp.example.com --user username --password password --local-dir /path/to/local/directory
```

### Download with Remote Deletion (Destructive Mode)

```bash
python3 ftp_sync.py --host ftp.example.com --user username --password password --local-dir /path/to/local/directory --delete-remote
```

### Advanced Usage

```bash
python3 ftp_sync.py \
    --host ftp.example.com \
    --user username \
    --password password \
    --remote-dir /specific/remote/directory \
    --local-dir /path/to/local/directory \
    --log-file custom_sync.log \
    --delete-remote
```

## Command Line Arguments

| Argument | Required | Default | Description |
|----------|----------|---------|-------------|
| `--host` | Yes | - | FTP server hostname or IP address |
| `--user` | Yes | - | FTP username |
| `--password` | Yes | - | FTP password |
| `--remote-dir` | No | `/` | Remote directory to start synchronization from |
| `--local-dir` | Yes | - | Local directory to save downloaded files |
| `--log-file` | No | `ftp_sync.log` | Path to log file for operation records |
| `--delete-remote` | No | `False` | **DESTRUCTIVE**: Delete remote files after successful download |

## Examples

### Download entire FTP root directory (safe mode)
```bash
python3 ftp_sync.py --host ftp.myserver.com --user myuser --password mypass --local-dir ./downloads
```

### Download and delete entire FTP root directory (destructive mode)
```bash
python3 ftp_sync.py --host ftp.myserver.com --user myuser --password mypass --local-dir ./downloads --delete-remote
```

### Download specific remote directory (safe mode)
```bash
python3 ftp_sync.py --host ftp.myserver.com --user myuser --password mypass --remote-dir /uploads/2024 --local-dir ./2024_files
```

### Use custom log file with deletion enabled
```bash
python3 ftp_sync.py --host ftp.myserver.com --user myuser --password mypass --local-dir ./downloads --log-file ./logs/sync_$(date +%Y%m%d).log --delete-remote
```

## How It Works

1. **Connection**: Establishes connection to the FTP server using provided credentials
2. **Safety Check**: Displays operation mode (safe download-only or destructive download-and-delete)
3. **Directory Processing**: Recursively traverses directories starting from the specified remote directory
4. **File Download**: Downloads each file to the corresponding local directory structure
5. **Verification**: Verifies successful download by checking file existence and size
6. **Optional Deletion**: Only when `--delete-remote` flag is used, deletes the remote file after successful download verification
7. **Logging**: Records all operations, successes, and errors in the log file with operation mode

## Directory Structure

The script maintains the same directory structure locally as exists on the remote FTP server. For example:

```
Remote FTP:           Local Directory:
/uploads/             ./downloads/uploads/
├── 2024/            ├── 2024/
│   ├── file1.txt    │   ├── file1.txt
│   └── file2.pdf    │   └── file2.pdf
└── archive/         └── archive/
    └── old.zip          └── old.zip
```

## Error Handling

- Network errors are caught and logged
- Failed downloads never result in file deletion (even when `--delete-remote` is used)
- Partial downloads are detected and logged as failures
- The script continues processing other files even if individual files fail
- Safe mode prevents accidental data loss

## Logging

All operations are logged with timestamps including:
- Connection events
- Operation mode (download only vs download and delete)
- Successful downloads (with or without deletion)
- Failed operations with error messages
- Sync start and completion times

Log format examples:

**Safe mode (download only):**
```
2024-01-15 10:30:00.123456 - Starting FTP sync (download only)
2024-01-15 10:30:01.234567 - Connected to ftp.example.com
2024-01-15 10:30:02.345678 - Downloaded: /uploads/file1.txt
2024-01-15 10:30:05.456789 - FTP sync completed successfully (download only)
```

**Destructive mode (download and delete):**
```
2024-01-15 10:30:00.123456 - Starting FTP sync (download and delete)
2024-01-15 10:30:01.234567 - Connected to ftp.example.com
2024-01-15 10:30:02.345678 - Downloaded and deleted: /uploads/file1.txt
2024-01-15 10:30:05.456789 - FTP sync completed successfully (download and delete)
```

## Security Considerations

- Passwords are passed as command-line arguments (consider using environment variables for production)
- FTP connections are not encrypted (consider FTPS if available)
- Always test with non-critical data first
- Ensure proper network security when transferring sensitive files

## Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues for bugs and feature requests.

## License

This project is licensed under the GNU General Public License v2.0 - see below for details.

```
FTP Sync - Recursive FTP download and cleanup tool
Copyright (C) 2024

This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 2 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License along
with this program; if not, write to the Free Software Foundation, Inc.,
51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
```

## Disclaimer

This software is provided "as is" without warranty of any kind. The authors are not responsible for any data loss or damage that may occur from using this tool. Always backup your data before running any destructive operations. 