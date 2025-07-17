def create_demo_structure(demo_file_bytes, demo_file_ints, demo_format_str, data_address_locations):
    # Construct demo header based on bytes read from file
    match demo_format_str:
        case "Doom 1.9":
            # Create the header based on known structure
            demo_header_data = {"Demo Format": demo_file_ints[0],
                           "Skill Level": demo_file_ints[1],
                           "Episode": demo_file_ints[2],
                           "Map": demo_file_ints[3],
                           "Multiplayer Mode": demo_file_ints[4],
                           "Respawn": demo_file_ints[5],
                           "Fast": demo_file_ints[6],
                           "Nomonsters": demo_file_ints[7],
                           "Player POV": demo_file_ints[8],
                           "Green Player Playing": demo_file_ints[9],
                           "Indigo Player Playing": demo_file_ints[10],
                           "Brown Player Playing": demo_file_ints[11],
                           "Red Player Playing": demo_file_ints[12],
                           }

        case "Boom 2.02":
            # Create the header based on known structure
            demo_header_data = {"Demo Format": demo_file_ints[0],
                           "Skill Level": demo_file_ints[8],
                           "Episode": demo_file_ints[9],
                           "Map": demo_file_ints[10],
                           "Multiplayer Mode": demo_file_ints[11],
                           "Respawn": demo_file_ints[12],
                           "Fast": demo_file_ints[13],
                           "Nomonsters": demo_file_ints[14],
                           "Player POV": demo_file_ints[15],
                           "Green Player Playing": demo_file_ints[16],
                           "Indigo Player Playing": demo_file_ints[17],
                           "Brown Player Playing": demo_file_ints[18],
                           "Red Player Playing": demo_file_ints[19],
                           }

    # Create the movement data structure
    # Each movement tic has four bytes: forward/backward, right/left, turn, action/use/weapon change
    four = range(4)
    # The first time stamp is: 0.02857 or 0.03
    tic = 1
    demo_movement_data = {}
    for index in range(data_address_locations[2] - data_address_locations[1]):
        if index % 4 == 0:
            addresses = [i + index + data_address_locations[1] - 1 for i in four]
            demo_movement_data[tic] = [demo_file_ints[x] for x in addresses]
            tic += 1
    demo_movement_time = len(demo_movement_data) / 35

    # Create the footer data structure
    # Each line in the footer is separated by a carriage return
    num_lines = len(data_address_locations) - 3
    footer_lines = []
    for line_index in range(num_lines):
        line = []
        for byte_index in range(data_address_locations[2 + line_index], data_address_locations[3 + line_index] - 1):
            try:
                string = str(demo_file_bytes[byte_index], encoding="utf-8")
                line.append(string)
            except:
                pass
        line = ("".join(line).strip())
        footer_lines.append(line)

    demo_footer_data = {"Features": footer_lines[-4], "Port": footer_lines[-2], "Parameters": footer_lines[-1]}
    return demo_header_data, demo_movement_data, demo_footer_data, demo_movement_time