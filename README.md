# What is this programme
It is called **Doom Speedrunning Analysis** and is a set of Python functions that read a selection of Doom and Doom II demo files and analyse them. The analysis is based on reading of the demo files themselves and as well as collecting analysis data produced by dsda-doom.

This programme requires dsda-doom. It is recommended to use the latest release (so later than 0.29.0)

# What do I need to do to use it:
## Caveat Lector - Be Aware of the Risks:
The author is a NOOB programmer. This is a fun / hobbiest interest to combine things I enjoy - Doom and learning to programme. This is ***not*** a professional project and comes with associated risks. Please do not use this directly on irreplaceable demos. Create a directory and copy in some demos. Use this to try the programme and understand more about what it does. I accept no responsibility for lost or damage resulting for the use of this program.

## To execute the code:
1) Ensure that dsda-doom is installed
2) Install the required libraries, which are imported
3) Edit main.py to enter settings as described
4) Execute main.py with Python version 3 or later
5) This opens a dialog to enable you to select:
   + The directory with the demo files (lmp) you wish to analyse
   + The directory with the dsda-doom executable
6) The dashboard will be displayed.

# So what does the code do exactly?
- Finds all demo files in a directory that is specified
- Loops over each file and:
  - Parses all data from the demo (header, movement and footer - currently supports Doom 1.9 and Boom 2.02)
  - Undertakes analysis (-analysis) and text file export (-export_text_file) on demo file using dsda-doom
  - Parses all data from the analysis and exported text files
  - Stores key data of interest from each demo to a dataframe
- Stores the dataframe for all demos (and associated metadata) to file (hdf5)
- Analyses and plots data to a dashboard
  - You can slice the dataframe in many ways to display the data you are interested in

# What does the dashboard look like?
I ran D5DA5 Map32 over 4,000 times to try a﻿nd achieve my target of sub 1m20s. I finally did and produced this dashboard using these scripts:
<details open>
<summary>Image of Dashboard</summary>
<IMG src=/D5DA5_Map32-Dashboard.png>
</details>

The console output from Python produce during the generation of this dashboard look like this:
<details>
<summary>Image of Console Output</summary>
  <IMG src=/D5DA5_Map32-Output.png>
</details>

The stored dataframe looks like this:
<details>
<summary>Image of Stored Dataframe</summary>
  <IMG src=/D5DA5_Map32-Dataframe.png>
</details>

# What does all the data in the dashboard represent?
The dashboard title captures the Wad and Map of the demos that the data is extracted from. The data is displayed on three rows:
## 1) Speedrunning times progression (top):
This is a plot of successful completion time (y-axis) plotted in chronological order (x-axis – first to last successful run).  This aims to answer: Over the course of all my (successful) attempts how much has my time been improving?
Some more features:
+ A moving average is superimposed (the window size used is in the legend)
+ The text shows the improvement from the max to min of the moving average
 
## 2a) Attempts overview (middle-left): 
A pie chart of the distribution of attempts for the given wad and map. The names are: successful – exited the map; failed – no map exit achieved; reset – short demos representing resets for quick cache (maps where the movement data was < specified number of seconds). This aims to answer: How many real attempts have I made? How many were successful and how many failed?

## 2b) Category overview (middle-right):
A pie chart of the distribution of categories for successful attempts on the given wad and map
This aims to answer: How many successful runs have I had in different categories for a given wad and map? Do I preference one category over another?

## 3) Histogram of speedrunning times (bottom):
A histogram of the successful completion times for the given wad, map and for the given category. 
This aims to answers: How distributed are my completion times on successful attempts? Could I improve – this is not hard science?
Some more features:
+ Text indication of average and fastest completion time for current category
+ Text indication of where the best time is on the normal distribution – a very rough indicator of could I do better?
+ The histogram data has been fit with a normal distribution (because why not)

# Further Infomation:
### For additional details see the announcement thread on Doomworld:
https://www.doomworld.com/forum/topic/154258-fun-analysing-my-speedrunning-data/

### Contact Information:
Doomworld: https://www.doomworld.com/profile/37082-improversgaming/

YouTube: www.youtube.com/@improversgaming

E-mail: improversgaming@gmail.com

### This programme was created by **improversgaming** in July 2025
