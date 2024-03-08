import os
import sys
import shutil
import hashlib
import time

def calculate_md5(file_path):
    md5_hash = hashlib.md5()
    with open(file_path, "rb") as file:
        # Read and update hash string value in blocks
        for byte_block in iter(lambda: file.read(4096), b""):
            md5_hash.update(byte_block)
    return md5_hash.hexdigest()

def current_time():
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

def synchronize_folders(source_dir, backup_dir, log_file):            
    # Create backup directory if it does not exist
    if not os.path.exists(backup_dir):
        os.makedirs(backup_dir)

    # Get list of files in the source directory
    source_files = []
    for item in os.listdir(source_dir):
        if os.path.isfile(os.path.join(source_dir, item)):
            source_files.append(item)


    # Get list of files in the backup directory
    backup_files = []
    for item in os.listdir(backup_dir):
        if os.path.isfile(os.path.join(backup_dir, item)):
            backup_files.append(item)

    # Dictionary to store MD5 hashes of source files
    source_hashes = {}

    # Calculate MD5 hashes for files in the source directory
    for file_name in source_files:
        file_path = os.path.join(source_dir, file_name)
        source_hashes[file_name] = calculate_md5(file_path)

    # Synchronize files from source to backup
    for file_name, md5_hash in source_hashes.items():
        source_file_path = os.path.join(source_dir, file_name)
        backup_file_path = os.path.join(backup_dir, file_name)

        if file_name not in backup_files:
            # Copy file from source to backup
            shutil.copy2(source_file_path, backup_file_path)
            # Log file creation
            with open(log_file, 'a') as log:
                timestamp = current_time()
                log.write(f"<{timestamp}> File created: {file_name}\n")
            print(f"<{timestamp}> File created: {file_name}")
        
        elif source_hashes[file_name] != calculate_md5(backup_file_path):
            # Copy file from source to backup
            shutil.copy2(source_file_path, backup_file_path)
            # Log file copying
            with open(log_file, 'a') as log:
                timestamp = current_time()
                log.write(f"<{timestamp}> File copied: {file_name}\n")
            print(f"<{timestamp}> File copied: {file_name}")

    # Remove files from backup if they are not in source
    for file_name in backup_files:
        backup_file_path = os.path.join(backup_dir, file_name)
        if file_name not in source_files:
            os.remove(backup_file_path)
            # Log file removal
            with open(log_file, 'a') as log:
                timestamp = current_time()
                log.write(f"<{timestamp}> File removed: {file_name}\n")
            print(f"<{timestamp}> File removed: {file_name}")

if __name__ == "__main__":
    if len(sys.argv) != 5:
        print("Start the script with these parameters:\n python folder_backup.py <source directory path> <backup directory path> <backup period in seconds> <log file path>")
        sys.exit(1)

    source_dir = sys.argv[1]
    backup_dir = sys.argv[2]
    interval_seconds = int(sys.argv[3])
    log_file = sys.argv[4]

    # Check if the source directory exists
    if not os.path.exists(source_dir):
        print(f"The source directory does not exist!\n{source_dir}")
        sys.exit(1)
    
    print(f"Synchronization of these folders is done:\n{source_dir}\n{backup_dir}\n")
    while True:
        synchronize_folders(source_dir, backup_dir, log_file)
        timestamp = current_time()
        print(f"<{timestamp}> Synchronization done")
        time.sleep(interval_seconds)