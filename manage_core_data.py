import pandas as pd
from datetime import datetime
import time
import xarray

def parse_time_str_to_seconds(time_str):
    # This functions takes a time string in format HH:MM:SS:TH
    # And converts it to seconds
    time_data = time_str.strip().replace(".",":").split(":")
    if len(time_data) == 2: #ss, ht
        run_time_s = float(time_data[0]) + (float(time_data[1])/100)
    elif len(time_data) == 3: #mm, ss, ht
        run_time_s = float(time_data[0]) * 60 + float(time_data[1]) + (float(time_data[2])/100)
    elif len(time_data) == 4: #hh, mm, ss, th
        run_time_s = float(time_data[0]) * 3600 + float(time_data[0]) * 60 + float(time_data[1]) + (float(time_data[3])/100)
    else:
        print(f"Warning: time format unknown for {time_str}")
    return run_time_s

def create_dataframe_for_demo(filename, demo_header_data, demo_footer_data,
                            demo_movement_time, dsda_analysis_file_data,
                            dsda_text_file_data, dsda_levelstat_file,
                            file_modification_date, file_modification_time):
    # Determine if the demo had a successful exit
    # If so the dsda_text_file_data will have a time set that is not 0:00
    if dsda_text_file_data["Time"] == "0:00":
        complete = "N"
        time_str = 'N/A'
        # Record the demo movement time as this can be used to determine
        # if failed attempt was a quick reset at start
        run_time_s = round(demo_movement_time, 2)
    else:
        complete = "Y"
        time_str = dsda_text_file_data["Time"]
        # As a time was recorded in the dsda text file parse it to seconds
        # This makes comparisons later easier
        run_time_s = parse_time_str_to_seconds(dsda_text_file_data["Time"])

    # Determine WAD name, which is either a Pwad
    # or one of the original game wads
    try:
        # First look for a pWAD - is it listed in the text file?
        wad_name = dsda_text_file_data["Pwad"][:-4]
        if complete == "Y":
            # If complete the map_string is always defined
            map_name = dsda_levelstat_file["Map"]
        elif complete == "N":
            # If incomplete then the map is encoded by a movie key
            map_name = dsda_text_file_data["Movie"].split()[0]
    except:
        # If it is not a pWAD then it is an original game iWAD
        if complete == "Y":
            # If complete the map_string is always defined
            map_string = dsda_levelstat_file["Map"]
        elif complete == "N":
            # If incomplete then the map is encoded by a movie key
            map_string = dsda_text_file_data["Movie"].split()[0]

        # Now finalise WAD and Map ID based on the map id
        if map_string[0] == "E" and map_string[2] == "M":
            wad_name = "Doom"
            map_name = map_string
        elif map_string[:3] == "MAP":
            wad_name = "Doom II"
            map_name = map_string

    # Add miscellaneous data
    skill_level = demo_header_data["Skill Level"] + 1
    port_used = demo_footer_data["Port"]
    category = dsda_analysis_file_data["category"]
    complevel_str_list = dsda_text_file_data["Exe"].split(" ")
    complevel = complevel_str_list[complevel_str_list.index("-complevel") + 1]

    # Set data to be stored to master data store
    collected_demo_data = {"filename": [filename],
                           "WAD": [wad_name],
                           "Map": [map_name],
                           "Skill": [skill_level],
                           "Complete": [complete],
                           "Category": [category],
                           "Port": [port_used],
                           "Time": [run_time_s],
                           "Time (str)": [time_str],
                           "Complevel": [complevel],
                           "Demo Date": [file_modification_date],
                           "Demo Time": [file_modification_time],
    }
    return collected_demo_data

def store_master_data_to_hdf5(master_demo_data, start_time, demo_directory_name, version, release_status):
    # This function stores the master data (for all demos) to hdf5 file
    # Create the master dataframe of all demo runs
    master_demo_data = pd.DataFrame(master_demo_data)

    # Add metadata to dataframe
    current_date, current_time = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S').split(" ")
    end_time = time.time()
    processing_time = int(end_time - start_time)
    metadata = f"Date: {current_date}, Time: {current_time}, Version: {version}, Status: {release_status}, Processing Time: {processing_time}"

    # Add metadata to xarray
    master_demo_data = xarray.Dataset.from_dataframe(master_demo_data)
    master_demo_data.attrs['Metadata'] = metadata

    # Save the dataframe to file
    master_dataframe_file_location = demo_directory_name + "\\" + "speedrunning_analysis.hdf5"
    master_demo_data.to_netcdf(master_dataframe_file_location)
    return master_dataframe_file_location