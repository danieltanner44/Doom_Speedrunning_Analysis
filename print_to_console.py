from tabulate import tabulate
from colorama import Fore, Back, Style

def print_to_console(input_list):
    # This function simply prints messages to terminal so that clutter is removed from the main loop
    output_str = input_list[0]
    match output_str:
        case "processing...":
            print_str, demo_filenames, filename, file_index = input_list
            if file_index == 0:
                print(f"\n\n{Fore.BLACK}{Back.BLUE}Performing Analysis on Demo Files{Style.RESET_ALL}")
                print(f"Found {len(demo_filenames)} demo files, processing ... \n")

            print(f"\n{Fore.BLACK}{Back.WHITE}Processing File: {file_index + 1} of {len(demo_filenames)}{Style.RESET_ALL}")
            print(f"Current file: {filename}")
        case "Unknown":
            demo_format_str, filename, demo_format_int = input_list
            print(f"{Fore.BLACK}{Back.YELLOW}WARNING: Skipping file {filename} as demo format {demo_format_int} is unknown\n{Style.RESET_ALL}")
        case "data sources":
            print_str, filename, demo_header_data, demo_movement_data, demo_footer_data, dsda_analysis_file_data, dsda_text_file_data, dsda_levelstat_file, collected_demo_data = input_list
            print("=============================================================")
            print(f"Data extracted from Demo file: {filename}")
            print(f"Demo Header Data: {demo_header_data}")
            # If there is loads of movement data just show preview of first 10 elements
            if len(demo_movement_data) > 10:
                preview_demo_movement_data = {key: demo_movement_data[key] for key in list(demo_movement_data)[:10]}
                print(f"Demo Movement Data (preview): {preview_demo_movement_data}...")
            else:
                print(f"Demo Movement Data: {demo_movement_data}")
            print(f"Demo Footer Data: {demo_footer_data}")
            print("=============================================================")
            print(f"Data extracted from dsda-doom analysis file: ")
            print(f"Dsda-Doom Analysis File Data: {dsda_analysis_file_data}")
            print(f"Dsda-Doom Text File Data: {dsda_text_file_data}")
            print(f"Dsda-Doom Levelstat File Data: {dsda_levelstat_file}")
            print("=============================================================")
            print(f"Collated data from demo captured in dataframe: ")
            print(f"Dataframe: {collected_demo_data}\n")
        case "master dataframe":
            output_str, master_dataframe_file_location, master_demo_data = input_list
            print(f"\n{Fore.BLACK}{Back.BLUE}The master dataframe has been created and saved to: {Style.RESET_ALL}")
            print(f"{master_dataframe_file_location}")
            print(f"The master dataframe looks like: ")
            print(tabulate(master_demo_data, headers='keys', tablefmt='psql') + "\n")

        case "metadata":
            output_str, metadata = input_list
            print(f"The metadata for the master data is: {metadata}")
        case _:
            print(f"Error: List has unexpected number of elements")
    return