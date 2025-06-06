#!/usr/bin/env python3

import os
import ftplib
import argparse
from datetime import datetime
from typing import TextIO, List

def ensure_local_dir(local_path: str) -> None:
    """Create local directory if it doesn't exist"""
    if not os.path.exists(local_path):
        os.makedirs(local_path)

def process_directory(ftp: ftplib.FTP, remote_dir: str, local_dir: str, log_file: TextIO, delete_remote: bool = False) -> None:
    """Recursively download and optionally delete files from remote directory"""
    print(f"Processing directory: {remote_dir}")
    
    # Change to remote directory
    ftp.cwd(remote_dir)
    
    # Create corresponding local directory
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
            
        remote_path: str = f"{remote_dir}/{file_name}" if remote_dir != '/' else f"/{file_name}"
        local_path: str = os.path.join(local_dir, file_name)
        
        # Check if it's a directory
        if item.startswith('d'):
            # Recursively process subdirectory
            process_directory(ftp, remote_path, local_path, log_file, delete_remote)
        else:
            # Download file
            try:
                with open(local_path, 'wb') as local_file:
                    ftp.retrbinary(f'RETR {file_name}', local_file.write)
                
                # Verify file was downloaded successfully
                if os.path.exists(local_path) and os.path.getsize(local_path) > 0:
                    if delete_remote:
                        # Delete remote file only if flag is set
                        ftp.delete(file_name)
                        log_file.write(f"{datetime.now()} - Downloaded and deleted: {remote_path}\n")
                        print(f"Downloaded and deleted: {remote_path}")
                    else:
                        log_file.write(f"{datetime.now()} - Downloaded: {remote_path}\n")
                        print(f"Downloaded: {remote_path}")
                else:
                    log_file.write(f"{datetime.now()} - Download failed: {remote_path}\n")
                    print(f"Download failed: {remote_path}")
            except Exception as e:
                log_file.write(f"{datetime.now()} - Error processing {remote_path}: {str(e)}\n")
                print(f"Error processing {remote_path}: {str(e)}")
    
    # Return to parent directory
    ftp.cwd('..')

def main() -> None:
    parser: argparse.ArgumentParser = argparse.ArgumentParser(description='Recursively download files from FTP server with optional deletion')
    parser.add_argument('--host', required=True, help='FTP server hostname')
    parser.add_argument('--user', required=True, help='FTP username')
    parser.add_argument('--password', required=True, help='FTP password')
    parser.add_argument('--remote-dir', default='/', help='Remote directory to start from')
    parser.add_argument('--local-dir', required=True, help='Local directory to save files')
    parser.add_argument('--log-file', default='ftp_sync.log', help='Log file path')
    parser.add_argument('--delete-remote', action='store_true', help='Delete remote files after successful download (DESTRUCTIVE)')
    
    args: argparse.Namespace = parser.parse_args()
    
    # Ensure local directory exists
    ensure_local_dir(args.local_dir)
    
    # Open log file
    with open(args.log_file, 'a') as log_file:
        operation_mode: str = "download and delete" if args.delete_remote else "download only"
        log_file.write(f"\n{datetime.now()} - Starting FTP sync ({operation_mode})\n")
        
        try:
            # Connect to FTP server
            ftp: ftplib.FTP = ftplib.FTP(args.host)
            ftp.login(args.user, args.password)
            
            log_file.write(f"{datetime.now()} - Connected to {args.host}\n")
            print(f"Connected to {args.host}")
            
            if args.delete_remote:
                print("⚠️  WARNING: Remote files will be DELETED after download!")
            else:
                print("ℹ️  Safe mode: Files will be downloaded but NOT deleted from remote server")
            
            # Process directories recursively
            process_directory(ftp, args.remote_dir, args.local_dir, log_file, args.delete_remote)
            
            # Close connection
            ftp.quit()
            log_file.write(f"{datetime.now()} - FTP sync completed successfully ({operation_mode})\n")
            print(f"FTP sync completed successfully ({operation_mode})")
            
        except Exception as e:
            log_file.write(f"{datetime.now()} - Error: {str(e)}\n")
            print(f"Error: {str(e)}")

if __name__ == "__main__":
    main()
