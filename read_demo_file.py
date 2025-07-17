import os
import time
from datetime import datetime

def check_demo_format_support(demo_format_int):
    # Check is demo format supported
    supported_demo_formats = ["Doom 1.9", "Boom 2.02"]
    match demo_format_int:
        case 109:
            demo_format_str = "Doom 1.9"
            movement_data_start_address = 14
        case 202:
            demo_format_str = "Boom 2.02"
            movement_data_start_address = 110
        case _:
            demo_format_str = "Unknown"
            movement_data_start_address = 0

    print(f"The demo format is: {demo_format_str}")
    if demo_format_str not in supported_demo_formats:
        print(f"SKIPPING: Unfortunately this demo format is not currently supported\n")
    return demo_format_str, movement_data_start_address


def read_demo_file(directory_name, filename):
    # Read the raw demo file data
    current_demo_file = directory_name + "\\" + filename

    # Read the file modification date and time
    file_modification_info = datetime.strptime(time.ctime(os.path.getmtime(current_demo_file)),"%a %b %d %H:%M:%S %Y")
    file_modification_date, file_modification_time = str(file_modification_info).split(" ")

    # Read all of the demo file bytes
    demo_file_bytes = []
    demo_file_ints = []
    with open(current_demo_file, "rb") as f:
        # Read the demo format from the first byte
        byte = f.read(1)
        demo_file_bytes.append(byte)
        demo_file_ints.append(int.from_bytes(byte))
        demo_format_int = demo_file_ints[0]

        # Find the initial header address locations and demo format str
        demo_format_str, movement_data_start_address = check_demo_format_support(demo_format_int)

        # Read the rest of the bytes from the whole demo file
        # Also store as signed integers
        while (byte := f.read(1)):
            demo_file_bytes.append(byte)
            demo_file_ints.append(int.from_bytes(byte, signed=True))

    # Now scan the read bytes for key address locations
    # Set the demo header address location range
    data_address_locations = [0, movement_data_start_address]

    # Now find the address locations for the movement data and footer
    end_movement_byte = False
    for address, each_byte in enumerate(demo_file_bytes):
        # End of movement data encoded by 0x80
        # Carriage returns in footer encoded by 0x0A
        if each_byte[0] == 0x80:
            # Once found add byte address to denote end of movement data
            data_address_locations.append(address + 1)
            end_movement_byte = True
        # Only look for the end of carriage characters after the movement data block as
        # the movement data block can have this character as it decodes via "utf-8" to "3"
        # Add each byte that denotes a new line in the footer
        elif each_byte[0] == 0x0A and end_movement_byte:
            data_address_locations.append(address + 1)

    return demo_file_bytes, demo_file_ints, demo_format_int, demo_format_str, data_address_locations, file_modification_date, file_modification_time