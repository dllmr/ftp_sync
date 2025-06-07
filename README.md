# FTP Sync

A Python script that recursively downloads files from an FTP server with optional deletion of remote files. By default, the script only downloads files (safe mode). Remote file deletion is only performed when explicitly requested via command line flag.

## ⚠️ Warning

**When using the `--delete-remote` flag, this script DELETES files from the remote FTP server after downloading them.** Use with extreme caution and always test with non-critical data first. Make sure you have proper backups before running this script with the deletion flag on important data.

## Features

- **Safe by default**: Downloads files without deleting them from remote server
- **Optional deletion**: Remote file deletion only when `--delete-remote` flag is used
- **Flatten option**: Download all files to top-level directory, ignoring remote directory structure
- **Flexible logging**: Optional logging with ability to disable log file creation
- Recursively processes directories and subdirectories
- Downloads files from FTP server to local directory
- Comprehensive logging of all operations (when enabled)
- Type-hinted Python code for better maintainability
- Command-line interface with flexible options and short argument versions

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
python3 ftp_sync.py --server ftp.example.com --user username --password password --local-dir /path/to/local/directory
```

### Using Short Arguments

```bash
python3 ftp_sync.py -s ftp.example.com -u username -p password -l /path/to/local/directory
```

### Download with Remote Deletion (Destructive Mode)

```bash
python3 ftp_sync.py -s ftp.example.com -u username -p password -l /path/to/local/directory --delete-remote
```

### Flatten Directory Structure

```bash
python3 ftp_sync.py -s ftp.example.com -u username -p password -l /path/to/local/directory --flatten
```

### Disable Logging

```bash
python3 ftp_sync.py -s ftp.example.com -u username -p password -l /path/to/local/directory --no-log
```

### Advanced Usage with All Options

```bash
python3 ftp_sync.py \
    --server ftp.example.com \
    --user username \
    --password password \
    --remote-dir /specific/remote/directory \
    --local-dir /path/to/local/directory \
    --delete-remote \
    --flatten \
    --no-log
```

## Command Line Arguments

| Short | Long | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `-s` | `--server` | Yes | - | FTP server hostname or IP address |
| `-u` | `--user` | Yes | - | FTP username |
| `-p` | `--password` | Yes | - | FTP password |
| `-r` | `--remote-dir` | No | `/` | Remote directory to start synchronization from |
| `-l` | `--local-dir` | Yes | - | Local directory to save downloaded files |
| `-d` | `--delete-remote` | No | `False` | **DESTRUCTIVE**: Delete remote files after successful download |
| `-f` | `--flatten` | No | `False` | Download all files to top-level directory, flattening directory structure |
| `-n` | `--no-log` | No | `False` | Disable log file creation (no logging to file) |

## Examples

### Download entire FTP root directory (safe mode)
```bash
python3 ftp_sync.py -s ftp.myserver.com -u myuser -p mypass -l ./downloads
```

### Download and delete entire FTP root directory (destructive mode)
```bash
python3 ftp_sync.py -s ftp.myserver.com -u myuser -p mypass -l ./downloads -d
```

### Download specific remote directory with flattened structure
```bash
python3 ftp_sync.py -s ftp.myserver.com -u myuser -p mypass -r /uploads/2024 -l ./2024_files --flatten
```

### Download without creating log file
```bash
python3 ftp_sync.py -s ftp.myserver.com -u myuser -p mypass -l ./downloads --no-log
```

### Combine all options using short arguments
```bash
python3 ftp_sync.py -s ftp.myserver.com -u myuser -p mypass -r /data -l ./downloads -dfn
```

## How It Works

1. **Connection**: Establishes connection to the FTP server using provided credentials
2. **Safety Check**: Displays operation mode (safe download-only or destructive download-and-delete)
3. **Directory Processing**: Recursively traverses directories starting from the specified remote directory
4. **File Download**: Downloads each file to the corresponding local directory structure (or flattened if `--flatten` is used)
5. **Verification**: Verifies successful download by checking file existence and size
6. **Optional Deletion**: Only when `--delete-remote` flag is used, deletes the remote file after successful download verification
7. **Logging**: Records all operations, successes, and errors in the log file (unless `--no-log` is specified)

## Directory Structure Options

### Normal Mode (Default)
The script maintains the same directory structure locally as exists on the remote FTP server:

```
Remote FTP:           Local Directory:
/uploads/             ./downloads/uploads/
├── 2024/            ├── 2024/
│   ├── file1.txt    │   ├── file1.txt
│   └── file2.pdf    │   └── file2.pdf
└── archive/         └── archive/
    └── old.zip          └── old.zip
```

### Flatten Mode (`--flatten`)
All files are downloaded to the top-level local directory with path-based naming to prevent conflicts:

```
Remote FTP:           Local Directory (Flattened):
/uploads/             ./downloads/
├── 2024/            ├── uploads_2024_file1.txt
│   ├── file1.txt    ├── uploads_2024_file2.pdf
│   └── file2.pdf    └── uploads_archive_old.zip
└── archive/
    └── old.zip
```

## Error Handling

- Network errors are caught and logged
- Failed downloads never result in file deletion (even when `--delete-remote` is used)
- Partial downloads are detected and logged as failures
- The script continues processing other files even if individual files fail
- Safe mode prevents accidental data loss

## Logging

All operations are logged with timestamps (unless `--no-log` is specified) including:
- Connection events
- Operation mode (download only vs download and delete)
- Directory structure mode (normal vs flattened)
- Successful downloads (with or without deletion)
- Failed operations with error messages
- Sync start and completion times

The log file is always named `ftp_sync.log` and is created in the current working directory.

Log format examples:

**Safe mode (download only):**
```
2024-01-15 10:30:00.123456 - Starting FTP sync (download only)
2024-01-15 10:30:01.234567 - Connected to ftp.example.com
2024-01-15 10:30:02.345678 - Downloaded: /uploads/file1.txt -> ./downloads/uploads/file1.txt
2024-01-15 10:30:05.456789 - FTP sync completed successfully (download only)
```

**Destructive mode with flattening:**
```
2024-01-15 10:30:00.123456 - Starting FTP sync (download and delete) (flattened)
2024-01-15 10:30:01.234567 - Connected to ftp.example.com
2024-01-15 10:30:02.345678 - Downloaded and deleted: /uploads/file1.txt -> ./downloads/uploads_file1.txt
2024-01-15 10:30:05.456789 - FTP sync completed successfully (download and delete) (flattened)
```

**No-log mode:**
When `--no-log` is specified, no log file is created and all logging output is discarded while console output remains visible.

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