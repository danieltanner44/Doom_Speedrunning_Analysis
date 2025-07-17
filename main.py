# Created by Improvers Gaming on 17th July 2025
# Doomworld: https://www.doomworld.com/profile/37082-improversgaming/
# YouTube: www.youtube.com/@improversgaming

# From General Libraries
import time
import xarray
# From Developed Project Files
from create_display_dashboard import create_display_dashboard
from read_demo_file import read_demo_file
from create_demo_structure import create_demo_structure
from perform_dsda_doom_analysis import perform_dsda_doom_analysis
from find_files import find_demo_files
from manage_core_data import create_dataframe_for_demo
from manage_core_data import store_master_data_to_hdf5
from find_files import get_directory
from print_to_console import print_to_console


'''
Current Limitations:
 - Single player
 - Single map demo (not movies)
 - Reads demo files in Boom 2.02 and Doom 1.9 format only

Desirable Considerations for Future Work:
 - Check that required WAD is in dsda-doom folder (for -timedemo)
 - Add support for master data store not found
 - Create an automation for sensible initial filters for dashboard
 - Consider other data to store: etc.
 - Restructure code to promote better architecture
 - Optimise and check how much processing of incomplete runs
    - Parsing the movement data has no known benefit
 - Rebuild visualisation of data to be:
    - filterable from the dashboard
    - dynamically updated with filter change
 - Add documentation and code comments
 - Upload to GitHub
 - Consider whether adding new metrics would be useful
    - Calculate overall playtime by including incomplete demo time
'''

if __name__ == '__main__':
    # =================================================================================
    # ===============       USER SETS THESE BEFORE RUNNING SCRIPT       ===============
    # =================================================================================
    # Main user settings
    # Set both to True to process demo files and display dashboard
    # Set only display_dashboard to True to read previous data file and display
    perform_analysis = True     # Set True to process demo files or False to skip
    display_dashboard = True     # Set True to show load datastore or False to skip

    # Choose the settings to filter the data for the Dashboard (case-sensitive!!!)
    WAD_filter = "D5DA5"  # Enter WAD Filter, e.g., "Doom", "Doom II", "Scythe", "D5DA5"
    map_filter = "MAP32"  # Enter Map Filter, e.g., "Map01", "E1M1"
    category_filter = "UV Max"  # Enter Category Filter, e.g., "UV Speed", "NoMo", etc.
    # The reset time threshold sets the time to determine if a demo was quickly reset

    # Often Quickstart Cache adds attempts that are not valid, this takes them out
    reset_time_threshold = 2    # Set in seconds
    # =================================================================================
    # ========================       END OF USER SETTINGS       =======================
    # =================================================================================

    # Capture the time require to run script, added to master data store metadata
    start_time = time.time()
    dialog_title = 'Select Folder of Demo Files to Analyse'
    demo_directory_name = get_directory(dialog_title)
    dialog_title = 'Select Folder with dsda-doom Executable'
    dsda_doom_directory = get_directory(dialog_title)

    if perform_analysis:
        # Identify demo files
        demo_filenames = find_demo_files(demo_directory_name)

        # Loop over demo files and process them
        for file_index, filename in enumerate(demo_filenames):

            # Print details of current file being processed
            print_to_console(["processing...", demo_filenames, filename, file_index])

            # Read all data from demo file
            demo_file_bytes, demo_file_ints, demo_format_int, demo_format_str, data_address_locations, file_modification_date, file_modification_time = read_demo_file(demo_directory_name, filename)

            # If demo format is unknown then warn and skip to next file
            if demo_format_str == "Unknown":
                print_to_console([demo_format_str, filename, demo_format_int])
                continue

            # Parse data from demo file for header, movement and footer
            demo_header_data, demo_movement_data, demo_footer_data, demo_movement_time = create_demo_structure(demo_file_bytes, demo_file_ints, demo_format_str, data_address_locations)

            # Undertake analysis with dsda-doom -analysis, -export_text_file and -levelstat
            # Parse all data from these three files
            dsda_analysis_file_data, dsda_text_file_data, dsda_levelstat_file = perform_dsda_doom_analysis(file_index, demo_directory_name, filename, dsda_doom_directory)

            # Create dataframe for demo file - pulling data from demo and analysis files
            collected_demo_data = create_dataframe_for_demo(filename, demo_header_data, demo_footer_data,
                                                            demo_movement_time, dsda_analysis_file_data,
                                                            dsda_text_file_data, dsda_levelstat_file,
                                                            file_modification_date, file_modification_time)

            # Compile each demo dataframe into a master dataframe of all demos
            if file_index == 0:
                master_demo_data = collected_demo_data
            else:
                for key in master_demo_data.keys():
                    master_demo_data[key].extend(collected_demo_data[key])

            # Print details of all data sources, namely: demo (header, movement, footer),
            # analysis files (analysis, text file and levelstat) and demo dataframe
            print_to_console(["data sources", filename, demo_header_data, demo_movement_data, demo_footer_data,
                      dsda_analysis_file_data, dsda_text_file_data, dsda_levelstat_file, collected_demo_data])

        # Store the master dataframe to file in hdf5 format
        # Create and store metafile with it that captures general information about dataframe
        master_dataframe_file_location = store_master_data_to_hdf5(master_demo_data, start_time, demo_directory_name)

        # Print metadata details for master dataframe
        print_to_console(["master dataframe", master_dataframe_file_location, master_demo_data])

    if display_dashboard:
        # Create file string to stored master data
        # Open master data and retrieve metadata
        master_dataframe_file_location = demo_directory_name + "\\" + "speedrunning_analysis.hdf5"
        master_demo_data = xarray.open_dataset(master_dataframe_file_location)
        metadata = master_demo_data.attrs['Metadata']

        # Print metadata details for master data
        print_to_console(["metadata", metadata])

        # Convert master data back to dataframe
        master_demo_data = master_demo_data.to_dataframe()

        create_display_dashboard(master_demo_data, WAD_filter, map_filter, category_filter, reset_time_threshold)