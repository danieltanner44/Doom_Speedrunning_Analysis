import os
import subprocess
import shutil
from print_to_console import print_to_console

def perform_dsda_doom_analysis(file_index, directory_name, filename, dsda_doom_directory, iWAD, pWAD):
    # This function executes dsda-doom analysis on each demo file
    # It then parses all data from the output files produced
    current_demo_file = directory_name + "\\" + filename
    # For the first analysis allow the graphics to play as a check that WAD is loaded correctly
    # Notes:
    # -nosound -nodraw allow dsda-doom to play the demo in the background
    # -timedemo allows dsda-doom to play the demo as quickly as possible

    # Check that the required WAD files are available to dsda-doom
    # If they are not the demo will still play back but the outcome will be wrong
    if pWAD is not None:
        pWAD_file = dsda_doom_directory + "\\" + pWAD
        check = shutil.which(pWAD_file)
        if check is None:
            print_to_console(["pWAD missing", pWAD])
            return None, None, None
    if iWAD is not None:
        iWAD_file = dsda_doom_directory + "\\" + iWAD
        check = shutil.which(iWAD_file)
        if check is None:
            print_to_console(["iWAD missing", pWAD])
            return None, None, None

    # Replace -timedemo with -playdemo (and omit -nosound and -nodraw) if you wish to watch the demos in realtime
    if file_index == 0:
        dsda_executable_file = "dsda-doom -nosound -timedemo " + current_demo_file + " -analysis -levelstat -export_text_file"
    else:
        dsda_executable_file = "dsda-doom -nodraw -nosound -timedemo " + current_demo_file + " -analysis -levelstat -export_text_file"
    os.chdir(dsda_doom_directory)
    print(f"Executing: {dsda_executable_file} From directory: {os.getcwd()}")
    # Call the dsda-analysis as a subprocess to avoid it dumping its output into the terminal
    with open(os.devnull, "w") as dump:
        subprocess.call(dsda_executable_file, stdout=dump)

    # Now read each of the three dsda-doom output files
    # Read analysis file and convert to dictionary
    dsda_analysis_file = dsda_doom_directory + "\\" + "analysis.txt"
    dsda_analysis_file_data = {}
    with open(dsda_analysis_file, "r") as f:
        # Read the analysis file
        while line := f.readline():
            line = line.strip().split(" ")
            if len(line) == 2:
                key, value = line
                dsda_analysis_file_data[key] = value
            elif len(line) == 3:
                key = line[0]
                value = " ".join(line[1:3])
                dsda_analysis_file_data[key] = value

    # Read text file and convert to dictionary
    dsda_text_file = directory_name + "\\" + filename[:-4] + ".txt"
    dsda_text_file_data = {}
    with open(dsda_text_file, "r") as f:
        # Read the text file - skipping the first three lines
        for _ in range(3):
            next(f)
        while line := f.readline():
            line = line.split(":",1)
            for index, element in enumerate(line):
                line[index] = line[index].strip()
            if len(line) > 1:
                dsda_text_file_data[line[0]] = line[1]

    # Read levelstat file and convert to dictionary
    # File only present if the map was complete (exit achieved)
    # The file may be present but from a different demo so need to check
    if dsda_text_file_data["Time"] != "0:00":
        dsda_levelstat_file = dsda_doom_directory + "\\" + "levelstat.txt"
        dsda_levelstat_file_data = {}
        with open(dsda_levelstat_file, "r") as f:
            line = f.readline()
            # MAP32 - 1:23.09 (1:23)  K: 1854/1854  I: 43/138  S: 0/0
            line = line.strip().replace("(","").replace(")","").replace(".",":").split(" ")
            dsda_levelstat_file_data["Map"] = line[0].strip()
            dsda_levelstat_file_data["Time"] = line[2].strip()
            for index, element in enumerate(line):
                match element:
                    case "K:":
                        dsda_levelstat_file_data["Map K"] = line[index + 1].strip().split("/")[0]
                        dsda_levelstat_file_data["Num K"] = line[index + 1].strip().split("/")[1]
                    case "I:":
                        dsda_levelstat_file_data["Map I"] = line[index + 1].strip().split("/")[0]
                        dsda_levelstat_file_data["Num I"] = line[index + 1].strip().split("/")[1]
                    case "S:":
                        dsda_levelstat_file_data["Map S"] = line[index + 1].strip().split("/")[0]
                        dsda_levelstat_file_data["Num S"] = line[index + 1].strip().split("/")[1]
    else:
        dsda_levelstat_file_data = None
    return dsda_analysis_file_data, dsda_text_file_data, dsda_levelstat_file_data