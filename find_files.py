import os
import tkinter as tk
from tkinter import filedialog

def get_directory(dialog_title):
    # This function creates a dialog box to allow the user to select
    # the directories needed for processing demos
    root = tk.Tk()
    root.withdraw()
    selected_directory = filedialog.askdirectory(title=dialog_title)
    return selected_directory

def find_demo_files(demo_directory_name):
    # This function returns the filenames of all demos in the target directory
    # Find all files in target directory
    all_files = os.listdir(demo_directory_name)

    # Sort filenames by their creation data
    # Needed as successful times have different name format
    file_modification_times = {}
    for file in all_files:
        full_file_path = demo_directory_name + "\\" + file
        file_modification_times[file] = os.path.getmtime(full_file_path)
    sorted_demo_files = dict(sorted(file_modification_times.items(), key=lambda item: item[1]))
    # Finalise set of names of demo files
    demo_filenames = []
    for file in sorted_demo_files.keys():
        if file.endswith(".lmp"):
            demo_filenames.append(file)
    return demo_filenames