import numpy as np
import pandas as pd
import statistics
from scipy.stats import norm
import matplotlib.gridspec as gridspec
import matplotlib.pyplot as plt

def create_display_dashboard(master_demo_data, WAD_filter, map_filter, category_filter, reset_time_threshold):
    # This function finalises data for display and creates and displays the dashboard

    # First filter the data down to what will be displayed
    # Create main data frame to view on dashboard
    # Full dataset for selected WAD and Map
    # This data is for the pie charts
    wad_map_filtered_master_demo_data = pd.DataFrame(dict(master_demo_data[
        (master_demo_data["WAD"] == WAD_filter) &
        (master_demo_data["Map"] == map_filter)
    ]))

    # Create subset of data frame filtered by selected Category and Completed
    # This is data for completion time plot and histogram
    comp_cat_wad_map_filtered_master_demo_data = wad_map_filtered_master_demo_data[
        (master_demo_data["Category"] == category_filter) &
        (master_demo_data["Complete"] == "Y")]


    # Create a moving average of completion time data (MAT) for all successful demos
    # Create a moving average window size that is somewhat sensible
    window_length = max(int(len(comp_cat_wad_map_filtered_master_demo_data) / 20), 4)
    # Added this line as receiving warning in console
    comp_cat_wad_map_filtered_master_demo_data = comp_cat_wad_map_filtered_master_demo_data.copy()
    comp_cat_wad_map_filtered_master_demo_data["MAT"] = (comp_cat_wad_map_filtered_master_demo_data.loc[:, "Time"].rolling(window=window_length).mean())
    # Find the minimum and maximum for text display
    min_mat = np.nanmin(comp_cat_wad_map_filtered_master_demo_data["MAT"])
    max_mat = np.nanmax(comp_cat_wad_map_filtered_master_demo_data["MAT"])
    # Determine average and best time metrics for filtered data
    time_data = comp_cat_wad_map_filtered_master_demo_data["Time"]
    average_completion_time = statistics.mean(time_data)
    best_completion_time = min(time_data)

    # Determine the attempt statistics for all demos
    # Create dictionary of attempts data to display in pie chart
    # The reset threshold for reset is in seconds and demos shorter than this are considered reset (quick cache for starting orientation)
    num_good_attempts = len(wad_map_filtered_master_demo_data[(wad_map_filtered_master_demo_data["Complete"] == "Y")
                              & (wad_map_filtered_master_demo_data["Time"] >= reset_time_threshold)])
    num_failed_attempts = len(wad_map_filtered_master_demo_data[(wad_map_filtered_master_demo_data["Complete"] == "N")
                            & (wad_map_filtered_master_demo_data["Time"] >= reset_time_threshold)])
    num_early_resets = len(wad_map_filtered_master_demo_data[wad_map_filtered_master_demo_data["Time"] < reset_time_threshold])
    number_of_attempts = num_good_attempts + num_failed_attempts + num_early_resets
    pie_data_attempts = {f"Successful ({num_good_attempts})": num_good_attempts,
                         f"Failed ({num_failed_attempts})": num_failed_attempts,
                         f"Reset ({num_early_resets} < {reset_time_threshold}s)": num_early_resets}

    # Determine the category breakdown for successful runs
    # Create dictionary of category data to display in pie chart
    category_data_successful_demos = wad_map_filtered_master_demo_data[(wad_map_filtered_master_demo_data["Complete"] == "Y")
                                                       & (wad_map_filtered_master_demo_data["Time"] >= reset_time_threshold)]
    category_counts = dict(category_data_successful_demos["Category"].value_counts())
    # For each key (category) set value to int and update key to include int
    # So "UV Speed" -> "UV Speed (10)" if there were 10 UV Speed completed runs
    for key in list(category_counts.keys()):
        category_counts[key] = int(category_counts[key])
        new_key = key + f" ({category_counts[key]})"
        category_counts[new_key] = category_counts.pop(key)

    # Determine data for completion time distribution and fitted normal distribution
    # Find mean and standard deviation for time data
    mean, std = norm.fit(time_data)
    tmin, tmax = min(time_data) * 0.9, max(time_data) * 1.1
    t = np.linspace(tmin, tmax, 100)
    # Create fitted distribution
    normal_distribution_data = norm.pdf(t, mean, std)
    # Use the cumulative normal distribution to determine the proportion of the
    # distribution that my time is better than
    percent_faster_than = norm.cdf(best_completion_time, loc=mean, scale=std) * 100

    # Start plotting all of the elmenent and data
    fig = plt.figure(figsize=(14, 12), constrained_layout=True)
    # Add title to Figure
    fig.suptitle(f"SPEEDRUNNING ANALYSIS - WAD: {WAD_filter}, Map: {map_filter}", fontsize=20,
                 fontweight='bold')

    # Use gridspec to create the desired layout
    gs = gridspec.GridSpec(3, 2, height_ratios=[1, 1, 1], figure=fig)
    ax0 = fig.add_subplot(gs[0, :])
    ax1 = fig.add_subplot(gs[1, 0])
    ax2 = fig.add_subplot(gs[1, 1])
    ax3 = fig.add_subplot(gs[2, :])

    # TOP PLOT: Moving Average
    ax0.plot(range(len(comp_cat_wad_map_filtered_master_demo_data)), comp_cat_wad_map_filtered_master_demo_data['Time'], label='Individual Run Times', marker='o')
    ax0.plot(range(len(comp_cat_wad_map_filtered_master_demo_data)), comp_cat_wad_map_filtered_master_demo_data['MAT'], label=f'Moving Average ({window_length})', marker='o')
    ax0.set_title(f"Speedrunning completion time progression: {category_filter}", fontsize=10,
                 fontweight='bold')
    ax0.set_xlabel("Successful Run #")
    ax0.set_ylabel("Time (s)")
    ax0.set_xlim(0, len(comp_cat_wad_map_filtered_master_demo_data) * 1.1)
    ax0.set_ylim(min(time_data) * 0.9, max(time_data) * 1.1)
    ax0.text(0.05, 0.95, f"Moving average runtime improvement: {round(max_mat, 1)}s to {round(min_mat, 1)}s",
             fontsize=10, fontweight='bold', transform=ax0.transAxes, verticalalignment='top', horizontalalignment='left')
    ax0.legend()
    ax0.grid(True)

    # MIDDLE PLOT - LEFT: Pie Chart of Attempts
    myexplode = [0.1 for _ in range(len(pie_data_attempts))]
    ax1.pie(pie_data_attempts.values(), labels=pie_data_attempts.keys(), autopct='%1.1f%%', explode=myexplode, shadow=True)
    ax1.set_title(f"Attempt outcomes ({number_of_attempts}): All Categories", fontsize=10, fontweight='bold')
    ax1.legend(pie_data_attempts.keys(), loc="best")

    # MIDDLE PLOT - RIGHT: Pie Chart of Catagories
    myexplode = [0.1 for _ in range(len(category_counts))]
    ax2.pie(category_counts.values(), labels=category_counts.keys(), autopct='%1.1f%%', explode=myexplode, shadow=True)
    ax2.set_title(f"Speedrun Categories ({num_good_attempts}): Successful Runs", fontsize=10, fontweight='bold')

    # BOTTOM PLOT: Histogram of run times
    ax3.hist(time_data, bins=10, density=True, alpha=0.6, color='b')
    ax3.plot(t, normal_distribution_data, 'k', linewidth=2)
    ax3.set_title(f"Histogram of speedrunning completion times: {category_filter}", fontsize=10, fontweight='bold')
    ax3.set_xlabel("Time (s)")
    ax3.set_ylabel("Count")
    ax3.grid(True)
    ax3.set_xlim(min(time_data) * 0.9, max(time_data) * 1.1)
    ax3.text(0.05, 0.95, f"Average run time: {round(average_completion_time, 1)}s", fontsize=10, fontweight='bold', transform=ax3.transAxes, verticalalignment='top',
             horizontalalignment='left')
    ax3.text(0.05, 0.90, f"Fastest run time: {round(best_completion_time, 1)}s", fontsize=10, fontweight='bold', transform=ax3.transAxes, verticalalignment='top',
             horizontalalignment='left')
    ax3.text(0.05, 0.85, f"The fastest run beats {round(100 - percent_faster_than, 1)}% of distribution", fontsize=10, fontweight='bold', transform=ax3.transAxes, verticalalignment='top',
             horizontalalignment='left')

    # Add thicker borders to top and bottom plots to improve visual separation
    # Not perfect, but it helps
    for ax in [ax0, ax3]:
        ax.set_facecolor("#f0f0f0")
        for spine in ax.spines.values():
            spine.set_edgecolor("black")
            spine.set_linewidth(1.5)
    # Display the dashboard
    plt.show()

    return