import os
import time
from datetime import datetime
from print_to_console import print_to_console

def check_demo_format_support(demo_format_int):
    # Check is demo format supported
    match demo_format_int[-1]:
        case 109:
            demo_format_str = "Doom"
            movement_data_start_address = 14
            if demo_format_int[0] == 255:
                movement_data_start_address += 27
        case 202:
            demo_format_str = "Boom"
            movement_data_start_address = 110
            if demo_format_int[0] == 255:
                movement_data_start_address += 27
        case 203:
            demo_format_str = "MBF"
            movement_data_start_address = 114
        case 255: # Has umapinfo
            demo_format_str = "UMAPINFO"
            movement_data_start_address = None
        case 128:
            # Where only the footer is captured no header or movement data
            demo_format_str = "Demo format invalid"
            movement_data_start_address = 0
        case _:
            demo_format_str = "Demo format unknown"
            movement_data_start_address = 0
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
    demo_format_int = []
    with open(current_demo_file, "rb") as f:
        # Read the demo format from the first byte
        byte = f.read(1)
        demo_file_bytes.append(byte)
        demo_file_ints.append(int.from_bytes(byte))
        demo_format_int.append(demo_file_ints[0])

        # Read the rest of the bytes from the whole demo file
        # Also store as signed integers
        while (byte := f.read(1)):
            demo_file_bytes.append(byte)
            demo_file_ints.append(int.from_bytes(byte, signed=True))

    if demo_format_int[0] == 255:
        demo_format_int.append(int.from_bytes(demo_file_bytes[27]))

    # Find the initial header address locations and demo format str
    demo_format_str, movement_data_start_address = check_demo_format_support(demo_format_int)
    if demo_format_str == "Demo format invalid":
        print_to_console(["Demo format invalid"])
        return None, None, None, None, None, None, None
    elif demo_format_str == "Demo format unknown":
        print_to_console(["Demo format unknown", filename, demo_format_int])
        return None, None, None, None, None, None, None
    else:
        print_to_console(["Demo format", demo_format_str, demo_format_int])

    # Now scan the read bytes for key address locations
    # Set the demo header address location range
    data_address_locations = [0, movement_data_start_address]

    # Now find the address locations for the movement data and footer
    end_movement_byte = False
    for address, each_byte in enumerate(demo_file_bytes):
        # End of movement data encoded by 0x80
        # Carriage returns in footer encoded by 0x0A
        # Skip the header as it may have a 0x80 for other purposes
        if each_byte[0] == 0x80 and address >= data_address_locations[1] - 1:
            data_address_locations.append(address + 1)
            end_movement_byte = True
        # Only look for the end of carriage characters after the movement data block as
        # the movement data block can have this character as it decodes via "utf-8" to "3"
        # Add each byte that denotes a new line in the footer
        elif each_byte[0] == 0x0A and end_movement_byte:
            data_address_locations.append(address + 1)

    return demo_file_bytes, demo_file_ints, demo_format_int[-1], demo_format_str, data_address_locations, file_modification_date, file_modification_time