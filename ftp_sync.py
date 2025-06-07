#!/usr/bin/env python3

import os
import sys
import ftplib
import argparse
from datetime import datetime
from typing import TextIO, List

def ensure_local_dir(local_path: str) -> None:
    """Create local directory if it doesn't exist"""
    if not os.path.exists(local_path):
        os.makedirs(local_path)

def process_directory(ftp: ftplib.FTP, remote_dir: str, local_dir: str, log_file: TextIO, delete_remote: bool = False, flatten: bool = False) -> bool:
    """Recursively download and optionally delete files from remote directory
    Returns True if all operations successful, False if any errors occurred"""
    print(f"Processing directory: {remote_dir}")
    
    success = True
    
    # Change to remote directory
    ftp.cwd(remote_dir)
    
    # Create corresponding local directory only if not flattening
    if not flatten:
        ensure_local_dir(local_dir)
    
    # List files and directories
    file_list: List[str] = []
    ftp.dir(file_list.append)
    
    # Process each item
    for item in file_list:
        # Parse the item string to get file/directory name
        tokens: List[str] = item.split()
        if len(tokens) < 9:
            continue
            
        file_name: str = " ".join(tokens[8:])
        
        # Skip current and parent directory entries
        if file_name in ['.', '..']:
            continue
            
        # Construct absolute remote path
        if remote_dir.endswith('/'):
            remote_path: str = f"{remote_dir}{file_name}"
        else:
            remote_path: str = f"{remote_dir}/{file_name}"
        
        # Check if it's a directory
        if item.startswith('d'):
            # Recursively process subdirectory
            if flatten:
                # When flattening, continue using the same local_dir (root)
                if not process_directory(ftp, remote_path, local_dir, log_file, delete_remote, flatten):
                    success = False
            else:
                # Normal behavior: create subdirectory
                sub_local_path: str = os.path.join(local_dir, file_name)
                if not process_directory(ftp, remote_path, sub_local_path, log_file, delete_remote, flatten):
                    success = False
        else:
            # Determine local file path
            if flatten:
                # Create a safe filename by replacing path separators with underscores
                # Remove leading slash and replace remaining slashes with underscores
                safe_remote_path = remote_path.lstrip('/').replace('/', '_')
                local_path: str = os.path.join(local_dir, safe_remote_path)
            else:
                local_path: str = os.path.join(local_dir, file_name)
            
            # Download file
            try:
                with open(local_path, 'wb') as local_file:
                    ftp.retrbinary(f'RETR {file_name}', local_file.write)
                
                # Verify file was downloaded successfully
                if os.path.exists(local_path) and os.path.getsize(local_path) > 0:
                    if delete_remote:
                        # Delete remote file only if flag is set
                        ftp.delete(file_name)
                        log_file.write(f"{datetime.now()} - Downloaded and deleted: {remote_path} -> {local_path}\n")
                        print(f"Downloaded and deleted: {remote_path} -> {local_path}")
                    else:
                        log_file.write(f"{datetime.now()} - Downloaded: {remote_path} -> {local_path}\n")
                        print(f"Downloaded: {remote_path} -> {local_path}")
                else:
                    log_file.write(f"{datetime.now()} - Download failed: {remote_path}\n")
                    print(f"Download failed: {remote_path}")
                    success = False
            except Exception as e:
                log_file.write(f"{datetime.now()} - Error processing {remote_path}: {str(e)}\n")
                print(f"Error processing {remote_path}: {str(e)}")
                success = False
    
    # Return to parent directory
    ftp.cwd('..')
    
    return success

def main() -> None:
    parser: argparse.ArgumentParser = argparse.ArgumentParser(description='Recursively download files from FTP server with optional deletion')
    parser.add_argument('-s', '--server', required=True, help='FTP server hostname')
    parser.add_argument('-u', '--user', required=True, help='FTP username')
    parser.add_argument('-p', '--password', required=True, help='FTP password')
    parser.add_argument('-r', '--remote-dir', default='/', help='Remote directory to start from')
    parser.add_argument('-l', '--local-dir', required=True, help='Local directory to save files')
    parser.add_argument('-d', '--delete-remote', action='store_true', help='Delete remote files after successful download (DESTRUCTIVE)')
    parser.add_argument('-f', '--flatten', action='store_true', help='Download all files to top-level directory, flattening directory structure')
    parser.add_argument('-n', '--no-log', action='store_true', help='Disable log file creation (no logging to file)')
    
    args: argparse.Namespace = parser.parse_args()
    
    # Ensure remote directory is absolute path
    if not args.remote_dir.startswith('/'):
        args.remote_dir = '/' + args.remote_dir
    
    # Ensure local directory exists
    ensure_local_dir(args.local_dir)
    
    # Track overall success
    overall_success = True
    
    # Open log file or null device
    log_file_path = os.devnull if args.no_log else 'ftp_sync.log'
    with open(log_file_path, 'a') as log_file:
        operation_mode: str = "download and delete" if args.delete_remote else "download only"
        structure_mode: str = " (flattened)" if args.flatten else ""
        log_file.write(f"\n{datetime.now()} - Starting FTP sync ({operation_mode}{structure_mode})\n")
        
        try:
            # Connect to FTP server
            ftp: ftplib.FTP = ftplib.FTP(args.server)
            ftp.login(args.user, args.password)
            
            log_file.write(f"{datetime.now()} - Connected to {args.server}\n")
            print(f"Connected to {args.server}")
            
            if args.delete_remote:
                print("⚠️ WARNING: Remote files will be DELETED after download!")
            else:
                print("ℹ️ Safe mode: Files will be downloaded but NOT deleted from remote server")
            
            if args.flatten:
                print("📁 Flatten mode: All files will be downloaded to the top-level directory")
            
            if args.no_log:
                print("🚫 No-log mode: File logging disabled")
            
            # Process directories recursively
            if not process_directory(ftp, args.remote_dir, args.local_dir, log_file, args.delete_remote, args.flatten):
                overall_success = False
            
            # Close connection
            ftp.quit()
            
            if overall_success:
                log_file.write(f"{datetime.now()} - FTP sync completed successfully ({operation_mode}{structure_mode})\n")
                print(f"FTP sync completed successfully ({operation_mode}{structure_mode})")
            else:
                log_file.write(f"{datetime.now()} - FTP sync completed with errors ({operation_mode}{structure_mode})\n")
                print(f"FTP sync completed with errors ({operation_mode}{structure_mode})")
            
        except Exception as e:
            log_file.write(f"{datetime.now()} - Error: {str(e)}\n")
            print(f"Error: {str(e)}")
            overall_success = False
    
    # Exit with appropriate code
    if overall_success:
        sys.exit(0)  # Success
    else:
        sys.exit(1)  # Failure

if __name__ == "__main__":
    main()
