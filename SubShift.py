import os
import re
import sys
from datetime import timedelta

# Regular expressions for different subtitle formats
ass_pattern = r'(\d+:\d+:\d+\.\d{2})'  # for .ass files (e.g., 0:00:20.00)
srt_vtt_pattern = r'(\d{2}:\d{2}:\d{2},\d{3})'  # for .srt and .vtt files (e.g., 00:00:20,500)

def shift_time_Dot_Format(time_str, shift_seconds):
    """Shift time in 'hours:minutes:seconds.milliseconds' format for .ass files."""
    time_parts = time_str.split(':')  # Split the time string by ':'
    # Handle cases with hours, minutes, and seconds properly
    Hours = int(time_parts[0])
    Minutes = int(time_parts[1])
    # Separate seconds and milliseconds
    Seconds, Milliseconds = map(float, time_parts[2].split('.'))
    # print(Seconds,'  ',Milliseconds)
    print(shift_seconds)
    original_time = timedelta(hours=Hours, minutes=Minutes, seconds=Seconds, milliseconds=Milliseconds*10)
    shifted_time = original_time + timedelta(seconds=shift_seconds)
    total_seconds = shifted_time.total_seconds()
    hours = int(total_seconds // 3600)
    minutes = int((total_seconds % 3600) // 60)
    seconds = total_seconds % 60  # Keep seconds as float for decimal
    return f"{hours}:{minutes:02d}:{seconds:.2f}"


def shift_time_Comma_Format(time_str, shift_seconds):
    """Shift time in 'hours:minutes:seconds,milliseconds' format for .srt and .vtt files."""
    hours, minutes, seconds = time_str.split(':')
    
    # Split seconds and milliseconds correctly (e.g., 00:00:20,500 -> 20,500)
    seconds, milliseconds = seconds.split(',')
    
    # Create a timedelta object
    original_time = timedelta(hours=int(hours), minutes=int(minutes), seconds=int(seconds), milliseconds=int(milliseconds))
    
    # Add the shift time
    shifted_time = original_time + timedelta(seconds=shift_seconds)
    
    # Calculate milliseconds from microseconds
    milliseconds = int(shifted_time.microseconds / 1000)
    
    # Return the updated time in the same format
    return f'{str(shifted_time.seconds // 3600).zfill(2)}:{str((shifted_time.seconds % 3600) // 60).zfill(2)}:{str(shifted_time.seconds % 60).zfill(2)},{str(milliseconds).zfill(3)}'


def process_file(file_path, shift_seconds):
    """Process a single file and shift its times."""
    if file_path.endswith(('.ass', '.ssa')):
        time_pattern = ass_pattern
        shift_function = shift_time_Dot_Format
    elif file_path.endswith(('.srt', '.vtt', '.sub', '.sbv', '.lrc')):
        time_pattern = srt_vtt_pattern
        shift_function = shift_time_Comma_Format
    else:
        print(f"Skipping {file_path}: Unsupported file format.")
        return

    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()

    # Apply the time shifting
    shifted_content = re.sub(time_pattern, lambda match: shift_function(match.group(0), shift_seconds), content)

    # Save the shifted content back to the file
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(shifted_content)
        print(f"timestamp shifted sccessfully in file '{file_path}'")

def process_folder(folder_path, shift_seconds):
    """Process all valid files in the folder and its subfolders."""
    for root, _, files in os.walk(folder_path):
        for file in files:
            if file.endswith(('.ass', '.ssa', '.srt', '.vtt', '.sub', '.sbv', '.lrc')):
                process_file(os.path.join(root, file), shift_seconds)


def get_time(time_str):
    # If string just contains a decimal number (like "66.7" or "-66.7")
    if all(c in "0123456789.-" for c in time_str):
        return float(time_str)
    
    # Handle negative times
    negative = time_str.startswith('-')
    if negative:
        time_str = time_str[1:]
    
    # Replace comma with dot for milliseconds format
    time_str = time_str.replace(',', '.')
    
    try:
        # Split by colon
        parts = time_str.split(':')
        
        if len(parts) == 3:  # Format: "HH:MM:SS.ss" or "HH:MM:SS,sss"
            hours = int(parts[0])
            minutes = int(parts[1])
            seconds = float(parts[2])
            total_seconds = hours * 3600 + minutes * 60 + seconds
            
        elif len(parts) == 2:  # Format: "MM:SS.ss"
            minutes = int(parts[0])
            seconds = float(parts[1])
            total_seconds = minutes * 60 + seconds
            
        else:  # Assume it's just seconds if no colons
            total_seconds = float(time_str)
        
        return -total_seconds if negative else total_seconds
    
    except ValueError:
        raise ValueError(f"Invalid time format: {time_str}")


def main():
    if len(sys.argv) != 3:
        print("Usage: python SubShift.py <file_or_folder_path> <shift_seconds>")
        return

    path = sys.argv[1]
    shift_seconds = get_time(sys.argv[2])

    if os.path.isfile(path):
        process_file(path, shift_seconds)
    elif os.path.isdir(path):
        process_folder(path, shift_seconds)
    else:
        print(f"{path} is not a valid file or folder.")

if __name__ == '__main__':
    main()
