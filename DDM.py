#Diet Data Metrics
import os
import tkinter
import time
import math
from tkinter import *
from PIL import ImageTk, Image
from tkinter import font
from os import path
from datetime import datetime
from tkinter import ttk #for notebook module

#Build Main Window
root = tkinter.Tk()
root.geometry('1280x640')
root.title('paperWeight')
root.iconbitmap('app_icon.ico')
root.resizable(0, 0)

#notebook styling
style = ttk.Style()
style.configure("TNotebook", background="gray")

#Setup Notebook
TabControl = ttk.Notebook(root, style="TNotebook")
Diet_Data_Metrics = ttk.Frame(TabControl)
Nutrition_Data_Metrics = ttk.Frame(TabControl)
Exercise_Data_Metrics = ttk.Frame(TabControl)
Nutrition_Library = ttk.Frame(TabControl)
Settings = ttk.Frame(TabControl)
TabControl.add(Diet_Data_Metrics, text="Main Log", padding=3)
TabControl.add(Nutrition_Data_Metrics, text="Nutrition Log", padding=3)
TabControl.add(Nutrition_Library, text="Nutrition Library", padding=3)
TabControl.add(Exercise_Data_Metrics, text="Exercise Log", padding=3)
TabControl.add(Settings, text="Settings", padding=3)
TabControl.pack(expand=1, fill="both")

#Locate and Create Database Directory
boot = 0
polyfile = "C:/polyfile"
dummy = 0
if path.exists(polyfile):
    dummy = 1
else:
    os.makedirs(polyfile)

def cleanup_empty_directories():
    dir_list = [f.path for f in os.scandir(polyfile) if f.is_dir()]
    if len(dir_list) > 0:
        for directory in dir_list:
            files = [f.path for f in os.scandir(directory) if f.is_file()]
            if len(files) == 0:
                os.rmdir(directory)
cleanup_empty_directories()

#Declare Fonts
small_font = font.Font(family="Comic Sans MS", size=8)
smaller_font = font.Font(family="Comic Sans MS", size=6, weight="bold")

#Weight Controls
Weight_Control_Canvas = tkinter.Canvas(Diet_Data_Metrics, width=360, height=50, background="pink")
Weight_Control_Canvas.place(x=680, y=5)

#Weight, Age, Sex Controls for Nutrition Data Metrics
WeightN_Control_Canvas = tkinter.Canvas(Nutrition_Data_Metrics, width=685, height=50, background="lightgrey")
WeightN_Control_Canvas.place(x=350, y=5)

#Weight Graph Controls
Graphing = tkinter.Canvas(Diet_Data_Metrics, width=215, height=50, background="LightSalmon")
Graphing.place(x=1045, y=5)

#Log Water Intake Canvas
Water_Canvas = tkinter.Canvas(Diet_Data_Metrics, width=340, height=50, background="skyblue")
Water_Canvas.place(x=5, y=60)

#Diet Data Canvas
Diet_Data = tkinter.Canvas(Diet_Data_Metrics, width=900, height=535, background="grey", bd=3, relief='sunken')
Diet_Data.place(x=355, y=60)

#Data Log
Data_Log_Preview = tkinter.Canvas(Diet_Data_Metrics, width=340, height=360, background="grey", bd=2, relief="sunken")
Data_Log_Preview.place(x=3, y=237)


# Create Standard Calorie vs Time Axis
def bulid_axis():
    #data fetch
    day_fetch = str(Day.get())
    month_fetch = str(Month.get())
    year_fetch = str(Year.get())
    polyfile_dir = "/" + day_fetch + month_fetch + year_fetch
    wake_log = "/wake_log.txt"
    real_time = False
    if path.exists(polyfile + polyfile_dir + wake_log):
        read_w = open(polyfile + polyfile_dir + wake_log, "r", encoding='utf8')
        x_start = read_w.read()
        read_w.close()
        x_start_split = x_start.split(":")
        hour_start = int(x_start_split[0])
        min_start = str(x_start_split[1])
        am_pm_start = str(x_start_split[2])
        real_time = True
        if hour_start == 12:
            hour_start = 0

    Calorie_Axis = Diet_Data.create_line(50, 500, 50, 100, width=2)
    Calorie_datapoints = 16
    cal_y = 475
    increment = 100
    while Calorie_datapoints != 0:
        Diet_Data.create_line(50, cal_y, 40, cal_y, width=2, fill="lime")
        Diet_Data.create_text(30, cal_y, text=str(increment))
        increment = increment + 100
        cal_y = cal_y - 25
        Calorie_datapoints = Calorie_datapoints - 1

    Time_Axis = Diet_Data.create_line(50, 500, 850, 500, width=2)
    Time_datapoints = 16
    Time_x = 100
    time_inc = 1
    #Set Wake Point and Sleep Point ----store wake duration

    #Plot Axis Datapoints
    while Time_datapoints != 0:
        Diet_Data.create_line(Time_x, 500, Time_x, 510, width=2, fill="lime")
        if real_time == True:
            if hour_start == 11:
                if am_pm_start == "am":
                    am_pm_start = "pm"
                else:
                    am_pm_start = "am"
            Diet_Data.create_text(Time_x, 520, text=(str(hour_start + time_inc) + ":" + min_start + am_pm_start),
                                  font=("Times New Roman", 7, "bold"))
            if (hour_start + time_inc) == 12:
                hour_start = 0
                time_inc = 0
            if (hour_start + time_inc) == 11:
                if am_pm_start == "am":
                    am_pm_start = "pm"
                else:
                    am_pm_start = "am"
        else:
            Diet_Data.create_text(Time_x, 520, text=str(time_inc))
        Time_datapoints = Time_datapoints - 1
        Time_x = Time_x + 50
        time_inc = time_inc + 1

    #Graph Label
    Diet_Data.create_text(440, 130, text="Graph Showing", font=("Times New Roman", 10, "bold"))
    Diet_Data.create_text(393, 145, text="CALORIES(cal)", font=("Times New Roman", 10, "bold"))
    Diet_Data.create_text(450, 145, text="vs", font=("Times New Roman", 10, "bold"))
    Diet_Data.create_text(490, 145, text="TIME(hrs)", font=("Times New Roman", 10, "bold"))

    #Plot Red Zone
    Diet_Data.create_line(50, 300, 850, 300, fill="red", dash=(3, 1))

    #baby proofing
    child_safety = 0
    double_check = "start"

    #Plot Food Data Points
    food_log = "/food_log.txt"
    if path.exists(polyfile + polyfile_dir + food_log):
        read_flog = open(polyfile + polyfile_dir + food_log, "r", encoding='utf8')
        f_data = read_flog.read().splitlines()
        read_flog.close()
        food_data_points = []
        cycle_factor = 0
        for food_item in f_data:
            data_point = food_item.split(":")
            cal_val = int(data_point[4])
            y_val = 500 - ((cal_val/100)*25)
            #determine x_val
            time_hr = int(data_point[0])
            time_min = int(data_point[1])
            time_cycle = data_point[2]
            if path.exists(polyfile + polyfile_dir + wake_log):
                begin = open(polyfile + polyfile_dir + wake_log, "r", encoding='utf8')
                start_data = begin.read()
                begin.close()
                start_data_s = start_data.split(":")
                start_hr = int(start_data_s[0])
                start_min = int(start_data_s[1])
                if cycle_factor == 0:
                    start_cycle = start_data_s[2]
                # adjust for cycle
                if time_cycle != start_cycle:
                    start_cycle = time_cycle
                    cycle_factor = cycle_factor + 1
                    if time_hr == 12: #12 hour bugfix_1
                        time_hr = 0
                if (start_hr == 12) and (time_hr == 12) and (cycle_factor == 0): #12 hour bugfix_2
                    time_hr = 0
                if (time_cycle == start_cycle) and (start_hr == 12):
                    start_hr = 0
                time_hr_mag = (time_hr + (12*cycle_factor)) - start_hr
                time_min_mag = time_min - start_min
                x_val = 50 + (time_hr_mag*50) + ((time_min_mag/60)*50)

                #enforce child safety
                if x_val > 850:
                    child_safety = 1
                    error_val = 2
                if x_val < 50:
                    child_safety = 1
                    error_val = 3
                if child_safety == 0:
                    if double_check != "start":
                        if x_val < double_check:
                            child_safety = 1
                            error_start = double_check
                            error_val = 1
                double_check = x_val

                if child_safety == 0:
                    food_data_points.append(str(x_val) + ":" + str(y_val))

        #plot range error if necessary (child safety)
        if child_safety == 1:
            error_message_1 = "Range Error - Food Data times are not \nin the proper sequence"
            error_message_2 = "Range Error -\nOut Of Bounds"
            if error_val == 1:
                error_message = error_message_1
                Diet_Data.create_line(error_start, 475, 850, 475, width=2, fill="red")
                Diet_Data.create_line(error_start, 490, error_start, 460, width=2, fill="red")
                Diet_Data.create_line(850, 490, 850, 460, width=2, fill="red")
                line_center = ((850 - error_start)/2) + error_start
                Diet_Data.create_text(line_center, 460,
                                      text=error_message,
                                      fill="red", justify="center")
            if error_val == 2:
                error_message = error_message_2
                Diet_Data.create_line(850, 500, 850, 100, width=2, fill="lightblue")
                Diet_Data.create_text(800, 250, text=error_message, fill="lightblue", justify="center")
                diag = 500
                while diag != 100:
                    Diet_Data.create_line(850, diag, 875, (diag - 25), width=2, fill="lightblue")
                    diag = diag - 25

            if error_val == 3:
                error_message = error_message_2
                Diet_Data.create_line(51, 499, 51, 100, width=2, fill="lightblue")
                Diet_Data.create_text(100, 250, text=error_message, fill="lightblue", justify="center")
                diag = 500
                while diag != 100:
                    Diet_Data.create_line(51, diag, 26, (diag - 25), width=2, fill="lightblue")
                    diag = diag - 25


        #plot data points
        if len(food_data_points) != 0:
            for point in food_data_points:
                pt_split = point.split(":")
                x_point = int(float(pt_split[0]))
                y_point = int(float(pt_split[1]))
                if y_point < 300:
                    colour = "red"
                else:
                    colour = "green"
                Diet_Data.create_oval(x_point-6, y_point-6, x_point+6, y_point+6, fill=colour)
                if Guide_Status == 1:
                    if y_point < 300:
                        colour = "red"
                    else:
                        colour = "lime"
                    Diet_Data.create_line(x_point, y_point, x_point, 500, fill=colour, dash=(3, 1))
                    Diet_Data.create_line(x_point, y_point, 50, y_point, fill=colour, dash=(3, 1))
                Diet_Data.update()
            line_count = (len(food_data_points)) - 1
            while line_count != 0:
                coords_one = food_data_points[line_count]
                coords_two = food_data_points[(line_count-1)]
                split_one = coords_one.split(":")
                x_1 = split_one[0]
                y_1 = split_one[1]
                split_two = coords_two.split(":")
                x_2 = split_two[0]
                y_2 = split_two[1]
                Diet_Data.create_line(x_1, y_1, x_2, y_2, fill="lime")
                line_count = line_count - 1

        #store food data points
        food_graph = "/Food Graph.txt"
        Food_Store = open(polyfile + polyfile_dir + food_graph, "w", encoding='utf8')
        for item in food_data_points:
            Food_Store.write(item + "\n")
        Food_Store.close()

def plot_food_averages():
    #fetch data
    day_fetch = str(Day.get())
    month_fetch = str(Month.get())
    year_fetch = str(Year.get())
    #locate food_graphs
    polyfile_dir = "/" + day_fetch + month_fetch + year_fetch
    food_graph = "/Food Graph.txt"
    food = "Food Graph.txt"
    dir_list = [f.path for f in os.scandir(polyfile) if f.is_dir()]
    graph_list = []
    for directory in dir_list:
        file_list = [f.path for f in os.scandir(directory) if f.is_file()]
        for file in file_list:
            if path.basename(file) == food:
                graph_list.append(file)
    x_data = []
    y_data = []
    for graphs in graph_list:
        graph_data = open(graphs, "r", encoding='utf8')
        graph_read = graph_data.read().splitlines()
        graph_data.close()
        for coords in graph_read:
            split_data = coords.split(":")
            x_data.append(float(split_data[0]))
            x_data.sort()
            y_pos = x_data.index((float(split_data[0])))
            y_data.insert(y_pos, (float(split_data[1])))

    #calculate and plot averages
    average_x = []
    average_y = []
    index_set = 0
    for data_point in x_data:
        count = 0
        index = 0
        x_check = 0
        y_check = 0
        location = []
        location.clear()
        #check for duplicates
        for dupes in x_data:
            if data_point == dupes:
                count = count + 1
                location.append(index)
            index = index + 1
        #calculate y average
        if count > 1:
            y_sum = 0
            for y in location:
                y_sum = y_sum + float(y_data[y])
            avg_y = y_sum/count
            new_y = avg_y
        else:
            new_y = y_data[index_set]
        new_x = data_point
        for new in average_x:
            if new == new_x:
                x_check = 1
        if x_check == 0:
            average_x.append(new_x)
            average_y.append(new_y)
        index_set = index_set + 1

    avg_graph = len(average_x) - 1
    if avg_graph > 0:
        while avg_graph != 0:
            point_one = avg_graph
            point_two = avg_graph - 1
            Diet_Data.create_line(average_x[point_one], average_y[point_one], average_x[point_two], average_y[point_two],
                                  fill="green", dash=(3, 1))
            avg_graph = avg_graph - 1

def Wake_Duration():
    # data fetch
    day_fetch = str(Day.get())
    month_fetch = str(Month.get())
    year_fetch = str(Year.get())
    polyfile_dir = "/" + day_fetch + month_fetch + year_fetch
    wake_log = "/wake_log.txt"
    real_time = False
    if path.exists(polyfile + polyfile_dir + wake_log):
        read_w = open(polyfile + polyfile_dir + wake_log, "r", encoding='utf8')
        x_start = read_w.read()
        read_w.close()
        x_start_split = x_start.split(":")
        hour_start = int(x_start_split[0])
        min_start = str(x_start_split[1])
        am_pm_start = str(x_start_split[2])
        real_time = True
    # Set Wake Point and Sleep Point ----store wake duration
    if real_time == True:
        Diet_Data.create_text(50, 532, text=(str(hour_start) + ":" + min_start + am_pm_start),
                              font=("Times New Roman", 8, "bold"), fill="purple")
        Diet_Data.create_line(50, 500, 50, 520, fill="purple", width=2)
        sleep_log = "/sleep_log.txt"
        if path.exists(polyfile + polyfile_dir + sleep_log):
            check_sleep = open(polyfile + polyfile_dir + sleep_log, "r", encoding='utf8')
            r_sleep = check_sleep.read()
            check_sleep.close()
            sleep_splice = r_sleep.split(":")
            sleep_print_str = sleep_splice[0] + ":" + sleep_splice[1] + sleep_splice[2]
            sleep_hr = int(sleep_splice[0])
            sleep_min = int(sleep_splice[1])
            sleep_cycle = sleep_splice[2]
            if am_pm_start == sleep_cycle:
                if hour_start == 12:
                    hour_start = 0
                if (sleep_hr > hour_start) and (sleep_hr == 12):
                    sleep_hr_mag = 24 - hour_start
                elif (sleep_hr > hour_start):
                    sleep_hr_mag = abs(hour_start - sleep_hr)
                else:
                    sleep_hr_mag = 24 - (hour_start - sleep_hr)
                sleep_min_mag = sleep_min - (int(min_start))
                if sleep_min_mag < 0:
                    sleep_hr_mag = sleep_hr_mag - 1
                    sleep_min_mag = sleep_min_mag + 60
                sleep_x = (50 + (sleep_hr_mag * 50)) + ((sleep_min_mag / 60) * 50)
                sleep_hr_mag = round(sleep_hr_mag, 2)
                sleep_min_mag = round(sleep_min_mag, 2)
                wake_duration = str(sleep_hr_mag) + "hrs & " + str(sleep_min_mag) + "mins"
            else:
                if am_pm_start != sleep_cycle:
                    if hour_start == 12:
                        sleep_hr = 12 + sleep_hr
                        hour_start = 0
                    else:
                        sleep_hr = sleep_hr + 12
                sleep_hr_mag = abs(sleep_hr - hour_start)
                sleep_min_mag = sleep_min - (int(min_start))
                if sleep_min_mag < 0:
                    sleep_hr_mag = sleep_hr_mag - 1
                    sleep_min_mag = sleep_min_mag + 60
                sleep_x = (50 + (sleep_hr_mag * 50)) + ((sleep_min_mag / 60) * 50)
                sleep_hr_mag = round(sleep_hr_mag, 2)
                sleep_min_mag = round(sleep_min_mag, 2)
                wake_duration = str(sleep_hr_mag) + "hrs & " + str(sleep_min_mag) + "mins"
            Diet_Data.create_text(sleep_x, 532, text=sleep_print_str,
                                  font=("Times New Roman", 8, "bold"), fill="purple")
            Diet_Data.create_text(355, 45, text=("Wake Duration: "),
                                  fill="purple", font=("Times New Roman", 10, "bold"))
            if sleep_hr_mag < 16:
                Diet_Data.create_text(450, 45, text=wake_duration,
                                      fill="purple", font=("Times New Roman", 10, "bold"))
                Diet_Data.create_line(sleep_x, 500, sleep_x, 520, width=2, fill="purple")
            else:
                Diet_Data.create_text(450, 45, text=wake_duration,
                                      fill="red", font=("Times New Roman", 10, "bold"))
                Diet_Data.create_line(850, 500, sleep_x, 500, fill="red", dash=(3, 1))
                Diet_Data.create_line(sleep_x, 500, sleep_x, 520, width=2, fill="red")
            # wake duration store
            wake_duration_log = "/wake_duration.txt"
            wake_dur_store = open(polyfile + polyfile_dir + wake_duration_log, "w", encoding='utf8')
            wake_dur_store.write(str(sleep_hr_mag) + ":" + str(sleep_min_mag))
            wake_dur_store.close()

            # calculate average wake duration
            wake_list = []
            average_hour_list = []
            average_min_list = []
            wake_poly = [f.path for f in os.scandir(polyfile) if f.is_dir()]
            file_scan = []
            for storage in wake_poly:
                file_check = [f.path for f in os.scandir(storage) if f.is_file()]
                for txt in file_check:
                    file_scan.append(txt)
            for file in file_scan:
                file_name = path.basename(file)
                if file_name == "wake_duration.txt":
                    pull_wake_val = open(file, "r", encoding='utf8')
                    store_wake = pull_wake_val.read()
                    pull_wake_val.close()
                    wake_list.append(store_wake)
            for data in wake_list:
                data_split = data.split(":")
                average_hour_list.append(data_split[0])
                average_min_list.append(data_split[1])
            average_hours = 0
            average_mins = 0
            hours_total = 0
            mins_total = 0
            for hours in average_hour_list:
                hours_total = hours_total + int(hours)
            for mins in average_min_list:
                mins_total = mins_total + (int(mins) / 60)
            hours_total = hours_total + mins_total
            average_hours = hours_total / (len(average_hour_list))
            frac, whole = math.modf(average_hours)
            average_hours = whole
            average_mins = 60 * frac
            average_hours = round(average_hours, 2)
            average_mins = round(average_mins, 2)
            Average_Wake_Duration = str(average_hours) + "hrs & " + str(average_mins) + "mins"
            Diet_Data.create_text(380, 60, text=("Average Wake Duration: "),
                                  fill="purple", font=("Times New Roman", 10, "bold"))
            Diet_Data.create_text(513, 60, text=Average_Wake_Duration,
                                  fill="purple", font=("Times New Roman", 10, "bold"))
            #Average Sleep Duration
            avg_hours = 24 - average_hours
            avg_mins = 0 - average_mins
            if avg_mins < 0:
                avg_hours = avg_hours - 1
                avg_mins = 60 - abs(avg_mins)
            avg_hours = round(avg_hours, 2)
            avg_mins = round(avg_mins, 2)
            Average_Sleep_Duration = str(avg_hours) + "hrs & " + str(avg_mins) + "mins"
            Diet_Data.create_text(378, 75, text=("Average Sleep Duration: "),
                                  fill="purple", font=("Times New Roman", 10, "bold"))
            Diet_Data.create_text(507, 75, text=Average_Sleep_Duration,
                                  fill="purple", font=("Times New Roman", 10, "bold"))

def weightcontrol_model_three():
    day_fetch = str(Day.get())
    month_fetch = str(Month.get())
    year_fetch = str(Year.get())
    polyfile_dir = "/" + day_fetch + month_fetch + year_fetch
    W_H = "/Weight and Height.txt"
    if path.exists(polyfile + polyfile_dir + W_H):
        fetch = open(polyfile + polyfile_dir + W_H, "r", encoding='utf8')
        data = fetch.read()
        fetch.close()
        data_split = data.split(":")
        Weight = float(data_split[0])
        Height = float(data_split[1])
    else:
        Weight = 100
        Height = 1.72
    age = float(Age.get())
    if gender == 1:
        BMR = 66.47 + (13.75 * Weight) + (5.003 * (Height * 100)) - (6.755 * age)
    else:
        BMR = 655.1 + (9.563 * Weight) + (1.85 * (Height * 100)) - (4.676 * age)
    BMR = round(BMR, 2)
    max_calories = (BMR * 1.25) - 300
    snack = 100
    snack_y = 500 - ((snack/100)*25)
    meal = (max_calories/3) * 0.55
    meal_y = 500 - ((meal/100)*25)
    sub_meal =  (max_calories/3) * 0.45
    sub_meal_y = 500 - ((sub_meal/100)*25)
    snack_one = 100
    meal_one = 175
    sub_meal_one = 275
    snack_two = 350
    meal_two = 425
    sub_meal_two = 525
    snack_three = 600
    meal_three = 675
    sub_meal_three = 775

    #plot meals
    Diet_Data.create_text(snack_one, snack_y-10, text="Snack")
    Diet_Data.create_text(meal_one, meal_y-10, text="Meal One")
    Diet_Data.create_oval(snack_one-3, snack_y-3, snack_one+3, snack_y-3, fill="blue")
    Diet_Data.create_oval(meal_one-3, meal_y-3, meal_one+3, meal_y+3, fill="blue")
    Diet_Data.create_line(snack_one, snack_y, meal_one, meal_y, fill="orange")
    Diet_Data.create_text(sub_meal_one, sub_meal_y-10, text="Sub-Meal One")
    Diet_Data.create_oval(sub_meal_one-3, sub_meal_y-3, sub_meal_one+3, sub_meal_y+3, fill="blue")
    Diet_Data.create_line(meal_one, meal_y, sub_meal_one, sub_meal_y, fill="orange")
    Diet_Data.create_text(snack_two, snack_y-10, text="Snack")
    Diet_Data.create_oval(snack_two-3, snack_y-3, snack_two+3, snack_y+3, fill="blue")
    Diet_Data.create_line(sub_meal_one, sub_meal_y, snack_two, snack_y, fill="orange")
    Diet_Data.create_text(meal_two, meal_y-10, text="Meal Two")
    Diet_Data.create_oval(meal_two-3, meal_y-3, meal_two+3, meal_y+3, fill="blue")
    Diet_Data.create_line(snack_two, snack_y, meal_two, meal_y, fill="orange")
    Diet_Data.create_text(sub_meal_two, sub_meal_y-10, text="Sub-Meal Two")
    Diet_Data.create_oval(sub_meal_two-3, sub_meal_y-3, sub_meal_two+3, sub_meal_y+3, fill="blue")
    Diet_Data.create_line(meal_two, meal_y, sub_meal_two, sub_meal_y, fill="orange")
    Diet_Data.create_text(snack_three, snack_y-10, text="Snack")
    Diet_Data.create_oval(snack_three-3, snack_y-3, snack_three+3, snack_y+3, fill="blue")
    Diet_Data.create_line(sub_meal_two, sub_meal_y, snack_three, snack_y, fill="orange")
    Diet_Data.create_text(meal_three, meal_y-10, text="Meal Three")
    Diet_Data.create_oval(meal_three-3, meal_y-3, meal_three+3, meal_y+3, fill="blue")
    Diet_Data.create_line(snack_three, snack_y, meal_three, meal_y, fill="orange")
    Diet_Data.create_text(sub_meal_three, sub_meal_y-10, text="Sub-Meal Three")
    Diet_Data.create_oval(sub_meal_three-3, sub_meal_y-3, sub_meal_three+3, sub_meal_y+3, fill="blue")
    Diet_Data.create_line(meal_three, meal_y, sub_meal_three, sub_meal_y, fill="orange")

    Diet_Data.update()

def weightcontrol_model_two():
    day_fetch = str(Day.get())
    month_fetch = str(Month.get())
    year_fetch = str(Year.get())
    polyfile_dir = "/" + day_fetch + month_fetch + year_fetch
    W_H = "/Weight and Height.txt"
    if path.exists(polyfile + polyfile_dir + W_H):
        fetch = open(polyfile + polyfile_dir + W_H, "r", encoding='utf8')
        data = fetch.read()
        fetch.close()
        data_split = data.split(":")
        Weight = float(data_split[0])
        Height = float(data_split[1])
    else:
        Weight = 100
        Height = 1.72
    age = float(Age.get())
    if gender == 1:
        BMR = 66.47 + (13.75 * Weight) + (5.003 * (Height * 100)) - (6.755 * age)
    else:
        BMR = 655.1 + (9.563 * Weight) + (1.85 * (Height * 100)) - (4.676 * age)
    BMR = round(BMR, 2)
    max_calories = (BMR * 1.25) - 300
    meal_value = max_calories/3
    snack_value = 100
    snack_y = 500 - ((snack_value/100)*25)
    meal_y = 500 - ((meal_value/100)*25)
    breakfast = 225
    lunch = 475
    dinner = 725
    snack_one = 100
    snack_two = 350
    snack_three = 600
    #plot meal points
    Diet_Data.create_text(snack_one, snack_y-10, text="Snack")
    Diet_Data.create_oval(snack_one-3, snack_y-3, snack_one+3, snack_y+3, fill="blue")
    Diet_Data.create_text(breakfast, meal_y-10, text="Breakfast")
    Diet_Data.create_oval(breakfast-3, meal_y-3, breakfast+3, meal_y+3, fill="blue")
    Diet_Data.create_line(snack_one, snack_y, breakfast, meal_y, fill="orange")
    Diet_Data.create_text(snack_two, snack_y-10, text="Snack")
    Diet_Data.create_oval(snack_two-3, snack_y-3, snack_two+3, snack_y+3, fill="blue")
    Diet_Data.create_line(breakfast, meal_y, snack_two, snack_y, fill="orange")
    Diet_Data.create_text(lunch, meal_y-10, text="Lunch")
    Diet_Data.create_oval(lunch-3, meal_y-3, lunch+3, meal_y+3, fill="blue")
    Diet_Data.create_line(snack_two, snack_y, lunch, meal_y, fill="orange")
    Diet_Data.create_text(snack_three, snack_y-10, text="Snack")
    Diet_Data.create_oval(snack_three-3, snack_y-3, snack_three+3, snack_y+3, fill="blue")
    Diet_Data.create_line(lunch, meal_y, snack_three, snack_y, fill="orange")
    Diet_Data.create_text(dinner, meal_y-10, text="Dinner")
    Diet_Data.create_oval(dinner-3, meal_y-3, dinner+3, meal_y+3, fill="blue")
    Diet_Data.create_line(snack_three, snack_y, dinner, meal_y, fill="orange")

def weightcontrol_model_one():
    day_fetch = str(Day.get())
    month_fetch = str(Month.get())
    year_fetch = str(Year.get())
    polyfile_dir = "/" + day_fetch + month_fetch + year_fetch
    W_H = "/Weight and Height.txt"
    if path.exists(polyfile + polyfile_dir + W_H):
        fetch = open(polyfile + polyfile_dir + W_H, "r", encoding='utf8')
        data = fetch.read()
        fetch.close()
        data_split = data.split(":")
        Weight = float(data_split[0])
        Height = float(data_split[1])
    else:
        Weight = 100
        Height = 1.72
    age = float(Age.get())
    if gender == 1:
        BMR = 66.47 + (13.75 * Weight) + (5.003 * (Height * 100)) - (6.755 * age)
    else:
        BMR = 655.1 + (9.563 * Weight) + (1.85 * (Height * 100)) - (4.676 * age)
    BMR = round(BMR, 2)
    max_calories = BMR * 1.2
    breakfast = (max_calories / 3.71)
    lunch = (max_calories / 3.71)
    dinner = (max_calories / 3.71)
    standard_snack = (max_calories / 26)
    breakfast_y = (500 - ((breakfast / 100) * 25))
    breakfast_x = 100
    lunch_y = (500 - ((lunch / 100) * 25))
    lunch_x = 350
    dinner_y = (500 - ((dinner / 100) * 25))
    dinner_x = 650
    s_snack_y = 500 - ((standard_snack / 100) * 25)
    s_snack_x = 150
    Diet_Data.create_oval(breakfast_x - 3, breakfast_y - 3, breakfast_x + 3, breakfast_y + 3, fill="blue")

    Diet_Data.create_oval(s_snack_x - 3, s_snack_y - 3, s_snack_x + 3, s_snack_y + 3, fill="blue")
    Diet_Data.create_text(s_snack_x, s_snack_y + 10, text="Snack")
    Diet_Data.create_line(breakfast_x, breakfast_y, s_snack_x, s_snack_y, fill="orange")

    s_snack_x = s_snack_x + 100
    Diet_Data.create_oval(s_snack_x - 3, s_snack_y - 3, s_snack_x + 3, s_snack_y + 3, fill="blue")
    Diet_Data.create_text(s_snack_x, s_snack_y + 10, text="Snack")
    Diet_Data.create_line(s_snack_x - 100, s_snack_y, s_snack_x, s_snack_y, fill="orange")

    Diet_Data.create_oval(lunch_x - 3, lunch_y - 3, lunch_x + 3, lunch_y + 3, fill="blue")
    Diet_Data.create_line(s_snack_x, s_snack_y, lunch_x, lunch_y, fill="orange")

    s_snack_x = s_snack_x + 200
    Diet_Data.create_oval(s_snack_x - 3, s_snack_y - 3, s_snack_x + 3, s_snack_y + 3, fill="blue")
    Diet_Data.create_text(s_snack_x, s_snack_y + 10, text="Snack")
    Diet_Data.create_line(lunch_x, lunch_y, s_snack_x, s_snack_y, fill="orange")

    s_snack_x = s_snack_x + 100
    Diet_Data.create_oval(s_snack_x - 3, s_snack_y - 3, s_snack_x + 3, s_snack_y + 3, fill="blue")
    Diet_Data.create_text(s_snack_x, s_snack_y + 10, text="Snack")
    Diet_Data.create_line(s_snack_x - 100, s_snack_y, s_snack_x, s_snack_y, fill="orange")

    Diet_Data.create_oval(dinner_x - 3, dinner_y - 3, dinner_x + 3, dinner_y + 3, fill="blue")
    Diet_Data.create_line(s_snack_x, s_snack_y, dinner_x, dinner_y, fill="orange")

    s_snack_x = s_snack_x + 200
    Diet_Data.create_oval(s_snack_x - 3, s_snack_y - 3, s_snack_x + 3, s_snack_y + 3, fill="blue")
    Diet_Data.create_text(s_snack_x, s_snack_y + 10, text="Snack")
    Diet_Data.create_line(dinner_x, dinner_y, s_snack_x, s_snack_y, fill="orange")

    Diet_Data.create_text(breakfast_x, breakfast_y + 10, text="Breakfast")
    Diet_Data.create_text(lunch_x, lunch_y + 10, text="Lunch")
    Diet_Data.create_text(dinner_x, dinner_y + 10, text="Dinner")

def Calculate_BMI():
    day_fetch = str(Day.get())
    month_fetch = str(Month.get())
    year_fetch = str(Year.get())
    polyfile_dir = "/" + day_fetch + month_fetch + year_fetch
    W_H = "/Weight and Height.txt"
    store_weight = 0
    if path.exists(polyfile + polyfile_dir + W_H):
        fetch = open(polyfile + polyfile_dir + W_H, "r", encoding='utf8')
        data = fetch.read()
        fetch.close()
        data_split = data.split(":")
        Weight = float(data_split[0])
        store_weight = Weight
        Height = float(data_split[1])
        BMI = Weight/(Height**2)
        BMI = round(BMI, 2)
        Diet_Data.create_text(325, 15, text="BMI =", font=("Times New Roman", 10, "bold"), fill="pink")
        Diet_Data.create_text(365, 15, text=str(BMI), font=("Times New Roman", 10, "bold"), fill="pink")
        #calculate BMR
        age = float(Age.get())
        if gender == 1:
            BMR = 66.47 + (13.75*Weight) + (5.003*(Height*100)) - (6.755*age)
        else:
            BMR = 655.1 + (9.563*Weight) + (1.85*(Height*100)) - (4.676*age)
        BMR = round(BMR, 2)
        Diet_Data.create_text(327, 30, text="BMR =", font=("Times New Roman", 10, "bold"), fill="pink")
        Diet_Data.create_text(390, 30, text=str(BMR) + " (cal)", font=("Times New Roman", 10, "bold"), fill="pink")
        recc_calories = (BMR*1.25)
        weight_loss = (recc_calories*0.6)
        weight_loss = round(weight_loss, 2)
        recc_calories = round(recc_calories, 2)
        Diet_Data.create_text(689, 45, text="Recommended Calorie Intake = ",
                              font=("Times New Roman", 10, "bold"), fill="orange")
        Diet_Data.create_text(820, 45, text=(str(recc_calories) + " (cal)"),
                              font=("Times New Roman", 10, "bold"), fill="orange")
        Diet_Data.create_text(713, 60, text="Recommended Intake for Weight Loss = ",
                              font=("Times New Roman", 10, "bold"), fill="white")
        Diet_Data.create_text(863, 60, text=(str(weight_loss) + " (cal)"),
                              font=("Times New Roman", 10, "bold"), fill="white")
        #Average Caloric Intake
        cal_total = "Calorie Total.txt"
        cal_sum = 0
        cal_num = 0
        dirs = [f.path for f in os.scandir(polyfile) if f.is_dir()]
        file_list = []
        for pat in dirs:
            fils = [f.path for f in os.scandir(pat) if f.is_file()]
            for item in fils:
                file_list.append(item)
        for text in file_list:
            if path.basename(text) == cal_total:
                pull_cal = open(text, "r", encoding='utf8')
                cal_val = pull_cal.read()
                pull_cal.close()
                cal_sum = cal_sum + int(cal_val)
                cal_num = cal_num + 1
        if cal_num > 0:
            Average_Calorie_Intake = cal_sum/cal_num
            if Average_Calorie_Intake > recc_calories:
                colour = "red"
            else:
                colour = "lime"
            Average_Calorie_Intake = round(Average_Calorie_Intake, 2)
            Diet_Data.create_text(670, 15, text="Average Calorie Intake =",
                                  font=("Times New Roman", 10, "bold"), fill="lime")
            Diet_Data.create_text(778, 15, text=(str(Average_Calorie_Intake) + " (cal)"),
                                  font=("Times New Roman", 10, "bold"), fill=colour)
        #Print Daily Total
        cal_path = "/Calorie Total.txt"
        if path.exists(polyfile + polyfile_dir + cal_path):
            read_daily_val = open(polyfile + polyfile_dir + cal_path, "r", encoding='utf8')
            daily_total = read_daily_val.read()
            read_daily_val.close()
            Diet_Data.create_text(660, 30, text="Daily Calorie Total =",
                                  font=("Times New Roman", 10, "bold"), fill="lime")
            total_check = int(daily_total)
            if total_check > recc_calories:
                colour = "red"
            else:
                colour = "lime"
            Diet_Data.create_text(752, 30, text=(daily_total + " (cal)"),
                                  font=("Times New Roman", 10, "bold"), fill=colour)
    #display water log data
    if store_weight == 0:
        max_water = 64.00
    else:
        max_water = ((store_weight*2.2) * 0.666)
    max_water = round(max_water, 2)
    Diet_Data.create_text(79, 50, text="Max Water Intake =", font=("Times New Roman", 10, "bold"), fill="cyan")
    Diet_Data.create_text(180, 50, text=(str(max_water) + " Ounces"),
                          font=("Times New Roman", 10, "bold"), fill="cyan")
    Recommended_Water_Intake = max_water * 0.6
    Recommended_Water_Intake = round(Recommended_Water_Intake, 2)
    recc_x = ((Recommended_Water_Intake / max_water * 250) + 25)
    Diet_Data.create_text(107, 70, text="Recommended Water Intake =",
                          font=("Times New Roman", 10, "bold"), fill="navy")
    Diet_Data.create_text(230, 70, text=(str(Recommended_Water_Intake) + " Ounces"),
                          font=("Times New Roman", 10, "bold"), fill="navy")
    water_log = "/water log.txt"
    if path.exists(polyfile + polyfile_dir + water_log):
        read_water = open(polyfile + polyfile_dir + water_log, "r", encoding='utf8')
        water_data = read_water.read().splitlines()
        read_water.close()
        #create water scale
        Diet_Data.create_rectangle(25, 20, 275, 35, fill="white")
        water_amount = 0
        for water in water_data:
            split_water = water.split(":")
            water_time = split_water[0] + ":" + split_water[1] + split_water[2]
            water_amount = float(split_water[3]) + water_amount
            water_x = (((water_amount/max_water) * 250) + 25)
            if water_x <= 275:
                Diet_Data.create_rectangle(25, 20, water_x, 35, fill="cyan")
            else:
                Diet_Data.create_text(245, 28, text="Tank Full",
                                      font=("Times New Roman", 10, "bold"), fill="navy")
        Diet_Data.create_text(96, 28, text=("Daily Total = " + str(water_amount) + " Ounces"))
        Diet_Data.create_line(recc_x, 17, recc_x, 38, width=2, fill="navy")

def Keep_Hydrated():
    #build y-hydration values
    ounce = 1
    while ounce != 13:
        o_line = 500 - (25*ounce)
        Diet_Data.create_text(12, o_line, text=str(ounce), fill="cyan",
                              font=("Comic Sans MS", 10, "bold"))
        ounce = ounce + 1

    #check for data
    day_fetch = str(Day.get())
    month_fetch = str(Month.get())
    year_fetch = str(Year.get())
    polyfile_dir = "/" + day_fetch + month_fetch + year_fetch
    water_log = "/water log.txt"
    wake_log = "/wake_log.txt"
    if path.exists(polyfile + polyfile_dir + wake_log):
        begin = open(polyfile + polyfile_dir + wake_log, "r", encoding='utf8')
        start_data = begin.read()
        begin.close()
        split_start = start_data.split(":")
        start_hr = int(split_start[0])
        start_min = int(split_start[1])
        start_cycle = split_start[2]
        if start_hr == 12:
            start_hr = 0
        if path.exists(polyfile + polyfile_dir + water_log):
            read_water = open(polyfile + polyfile_dir + water_log, "r", encoding='utf8')
            water_data = read_water.read().splitlines()
            read_water.close()
            cycle_factor = 0
            for data in water_data:
                split = data.split(":")
                water_hr = int(split[0])
                water_min = int(split[1])
                water_cycle = split[2]
                water_amount = int(split[3])
                #cycle check and increment
                if water_cycle != start_cycle:
                    cycle_factor = cycle_factor + 1
                #determine hour and min magnitude
                if (water_cycle == start_cycle) and (water_hr == 12) and (cycle_factor == 0): #12 hour bugfix_1
                    water_hr = 0
                if water_cycle == start_cycle:
                    hr_mag = abs(water_hr - start_hr)
                    min_mag = water_min - start_min
                    if min_mag < 0:
                        hr_mag = hr_mag - 1
                        min_mag = min_mag + 60
                if water_cycle != start_cycle:
                    if water_hr == 12:
                        hr_mag = (water_hr*cycle_factor) - start_hr
                    else:
                        hr_mag = (water_hr + (cycle_factor*12)) - start_hr
                    min_mag = water_min - start_min
                    if min_mag < 0:
                        hr_mag = hr_mag - 1
                        min_mag = min_mag + 60
                if (water_cycle == start_cycle) and (water_hr < start_hr) and (cycle_factor == 0):
                    hr_mag = (water_hr - start_hr) + 24
                    min_mag = water_min - start_min
                    if min_mag < 0:
                        hr_mag = hr_mag - 1
                        min_mag = min_mag + 60
                if water_cycle != start_cycle: #logic bugfix - must be stated after calculations
                    start_cycle = water_cycle

                #calculate x and y values
                water_x = 50 + (hr_mag*50) + ((min_mag/60)*50)
                water_y = 500 - (water_amount*25)

                #plot hydration
                Diet_Data.create_rectangle(water_x-5, 500, water_x+5, water_y, fill="cyan")
                if Guide_Status == 1:
                    Diet_Data.create_line(water_x, water_y, 50, water_y, fill="cyan", dash=(3, 1))


def update_data_metrics():
    #clear canvas to intialize
    Diet_Data.delete("all")
    if Hydro == 1:
        Keep_Hydrated()
    Wake_Duration()
    Calculate_BMI()
    bulid_axis()
    # show averages
    if Average_Calc == 1:
        plot_food_averages()
    #fetch weight control data
    dummy = 0
    Weight_Control = Maintain_Weight.get()
    if Weight_Control == "Model One":
        weightcontrol_model_one()
    elif Weight_Control == "Model Two":
        weightcontrol_model_two()
    elif Weight_Control == "Model Three":
        weightcontrol_model_three()

def update_log_screen():
    #Clear Canvas to Initialize
    Data_Log_Preview.delete("all")
    day_fetch = str(Day.get())
    month_fetch = str(Month.get())
    year_fetch = str(Year.get())

    #Initialize Sleep Boxes
    Asleep.delete(0, "end")
    Asleep.insert(0, "12:00")
    Asleep_amp.config(state="normal")
    Asleep_amp.delete(0, "end")
    Asleep_amp.insert(0, "am")
    Asleep_amp.config(state="readonly")
    Awoke.delete(0, "end")
    Awoke.insert(0, "12:00")
    Awoke_amp.config(state="normal")
    Awoke_amp.delete(0, "end")
    Awoke_amp.insert(0, "am")
    Awoke_amp.config(state="readonly")

    #Fetch Heading Information
    Data_Log_Preview.create_text(170, 10, text=("Displaying Log for: " + day_fetch + " " +
                                                month_fetch + " " + year_fetch),
                                 font=("Times New Roman", 8))

    #update sleep information
    polyfile_dir = "/" + day_fetch + month_fetch + year_fetch
    wake_log = "/wake_log.txt"
    if path.exists(polyfile + polyfile_dir + wake_log):
        get_wake = open(polyfile + polyfile_dir + wake_log, "r", encoding="utf8")
        wake_data = get_wake.read().splitlines()
        get_wake.close()
        if len(wake_data) > 0:
            wake = wake_data[0]
            split_wake = wake.split(":")
            Data_Log_Preview.create_text(60, 30, text=("Awoke at: "),
                                         font=("Times New Roman", 8, "bold"), fill="purple")
            Data_Log_Preview.create_text(110, 30, text=(split_wake[0] + ":" + split_wake[1] + split_wake[2]),
                                         font=("Times New Roman", 8, "bold"), fill="purple")
            Data_Log_Preview.update()
            Awoke.delete(0, "end")
            Awoke.insert(0, (split_wake[0] + ":" + split_wake[1]))
            Awoke_amp.config(state="normal")
            Awoke_amp.delete(0, "end")
            Awoke_amp.insert(0, str((split_wake[2])))
            Awoke_amp.config(state="readonly")
    sleep_log = "/sleep_log.txt"
    if path.exists(polyfile + polyfile_dir + sleep_log):
        get_sleep = open(polyfile + polyfile_dir + sleep_log, "r", encoding="utf8")
        sleep_data = get_sleep.read().splitlines()
        get_sleep.close()
        if len(sleep_data) > 0:
            sleep = sleep_data[0]
            split_sleep = sleep.split(":")
            Data_Log_Preview.create_text(60, 50, text=("Asleep at: "),
                                         font=("Times New Roman", 8, "bold"), fill="purple")
            Data_Log_Preview.create_text(110, 50, text=(split_sleep[0] + ":" + split_sleep[1] + split_sleep[2]),
                                         font=("Times New Roman", 8, "bold"), fill="purple")
            Asleep.delete(0, "end")
            Asleep.insert(0, (split_sleep[0] + ":" + split_sleep[1]))
            Asleep_amp.config(state="normal")
            Asleep_amp.delete(0, "end")
            Asleep_amp.insert(0, str((split_sleep[2])))
            Asleep_amp.config(state="readonly")

    #reset weight height boxes
    Weight.config(state="normal")
    Height.config(state="normal")
    Weight.delete(0, "end")
    Weight.insert(0, "100.0")
    Height.delete(0, "end")
    Height.insert(0, "1.72")
    Weight.config(state="readonly")
    Height.config(state="readonly")

    # update weight and height
    W_H = "/Weight and Height.txt"
    if path.exists(polyfile + polyfile_dir + W_H):
        read_W_H = open(polyfile + polyfile_dir + W_H, "r", encoding='utf8')
        store_vals = read_W_H.read()
        read_W_H.close()
        split_vals = store_vals.split(":")
        Weight_Get = split_vals[0]
        Height_Get = split_vals[1]
        Data_Log_Preview.create_text(200, 30, text=("Weight:"),
                                     font=("Times New Roman", 8, "bold"), fill="pink")
        Data_Log_Preview.create_text(250, 30, text=(Weight_Get + " kgs"),
                                     font=("Times New Roman", 8, "bold"), fill="pink")
        Data_Log_Preview.create_text(200, 50, text=("Height:"),
                                     font=("Times New Roman", 8, "bold"), fill="pink")
        Data_Log_Preview.create_text(255, 50, text=(Height_Get + " meters"),
                                     font=("Times New Roman", 8, "bold"), fill="pink")
        #update weight height boxes
        Weight.config(state="normal")
        Height.config(state="normal")
        Weight.delete(0, "end")
        Weight.insert(0, Weight_Get)
        Height.delete(0, "end")
        Height.insert(0, Height_Get)
        Weight.config(state="readonly")
        Height.config(state="readonly")

    #update food information
    food_log = "/food_log.txt"
    top = 90
    if path.exists(polyfile + polyfile_dir + food_log):
        get_food = open(polyfile + polyfile_dir + food_log, "r", encoding="utf8")
        food_data = get_food.read().splitlines()
        get_food.close()
        Data_Log_Preview.create_text(40, 75, text="TIME")
        Data_Log_Preview.create_text(170, 75, text="Food Name")
        Data_Log_Preview.create_text(300, 75, text="Calories")
        calorie_total = 0
        for x in food_data:
            food_print = x.split(":")
            Data_Log_Preview.create_text(40, top, text=(food_print[0] + ":" + food_print[1] + food_print[2]), fill="lime")
            Data_Log_Preview.create_text(170, top, text=food_print[3], fill="lime")
            Data_Log_Preview.create_text(300, top, text=food_print[4], fill="lime")
            top = top + 18
            calorie_total = calorie_total + int(food_print[4])
        #store calorie total
        cal_total = "/Calorie Total.txt"
        cal_write = open(polyfile + polyfile_dir + cal_total, "w", encoding="utf8")
        cal_write.write(str(calorie_total))
        cal_write.close()
        #update log screen
        Data_Log_Preview.create_text(170, 350, text=("Calorie Total = " + str(calorie_total)), fill="lime")
        Data_Log_Preview.update()

    update_data_metrics()

#Show Averages
Average_Calc = 1
def Calc_Averages():
    global Average_Calc
    if Average_Calc == 1:
        Average_Calc = 0
    else:
        Average_Calc = 1
    update_data_metrics()

Show_Averages = tkinter.Checkbutton(Diet_Data_Metrics, text="Plot Averages", offvalue=2, onvalue=3, command=Calc_Averages)
Show_Averages['font'] = small_font
Show_Averages.place(x=50, y=200)
Show_Averages.select()

#Display Guides
Guide_Status = 0
def Display_Guides():
    global Guide_Status
    if Guide_Status == 0:
        Guide_Status = 1
    else:
        Guide_Status = 0
    update_data_metrics()

Show_Guides = tkinter.Checkbutton(Diet_Data_Metrics, text="Display Guides", offvalue=2, onvalue=3, command=Display_Guides)
Show_Guides['font'] = small_font
Show_Guides.place(x=150, y=200)

#Date Canvas Diet Data Metrics
Date_Canvas = tkinter.Canvas(Diet_Data_Metrics, width=340, height=50, background="lightgrey")
Date_Canvas.place(x=5, y=5)
Date_Canvas.create_text(29, 26, text="Day:", font=("Comic Sans MS", 10))
Date_Canvas.create_text(125, 26, text="Month:", font=("Comic Sans MS", 10))
Date_Canvas.create_text(268, 26, text="Year:", font=("Comic Sans MS", 10))

#Date_Canvas Nutrition Data Metrics
DateN_Canvas = tkinter.Canvas(Nutrition_Data_Metrics, width=340, height=50, background="lightgrey")
DateN_Canvas.place(x=5, y=5)
DateN_Canvas.create_text(29, 26, text="Day:", font=("Comic Sans MS", 10))
DateN_Canvas.create_text(125, 26, text="Month:", font=("Comic Sans MS", 10))
DateN_Canvas.create_text(268, 26, text="Year:", font=("Comic Sans MS", 10))
DateN_Canvas.create_rectangle(3, 3, 340, 50, outline="grey")

#create polyfile record
def polyfile_record():
    #fetch date info
    dummy = 0
    day_fetch = str(Day.get())
    month_fetch = str(Month.get())
    year_fetch = str(Year.get())
    polyfile_dir = "/" + day_fetch + month_fetch + year_fetch
    if path.exists(polyfile + polyfile_dir):
        dummy = dummy + 1
    else:
        os.makedirs(polyfile + polyfile_dir)
    #Configure Day Range (for each month and leap year)
    month_pull = Month.get()
    year_pull = Year.get()
    leap = True
    leap_check = str((int(year_pull))/4)
    split_leap = leap_check.split(".")
    if int(split_leap[1]) > 0:
        leap = False
    if (month_pull == "September") or (month_pull == "April") or (month_pull == "June") or (month_pull == "November"):
        Day.config(from_=1, to=30)
    elif (month_pull == "February") and (leap == True):
        Day.config(from_=1, to=29)
    elif month_pull == "February":
        Day.config(from_=1, to=28)
    else:
        Day.config(from_=1, to=31)
    update_log_screen()

date_data_get = datetime.now()        #Fetch OS Time and Date Information
day_get = date_data_get.day
month_get = date_data_get.month
year_get = str(date_data_get.year)
hour_get = date_data_get.hour
min_get = date_data_get.minute
if min_get < 10:
    min_get = "0" + str(min_get)
if hour_get == 12:
    cycle_get = "pm"
elif hour_get > 12:
    cycle_get = "pm"
    hour_get = hour_get - 12
else:
    cycle_get = "am"
if hour_get == 0:
    hour_get = 12
    cycle_get = "am"

#Diet Data Metrics Date Setup
Day = tkinter.Spinbox(Diet_Data_Metrics, width=3, from_=1, to=31, state="normal", command=polyfile_record)
Day.place(x=50, y=22)
Day.delete(0, "end")
Day.insert(0, day_get)
Day.config(state="readonly")

Month = tkinter.Spinbox(Diet_Data_Metrics, width=10, values=("January", "February", "March", "April", "May", "June", "July", "August", "September", "October",
             "November", "December"), state="normal", command=polyfile_record)
Month.place(x=154, y=22)
Month_List = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October",
             "November", "December"]
Month.delete(0, "end")
Month.insert(0, Month_List[month_get-1])
Month.config(state="readonly")

Year = tkinter.Spinbox(Diet_Data_Metrics, width=4, from_=2020, to=2100, state="normal", command=polyfile_record)
Year.place(x=293, y=22)
Year.delete(0, "end")
Year.insert(0, year_get)
Year.config(state="readonly")

#Input Weight And Height
def store_weight_height():
    #fetch data
    pull_weight = Weight.get()
    pull_height = Height.get()
    day_fetch = str(Day.get())
    month_fetch = str(Month.get())
    year_fetch = str(Year.get())
    polyfile_dir = "/" + day_fetch + month_fetch + year_fetch
    W_H = "/Weight and Height.txt"
    store_W_H = open(polyfile + polyfile_dir + W_H, "w", encoding='utf8')
    store_W_H.write(str(pull_weight) + ":" + str(pull_height))
    store_W_H.close()
    update_log_screen()


Weight = tkinter.Spinbox(Diet_Data_Metrics, width=5, from_=0, to=200, state="normal", increment=0.1)
Weight.place(x=733, y=10)
Weight.delete(0, "end")
Weight.insert(0, "100.0")
Weight.config(state="readonly")
Weight_Control_Canvas.create_text(28, 15, text="Weight:", font=("Comic Sans MS", 10))
Weight_Control_Canvas.create_text(112, 14, text="(kg)", font=("Comic Sans MS", 10))

Height = tkinter.Spinbox(Diet_Data_Metrics, width=5, from_=0, to=3, state="normal", increment=0.01)
Height.place(x=733, y=34)
Height.delete(0, "end")
Height.insert(0, "1.72")
Height.config(state="readonly")
Weight_Control_Canvas.create_text(30, 38, text="Height:", font=("Comic Sans MS", 10))
Weight_Control_Canvas.create_text(124, 37, text="(meters)", font=("Comic Sans MS", 10))

Log_Weight_Height = tkinter.Button(Diet_Data_Metrics, text="Log Weight\n& Height", command=store_weight_height)
Log_Weight_Height['font'] = small_font
Log_Weight_Height.place(x=836, y=11)

#Set Male/Female
gender = 1
def H_1():
    global gender
    gender = 0
    Male.deselect()
    Female.select()
    update_data_metrics()

def H_2():
    global gender
    gender = 1
    Female.deselect()
    Male.select()
    update_data_metrics()

Male = tkinter.Checkbutton(Diet_Data_Metrics, text="Male", offvalue=2, onvalue=3, command=H_2)
Male['font'] = smaller_font
Male.place(x=920, y=10)
Male.select()

Female = tkinter.Checkbutton(Diet_Data_Metrics, text="Female", offvalue=2, onvalue=3, command=H_1)
Female['font'] = smaller_font
Female.place(x=916, y=33)

#Plot Hydration
Hydro = 0
def Plot_Hydration():
    global Hydro
    if Hydro == 0:
        Hydro = 1
    else:
        Hydro = 0
    update_data_metrics()

plot_hydro = tkinter.Checkbutton(Diet_Data_Metrics, text="Plot\nHydration", offvalue=2, onvalue=3,
                                 command=Plot_Hydration)
plot_hydro['font'] = small_font
plot_hydro.place(x=263, y=67)


#Set Age
Weight_Control_Canvas.create_text(310, 26, text="Age:", font=("Comic Sans MS", 10))
Age = tkinter.Spinbox(Diet_Data_Metrics, width=3, from_=12, to=120, state="normal", command=update_data_metrics)
Age.place(x=1005, y=22)
Age.delete(0, "end")
Age.insert(0, "25")
Age.config(state="readonly")

#Weight Control Graphs
Graphing.create_text(57, 15, text="Weight Control:", font=("Comic Sans MS", 10))
Maintain_Weight = tkinter.Spinbox(Diet_Data_Metrics, values=("None", "Model One", "Model Two", "Model Three"),
                                  width=15, state="readonly", command=update_data_metrics)
Maintain_Weight.place(x=1152, y=10)

Graphing.create_text(65, 40, text="Weight Loss:", font=("Comic Sans MS", 10))
Lose_Weight = tkinter.Spinbox(Diet_Data_Metrics, values=("None", "Model One", "Model Two", "Model Three"),
                                  width=15, state="readonly", command=update_data_metrics)
Lose_Weight.place(x=1152, y=35)

def clear_water():
    # fetch data
    day_fetch = str(Day.get())
    month_fetch = str(Month.get())
    year_fetch = str(Year.get())
    polyfile_dir = "/" + day_fetch + month_fetch + year_fetch
    water_log = "/water log.txt"
    if path.exists(polyfile + polyfile_dir + water_log):
        pull_list = open(polyfile + polyfile_dir + water_log, "r", encoding='utf8')
        water_stuff = pull_list.read().splitlines()
        pull_list.close()
        if len(water_stuff) > 0:
            water_stuff.pop()
            if len(water_stuff) > 0:
                push_list = open(polyfile + polyfile_dir + water_log, "w", encoding='utf8')
                for data in water_stuff:
                    push_list.write(data + "\n")
                push_list.close()
                update_data_metrics()
            else:
                os.remove(polyfile + polyfile_dir + water_log)
                update_data_metrics()
        else:
            os.remove(polyfile + polyfile_dir + water_log)
            update_data_metrics()


def store_water():
    #fetch data
    water_time = Water_Time.get()
    water_cycle = Water_Cycle.get()
    water_amount = Water_Amount.get()
    day_fetch = str(Day.get())
    month_fetch = str(Month.get())
    year_fetch = str(Year.get())
    polyfile_dir = "/" + day_fetch + month_fetch + year_fetch
    water_log = "/water log.txt"
    #Validate and store
    try:
        split = water_time.split(":")
        int_check_one = int(split[0])
        int_check_two = int(split[1])
        if len(split) == 2:
            if (int_check_one > 0) and (int_check_two >= 0) and (int_check_one <= 12) and (int_check_two <= 59):
                store_wata = open(polyfile + polyfile_dir + water_log, "a", encoding='utf8')
                store_wata.write(water_time + ":" + water_cycle + ":" + water_amount + "\n")
                store_wata.close()
                update_data_metrics()
            else:
                Water_Time.delete(0, "end")
                Water_Time.insert(0, "err")
        else:
            Water_Time.delete(0, "end")
            Water_Time.insert(0, "err")
    except:
        Water_Time.delete(0, "end")
        Water_Time.insert(0, "err")

#Water Data Input
Water_Canvas.create_text(24, 14, text="Time:", font=("Comic Sans MS", 10))
Water_Canvas.create_text(38, 39, text="Quantity:", font=("Comic Sans MS", 10))
Water_Canvas.create_text(114, 39, text="(OZ.)", font=("Comic Sans MS", 10))
Water_Time = tkinter.Entry(Diet_Data_Metrics, width=5)
Water_Time.place(x=50, y=65)
Water_Time.delete(0, "end")
Water_Time.insert(0, (str(hour_get) + ":" + str(min_get)))
Water_Cycle = tkinter.Spinbox(Diet_Data_Metrics, width=3, values=("am", "pm"), state="normal")
Water_Cycle.place(x=88, y=65)
Water_Cycle.delete(0, "end")
Water_Cycle.insert(0, cycle_get)
Water_Cycle.config(state="readonly")
Water_Amount = tkinter.Spinbox(Diet_Data_Metrics, width=2, from_=1, to=12, state="normal")
Water_Amount.delete(0, "end")
Water_Amount.insert(0, "8")
Water_Amount.config(state="readonly")
Water_Amount.place(x=73, y=90)

Log_Water = tkinter.Button(Diet_Data_Metrics, text="Add Water", command=store_water)
Log_Water['font'] = small_font
Log_Water.place(x=148, y=75)

Clear_Water = tkinter.Button(Diet_Data_Metrics, text="clear", command=clear_water)
Clear_Water['font'] = small_font
Clear_Water.place(x=220, y=75)

#Sleep data INPUT
sleep_section = tkinter.Canvas(Diet_Data_Metrics, width=320, height=50, background="plum3")
sleep_section.place(x=355, y=5)
sleep_section.create_text(47, 13, text="Awoke at:", font=("Comic Sans MS", 10))
sleep_section.create_text(205, 13, text="Asleep at:", font=("Comic Sans MS", 10))

def Log_Wake():
    wake = Awoke.get()
    #Validate and store Wake Time
    try:
        wa_split = wake.split(":")
        if len(wa_split) == 2:
            num_check_one = int(wa_split[0])
            num_check_two = int(wa_split[1])
            if (num_check_one <= 12) and (num_check_two <= 59) and (num_check_one > 0) and (num_check_two >= 0):
                wake_am_pm = Awoke_amp.get()
                day_fetch = str(Day.get())
                month_fetch = str(Month.get())
                year_fetch = str(Year.get())
                polyfile_dir = "/" + day_fetch + month_fetch + year_fetch
                wake_log = "/wake_log.txt"
                set_wake = open(polyfile + polyfile_dir + wake_log, "w", encoding='utf8')
                set_wake.write(wake + ":" + wake_am_pm)
                set_wake.close()
                update_log_screen()
                Wake_Duration()
            else:
                Awoke.delete(0, "end")
                Awoke.insert(0, "invalid")
        else:
            Awoke.delete(0, "end")
            Awoke.insert(0, "invalid")
    except:
        Awoke.delete(0, "end")
        Awoke.insert(0, "invalid")

def Log_Sleep():
    sleep = Asleep.get()
    #Validate and store Sleep Time
    try:
        sl_split = sleep.split(":")
        if len(sl_split) == 2:
            num_check_one = int(sl_split[0])
            num_check_two = int(sl_split[1])
            if (num_check_one <= 12) and (num_check_two <= 59) and (num_check_one > 0) and (num_check_two >= 0):
                sleep_am_pm = Asleep_amp.get()
                day_fetch = str(Day.get())
                month_fetch = str(Month.get())
                year_fetch = str(Year.get())
                polyfile_dir = "/" + day_fetch + month_fetch + year_fetch
                sleep_log = "/sleep_log.txt"
                set_sleep = open(polyfile + polyfile_dir + sleep_log, "w", encoding='utf8')
                set_sleep.write(sleep + ":" + sleep_am_pm)
                set_sleep.close()
                update_log_screen()
                Wake_Duration()
            else:
                Asleep.delete(0, "end")
                Asleep.insert(0, "invalid")
        else:
            Asleep.delete(0, "end")
            Asleep.insert(0, "invalid")
    except:
        Asleep.delete(0, "end")
        Asleep.insert(0, "invalid")

Awoke = tkinter.Entry(Diet_Data_Metrics, width=5)
Awoke.place(x=435, y=8)
Awoke.insert(0, "12:00")
Awoke_amp = tkinter.Spinbox(Diet_Data_Metrics, width=3, values=("am", "pm"), state="readonly")
Awoke_amp.place(x=473, y=8)

Asleep = tkinter.Entry(Diet_Data_Metrics, width=5)
Asleep.place(x=590, y=8)
Asleep.insert(0, "12:00")
Asleep_amp = tkinter.Spinbox(Diet_Data_Metrics, width=3, values=("am", "pm"), state="readonly")
Asleep_amp.place(x=628, y=8)

Log_Wake_Time = tkinter.Button(Diet_Data_Metrics, text="Log Wake Time", command=Log_Wake)
Log_Wake_Time['font'] = small_font
Log_Wake_Time.place(x=395, y=29)

Log_Sleep_Time = tkinter.Button(Diet_Data_Metrics, text="Log Sleep Time", command=Log_Sleep)
Log_Sleep_Time['font'] = small_font
Log_Sleep_Time.place(x=555, y=29)

#Food Input
food_section = tkinter.Canvas(Diet_Data_Metrics, width=340, height=75, background="lightgreen")
food_section.place(x=5, y=115)
food_section.create_text(45, 15, text="Food Name:", font=("Comic Sans MS", 10))
food_section.create_text(54, 40, text="Calories:", font=("Comic Sans MS", 10))
food_section.create_text(64, 65, text="Time:", font=("Comic Sans MS", 10))
food_section.create_text(154, 40, text="(cal)", font=("Comic Sans MS", 10))

def Log_Food_Data():
    #get input data
    Food = Food_Name.get()
    Calorie_val = Calories.get()
    TIME = Time.get()
    am_pm = Time_amp.get()
    if Food == "":
        Food = "Unknown"
    if len(Food) > 32:
        Food_Name.delete(0, "end")
        Food_Name.insert(0, "32 Characters max!")
    else:
        #begin validation
        try:
            Calorie_int_check = int(Calorie_val)
            t_split = TIME.split(":")
            if Calorie_int_check > 0:
                if len(t_split) == 2:
                    t_hr_check = int(t_split[0])
                    t_min_check = int(t_split[1])
                    if (t_hr_check <= 12) and (t_min_check <= 59) and (t_hr_check > 0) and (t_min_check >= 0):
                        #Store Data
                        day_fetch = str(Day.get())
                        month_fetch = str(Month.get())
                        year_fetch = str(Year.get())
                        polyfile_dir = "/" + day_fetch + month_fetch + year_fetch
                        food_log = "/food_log.txt"
                        food_store = open(polyfile + polyfile_dir + food_log, "a", encoding='utf8')
                        food_store.write(TIME + ":" + am_pm + ":" + Food + ":" + Calorie_val + "\n")
                        food_store.close()
                        #update log screen
                        update_log_screen()
                    else:
                        Time.delete(0, "end")
                        Time.insert(0, "invalid")
                else:
                    Time.delete(0, "end")
                    Time.insert(0, "invalid")
            else:
                Calories.delete(0, "end")
                Calories.insert(0, "invalid")
        except:
            Calories.delete(0, "end")
            Calories.insert(0, "invalid")

def ClearFood():
    day_fetch = str(Day.get())
    month_fetch = str(Month.get())
    year_fetch = str(Year.get())
    polyfile_dir = "/" + day_fetch + month_fetch + year_fetch
    food_log = "/food_log.txt"
    if path.exists(polyfile + polyfile_dir + food_log):
        food_store = open(polyfile + polyfile_dir + food_log, "r", encoding='utf8')
        data_pull = food_store.read().splitlines()
        food_store.close()
        if len(data_pull) > 0:
            data_pull.pop()
        ammend = open(polyfile + polyfile_dir + food_log, "w", encoding='utf8')
        for item in data_pull:
            ammend.write(item +"\n")
        ammend.close()
        update_log_screen()

Food_Name = tkinter.Entry(Diet_Data_Metrics, width=30)
Food_Name.place(x=90, y=120)

Calories = tkinter.Entry(Diet_Data_Metrics, width=8)
Calories.place(x=90, y=145)

Time = tkinter.Entry(Diet_Data_Metrics, width=6)
Time.place(x=90, y=170)
Time.insert(0, (str(hour_get)+ ":" + str(min_get)))
Time_amp = tkinter.Spinbox(Diet_Data_Metrics, width=3, values=("am", "pm"), state="normal")
Time_amp.place(x=135, y=170)
Time_amp.delete(0, "end")
Time_amp.insert(0, cycle_get)
Time_amp.config(state="readonly")

Log_Food = tkinter.Button(Diet_Data_Metrics, text="Add Food", command=Log_Food_Data)
Log_Food['font'] = small_font
Log_Food.place(x=210, y=155)

Clear_Item = tkinter.Button(Diet_Data_Metrics, text="clear", command=ClearFood)
Clear_Item['font'] = small_font
Clear_Item.place(x=273, y=155)

polyfile_record() #auto-creates a file directory and calls the log-screen to update

#method for adding data to nutrition log -----------------------------------------
def add_to_nutrition():
    # fetch nutrition spinbox data
    calcium = Calcium.get()
    chromium = Chromium.get()
    copper = Copper.get()
    fluoride = Fluoride.get()
    iodine = Iodine.get()
    iron = Iron.get()
    magnesium = Magnesium.get()
    manganese = Manganese.get()
    molybdenum = Molybdenum.get()
    phosphorus = Phosphorus.get()
    selenium = Selenium.get()
    zinc = Zinc.get()
    potassium = Potassium.get()
    sodium = Sodium.get()
    chloride = Chloride.get()
    vitamin_a = Vitamin_A.get()
    vitamin_c = Vitamin_C.get()
    vitamin_d = Vitamin_D.get()
    vitamin_e = Vitamin_E.get()
    vitamin_k = Vitamin_K.get()
    thiamin = Thiamin.get()
    riboflavin = Riboflavin.get()
    niacin = Niacin.get()
    vitamin_b6 = Vitamin_B6.get()
    folate = Folate.get()
    vitamin_b12 = Vitamin_B12.get()
    pantothenic_acid = Pantothenic_Acid.get()
    biotin = Biotin.get()
    choline = Choline.get()
    carbohydrate = Carbohydrate.get()
    total_fat = Total_Fat.get()
    saturated_fat = Saturated_Fat.get()
    cholesterol = Cholesterol.get()
    protein = Protein.get()
    fiber = Fiber.get()
    linoleic_acid = Linoleic_Acid.get()
    alpha_linoleic_acid = Alpha_Linoleic_Acid.get()

    # add nutrition data
    nutri_read = open(polyfile + "/SS.txt", "r", encoding="utf8")
    nutri = nutri_read.read().splitlines()
    nutri_read.close()
    # clear first five items
    nutri.pop(0)
    nutri.pop(0)
    nutri.pop(0)
    nutri.pop(0)
    nutri.pop(0)
    for item in nutri:
        work = item.split("*")
        if work[0] == "Calcium":
            calcium = float(calcium) + float(work[1])
            Calcium.config(state="normal")
            Calcium.delete(0, "end")
            Calcium.insert(0, calcium)
            Calcium.config(state="readonly")
        elif work[0] == "Chromium":
            chromium = float(chromium) + float(work[1])
            Chromium.config(state="normal")
            Chromium.delete(0, "end")
            Chromium.insert(0, chromium)
            Chromium.config(state="readonly")
        elif work[0] == "Copper":
            copper = float(copper) + float(work[1])
            Copper.config(state="normal")
            Copper.delete(0, "end")
            Copper.insert(0, copper)
            Copper.config(state="readonly")
        elif work[0] == "Fluoride":
            fluoride = float(fluoride) + float(work[1])
            Fluoride.config(state="normal")
            Fluoride.delete(0, "end")
            Fluoride.insert(0, fluoride)
            Fluoride.config(state="readonly")
        elif work[0] == "Iodine":
            iodine = float(iodine) + float(work[1])
            Iodine.config(state="normal")
            Iodine.delete(0, "end")
            Iodine.insert(0, iodine)
            Iodine.config(state="readonly")
        elif work[0] == "Iron":
            iron = float(iron) + float(work[1])
            Iron.config(state="normal")
            Iron.delete(0, "end")
            Iron.insert(0, iron)
            Iron.config(state="readonly")
        elif work[0] == "Magnesium":
            magnesium = float(magnesium) + float(work[1])
            Magnesium.config(state="normal")
            Magnesium.delete(0, "end")
            Magnesium.insert(0, magnesium)
            Magnesium.config(state="readonly")
        elif work[0] == "Manganese":
            manganese = float(manganese) + float(work[1])
            Manganese.config(state="normal")
            Manganese.delete(0, "end")
            Manganese.insert(0, manganese)
            Manganese.config(state="readonly")
        elif work[0] == "Molybdenum":
            molybdenum = float(molybdenum) + float(work[1])
            Molybdenum.config(state="normal")
            Molybdenum.delete(0, "end")
            Molybdenum.insert(0, molybdenum)
            Molybdenum.config(state="readonly")
        elif work[0] == "Phosphorus":
            phosphorus = float(phosphorus) + float(work[1])
            Phosphorus.config(state="normal")
            Phosphorus.delete(0, "end")
            Phosphorus.insert(0, phosphorus)
            Phosphorus.config(state="readonly")
        elif work[0] == "Selenium":
            selenium = float(selenium) + float(work[1])
            Selenium.config(state="normal")
            Selenium.delete(0, "end")
            Selenium.insert(0, selenium)
            Selenium.config(state="readonly")
        elif work[0] == "Zinc":
            zinc = float(zinc) + float(work[1])
            Zinc.config(state="normal")
            Zinc.delete(0, "end")
            Zinc.insert(0, zinc)
            Zinc.config(state="readonly")
        elif work[0] == "Potassium":
            potassium = float(potassium) + float(work[1])
            Potassium.config(state="normal")
            Potassium.delete(0, "end")
            Potassium.insert(0, potassium)
            Potassium.config(state="readonly")
        elif work[0] == "Sodium":
            sodium = float(sodium) + float(work[1])
            Sodium.config(state="normal")
            Sodium.delete(0, "end")
            Sodium.insert(0, sodium)
            Sodium.config(state="readonly")
        elif work[0] == "Chloride":
            chloride = float(chloride) + float(work[1])
            Chloride.config(state="normal")
            Chloride.delete(0, "end")
            Chloride.insert(0, chloride)
            Chloride.config(state="readonly")
        elif work[0] == "Vitamin A":
            vitamin_a = float(vitamin_a) + float(work[1])
            Vitamin_A.config(state="normal")
            Vitamin_A.delete(0, "end")
            Vitamin_A.insert(0, vitamin_a)
            Vitamin_A.config(state="readonly")
        elif work[0] == "Vitamin C":
            vitamin_c = float(vitamin_c) + float(work[1])
            Vitamin_C.config(state="normal")
            Vitamin_C.delete(0, "end")
            Vitamin_C.insert(0, vitamin_c)
            Vitamin_C.config(state="readonly")
        elif work[0] == "Vitamin D":
            vitamin_d = float(vitamin_d) + float(work[1])
            Vitamin_D.config(state="normal")
            Vitamin_D.delete(0, "end")
            Vitamin_D.insert(0, vitamin_d)
            Vitamin_D.config(state="readonly")
        elif work[0] == "Vitamin E":
            vitamin_e = float(vitamin_e) + float(work[1])
            Vitamin_E.config(state="normal")
            Vitamin_E.delete(0, "end")
            Vitamin_E.insert(0, vitamin_e)
            Vitamin_E.config(state="readonly")
        elif work[0] == "Vitamin K":
            vitamin_k = float(vitamin_k) + float(work[1])
            Vitamin_K.config(state="normal")
            Vitamin_K.delete(0, "end")
            Vitamin_K.insert(0, vitamin_k)
            Vitamin_K.config(state="readonly")
        elif work[0] == "Thiamin":
            thiamin = float(thiamin) + float(work[1])
            Thiamin.config(state="normal")
            Thiamin.delete(0, "end")
            Thiamin.insert(0, thiamin)
            Thiamin.config(state="readonly")
        elif work[0] == "Riboflavin":
            riboflavin = float(riboflavin) + float(work[1])
            Riboflavin.config(state="normal")
            Riboflavin.delete(0, "end")
            Riboflavin.insert(0, riboflavin)
            Riboflavin.config(state="readonly")
        elif work[0] == "Niacin":
            niacin = float(niacin) + float(work[1])
            Niacin.config(state="normal")
            Niacin.delete(0, "end")
            Niacin.insert(0, niacin)
            Niacin.config(state="readonly")
        elif work[0] == "Vitamin B6":
            vitamin_b6 = float(vitamin_b6) + float(work[1])
            Vitamin_B6.config(state="normal")
            Vitamin_B6.delete(0, "end")
            Vitamin_B6.insert(0, vitamin_b6)
            Vitamin_B6.config(state="readonly")
        elif work[0] == "Folate":
            folate = float(folate) + float(work[1])
            Folate.config(state="normal")
            Folate.delete(0, "end")
            Folate.insert(0, folate)
            Folate.config(state="readonly")
        elif work[0] == "Vitamin B12":
            vitamin_b12 = float(vitamin_b12) + float(work[1])
            Vitamin_B12.config(state="normal")
            Vitamin_B12.delete(0, "end")
            Vitamin_B12.insert(0, vitamin_b12)
            Vitamin_B12.config(state="readonly")
        elif work[0] == "Pantothenic Acid":
            pantothenic_acid = float(pantothenic_acid) + float(work[1])
            Pantothenic_Acid.config(state="normal")
            Pantothenic_Acid.delete(0, "end")
            Pantothenic_Acid.insert(0, pantothenic_acid)
            Pantothenic_Acid.config(state="readonly")
        elif work[0] == "Biotin":
            biotin = float(biotin) + float(work[1])
            Biotin.config(state="normal")
            Biotin.delete(0, "end")
            Biotin.insert(0, biotin)
            Biotin.config(state="readonly")
        elif work[0] == "Choline":
            choline = float(choline) + float(work[1])
            Choline.config(state="normal")
            Choline.delete(0, "end")
            Choline.insert(0, choline)
            Choline.config(state="readonly")
        elif work[0] == "Carbohydrate":
            carbohydrate = float(carbohydrate) + float(work[1])
            Carbohydrate.config(state="normal")
            Carbohydrate.delete(0, "end")
            Carbohydrate.insert(0, carbohydrate)
            Carbohydrate.config(state="readonly")
        elif work[0] == "Protein":
            protein = float(protein) + float(work[1])
            Protein.config(state="normal")
            Protein.delete(0, "end")
            Protein.insert(0, protein)
            Protein.config(state="readonly")
        elif work[0] == "Fiber":
            fiber = float(fiber) + float(work[1])
            Fiber.config(state="normal")
            Fiber.delete(0, "end")
            Fiber.insert(0, fiber)
            Fiber.config(state="readonly")
        elif work[0] == "Linoleic Acid":
            linoleic_acid = float(linoleic_acid) + float(work[1])
            Linoleic_Acid.config(state="normal")
            Linoleic_Acid.delete(0, "end")
            Linoleic_Acid.insert(0, linoleic_acid)
            Linoleic_Acid.config(state="readonly")
        elif work[0] == "Alpha Linoleic Acid":
            alpha_linoleic_acid = float(alpha_linoleic_acid) + float(work[1])
            Alpha_Linoleic_Acid.config(state="normal")
            Alpha_Linoleic_Acid.delete(0, "end")
            Alpha_Linoleic_Acid.insert(0, alpha_linoleic_acid)
            Alpha_Linoleic_Acid.config(state="readonly")
        elif work[0] == "Total Fat":
            total_fat = float(total_fat) + float(work[1])
            Total_Fat.config(state="normal")
            Total_Fat.delete(0, "end")
            Total_Fat.insert(0, total_fat)
            Total_Fat.config(state="readonly")
        elif work[0] == "Saturated Fat":
            saturated_fat = float(saturated_fat) + float(work[1])
            Saturated_Fat.config(state="normal")
            Saturated_Fat.delete(0, "end")
            Saturated_Fat.insert(0, saturated_fat)
            Saturated_Fat.config(state="readonly")
        elif work[0] == "Cholesterol":
            cholesterol = float(cholesterol) + float(work[1])
            Cholesterol.config(state="normal")
            Cholesterol.delete(0, "end")
            Cholesterol.insert(0, cholesterol)
            Cholesterol.config(state="readonly")
    discrete_store()
    Draw_Nutrition_Log()

def reset_boxes():
    Calcium.config(state="normal")
    Calcium.delete(0, "end")
    Calcium.insert(0, "0.0")
    Calcium.config(state="readonly")

    Chromium.config(state="normal")
    Chromium.delete(0, "end")
    Chromium.insert(0, "0.0")
    Chromium.config(state="readonly")

    Copper.config(state="normal")
    Copper.delete(0, "end")
    Copper.insert(0, "0.0")
    Copper.config(state="readonly")

    Fluoride.config(state="normal")
    Fluoride.delete(0, "end")
    Fluoride.insert(0, "0.0")
    Fluoride.config(state="readonly")

    Iodine.config(state="normal")
    Iodine.delete(0, "end")
    Iodine.insert(0, "0.0")
    Iodine.config(state="readonly")

    Iron.config(state="normal")
    Iron.delete(0, "end")
    Iron.insert(0, "0.0")
    Iron.config(state="readonly")

    Magnesium.config(state="normal")
    Magnesium.delete(0, "end")
    Magnesium.insert(0, "0.0")
    Magnesium.config(state="readonly")

    Manganese.config(state="normal")
    Manganese.delete(0, "end")
    Manganese.insert(0, "0.0")
    Manganese.config(state="readonly")

    Molybdenum.config(state="normal")
    Molybdenum.delete(0, "end")
    Molybdenum.insert(0, "0.0")
    Molybdenum.config(state="readonly")

    Phosphorus.config(state="normal")
    Phosphorus.delete(0, "end")
    Phosphorus.insert(0, "0.0")
    Phosphorus.config(state="readonly")

    Selenium.config(state="normal")
    Selenium.delete(0, "end")
    Selenium.insert(0, "0.0")
    Selenium.config(state="readonly")

    Zinc.config(state="normal")
    Zinc.delete(0, "end")
    Zinc.insert(0, "0.0")
    Zinc.config(state="readonly")

    Potassium.config(state="normal")
    Potassium.delete(0, "end")
    Potassium.insert(0, "0.0")
    Potassium.config(state="readonly")

    Sodium.config(state="normal")
    Sodium.delete(0, "end")
    Sodium.insert(0, "0.0")
    Sodium.config(state="readonly")

    Chloride.config(state="normal")
    Chloride.delete(0, "end")
    Chloride.insert(0, "0.0")
    Chloride.config(state="readonly")

    Vitamin_A.config(state="normal")
    Vitamin_A.delete(0, "end")
    Vitamin_A.insert(0, "0.0")
    Vitamin_A.config(state="readonly")

    Vitamin_C.config(state="normal")
    Vitamin_C.delete(0, "end")
    Vitamin_C.insert(0, "0.0")
    Vitamin_C.config(state="readonly")

    Vitamin_D.config(state="normal")
    Vitamin_D.delete(0, "end")
    Vitamin_D.insert(0, "0.0")
    Vitamin_D.config(state="readonly")

    Vitamin_E.config(state="normal")
    Vitamin_E.delete(0, "end")
    Vitamin_E.insert(0, "0.0")
    Vitamin_E.config(state="readonly")

    Vitamin_K.config(state="normal")
    Vitamin_K.delete(0, "end")
    Vitamin_K.insert(0, "0.0")
    Vitamin_K.config(state="readonly")

    Thiamin.config(state="normal")
    Thiamin.delete(0, "end")
    Thiamin.insert(0, "0.0")
    Thiamin.config(state="readonly")

    Riboflavin.config(state="normal")
    Riboflavin.delete(0, "end")
    Riboflavin.insert(0, "0.0")
    Riboflavin.config(state="readonly")

    Niacin.config(state="normal")
    Niacin.delete(0, "end")
    Niacin.insert(0, "0.0")
    Niacin.config(state="readonly")

    Vitamin_B6.config(state="normal")
    Vitamin_B6.delete(0, "end")
    Vitamin_B6.insert(0, "0.0")
    Vitamin_B6.config(state="readonly")

    Folate.config(state="normal")
    Folate.delete(0, "end")
    Folate.insert(0, "0.0")
    Folate.config(state="readonly")

    Vitamin_B12.config(state="normal")
    Vitamin_B12.delete(0, "end")
    Vitamin_B12.insert(0, "0.0")
    Vitamin_B12.config(state="readonly")

    Pantothenic_Acid.config(state="normal")
    Pantothenic_Acid.delete(0, "end")
    Pantothenic_Acid.insert(0, "0.0")
    Pantothenic_Acid.config(state="readonly")

    Biotin.config(state="normal")
    Biotin.delete(0, "end")
    Biotin.insert(0, "0.0")
    Biotin.config(state="readonly")

    Choline.config(state="normal")
    Choline.delete(0, "end")
    Choline.insert(0, "0.0")
    Choline.config(state="readonly")

    Carbohydrate.config(state="normal")
    Carbohydrate.delete(0, "end")
    Carbohydrate.insert(0, "0.0")
    Carbohydrate.config(state="readonly")

    Protein.config(state="normal")
    Protein.delete(0, "end")
    Protein.insert(0, "0.0")
    Protein.config(state="readonly")

    Fiber.config(state="normal")
    Fiber.delete(0, "end")
    Fiber.insert(0, "0.0")
    Fiber.config(state="readonly")

    Linoleic_Acid.config(state="normal")
    Linoleic_Acid.delete(0, "end")
    Linoleic_Acid.insert(0, "0.0")
    Linoleic_Acid.config(state="readonly")

    Alpha_Linoleic_Acid.config(state="normal")
    Alpha_Linoleic_Acid.delete(0, "end")
    Alpha_Linoleic_Acid.insert(0, "0.0")
    Alpha_Linoleic_Acid.config(state="readonly")

    Total_Fat.config(state="normal")
    Total_Fat.delete(0, "end")
    Total_Fat.insert(0, "0.0")
    Total_Fat.config(state="readonly")

    Saturated_Fat.config(state="normal")
    Saturated_Fat.delete(0, "end")
    Saturated_Fat.insert(0, "0.0")
    Saturated_Fat.config(state="readonly")

    Cholesterol.config(state="normal")
    Cholesterol.delete(0, "end")
    Cholesterol.insert(0, "0.0")
    Cholesterol.config(state="readonly")

    discrete_store()
    Draw_Nutrition_Log()

#reset nutrition spinboxes button
reset_all = tkinter.Button(Nutrition_Data_Metrics, text="RESET ALL", command=reset_boxes)
reset_all['font'] = small_font
reset_all.place(x=140, y=75)

#Nutrition Data Metrics Canvas Declarations
Discretionary = tkinter.Canvas(Nutrition_Data_Metrics, width=340, height=350, background="mediumpurple2")
Discretionary.place(x=695, y=250)

Macronutrients = tkinter.Canvas(Nutrition_Data_Metrics, width=340, height=185, background="lightgreen")
Macronutrients.place(x=695, y=60)

Vitamins = tkinter.Canvas(Nutrition_Data_Metrics, width=340, height=485, background="skyblue2")
Vitamins.place(x=350, y=115)

Elements = tkinter.Canvas(Nutrition_Data_Metrics, width=340, height=485, background="mistyrose2")
Elements.place(x=5, y=115)

#Nutrition Data Metrics Data Log
Nutrition_Log = tkinter.Canvas(Nutrition_Data_Metrics, width=220, height=590, background="grey", bd=2, relief='sunken')
Nutrition_Log.place(x=1040, y=5)

def Draw_Nutrition_Log():
    Nutrition_Log.delete("all")

    #fetch date info
    day_fetch = str(DayN.get())
    month_fetch = str(MonthN.get())
    year_fetch = str(YearN.get())
    polyfile_dir = "/" + day_fetch + month_fetch + year_fetch

    #Build Axis
    Nutrition_Log.create_text(110, 20, text="DAILY LOG", fill="white", font=("Comic Sans MS", 10))
    Nutrition_Log.create_line(20, 40, 20, 560, width=2)
    Nutrition_Log.create_line(20, 560, 20, 570, width=2, fill="white")
    Nutrition_Log.create_text(20, 580, text="0", fill="white")
    Nutrition_Log.create_line(20, 560, 200, 560, width=2)
    Nutrition_Log.create_line(200, 560, 200, 570, width=2, fill="white")
    Nutrition_Log.create_text(200, 580, text="100", fill="white")
    Nutrition_Log.create_text(110, 580, text="% Daily Value", fill="white", font=("Comic Sans MS", 10))

    #Build Histogram
    #Read DRI stats
    stats = "/DRI_stats.txt"
    pull_stats = open(polyfile + stats, "r", encoding="utf8")
    data_pull = pull_stats.read().splitlines()
    pull_stats.close()

    # initialize log storage
    nutri_log = "/Nutrition_Log.txt"
    nutri = open(polyfile + polyfile_dir + nutri_log, "w", encoding="utf8")

    #Calcium
    Calcium_Stat = float(data_pull[0])
    Calcium_Data = float(Calcium.get())
    nutri.write(str(Calcium_Data) + "\n")
    Calcium_Percent = str(round(((Calcium_Data / Calcium_Stat) * 100), 2))
    if Calcium_Data > Calcium_Stat:
        Calcium_Colour = "red"
        Calcium_Data = Calcium_Stat
    else:
        Calcium_Colour = "mistyrose2"
    Calcium_Value = round((((Calcium_Data/Calcium_Stat) * 180) + 20), 2)
    Nutrition_Log.create_rectangle(20, 45, Calcium_Value, 55, fill=Calcium_Colour, outline=Calcium_Colour)
    Nutrition_Log.create_text(80, 50, text="Calcium", fill="black", font=("Comic Sans MS", 8))
    Nutrition_Log.create_text(150, 50, text=(Calcium_Percent + "%"), fill="black")
    Nutrition_Log.create_rectangle(20, 45, 200, 55)


    # Chromium
    Chromium_Stat = float(data_pull[1])
    Chromium_Data = float(Chromium.get())
    nutri.write(str(Chromium_Data) + "\n")
    Chromium_Percent = str(round(((Chromium_Data / Chromium_Stat) * 100), 2))
    if Chromium_Data > Chromium_Stat:
        Chromium_Colour = "red"
        Chromium_Data = Chromium_Stat
    else:
        Chromium_Colour = "mistyrose2"
    Chromium_Value = round((((Chromium_Data / Chromium_Stat) * 180) + 20), 2)
    Nutrition_Log.create_rectangle(20, 60, Chromium_Value, 70, fill=Chromium_Colour, outline=Chromium_Colour)
    Nutrition_Log.create_text(80, 65, text="Chromium", fill="black", font=("Comic Sans MS", 8))
    Nutrition_Log.create_text(150, 65, text=(Chromium_Percent + "%"), fill="black")
    Nutrition_Log.create_rectangle(20, 60, 200, 70)

    # Copper
    Copper_Stat = float(data_pull[2])
    Copper_Data = float(Copper.get())
    nutri.write(str(Copper_Data) + "\n")
    Copper_Percent = str(round(((Copper_Data / Copper_Stat) * 100), 2))
    if Copper_Data > Copper_Stat:
        Copper_Colour = "red"
        Copper_Data = Copper_Stat
    else:
        Copper_Colour = "mistyrose2"
    Copper_Value = round((((Copper_Data / Copper_Stat) * 180) + 20), 2)
    Nutrition_Log.create_rectangle(20, 75, Copper_Value, 85, fill=Copper_Colour, outline=Copper_Colour)
    Nutrition_Log.create_text(80, 80, text="Copper", fill="black", font=("Comic Sans MS", 8))
    Nutrition_Log.create_text(150, 80, text=(Copper_Percent + "%"), fill="black")
    Nutrition_Log.create_rectangle(20, 75, 200, 85)

    # Fluoride
    Fluoride_Stat = float(data_pull[3])
    Fluoride_Data = float(Fluoride.get())
    nutri.write(str(Fluoride_Data) + "\n")
    Fluoride_Percent = str(round(((Fluoride_Data / Fluoride_Stat) * 100), 2))
    if Fluoride_Data > Fluoride_Stat:
        Fluoride_Colour = "red"
        Fluoride_Data = Fluoride_Stat
    else:
        Fluoride_Colour = "mistyrose2"
    Fluoride_Value = round((((Fluoride_Data / Fluoride_Stat) * 180) + 20), 2)
    Nutrition_Log.create_rectangle(20, 90, Fluoride_Value, 100, fill=Fluoride_Colour, outline=Fluoride_Colour)
    Nutrition_Log.create_text(80, 95, text="Fluoride", fill="black", font=("Comic Sans MS", 8))
    Nutrition_Log.create_text(150, 95, text=(Fluoride_Percent + "%"), fill="black")
    Nutrition_Log.create_rectangle(20, 90, 200, 100)

    # Iodine
    Iodine_Stat = float(data_pull[4])
    Iodine_Data = float(Iodine.get())
    nutri.write(str(Iodine_Data) + "\n")
    Iodine_Percent = str(round(((Iodine_Data / Iodine_Stat) * 100), 2))
    if Iodine_Data > Iodine_Stat:
        Iodine_Colour = "red"
        Iodine_Data = Iodine_Stat
    else:
        Iodine_Colour = "mistyrose2"
    Iodine_Value = round((((Iodine_Data / Iodine_Stat) * 180) + 20), 2)
    Nutrition_Log.create_rectangle(20, 105, Iodine_Value, 115, fill=Iodine_Colour, outline=Iodine_Colour)
    Nutrition_Log.create_text(80, 110, text="Iodine", fill="black", font=("Comic Sans MS", 8))
    Nutrition_Log.create_text(150, 110, text=(Iodine_Percent + "%"), fill="black")
    Nutrition_Log.create_rectangle(20, 105, 200, 115)

    # Iron
    Iron_Stat = float(data_pull[5])
    Iron_Data = float(Iron.get())
    nutri.write(str(Iron_Data) + "\n")
    Iron_Percent = str(round(((Iron_Data / Iron_Stat) * 100), 2))
    if Iron_Data > Iron_Stat:
        Iron_Colour = "red"
        Iron_Data = Iron_Stat
    else:
        Iron_Colour = "mistyrose2"
    Iron_Value = round((((Iron_Data / Iron_Stat) * 180) + 20), 2)
    Nutrition_Log.create_rectangle(20, 120, Iron_Value, 130, fill=Iron_Colour, outline=Iron_Colour)
    Nutrition_Log.create_text(80, 125, text="Iron", fill="black", font=("Comic Sans MS", 8))
    Nutrition_Log.create_text(150, 125, text=(Iron_Percent + "%"), fill="black")
    Nutrition_Log.create_rectangle(20, 120, 200, 130)

    # Magnesium
    Magnesium_Stat = float(data_pull[6])
    Magnesium_Data = float(Magnesium.get())
    nutri.write(str(Magnesium_Data) + "\n")
    Magnesium_Percent = str(round(((Magnesium_Data / Magnesium_Stat) * 100), 2))
    if Magnesium_Data > Magnesium_Stat:
        Magnesium_Colour = "red"
        Magnesium_Data = Magnesium_Stat
    else:
        Magnesium_Colour = "mistyrose2"
    Magnesium_Value = round((((Magnesium_Data / Magnesium_Stat) * 180) + 20), 2)
    Nutrition_Log.create_rectangle(20, 135, Magnesium_Value, 145, fill=Magnesium_Colour, outline=Magnesium_Colour)
    Nutrition_Log.create_text(80, 140, text="Magnesium", fill="black", font=("Comic Sans MS", 8))
    Nutrition_Log.create_text(150, 140, text=(Magnesium_Percent + "%"), fill="black")
    Nutrition_Log.create_rectangle(20, 135, 200, 145)

    # Manganese
    Manganese_Stat = float(data_pull[7])
    Manganese_Data = float(Manganese.get())
    nutri.write(str(Manganese_Data) + "\n")
    Manganese_Percent = str(round(((Manganese_Data / Manganese_Stat) * 100), 2))
    if Manganese_Data > Manganese_Stat:
        Manganese_Colour = "red"
        Manganese_Data = Manganese_Stat
    else:
        Manganese_Colour = "mistyrose2"
    Manganese_Value = round((((Manganese_Data / Manganese_Stat) * 180) + 20), 2)
    Nutrition_Log.create_rectangle(20, 150, Manganese_Value, 160, fill=Manganese_Colour, outline=Manganese_Colour)
    Nutrition_Log.create_text(80, 155, text="Manganese", fill="black", font=("Comic Sans MS", 8))
    Nutrition_Log.create_text(150, 155, text=(Manganese_Percent + "%"), fill="black")
    Nutrition_Log.create_rectangle(20, 150, 200, 160)

    # Molybdenum
    Molybdenum_Stat = float(data_pull[8])
    Molybdenum_Data = float(Molybdenum.get())
    nutri.write(str(Molybdenum_Data) + "\n")
    Molybdenum_Percent = str(round(((Molybdenum_Data / Molybdenum_Stat) * 100), 2))
    if Molybdenum_Data > Molybdenum_Stat:
        Molybdenum_Colour = "red"
        Molybdenum_Data = Molybdenum_Stat
    else:
        Molybdenum_Colour = "mistyrose2"
    Molybdenum_Value = round((((Molybdenum_Data / Molybdenum_Stat) * 180) + 20), 2)
    Nutrition_Log.create_rectangle(20, 165, Molybdenum_Value, 175, fill=Molybdenum_Colour, outline=Molybdenum_Colour)
    Nutrition_Log.create_text(80, 170, text="Molybdenum", fill="black", font=("Comic Sans MS", 8))
    Nutrition_Log.create_text(150, 170, text=(Molybdenum_Percent + "%"), fill="black")
    Nutrition_Log.create_rectangle(20, 165, 200, 175)

    # Phosphorus
    Phosphorus_Stat = float(data_pull[9])
    Phosphorus_Data = float(Phosphorus.get())
    nutri.write(str(Phosphorus_Data) + "\n")
    Phosphorus_Percent = str(round(((Phosphorus_Data / Phosphorus_Stat) * 100), 2))
    if Phosphorus_Data > Phosphorus_Stat:
        Phosphorus_Colour = "red"
        Phosphorus_Data = Phosphorus_Stat
    else:
        Phosphorus_Colour = "mistyrose2"
    Phosphorus_Value = round((((Phosphorus_Data / Phosphorus_Stat) * 180) + 20), 2)
    Nutrition_Log.create_rectangle(20, 180, Phosphorus_Value, 190, fill=Phosphorus_Colour, outline=Phosphorus_Colour)
    Nutrition_Log.create_text(80, 185, text="Phosphorus", fill="black", font=("Comic Sans MS", 8))
    Nutrition_Log.create_text(150, 185, text=(Phosphorus_Percent + "%"), fill="black")
    Nutrition_Log.create_rectangle(20, 180, 200, 190)

    # Selenium
    Selenium_Stat = float(data_pull[10])
    Selenium_Data = float(Selenium.get())
    nutri.write(str(Selenium_Data) + "\n")
    Selenium_Percent = str(round(((Selenium_Data / Selenium_Stat) * 100), 2))
    if Selenium_Data > Selenium_Stat:
        Selenium_Colour = "red"
        Selenium_Data = Selenium_Stat
    else:
        Selenium_Colour = "mistyrose2"
    Selenium_Value = round((((Selenium_Data / Selenium_Stat) * 180) + 20), 2)
    Nutrition_Log.create_rectangle(20, 195, Selenium_Value, 205, fill=Selenium_Colour, outline=Selenium_Colour)
    Nutrition_Log.create_text(80, 200, text="Selenium", fill="black", font=("Comic Sans MS", 8))
    Nutrition_Log.create_text(150, 200, text=(Selenium_Percent + "%"), fill="black")
    Nutrition_Log.create_rectangle(20, 195, 200, 205)

    # Zinc
    Zinc_Stat = float(data_pull[11])
    Zinc_Data = float(Zinc.get())
    nutri.write(str(Zinc_Data) + "\n")
    Zinc_Percent = str(round(((Zinc_Data / Zinc_Stat) * 100), 2))
    if Zinc_Data > Zinc_Stat:
        Zinc_Colour = "red"
        Zinc_Data = Zinc_Stat
    else:
        Zinc_Colour = "mistyrose2"
    Zinc_Value = round((((Zinc_Data / Zinc_Stat) * 180) + 20), 2)
    Nutrition_Log.create_rectangle(20, 210, Zinc_Value, 220, fill=Zinc_Colour, outline=Zinc_Colour)
    Nutrition_Log.create_text(80, 215, text="Zinc", fill="black", font=("Comic Sans MS", 8))
    Nutrition_Log.create_text(150, 215, text=(Zinc_Percent + "%"), fill="black")
    Nutrition_Log.create_rectangle(20, 210, 200, 220)

    # Potassium
    Potassium_Stat = float(data_pull[12])
    Potassium_Data = float(Potassium.get())
    nutri.write(str(Potassium_Data) + "\n")
    Potassium_Percent = str(round(((Potassium_Data / Potassium_Stat) * 100), 2))
    if Potassium_Data > Potassium_Stat:
        Potassium_Colour = "red"
        Potassium_Data = Potassium_Stat
    else:
        Potassium_Colour = "mistyrose2"
    Potassium_Value = round((((Potassium_Data / Potassium_Stat) * 180) + 20), 2)
    Nutrition_Log.create_rectangle(20, 225, Potassium_Value, 235, fill=Potassium_Colour, outline=Potassium_Colour)
    Nutrition_Log.create_text(80, 230, text="Potassium", fill="black", font=("Comic Sans MS", 8))
    Nutrition_Log.create_text(150, 230, text=(Potassium_Percent + "%"), fill="black")
    Nutrition_Log.create_rectangle(20, 225, 200, 235)

    # Sodium
    Sodium_Stat = float(data_pull[13])
    Sodium_Data = float(Sodium.get())
    nutri.write(str(Sodium_Data) + "\n")
    Sodium_Percent = str(round(((Sodium_Data / Sodium_Stat) * 100), 2))
    if Sodium_Data > Sodium_Stat:
        Sodium_Colour = "red"
        Sodium_Data = Sodium_Stat
    else:
        Sodium_Colour = "mistyrose2"
    Sodium_Value = round((((Sodium_Data / Sodium_Stat) * 180) + 20), 2)
    Nutrition_Log.create_rectangle(20, 240, Sodium_Value, 250, fill=Sodium_Colour, outline=Sodium_Colour)
    Nutrition_Log.create_text(80, 245, text="Sodium", fill="black", font=("Comic Sans MS", 8))
    Nutrition_Log.create_text(150, 245, text=(Sodium_Percent + "%"), fill="black")
    Nutrition_Log.create_rectangle(20, 240, 200, 250)

    # Chloride
    Chloride_Stat = float(data_pull[14])
    Chloride_Data = float(Chloride.get())
    nutri.write(str(Chloride_Data) + "\n")
    Chloride_Percent = str(round(((Chloride_Data / Chloride_Stat) * 100), 2))
    if Chloride_Data > Chloride_Stat:
        Chloride_Colour = "red"
        Chloride_Data = Chloride_Stat
    else:
        Chloride_Colour = "mistyrose2"
    Chloride_Value = round((((Chloride_Data / Chloride_Stat) * 180) + 20), 2)
    Nutrition_Log.create_rectangle(20, 255, Chloride_Value, 265, fill=Chloride_Colour, outline=Chloride_Colour)
    Nutrition_Log.create_text(80, 260, text="Chloride", fill="black", font=("Comic Sans MS", 8))
    Nutrition_Log.create_text(150, 260, text=(Chloride_Percent + "%"), fill="black")
    Nutrition_Log.create_rectangle(20, 255, 200, 265)

    # Vitamin_A
    Vitamin_A_Stat = float(data_pull[15])
    Vitamin_A_Data = float(Vitamin_A.get())
    nutri.write(str(Vitamin_A_Data) + "\n")
    Vitamin_A_Percent = str(round(((Vitamin_A_Data / Vitamin_A_Stat) * 100), 2))
    if Vitamin_A_Data > Vitamin_A_Stat:
        Vitamin_A_Colour = "red"
        Vitamin_A_Data = Vitamin_A_Stat
    else:
        Vitamin_A_Colour = "skyblue2"
    Vitamin_A_Value = round((((Vitamin_A_Data / Vitamin_A_Stat) * 180) + 20), 2)
    Nutrition_Log.create_rectangle(20, 270, Vitamin_A_Value, 280, fill=Vitamin_A_Colour, outline=Vitamin_A_Colour)
    Nutrition_Log.create_text(80, 275, text="Vitamin A", fill="black", font=("Comic Sans MS", 8))
    Nutrition_Log.create_text(150, 275, text=(Vitamin_A_Percent + "%"), fill="black")
    Nutrition_Log.create_rectangle(20, 270, 200, 280)

    # Vitamin_C
    Vitamin_C_Stat = float(data_pull[16])
    Vitamin_C_Data = float(Vitamin_C.get())
    nutri.write(str(Vitamin_C_Data) + "\n")
    Vitamin_C_Percent = str(round(((Vitamin_C_Data / Vitamin_C_Stat) * 100), 2))
    if Vitamin_C_Data > Vitamin_C_Stat:
        Vitamin_C_Colour = "red"
        Vitamin_C_Data = Vitamin_C_Stat
    else:
        Vitamin_C_Colour = "skyblue2"
    Vitamin_C_Value = round((((Vitamin_C_Data / Vitamin_C_Stat) * 180) + 20), 2)
    Nutrition_Log.create_rectangle(20, 285, Vitamin_C_Value, 295, fill=Vitamin_C_Colour, outline=Vitamin_C_Colour)
    Nutrition_Log.create_text(80, 290, text="Vitamin C", fill="black", font=("Comic Sans MS", 8))
    Nutrition_Log.create_text(150, 290, text=(Vitamin_C_Percent + "%"), fill="black")
    Nutrition_Log.create_rectangle(20, 285, 200, 295)

    # Vitamin_D
    Vitamin_D_Stat = float(data_pull[17])
    Vitamin_D_Data = float(Vitamin_D.get())
    nutri.write(str(Vitamin_D_Data) + "\n")
    Vitamin_D_Percent = str(round(((Vitamin_D_Data / Vitamin_D_Stat) * 100), 2))
    if Vitamin_D_Data > Vitamin_D_Stat:
        Vitamin_D_Colour = "red"
        Vitamin_D_Data = Vitamin_D_Stat
    else:
        Vitamin_D_Colour = "skyblue2"
    Vitamin_D_Value = round((((Vitamin_D_Data / Vitamin_D_Stat) * 180) + 20), 2)
    Nutrition_Log.create_rectangle(20, 300, Vitamin_D_Value, 310, fill=Vitamin_D_Colour, outline=Vitamin_D_Colour)
    Nutrition_Log.create_text(80, 305, text="Vitamin D", fill="black", font=("Comic Sans MS", 8))
    Nutrition_Log.create_text(150, 305, text=(Vitamin_D_Percent + "%"), fill="black")
    Nutrition_Log.create_rectangle(20, 300, 200, 310)

    # Vitamin_E
    Vitamin_E_Stat = float(data_pull[18])
    Vitamin_E_Data = float(Vitamin_E.get())
    nutri.write(str(Vitamin_E_Data) + "\n")
    Vitamin_E_Percent = str(round(((Vitamin_E_Data / Vitamin_E_Stat) * 100), 2))
    if Vitamin_E_Data > Vitamin_E_Stat:
        Vitamin_E_Colour = "red"
        Vitamin_E_Data = Vitamin_E_Stat
    else:
        Vitamin_E_Colour = "skyblue2"
    Vitamin_E_Value = round((((Vitamin_E_Data / Vitamin_E_Stat) * 180) + 20), 2)
    Nutrition_Log.create_rectangle(20, 315, Vitamin_E_Value, 325, fill=Vitamin_E_Colour, outline=Vitamin_E_Colour)
    Nutrition_Log.create_text(80, 320, text="Vitamin E", fill="black", font=("Comic Sans MS", 8))
    Nutrition_Log.create_text(150, 320, text=(Vitamin_E_Percent + "%"), fill="black")
    Nutrition_Log.create_rectangle(20, 315, 200, 325)

    # Vitamin_K
    Vitamin_K_Stat = float(data_pull[19])
    Vitamin_K_Data = float(Vitamin_K.get())
    nutri.write(str(Vitamin_K_Data) + "\n")
    Vitamin_K_Percent = str(round(((Vitamin_K_Data / Vitamin_K_Stat) * 100), 2))
    if Vitamin_K_Data > Vitamin_K_Stat:
        Vitamin_K_Colour = "red"
        Vitamin_K_Data = Vitamin_K_Stat
    else:
        Vitamin_K_Colour = "skyblue2"
    Vitamin_K_Value = round((((Vitamin_K_Data / Vitamin_K_Stat) * 180) + 20), 2)
    Nutrition_Log.create_rectangle(20, 330, Vitamin_K_Value, 340, fill=Vitamin_K_Colour, outline=Vitamin_K_Colour)
    Nutrition_Log.create_text(80, 335, text="Vitamin K", fill="black", font=("Comic Sans MS", 8))
    Nutrition_Log.create_text(150, 335, text=(Vitamin_K_Percent + "%"), fill="black")
    Nutrition_Log.create_rectangle(20, 330, 200, 340)

    # Thiamin
    Thiamin_Stat = float(data_pull[20])
    Thiamin_Data = float(Thiamin.get())
    nutri.write(str(Thiamin_Data) + "\n")
    Thiamin_Percent = str(round(((Thiamin_Data / Thiamin_Stat) * 100), 2))
    if Thiamin_Data > Thiamin_Stat:
        Thiamin_Colour = "red"
        Thiamin_Data = Thiamin_Stat
    else:
        Thiamin_Colour = "skyblue2"
    Thiamin_Value = round((((Thiamin_Data / Thiamin_Stat) * 180) + 20), 2)
    Nutrition_Log.create_rectangle(20, 345, Thiamin_Value, 355, fill=Thiamin_Colour, outline=Thiamin_Colour)
    Nutrition_Log.create_text(80, 350, text="Thiamin", fill="black", font=("Comic Sans MS", 8))
    Nutrition_Log.create_text(150, 350, text=(Thiamin_Percent + "%"), fill="black")
    Nutrition_Log.create_rectangle(20, 345, 200, 355)

    # Riboflavin
    Riboflavin_Stat = float(data_pull[21])
    Riboflavin_Data = float(Riboflavin.get())
    nutri.write(str(Riboflavin_Data) + "\n")
    Riboflavin_Percent = str(round(((Riboflavin_Data / Riboflavin_Stat) * 100), 2))
    if Riboflavin_Data > Riboflavin_Stat:
        Riboflavin_Colour = "red"
        Riboflavin_Data = Riboflavin_Stat
    else:
        Riboflavin_Colour = "skyblue2"
    Riboflavin_Value = round((((Riboflavin_Data / Riboflavin_Stat) * 180) + 20), 2)
    Nutrition_Log.create_rectangle(20, 360, Riboflavin_Value, 370, fill=Riboflavin_Colour, outline=Riboflavin_Colour)
    Nutrition_Log.create_text(80, 365, text="Riboflavin", fill="black", font=("Comic Sans MS", 8))
    Nutrition_Log.create_text(150, 365, text=(Riboflavin_Percent + "%"), fill="black")
    Nutrition_Log.create_rectangle(20, 360, 200, 370)

    # Niacin
    Niacin_Stat = float(data_pull[22])
    Niacin_Data = float(Niacin.get())
    nutri.write(str(Niacin_Data) + "\n")
    Niacin_Percent = str(round(((Niacin_Data / Niacin_Stat) * 100), 2))
    if Niacin_Data > Niacin_Stat:
        Niacin_Colour = "red"
        Niacin_Data = Niacin_Stat
    else:
        Niacin_Colour = "skyblue2"
    Niacin_Value = round((((Niacin_Data / Niacin_Stat) * 180) + 20), 2)
    Nutrition_Log.create_rectangle(20, 375, Niacin_Value, 385, fill=Niacin_Colour, outline=Niacin_Colour)
    Nutrition_Log.create_text(80, 380, text="Niacin", fill="black", font=("Comic Sans MS", 8))
    Nutrition_Log.create_text(150, 380, text=(Niacin_Percent + "%"), fill="black")
    Nutrition_Log.create_rectangle(20, 375, 200, 385)

    # Vitamin_B6
    Vitamin_B6_Stat = float(data_pull[23])
    Vitamin_B6_Data = float(Vitamin_B6.get())
    nutri.write(str(Vitamin_B6_Data) + "\n")
    Vitamin_B6_Percent = str(round(((Vitamin_B6_Data / Vitamin_B6_Stat) * 100), 2))
    if Vitamin_B6_Data > Vitamin_B6_Stat:
        Vitamin_B6_Colour = "red"
        Vitamin_B6_Data = Vitamin_B6_Stat
    else:
        Vitamin_B6_Colour = "skyblue2"
    Vitamin_B6_Value = round((((Vitamin_B6_Data / Vitamin_B6_Stat) * 180) + 20), 2)
    Nutrition_Log.create_rectangle(20, 390, Vitamin_B6_Value, 400, fill=Vitamin_B6_Colour, outline=Vitamin_B6_Colour)
    Nutrition_Log.create_text(80, 395, text="Vitamin B6", fill="black", font=("Comic Sans MS", 8))
    Nutrition_Log.create_text(150, 395, text=(Vitamin_B6_Percent + "%"), fill="black")
    Nutrition_Log.create_rectangle(20, 390, 200, 400)

    # Folate
    Folate_Stat = float(data_pull[24])
    Folate_Data = float(Folate.get())
    nutri.write(str(Folate_Data) + "\n")
    Folate_Percent = str(round(((Folate_Data / Folate_Stat) * 100), 2))
    if Folate_Data > Folate_Stat:
        Folate_Colour = "red"
        Folate_Data = Folate_Stat
    else:
        Folate_Colour = "skyblue2"
    Folate_Value = round((((Folate_Data / Folate_Stat) * 180) + 20), 2)
    Nutrition_Log.create_rectangle(20, 405, Folate_Value, 415, fill=Folate_Colour, outline=Folate_Colour)
    Nutrition_Log.create_text(80, 410, text="Folate", fill="black", font=("Comic Sans MS", 8))
    Nutrition_Log.create_text(150, 410, text=(Folate_Percent + "%"), fill="black")
    Nutrition_Log.create_rectangle(20, 405, 200, 415)

    # Vitamin_B12
    Vitamin_B12_Stat = float(data_pull[25])
    Vitamin_B12_Data = float(Vitamin_B12.get())
    nutri.write(str(Vitamin_B12_Data) + "\n")
    Vitamin_B12_Percent = str(round(((Vitamin_B12_Data / Vitamin_B12_Stat) * 100), 2))
    if Vitamin_B12_Data > Vitamin_B12_Stat:
        Vitamin_B12_Colour = "red"
        Vitamin_B12_Data = Vitamin_B12_Stat
    else:
        Vitamin_B12_Colour = "skyblue2"
    Vitamin_B12_Value = round((((Vitamin_B12_Data / Vitamin_B12_Stat) * 180) + 20), 2)
    Nutrition_Log.create_rectangle(20, 420, Vitamin_B12_Value, 430, fill=Vitamin_B12_Colour, outline=Vitamin_B12_Colour)
    Nutrition_Log.create_text(80, 425, text="Vitamin B12", fill="black", font=("Comic Sans MS", 8))
    Nutrition_Log.create_text(150, 425, text=(Vitamin_B12_Percent + "%"), fill="black")
    Nutrition_Log.create_rectangle(20, 420, 200, 430)

    # Pantothenic Acid
    Pantothenic_Acid_Stat = float(data_pull[26])
    Pantothenic_Acid_Data = float(Pantothenic_Acid.get())
    nutri.write(str(Pantothenic_Acid_Data) + "\n")
    Pantothenic_Acid_Percent = str(round(((Pantothenic_Acid_Data / Pantothenic_Acid_Stat) * 100), 2))
    if Pantothenic_Acid_Data > Pantothenic_Acid_Stat:
        Pantothenic_Acid_Colour = "red"
        Pantothenic_Acid_Data = Pantothenic_Acid_Stat
    else:
        Pantothenic_Acid_Colour = "skyblue2"
    Pantothenic_Acid_Value = round((((Pantothenic_Acid_Data / Pantothenic_Acid_Stat) * 180) + 20), 2)
    Nutrition_Log.create_rectangle(20, 435, Pantothenic_Acid_Value, 445, fill=Pantothenic_Acid_Colour, outline=Pantothenic_Acid_Colour)
    Nutrition_Log.create_text(80, 440, text="Pantothenic Acid", fill="black", font=("Comic Sans MS", 8))
    Nutrition_Log.create_text(150, 440, text=(Pantothenic_Acid_Percent + "%"), fill="black")
    Nutrition_Log.create_rectangle(20, 435, 200, 445)

    # Biotin
    Biotin_Stat = float(data_pull[27])
    Biotin_Data = float(Biotin.get())
    nutri.write(str(Biotin_Data) + "\n")
    Biotin_Percent = str(round(((Biotin_Data / Biotin_Stat) * 100), 2))
    if Biotin_Data > Biotin_Stat:
        Biotin_Colour = "red"
        Biotin_Data = Biotin_Stat
    else:
        Biotin_Colour = "skyblue2"
    Biotin_Value = round((((Biotin_Data / Biotin_Stat) * 180) + 20), 2)
    Nutrition_Log.create_rectangle(20, 450, Biotin_Value, 460, fill=Biotin_Colour, outline=Biotin_Colour)
    Nutrition_Log.create_text(80, 455, text="Biotin", fill="black", font=("Comic Sans MS", 8))
    Nutrition_Log.create_text(150, 455, text=(Biotin_Percent + "%"), fill="black")
    Nutrition_Log.create_rectangle(20, 450, 200, 460)

    # Choline
    Choline_Stat = float(data_pull[28])
    Choline_Data = float(Choline.get())
    nutri.write(str(Choline_Data) + "\n")
    Choline_Percent = str(round(((Choline_Data / Choline_Stat) * 100), 2))
    if Choline_Data > Choline_Stat:
        Choline_Colour = "red"
        Choline_Data = Choline_Stat
    else:
        Choline_Colour = "skyblue2"
    Choline_Value = round((((Choline_Data / Choline_Stat) * 180) + 20), 2)
    Nutrition_Log.create_rectangle(20, 465, Choline_Value, 475, fill=Choline_Colour, outline=Choline_Colour)
    Nutrition_Log.create_text(80, 470, text="Choline", fill="black", font=("Comic Sans MS", 8))
    Nutrition_Log.create_text(150, 470, text=(Choline_Percent + "%"), fill="black")
    Nutrition_Log.create_rectangle(20, 465, 200, 475)

    # Protein
    Protein_Stat = float(data_pull[29])
    Protein_Data = float(Protein.get())
    nutri.write(str(Protein_Data) + "\n")
    Protein_Percent = str(round(((Protein_Data / Protein_Stat) * 100), 2))
    if Protein_Data > Protein_Stat:
        Protein_Colour = "red"
        Protein_Data = Protein_Stat
    else:
        Protein_Colour = "lightgreen"
    Protein_Value = round((((Protein_Data / Protein_Stat) * 180) + 20), 2)
    Nutrition_Log.create_rectangle(20, 480, Protein_Value, 490, fill=Protein_Colour, outline=Protein_Colour)
    Nutrition_Log.create_text(80, 485, text="Protein", fill="black", font=("Comic Sans MS", 8))
    Nutrition_Log.create_text(150, 485, text=(Protein_Percent + "%"), fill="black")
    Nutrition_Log.create_rectangle(20, 480, 200, 490)

    # Carbohydrate
    Carbohydrate_Stat = float(data_pull[30])
    Carbohydrate_Data = float(Carbohydrate.get())
    nutri.write(str(Carbohydrate_Data) + "\n")
    Carbohydrate_Percent = str(round(((Carbohydrate_Data / Carbohydrate_Stat) * 100), 2))
    if Carbohydrate_Data > Carbohydrate_Stat:
        Carbohydrate_Colour = "red"
        Carbohydrate_Data = Carbohydrate_Stat
    else:
        Carbohydrate_Colour = "lightgreen"
    Carbohydrate_Value = round((((Carbohydrate_Data / Carbohydrate_Stat) * 180) + 20), 2)
    Nutrition_Log.create_rectangle(20, 495, Carbohydrate_Value, 505, fill=Carbohydrate_Colour, outline=Carbohydrate_Colour)
    Nutrition_Log.create_text(80, 500, text="Carbohydrate", fill="black", font=("Comic Sans MS", 8))
    Nutrition_Log.create_text(150, 500, text=(Carbohydrate_Percent + "%"), fill="black")
    Nutrition_Log.create_rectangle(20, 495, 200, 505)

    # Fiber
    Fiber_Stat = float(data_pull[31])
    Fiber_Data = float(Fiber.get())
    nutri.write(str(Fiber_Data) + "\n")
    Fiber_Percent = str(round(((Fiber_Data / Fiber_Stat) * 100), 2))
    if Fiber_Data > Fiber_Stat:
        Fiber_Colour = "red"
        Fiber_Data = Fiber_Stat
    else:
        Fiber_Colour = "lightgreen"
    Fiber_Value = round((((Fiber_Data / Fiber_Stat) * 180) + 20), 2)
    Nutrition_Log.create_rectangle(20, 510, Fiber_Value, 520, fill=Fiber_Colour, outline=Fiber_Colour)
    Nutrition_Log.create_text(80, 515, text="Fiber", fill="black", font=("Comic Sans MS", 8))
    Nutrition_Log.create_text(150, 515, text=(Fiber_Percent + "%"), fill="black")
    Nutrition_Log.create_rectangle(20, 510, 200, 520)

    # Linoleic Acid
    Linoleic_Acid_Stat = float(data_pull[32])
    Linoleic_Acid_Data = float(Linoleic_Acid.get())
    nutri.write(str(Linoleic_Acid_Data) + "\n")
    Linoleic_Acid_Percent = str(round(((Linoleic_Acid_Data / Linoleic_Acid_Stat) * 100), 2))
    if Linoleic_Acid_Data > Linoleic_Acid_Stat:
        Linoleic_Acid_Colour = "red"
        Linoleic_Acid_Data = Linoleic_Acid_Stat
    else:
        Linoleic_Acid_Colour = "lightgreen"
    Linoleic_Acid_Value = round((((Linoleic_Acid_Data / Linoleic_Acid_Stat) * 180) + 20), 2)
    Nutrition_Log.create_rectangle(20, 525, Linoleic_Acid_Value, 535, fill=Linoleic_Acid_Colour, outline=Linoleic_Acid_Colour)
    Nutrition_Log.create_text(80, 530, text="Linoleic Acid", fill="black", font=("Comic Sans MS", 8))
    Nutrition_Log.create_text(150, 530, text=(Linoleic_Acid_Percent + "%"), fill="black")
    Nutrition_Log.create_rectangle(20, 525, 200, 535)

    # Alpha Linoleic Acid
    Alpha_Linoleic_Acid_Stat = float(data_pull[33])
    Alpha_Linoleic_Acid_Data = float(Alpha_Linoleic_Acid.get())
    nutri.write(str(Alpha_Linoleic_Acid_Data) + "\n")
    Alpha_Linoleic_Acid_Percent = str(round(((Alpha_Linoleic_Acid_Data / Alpha_Linoleic_Acid_Stat) * 100), 2))
    if Alpha_Linoleic_Acid_Data > Alpha_Linoleic_Acid_Stat:
        Alpha_Linoleic_Acid_Colour = "red"
        Alpha_Linoleic_Acid_Data = Alpha_Linoleic_Acid_Stat
    else:
        Alpha_Linoleic_Acid_Colour = "lightgreen"
    Alpha_Linoleic_Acid_Value = round((((Alpha_Linoleic_Acid_Data / Alpha_Linoleic_Acid_Stat) * 180) + 20), 2)
    Nutrition_Log.create_rectangle(20, 540, Alpha_Linoleic_Acid_Value, 550, fill=Alpha_Linoleic_Acid_Colour, outline=Alpha_Linoleic_Acid_Colour)
    Nutrition_Log.create_text(80, 545, text="α-Linoleic Acid", fill="black", font=("Comic Sans MS", 8))
    Nutrition_Log.create_text(150, 545, text=(Alpha_Linoleic_Acid_Percent + "%"), fill="black")
    Nutrition_Log.create_rectangle(20, 540, 200, 550)

    #close storage
    nutri.close()

    #check for empty files and delete
    empty_check = open(polyfile + polyfile_dir + nutri_log, "r", encoding="utf8")
    zero = empty_check.read().splitlines()
    empty_check.close()
    count = 0
    for x in zero:
        value = float(x)
        if value > 0:
            count = count + 1
    if count == 0:
        os.remove(polyfile + polyfile_dir + nutri_log)

#Nutrition Data Metrics Discretionary Nutrients Input
def Discretionary_Nutrients():
    Discretionary.delete("all")
    Discretionary.create_text(170, 20, text="DISCRETIONARY NUTRIENTS",
                              font=("Comic Sans MS", 10))
    Discretionary.create_line(0, 35, 340, 35)
    Discretionary.create_rectangle(3, 3, 341, 350, width=2, outline="grey")  # Border
    Discretionary.create_text(110, 60, text="Total Fat:", font=("Comic Sans MS", 10))
    Discretionary.create_text(110, 160, text="Saturated Fat:", font=("Comic Sans MS", 10))
    Discretionary.create_text(110, 260, text="Cholesterol:", font=("Comic Sans MS", 10))
    Discretionary.create_text(205, 60, text="(grams)", font=("Comic Sans MS", 10))
    Discretionary.create_text(220, 160, text="(grams)", font=("Comic Sans MS", 10))
    Discretionary.create_text(223, 260, text="(milligrams)", font=("Comic Sans MS", 10))
    Discretionary.create_text(170, 78, text="Maximum Total Fat Per Day = 77 grams", font=("Comic Sans MS", 10))
    Discretionary.create_text(170, 178, text="Maximum Saturated Fat Per Day = 22 grams", font=("Comic Sans MS", 10))
    Discretionary.create_text(170, 278, text="Maximum Cholesterol Intake Per Day = 300mg", font=("Comic Sans MS", 10))

    #fetch data:
    total_fat = float(Total_Fat.get())
    TF = 40 + ((total_fat/77) * 260)
    saturated_fat = float(Saturated_Fat.get())
    SF = 40 + ((saturated_fat / 22) * 260)
    cholesterol = float(Cholesterol.get())
    CH = 40 + ((cholesterol / 300) * 260)
    if total_fat > 77:
        TF = 300
    if saturated_fat > 22:
        SF = 300
    if cholesterol > 300:
        CH = 300

    #Display Boxes:
    Discretionary.create_rectangle(40, 90, TF, 110, fill="red")
    Discretionary.create_rectangle(40, 90, 300, 110)
    Discretionary.create_rectangle(40, 190, SF, 210, fill="red")
    Discretionary.create_rectangle(40, 190, 300, 210)
    Discretionary.create_rectangle(40, 290, CH, 310, fill="red")
    Discretionary.create_rectangle(40, 290, 300, 310)

    if total_fat > 77:
        Discretionary.create_text(170, 100, text="ABOVE DAILY MAXIMUM!",
                                  font=("Comic Sans MS", 10))
    if saturated_fat > 22:
        Discretionary.create_text(170, 200, text="ABOVE DAILY MAXIMUM!",
                                  font=("Comic Sans MS", 10))
    if cholesterol > 300:
        Discretionary.create_text(170, 300, text="ABOVE DAILY MAXIMUM!",
                                  font=("Comic Sans MS", 10))
def clear_garbage():
    day_fetch = str(DayN.get())
    month_fetch = str(MonthN.get())
    year_fetch = str(YearN.get())
    polyfile_dir = "/" + day_fetch + month_fetch + year_fetch
    w_path = "/DD_store.txt"
    if path.exists(polyfile + polyfile_dir + w_path):
        get = open(polyfile + polyfile_dir + w_path, "r", encoding="utf8")
        get_d = get.read().splitlines()
        get.close()
        one = float(get_d[0])
        two = float(get_d[1])
        three = float(get_d[2])
        if (one == 0) and (two == 0) and (three == 0):
            os.remove(polyfile + polyfile_dir + w_path)

#Discretionary Nutrients Update
def discretionary_update():
    day_fetch = str(DayN.get())
    month_fetch = str(MonthN.get())
    year_fetch = str(YearN.get())
    polyfile_dir = "/" + day_fetch + month_fetch + year_fetch
    w_path = "/DD_store.txt"
    if path.exists(polyfile + polyfile_dir + w_path):
        read_d = open(polyfile + polyfile_dir + w_path, "r", encoding="utf8")
        data_get = read_d.read().splitlines()
        read_d.close()
        Total_Fat.config(state="normal")
        Total_Fat.delete(0, "end")
        Total_Fat.insert(0, data_get[0])
        Total_Fat.config(state="readonly")

        Saturated_Fat.config(state="normal")
        Saturated_Fat.delete(0, "end")
        Saturated_Fat.insert(0, data_get[1])
        Saturated_Fat.config(state="readonly")

        Cholesterol.config(state="normal")
        Cholesterol.delete(0, "end")
        Cholesterol.insert(0, data_get[2])
        Cholesterol.config(state="readonly")
    else:
        Total_Fat.config(state="normal")
        Total_Fat.delete(0, "end")
        Total_Fat.insert(0, 0.0)
        Total_Fat.config(state="readonly")

        Saturated_Fat.config(state="normal")
        Saturated_Fat.delete(0, "end")
        Saturated_Fat.insert(0, 0.0)
        Saturated_Fat.config(state="readonly")

        Cholesterol.config(state="normal")
        Cholesterol.delete(0, "end")
        Cholesterol.insert(0, 0)
        Cholesterol.config(state="readonly")
    clear_garbage()
    Discretionary_Nutrients()

#Discretionary Nutrients Storage
def discrete_store():
    t_fat = Total_Fat.get()
    s_fat = Saturated_Fat.get()
    choles = Cholesterol.get()

    #write data
    day_fetch = str(DayN.get())
    month_fetch = str(MonthN.get())
    year_fetch = str(YearN.get())
    polyfile_dir = "/" + day_fetch + month_fetch + year_fetch
    w_path = "/DD_store.txt"
    write_d = open(polyfile + polyfile_dir + w_path, "w", encoding="utf8")
    write_d.write(t_fat + "\n")
    write_d.write(s_fat + "\n")
    write_d.write(choles + "\n")
    write_d.close()
    clear_garbage()
    Discretionary_Nutrients()

Total_Fat = tkinter.Spinbox(Nutrition_Data_Metrics, width=4, from_=0, to=200, increment=0.1, state="readonly",
                          command=discrete_store)
Total_Fat.place(x=836, y=300)

Saturated_Fat = tkinter.Spinbox(Nutrition_Data_Metrics, width=4, from_=0, to=200, increment=0.1, state="readonly",
                          command=discrete_store)
Saturated_Fat.place(x=852, y=400)

Cholesterol = tkinter.Spinbox(Nutrition_Data_Metrics, width=4, from_=0, to=300, increment=1, state="readonly",
                          command=discrete_store)
Cholesterol.place(x=841, y=500)

Discretionary_Nutrients()
#Nutrition Data Metrics Macronutrients Input
def Draw_Macronutrients():
    Macronutrients.create_text(110, 20, text="MACRONUTRIENTS", font=("Comic Sans MS", 10))
    Macronutrients.create_rectangle(3, 3, 341, 185, width=2, outline="grey")#Border
    Macronutrients.create_text(280, 20, text="          Dietary\nReference Intakes",
                         font=("Comic Sans MS", 8))
    Macronutrients.create_line(220, 0, 220, 185)
    Macronutrients.create_line(0, 35, 340, 35)
    Macronutrients.create_line(0, 65, 340, 65)
    Macronutrients.create_line(0, 95, 340, 95)
    Macronutrients.create_line(0, 125, 340, 125)
    Macronutrients.create_line(0, 155, 340, 155)
    #Macronutrients.create_line(0, 185, 340, 185)
    Macronutrients.create_text(95, 50, text="Protein:", font=("Comic Sans MS", 10))
    Macronutrients.create_text(173, 50, text="(g/d)", font=("Comic Sans MS", 8))
    Macronutrients.create_text(75, 80, text="Carbohydrate:", font=("Comic Sans MS", 10))
    Macronutrients.create_text(173, 80, text="(g/d)", font=("Comic Sans MS", 8))
    Macronutrients.create_text(99, 110, text="Fiber:", font=("Comic Sans MS", 10))
    Macronutrients.create_text(173, 110, text="(g/d)", font=("Comic Sans MS", 8))
    Macronutrients.create_text(76, 140, text="Linoleic Acid:", font=("Comic Sans MS", 10))
    Macronutrients.create_text(173, 140, text="(g/d)", font=("Comic Sans MS", 8))
    Macronutrients.create_text(70, 170, text="α-Linoleic Acid:", font=("Comic Sans MS", 10))
    Macronutrients.create_text(173, 170, text="(g/d)", font=("Comic Sans MS", 8))
Draw_Macronutrients()

#Macronutrients Spinboxes
Protein = tkinter.Spinbox(Nutrition_Data_Metrics, width=4, from_=0, to=200, increment=0.1, state="readonly",
                          command=Draw_Nutrition_Log)
Protein.place(x=815, y=100)

Carbohydrate = tkinter.Spinbox(Nutrition_Data_Metrics, width=4, from_=0, to=500, increment=1, state="readonly",
                          command=Draw_Nutrition_Log)
Carbohydrate.place(x=815, y=130)

Fiber = tkinter.Spinbox(Nutrition_Data_Metrics, width=4, from_=0, to=150, increment=0.1, state="readonly",
                          command=Draw_Nutrition_Log)
Fiber.place(x=815, y=160)

Linoleic_Acid = tkinter.Spinbox(Nutrition_Data_Metrics, width=4, from_=0, to=200, increment=0.1, state="readonly",
                          command=Draw_Nutrition_Log)
Linoleic_Acid.place(x=815, y=190)

Alpha_Linoleic_Acid = tkinter.Spinbox(Nutrition_Data_Metrics, width=4, from_=0, to=20, increment=0.01, state="readonly",
                          command=Draw_Nutrition_Log)
Alpha_Linoleic_Acid.place(x=815, y=220)

#Nutrition Data Metrics Vitamins Input
def Draw_Vitamins():
    Vitamins.create_rectangle(3, 3, 340, 485, width=2, outline="grey") #Border
    Vitamins.create_text(280, 20, text="          Dietary\nReference Intakes",
                         font=("Comic Sans MS", 8))
    Vitamins.create_line(220, 0, 220, 455)
    Vitamins.create_line(0, 35, 340, 35)
    Vitamins.create_line(0, 65, 340, 65)
    Vitamins.create_line(0, 95, 340, 95)
    Vitamins.create_line(0, 125, 340, 125)
    Vitamins.create_line(0, 155, 340, 155)
    Vitamins.create_line(0, 185, 340, 185)
    Vitamins.create_line(0, 215, 340, 215)
    Vitamins.create_line(0, 245, 340, 245)
    Vitamins.create_line(0, 275, 340, 275)
    Vitamins.create_line(0, 305, 340, 305)
    Vitamins.create_line(0, 335, 340, 335)
    Vitamins.create_line(0, 365, 340, 365)
    Vitamins.create_line(0, 395, 340, 395)
    Vitamins.create_line(0, 425, 340, 425)
    Vitamins.create_line(0, 455, 340, 455)
    Vitamins.create_text(110, 20, text="VITAMINS", font=("Comic Sans MS", 10))
    Vitamins.create_text(93, 50, text="Vitamin A:", font=("Comic Sans MS", 10))
    Vitamins.create_text(182, 50, text="(μg/d)", font=("Comic Sans MS", 8))
    Vitamins.create_text(93, 80, text="Vitamin C:", font=("Comic Sans MS", 10))
    Vitamins.create_text(182, 80, text="(mg/d)", font=("Comic Sans MS", 8))
    Vitamins.create_text(93, 110, text="Vitamin D:", font=("Comic Sans MS", 10))
    Vitamins.create_text(182, 110, text="(μg/d)", font=("Comic Sans MS", 8))
    Vitamins.create_text(93, 140, text="Vitamin E:", font=("Comic Sans MS", 10))
    Vitamins.create_text(182, 140, text="(mg/d)", font=("Comic Sans MS", 8))
    Vitamins.create_text(93, 170, text="Vitamin K:", font=("Comic Sans MS", 10))
    Vitamins.create_text(182, 170, text="(μg/d)", font=("Comic Sans MS", 8))
    Vitamins.create_text(97, 200, text="Thiamin:", font=("Comic Sans MS", 10))
    Vitamins.create_text(182, 200, text="(mg/d)", font=("Comic Sans MS", 8))
    Vitamins.create_text(91, 230, text="Riboflavin:", font=("Comic Sans MS", 10))
    Vitamins.create_text(182, 230, text="(mg/d)", font=("Comic Sans MS", 8))
    Vitamins.create_text(101, 260, text="Niacin:", font=("Comic Sans MS", 10))
    Vitamins.create_text(182, 260, text="(mg/d)", font=("Comic Sans MS", 8))
    Vitamins.create_text(90, 290, text="Vitamin B6:", font=("Comic Sans MS", 10))
    Vitamins.create_text(182, 290, text="(mg/d)", font=("Comic Sans MS", 8))
    Vitamins.create_text(102, 320, text="Folate:", font=("Comic Sans MS", 10))
    Vitamins.create_text(182, 320, text="(μg/d)", font=("Comic Sans MS", 8))
    Vitamins.create_text(87, 350, text="Vitamin B12:", font=("Comic Sans MS", 10))
    Vitamins.create_text(182, 350, text="(μg/d)", font=("Comic Sans MS", 8))
    Vitamins.create_text(71, 380, text="Pantothenic Acid:", font=("Comic Sans MS", 10))
    Vitamins.create_text(182, 380, text="(mg/d)", font=("Comic Sans MS", 8))
    Vitamins.create_text(104, 410, text="Biotin:", font=("Comic Sans MS", 10))
    Vitamins.create_text(182, 410, text="(μg/d)", font=("Comic Sans MS", 8))
    Vitamins.create_text(100, 440, text="Choline:", font=("Comic Sans MS", 10))
    Vitamins.create_text(182, 440, text="(mg/d)", font=("Comic Sans MS", 8))
Draw_Vitamins()

#Vitamins Spinboxes
Vitamin_A = tkinter.Spinbox(Nutrition_Data_Metrics, width=4, from_=0, to=2000, increment=5, state="readonly",
                            command=Draw_Nutrition_Log)
Vitamin_A.place(x=475, y=155)

Vitamin_C = tkinter.Spinbox(Nutrition_Data_Metrics, width=4, from_=0, to=2000, increment=0.1, state="readonly",
                            command=Draw_Nutrition_Log)
Vitamin_C.place(x=475, y=185)

Vitamin_D = tkinter.Spinbox(Nutrition_Data_Metrics, width=4, from_=0, to=100, increment=0.01, state="readonly",
                            command=Draw_Nutrition_Log)
Vitamin_D.place(x=475, y=215)

Vitamin_E = tkinter.Spinbox(Nutrition_Data_Metrics, width=4, from_=0, to=100, increment=0.01, state="readonly",
                            command=Draw_Nutrition_Log)
Vitamin_E.place(x=475, y=245)

Vitamin_K = tkinter.Spinbox(Nutrition_Data_Metrics, width=4, from_=0, to=500, increment=1, state="readonly",
                            command=Draw_Nutrition_Log)
Vitamin_K.place(x=475, y=275)

Thiamin = tkinter.Spinbox(Nutrition_Data_Metrics, width=4, from_=0, to=20, increment=0.01, state="readonly",
                            command=Draw_Nutrition_Log)
Thiamin.place(x=475, y=305)

Riboflavin = tkinter.Spinbox(Nutrition_Data_Metrics, width=4, from_=0, to=20, increment=0.01, state="readonly",
                            command=Draw_Nutrition_Log)
Riboflavin.place(x=475, y=335)

Niacin = tkinter.Spinbox(Nutrition_Data_Metrics, width=4, from_=0, to=100, increment=0.1, state="readonly",
                            command=Draw_Nutrition_Log)
Niacin.place(x=475, y=365)

Vitamin_B6 = tkinter.Spinbox(Nutrition_Data_Metrics, width=4, from_=0, to=20, increment=0.01, state="readonly",
                            command=Draw_Nutrition_Log)
Vitamin_B6.place(x=475, y=395)

Folate = tkinter.Spinbox(Nutrition_Data_Metrics, width=4, from_=0, to=2000, increment=1, state="readonly",
                            command=Draw_Nutrition_Log)
Folate.place(x=475, y=425)

Vitamin_B12 = tkinter.Spinbox(Nutrition_Data_Metrics, width=4, from_=0, to=20, increment=0.01, state="readonly",
                            command=Draw_Nutrition_Log)
Vitamin_B12.place(x=475, y=455)

Pantothenic_Acid = tkinter.Spinbox(Nutrition_Data_Metrics, width=4, from_=0, to=50, increment=0.01, state="readonly",
                            command=Draw_Nutrition_Log)
Pantothenic_Acid.place(x=475, y=485)

Biotin = tkinter.Spinbox(Nutrition_Data_Metrics, width=4, from_=0, to=200, increment=0.1, state="readonly",
                            command=Draw_Nutrition_Log)
Biotin.place(x=475, y=515)

Choline = tkinter.Spinbox(Nutrition_Data_Metrics, width=4, from_=0, to=2000, increment=1, state="readonly",
                            command=Draw_Nutrition_Log)
Choline.place(x=475, y=545)

#Nutrition Data Metrics Elements Input
def Draw_Elements():
    Elements.create_rectangle(3, 3, 340, 485, width=2, outline="grey") #Border
    Elements.create_text(110, 20, text="ELEMENTS", font=("Comic Sans MS", 10))
    Elements.create_text(280, 20, text="          Dietary\nReference Intakes",
                         font=("Comic Sans MS", 8))
    Elements.create_line(220, 0, 220, 485)
    Elements.create_line(0, 35, 340, 35)
    Elements.create_line(0, 65, 340, 65)
    Elements.create_line(0, 95, 340, 95)
    Elements.create_line(0, 125, 340, 125)
    Elements.create_line(0, 155, 340, 155)
    Elements.create_line(0, 185, 340, 185)
    Elements.create_line(0, 215, 340, 215)
    Elements.create_line(0, 245, 340, 245)
    Elements.create_line(0, 275, 340, 275)
    Elements.create_line(0, 305, 340, 305)
    Elements.create_line(0, 335, 340, 335)
    Elements.create_line(0, 365, 340, 365)
    Elements.create_line(0, 395, 340, 395)
    Elements.create_line(0, 425, 340, 425)
    Elements.create_line(0, 455, 340, 455)
    Elements.create_text(86, 50, text="Calcium:", font=("Comic Sans MS", 10))
    Elements.create_text(172, 50, text="(mg/d)", font=("Comic Sans MS", 8))
    Elements.create_text(80, 80, text="Chromium:", font=("Comic Sans MS", 10))
    Elements.create_text(172, 80, text="(μg/d)", font=("Comic Sans MS", 8))
    Elements.create_text(87, 110, text="Copper:", font=("Comic Sans MS", 10))
    Elements.create_text(172, 110, text="(μg/d)", font=("Comic Sans MS", 8))
    Elements.create_text(82, 140, text="Fluoride:", font=("Comic Sans MS", 10))
    Elements.create_text(172, 140, text="(mg/d)", font=("Comic Sans MS", 8))
    Elements.create_text(88, 170, text="Iodine:", font=("Comic Sans MS", 10))
    Elements.create_text(172, 170, text="(μg/d)", font=("Comic Sans MS", 8))
    Elements.create_text(95, 200, text="Iron:", font=("Comic Sans MS", 10))
    Elements.create_text(172, 200, text="(mg/d)", font=("Comic Sans MS", 8))
    Elements.create_text(75, 230, text="Magnesium:", font=("Comic Sans MS", 10))
    Elements.create_text(172, 230, text="(mg/d)", font=("Comic Sans MS", 8))
    Elements.create_text(75, 260, text="Manganese:", font=("Comic Sans MS", 10))
    Elements.create_text(172, 260, text="(mg/d)", font=("Comic Sans MS", 8))
    Elements.create_text(70, 290, text="Molybdenum:", font=("Comic Sans MS", 10))
    Elements.create_text(172, 290, text="(μg/d)", font=("Comic Sans MS", 8))
    Elements.create_text(74, 320, text="Phosphorus:", font=("Comic Sans MS", 10))
    Elements.create_text(172, 320, text="(mg/d)", font=("Comic Sans MS", 8))
    Elements.create_text(81, 350, text="Selenium:", font=("Comic Sans MS", 10))
    Elements.create_text(172, 350, text="(μg/d)", font=("Comic Sans MS", 8))
    Elements.create_text(95, 380, text="Zinc:", font=("Comic Sans MS", 10))
    Elements.create_text(172, 380, text="(mg/d)", font=("Comic Sans MS", 8))
    Elements.create_text(79, 410, text="Potassium:", font=("Comic Sans MS", 10))
    Elements.create_text(172, 410, text="(mg/d)", font=("Comic Sans MS", 8))
    Elements.create_text(86, 440, text="Sodium:", font=("Comic Sans MS", 10))
    Elements.create_text(172, 440, text="(mg/d)", font=("Comic Sans MS", 8))
    Elements.create_text(83, 470, text="Chloride:", font=("Comic Sans MS", 10))
    Elements.create_text(172, 470, text="(g/d)", font=("Comic Sans MS", 8))
Draw_Elements()

#Elements Spinboxes
Calcium = tkinter.Spinbox(Nutrition_Data_Metrics, width=4, from_=0, to=2000, increment=5, state="readonly",
                          command=Draw_Nutrition_Log)
Calcium.place(x=120, y=155)

Chromium = tkinter.Spinbox(Nutrition_Data_Metrics, width=4, from_=0, to=100, increment=0.1, state="readonly",
                           command=Draw_Nutrition_Log)
Chromium.place(x=120, y=185)

Copper = tkinter.Spinbox(Nutrition_Data_Metrics, width=4, from_=0, to=2000, increment=5, state="readonly",
                         command=Draw_Nutrition_Log)
Copper.place(x=120, y=215)

Fluoride = tkinter.Spinbox(Nutrition_Data_Metrics, width=4, from_=0, to=20, increment=0.01, state="readonly",
                           command=Draw_Nutrition_Log)
Fluoride.place(x=120, y=245)

Iodine = tkinter.Spinbox(Nutrition_Data_Metrics, width=4, from_=0, to=200, increment=1, state="readonly",
                         command=Draw_Nutrition_Log)
Iodine.place(x=120, y=275)

Iron = tkinter.Spinbox(Nutrition_Data_Metrics, width=4, from_=0, to=50, increment=0.01, state="readonly",
                       command=Draw_Nutrition_Log)
Iron.place(x=120, y=305)

Magnesium = tkinter.Spinbox(Nutrition_Data_Metrics, width=4, from_=0, to=1000, increment=1, state="readonly",
                            command=Draw_Nutrition_Log)
Magnesium.place(x=120, y=335)

Manganese = tkinter.Spinbox(Nutrition_Data_Metrics, width=4, from_=0, to=10, increment=0.01, state="readonly",
                            command=Draw_Nutrition_Log)
Manganese.place(x=120, y=365)

Molybdenum = tkinter.Spinbox(Nutrition_Data_Metrics, width=4, from_=0, to=100, increment=0.1, state="readonly",
                             command=Draw_Nutrition_Log)
Molybdenum.place(x=120, y=395)

Phosphorus = tkinter.Spinbox(Nutrition_Data_Metrics, width=4, from_=0, to=1200, increment=5, state="readonly",
                             command=Draw_Nutrition_Log)
Phosphorus.place(x=120, y=425)

Selenium = tkinter.Spinbox(Nutrition_Data_Metrics, width=4, from_=0, to=150, increment=0.1, state="readonly",
                           command=Draw_Nutrition_Log)
Selenium.place(x=120, y=455)

Zinc = tkinter.Spinbox(Nutrition_Data_Metrics, width=4, from_=0, to=50, increment=0.01, state="readonly",
                       command=Draw_Nutrition_Log)
Zinc.place(x=120, y=485)

Potassium = tkinter.Spinbox(Nutrition_Data_Metrics, width=4, from_=0, to=5000, increment=5, state="readonly",
                            command=Draw_Nutrition_Log)
Potassium.place(x=120, y=515)

Sodium = tkinter.Spinbox(Nutrition_Data_Metrics, width=4, from_=0, to=9999, increment=5, state="readonly",
                         command=Draw_Nutrition_Log)
Sodium.place(x=120, y=545)

Chloride = tkinter.Spinbox(Nutrition_Data_Metrics, width=4, from_=0, to=10, increment=0.01, state="readonly",
                           command=Draw_Nutrition_Log)
Chloride.place(x=120, y=575)

def update_nutrition_spinboxes():
    # fetch date info
    day_fetch = str(DayN.get())
    month_fetch = str(MonthN.get())
    year_fetch = str(YearN.get())
    polyfile_dir = "/" + day_fetch + month_fetch + year_fetch
    nutri_log = "/Nutrition_Log.txt"
    if path.exists(polyfile + polyfile_dir + nutri_log):
        nutri = open(polyfile + polyfile_dir + nutri_log, "r", encoding="utf8")
        data = nutri.read().splitlines()
        nutri.close()
        # Calcium
        Calcium.config(state="normal")
        Calcium.delete(0, "end")
        Calcium.insert(0, data[0])
        Calcium.config(state="readonly")

        # Chromium
        Chromium.config(state="normal")
        Chromium.delete(0, "end")
        Chromium.insert(0, data[1])
        Chromium.config(state="readonly")

        # Copper
        Copper.config(state="normal")
        Copper.delete(0, "end")
        Copper.insert(0, data[2])
        Copper.config(state="readonly")

        # Fluoride
        Fluoride.config(state="normal")
        Fluoride.delete(0, "end")
        Fluoride.insert(0, data[3])
        Fluoride.config(state="readonly")

        # Iodine
        Iodine.config(state="normal")
        Iodine.delete(0, "end")
        Iodine.insert(0, data[4])
        Iodine.config(state="readonly")

        # Iron
        Iron.config(state="normal")
        Iron.delete(0, "end")
        Iron.insert(0, data[5])
        Iron.config(state="readonly")

        # Magnesium
        Magnesium.config(state="normal")
        Magnesium.delete(0, "end")
        Magnesium.insert(0, data[6])
        Magnesium.config(state="readonly")

        # Manganese
        Manganese.config(state="normal")
        Manganese.delete(0, "end")
        Manganese.insert(0, data[7])
        Manganese.config(state="readonly")

        # Molybdenum
        Molybdenum.config(state="normal")
        Molybdenum.delete(0, "end")
        Molybdenum.insert(0, data[8])
        Molybdenum.config(state="readonly")

        # Phosphorus
        Phosphorus.config(state="normal")
        Phosphorus.delete(0, "end")
        Phosphorus.insert(0, data[9])
        Phosphorus.config(state="readonly")

        # Selenium
        Selenium.config(state="normal")
        Selenium.delete(0, "end")
        Selenium.insert(0, data[10])
        Selenium.config(state="readonly")

        # Zinc
        Zinc.config(state="normal")
        Zinc.delete(0, "end")
        Zinc.insert(0, data[11])
        Zinc.config(state="readonly")

        # Potassium
        Potassium.config(state="normal")
        Potassium.delete(0, "end")
        Potassium.insert(0, data[12])
        Potassium.config(state="readonly")

        # Sodium
        Sodium.config(state="normal")
        Sodium.delete(0, "end")
        Sodium.insert(0, data[13])
        Sodium.config(state="readonly")

        # Chloride
        Chloride.config(state="normal")
        Chloride.delete(0, "end")
        Chloride.insert(0, data[14])
        Chloride.config(state="readonly")

        # Vitamin A
        Vitamin_A.config(state="normal")
        Vitamin_A.delete(0, "end")
        Vitamin_A.insert(0, data[15])
        Vitamin_A.config(state="readonly")

        # Vitamin C
        Vitamin_C.config(state="normal")
        Vitamin_C.delete(0, "end")
        Vitamin_C.insert(0, data[16])
        Vitamin_C.config(state="readonly")

        # Vitamin D
        Vitamin_D.config(state="normal")
        Vitamin_D.delete(0, "end")
        Vitamin_D.insert(0, data[17])
        Vitamin_D.config(state="readonly")

        # Vitamin E
        Vitamin_E.config(state="normal")
        Vitamin_E.delete(0, "end")
        Vitamin_E.insert(0, data[18])
        Vitamin_E.config(state="readonly")

        # Vitamin K
        Vitamin_K.config(state="normal")
        Vitamin_K.delete(0, "end")
        Vitamin_K.insert(0, data[19])
        Vitamin_K.config(state="readonly")

        # Thiamin
        Thiamin.config(state="normal")
        Thiamin.delete(0, "end")
        Thiamin.insert(0, data[20])
        Thiamin.config(state="readonly")

        # Riboflavin
        Riboflavin.config(state="normal")
        Riboflavin.delete(0, "end")
        Riboflavin.insert(0, data[21])
        Riboflavin.config(state="readonly")

        # Niacin
        Niacin.config(state="normal")
        Niacin.delete(0, "end")
        Niacin.insert(0, data[22])
        Niacin.config(state="readonly")

        # Vitamin B6
        Vitamin_B6.config(state="normal")
        Vitamin_B6.delete(0, "end")
        Vitamin_B6.insert(0, data[23])
        Vitamin_B6.config(state="readonly")

        # Folate
        Folate.config(state="normal")
        Folate.delete(0, "end")
        Folate.insert(0, data[24])
        Folate.config(state="readonly")

        # Vitamin B12
        Vitamin_B12.config(state="normal")
        Vitamin_B12.delete(0, "end")
        Vitamin_B12.insert(0, data[25])
        Vitamin_B12.config(state="readonly")

        # Pantothenic Acid
        Pantothenic_Acid.config(state="normal")
        Pantothenic_Acid.delete(0, "end")
        Pantothenic_Acid.insert(0, data[26])
        Pantothenic_Acid.config(state="readonly")

        # Biotin
        Biotin.config(state="normal")
        Biotin.delete(0, "end")
        Biotin.insert(0, data[27])
        Biotin.config(state="readonly")

        # Choline
        Choline.config(state="normal")
        Choline.delete(0, "end")
        Choline.insert(0, data[28])
        Choline.config(state="readonly")

        # Protein
        Protein.config(state="normal")
        Protein.delete(0, "end")
        Protein.insert(0, data[29])
        Protein.config(state="readonly")

        # Carbohydrate
        Carbohydrate.config(state="normal")
        Carbohydrate.delete(0, "end")
        Carbohydrate.insert(0, data[30])
        Carbohydrate.config(state="readonly")

        # Fiber
        Fiber.config(state="normal")
        Fiber.delete(0, "end")
        Fiber.insert(0, data[31])
        Fiber.config(state="readonly")

        # Linoleic Acid
        Linoleic_Acid.config(state="normal")
        Linoleic_Acid.delete(0, "end")
        Linoleic_Acid.insert(0, data[32])
        Linoleic_Acid.config(state="readonly")

        # Alpha Linoleic Acid
        Alpha_Linoleic_Acid.config(state="normal")
        Alpha_Linoleic_Acid.delete(0, "end")
        Alpha_Linoleic_Acid.insert(0, data[33])
        Alpha_Linoleic_Acid.config(state="readonly")
    else:
        # Calcium
        Calcium.config(state="normal")
        Calcium.delete(0, "end")
        Calcium.insert(0, 0)
        Calcium.config(state="readonly")

        # Chromium
        Chromium.config(state="normal")
        Chromium.delete(0, "end")
        Chromium.insert(0, 0)
        Chromium.config(state="readonly")

        # Copper
        Copper.config(state="normal")
        Copper.delete(0, "end")
        Copper.insert(0, 0)
        Copper.config(state="readonly")

        # Fluoride
        Fluoride.config(state="normal")
        Fluoride.delete(0, "end")
        Fluoride.insert(0, 0)
        Fluoride.config(state="readonly")

        # Iodine
        Iodine.config(state="normal")
        Iodine.delete(0, "end")
        Iodine.insert(0, 0)
        Iodine.config(state="readonly")

        # Iron
        Iron.config(state="normal")
        Iron.delete(0, "end")
        Iron.insert(0, 0)
        Iron.config(state="readonly")

        # Magnesium
        Magnesium.config(state="normal")
        Magnesium.delete(0, "end")
        Magnesium.insert(0, 0)
        Magnesium.config(state="readonly")

        # Manganese
        Manganese.config(state="normal")
        Manganese.delete(0, "end")
        Manganese.insert(0, 0)
        Manganese.config(state="readonly")

        # Molybdenum
        Molybdenum.config(state="normal")
        Molybdenum.delete(0, "end")
        Molybdenum.insert(0, 0)
        Molybdenum.config(state="readonly")

        # Phosphorus
        Phosphorus.config(state="normal")
        Phosphorus.delete(0, "end")
        Phosphorus.insert(0, 0)
        Phosphorus.config(state="readonly")

        # Selenium
        Selenium.config(state="normal")
        Selenium.delete(0, "end")
        Selenium.insert(0, 0)
        Selenium.config(state="readonly")

        # Zinc
        Zinc.config(state="normal")
        Zinc.delete(0, "end")
        Zinc.insert(0, 0)
        Zinc.config(state="readonly")

        # Potassium
        Potassium.config(state="normal")
        Potassium.delete(0, "end")
        Potassium.insert(0, 0)
        Potassium.config(state="readonly")

        # Sodium
        Sodium.config(state="normal")
        Sodium.delete(0, "end")
        Sodium.insert(0, 0)
        Sodium.config(state="readonly")

        # Chloride
        Chloride.config(state="normal")
        Chloride.delete(0, "end")
        Chloride.insert(0, 0)
        Chloride.config(state="readonly")

        # Vitamin A
        Vitamin_A.config(state="normal")
        Vitamin_A.delete(0, "end")
        Vitamin_A.insert(0, 0)
        Vitamin_A.config(state="readonly")

        # Vitamin C
        Vitamin_C.config(state="normal")
        Vitamin_C.delete(0, "end")
        Vitamin_C.insert(0, 0)
        Vitamin_C.config(state="readonly")

        # Vitamin D
        Vitamin_D.config(state="normal")
        Vitamin_D.delete(0, "end")
        Vitamin_D.insert(0, 0)
        Vitamin_D.config(state="readonly")

        # Vitamin E
        Vitamin_E.config(state="normal")
        Vitamin_E.delete(0, "end")
        Vitamin_E.insert(0, 0)
        Vitamin_E.config(state="readonly")

        # Vitamin K
        Vitamin_K.config(state="normal")
        Vitamin_K.delete(0, "end")
        Vitamin_K.insert(0, 0)
        Vitamin_K.config(state="readonly")

        # Thiamin
        Thiamin.config(state="normal")
        Thiamin.delete(0, "end")
        Thiamin.insert(0, 0)
        Thiamin.config(state="readonly")

        # Riboflavin
        Riboflavin.config(state="normal")
        Riboflavin.delete(0, "end")
        Riboflavin.insert(0, 0)
        Riboflavin.config(state="readonly")

        # Niacin
        Niacin.config(state="normal")
        Niacin.delete(0, "end")
        Niacin.insert(0, 0)
        Niacin.config(state="readonly")

        # Vitamin B6
        Vitamin_B6.config(state="normal")
        Vitamin_B6.delete(0, "end")
        Vitamin_B6.insert(0, 0)
        Vitamin_B6.config(state="readonly")

        # Folate
        Folate.config(state="normal")
        Folate.delete(0, "end")
        Folate.insert(0, 0)
        Folate.config(state="readonly")

        # Vitamin B12
        Vitamin_B12.config(state="normal")
        Vitamin_B12.delete(0, "end")
        Vitamin_B12.insert(0, 0)
        Vitamin_B12.config(state="readonly")

        # Pantothenic Acid
        Pantothenic_Acid.config(state="normal")
        Pantothenic_Acid.delete(0, "end")
        Pantothenic_Acid.insert(0, 0)
        Pantothenic_Acid.config(state="readonly")

        # Biotin
        Biotin.config(state="normal")
        Biotin.delete(0, "end")
        Biotin.insert(0, 0)
        Biotin.config(state="readonly")

        # Choline
        Choline.config(state="normal")
        Choline.delete(0, "end")
        Choline.insert(0, 0)
        Choline.config(state="readonly")

        # Protein
        Protein.config(state="normal")
        Protein.delete(0, "end")
        Protein.insert(0, 0)
        Protein.config(state="readonly")

        # Carbohydrate
        Carbohydrate.config(state="normal")
        Carbohydrate.delete(0, "end")
        Carbohydrate.insert(0, 0)
        Carbohydrate.config(state="readonly")

        # Fiber
        Fiber.config(state="normal")
        Fiber.delete(0, "end")
        Fiber.insert(0, 0)
        Fiber.config(state="readonly")

        # Linoleic Acid
        Linoleic_Acid.config(state="normal")
        Linoleic_Acid.delete(0, "end")
        Linoleic_Acid.insert(0, 0)
        Linoleic_Acid.config(state="readonly")

        # Alpha Linoleic Acid
        Alpha_Linoleic_Acid.config(state="normal")
        Alpha_Linoleic_Acid.delete(0, "end")
        Alpha_Linoleic_Acid.insert(0, 0)
        Alpha_Linoleic_Acid.config(state="readonly")

    # update discretionary boxes
    discretionary_update()

    #Draw Nutrition Log
    Draw_Nutrition_Log()


# Dietary Reference Intakes
def update_reference_intakes():
    # re-initialize canvases
    Macronutrients.delete("all")
    Vitamins.delete("all")
    Elements.delete("all")
    Draw_Macronutrients()
    Draw_Vitamins()
    Draw_Elements()

    # fetch body data
    age = int(AgeN.get())
    bio = genderN
    pregnant = pregN
    lactating = lactN

    # Calcium
    Cal_Int = 0
    if (pregnant == 0) and (lactating == 0):
        if age <= 1:
            Cal_Int = 260
        elif age <= 3:
            Cal_Int = 700
        elif age <= 8:
            Cal_Int = 1000
        elif (age <= 13) and (bio == 0):
            Cal_Int = 1300
        elif (age <= 13) and (bio == 1):
            Cal_Int = 1300
        elif (age <= 18) and (bio == 0):
            Cal_Int = 1300
        elif (age <= 18) and (bio == 1):
            Cal_Int = 1300
        elif (age <= 30) and (bio == 0):
            Cal_Int = 1000
        elif (age <= 30) and (bio == 1):
            Cal_Int = 1000
        elif (age <= 50) and (bio == 0):
            Cal_Int = 1000
        elif (age <= 50) and (bio == 1):
            Cal_Int = 1000
        elif (age <= 70) and (bio == 0):
            Cal_Int = 1200
        elif (age <= 70) and (bio == 1):
            Cal_Int = 1000
        elif (age > 70) and (bio == 0):
            Cal_Int = 1200
        elif (age > 70) and (bio == 1):
            Cal_Int = 1200
    else:
        if (pregnant == 1) and (lactating == 1):
            if age <= 18:
                Cal_Int = 1300
            elif age <= 30:
                Cal_Int = 1000
            elif age <= 50:
                Cal_Int = 1000
        elif (pregnant == 1) and (lactating == 0):
            if age <= 18:
                Cal_Int = 1300
            elif age <= 30:
                Cal_Int = 1000
            elif age <= 50:
                Cal_Int = 1000
        elif lactating == 1:
            if age <= 18:
                Cal_Int = 1300
            elif age <= 30:
                Cal_Int = 1000
            elif age <= 50:
                Cal_Int = 1000

    # Chromium
    Chr_Int = 0
    if (pregnant == 0) and (lactating == 0):
        if age <= 1:
            Chr_Int = 5.5
        elif age <= 3:
            Chr_Int = 11
        elif age <= 8:
            Chr_Int = 15
        elif (age <= 13) and (bio == 0):
            Chr_Int = 21
        elif (age <= 13) and (bio == 1):
            Chr_Int = 25
        elif (age <= 18) and (bio == 0):
            Chr_Int = 24
        elif (age <= 18) and (bio == 1):
            Chr_Int = 35
        elif (age <= 30) and (bio == 0):
            Chr_Int = 25
        elif (age <= 30) and (bio == 1):
            Chr_Int = 35
        elif (age <= 50) and (bio == 0):
            Chr_Int = 25
        elif (age <= 50) and (bio == 1):
            Chr_Int = 35
        elif (age <= 70) and (bio == 0):
            Chr_Int = 20
        elif (age <= 70) and (bio == 1):
            Chr_Int = 30
        elif (age > 70) and (bio == 0):
            Chr_Int = 20
        elif (age > 70) and (bio == 1):
            Chr_Int = 30
    else:
        if (pregnant == 1) and (lactating == 1):
            if age <= 18:
                Chr_Int = 45
            elif age <= 30:
                Chr_Int = 45
            elif age <= 50:
                Chr_Int = 45
        elif (pregnant == 1) and (lactating == 0):
            if age <= 18:
                Chr_Int = 29
            elif age <= 30:
                Chr_Int = 30
            elif age <= 50:
                Chr_Int = 30
        elif lactating == 1:
            if age <= 18:
                Chr_Int = 44
            elif age <= 30:
                Chr_Int = 45
            elif age <= 50:
                Chr_Int = 45

    # Copper
    Cop_Int = 0
    if (pregnant == 0) and (lactating == 0):
        if age <= 1:
            Cop_Int = 220
        elif age <= 3:
            Cop_Int = 340
        elif age <= 8:
            Cop_Int = 440
        elif (age <= 13) and (bio == 0):
            Cop_Int = 700
        elif (age <= 13) and (bio == 1):
            Cop_Int = 700
        elif (age <= 18) and (bio == 0):
            Cop_Int = 890
        elif (age <= 18) and (bio == 1):
            Cop_Int = 890
        elif (age <= 30) and (bio == 0):
            Cop_Int = 900
        elif (age <= 30) and (bio == 1):
            Cop_Int = 900
        elif (age <= 50) and (bio == 0):
            Cop_Int = 900
        elif (age <= 50) and (bio == 1):
            Cop_Int = 900
        elif (age <= 70) and (bio == 0):
            Cop_Int = 900
        elif (age <= 70) and (bio == 1):
            Cop_Int = 900
        elif (age > 70) and (bio == 0):
            Cop_Int = 900
        elif (age > 70) and (bio == 1):
            Cop_Int = 900
    else:
        if (pregnant == 1) and (lactating == 1):
            if age <= 18:
                Cop_Int = 1300
            elif age <= 30:
                Cop_Int = 1300
            elif age <= 50:
                Cop_Int = 1300
        elif (pregnant == 1) and (lactating == 0):
            if age <= 18:
                Cop_Int = 1000
            elif age <= 30:
                Cop_Int = 1000
            elif age <= 50:
                Cop_Int = 1000
        elif lactating == 1:
            if age <= 18:
                Cop_Int = 1300
            elif age <= 30:
                Cop_Int = 1300
            elif age <= 50:
                Cop_Int = 1300

    #Fluoride
    Flu_Int = 0
    if (pregnant == 0) and (lactating == 0):
        if age <= 1:
            Flu_Int = 0.5
        elif age <= 3:
            Flu_Int = 0.7
        elif age <= 8:
            Flu_Int = 1
        elif (age <= 13) and (bio == 0):
            Flu_Int = 2
        elif (age <= 13) and (bio == 1):
            Flu_Int = 2
        elif (age <= 18) and (bio == 0):
            Flu_Int = 3
        elif (age <= 18) and (bio == 1):
            Flu_Int = 3
        elif (age <= 30) and (bio == 0):
            Flu_Int = 3
        elif (age <= 30) and (bio == 1):
            Flu_Int = 4
        elif (age <= 50) and (bio == 0):
            Flu_Int = 3
        elif (age <= 50) and (bio == 1):
            Flu_Int = 4
        elif (age <= 70) and (bio == 0):
            Flu_Int = 3
        elif (age <= 70) and (bio == 1):
            Flu_Int = 4
        elif (age > 70) and (bio == 0):
            Flu_Int = 3
        elif (age > 70) and (bio == 1):
            Flu_Int = 4
    else:
        if (pregnant == 1) and (lactating == 1):
            if age <= 18:
                Flu_Int = 3
            elif age <= 30:
                Flu_Int = 3
            elif age <= 50:
                Flu_Int = 3
        elif (pregnant == 1) and (lactating == 0):
            if age <= 18:
                Flu_Int = 3
            elif age <= 30:
                Flu_Int = 3
            elif age <= 50:
                Flu_Int = 3
        elif lactating == 1:
            if age <= 18:
                Flu_Int = 3
            elif age <= 30:
                Flu_Int = 3
            elif age <= 50:
                Flu_Int = 3

    # Iodine
    Iod_Int = 0
    if (pregnant == 0) and (lactating == 0):
        if age <= 1:
            Iod_Int = 130
        elif age <= 3:
            Iod_Int = 90
        elif age <= 8:
            Iod_Int = 90
        elif (age <= 13) and (bio == 0):
            Iod_Int = 120
        elif (age <= 13) and (bio == 1):
            Iod_Int = 120
        elif (age <= 18) and (bio == 0):
            Iod_Int = 150
        elif (age <= 18) and (bio == 1):
            Iod_Int = 150
        elif (age <= 30) and (bio == 0):
            Iod_Int = 150
        elif (age <= 30) and (bio == 1):
            Iod_Int = 150
        elif (age <= 50) and (bio == 0):
            Iod_Int = 150
        elif (age <= 50) and (bio == 1):
            Iod_Int = 150
        elif (age <= 70) and (bio == 0):
            Iod_Int = 150
        elif (age <= 70) and (bio == 1):
            Iod_Int = 150
        elif (age > 70) and (bio == 0):
            Iod_Int = 150
        elif (age > 70) and (bio == 1):
            Iod_Int = 150
    else:
        if (pregnant == 1) and (lactating == 1):
            if age <= 18:
                Iod_Int = 290
            elif age <= 30:
                Iod_Int = 290
            elif age <= 50:
                Iod_Int = 290
        elif (pregnant == 1) and (lactating == 0):
            if age <= 18:
                Iod_Int = 220
            elif age <= 30:
                Iod_Int = 220
            elif age <= 50:
                Iod_Int = 220
        elif lactating == 1:
            if age <= 18:
                Iod_Int = 290
            elif age <= 30:
                Iod_Int = 290
            elif age <= 50:
                Iod_Int = 290

    # Iron
    Iro_Int = 0
    if (pregnant == 0) and (lactating == 0):
        if age <= 1:
            Iro_Int = 11
        elif age <= 3:
            Iro_Int = 7
        elif age <= 8:
            Iro_Int = 10
        elif (age <= 13) and (bio == 0):
            Iro_Int = 8
        elif (age <= 13) and (bio == 1):
            Iro_Int = 8
        elif (age <= 18) and (bio == 0):
            Iro_Int = 15
        elif (age <= 18) and (bio == 1):
            Iro_Int = 11
        elif (age <= 30) and (bio == 0):
            Iro_Int = 18
        elif (age <= 30) and (bio == 1):
            Iro_Int = 8
        elif (age <= 50) and (bio == 0):
            Iro_Int = 18
        elif (age <= 50) and (bio == 1):
            Iro_Int = 8
        elif (age <= 70) and (bio == 0):
            Iro_Int = 8
        elif (age <= 70) and (bio == 1):
            Iro_Int = 8
        elif (age > 70) and (bio == 0):
            Iro_Int = 8
        elif (age > 70) and (bio == 1):
            Iro_Int = 8
    else:
        if (pregnant == 1) and (lactating == 1):
            if age <= 18:
                Iro_Int = 27
            elif age <= 30:
                Iro_Int = 27
            elif age <= 50:
                Iro_Int = 27
        elif (pregnant == 1) and (lactating == 0):
            if age <= 18:
                Iro_Int = 27
            elif age <= 30:
                Iro_Int = 27
            elif age <= 50:
                Iro_Int = 27
        elif lactating == 1:
            if age <= 18:
                Iro_Int = 10
            elif age <= 30:
                Iro_Int = 9
            elif age <= 50:
                Iro_Int = 9

    # Magnesium
    Mag_Int = 0
    if (pregnant == 0) and (lactating == 0):
        if age <= 1:
            Mag_Int = 75
        elif age <= 3:
            Mag_Int = 80
        elif age <= 8:
            Mag_Int = 130
        elif (age <= 13) and (bio == 0):
            Mag_Int = 240
        elif (age <= 13) and (bio == 1):
            Mag_Int = 240
        elif (age <= 18) and (bio == 0):
            Mag_Int = 360
        elif (age <= 18) and (bio == 1):
            Mag_Int = 410
        elif (age <= 30) and (bio == 0):
            Mag_Int = 310
        elif (age <= 30) and (bio == 1):
            Mag_Int = 400
        elif (age <= 50) and (bio == 0):
            Mag_Int = 320
        elif (age <= 50) and (bio == 1):
            Mag_Int = 420
        elif (age <= 70) and (bio == 0):
            Mag_Int = 320
        elif (age <= 70) and (bio == 1):
            Mag_Int = 420
        elif (age > 70) and (bio == 0):
            Mag_Int = 320
        elif (age > 70) and (bio == 1):
            Mag_Int = 420
    else:
        if (pregnant == 1) and (lactating == 1):
            if age <= 18:
                Mag_Int = 400
            elif age <= 30:
                Mag_Int = 350
            elif age <= 50:
                Mag_Int = 360
        elif (pregnant == 1) and (lactating == 0):
            if age <= 18:
                Mag_Int = 400
            elif age <= 30:
                Mag_Int = 350
            elif age <= 50:
                Mag_Int = 360
        elif lactating == 1:
            if age <= 18:
                Mag_Int = 360
            elif age <= 30:
                Mag_Int = 310
            elif age <= 50:
                Mag_Int = 320

    # Magnesium
    Man_Int = 0
    if (pregnant == 0) and (lactating == 0):
        if age <= 1:
            Man_Int = 0.6
        elif age <= 3:
            Man_Int = 1.2
        elif age <= 8:
            Man_Int = 1.5
        elif (age <= 13) and (bio == 0):
            Man_Int = 1.6
        elif (age <= 13) and (bio == 1):
            Man_Int = 1.9
        elif (age <= 18) and (bio == 0):
            Man_Int = 1.6
        elif (age <= 18) and (bio == 1):
            Man_Int = 2.2
        elif (age <= 30) and (bio == 0):
            Man_Int = 1.8
        elif (age <= 30) and (bio == 1):
            Man_Int = 2.3
        elif (age <= 50) and (bio == 0):
            Man_Int = 1.8
        elif (age <= 50) and (bio == 1):
            Man_Int = 2.3
        elif (age <= 70) and (bio == 0):
            Man_Int = 1.8
        elif (age <= 70) and (bio == 1):
            Man_Int = 2.3
        elif (age > 70) and (bio == 0):
            Man_Int = 1.8
        elif (age > 70) and (bio == 1):
            Man_Int = 2.3
    else:
        if (pregnant == 1) and (lactating == 1):
            if age <= 18:
                Man_Int = 2.6
            elif age <= 30:
                Man_Int = 2.6
            elif age <= 50:
                Man_Int = 2.6
        elif (pregnant == 1) and (lactating == 0):
            if age <= 18:
                Man_Int = 2.0
            elif age <= 30:
                Man_Int = 2.0
            elif age <= 50:
                Man_Int = 2.0
        elif lactating == 1:
            if age <= 18:
                Man_Int = 2.6
            elif age <= 30:
                Man_Int = 2.6
            elif age <= 50:
                Man_Int = 2.6

    # Molybdenum
    Mol_Int = 0
    if (pregnant == 0) and (lactating == 0):
        if age <= 1:
            Mol_Int = 3
        elif age <= 3:
            Mol_Int = 17
        elif age <= 8:
            Mol_Int = 22
        elif (age <= 13) and (bio == 0):
            Mol_Int = 34
        elif (age <= 13) and (bio == 1):
            Mol_Int = 34
        elif (age <= 18) and (bio == 0):
            Mol_Int = 43
        elif (age <= 18) and (bio == 1):
            Mol_Int = 43
        elif (age <= 30) and (bio == 0):
            Mol_Int = 45
        elif (age <= 30) and (bio == 1):
            Mol_Int = 45
        elif (age <= 50) and (bio == 0):
            Mol_Int = 45
        elif (age <= 50) and (bio == 1):
            Mol_Int = 45
        elif (age <= 70) and (bio == 0):
            Mol_Int = 45
        elif (age <= 70) and (bio == 1):
            Mol_Int = 45
        elif (age > 70) and (bio == 0):
            Mol_Int = 45
        elif (age > 70) and (bio == 1):
            Mol_Int = 45
    else:
        if (pregnant == 1) and (lactating == 1):
            if age <= 18:
                Mol_Int = 50
            elif age <= 30:
                Mol_Int = 50
            elif age <= 50:
                Mol_Int = 50
        elif (pregnant == 1) and (lactating == 0):
            if age <= 18:
                Mol_Int = 50
            elif age <= 30:
                Mol_Int = 50
            elif age <= 50:
                Mol_Int = 50
        elif lactating == 1:
            if age <= 18:
                Mol_Int = 50
            elif age <= 30:
                Mol_Int = 50
            elif age <= 50:
                Mol_Int = 50

    # Phosphorus
    Pho_Int = 0
    if (pregnant == 0) and (lactating == 0):
        if age <= 1:
            Pho_Int = 275
        elif age <= 3:
            Pho_Int = 460
        elif age <= 8:
            Pho_Int = 500
        elif (age <= 13) and (bio == 0):
            Pho_Int = 1250
        elif (age <= 13) and (bio == 1):
            Pho_Int = 1250
        elif (age <= 18) and (bio == 0):
            Pho_Int = 1250
        elif (age <= 18) and (bio == 1):
            Pho_Int = 1250
        elif (age <= 30) and (bio == 0):
            Pho_Int = 700
        elif (age <= 30) and (bio == 1):
            Pho_Int = 700
        elif (age <= 50) and (bio == 0):
            Pho_Int = 700
        elif (age <= 50) and (bio == 1):
            Pho_Int = 700
        elif (age <= 70) and (bio == 0):
            Pho_Int = 700
        elif (age <= 70) and (bio == 1):
            Pho_Int = 700
        elif (age > 70) and (bio == 0):
            Pho_Int = 700
        elif (age > 70) and (bio == 1):
            Pho_Int = 700
    else:
        if (pregnant == 1) and (lactating == 1):
            if age <= 18:
                Pho_Int = 1250
            elif age <= 30:
                Pho_Int = 700
            elif age <= 50:
                Pho_Int = 700
        elif (pregnant == 1) and (lactating == 0):
            if age <= 18:
                Pho_Int = 1250
            elif age <= 30:
                Pho_Int = 700
            elif age <= 50:
                Pho_Int = 700
        elif lactating == 1:
            if age <= 18:
                Pho_Int = 1250
            elif age <= 30:
                Pho_Int = 700
            elif age <= 50:
                Pho_Int = 700

    # Selenium
    Sel_Int = 0
    if (pregnant == 0) and (lactating == 0):
        if age <= 1:
            Sel_Int = 20
        elif age <= 3:
            Sel_Int = 20
        elif age <= 8:
            Sel_Int = 30
        elif (age <= 13) and (bio == 0):
            Sel_Int = 40
        elif (age <= 13) and (bio == 1):
            Sel_Int = 40
        elif (age <= 18) and (bio == 0):
            Sel_Int = 55
        elif (age <= 18) and (bio == 1):
            Sel_Int = 55
        elif (age <= 30) and (bio == 0):
            Sel_Int = 55
        elif (age <= 30) and (bio == 1):
            Sel_Int = 55
        elif (age <= 50) and (bio == 0):
            Sel_Int = 55
        elif (age <= 50) and (bio == 1):
            Sel_Int = 55
        elif (age <= 70) and (bio == 0):
            Sel_Int = 55
        elif (age <= 70) and (bio == 1):
            Sel_Int = 55
        elif (age > 70) and (bio == 0):
            Sel_Int = 55
        elif (age > 70) and (bio == 1):
            Sel_Int = 55
    else:
        if (pregnant == 1) and (lactating == 1):
            if age <= 18:
                Sel_Int = 70
            elif age <= 30:
                Sel_Int = 70
            elif age <= 50:
                Sel_Int = 70
        elif (pregnant == 1) and (lactating == 0):
            if age <= 18:
                Sel_Int = 60
            elif age <= 30:
                Sel_Int = 60
            elif age <= 50:
                Sel_Int = 60
        elif lactating == 1:
            if age <= 18:
                Sel_Int = 70
            elif age <= 30:
                Sel_Int = 70
            elif age <= 50:
                Sel_Int = 70

    # Zinc
    Zin_Int = 0
    if (pregnant == 0) and (lactating == 0):
        if age <= 1:
            Zin_Int = 3
        elif age <= 3:
            Zin_Int = 3
        elif age <= 8:
            Zin_Int = 5
        elif (age <= 13) and (bio == 0):
            Zin_Int = 8
        elif (age <= 13) and (bio == 1):
            Zin_Int = 8
        elif (age <= 18) and (bio == 0):
            Zin_Int = 9
        elif (age <= 18) and (bio == 1):
            Zin_Int = 11
        elif (age <= 30) and (bio == 0):
            Zin_Int = 8
        elif (age <= 30) and (bio == 1):
            Zin_Int = 11
        elif (age <= 50) and (bio == 0):
            Zin_Int = 8
        elif (age <= 50) and (bio == 1):
            Zin_Int = 11
        elif (age <= 70) and (bio == 0):
            Zin_Int = 8
        elif (age <= 70) and (bio == 1):
            Zin_Int = 11
        elif (age > 70) and (bio == 0):
            Zin_Int = 8
        elif (age > 70) and (bio == 1):
            Zin_Int = 11
    else:
        if (pregnant == 1) and (lactating == 1):
            if age <= 18:
                Zin_Int = 13
            elif age <= 30:
                Zin_Int = 12
            elif age <= 50:
                Zin_Int = 12
        elif (pregnant == 1) and (lactating == 0):
            if age <= 18:
                Zin_Int = 12
            elif age <= 30:
                Zin_Int = 11
            elif age <= 50:
                Zin_Int = 11
        elif lactating == 1:
            if age <= 18:
                Zin_Int = 13
            elif age <= 30:
                Zin_Int = 12
            elif age <= 50:
                Zin_Int = 12

    # Potassium
    Pot_Int = 0
    if (pregnant == 0) and (lactating == 0):
        if age <= 1:
            Pot_Int = 860
        elif age <= 3:
            Pot_Int = 2000
        elif age <= 8:
            Pot_Int = 2300
        elif (age <= 13) and (bio == 0):
            Pot_Int = 2300
        elif (age <= 13) and (bio == 1):
            Pot_Int = 2500
        elif (age <= 18) and (bio == 0):
            Pot_Int = 2300
        elif (age <= 18) and (bio == 1):
            Pot_Int = 3000
        elif (age <= 30) and (bio == 0):
            Pot_Int = 2600
        elif (age <= 30) and (bio == 1):
            Pot_Int = 3400
        elif (age <= 50) and (bio == 0):
            Pot_Int = 2600
        elif (age <= 50) and (bio == 1):
            Pot_Int = 3400
        elif (age <= 70) and (bio == 0):
            Pot_Int = 2600
        elif (age <= 70) and (bio == 1):
            Pot_Int = 3400
        elif (age > 70) and (bio == 0):
            Pot_Int = 2600
        elif (age > 70) and (bio == 1):
            Pot_Int = 3400
    else:
        if (pregnant == 1) and (lactating == 1):
            if age <= 18:
                Pot_Int = 2600
            elif age <= 30:
                Pot_Int = 2900
            elif age <= 50:
                Pot_Int = 2900
        elif (pregnant == 1) and (lactating == 0):
            if age <= 18:
                Pot_Int = 2600
            elif age <= 30:
                Pot_Int = 2900
            elif age <= 50:
                Pot_Int = 2900
        elif lactating == 1:
            if age <= 18:
                Pot_Int = 2500
            elif age <= 30:
                Pot_Int = 2800
            elif age <= 50:
                Pot_Int = 2800

    # Sodium
    Sod_Int = 0
    if (pregnant == 0) and (lactating == 0):
        if age <= 1:
            Sod_Int = 370
        elif age <= 3:
            Sod_Int = 800
        elif age <= 8:
            Sod_Int = 1000
        elif (age <= 13) and (bio == 0):
            Sod_Int = 1200
        elif (age <= 13) and (bio == 1):
            Sod_Int = 1200
        elif (age <= 18) and (bio == 0):
            Sod_Int = 1500
        elif (age <= 18) and (bio == 1):
            Sod_Int = 1500
        elif (age <= 30) and (bio == 0):
            Sod_Int = 1500
        elif (age <= 30) and (bio == 1):
            Sod_Int = 1500
        elif (age <= 50) and (bio == 0):
            Sod_Int = 1500
        elif (age <= 50) and (bio == 1):
            Sod_Int = 1500
        elif (age <= 70) and (bio == 0):
            Sod_Int = 1500
        elif (age <= 70) and (bio == 1):
            Sod_Int = 1500
        elif (age > 70) and (bio == 0):
            Sod_Int = 1500
        elif (age > 70) and (bio == 1):
            Sod_Int = 1500
    else:
        if (pregnant == 1) and (lactating == 1):
            if age <= 18:
                Sod_Int = 1500
            elif age <= 30:
                Sod_Int = 1500
            elif age <= 50:
                Sod_Int = 1500
        elif (pregnant == 1) and (lactating == 0):
            if age <= 18:
                Sod_Int = 1500
            elif age <= 30:
                Sod_Int = 1500
            elif age <= 50:
                Sod_Int = 1500
        elif lactating == 1:
            if age <= 18:
                Sod_Int = 1500
            elif age <= 30:
                Sod_Int = 1500
            elif age <= 50:
                Sod_Int = 1500

    # Chloride
    Chl_Int = 0
    if (pregnant == 0) and (lactating == 0):
        if age <= 1:
            Chl_Int = 0.57
        elif age <= 3:
            Chl_Int = 1.5
        elif age <= 8:
            Chl_Int = 1.9
        elif (age <= 13) and (bio == 0):
            Chl_Int = 2.3
        elif (age <= 13) and (bio == 1):
            Chl_Int = 2.3
        elif (age <= 18) and (bio == 0):
            Chl_Int = 2.3
        elif (age <= 18) and (bio == 1):
            Chl_Int = 2.3
        elif (age <= 30) and (bio == 0):
            Chl_Int = 2.3
        elif (age <= 30) and (bio == 1):
            Chl_Int = 2.3
        elif (age <= 50) and (bio == 0):
            Chl_Int = 2.3
        elif (age <= 50) and (bio == 1):
            Chl_Int = 2.3
        elif (age <= 70) and (bio == 0):
            Chl_Int = 2.0
        elif (age <= 70) and (bio == 1):
            Chl_Int = 2.0
        elif (age > 70) and (bio == 0):
            Chl_Int = 1.8
        elif (age > 70) and (bio == 1):
            Chl_Int = 1.8
    else:
        if (pregnant == 1) and (lactating == 1):
            if age <= 18:
                Chl_Int = 2.3
            elif age <= 30:
                Chl_Int = 2.3
            elif age <= 50:
                Chl_Int = 2.3
        elif (pregnant == 1) and (lactating == 0):
            if age <= 18:
                Chl_Int = 2.3
            elif age <= 30:
                Chl_Int = 2.3
            elif age <= 50:
                Chl_Int = 2.3
        elif lactating == 1:
            if age <= 18:
                Chl_Int = 2.3
            elif age <= 30:
                Chl_Int = 2.3
            elif age <= 50:
                Chl_Int = 2.3

    # Vitamin A
    Vita_A_Int = 0
    if (pregnant == 0) and (lactating == 0):
        if age <= 1:
            Vita_A_Int = 500
        elif age <= 3:
            Vita_A_Int = 300
        elif age <= 8:
            Vita_A_Int = 400
        elif (age <= 13) and (bio == 0):
            Vita_A_Int = 600
        elif (age <= 13) and (bio == 1):
            Vita_A_Int = 600
        elif (age <= 18) and (bio == 0):
            Vita_A_Int = 700
        elif (age <= 18) and (bio == 1):
            Vita_A_Int = 900
        elif (age <= 30) and (bio == 0):
            Vita_A_Int = 700
        elif (age <= 30) and (bio == 1):
            Vita_A_Int = 900
        elif (age <= 50) and (bio == 0):
            Vita_A_Int = 700
        elif (age <= 50) and (bio == 1):
            Vita_A_Int = 900
        elif (age <= 70) and (bio == 0):
            Vita_A_Int = 700
        elif (age <= 70) and (bio == 1):
            Vita_A_Int = 900
        elif (age > 70) and (bio == 0):
            Vita_A_Int = 700
        elif (age > 70) and (bio == 1):
            Vita_A_Int = 900
    else:
        if (pregnant == 1) and (lactating == 1):
            if age <= 18:
                Vita_A_Int = 1200
            elif age <= 30:
                Vita_A_Int = 1300
            elif age <= 50:
                Vita_A_Int = 1300
        elif (pregnant == 1) and (lactating == 0):
            if age <= 18:
                Vita_A_Int = 750
            elif age <= 30:
                Vita_A_Int = 770
            elif age <= 50:
                Vita_A_Int = 770
        elif lactating == 1:
            if age <= 18:
                Vita_A_Int = 1200
            elif age <= 30:
                Vita_A_Int = 1300
            elif age <= 50:
                Vita_A_Int = 1300

    # Vitamin C
    Vita_C_Int = 0
    if (pregnant == 0) and (lactating == 0):
        if age <= 1:
            Vita_C_Int = 50
        elif age <= 3:
            Vita_C_Int = 15
        elif age <= 8:
            Vita_C_Int = 25
        elif (age <= 13) and (bio == 0):
            Vita_C_Int = 45
        elif (age <= 13) and (bio == 1):
            Vita_C_Int = 45
        elif (age <= 18) and (bio == 0):
            Vita_C_Int = 65
        elif (age <= 18) and (bio == 1):
            Vita_C_Int = 75
        elif (age <= 30) and (bio == 0):
            Vita_C_Int = 75
        elif (age <= 30) and (bio == 1):
            Vita_C_Int = 90
        elif (age <= 50) and (bio == 0):
            Vita_C_Int = 75
        elif (age <= 50) and (bio == 1):
            Vita_C_Int = 90
        elif (age <= 70) and (bio == 0):
            Vita_C_Int = 75
        elif (age <= 70) and (bio == 1):
            Vita_C_Int = 90
        elif (age > 70) and (bio == 0):
            Vita_C_Int = 75
        elif (age > 70) and (bio == 1):
            Vita_C_Int = 90
    else:
        if (pregnant == 1) and (lactating == 1):
            if age <= 18:
                Vita_C_Int = 115
            elif age <= 30:
                Vita_C_Int = 120
            elif age <= 50:
                Vita_C_Int = 120
        elif (pregnant == 1) and (lactating == 0):
            if age <= 18:
                Vita_C_Int = 80
            elif age <= 30:
                Vita_C_Int = 85
            elif age <= 50:
                Vita_C_Int = 85
        elif lactating == 1:
            if age <= 18:
                Vita_C_Int = 115
            elif age <= 30:
                Vita_C_Int = 120
            elif age <= 50:
                Vita_C_Int = 120

    # Vitamin D
    Vita_D_Int = 0
    if (pregnant == 0) and (lactating == 0):
        if age <= 1:
            Vita_D_Int = 10
        elif age <= 3:
            Vita_D_Int = 15
        elif age <= 8:
            Vita_D_Int = 15
        elif (age <= 13) and (bio == 0):
            Vita_D_Int = 15
        elif (age <= 13) and (bio == 1):
            Vita_D_Int = 15
        elif (age <= 18) and (bio == 0):
            Vita_D_Int = 15
        elif (age <= 18) and (bio == 1):
            Vita_D_Int = 15
        elif (age <= 30) and (bio == 0):
            Vita_D_Int = 15
        elif (age <= 30) and (bio == 1):
            Vita_D_Int = 15
        elif (age <= 50) and (bio == 0):
            Vita_D_Int = 15
        elif (age <= 50) and (bio == 1):
            Vita_D_Int = 15
        elif (age <= 70) and (bio == 0):
            Vita_D_Int = 15
        elif (age <= 70) and (bio == 1):
            Vita_D_Int = 15
        elif (age > 70) and (bio == 0):
            Vita_D_Int = 20
        elif (age > 70) and (bio == 1):
            Vita_D_Int = 20
    else:
        if (pregnant == 1) and (lactating == 1):
            if age <= 18:
                Vita_D_Int = 15
            elif age <= 30:
                Vita_D_Int = 15
            elif age <= 50:
                Vita_D_Int = 15
        elif (pregnant == 1) and (lactating == 0):
            if age <= 18:
                Vita_D_Int = 15
            elif age <= 30:
                Vita_D_Int = 15
            elif age <= 50:
                Vita_D_Int = 15
        elif lactating == 1:
            if age <= 18:
                Vita_D_Int = 15
            elif age <= 30:
                Vita_D_Int = 15
            elif age <= 50:
                Vita_D_Int = 15

    # Vitamin E
    Vita_E_Int = 0
    if (pregnant == 0) and (lactating == 0):
        if age <= 1:
            Vita_E_Int = 5
        elif age <= 3:
            Vita_E_Int = 6
        elif age <= 8:
            Vita_E_Int = 7
        elif (age <= 13) and (bio == 0):
            Vita_E_Int = 11
        elif (age <= 13) and (bio == 1):
            Vita_E_Int = 11
        elif (age <= 18) and (bio == 0):
            Vita_E_Int = 15
        elif (age <= 18) and (bio == 1):
            Vita_E_Int = 15
        elif (age <= 30) and (bio == 0):
            Vita_E_Int = 15
        elif (age <= 30) and (bio == 1):
            Vita_E_Int = 15
        elif (age <= 50) and (bio == 0):
            Vita_E_Int = 15
        elif (age <= 50) and (bio == 1):
            Vita_E_Int = 15
        elif (age <= 70) and (bio == 0):
            Vita_E_Int = 15
        elif (age <= 70) and (bio == 1):
            Vita_E_Int = 15
        elif (age > 70) and (bio == 0):
            Vita_E_Int = 15
        elif (age > 70) and (bio == 1):
            Vita_E_Int = 15
    else:
        if (pregnant == 1) and (lactating == 1):
            if age <= 18:
                Vita_E_Int = 19
            elif age <= 30:
                Vita_E_Int = 19
            elif age <= 50:
                Vita_E_Int = 19
        elif (pregnant == 1) and (lactating == 0):
            if age <= 18:
                Vita_E_Int = 15
            elif age <= 30:
                Vita_E_Int = 15
            elif age <= 50:
                Vita_E_Int = 15
        elif lactating == 1:
            if age <= 18:
                Vita_E_Int = 19
            elif age <= 30:
                Vita_E_Int = 19
            elif age <= 50:
                Vita_E_Int = 19

    # Vitamin K
    Vita_K_Int = 0
    if (pregnant == 0) and (lactating == 0):
        if age <= 1:
            Vita_K_Int = 2.5
        elif age <= 3:
            Vita_K_Int = 30
        elif age <= 8:
            Vita_K_Int = 55
        elif (age <= 13) and (bio == 0):
            Vita_K_Int = 60
        elif (age <= 13) and (bio == 1):
            Vita_K_Int = 60
        elif (age <= 18) and (bio == 0):
            Vita_K_Int = 75
        elif (age <= 18) and (bio == 1):
            Vita_K_Int = 75
        elif (age <= 30) and (bio == 0):
            Vita_K_Int = 90
        elif (age <= 30) and (bio == 1):
            Vita_K_Int = 120
        elif (age <= 50) and (bio == 0):
            Vita_K_Int = 90
        elif (age <= 50) and (bio == 1):
            Vita_K_Int = 120
        elif (age <= 70) and (bio == 0):
            Vita_K_Int = 90
        elif (age <= 70) and (bio == 1):
            Vita_K_Int = 120
        elif (age > 70) and (bio == 0):
            Vita_K_Int = 90
        elif (age > 70) and (bio == 1):
            Vita_K_Int = 120
    else:
        if (pregnant == 1) and (lactating == 1):
            if age <= 18:
                Vita_K_Int = 75
            elif age <= 30:
                Vita_K_Int = 90
            elif age <= 50:
                Vita_K_Int = 90
        elif (pregnant == 1) and (lactating == 0):
            if age <= 18:
                Vita_K_Int = 75
            elif age <= 30:
                Vita_K_Int = 90
            elif age <= 50:
                Vita_K_Int = 90
        elif lactating == 1:
            if age <= 18:
                Vita_K_Int = 75
            elif age <= 30:
                Vita_K_Int = 90
            elif age <= 50:
                Vita_K_Int = 90

    # Thiamin
    Thia_Int = 0
    if (pregnant == 0) and (lactating == 0):
        if age <= 1:
            Thia_Int = 0.3
        elif age <= 3:
            Thia_Int = 0.5
        elif age <= 8:
            Thia_Int = 0.6
        elif (age <= 13) and (bio == 0):
            Thia_Int = 0.9
        elif (age <= 13) and (bio == 1):
            Thia_Int = 0.9
        elif (age <= 18) and (bio == 0):
            Thia_Int = 1.0
        elif (age <= 18) and (bio == 1):
            Thia_Int = 1.2
        elif (age <= 30) and (bio == 0):
            Thia_Int = 1.1
        elif (age <= 30) and (bio == 1):
            Thia_Int = 1.2
        elif (age <= 50) and (bio == 0):
            Thia_Int = 1.1
        elif (age <= 50) and (bio == 1):
            Thia_Int = 1.2
        elif (age <= 70) and (bio == 0):
            Thia_Int = 1.1
        elif (age <= 70) and (bio == 1):
            Thia_Int = 1.2
        elif (age > 70) and (bio == 0):
            Thia_Int = 1.1
        elif (age > 70) and (bio == 1):
            Thia_Int = 1.2
    else:
        if (pregnant == 1) and (lactating == 1):
            if age <= 18:
                Thia_Int = 1.4
            elif age <= 30:
                Thia_Int = 1.4
            elif age <= 50:
                Thia_Int = 1.4
        elif (pregnant == 1) and (lactating == 0):
            if age <= 18:
                Thia_Int = 1.4
            elif age <= 30:
                Thia_Int = 1.4
            elif age <= 50:
                Thia_Int = 1.4
        elif lactating == 1:
            if age <= 18:
                Thia_Int = 1.4
            elif age <= 30:
                Thia_Int = 1.4
            elif age <= 50:
                Thia_Int = 1.4

    # Riboflavin
    Ribo_Int = 0
    if (pregnant == 0) and (lactating == 0):
        if age <= 1:
            Ribo_Int = 0.4
        elif age <= 3:
            Ribo_Int = 0.5
        elif age <= 8:
            Ribo_Int = 0.6
        elif (age <= 13) and (bio == 0):
            Ribo_Int = 0.9
        elif (age <= 13) and (bio == 1):
            Ribo_Int = 0.9
        elif (age <= 18) and (bio == 0):
            Ribo_Int = 1.0
        elif (age <= 18) and (bio == 1):
            Ribo_Int = 1.3
        elif (age <= 30) and (bio == 0):
            Ribo_Int = 1.1
        elif (age <= 30) and (bio == 1):
            Ribo_Int = 1.3
        elif (age <= 50) and (bio == 0):
            Ribo_Int = 1.1
        elif (age <= 50) and (bio == 1):
            Ribo_Int = 1.3
        elif (age <= 70) and (bio == 0):
            Ribo_Int = 1.1
        elif (age <= 70) and (bio == 1):
            Ribo_Int = 1.3
        elif (age > 70) and (bio == 0):
            Ribo_Int = 1.1
        elif (age > 70) and (bio == 1):
            Ribo_Int = 1.3
    else:
        if (pregnant == 1) and (lactating == 1):
            if age <= 18:
                Ribo_Int = 1.6
            elif age <= 30:
                Ribo_Int = 1.6
            elif age <= 50:
                Ribo_Int = 1.6
        elif (pregnant == 1) and (lactating == 0):
            if age <= 18:
                Ribo_Int = 1.4
            elif age <= 30:
                Ribo_Int = 1.4
            elif age <= 50:
                Ribo_Int = 1.4
        elif lactating == 1:
            if age <= 18:
                Ribo_Int = 1.6
            elif age <= 30:
                Ribo_Int = 1.6
            elif age <= 50:
                Ribo_Int = 1.6

    # Niacin
    Niac_Int = 0
    if (pregnant == 0) and (lactating == 0):
        if age <= 1:
            Niac_Int = 4
        elif age <= 3:
            Niac_Int = 6
        elif age <= 8:
            Niac_Int = 8
        elif (age <= 13) and (bio == 0):
            Niac_Int = 12
        elif (age <= 13) and (bio == 1):
            Niac_Int = 12
        elif (age <= 18) and (bio == 0):
            Niac_Int = 14
        elif (age <= 18) and (bio == 1):
            Niac_Int = 16
        elif (age <= 30) and (bio == 0):
            Niac_Int = 14
        elif (age <= 30) and (bio == 1):
            Niac_Int = 16
        elif (age <= 50) and (bio == 0):
            Niac_Int = 14
        elif (age <= 50) and (bio == 1):
            Niac_Int = 16
        elif (age <= 70) and (bio == 0):
            Niac_Int = 14
        elif (age <= 70) and (bio == 1):
            Niac_Int = 16
        elif (age > 70) and (bio == 0):
            Niac_Int = 14
        elif (age > 70) and (bio == 1):
            Niac_Int = 16
    else:
        if (pregnant == 1) and (lactating == 1):
            if age <= 18:
                Niac_Int = 18
            elif age <= 30:
                Niac_Int = 18
            elif age <= 50:
                Niac_Int = 18
        elif (pregnant == 1) and (lactating == 0):
            if age <= 18:
                Niac_Int = 18
            elif age <= 30:
                Niac_Int = 18
            elif age <= 50:
                Niac_Int = 18
        elif lactating == 1:
            if age <= 18:
                Niac_Int = 17
            elif age <= 30:
                Niac_Int = 17
            elif age <= 50:
                Niac_Int = 17

    # Vitamin B6
    Vita_B6_Int = 0
    if (pregnant == 0) and (lactating == 0):
        if age <= 1:
            Vita_B6_Int = 0.3
        elif age <= 3:
            Vita_B6_Int = 0.5
        elif age <= 8:
            Vita_B6_Int = 0.6
        elif (age <= 13) and (bio == 0):
            Vita_B6_Int = 1.0
        elif (age <= 13) and (bio == 1):
            Vita_B6_Int = 1.0
        elif (age <= 18) and (bio == 0):
            Vita_B6_Int = 1.2
        elif (age <= 18) and (bio == 1):
            Vita_B6_Int = 1.3
        elif (age <= 30) and (bio == 0):
            Vita_B6_Int = 1.3
        elif (age <= 30) and (bio == 1):
            Vita_B6_Int = 1.3
        elif (age <= 50) and (bio == 0):
            Vita_B6_Int = 1.3
        elif (age <= 50) and (bio == 1):
            Vita_B6_Int = 1.3
        elif (age <= 70) and (bio == 0):
            Vita_B6_Int = 1.5
        elif (age <= 70) and (bio == 1):
            Vita_B6_Int = 1.7
        elif (age > 70) and (bio == 0):
            Vita_B6_Int = 1.5
        elif (age > 70) and (bio == 1):
            Vita_B6_Int = 1.7
    else:
        if (pregnant == 1) and (lactating == 1):
            if age <= 18:
                Vita_B6_Int = 2.0
            elif age <= 30:
                Vita_B6_Int = 2.0
            elif age <= 50:
                Vita_B6_Int = 2.0
        elif (pregnant == 1) and (lactating == 0):
            if age <= 18:
                Vita_B6_Int = 1.9
            elif age <= 30:
                Vita_B6_Int = 1.9
            elif age <= 50:
                Vita_B6_Int = 1.9
        elif lactating == 1:
            if age <= 18:
                Vita_B6_Int = 2.0
            elif age <= 30:
                Vita_B6_Int = 2.0
            elif age <= 50:
                Vita_B6_Int = 2.0

    # Folate
    Fola_Int = 0
    if (pregnant == 0) and (lactating == 0):
        if age <= 1:
            Fola_Int = 80
        elif age <= 3:
            Fola_Int = 150
        elif age <= 8:
            Fola_Int = 200
        elif (age <= 13) and (bio == 0):
            Fola_Int = 300
        elif (age <= 13) and (bio == 1):
            Fola_Int = 300
        elif (age <= 18) and (bio == 0):
            Fola_Int = 400
        elif (age <= 18) and (bio == 1):
            Fola_Int = 400
        elif (age <= 30) and (bio == 0):
            Fola_Int = 400
        elif (age <= 30) and (bio == 1):
            Fola_Int = 400
        elif (age <= 50) and (bio == 0):
            Fola_Int = 400
        elif (age <= 50) and (bio == 1):
            Fola_Int = 400
        elif (age <= 70) and (bio == 0):
            Fola_Int = 400
        elif (age <= 70) and (bio == 1):
            Fola_Int = 400
        elif (age > 70) and (bio == 0):
            Fola_Int = 400
        elif (age > 70) and (bio == 1):
            Fola_Int = 400
    else:
        if (pregnant == 1) and (lactating == 1):
            if age <= 18:
                Fola_Int = 600
            elif age <= 30:
                Fola_Int = 600
            elif age <= 50:
                Fola_Int = 600
        elif (pregnant == 1) and (lactating == 0):
            if age <= 18:
                Fola_Int = 600
            elif age <= 30:
                Fola_Int = 600
            elif age <= 50:
                Fola_Int = 600
        elif lactating == 1:
            if age <= 18:
                Fola_Int = 500
            elif age <= 30:
                Fola_Int = 500
            elif age <= 50:
                Fola_Int = 500

    # Vitamin B12
    Vita_B12_Int = 0
    if (pregnant == 0) and (lactating == 0):
        if age <= 1:
            Vita_B12_Int = 0.5
        elif age <= 3:
            Vita_B12_Int = 0.9
        elif age <= 8:
            Vita_B12_Int = 1.2
        elif (age <= 13) and (bio == 0):
            Vita_B12_Int = 1.8
        elif (age <= 13) and (bio == 1):
            Vita_B12_Int = 1.8
        elif (age <= 18) and (bio == 0):
            Vita_B12_Int = 2.4
        elif (age <= 18) and (bio == 1):
            Vita_B12_Int = 2.4
        elif (age <= 30) and (bio == 0):
            Vita_B12_Int = 2.4
        elif (age <= 30) and (bio == 1):
            Vita_B12_Int = 2.4
        elif (age <= 50) and (bio == 0):
            Vita_B12_Int = 2.4
        elif (age <= 50) and (bio == 1):
            Vita_B12_Int = 2.4
        elif (age <= 70) and (bio == 0):
            Vita_B12_Int = 2.4
        elif (age <= 70) and (bio == 1):
            Vita_B12_Int = 2.4
        elif (age > 70) and (bio == 0):
            Vita_B12_Int = 2.4
        elif (age > 70) and (bio == 1):
            Vita_B12_Int = 2.4
    else:
        if (pregnant == 1) and (lactating == 1):
            if age <= 18:
                Vita_B12_Int = 2.8
            elif age <= 30:
                Vita_B12_Int = 2.8
            elif age <= 50:
                Vita_B12_Int = 2.8
        elif (pregnant == 1) and (lactating == 0):
            if age <= 18:
                Vita_B12_Int = 2.6
            elif age <= 30:
                Vita_B12_Int = 2.6
            elif age <= 50:
                Vita_B12_Int = 2.6
        elif lactating == 1:
            if age <= 18:
                Vita_B12_Int = 2.8
            elif age <= 30:
                Vita_B12_Int = 2.8
            elif age <= 50:
                Vita_B12_Int = 2.8

    # Pantothenic Acid
    Pant_Int = 0
    if (pregnant == 0) and (lactating == 0):
        if age <= 1:
            Pant_Int = 1.8
        elif age <= 3:
            Pant_Int = 2
        elif age <= 8:
            Pant_Int = 3
        elif (age <= 13) and (bio == 0):
            Pant_Int = 4
        elif (age <= 13) and (bio == 1):
            Pant_Int = 4
        elif (age <= 18) and (bio == 0):
            Pant_Int = 5
        elif (age <= 18) and (bio == 1):
            Pant_Int = 5
        elif (age <= 30) and (bio == 0):
            Pant_Int = 5
        elif (age <= 30) and (bio == 1):
            Pant_Int = 5
        elif (age <= 50) and (bio == 0):
            Pant_Int = 5
        elif (age <= 50) and (bio == 1):
            Pant_Int = 5
        elif (age <= 70) and (bio == 0):
            Pant_Int = 5
        elif (age <= 70) and (bio == 1):
            Pant_Int = 5
        elif (age > 70) and (bio == 0):
            Pant_Int = 5
        elif (age > 70) and (bio == 1):
            Pant_Int = 5
    else:
        if (pregnant == 1) and (lactating == 1):
            if age <= 18:
                Pant_Int = 7
            elif age <= 30:
                Pant_Int = 7
            elif age <= 50:
                Pant_Int = 7
        elif (pregnant == 1) and (lactating == 0):
            if age <= 18:
                Pant_Int = 6
            elif age <= 30:
                Pant_Int = 6
            elif age <= 50:
                Pant_Int = 6
        elif lactating == 1:
            if age <= 18:
                Pant_Int = 7
            elif age <= 30:
                Pant_Int = 7
            elif age <= 50:
                Pant_Int = 7

    # Biotin
    Biot_Int = 0
    if (pregnant == 0) and (lactating == 0):
        if age <= 1:
            Biot_Int = 6
        elif age <= 3:
            Biot_Int = 8
        elif age <= 8:
            Biot_Int = 12
        elif (age <= 13) and (bio == 0):
            Biot_Int = 20
        elif (age <= 13) and (bio == 1):
            Biot_Int = 20
        elif (age <= 18) and (bio == 0):
            Biot_Int = 25
        elif (age <= 18) and (bio == 1):
            Biot_Int = 25
        elif (age <= 30) and (bio == 0):
            Biot_Int = 30
        elif (age <= 30) and (bio == 1):
            Biot_Int = 30
        elif (age <= 50) and (bio == 0):
            Biot_Int = 30
        elif (age <= 50) and (bio == 1):
            Biot_Int = 30
        elif (age <= 70) and (bio == 0):
            Biot_Int = 30
        elif (age <= 70) and (bio == 1):
            Biot_Int = 30
        elif (age > 70) and (bio == 0):
            Biot_Int = 30
        elif (age > 70) and (bio == 1):
            Biot_Int = 30
    else:
        if (pregnant == 1) and (lactating == 1):
            if age <= 18:
                Biot_Int = 35
            elif age <= 30:
                Biot_Int = 35
            elif age <= 50:
                Biot_Int = 35
        elif (pregnant == 1) and (lactating == 0):
            if age <= 18:
                Biot_Int = 30
            elif age <= 30:
                Biot_Int = 30
            elif age <= 50:
                Biot_Int = 30
        elif lactating == 1:
            if age <= 18:
                Biot_Int = 35
            elif age <= 30:
                Biot_Int = 35
            elif age <= 50:
                Biot_Int = 35

    # Choline
    Chol_Int = 0
    if (pregnant == 0) and (lactating == 0):
        if age <= 1:
            Chol_Int = 150
        elif age <= 3:
            Chol_Int = 200
        elif age <= 8:
            Chol_Int = 250
        elif (age <= 13) and (bio == 0):
            Chol_Int = 375
        elif (age <= 13) and (bio == 1):
            Chol_Int = 375
        elif (age <= 18) and (bio == 0):
            Chol_Int = 400
        elif (age <= 18) and (bio == 1):
            Chol_Int = 550
        elif (age <= 30) and (bio == 0):
            Chol_Int = 425
        elif (age <= 30) and (bio == 1):
            Chol_Int = 550
        elif (age <= 50) and (bio == 0):
            Chol_Int = 425
        elif (age <= 50) and (bio == 1):
            Chol_Int = 550
        elif (age <= 70) and (bio == 0):
            Chol_Int = 425
        elif (age <= 70) and (bio == 1):
            Chol_Int = 550
        elif (age > 70) and (bio == 0):
            Chol_Int = 425
        elif (age > 70) and (bio == 1):
            Chol_Int = 550
    else:
        if (pregnant == 1) and (lactating == 1):
            if age <= 18:
                Chol_Int = 550
            elif age <= 30:
                Chol_Int = 550
            elif age <= 50:
                Chol_Int = 550
        elif (pregnant == 1) and (lactating == 0):
            if age <= 18:
                Chol_Int = 450
            elif age <= 30:
                Chol_Int = 450
            elif age <= 50:
                Chol_Int = 450
        elif lactating == 1:
            if age <= 18:
                Chol_Int = 550
            elif age <= 30:
                Chol_Int = 550
            elif age <= 50:
                Chol_Int = 550

    # Protein
    Prot_Int = 0
    if (pregnant == 0) and (lactating == 0):
        if age <= 1:
            Prot_Int = 11
        elif age <= 3:
            Prot_Int = 13
        elif age <= 8:
            Prot_Int = 19
        elif (age <= 13) and (bio == 0):
            Prot_Int = 34
        elif (age <= 13) and (bio == 1):
            Prot_Int = 34
        elif (age <= 18) and (bio == 0):
            Prot_Int = 46
        elif (age <= 18) and (bio == 1):
            Prot_Int = 52
        elif (age <= 30) and (bio == 0):
            Prot_Int = 46
        elif (age <= 30) and (bio == 1):
            Prot_Int = 56
        elif (age <= 50) and (bio == 0):
            Prot_Int = 46
        elif (age <= 50) and (bio == 1):
            Prot_Int = 56
        elif (age <= 70) and (bio == 0):
            Prot_Int = 46
        elif (age <= 70) and (bio == 1):
            Prot_Int = 56
        elif (age > 70) and (bio == 0):
            Prot_Int = 46
        elif (age > 70) and (bio == 1):
            Prot_Int = 56
    else:
        if (pregnant == 1) and (lactating == 1):
            if age <= 18:
                Prot_Int = 71
            elif age <= 30:
                Prot_Int = 71
            elif age <= 50:
                Prot_Int = 71
        elif (pregnant == 1) and (lactating == 0):
            if age <= 18:
                Prot_Int = 71
            elif age <= 30:
                Prot_Int = 71
            elif age <= 50:
                Prot_Int = 71
        elif lactating == 1:
            if age <= 18:
                Prot_Int = 71
            elif age <= 30:
                Prot_Int = 71
            elif age <= 50:
                Prot_Int = 71

    # Carbohydrate
    Carb_Int = 0
    if (pregnant == 0) and (lactating == 0):
        if age <= 1:
            Carb_Int = 95
        elif age <= 3:
            Carb_Int = 130
        elif age <= 8:
            Carb_Int = 130
        elif (age <= 13) and (bio == 0):
            Carb_Int = 130
        elif (age <= 13) and (bio == 1):
            Carb_Int = 130
        elif (age <= 18) and (bio == 0):
            Carb_Int = 130
        elif (age <= 18) and (bio == 1):
            Carb_Int = 130
        elif (age <= 30) and (bio == 0):
            Carb_Int = 130
        elif (age <= 30) and (bio == 1):
            Carb_Int = 130
        elif (age <= 50) and (bio == 0):
            Carb_Int = 130
        elif (age <= 50) and (bio == 1):
            Carb_Int = 130
        elif (age <= 70) and (bio == 0):
            Carb_Int = 130
        elif (age <= 70) and (bio == 1):
            Carb_Int = 130
        elif (age > 70) and (bio == 0):
            Carb_Int = 130
        elif (age > 70) and (bio == 1):
            Carb_Int = 130
    else:
        if (pregnant == 1) and (lactating == 1):
            if age <= 18:
                Carb_Int = 210
            elif age <= 30:
                Carb_Int = 210
            elif age <= 50:
                Carb_Int = 210
        elif (pregnant == 1) and (lactating == 0):
            if age <= 18:
                Carb_Int = 175
            elif age <= 30:
                Carb_Int = 175
            elif age <= 50:
                Carb_Int = 175
        elif lactating == 1:
            if age <= 18:
                Carb_Int = 210
            elif age <= 30:
                Carb_Int = 210
            elif age <= 50:
                Carb_Int = 210

    # Fiber
    Fibe_Int = 0
    if (pregnant == 0) and (lactating == 0):
        if age <= 1:
            Fibe_Int = 19
        elif age <= 3:
            Fibe_Int = 19
        elif age <= 8:
            Fibe_Int = 25
        elif (age <= 13) and (bio == 0):
            Fibe_Int = 26
        elif (age <= 13) and (bio == 1):
            Fibe_Int = 31
        elif (age <= 18) and (bio == 0):
            Fibe_Int = 26
        elif (age <= 18) and (bio == 1):
            Fibe_Int = 38
        elif (age <= 30) and (bio == 0):
            Fibe_Int = 25
        elif (age <= 30) and (bio == 1):
            Fibe_Int = 38
        elif (age <= 50) and (bio == 0):
            Fibe_Int = 25
        elif (age <= 50) and (bio == 1):
            Fibe_Int = 38
        elif (age <= 70) and (bio == 0):
            Fibe_Int = 21
        elif (age <= 70) and (bio == 1):
            Fibe_Int = 30
        elif (age > 70) and (bio == 0):
            Fibe_Int = 21
        elif (age > 70) and (bio == 1):
            Fibe_Int = 30
    else:
        if (pregnant == 1) and (lactating == 1):
            if age <= 18:
                Fibe_Int = 29
            elif age <= 30:
                Fibe_Int = 29
            elif age <= 50:
                Fibe_Int = 29
        elif (pregnant == 1) and (lactating == 0):
            if age <= 18:
                Fibe_Int = 28
            elif age <= 30:
                Fibe_Int = 28
            elif age <= 50:
                Fibe_Int = 28
        elif lactating == 1:
            if age <= 18:
                Fibe_Int = 29
            elif age <= 30:
                Fibe_Int = 29
            elif age <= 50:
                Fibe_Int = 29

    # Linoleic Acid
    Lino_Int = 0
    if (pregnant == 0) and (lactating == 0):
        if age <= 1:
            Lino_Int = 4.6
        elif age <= 3:
            Lino_Int = 7
        elif age <= 8:
            Lino_Int = 10
        elif (age <= 13) and (bio == 0):
            Lino_Int = 10
        elif (age <= 13) and (bio == 1):
            Lino_Int = 12
        elif (age <= 18) and (bio == 0):
            Lino_Int = 11
        elif (age <= 18) and (bio == 1):
            Lino_Int = 16
        elif (age <= 30) and (bio == 0):
            Lino_Int = 12
        elif (age <= 30) and (bio == 1):
            Lino_Int = 17
        elif (age <= 50) and (bio == 0):
            Lino_Int = 12
        elif (age <= 50) and (bio == 1):
            Lino_Int = 17
        elif (age <= 70) and (bio == 0):
            Lino_Int = 11
        elif (age <= 70) and (bio == 1):
            Lino_Int = 14
        elif (age > 70) and (bio == 0):
            Lino_Int = 11
        elif (age > 70) and (bio == 1):
            Lino_Int = 14
    else:
        if (pregnant == 1) and (lactating == 1):
            if age <= 18:
                Lino_Int = 13
            elif age <= 30:
                Lino_Int = 13
            elif age <= 50:
                Lino_Int = 13
        elif (pregnant == 1) and (lactating == 0):
            if age <= 18:
                Lino_Int = 13
            elif age <= 30:
                Lino_Int = 13
            elif age <= 50:
                Lino_Int = 13
        elif lactating == 1:
            if age <= 18:
                Lino_Int = 13
            elif age <= 30:
                Lino_Int = 13
            elif age <= 50:
                Lino_Int = 13

    # Alpha Linoleic Acid
    ALino_Int = 0
    if (pregnant == 0) and (lactating == 0):
        if age <= 1:
            ALino_Int = 0.5
        elif age <= 3:
            ALino_Int = 0.7
        elif age <= 8:
            ALino_Int = 0.9
        elif (age <= 13) and (bio == 0):
            ALino_Int = 1.0
        elif (age <= 13) and (bio == 1):
            ALino_Int = 1.2
        elif (age <= 18) and (bio == 0):
            ALino_Int = 1.1
        elif (age <= 18) and (bio == 1):
            ALino_Int = 1.6
        elif (age <= 30) and (bio == 0):
            ALino_Int = 1.1
        elif (age <= 30) and (bio == 1):
            ALino_Int = 1.6
        elif (age <= 50) and (bio == 0):
            ALino_Int = 1.1
        elif (age <= 50) and (bio == 1):
            ALino_Int = 1.6
        elif (age <= 70) and (bio == 0):
            ALino_Int = 1.1
        elif (age <= 70) and (bio == 1):
            ALino_Int = 1.6
        elif (age > 70) and (bio == 0):
            ALino_Int = 1.1
        elif (age > 70) and (bio == 1):
            ALino_Int = 1.6
    else:
        if (pregnant == 1) and (lactating == 1):
            if age <= 18:
                ALino_Int = 1.4
            elif age <= 30:
                ALino_Int = 1.4
            elif age <= 50:
                ALino_Int = 1.4
        elif (pregnant == 1) and (lactating == 0):
            if age <= 18:
                ALino_Int = 1.4
            elif age <= 30:
                ALino_Int = 1.4
            elif age <= 50:
                ALino_Int = 1.4
        elif lactating == 1:
            if age <= 18:
                ALino_Int = 1.3
            elif age <= 30:
                ALino_Int = 1.3
            elif age <= 50:
                ALino_Int = 1.3

    #update canvas information
    Elements.create_text(280, 50, text=(str(Cal_Int) + " (mg/d)"), font=("Comic Sans MS", 8))
    Elements.create_text(280, 80, text=(str(Chr_Int) + " (μg/d)"), font=("Comic Sans MS", 8))
    Elements.create_text(280, 110, text=(str(Cop_Int) + " (μg/d)"), font=("Comic Sans MS", 8))
    Elements.create_text(280, 140, text=(str(Flu_Int) + " (mg/d)"), font=("Comic Sans MS", 8))
    Elements.create_text(280, 170, text=(str(Iod_Int) + " (μg/d)"), font=("Comic Sans MS", 8))
    Elements.create_text(280, 200, text=(str(Iro_Int) + " (mg/d)"), font=("Comic Sans MS", 8))
    Elements.create_text(280, 230, text=(str(Mag_Int) + " (mg/d)"), font=("Comic Sans MS", 8))
    Elements.create_text(280, 260, text=(str(Man_Int) + " (mg/d)"), font=("Comic Sans MS", 8))
    Elements.create_text(280, 290, text=(str(Mol_Int) + " (μg/d)"), font=("Comic Sans MS", 8))
    Elements.create_text(280, 320, text=(str(Pho_Int) + " (mg/d)"), font=("Comic Sans MS", 8))
    Elements.create_text(280, 350, text=(str(Sel_Int) + " (μg/d)"), font=("Comic Sans MS", 8))
    Elements.create_text(280, 380, text=(str(Zin_Int) + " (mg/d)"), font=("Comic Sans MS", 8))
    Elements.create_text(280, 410, text=(str(Pot_Int) + " (mg/d)"), font=("Comic Sans MS", 8))
    Elements.create_text(280, 440, text=(str(Sod_Int) + " (mg/d)"), font=("Comic Sans MS", 8))
    Elements.create_text(280, 470, text=(str(Chl_Int) + " (g/d)"), font=("Comic Sans MS", 8))

    Vitamins.create_text(280, 50, text=(str(Vita_A_Int) + " (μg/d)"), font=("Comic Sans MS", 8))
    Vitamins.create_text(280, 80, text=(str(Vita_C_Int) + " (mg/d)"), font=("Comic Sans MS", 8))
    Vitamins.create_text(280, 110, text=(str(Vita_D_Int) + " (μg/d)"), font=("Comic Sans MS", 8))
    Vitamins.create_text(280, 140, text=(str(Vita_E_Int) + " (mg/d)"), font=("Comic Sans MS", 8))
    Vitamins.create_text(280, 170, text=(str(Vita_K_Int) + " (μg/d)"), font=("Comic Sans MS", 8))
    Vitamins.create_text(280, 200, text=(str(Thia_Int) + " (mg/d)"), font=("Comic Sans MS", 8))
    Vitamins.create_text(280, 230, text=(str(Ribo_Int) + " (mg/d)"), font=("Comic Sans MS", 8))
    Vitamins.create_text(280, 260, text=(str(Niac_Int) + " (mg/d)"), font=("Comic Sans MS", 8))
    Vitamins.create_text(280, 290, text=(str(Vita_B6_Int) + " (mg/d)"), font=("Comic Sans MS", 8))
    Vitamins.create_text(280, 320, text=(str(Fola_Int) + " (μg/d)"), font=("Comic Sans MS", 8))
    Vitamins.create_text(280, 350, text=(str(Vita_B12_Int) + " (μg/d)"), font=("Comic Sans MS", 8))
    Vitamins.create_text(280, 380, text=(str(Pant_Int) + " (mg/d)"), font=("Comic Sans MS", 8))
    Vitamins.create_text(280, 410, text=(str(Biot_Int) + " (μg/d)"), font=("Comic Sans MS", 8))
    Vitamins.create_text(280, 440, text=(str(Chol_Int) + " (mg/d)"), font=("Comic Sans MS", 8))

    Macronutrients.create_text(280, 50, text=(str(Prot_Int) + " (g/d)"), font=("Comic Sans MS", 8))
    Macronutrients.create_text(280, 80, text=(str(Carb_Int) + " (g/d)"), font=("Comic Sans MS", 8))
    Macronutrients.create_text(280, 110, text=(str(Fibe_Int) + " (g/d)"), font=("Comic Sans MS", 8))
    Macronutrients.create_text(280, 140, text=(str(Lino_Int) + " (g/d)"), font=("Comic Sans MS", 8))
    Macronutrients.create_text(280, 170, text=(str(ALino_Int) + " (g/d)"), font=("Comic Sans MS", 8))

    #Write data to file
    DRI_stats = "/DRI_stats.txt"
    store = open(polyfile + DRI_stats, "w", encoding="utf8")
    store.write(str(Cal_Int) + "\n")
    store.write(str(Chr_Int) + "\n")
    store.write(str(Cop_Int) + "\n")
    store.write(str(Flu_Int) + "\n")
    store.write(str(Iod_Int) + "\n")
    store.write(str(Iro_Int) + "\n")
    store.write(str(Mag_Int) + "\n")
    store.write(str(Man_Int) + "\n")
    store.write(str(Mol_Int) + "\n")
    store.write(str(Pho_Int) + "\n")
    store.write(str(Sel_Int) + "\n")
    store.write(str(Zin_Int) + "\n")
    store.write(str(Pot_Int) + "\n")
    store.write(str(Sod_Int) + "\n")
    store.write(str(Chl_Int) + "\n")
    store.write(str(Vita_A_Int) + "\n")
    store.write(str(Vita_C_Int) + "\n")
    store.write(str(Vita_D_Int) + "\n")
    store.write(str(Vita_E_Int) + "\n")
    store.write(str(Vita_K_Int) + "\n")
    store.write(str(Thia_Int) + "\n")
    store.write(str(Ribo_Int) + "\n")
    store.write(str(Niac_Int) + "\n")
    store.write(str(Vita_B6_Int) + "\n")
    store.write(str(Fola_Int) + "\n")
    store.write(str(Vita_B12_Int) + "\n")
    store.write(str(Pant_Int) + "\n")
    store.write(str(Biot_Int) + "\n")
    store.write(str(Chol_Int) + "\n")
    store.write(str(Prot_Int) + "\n")
    store.write(str(Carb_Int) + "\n")
    store.write(str(Fibe_Int) + "\n")
    store.write(str(Lino_Int) + "\n")
    store.write(str(ALino_Int) + "\n")
    store.close()

    #update display
    update_nutrition_spinboxes()

#create polyfile record
def polyfile_recordN():
    #fetch date info
    dummy = 0
    day_fetch = str(DayN.get())
    month_fetch = str(MonthN.get())
    year_fetch = str(YearN.get())
    polyfile_dir = "/" + day_fetch + month_fetch + year_fetch
    if path.exists(polyfile + polyfile_dir):
        dummy = dummy + 1
    else:
        os.makedirs(polyfile + polyfile_dir)
    #Configure Day Range (for each month and leap year)
    month_pull = MonthN.get()
    year_pull = YearN.get()
    leap = True
    leap_check = str((int(year_pull))/4)
    split_leap = leap_check.split(".")
    if int(split_leap[1]) > 0:
        leap = False
    if (month_pull == "September") or (month_pull == "April") or (month_pull == "June") or (month_pull == "November"):
        DayN.config(from_=1, to=30)
    elif (month_pull == "February") and (leap == True):
        DayN.config(from_=1, to=29)
    elif month_pull == "February":
        DayN.config(from_=1, to=28)
    else:
        DayN.config(from_=1, to=31)
    update_nutrition_spinboxes()

#Nutrition Data Metrics Date Setup
DayN = tkinter.Spinbox(Nutrition_Data_Metrics, width=3, from_=1, to=31, state="normal",
                       command=polyfile_recordN)
DayN.place(x=50, y=22)
DayN.delete(0, "end")
DayN.insert(0, day_get)
DayN.config(state="readonly")

MonthN = tkinter.Spinbox(Nutrition_Data_Metrics, width=10, values=("January", "February", "March", "April", "May", "June", "July", "August", "September", "October",
             "November", "December"), state="normal", command=polyfile_recordN)
MonthN.place(x=154, y=22)
MonthN_List = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October",
             "November", "December"]
MonthN.delete(0, "end")
MonthN.insert(0, Month_List[month_get-1])
MonthN.config(state="readonly")

YearN = tkinter.Spinbox(Nutrition_Data_Metrics, width=4, from_=2020, to=2100, state="normal",
                        command=polyfile_recordN)
YearN.place(x=293, y=22)
YearN.delete(0, "end")
YearN.insert(0, year_get)
YearN.config(state="readonly")

#Nutrition Data Metrics Weight, Age and Sex
WeightN_Control_Canvas.create_rectangle(3, 3, 686, 51, width=2, outline="grey")
WeightN_Control_Canvas.create_text(110, 26, text="Your Dietary Reference Intake (DRI)\n"
                                                "is determined based on age, gender and\n"
                                                "your pregnancy/breastfeeding status.",
                                   font=("Comic Sans MS", 8))
WeightN_Control_Canvas.create_line(225, 0, 225, 50)

#Set Male/Female
genderN = 1
pregN = 0
lactN = 0
def G_1():
    global genderN
    genderN = 0
    MaleN.deselect()
    FemaleN.select()
    update_reference_intakes()

def G_2():
    global genderN
    global pregN
    global lactN
    genderN = 1
    FemaleN.deselect()
    MaleN.select()
    PregnantN.deselect()
    pregN = 0
    LactatingN.deselect()
    lactN = 0
    update_reference_intakes()

def P_1():
    global pregN
    if pregN == 0:
        pregN = 1
    else:
        pregN = 0
    MaleN.deselect()
    FemaleN.select()
    update_reference_intakes()

def L_1():
    global lactN
    if lactN == 0:
        lactN = 1
    else:
        lactN = 0
    MaleN.deselect()
    FemaleN.select()
    update_reference_intakes()

WeightN_Control_Canvas.create_text(387, 14, text="Set Gender:", font=("Comic Sans MS", 10))
MaleN_Check = IntVar()
MaleN = tkinter.Checkbutton(Nutrition_Data_Metrics, text="Male", offvalue=0, onvalue=1,
                            variable=MaleN_Check, command=G_2)
MaleN['font'] = smaller_font
MaleN.place(x=678, y=30)
MaleN.select()

FemaleN_Check = IntVar()
FemaleN = tkinter.Checkbutton(Nutrition_Data_Metrics, text="Female", offvalue=0.1, onvalue=0.2,
                              variable=FemaleN_Check, command=G_1)
FemaleN['font'] = smaller_font
FemaleN.place(x=741, y=30)
WeightN_Control_Canvas.create_line(470, 0, 470, 50)

#Pregnant and/or Lactating
WeightN_Control_Canvas.create_text(575, 15, text="Are you Pregnant and/or Lactating:",
                                   font=("Comic Sans MS", 8))
PregnantN_Check = IntVar()
PregnantN = tkinter.Checkbutton(Nutrition_Data_Metrics, text="Pregnant", offvalue=4, onvalue=5,
                                variable=PregnantN_Check, command=P_1)
PregnantN['font'] = smaller_font
PregnantN.place(x=855, y=30)
PregnantN.deselect()

LactatingN_Check = IntVar()
LactatingN = tkinter.Checkbutton(Nutrition_Data_Metrics, text="Lactating", offvalue=4, onvalue=5,
                                 variable=LactatingN_Check, command=L_1)
LactatingN['font'] = smaller_font
LactatingN.place(x=935, y=30)
LactatingN.deselect()

#Set Age
WeightN_Control_Canvas.create_text(262, 14, text="Set Age:", font=("Comic Sans MS", 10))
AgeN = tkinter.Spinbox(Nutrition_Data_Metrics, width=3, from_=1, to=120, state="normal",
                       command=update_reference_intakes)
AgeN.place(x=597, y=32)
AgeN.delete(0, "end")
AgeN.insert(0, "24")
AgeN.config(state="readonly")
WeightN_Control_Canvas.create_line(300, 0, 300, 50)

update_reference_intakes()

#Nutrition Library Operations Start ***************************************************

#Library Canvas
lib_canvas = tkinter.Canvas(Nutrition_Library, width=1255, height=590, background="lavenderblush2")
lib_canvas.place(x=5, y=5)
lib_canvas.create_rectangle(3, 3, 1255, 590, outline="grey")
lib_canvas.create_line(3, 55, 1255, 55, fill="cyan4")
lib_canvas.create_line(292, 3 , 292, 55, fill="cyan4")
img = ImageTk.PhotoImage(Image.open("border.png"))
lib_canvas.create_image(925, 0, anchor=NW, image=img)


#add to nutrition log event
def scale_log(event):
    if (event.x < 405) and (event.x > 205) and (event.y > 248) and (event.y < 262): #add to nutrition
        lib_canvas.create_rectangle(235, 248, 240, 262, fill="cyan")
        add_to_nutrition()
    elif (event.x < 600) and (event.x > 495) and (event.y >= 248) and (event.y < 255): #scale up and update display
        lib_canvas.create_rectangle(495, 248, 600, 255, fill="lime")
        #read SS
        scale_file = "/SS.txt"
        origin_data = open(polyfile + scale_file, "r", encoding="utf8")
        read_origin = origin_data.read().splitlines()
        origin_data.close()
        update_scale = open(polyfile + scale_file, "w", encoding="utf8")
        update_scale.write("update\n")
        update_scale.write(read_origin[1] + "\n")
        scale_value = float(read_origin[4])
        weight = float(read_origin[2])
        new_weight = weight + scale_value
        update_scale.write(str(new_weight) + "\n")
        update_scale.write(read_origin[3] + "\n")
        update_scale.write(str(scale_value) + "\n")
        origin_items = len(read_origin)
        start_origin = 5
        while origin_items != 5:
            examine_origin = (read_origin[start_origin]).split("*")
            if examine_origin[0] == "Calories":
                Calories = float(examine_origin[1])
                Calorie_Unit = Calories/weight
                Calories = round(((Calorie_Unit*scale_value) + Calories), 1)
                Calories_Value = "---"
                update_scale.write("Calories" + "*" + str(Calories) + "*" + Calories_Value + "*" + "cal" + "\n")
            elif examine_origin[0] == "Total Fat":
                TotalFat = float(examine_origin[1])
                TotalFat_Unit = TotalFat / weight
                TotalFat = round(((TotalFat_Unit * scale_value) + TotalFat), 2)
                TotalFat_Value = round(((TotalFat/77) * 100), 1)
                update_scale.write("Total Fat" + "*" + str(TotalFat) + "*" + str(TotalFat_Value) + "*" + "g" + "\n")
            elif examine_origin[0] == "Saturated Fat":
                SaturatedFat = float(examine_origin[1])
                SaturatedFat_Unit = SaturatedFat / weight
                SaturatedFat = round(((SaturatedFat_Unit * scale_value) + SaturatedFat), 2)
                SaturatedFat_Value = round(((SaturatedFat/22) * 100), 1)
                update_scale.write("Saturated Fat" + "*" + str(SaturatedFat) + "*" + str(SaturatedFat_Value) + "*" + "g" + "\n")
            elif examine_origin[0] == "Cholesterol":
                Cholesterol = float(examine_origin[1])
                Cholesterol_Unit = Cholesterol / weight
                Cholesterol = round(((Cholesterol_Unit * scale_value) + Cholesterol), 1)
                Cholesterol_Value = round(((Cholesterol/300) * 100), 1)
                update_scale.write("Cholesterol" + "*" + str(Cholesterol) + "*" + str(Cholesterol_Value) + "*" + "g" + "\n")
            elif examine_origin[0] == "Protein":
                Protein = float(examine_origin[1])
                Protein_Unit = Protein / weight
                Protein = round(((Protein_Unit * scale_value) + Protein), 2)
                Protein_Value = round(((Protein/56) * 100), 1)
                update_scale.write("Protein" + "*" + str(Protein) + "*" + str(Protein_Value) + "*" + "g" + "\n")
            elif examine_origin[0] == "Carbohydrate":
                Carbohydrate = float(examine_origin[1])
                Carbohydrate_Unit = Carbohydrate / weight
                Carbohydrate = round(((Carbohydrate_Unit * scale_value) + Carbohydrate), 2)
                Carbohydrate_Value = round(((Carbohydrate/130) * 100), 1)
                update_scale.write("Carbohydrate" + "*" + str(Carbohydrate) + "*" + str(Carbohydrate_Value) + "*" + "g" + "\n")
            elif examine_origin[0] == "Fiber":
                Fiber = float(examine_origin[1])
                Fiber_Unit = Fiber / weight
                Fiber = round(((Fiber_Unit * scale_value) + Fiber), 2)
                Fiber_Value = round(((Fiber/38) * 100), 1)
                update_scale.write("Fiber" + "*" + str(Fiber) + "*" + str(Fiber_Value) + "*" + "g" + "\n")
            elif examine_origin[0] == "Linoleic Acid":
                LinoleicAcid = float(examine_origin[1])
                LinoleicAcid_Unit = LinoleicAcid / weight
                LinoleicAcid = round(((LinoleicAcid_Unit * scale_value) + LinoleicAcid), 2)
                LinoleicAcid_Value = round(((LinoleicAcid/17) * 100), 1)
                update_scale.write("Linoleic Acid" + "*" + str(LinoleicAcid) + "*" + str(LinoleicAcid_Value) + "*" + "g" + "\n")
            elif examine_origin[0] == "Alpha Linoleic Acid":
                ALA = float(examine_origin[1])
                ALA_Unit = ALA / weight
                ALA = round(((ALA_Unit * scale_value) + ALA), 3)
                ALA_Value = round(((ALA/1.6) * 100), 1)
                update_scale.write("Alpha Linoleic Acid" + "*" + str(ALA) + "*" + str(ALA_Value) + "*" + "g" + "\n")
            elif examine_origin[0] == "Vitamin A":
                VitaminA = float(examine_origin[1])
                VitaminA_Unit = VitaminA / weight
                VitaminA = round(((VitaminA_Unit * scale_value) + VitaminA), 1)
                VitaminA_Value = round(((VitaminA/900) * 100), 1)
                update_scale.write("Vitamin A" + "*" + str(VitaminA) + "*" + str(VitaminA_Value) + "*" + "mcg" + "\n")
            elif examine_origin[0] == "Vitamin C":
                VitaminC = float(examine_origin[1])
                VitaminC_Unit = VitaminC / weight
                VitaminC = round(((VitaminC_Unit * scale_value) + VitaminC), 2)
                VitaminC_Value = round(((VitaminC/90) * 100), 1)
                update_scale.write("Vitamin C" + "*" + str(VitaminC) + "*" + str(VitaminC_Value) + "*" + "mg" + "\n")
            elif examine_origin[0] == "Vitamin D":
                VitaminD = float(examine_origin[1])
                VitaminD_Unit = VitaminD / weight
                VitaminD = round(((VitaminD_Unit * scale_value) + VitaminD), 3)
                VitaminD_Value = round(((VitaminD/15) * 100), 1)
                update_scale.write("Vitamin D" + "*" + str(VitaminD) + "*" + str(VitaminD_Value) + "*" + "mcg" + "\n")
            elif examine_origin[0] == "Vitamin E":
                VitaminE = float(examine_origin[1])
                VitaminE_Unit = VitaminE / weight
                VitaminE = round(((VitaminE_Unit * scale_value) + VitaminE), 3)
                VitaminE_Value = round(((VitaminE/15) * 100), 1)
                update_scale.write("Vitamin E" + "*" + str(VitaminE) + "*" + str(VitaminE_Value) + "*" + "mg" + "\n")
            elif examine_origin[0] == "Vitamin K":
                VitaminK = float(examine_origin[1])
                VitaminK_Unit = VitaminK / weight
                VitaminK = round(((VitaminK_Unit * scale_value) + VitaminK), 2)
                VitaminK_Value = round(((VitaminK/120) * 100), 1)
                update_scale.write("Vitamin K" + "*" + str(VitaminK) + "*" + str(VitaminK_Value) + "*" + "mcg" + "\n")
            elif examine_origin[0] == "Thiamin":
                Thiamin = float(examine_origin[1])
                Thiamin_Unit = Thiamin / weight
                Thiamin = round(((Thiamin_Unit * scale_value) + Thiamin), 3)
                Thiamin_Value = round(((Thiamin/1.2) * 100), 1)
                update_scale.write("Thiamin" + "*" + str(Thiamin) + "*" + str(Thiamin_Value) + "*" + "mg" + "\n")
            elif examine_origin[0] == "Riboflavin":
                Riboflavin = float(examine_origin[1])
                Riboflavin_Unit = Riboflavin / weight
                Riboflavin = round(((Riboflavin_Unit * scale_value) + Riboflavin), 3)
                Riboflavin_Value = round(((Riboflavin/1.3) * 100), 1)
                update_scale.write("Riboflavin" + "*" + str(Riboflavin) + "*" + str(Riboflavin_Value) + "*" + "mg" + "\n")
            elif examine_origin[0] == "Niacin":
                Niacin = float(examine_origin[1])
                Niacin_Unit = Niacin / weight
                Niacin = round(((Niacin_Unit * scale_value) + Niacin), 3)
                Niacin_Value = round(((Niacin/16) * 100), 1)
                update_scale.write("Niacin" + "*" + str(Niacin) + "*" + str(Niacin_Value) + "*" + "mg" + "\n")
            elif examine_origin[0] == "Vitamin B6":
                VitaminB6 = float(examine_origin[1])
                VitaminB6_Unit = VitaminB6 / weight
                VitaminB6 = round(((VitaminB6_Unit * scale_value) + VitaminB6), 3)
                VitaminB6_Value = round(((VitaminB6/1.3) * 100), 1)
                update_scale.write("Vitamin B6" + "*" + str(VitaminB6) + "*" + str(VitaminB6_Value) + "*" + "mg" + "\n")
            elif examine_origin[0] == "Folate":
                Folate = float(examine_origin[1])
                Folate_Unit = Folate / weight
                Folate = round(((Folate_Unit * scale_value) + Folate), 1)
                Folate_Value = round(((Folate/400) * 100), 1)
                update_scale.write("Folate" + "*" + str(Folate) + "*" + str(Folate_Value) + "*" + "mcg" + "\n")
            elif examine_origin[0] == "Vitamin B12":
                VitaminB12 = float(examine_origin[1])
                VitaminB12_Unit = VitaminB12 / weight
                VitaminB12 = round(((VitaminB12_Unit * scale_value) + VitaminB12), 3)
                VitaminB12_Value = round(((VitaminB12/2.4) * 100), 1)
                update_scale.write("Vitamin B12" + "*" + str(VitaminB12) + "*" + str(VitaminB12_Value) + "*" + "mcg" + "\n")
            elif examine_origin[0] == "Pantothenic Acid":
                PantothenicAcid = float(examine_origin[1])
                PantothenicAcid_Unit = PantothenicAcid / weight
                PantothenicAcid = round(((PantothenicAcid_Unit * scale_value) + PantothenicAcid), 3)
                PantothenicAcid_Value = round(((PantothenicAcid/5) * 100), 1)
                update_scale.write("Pantothenic Acid" + "*" + str(PantothenicAcid) + "*" + str(PantothenicAcid_Value) + "*" + "mg" + "\n")
            elif examine_origin[0] == "Biotin":
                Biotin = float(examine_origin[1])
                Biotin_Unit = Biotin / weight
                Biotin = round(((Biotin_Unit * scale_value) + Biotin), 3)
                Biotin_Value = round(((Biotin/30) * 100), 1)
                update_scale.write("Biotin" + "*" + str(Biotin) + "*" + str(Biotin_Value) + "*" + "mcg" + "\n")
            elif examine_origin[0] == "Choline":
                Choline = float(examine_origin[1])
                Choline_Unit = Choline / weight
                Choline = round(((Choline_Unit * scale_value) + Choline), 1)
                Choline_Value = round(((Choline/550) * 100), 1)
                update_scale.write("Choline" + "*" + str(Choline) + "*" + str(Choline_Value) + "*" + "mg" + "\n")
            elif examine_origin[0] == "Calcium":
                Calcium = float(examine_origin[1])
                Calcium_Unit = Calcium / weight
                Calcium = round(((Calcium_Unit * scale_value) + Calcium), 1)
                Calcium_Value = round(((Calcium/1000) * 100), 1)
                update_scale.write("Calcium" + "*" + str(Calcium) + "*" + str(Calcium_Value) + "*" + "mg" + "\n")
            elif examine_origin[0] == "Chromium":
                Chromium = float(examine_origin[1])
                Chromium_Unit = Chromium / weight
                Chromium = round(((Chromium_Unit * scale_value) + Chromium), 3)
                Chromium_Value = round(((Chromium/35) * 100), 1)
                update_scale.write("Chromium" + "*" + str(Chromium) + "*" + str(Chromium_Value) + "*" + "mcg" + "\n")
            elif examine_origin[0] == "Copper":
                Copper = float(examine_origin[1])
                Copper_Unit = Copper / weight
                Copper = round(((Copper_Unit * scale_value) + Copper), 1)
                Copper_Value = round(((Copper/900) * 100), 1)
                update_scale.write("Copper" + "*" + str(Copper) + "*" + str(Copper_Value) + "*" + "mcg" + "\n")
            elif examine_origin[0] == "Fluoride":
                Fluoride = float(examine_origin[1])
                Fluoride_Unit = Fluoride / weight
                Fluoride = round(((Fluoride_Unit * scale_value) + Fluoride), 3)
                Fluoride_Value = round(((Fluoride/4) * 100), 1)
                update_scale.write("Fluoride" + "*" + str(Fluoride) + "*" + str(Fluoride_Value) + "*" + "mg" + "\n")
            elif examine_origin[0] == "Iodine":
                Iodine = float(examine_origin[1])
                Iodine_Unit = Iodine / weight
                Iodine = round(((Iodine_Unit * scale_value) + Iodine), 2)
                Iodine_Value = round(((Iodine/150) * 100), 1)
                update_scale.write("Iodine" + "*" + str(Iodine) + "*" + str(Iodine_Value) + "*" + "mcg" + "\n")
            elif examine_origin[0] == "Iron":
                Iron = float(examine_origin[1])
                Iron_Unit = Iron / weight
                Iron = round(((Iron_Unit * scale_value) + Iron), 3)
                Iron_Value = round(((Iron/8) * 100), 1)
                update_scale.write("Iron" + "*" + str(Iron) + "*" + str(Iron_Value) + "*" + "mg" + "\n")
            elif examine_origin[0] == "Magnesium":
                Magnesium = float(examine_origin[1])
                Magnesium_Unit = Magnesium / weight
                Magnesium = round(((Magnesium_Unit * scale_value) + Magnesium), 1)
                Magnesium_Value = round(((Magnesium/400) * 100), 1)
                update_scale.write("Magnesium" + "*" + str(Magnesium) + "*" + str(Magnesium_Value) + "*" + "mg" + "\n")
            elif examine_origin[0] == "Manganese":
                Manganese = float(examine_origin[1])
                Manganese_Unit = Manganese / weight
                Manganese = round(((Manganese_Unit * scale_value) + Manganese), 3)
                Manganese_Value = round(((Manganese/2.3) * 100), 1)
                update_scale.write("Manganese" + "*" + str(Manganese) + "*" + str(Manganese_Value) + "*" + "mg" + "\n")
            elif examine_origin[0] == "Molybdenum":
                Molybdenum = float(examine_origin[1])
                Molybdenum_Unit = Molybdenum / weight
                Molybdenum = round(((Molybdenum_Unit * scale_value) + Molybdenum), 3)
                Molybdenum_Value = round(((Molybdenum/45) * 100), 1)
                update_scale.write("Molybdenum" + "*" + str(Molybdenum) + "*" + str(Molybdenum_Value) + "*" + "mcg" + "\n")
            elif examine_origin[0] == "Phosphorus":
                Phosphorus = float(examine_origin[1])
                Phosphorus_Unit = Phosphorus / weight
                Phosphorus = round(((Phosphorus_Unit * scale_value) + Phosphorus), 1)
                Phosphorus_Value = round(((Phosphorus/700) * 100), 1)
                update_scale.write("Phosphorus" + "*" + str(Phosphorus) + "*" + str(Phosphorus_Value) + "*" + "mg" + "\n")
            elif examine_origin[0] == "Selenium":
                Selenium = float(examine_origin[1])
                Selenium_Unit = Selenium / weight
                Selenium = round(((Selenium_Unit * scale_value) + Selenium), 2)
                Selenium_Value = round(((Selenium/55) * 100), 1)
                update_scale.write("Selenium" + "*" + str(Selenium) + "*" + str(Selenium_Value) + "*" + "mcg" + "\n")
            elif examine_origin[0] == "Zinc":
                Zinc = float(examine_origin[1])
                Zinc_Unit = Zinc / weight
                Zinc = round(((Zinc_Unit * scale_value) + Zinc), 3)
                Zinc_Value = round(((Zinc/11) * 100), 1)
                update_scale.write("Zinc" + "*" + str(Zinc) + "*" + str(Zinc_Value) + "*" + "mg" + "\n")
            elif examine_origin[0] == "Potassium":
                Potassium = float(examine_origin[1])
                Potassium_Unit = Potassium / weight
                Potassium = round(((Potassium_Unit * scale_value) + Potassium), 1)
                Potassium_Value = round(((Potassium/3400) * 100), 1)
                update_scale.write("Potassium" + "*" + str(Potassium) + "*" + str(Potassium_Value) + "*" + "mg" + "\n")
            elif examine_origin[0] == "Sodium":
                Sodium = float(examine_origin[1])
                Sodium_Unit = Sodium / weight
                Sodium = round(((Sodium_Unit * scale_value) + Sodium), 1)
                Sodium_Value = round(((Sodium/1500) * 100), 1)
                update_scale.write("Sodium" + "*" + str(Sodium) + "*" + str(Sodium_Value) + "*" + "mg" + "\n")
            elif examine_origin[0] == "Chloride":
                Chloride = float(examine_origin[1])
                Chloride_Unit = Chloride / weight
                Chloride = round(((Chloride_Unit * scale_value) + Chloride), 3)
                Chloride_Value = round(((Chloride/2.3) * 100), 1)
                update_scale.write("Chloride" + "*" + str(Chloride) + "*" + str(Chloride_Value) + "*" + "g" + "\n")
            else:
                update_scale.write("Error" + "*" + "---" + "*" + "---" + "*" + "-" + "\n")
            origin_items = origin_items - 1
            start_origin = start_origin + 1
        update_scale.close()
        food_library()
    #Scale Down
    elif (event.x < 600) and (event.x > 495) and (event.y >= 255) and (event.y < 262):
        lib_canvas.create_rectangle(495, 255, 600, 262, fill="lime")
        # read SS
        scale_file = "/SS.txt"
        origin_data = open(polyfile + scale_file, "r", encoding="utf8")
        read_origin = origin_data.read().splitlines()
        origin_data.close()
        update_scale = open(polyfile + scale_file, "w", encoding="utf8")
        update_scale.write("update\n")
        update_scale.write(read_origin[1] + "\n")
        scale_value = float(read_origin[4])
        weight = float(read_origin[2])
        new_weight = weight - scale_value
        update_scale.write(str(new_weight) + "\n")
        update_scale.write(read_origin[3] + "\n")
        update_scale.write(str(scale_value) + "\n")
        origin_items = len(read_origin)
        start_origin = 5
        while origin_items != 5:
            examine_origin = (read_origin[start_origin]).split("*")
            if examine_origin[0] == "Calories":
                Calories = float(examine_origin[1])
                Calorie_Unit = Calories / weight
                Calories = abs(round(((Calorie_Unit * scale_value) - Calories), 1))
                Calories_Value = "---"
                update_scale.write("Calories" + "*" + str(Calories) + "*" + Calories_Value + "*" + "cal" + "\n")
            elif examine_origin[0] == "Total Fat":
                TotalFat = float(examine_origin[1])
                TotalFat_Unit = TotalFat / weight
                TotalFat = abs(round(((TotalFat_Unit * scale_value) - TotalFat), 2))
                TotalFat_Value = round(((TotalFat / 77) * 100), 1)
                update_scale.write("Total Fat" + "*" + str(TotalFat) + "*" + str(TotalFat_Value) + "*" + "g" + "\n")
            elif examine_origin[0] == "Saturated Fat":
                SaturatedFat = float(examine_origin[1])
                SaturatedFat_Unit = SaturatedFat / weight
                SaturatedFat = abs(round(((SaturatedFat_Unit * scale_value) - SaturatedFat), 2))
                SaturatedFat_Value = round(((SaturatedFat / 22) * 100), 1)
                update_scale.write(
                    "Saturated Fat" + "*" + str(SaturatedFat) + "*" + str(SaturatedFat_Value) + "*" + "g" + "\n")
            elif examine_origin[0] == "Cholesterol":
                Cholesterol = float(examine_origin[1])
                Cholesterol_Unit = Cholesterol / weight
                Cholesterol = abs(round(((Cholesterol_Unit * scale_value) - Cholesterol), 1))
                Cholesterol_Value = round(((Cholesterol / 300) * 100), 1)
                update_scale.write(
                    "Cholesterol" + "*" + str(Cholesterol) + "*" + str(Cholesterol_Value) + "*" + "g" + "\n")
            elif examine_origin[0] == "Protein":
                Protein = float(examine_origin[1])
                Protein_Unit = Protein / weight
                Protein = abs(round(((Protein_Unit * scale_value) - Protein), 2))
                Protein_Value = round(((Protein / 56) * 100), 1)
                update_scale.write("Protein" + "*" + str(Protein) + "*" + str(Protein_Value) + "*" + "g" + "\n")
            elif examine_origin[0] == "Carbohydrate":
                Carbohydrate = float(examine_origin[1])
                Carbohydrate_Unit = Carbohydrate / weight
                Carbohydrate = abs(round(((Carbohydrate_Unit * scale_value) - Carbohydrate), 2))
                Carbohydrate_Value = round(((Carbohydrate/130) * 100), 1)
                update_scale.write("Carbohydrate" + "*" + str(Carbohydrate) + "*" + str(Carbohydrate_Value) + "*" + "g" + "\n")
            elif examine_origin[0] == "Fiber":
                Fiber = float(examine_origin[1])
                Fiber_Unit = Fiber / weight
                Fiber = abs(round(((Fiber_Unit * scale_value) - Fiber), 2))
                Fiber_Value = round(((Fiber/38) * 100), 1)
                update_scale.write("Fiber" + "*" + str(Fiber) + "*" + str(Fiber_Value) + "*" + "g" + "\n")
            elif examine_origin[0] == "Linoleic Acid":
                LinoleicAcid = float(examine_origin[1])
                LinoleicAcid_Unit = LinoleicAcid / weight
                LinoleicAcid = abs(round(((LinoleicAcid_Unit * scale_value) - LinoleicAcid), 2))
                LinoleicAcid_Value = round(((LinoleicAcid / 17) * 100), 1)
                update_scale.write(
                    "Linoleic Acid" + "*" + str(LinoleicAcid) + "*" + str(LinoleicAcid_Value) + "*" + "g" + "\n")
            elif examine_origin[0] == "Alpha Linoleic Acid":
                ALA = float(examine_origin[1])
                ALA_Unit = ALA / weight
                ALA = abs(round(((ALA_Unit * scale_value) - ALA), 3))
                ALA_Value = round(((ALA / 1.6) * 100), 1)
                update_scale.write("Alpha Linoleic Acid" + "*" + str(ALA) + "*" + str(ALA_Value) + "*" + "g" + "\n")
            elif examine_origin[0] == "Vitamin A":
                VitaminA = float(examine_origin[1])
                VitaminA_Unit = VitaminA / weight
                VitaminA = abs(round(((VitaminA_Unit * scale_value) - VitaminA), 1))
                VitaminA_Value = round(((VitaminA / 900) * 100), 1)
                update_scale.write("Vitamin A" + "*" + str(VitaminA) + "*" + str(VitaminA_Value) + "*" + "mcg" + "\n")
            elif examine_origin[0] == "Vitamin C":
                VitaminC = float(examine_origin[1])
                VitaminC_Unit = VitaminC / weight
                VitaminC = abs(round(((VitaminC_Unit * scale_value) - VitaminC), 2))
                VitaminC_Value = round(((VitaminC / 90) * 100), 1)
                update_scale.write("Vitamin C" + "*" + str(VitaminC) + "*" + str(VitaminC_Value) + "*" + "mg" + "\n")
            elif examine_origin[0] == "Vitamin D":
                VitaminD = float(examine_origin[1])
                VitaminD_Unit = VitaminD / weight
                VitaminD = abs(round(((VitaminD_Unit * scale_value) - VitaminD), 3))
                VitaminD_Value = round(((VitaminD / 15) * 100), 1)
                update_scale.write("Vitamin D" + "*" + str(VitaminD) + "*" + str(VitaminD_Value) + "*" + "mcg" + "\n")
            elif examine_origin[0] == "Vitamin E":
                VitaminE = float(examine_origin[1])
                VitaminE_Unit = VitaminE / weight
                VitaminE = abs(round(((VitaminE_Unit * scale_value) - VitaminE), 3))
                VitaminE_Value = round(((VitaminE / 15) * 100), 1)
                update_scale.write("Vitamin E" + "*" + str(VitaminE) + "*" + str(VitaminE_Value) + "*" + "mg" + "\n")
            elif examine_origin[0] == "Vitamin K":
                VitaminK = float(examine_origin[1])
                VitaminK_Unit = VitaminK / weight
                VitaminK = abs(round(((VitaminK_Unit * scale_value) - VitaminK), 2))
                VitaminK_Value = round(((VitaminK / 120) * 100), 1)
                update_scale.write("Vitamin K" + "*" + str(VitaminK) + "*" + str(VitaminK_Value) + "*" + "mcg" + "\n")
            elif examine_origin[0] == "Thiamin":
                Thiamin = float(examine_origin[1])
                Thiamin_Unit = Thiamin / weight
                Thiamin = abs(round(((Thiamin_Unit * scale_value) - Thiamin), 3))
                Thiamin_Value = round(((Thiamin / 1.2) * 100), 1)
                update_scale.write("Thiamin" + "*" + str(Thiamin) + "*" + str(Thiamin_Value) + "*" + "mg" + "\n")
            elif examine_origin[0] == "Riboflavin":
                Riboflavin = float(examine_origin[1])
                Riboflavin_Unit = Riboflavin / weight
                Riboflavin = abs(round(((Riboflavin_Unit * scale_value) - Riboflavin), 3))
                Riboflavin_Value = round(((Riboflavin / 1.3) * 100), 1)
                update_scale.write(
                    "Riboflavin" + "*" + str(Riboflavin) + "*" + str(Riboflavin_Value) + "*" + "mg" + "\n")
            elif examine_origin[0] == "Niacin":
                Niacin = float(examine_origin[1])
                Niacin_Unit = Niacin / weight
                Niacin = abs(round(((Niacin_Unit * scale_value) - Niacin), 3))
                Niacin_Value = round(((Niacin / 16) * 100), 1)
                update_scale.write("Niacin" + "*" + str(Niacin) + "*" + str(Niacin_Value) + "*" + "mg" + "\n")
            elif examine_origin[0] == "Vitamin B6":
                VitaminB6 = float(examine_origin[1])
                VitaminB6_Unit = VitaminB6 / weight
                VitaminB6 = abs(round(((VitaminB6_Unit * scale_value) - VitaminB6), 3))
                VitaminB6_Value = round(((VitaminB6 / 1.3) * 100), 1)
                update_scale.write("Vitamin B6" + "*" + str(VitaminB6) + "*" + str(VitaminB6_Value) + "*" + "mg" + "\n")
            elif examine_origin[0] == "Folate":
                Folate = float(examine_origin[1])
                Folate_Unit = Folate / weight
                Folate = abs(round(((Folate_Unit * scale_value) - Folate), 1))
                Folate_Value = round(((Folate / 400) * 100), 1)
                update_scale.write("Folate" + "*" + str(Folate) + "*" + str(Folate_Value) + "*" + "mcg" + "\n")
            elif examine_origin[0] == "Vitamin B12":
                VitaminB12 = float(examine_origin[1])
                VitaminB12_Unit = VitaminB12 / weight
                VitaminB12 = abs(round(((VitaminB12_Unit * scale_value) - VitaminB12), 3))
                VitaminB12_Value = round(((VitaminB12 / 2.4) * 100), 1)
                update_scale.write(
                    "Vitamin B12" + "*" + str(VitaminB12) + "*" + str(VitaminB12_Value) + "*" + "mcg" + "\n")
            elif examine_origin[0] == "Pantothenic Acid":
                PantothenicAcid = float(examine_origin[1])
                PantothenicAcid_Unit = PantothenicAcid / weight
                PantothenicAcid = abs(round(((PantothenicAcid_Unit * scale_value) - PantothenicAcid), 3))
                PantothenicAcid_Value = round(((PantothenicAcid / 5) * 100), 1)
                update_scale.write("Pantothenic Acid" + "*" + str(PantothenicAcid) + "*" + str(
                    PantothenicAcid_Value) + "*" + "mg" + "\n")
            elif examine_origin[0] == "Biotin":
                Biotin = float(examine_origin[1])
                Biotin_Unit = Biotin / weight
                Biotin = abs(round(((Biotin_Unit * scale_value) - Biotin), 3))
                Biotin_Value = round(((Biotin / 30) * 100), 1)
                update_scale.write("Biotin" + "*" + str(Biotin) + "*" + str(Biotin_Value) + "*" + "mcg" + "\n")
            elif examine_origin[0] == "Choline":
                Choline = float(examine_origin[1])
                Choline_Unit = Choline / weight
                Choline = abs(round(((Choline_Unit * scale_value) - Choline), 1))
                Choline_Value = round(((Choline / 550) * 100), 1)
                update_scale.write("Choline" + "*" + str(Choline) + "*" + str(Choline_Value) + "*" + "mg" + "\n")
            elif examine_origin[0] == "Calcium":
                Calcium = float(examine_origin[1])
                Calcium_Unit = Calcium / weight
                Calcium = abs(round(((Calcium_Unit * scale_value) - Calcium), 1))
                Calcium_Value = round(((Calcium / 1000) * 100), 1)
                update_scale.write("Calcium" + "*" + str(Calcium) + "*" + str(Calcium_Value) + "*" + "mg" + "\n")
            elif examine_origin[0] == "Chromium":
                Chromium = float(examine_origin[1])
                Chromium_Unit = Chromium / weight
                Chromium = abs(round(((Chromium_Unit * scale_value) - Chromium), 3))
                Chromium_Value = round(((Chromium / 35) * 100), 1)
                update_scale.write("Chromium" + "*" + str(Chromium) + "*" + str(Chromium_Value) + "*" + "mcg" + "\n")
            elif examine_origin[0] == "Copper":
                Copper = float(examine_origin[1])
                Copper_Unit = Copper / weight
                Copper = abs(round(((Copper_Unit * scale_value) - Copper), 1))
                Copper_Value = round(((Copper / 900) * 100), 1)
                update_scale.write("Copper" + "*" + str(Copper) + "*" + str(Copper_Value) + "*" + "mcg" + "\n")
            elif examine_origin[0] == "Fluoride":
                Fluoride = float(examine_origin[1])
                Fluoride_Unit = Fluoride / weight
                Fluoride = abs(round(((Fluoride_Unit * scale_value) - Fluoride), 3))
                Fluoride_Value = round(((Fluoride / 4) * 100), 1)
                update_scale.write("Fluoride" + "*" + str(Fluoride) + "*" + str(Fluoride_Value) + "*" + "mg" + "\n")
            elif examine_origin[0] == "Iodine":
                Iodine = float(examine_origin[1])
                Iodine_Unit = Iodine / weight
                Iodine = abs(round(((Iodine_Unit * scale_value) - Iodine), 2))
                Iodine_Value = round(((Iodine / 150) * 100), 1)
                update_scale.write("Iodine" + "*" + str(Iodine) + "*" + str(Iodine_Value) + "*" + "mcg" + "\n")
            elif examine_origin[0] == "Iron":
                Iron = float(examine_origin[1])
                Iron_Unit = Iron / weight
                Iron = abs(round(((Iron_Unit * scale_value) - Iron), 3))
                Iron_Value = round(((Iron / 8) * 100), 1)
                update_scale.write("Iron" + "*" + str(Iron) + "*" + str(Iron_Value) + "*" + "mg" + "\n")
            elif examine_origin[0] == "Magnesium":
                Magnesium = float(examine_origin[1])
                Magnesium_Unit = Magnesium / weight
                Magnesium = abs(round(((Magnesium_Unit * scale_value) - Magnesium), 1))
                Magnesium_Value = round(((Magnesium / 400) * 100), 1)
                update_scale.write("Magnesium" + "*" + str(Magnesium) + "*" + str(Magnesium_Value) + "*" + "mg" + "\n")
            elif examine_origin[0] == "Manganese":
                Manganese = float(examine_origin[1])
                Manganese_Unit = Manganese / weight
                Manganese = abs(round(((Manganese_Unit * scale_value) - Manganese), 3))
                Manganese_Value = round(((Manganese / 2.3) * 100), 1)
                update_scale.write("Manganese" + "*" + str(Manganese) + "*" + str(Manganese_Value) + "*" + "mg" + "\n")
            elif examine_origin[0] == "Molybdenum":
                Molybdenum = float(examine_origin[1])
                Molybdenum_Unit = Molybdenum / weight
                Molybdenum = abs(round(((Molybdenum_Unit * scale_value) - Molybdenum), 3))
                Molybdenum_Value = round(((Molybdenum / 45) * 100), 1)
                update_scale.write(
                    "Molybdenum" + "*" + str(Molybdenum) + "*" + str(Molybdenum_Value) + "*" + "mcg" + "\n")
            elif examine_origin[0] == "Phosphorus":
                Phosphorus = float(examine_origin[1])
                Phosphorus_Unit = Phosphorus / weight
                Phosphorus = abs(round(((Phosphorus_Unit * scale_value) - Phosphorus), 1))
                Phosphorus_Value = round(((Phosphorus / 700) * 100), 1)
                update_scale.write(
                    "Phosphorus" + "*" + str(Phosphorus) + "*" + str(Phosphorus_Value) + "*" + "mg" + "\n")
            elif examine_origin[0] == "Selenium":
                Selenium = float(examine_origin[1])
                Selenium_Unit = Selenium / weight
                Selenium = abs(round(((Selenium_Unit * scale_value) - Selenium), 2))
                Selenium_Value = round(((Selenium / 55) * 100), 1)
                update_scale.write("Selenium" + "*" + str(Selenium) + "*" + str(Selenium_Value) + "*" + "mcg" + "\n")
            elif examine_origin[0] == "Zinc":
                Zinc = float(examine_origin[1])
                Zinc_Unit = Zinc / weight
                Zinc = abs(round(((Zinc_Unit * scale_value) - Zinc), 3))
                Zinc_Value = round(((Zinc / 11) * 100), 1)
                update_scale.write("Zinc" + "*" + str(Zinc) + "*" + str(Zinc_Value) + "*" + "mg" + "\n")
            elif examine_origin[0] == "Potassium":
                Potassium = float(examine_origin[1])
                Potassium_Unit = Potassium / weight
                Potassium = abs(round(((Potassium_Unit * scale_value) - Potassium), 1))
                Potassium_Value = round(((Potassium / 3400) * 100), 1)
                update_scale.write("Potassium" + "*" + str(Potassium) + "*" + str(Potassium_Value) + "*" + "mg" + "\n")
            elif examine_origin[0] == "Sodium":
                Sodium = float(examine_origin[1])
                Sodium_Unit = Sodium / weight
                Sodium = abs(round(((Sodium_Unit * scale_value) - Sodium), 1))
                Sodium_Value = round(((Sodium / 1500) * 100), 1)
                update_scale.write("Sodium" + "*" + str(Sodium) + "*" + str(Sodium_Value) + "*" + "mg" + "\n")
            elif examine_origin[0] == "Chloride":
                Chloride = float(examine_origin[1])
                Chloride_Unit = Chloride / weight
                Chloride = abs(round(((Chloride_Unit * scale_value) - Chloride), 3))
                Chloride_Value = round(((Chloride / 2.3) * 100), 1)
                update_scale.write("Chloride" + "*" + str(Chloride) + "*" + str(Chloride_Value) + "*" + "g" + "\n")
            else:
                update_scale.write("Error" + "*" + "---" + "*" + "---" + "*" + "-" + "\n")
            origin_items = origin_items - 1
            start_origin = start_origin + 1
        update_scale.close()
        food_library()




def no_records_found():
    #clear canvas and re-intialize
    lib_canvas.delete("all")
    lib_canvas.create_rectangle(3, 3, 1255, 590, outline="grey")
    lib_canvas.create_line(3, 55, 1255, 55, width=2, fill="cyan4")
    lib_canvas.create_line(292, 3, 292, 55, width=2, fill="cyan4")
    lib_canvas.create_image(925, 0, anchor=NW, image=img)

    # unbind buttons
    lib_canvas.unbind('<Button>')

    #display no data
    request = (search_field.get())
    lib_canvas.create_text(627, 275, text="No records found for:", font=("Comic Sans MS", 20))
    lib_canvas.create_text(627, 315, text=request, font=("Comic Sans MS", 20))


def health_library():
    # clear canvas and re-intialize
    lib_canvas.delete("all")
    lib_canvas.create_rectangle(3, 3, 1255, 590, outline="grey")
    lib_canvas.create_line(3, 55, 1255, 55, fill="cyan4")
    lib_canvas.create_line(292, 3, 292, 55, fill="cyan4")
    lib_canvas.create_image(925, 0, anchor=NW, image=img)

    #unbind buttons
    lib_canvas.unbind('<Button>')

    #search and find data
    library = os.getcwd()
    health_lib = library + "/Health_Lib"
    request = (search_field.get()).casefold()
    request = request + ".txt"

    #search library
    data = "0"
    lookup = [f.path for f in os.scandir(health_lib) if f.is_file()]
    for item in lookup:
        file = path.basename(item)
        if file.casefold() == request:
            data = item

    #read and display data
    if data != "0":
        #read data
        read_request = open(data, "r", encoding="utf8")
        store_request = read_request.read()
        read_request.close()

        split_request = store_request.split(":")
        Title = split_request[0]
        Heading_One = split_request[1]
        Section_One = split_request[2]
        Heading_Two = split_request[3]
        Section_Two = split_request[4]
        Table_Heading = split_request[5]
        Sub_Heading_One = split_request[6]
        Sub_Heading_Two = split_request[7]
        Sub_Heading_Three = split_request[8]

        #Display Title
        lib_canvas.create_text(628, 48, text=Title, font=("Times New Roman", 20))

        #Display Heading One
        lib_canvas.create_line(50, 65, 300, 65, width=2, dash=(1, 3), fill="cyan4")
        lib_canvas.create_text(175, 75, text=Heading_One, font=("Comic Sans MS", 10))
        lib_canvas.create_line(50, 85, 300, 85, width=2, dash=(1, 3), fill="cyan4")

        #Display Section One
        lines = Section_One.split("}")
        line_count = len(lines)
        line_val = 0
        while line_count != 0:
            line_y = (line_val * 18) + 72
            lib_canvas.create_text(50, line_y, text=lines[line_val],
                                   font=("Comic Sans MS", 10), anchor=NW)
            line_val = line_val + 1
            line_count = line_count - 1

        #Create Table
        lib_canvas.create_line(610, 245, 610, 590, width=2, fill="grey")
        lib_canvas.create_line(4, 245, 610, 245, width=2, fill="grey")

        #Display Heading Two
        lib_canvas.create_line(670, 260, 890, 260, width=2, dash=(1, 3), fill="cyan4")
        lib_canvas.create_text(780, 270, text=Heading_Two, font=("Comic Sans MS", 10))
        lib_canvas.create_line(670, 280, 890, 280, width=2, dash=(1, 3), fill="cyan4")

        #Display Section Two
        lines = Section_Two.split("}")
        line_count = len(lines)
        line_val = 0
        while line_count != 0:
            line_y = (line_val * 18) + 270
            lib_canvas.create_text(670, line_y, text=lines[line_val],
                                   font=("Comic Sans MS", 10), anchor=NW)
            line_val = line_val + 1
            line_count = line_count - 1

        #Build Table with nutrition info
        #Build Table Lines
        table_lines = 14
        t_start = 305
        while table_lines != 0:
            lib_canvas.create_line(4, t_start, 610, t_start, fill="cyan4")
            t_start = t_start + 20
            table_lines = table_lines - 1

        #construct table data
        items_L = len(split_request) - 9
        if items_L <= 16:
            lib_canvas.create_line(4, 265, 610, 265, width=2, fill="grey")
            lib_canvas.create_line(4, 285, 610, 285, width=2, fill="grey")
            lib_canvas.create_line(570, 265, 570, 590, width=2, fill="grey")
            lib_canvas.create_line(510, 265, 510, 590, width=2, fill="grey")
            lib_canvas.create_line(4, 590, 610, 590, width=2, fill="grey")
            lib_canvas.create_line(4, 245, 4, 590, width=2, fill="grey")

            #Add Table Headings
            lib_canvas.create_text(270, 255, text=Table_Heading, font=("Comic Sans MS", 10))
            lib_canvas.create_text(270, 275, text=Sub_Heading_One, font=("Comic Sans MS", 10))
            lib_canvas.create_text(540, 275, text=Sub_Heading_Two, font=("Comic Sans MS", 10))
            lib_canvas.create_text(590, 275, text=Sub_Heading_Three, font=("Comic Sans MS", 10))

            #insert table data
            initialize = 9
            y_start = 290
            while items_L != 1:
                working_item = split_request[initialize]
                split_work = working_item.split("*")
                food_name = split_work[0]
                milligrams = split_work[1]
                daily_value = split_work[2]
                lib_canvas.create_text(270, y_start, text=food_name,
                                       font=("Comic Sans MS", 10))
                lib_canvas.create_text(540, y_start+10, text=milligrams,
                                       font=("Comic Sans MS", 10))
                lib_canvas.create_text(590, y_start+10, text=(daily_value + "%"),
                                       font=("Comic Sans MS", 10))
                initialize = initialize + 1
                items_L = items_L - 1
                y_start = y_start + 20
        else:
            lib_canvas.create_line(4, 265, 610, 265, width=2, fill="grey")
            lib_canvas.create_line(4, 285, 610, 285, width=2, fill="grey")
            lib_canvas.create_line(570, 265, 570, 590, width=2, fill="grey")
            lib_canvas.create_line(510, 265, 510, 590, width=2, fill="grey")
            lib_canvas.create_line(4, 590, 610, 590, width=2, fill="grey")
            lib_canvas.create_line(4, 245, 4, 590, width=2, fill="grey")
            lib_canvas.create_line(305, 265, 305, 590, width=2, fill="grey")
            lib_canvas.create_line(265, 265, 265, 590, width=2, fill="grey")
            lib_canvas.create_line(205, 265, 205, 590, width=2, fill="grey")

            # Add Table Headings
            lib_canvas.create_text(305, 255, text=Table_Heading, font=("Comic Sans MS", 10))
            lib_canvas.create_text(103, 275, text=Sub_Heading_One, font=("Comic Sans MS", 10))
            lib_canvas.create_text(408, 275, text=Sub_Heading_One, font=("Comic Sans MS", 10))
            lib_canvas.create_text(235, 275, text=Sub_Heading_Two, font=("Comic Sans MS", 10))
            lib_canvas.create_text(540, 275, text=Sub_Heading_Two, font=("Comic Sans MS", 10))
            lib_canvas.create_text(285, 275, text=Sub_Heading_Three, font=("Comic Sans MS", 10))
            lib_canvas.create_text(590, 275, text=Sub_Heading_Three, font=("Comic Sans MS", 10))

            initialize = 9
            y_start = 290
            x_1 = 103
            x_2 = 235
            x_3 = 285
            while items_L != 1:
                working_item = split_request[initialize]
                split_work = working_item.split("*")
                food_name = split_work[0]
                milligrams = split_work[1]
                daily_value = split_work[2]
                lib_canvas.create_text(x_1, y_start, text=food_name,
                                       font=("Comic Sans MS", 10))
                lib_canvas.create_text(x_2, y_start + 10, text=milligrams,
                                       font=("Comic Sans MS", 10))
                lib_canvas.create_text(x_3, y_start + 10, text=(daily_value + "%"),
                                       font=("Comic Sans MS", 10))
                initialize = initialize + 1
                items_L = items_L - 1
                y_start = y_start + 20
                if y_start > 570:
                    y_start = 290
                    x_1 = 408
                    x_2 = 540
                    x_3 = 590

def food_library():
    # clear canvas and re-intialize
    lib_canvas.delete("all")
    lib_canvas.create_rectangle(3, 3, 1255, 590, outline="grey")
    lib_canvas.create_line(3, 55, 1255, 55, fill="cyan4")
    lib_canvas.create_line(292, 3, 292, 55, fill="cyan4")
    lib_canvas.create_image(925, 0, anchor=NW, image=img)

    #search and find data
    library = os.getcwd()
    food_lib = library + "/Food_Lib"
    request = (search_field.get()).casefold()
    request = request + ".txt"

    # key binding for scaling/logging data
    lib_canvas.bind('<Button>', scale_log)

    #search library
    data = "0"
    lookup = [f.path for f in os.scandir(food_lib) if f.is_file()]
    for item in lookup:
        file = path.basename(item)
        if file.casefold() == request:
            data = item

    #read and display data
    if data != "0":
        #read data
        read_request = open(data, "r", encoding="utf8")
        store_request = read_request.read()
        read_request.close()

        split_request = store_request.split(":")
        Title = split_request[0]
        Heading_One = split_request[1]
        Section_One = split_request[2]
        Heading_Two = split_request[3]
        Section_Two = split_request[4]
        Table_Heading = split_request[5]
        Sub_Heading_One = split_request[6] + split_request[7] + split_request[8]
        Sub_Heading_Two = split_request[9]
        Sub_Heading_Three = split_request[10]
        Scale_Factor = split_request[11]

        #Display Title
        lib_canvas.create_text(628, 48, text=Title, font=("Times New Roman", 20))

        #Display Heading One
        lib_canvas.create_line(50, 65, 300, 65, width=2, dash=(1, 3), fill="cyan4")
        lib_canvas.create_text(175, 75, text=Heading_One, font=("Comic Sans MS", 10))
        lib_canvas.create_line(50, 85, 300, 85, width=2, dash=(1, 3), fill="cyan4")

        #Display Section One
        lines = Section_One.split("}")
        line_count = len(lines)
        line_val = 0
        while line_count != 0:
            line_y = (line_val * 18) + 72
            lib_canvas.create_text(50, line_y, text=lines[line_val],
                                   font=("Comic Sans MS", 10), anchor=NW)
            line_val = line_val + 1
            line_count = line_count - 1

        #Create Table
        lib_canvas.create_line(610, 245, 610, 590, width=2, fill="grey")
        lib_canvas.create_line(4, 245, 610, 245, width=2, fill="grey")

        #Display Heading Two
        lib_canvas.create_line(670, 260, 890, 260, width=2, dash=(1, 3), fill="cyan4")
        lib_canvas.create_text(780, 270, text=Heading_Two, font=("Comic Sans MS", 10))
        lib_canvas.create_line(670, 280, 890, 280, width=2, dash=(1, 3), fill="cyan4")

        #Display Section Two
        lines = Section_Two.split("}")
        line_count = len(lines)
        line_val = 0
        while line_count != 0:
            line_y = (line_val * 18) + 270
            lib_canvas.create_text(670, line_y, text=lines[line_val],
                                   font=("Comic Sans MS", 10), anchor=NW)
            line_val = line_val + 1
            line_count = line_count - 1

        #Build Table with nutrition info
        #Build Table Lines
        table_lines = 14
        t_start = 305
        while table_lines != 0:
            lib_canvas.create_line(4, t_start, 610, t_start, fill="cyan4")
            t_start = t_start + 20
            table_lines = table_lines - 1

        #construct table data
        items_L = len(split_request) - 12
        if items_L <= 16:
            lib_canvas.create_line(4, 265, 610, 265, width=2, fill="grey")
            lib_canvas.create_line(4, 285, 610, 285, width=2, fill="grey")
            lib_canvas.create_line(570, 265, 570, 590, width=2, fill="grey")
            lib_canvas.create_line(510, 265, 510, 590, width=2, fill="grey")
            lib_canvas.create_line(4, 590, 610, 590, width=2, fill="grey")
            lib_canvas.create_line(4, 245, 4, 590, width=2, fill="grey")

            #insert table data
            initialize = 12
            y_start = 290
            #open scale storage
            update = False
            push = 0
            if path.exists(polyfile + "/SS.txt"):
                update_check = open(polyfile + "/SS.txt", "r", encoding="utf8")
                re_up = update_check.read().splitlines()
                update_check.close()
                if re_up[0] == "update":
                    update = True
                    weight = re_up[2] + re_up[3]
                    alt_heading = re_up[1] + re_up[2] + re_up[3]
                    origin = 5
                    push = 10
            if update == False:
                SS = open(polyfile + "/SS.txt", "w", encoding='utf8')
                SS.write("origin" + "\n")
                SS.write(split_request[6] + "\n")
                SS.write(split_request[7] + "\n")
                SS.write(split_request[8] + "\n")
                SS.write(Scale_Factor)
            while items_L != 1:
                if update == False:
                    working_item = split_request[initialize]
                    split_work = working_item.split("*")
                    food_name = split_work[0]
                    milligrams = split_work[1]
                    daily_value = split_work[2]
                    SI_Unit = split_work[3]
                else:
                    working_item = re_up[origin]
                    split_work = working_item.split("*")
                    food_name = split_work[0]
                    milligrams = split_work[1]
                    daily_value = split_work[2]
                    SI_Unit = split_work[3]
                lib_canvas.create_text(270, y_start + push, text=food_name,
                                       font=("Comic Sans MS", 10))
                lib_canvas.create_text(540, y_start+10, text=milligrams + SI_Unit,
                                       font=("Comic Sans MS", 10))
                lib_canvas.create_text(590, y_start+10, text=(daily_value + "%"),
                                       font=("Comic Sans MS", 10))
                #write data
                if update == False:
                    SS.write(food_name + "*" + milligrams + "*" + daily_value + "*" + SI_Unit)
                initialize = initialize + 1
                items_L = items_L - 1
                y_start = y_start + 20
                if update == True:
                    origin = origin + 1
            if update == False:
                SS.close()

            # Add Table Headings
            lib_canvas.create_text(125, 255, text=Table_Heading, font=("Comic Sans MS", 10))
            if update == False:
                lib_canvas.create_text(270, 275, text=Sub_Heading_One, font=("Comic Sans MS", 10))
            else:
                lib_canvas.create_text(270, 275, text=alt_heading, font=("Comic Sans MS", 10))
            lib_canvas.create_text(540, 275, text=Sub_Heading_Two, font=("Comic Sans MS", 10))
            lib_canvas.create_text(590, 275, text=Sub_Heading_Three, font=("Comic Sans MS", 10))

            # canvas button events
            lib_canvas.create_rectangle(245, 248, 405, 262, fill="lightblue")
            lib_canvas.create_rectangle(493, 248, 600, 262)
            lib_canvas.create_text(325, 255, text="Add to Nutrition Log +",
                                   font=("Comic Sans MS", 10), activefill="blue")
            lib_canvas.create_text(470, 255, text="Scale:",
                                   font=("Comic Sans MS", 10))
            lib_canvas.create_polygon(502, 248, 495, 254, 509, 254, 502, 248, fill="lightblue",
                                      activefill="cyan", outline="black")
            lib_canvas.create_polygon(502, 262, 495, 256, 509, 256, 502, 262, fill="lightblue",
                                      activefill="cyan", outline="black")
            if update == True:
                lib_canvas.create_text(555, 254, text=weight, font=("Comic Sans MS", 9))
        else:
            lib_canvas.create_line(4, 265, 610, 265, width=2, fill="grey")
            lib_canvas.create_line(4, 285, 610, 285, width=2, fill="grey")
            lib_canvas.create_line(570, 265, 570, 590, width=2, fill="grey")
            lib_canvas.create_line(510, 265, 510, 590, width=2, fill="grey")
            lib_canvas.create_line(4, 590, 610, 590, width=2, fill="grey")
            lib_canvas.create_line(4, 245, 4, 590, width=2, fill="grey")
            lib_canvas.create_line(305, 265, 305, 590, width=2, fill="grey")
            lib_canvas.create_line(265, 265, 265, 590, width=2, fill="grey")
            lib_canvas.create_line(205, 265, 205, 590, width=2, fill="grey")

            initialize = 12
            y_start = 290
            x_1 = 103
            x_2 = 235
            x_3 = 285
            # open scale storage
            update = False
            push = 0
            if path.exists(polyfile + "/SS.txt"):
                update_check = open(polyfile + "/SS.txt", "r", encoding="utf8")
                re_up = update_check.read().splitlines()
                update_check.close()
                if re_up[0] == "update":
                    update = True
                    weight = re_up[2] + re_up[3]
                    alt_heading = re_up[1] + re_up[2] + re_up[3]
                    origin = 5
                    push = 10
            if update == False:
                SS = open(polyfile + "/SS.txt", "w", encoding='utf8')
                SS.write("origin" + "\n")
                SS.write(split_request[6] + "\n")
                SS.write(split_request[7] + "\n")
                SS.write(split_request[8] + "\n")
                SS.write(Scale_Factor)
            while items_L != 1:
                if update == False:
                    working_item = split_request[initialize]
                    split_work = working_item.split("*")
                    food_name = split_work[0]
                    milligrams = split_work[1]
                    daily_value = split_work[2]
                    SI_Unit = split_work[3]
                else:
                    working_item = re_up[origin]
                    split_work = working_item.split("*")
                    food_name = split_work[0]
                    milligrams = split_work[1]
                    daily_value = split_work[2]
                    SI_Unit = split_work[3]
                lib_canvas.create_text(x_1, y_start + push, text=food_name,
                                       font=("Comic Sans MS", 10))
                lib_canvas.create_text(x_2, y_start + 10, text=milligrams + SI_Unit,
                                       font=("Comic Sans MS", 10))
                lib_canvas.create_text(x_3, y_start + 10, text=(daily_value + "%"),
                                       font=("Comic Sans MS", 10))
                # write data
                if update == False:
                    SS.write(food_name + "*" + milligrams + "*" + daily_value + "*" + SI_Unit)
                initialize = initialize + 1
                items_L = items_L - 1
                y_start = y_start + 20
                if y_start > 570:
                    y_start = 290
                    x_1 = 408
                    x_2 = 540
                    x_3 = 590
                if update == True:
                    origin = origin + 1
            if update == False:
                SS.close()

            # Add Table Headings
            lib_canvas.create_text(125, 255, text=Table_Heading, font=("Comic Sans MS", 10))
            if update == False:
                lib_canvas.create_text(103, 275, text=Sub_Heading_One, font=("Comic Sans MS", 10))
                lib_canvas.create_text(408, 275, text=Sub_Heading_One, font=("Comic Sans MS", 10))
            else:
                lib_canvas.create_text(103, 275, text=alt_heading, font=("Comic Sans MS", 10))
                lib_canvas.create_text(408, 275, text=alt_heading, font=("Comic Sans MS", 10))
            lib_canvas.create_text(235, 275, text=Sub_Heading_Two, font=("Comic Sans MS", 10))
            lib_canvas.create_text(540, 275, text=Sub_Heading_Two, font=("Comic Sans MS", 10))
            lib_canvas.create_text(285, 275, text=Sub_Heading_Three, font=("Comic Sans MS", 10))
            lib_canvas.create_text(590, 275, text=Sub_Heading_Three, font=("Comic Sans MS", 10))

            # canvas button events
            lib_canvas.create_rectangle(245, 248, 405, 262, fill="lightblue")
            lib_canvas.create_rectangle(493, 248, 600, 262)
            lib_canvas.create_text(325, 255, text="Add to Nutrition Log +",
                                   font=("Comic Sans MS", 10), activefill="blue")
            lib_canvas.create_text(470, 255, text="Scale:",
                                   font=("Comic Sans MS", 10))
            lib_canvas.create_polygon(502, 248, 495, 254, 509, 254, 502, 248, fill="lightblue",
                                      activefill="cyan", outline="black")
            lib_canvas.create_polygon(502, 262, 495, 256, 509, 256, 502, 262, fill="lightblue",
                                      activefill="cyan", outline="black")
            if update == True:
                lib_canvas.create_text(555, 254, text=weight, font=("Comic Sans MS", 9))
def SEARCH():
    library = os.getcwd()
    health_lib = library + "/Health_Lib"
    food_lib = library + "/Food_Lib"
    request = (search_field.get()).casefold()
    request = request + ".txt"

    #delete scale file
    if path.exists(polyfile + "/SS.txt"):
        os.remove(polyfile + "/SS.txt")

    #search health and food library
    existence = False
    lookup = [f.path for f in os.scandir(health_lib) if f.is_file()]
    for item in lookup:
        file = path.basename(item)
        if file.casefold() == request:
            health_library()
            existence = True
    if existence == False:
        lookup = [f.path for f in os.scandir(food_lib) if f.is_file()]
        for item in lookup:
            file = path.basename(item)
            if file.casefold() == request:
                food_library()
                existence = True
        if existence == False:
            no_records_found()


#create search button and entry box
search_field = tkinter.Entry(Nutrition_Library, width=30)
search_field.place(x=15, y=25)

search = tkinter.Button(Nutrition_Library, text="Search", width=8, command=SEARCH)
search['font'] = small_font
search.place(x=215, y=21)

#-----------------------------------------------------------------------------------------------------------
#Exercise Log Operations

#Creating GUI Layout for Exercise_Log

#Date_Canvas Exercise Data Metrics
DateE_Canvas = tkinter.Canvas(Exercise_Data_Metrics, width=340, height=50, background="lightgrey")
DateE_Canvas.place(x=5, y=5)
DateE_Canvas.create_text(29, 26, text="Day:", font=("Comic Sans MS", 10))
DateE_Canvas.create_text(125, 26, text="Month:", font=("Comic Sans MS", 10))
DateE_Canvas.create_text(268, 26, text="Year:", font=("Comic Sans MS", 10))
DateE_Canvas.create_rectangle(3, 3, 340, 50, outline="grey")

Weight_Data = tkinter.Canvas(Exercise_Data_Metrics, width=125, height=50, background="lightblue")
Weight_Data.place(x=350, y=5)
Weight_Data.create_text(28, 25, text="Weight:", font=("Comic Sans MS", 10))
Weight_Data.create_text(112, 24, text="(kg)", font=("Comic Sans MS", 10))

Exercise_List = tkinter.Canvas(Exercise_Data_Metrics, width=470, height=541, background="peachpuff")
Exercise_List.place(x=5, y=60)
Exercise_Background = ImageTk.PhotoImage(Image.open("exercise_list_bg.png"))
Exercise_List.create_image(0, 0, anchor=NW, image=Exercise_Background)
Exercise_List.create_line(345, 0, 345, 541, width=2, fill="grey")
Exercise_List.create_line(0, 45, 470, 45, width=2, fill="grey")
Exercise_List.create_text(172, 22, text="BODYWEIGHT EXERCISE LIST", font=("Comic Sans MS", 10), anchor="center")
Exercise_List.create_text(408, 22, text="            MET\n(Metabolic Equivalent)", font=("Comic Sans MS", 9),
                          anchor="center")
ex_lines = 45
while ex_lines < 311:
    Exercise_List.create_line(0, ex_lines+30, 470, ex_lines+30)
    ex_lines = ex_lines + 30
Exercise_List.create_line(0, 345, 470, 345, width=2, fill="grey")
Exercise_List.create_line(0, 390, 470, 390, width=2, fill="grey")
Exercise_List.create_text(172, 367, text="LIGHT INTENSITY ACTIVITIES", font=("Comic Sans MS", 10),
                          anchor="center")
Exercise_List.create_text(408, 367, text="            MET\n(Metabolic Equivalent)", font=("Comic Sans MS", 9),
                          anchor="center")
Exercise_List.create_rectangle(3, 3, 471, 542, width=2, outline="grey30") #border
Exercise_List.create_line(0, 420, 470, 420)
Exercise_List.create_line(0, 450, 470, 450)
Exercise_List.create_line(0, 480, 470, 480)
Exercise_List.create_line(0, 510, 470, 510)

Exercise_List.create_text(305, 50, text="Ab-Exercises:        min(s)         second(s)", font=("Comic Sans MS", 10), anchor="ne")
Exercise_List.create_text(305, 80, text="Bridges (Butt-Lift):        min(s)         second(s)", font=("Comic Sans MS", 10), anchor="ne")
Exercise_List.create_text(305, 110, text="Burpees:        min(s)         second(s)", font=("Comic Sans MS", 10), anchor="ne")
Exercise_List.create_text(305, 140, text="Crunches:        min(s)         second(s)", font=("Comic Sans MS", 10), anchor="ne")
Exercise_List.create_text(305, 170, text="Jumping Jacks:        min(s)         second(s)", font=("Comic Sans MS", 10), anchor="ne")
Exercise_List.create_text(305, 200, text="Lunges:        min(s)         second(s)", font=("Comic Sans MS", 10), anchor="ne")
Exercise_List.create_text(305, 230, text="Mountain Climbers:        min(s)         second(s)", font=("Comic Sans MS", 10), anchor="ne")
Exercise_List.create_text(305, 260, text="Push Ups:        min(s)         second(s)", font=("Comic Sans MS", 10), anchor="ne")
Exercise_List.create_text(305, 290, text="Sit-Ups:        min(s)         second(s)", font=("Comic Sans MS", 10), anchor="ne")
Exercise_List.create_text(305, 320, text="Squats:        min(s)         second(s)", font=("Comic Sans MS", 10), anchor="ne")
Exercise_List.create_text(305, 395, text="Sleeping:        Hr(s)         Min(s)", font=("Comic Sans MS", 10), anchor="ne")
Exercise_List.create_text(305, 425, text="Watching Television:        Hr(s)         Min(s)", font=("Comic Sans MS", 10), anchor="ne")
Exercise_List.create_text(305, 455, text="Writing, Desk Work:        Hr(s)         Min(s)", font=("Comic Sans MS", 10), anchor="ne")
Exercise_List.create_text(305, 485, text="Walking, Household:        Hr(s)         Min(s)", font=("Comic Sans MS", 10), anchor="ne")
Exercise_List.create_text(305, 515, text="Walking, 3.2km/ph:        Hr(s)         Min(s)", font=("Comic Sans MS", 10), anchor="ne")

#--------------MET Values
Exercise_List.create_text(408, 62, text="7.0", font=("Comic Sans MS", 10), anchor="center")
Exercise_List.create_text(408, 92, text="6.0", font=("Comic Sans MS", 10), anchor="center")
Exercise_List.create_text(408, 122, text="8.0", font=("Comic Sans MS", 10), anchor="center")
Exercise_List.create_text(408, 152, text="5.0", font=("Comic Sans MS", 10), anchor="center")
Exercise_List.create_text(408, 182, text="7.7", font=("Comic Sans MS", 10), anchor="center")
Exercise_List.create_text(408, 212, text="4.0", font=("Comic Sans MS", 10), anchor="center")
Exercise_List.create_text(408, 242, text="8.0", font=("Comic Sans MS", 10), anchor="center")
Exercise_List.create_text(408, 272, text="8.0", font=("Comic Sans MS", 10), anchor="center")
Exercise_List.create_text(408, 302, text="8.0", font=("Comic Sans MS", 10), anchor="center")
Exercise_List.create_text(408, 332, text="8.0", font=("Comic Sans MS", 10), anchor="center")


Exercise_List.create_text(408, 407, text="0.95", font=("Comic Sans MS", 10), anchor="center")
Exercise_List.create_text(408, 437, text="1.0", font=("Comic Sans MS", 10), anchor="center")
Exercise_List.create_text(408, 467, text="1.3", font=("Comic Sans MS", 10), anchor="center")
Exercise_List.create_text(408, 497, text="2.0", font=("Comic Sans MS", 10), anchor="center")
Exercise_List.create_text(408, 527, text="2.8", font=("Comic Sans MS", 10), anchor="center")

Exercise_Graph = tkinter.Canvas(Exercise_Data_Metrics, width=775, height=590,
                                background="grey", bd=3, relief="sunken")
Exercise_Graph.place(x=480, y=5)


def Draw_Exercise_Graph():
    # clear canvas to intialize
    Exercise_Graph.delete("all")

    #Build Axis
    Exercise_Graph.create_line(50, 540, 50, 25, width=2) #y_axis
    Exercise_Graph.create_line(50, 540, 725, 540, width=2) #x_axis

    #Y_axis
    top = 540
    numbering = 0
    while top > 50:
        Exercise_Graph.create_line(50, (top-25),40, (top-25), width=2, fill="lime")
        numbering = numbering + 150
        Exercise_Graph.create_text(25, (top-25), text=str(numbering))
        top = top - 25

    #X_axis
    if path.exists(polyfile + "/date_info.txt"):
        read_date_info = open(polyfile + "/date_info.txt", "r", encoding='utf8')
        info = read_date_info.read().splitlines()
        read_date_info.close()
        day_num = int(info[0])
        month = info[2]
        spacing = (675 / day_num)
        space = spacing
        incre = 0
        while incre != day_num:
            incre = incre + 1
            Exercise_Graph.create_line((50+spacing), 540, (50+spacing), 550, width=2, fill="lime")
            Exercise_Graph.create_text((50 + spacing), 560, text=str(incre))
            spacing = spacing + space

    #calculate MET data
    if path.exists(polyfile + "/date_info.txt"):
        read_date_info = open(polyfile + "/date_info.txt", "r", encoding='utf8')
        info = read_date_info.read().splitlines()
        read_date_info.close()
        day_num = int(info[0])
        month = info[2]
        year = info[3]
        start = 1
        spacing = (675 / day_num)
        while start != (day_num+1):
            x_val = 50 + (start * spacing)
            if path.exists(polyfile + "/" + str(start) + month + year + "/exercise_data.txt"):
                #read data
                ex_data = open(polyfile + "/" + str(start) + month + year + "/exercise_data.txt", "r", encoding="utf8")
                data_get = ex_data.read().splitlines()
                ex_data.close()
                Cal_Burnt = 0

                #get weight value
                if path.exists(polyfile + "/" + str(start) + month + year + "/ex_weight.txt"):
                    read_weight = open(polyfile + "/" + str(start) + month + year + "/ex_weight.txt", "r", encoding="utf8")
                    weight_data = read_weight.read()
                    read_weight.close()
                    Weight = float(weight_data)
                else:
                    if path.exists(polyfile + "/" + str(start) + month + year + "/Weight and Height.txt"):
                        read_weight = open(polyfile + "/" + str(start) + month + year + "/Weight and Height.txt", "r", encoding="utf8")
                        weight_data = read_weight.read()
                        read_weight.close()
                        split_weight = weight_data.split(":")
                        get_weight = split_weight[0]
                        Weight = float(get_weight)
                    else:
                        Weight = Weight_Box.get()

                #calculate calories burnt - MET's
                Exercises = data_get[0]
                split = Exercises.split(":")
                Time_Min = int(split[0])
                Time_Sec = int(split[1])
                MET_calc = (7 * 3.5 * float(Weight))/200
                Cal_Burnt = Cal_Burnt + ((Time_Min + (Time_Sec/60)) * MET_calc)

                Exercises = data_get[1]
                split = Exercises.split(":")
                Time_Min = int(split[0])
                Time_Sec = int(split[1])
                MET_calc = (6 * 3.5 * float(Weight)) / 200
                Cal_Burnt = Cal_Burnt + ((Time_Min + (Time_Sec / 60)) * MET_calc)

                Exercises = data_get[2]
                split = Exercises.split(":")
                Time_Min = int(split[0])
                Time_Sec = int(split[1])
                MET_calc = (8 * 3.5 * float(Weight)) / 200
                Cal_Burnt = Cal_Burnt + ((Time_Min + (Time_Sec / 60)) * MET_calc)

                Exercises = data_get[3]
                split = Exercises.split(":")
                Time_Min = int(split[0])
                Time_Sec = int(split[1])
                MET_calc = (5 * 3.5 * float(Weight)) / 200
                Cal_Burnt = Cal_Burnt + ((Time_Min + (Time_Sec / 60)) * MET_calc)

                Exercises = data_get[4]
                split = Exercises.split(":")
                Time_Min = int(split[0])
                Time_Sec = int(split[1])
                MET_calc = (7.7 * 3.5 * float(Weight)) / 200
                Cal_Burnt = Cal_Burnt + ((Time_Min + (Time_Sec / 60)) * MET_calc)

                Exercises = data_get[5]
                split = Exercises.split(":")
                Time_Min = int(split[0])
                Time_Sec = int(split[1])
                MET_calc = (4 * 3.5 * float(Weight)) / 200
                Cal_Burnt = Cal_Burnt + ((Time_Min + (Time_Sec / 60)) * MET_calc)

                Exercises = data_get[6]
                split = Exercises.split(":")
                Time_Min = int(split[0])
                Time_Sec = int(split[1])
                MET_calc = (8 * 3.5 * float(Weight)) / 200
                Cal_Burnt = Cal_Burnt + ((Time_Min + (Time_Sec / 60)) * MET_calc)

                Exercises = data_get[7]
                split = Exercises.split(":")
                Time_Min = int(split[0])
                Time_Sec = int(split[1])
                MET_calc = (8 * 3.5 * float(Weight)) / 200
                Cal_Burnt = Cal_Burnt + ((Time_Min + (Time_Sec / 60)) * MET_calc)

                Exercises = data_get[8]
                split = Exercises.split(":")
                Time_Min = int(split[0])
                Time_Sec = int(split[1])
                MET_calc = (8 * 3.5 * float(Weight)) / 200
                Cal_Burnt = Cal_Burnt + ((Time_Min + (Time_Sec / 60)) * MET_calc)

                Exercises = data_get[9]
                split = Exercises.split(":")
                Time_Min = int(split[0])
                Time_Sec = int(split[1])
                MET_calc = (8 * 3.5 * float(Weight)) / 200
                Cal_Burnt = Cal_Burnt + ((Time_Min + (Time_Sec / 60)) * MET_calc)

                Exer_Cal = Cal_Burnt #store exercise calories

                Exercises = data_get[10]
                split = Exercises.split(":")
                Time_Hr = int(split[0])
                Time_Min = int(split[1])
                MET_calc = (0.95 * 3.5 * float(Weight)) / 200
                Cal_Burnt = Cal_Burnt + (((Time_Hr*60) + Time_Min) * MET_calc)

                Exercises = data_get[11]
                split = Exercises.split(":")
                Time_Hr = int(split[0])
                Time_Min = int(split[1])
                MET_calc = (1 * 3.5 * float(Weight)) / 200
                Cal_Burnt = Cal_Burnt + (((Time_Hr * 60) + Time_Min) * MET_calc)

                Exercises = data_get[12]
                split = Exercises.split(":")
                Time_Hr = int(split[0])
                Time_Min = int(split[1])
                MET_calc = (1.3 * 3.5 * float(Weight)) / 200
                Cal_Burnt = Cal_Burnt + (((Time_Hr * 60) + Time_Min) * MET_calc)

                Exercises = data_get[13]
                split = Exercises.split(":")
                Time_Hr = int(split[0])
                Time_Min = int(split[1])
                MET_calc = (2.0 * 3.5 * float(Weight)) / 200
                Cal_Burnt = Cal_Burnt + (((Time_Hr * 60) + Time_Min) * MET_calc)

                Exercises = data_get[14]
                split = Exercises.split(":")
                Time_Hr = int(split[0])
                Time_Min = int(split[1])
                MET_calc = (2.8 * 3.5 * float(Weight)) / 200
                Cal_Burnt = Cal_Burnt + (((Time_Hr * 60) + Time_Min) * MET_calc)
                y_val = 540 - ((Cal_Burnt/3000) * 500)
                exer_y = Cal_Burnt - Exer_Cal
                z_val = 540 - ((exer_y/3000) * 500)

                Exercise_Graph.create_rectangle(x_val-5, 539, x_val+5, y_val, fill="cyan")
                Exercise_Graph.create_rectangle(x_val+5, y_val, x_val-5, z_val, fill="lime")
                Exercise_Graph.create_line(50, y_val, x_val, y_val, fill="yellow", dash=(3,1))
                Cal_Burnt = int(Cal_Burnt)
                Exer_Cal = int(Exer_Cal)
                Exercise_Graph.create_text(x_val, y_val-20, text=(str(Cal_Burnt) + "cal"), fill="white")
                Exercise_Graph.create_text(x_val, y_val-10, text=(str(Exer_Cal) + "cal"), fill="lime")

            start = start + 1

def update_exercise_boxes():
    # date info
    day_fetch = str(DayE.get())
    month_fetch = str(MonthE.get())
    year_fetch = str(YearE.get())
    polyfile_dir = "/" + day_fetch + month_fetch + year_fetch

    if path.exists(polyfile + polyfile_dir + "/exercise_data.txt"):
        get_data = open(polyfile + polyfile_dir + "/exercise_data.txt", "r", encoding="utf8")
        pull = get_data.read().splitlines()
        get_data.close()

        #Ab Exercises Insert
        Units = pull[0]
        Use = Units.split(":")

        Ab_Exercises_Min.config(state="normal")
        Ab_Exercises_Min.delete(0, "end")
        Ab_Exercises_Min.insert(0, Use[0])
        Ab_Exercises_Min.config(state="readonly")

        Ab_Exercises_Sec.config(state="normal")
        Ab_Exercises_Sec.delete(0, "end")
        Ab_Exercises_Sec.insert(0, Use[1])
        Ab_Exercises_Sec.config(state="readonly")

        #Bridges Insert
        Units = pull[1]
        Use = Units.split(":")

        Bridges_Min.config(state="normal")
        Bridges_Min.delete(0, "end")
        Bridges_Min.insert(0, Use[0])
        Bridges_Min.config(state="readonly")

        Bridges_Sec.config(state="normal")
        Bridges_Sec.delete(0, "end")
        Bridges_Sec.insert(0, Use[1])
        Bridges_Sec.config(state="readonly")

        # Burpees Insert
        Units = pull[2]
        Use = Units.split(":")

        Burpees_Min.config(state="normal")
        Burpees_Min.delete(0, "end")
        Burpees_Min.insert(0, Use[0])
        Burpees_Min.config(state="readonly")

        Burpees_Sec.config(state="normal")
        Burpees_Sec.delete(0, "end")
        Burpees_Sec.insert(0, Use[1])
        Burpees_Sec.config(state="readonly")

        # Crunches Insert
        Units = pull[3]
        Use = Units.split(":")

        Crunches_Min.config(state="normal")
        Crunches_Min.delete(0, "end")
        Crunches_Min.insert(0, Use[0])
        Crunches_Min.config(state="readonly")

        Crunches_Sec.config(state="normal")
        Crunches_Sec.delete(0, "end")
        Crunches_Sec.insert(0, Use[1])
        Crunches_Sec.config(state="readonly")

        # Jumping Jacks Insert
        Units = pull[4]
        Use = Units.split(":")

        Jumping_Jacks_Min.config(state="normal")
        Jumping_Jacks_Min.delete(0, "end")
        Jumping_Jacks_Min.insert(0, Use[0])
        Jumping_Jacks_Min.config(state="readonly")

        Jumping_Jacks_Sec.config(state="normal")
        Jumping_Jacks_Sec.delete(0, "end")
        Jumping_Jacks_Sec.insert(0, Use[1])
        Jumping_Jacks_Sec.config(state="readonly")

        # Lunges Insert
        Units = pull[5]
        Use = Units.split(":")

        Lunges_Min.config(state="normal")
        Lunges_Min.delete(0, "end")
        Lunges_Min.insert(0, Use[0])
        Lunges_Min.config(state="readonly")

        Lunges_Sec.config(state="normal")
        Lunges_Sec.delete(0, "end")
        Lunges_Sec.insert(0, Use[1])
        Lunges_Sec.config(state="readonly")

        # Mountain Climbers Insert
        Units = pull[6]
        Use = Units.split(":")

        Mountain_Climbers_Min.config(state="normal")
        Mountain_Climbers_Min.delete(0, "end")
        Mountain_Climbers_Min.insert(0, Use[0])
        Mountain_Climbers_Min.config(state="readonly")

        Mountain_Climbers_Sec.config(state="normal")
        Mountain_Climbers_Sec.delete(0, "end")
        Mountain_Climbers_Sec.insert(0, Use[1])
        Mountain_Climbers_Sec.config(state="readonly")

        # Push Ups Insert
        Units = pull[7]
        Use = Units.split(":")

        Push_Ups_Min.config(state="normal")
        Push_Ups_Min.delete(0, "end")
        Push_Ups_Min.insert(0, Use[0])
        Push_Ups_Min.config(state="readonly")

        Push_Ups_Sec.config(state="normal")
        Push_Ups_Sec.delete(0, "end")
        Push_Ups_Sec.insert(0, Use[1])
        Push_Ups_Sec.config(state="readonly")

        # Sit Ups Insert
        Units = pull[8]
        Use = Units.split(":")

        Sit_Ups_Min.config(state="normal")
        Sit_Ups_Min.delete(0, "end")
        Sit_Ups_Min.insert(0, Use[0])
        Sit_Ups_Min.config(state="readonly")

        Sit_Ups_Sec.config(state="normal")
        Sit_Ups_Sec.delete(0, "end")
        Sit_Ups_Sec.insert(0, Use[1])
        Sit_Ups_Sec.config(state="readonly")

        # Squats Ups Insert
        Units = pull[9]
        Use = Units.split(":")

        Squats_Min.config(state="normal")
        Squats_Min.delete(0, "end")
        Squats_Min.insert(0, Use[0])
        Sit_Ups_Min.config(state="readonly")

        Squats_Sec.config(state="normal")
        Squats_Sec.delete(0, "end")
        Squats_Sec.insert(0, Use[1])
        Squats_Sec.config(state="readonly")

        # Sleeping Insert
        Units = pull[10]
        Use = Units.split(":")

        Sleeping_Hr.config(state="normal")
        Sleeping_Hr.delete(0, "end")
        Sleeping_Hr.insert(0, Use[0])
        Sleeping_Hr.config(state="readonly")

        Sleeping_Min.config(state="normal")
        Sleeping_Min.delete(0, "end")
        Sleeping_Min.insert(0, Use[1])
        Sleeping_Min.config(state="readonly")

        # Watching Television Insert
        Units = pull[11]
        Use = Units.split(":")

        Watching_Television_Hr.config(state="normal")
        Watching_Television_Hr.delete(0, "end")
        Watching_Television_Hr.insert(0, Use[0])
        Watching_Television_Hr.config(state="readonly")

        Watching_Television_Min.config(state="normal")
        Watching_Television_Min.delete(0, "end")
        Watching_Television_Min.insert(0, Use[1])
        Watching_Television_Min.config(state="readonly")

        # Writing Deskwork Insert
        Units = pull[12]
        Use = Units.split(":")

        Writing_DeskWork_Hr.config(state="normal")
        Writing_DeskWork_Hr.delete(0, "end")
        Writing_DeskWork_Hr.insert(0, Use[0])
        Writing_DeskWork_Hr.config(state="readonly")

        Writing_DeskWork_Min.config(state="normal")
        Writing_DeskWork_Min.delete(0, "end")
        Writing_DeskWork_Min.insert(0, Use[1])
        Writing_DeskWork_Min.config(state="readonly")

        # Walking Household Insert
        Units = pull[13]
        Use = Units.split(":")

        Walking_Household_Hr.config(state="normal")
        Walking_Household_Hr.delete(0, "end")
        Walking_Household_Hr.insert(0, Use[0])
        Walking_Household_Hr.config(state="readonly")

        Walking_Household_Min.config(state="normal")
        Walking_Household_Min.delete(0, "end")
        Walking_Household_Min.insert(0, Use[1])
        Walking_Household_Min.config(state="readonly")

        # Walking Reg Insert
        Units = pull[14]
        Use = Units.split(":")

        Walking_Reg_Hr.config(state="normal")
        Walking_Reg_Hr.delete(0, "end")
        Walking_Reg_Hr.insert(0, Use[0])
        Walking_Reg_Hr.config(state="readonly")

        Walking_Reg_Min.config(state="normal")
        Walking_Reg_Min.delete(0, "end")
        Walking_Reg_Min.insert(0, Use[1])
        Walking_Reg_Min.config(state="readonly")
    else:
        Use = [0, 0]
        # Ab Exercises Insert
        Ab_Exercises_Min.config(state="normal")
        Ab_Exercises_Min.delete(0, "end")
        Ab_Exercises_Min.insert(0, Use[0])
        Ab_Exercises_Min.config(state="readonly")

        Ab_Exercises_Sec.config(state="normal")
        Ab_Exercises_Sec.delete(0, "end")
        Ab_Exercises_Sec.insert(0, Use[1])
        Ab_Exercises_Sec.config(state="readonly")

        # Bridges Insert
        Bridges_Min.config(state="normal")
        Bridges_Min.delete(0, "end")
        Bridges_Min.insert(0, Use[0])
        Bridges_Min.config(state="readonly")

        Bridges_Sec.config(state="normal")
        Bridges_Sec.delete(0, "end")
        Bridges_Sec.insert(0, Use[1])
        Bridges_Sec.config(state="readonly")

        # Burpees Insert
        Burpees_Min.config(state="normal")
        Burpees_Min.delete(0, "end")
        Burpees_Min.insert(0, Use[0])
        Burpees_Min.config(state="readonly")

        Burpees_Sec.config(state="normal")
        Burpees_Sec.delete(0, "end")
        Burpees_Sec.insert(0, Use[1])
        Burpees_Sec.config(state="readonly")

        # Crunches Insert
        Crunches_Min.config(state="normal")
        Crunches_Min.delete(0, "end")
        Crunches_Min.insert(0, Use[0])
        Crunches_Min.config(state="readonly")

        Crunches_Sec.config(state="normal")
        Crunches_Sec.delete(0, "end")
        Crunches_Sec.insert(0, Use[1])
        Crunches_Sec.config(state="readonly")

        # Jumping Jacks Insert
        Jumping_Jacks_Min.config(state="normal")
        Jumping_Jacks_Min.delete(0, "end")
        Jumping_Jacks_Min.insert(0, Use[0])
        Jumping_Jacks_Min.config(state="readonly")

        Jumping_Jacks_Sec.config(state="normal")
        Jumping_Jacks_Sec.delete(0, "end")
        Jumping_Jacks_Sec.insert(0, Use[1])
        Jumping_Jacks_Sec.config(state="readonly")

        # Lunges Insert
        Lunges_Min.config(state="normal")
        Lunges_Min.delete(0, "end")
        Lunges_Min.insert(0, Use[0])
        Lunges_Min.config(state="readonly")

        Lunges_Sec.config(state="normal")
        Lunges_Sec.delete(0, "end")
        Lunges_Sec.insert(0, Use[1])
        Lunges_Sec.config(state="readonly")

        # Mountain Climbers Insert
        Mountain_Climbers_Min.config(state="normal")
        Mountain_Climbers_Min.delete(0, "end")
        Mountain_Climbers_Min.insert(0, Use[0])
        Mountain_Climbers_Min.config(state="readonly")

        Mountain_Climbers_Sec.config(state="normal")
        Mountain_Climbers_Sec.delete(0, "end")
        Mountain_Climbers_Sec.insert(0, Use[1])
        Mountain_Climbers_Sec.config(state="readonly")

        # Push Ups Insert
        Push_Ups_Min.config(state="normal")
        Push_Ups_Min.delete(0, "end")
        Push_Ups_Min.insert(0, Use[0])
        Push_Ups_Min.config(state="readonly")

        Push_Ups_Sec.config(state="normal")
        Push_Ups_Sec.delete(0, "end")
        Push_Ups_Sec.insert(0, Use[1])
        Push_Ups_Sec.config(state="readonly")

        # Sit Ups Insert
        Sit_Ups_Min.config(state="normal")
        Sit_Ups_Min.delete(0, "end")
        Sit_Ups_Min.insert(0, Use[0])
        Sit_Ups_Min.config(state="readonly")

        Sit_Ups_Sec.config(state="normal")
        Sit_Ups_Sec.delete(0, "end")
        Sit_Ups_Sec.insert(0, Use[1])
        Sit_Ups_Sec.config(state="readonly")

        # Squats Ups Insert
        Squats_Min.config(state="normal")
        Squats_Min.delete(0, "end")
        Squats_Min.insert(0, Use[0])
        Sit_Ups_Min.config(state="readonly")

        Squats_Sec.config(state="normal")
        Squats_Sec.delete(0, "end")
        Squats_Sec.insert(0, Use[1])
        Squats_Sec.config(state="readonly")

        # Sleeping Insert
        Sleeping_Hr.config(state="normal")
        Sleeping_Hr.delete(0, "end")
        Sleeping_Hr.insert(0, Use[0])
        Sleeping_Hr.config(state="readonly")

        Sleeping_Min.config(state="normal")
        Sleeping_Min.delete(0, "end")
        Sleeping_Min.insert(0, Use[1])
        Sleeping_Min.config(state="readonly")

        # Watching Television Insert
        Watching_Television_Hr.config(state="normal")
        Watching_Television_Hr.delete(0, "end")
        Watching_Television_Hr.insert(0, Use[0])
        Watching_Television_Hr.config(state="readonly")

        Watching_Television_Min.config(state="normal")
        Watching_Television_Min.delete(0, "end")
        Watching_Television_Min.insert(0, Use[1])
        Watching_Television_Min.config(state="readonly")

        # Writing Deskwork Insert
        Writing_DeskWork_Hr.config(state="normal")
        Writing_DeskWork_Hr.delete(0, "end")
        Writing_DeskWork_Hr.insert(0, Use[0])
        Writing_DeskWork_Hr.config(state="readonly")

        Writing_DeskWork_Min.config(state="normal")
        Writing_DeskWork_Min.delete(0, "end")
        Writing_DeskWork_Min.insert(0, Use[1])
        Writing_DeskWork_Min.config(state="readonly")

        # Walking Household Insert
        Walking_Household_Hr.config(state="normal")
        Walking_Household_Hr.delete(0, "end")
        Walking_Household_Hr.insert(0, Use[0])
        Walking_Household_Hr.config(state="readonly")

        Walking_Household_Min.config(state="normal")
        Walking_Household_Min.delete(0, "end")
        Walking_Household_Min.insert(0, Use[1])
        Walking_Household_Min.config(state="readonly")

        # Walking Reg Insert
        Walking_Reg_Hr.config(state="normal")
        Walking_Reg_Hr.delete(0, "end")
        Walking_Reg_Hr.insert(0, Use[0])
        Walking_Reg_Hr.config(state="readonly")

        Walking_Reg_Min.config(state="normal")
        Walking_Reg_Min.delete(0, "end")
        Walking_Reg_Min.insert(0, Use[1])
        Walking_Reg_Min.config(state="readonly")


def store_exercise_info():
    #date info
    day_fetch = str(DayE.get())
    month_fetch = str(MonthE.get())
    year_fetch = str(YearE.get())
    polyfile_dir = "/" + day_fetch + month_fetch + year_fetch


    #gather exercise info
    Ab_Exercises_Data_One = Ab_Exercises_Min.get()
    Ab_Exercises_Data_Two = Ab_Exercises_Sec.get()
    Bridges_Data_One = Bridges_Min.get()
    Bridges_Data_Two = Bridges_Sec.get()
    Burpees_Data_One = Burpees_Min.get()
    Burpees_Data_Two = Burpees_Sec.get()
    Crunches_Data_One = Crunches_Min.get()
    Crunches_Data_Two = Crunches_Sec.get()
    Jumping_Jacks_Data_One = Jumping_Jacks_Min.get()
    Jumping_Jacks_Data_Two = Jumping_Jacks_Sec.get()
    Lunges_Data_One = Lunges_Min.get()
    Lunges_Data_Two = Lunges_Sec.get()
    Mountain_Climbers_Data_One = Mountain_Climbers_Min.get()
    Mountain_Climbers_Data_Two = Mountain_Climbers_Sec.get()
    Push_Ups_Data_One = Push_Ups_Min.get()
    Push_Ups_Data_Two = Push_Ups_Sec.get()
    Sit_Ups_Data_One = Sit_Ups_Min.get()
    Sit_Ups_Data_Two = Sit_Ups_Sec.get()
    Squats_Data_One = Squats_Min.get()
    Squats_Data_Two = Squats_Sec.get()
    Sleeping_Data_One = Sleeping_Hr.get()
    Sleeping_Data_Two = Sleeping_Min.get()
    Watching_Television_Data_One = Watching_Television_Hr.get()
    Watching_Television_Data_Two = Watching_Television_Min.get()
    Writing_Deskwork_Data_One = Writing_DeskWork_Hr.get()
    Writing_Deskwork_Data_Two = Writing_DeskWork_Min.get()
    Walking_Household_Data_One = Walking_Household_Hr.get()
    Walking_Household_Data_Two = Walking_Household_Min.get()
    Walking_Reg_Data_One = Walking_Reg_Hr.get()
    Walking_Reg_Data_Two = Walking_Reg_Min.get()

    null_check = (Ab_Exercises_Data_One + Ab_Exercises_Data_Two + Bridges_Data_One + Bridges_Data_Two
                  + Burpees_Data_One + Burpees_Data_Two + Crunches_Data_One + Crunches_Data_Two +
                  Jumping_Jacks_Data_One + Jumping_Jacks_Data_Two + Lunges_Data_One + Lunges_Data_Two +
                  Mountain_Climbers_Data_One + Mountain_Climbers_Data_Two + Push_Ups_Data_One +
                  Push_Ups_Data_Two + Sit_Ups_Data_One + Sit_Ups_Data_Two + Squats_Data_One + Squats_Data_Two
                  + Sleeping_Data_One + Sleeping_Data_Two + Watching_Television_Data_One +
                  Watching_Television_Data_Two + Writing_Deskwork_Data_One + Writing_Deskwork_Data_Two +
                  Walking_Household_Data_One + Walking_Household_Data_Two + Walking_Reg_Data_One +
                  Walking_Reg_Data_Two)

    if null_check != "000000000000000000000000000000":
        #store data
        ex_store = open(polyfile + polyfile_dir + "/exercise_data.txt", "w", encoding="utf8")
        ex_store.write(Ab_Exercises_Data_One + ":" + Ab_Exercises_Data_Two + "\n")
        ex_store.write(Bridges_Data_One + ":" + Bridges_Data_Two + "\n")
        ex_store.write(Burpees_Data_One + ":" + Burpees_Data_Two + "\n")
        ex_store.write(Crunches_Data_One + ":" + Crunches_Data_Two + "\n")
        ex_store.write(Jumping_Jacks_Data_One + ":" + Jumping_Jacks_Data_Two + "\n")
        ex_store.write(Lunges_Data_One + ":" + Lunges_Data_Two + "\n")
        ex_store.write(Mountain_Climbers_Data_One + ":" + Mountain_Climbers_Data_Two + "\n")
        ex_store.write(Push_Ups_Data_One + ":" + Push_Ups_Data_Two + "\n")
        ex_store.write(Sit_Ups_Data_One + ":" + Sit_Ups_Data_Two + "\n")
        ex_store.write(Squats_Data_One + ":" + Squats_Data_Two + "\n")
        ex_store.write(Sleeping_Data_One + ":" + Sleeping_Data_Two + "\n")
        ex_store.write(Watching_Television_Data_One + ":" + Watching_Television_Data_Two + "\n")
        ex_store.write(Writing_Deskwork_Data_One + ":" + Writing_Deskwork_Data_Two + "\n")
        ex_store.write(Walking_Household_Data_One + ":" + Walking_Household_Data_Two + "\n")
        ex_store.write(Walking_Reg_Data_One + ":" + Walking_Reg_Data_Two + "\n")
        ex_store.close()

    #call draw graph
    Draw_Exercise_Graph()

#create polyfile record for Exercise Log
def polyfile_recordE():
    #fetch date info
    dummy = 0
    day_fetch = str(DayE.get())
    month_fetch = str(MonthE.get())
    year_fetch = str(YearE.get())
    polyfile_dir = "/" + day_fetch + month_fetch + year_fetch
    if path.exists(polyfile + polyfile_dir):
        dummy = dummy + 1
    else:
        os.makedirs(polyfile + polyfile_dir)
    #Configure Day Range (for each month and leap year)
    month_pull = MonthE.get()
    year_pull = YearE.get()
    leap = True
    leap_check = str((int(year_pull))/4)
    split_leap = leap_check.split(".")
    if int(split_leap[1]) > 0:
        leap = False
    if (month_pull == "September") or (month_pull == "April") or (month_pull == "June") or (month_pull == "November"):
        Day.config(from_=1, to=30)
        day_count = 30
    elif (month_pull == "February") and (leap == True):
        Day.config(from_=1, to=29)
        day_count = 29
    elif month_pull == "February":
        Day.config(from_=1, to=28)
        day_count = 28
    else:
        Day.config(from_=1, to=31)
        day_count = 31

    #store date data to file
    store_date_info = open(polyfile + "/date_info.txt", "w", encoding='utf8')
    store_date_info.write(str(day_count) + "\n" + day_fetch + "\n" + month_pull + "\n" + year_pull)
    store_date_info.close()

    #update weight
    weight_fetch()

    #update exercise boxes
    update_exercise_boxes()

    #Draw Graph
    Draw_Exercise_Graph()

#Diet Data Metrics Date Setup
DayE = tkinter.Spinbox(Exercise_Data_Metrics, width=3, from_=1, to=31, state="normal", command=polyfile_recordE)
DayE.place(x=50, y=22)
DayE.delete(0, "end")
DayE.insert(0, day_get)
DayE.config(state="readonly")

MonthE = tkinter.Spinbox(Exercise_Data_Metrics, width=10, values=("January", "February", "March", "April", "May", "June", "July", "August", "September", "October",
             "November", "December"), state="normal", command=polyfile_recordE)
MonthE.place(x=154, y=22)
MonthE_List = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October",
             "November", "December"]
MonthE.delete(0, "end")
MonthE.insert(0, Month_List[month_get-1])
MonthE.config(state="readonly")

YearE = tkinter.Spinbox(Exercise_Data_Metrics, width=4, from_=2020, to=2100, state="normal", command=polyfile_recordE)
YearE.place(x=293, y=22)
YearE.delete(0, "end")
YearE.insert(0, year_get)
YearE.config(state="readonly")

#Weight Operations
def weight_fetch():
    # date info
    day_fetch = str(DayE.get())
    month_fetch = str(MonthE.get())
    year_fetch = str(YearE.get())
    polyfile_dir = "/" + day_fetch + month_fetch + year_fetch

    # insert weight information if it exists
    if path.exists(polyfile + polyfile_dir + "/ex_weight.txt"):
        read_weight = open(polyfile + polyfile_dir + "/ex_weight.txt", "r", encoding="utf8")
        weight_data = read_weight.read()
        read_weight.close()
        Weight_Box.config(state="normal")
        Weight_Box.delete(0, "end")
        Weight_Box.insert(0, weight_data)
        Weight_Box.config(state="readonly")
    else:
        if path.exists(polyfile + polyfile_dir + "/Weight and Height.txt"):
            read_weight = open(polyfile + polyfile_dir + "/Weight and Height.txt", "r", encoding="utf8")
            weight_data = read_weight.read()
            read_weight.close()
            split_data = weight_data.split(":")
            weight = split_data[0]
            Weight_Box.config(state="normal")
            Weight_Box.delete(0, "end")
            Weight_Box.insert(0, weight)
            Weight_Box.config(state="readonly")
        else:
            Weight_Box.config(state="normal")
            Weight_Box.delete(0, "end")
            Weight_Box.insert(0, "100.0")
            Weight_Box.config(state="readonly")

    #Draw Exercise Graph
    Draw_Exercise_Graph()

def weight_box_command():
    weight = Weight_Box.get()

    # store weight
    day_fetch = str(DayE.get())
    month_fetch = str(MonthE.get())
    year_fetch = str(YearE.get())
    polyfile_dir = "/" + day_fetch + month_fetch + year_fetch
    store = open(polyfile + polyfile_dir + "/ex_weight.txt", "w", encoding="utf8")
    store.write(weight)
    store.close()

    weight_fetch()

Weight_Box = tkinter.Spinbox(Exercise_Data_Metrics, width=5, from_=0, to=200, state="normal", increment=0.1,
                             command=weight_box_command)
Weight_Box.place(x=403, y=20)
Weight_Box.delete(0, "end")
Weight_Box.insert(0, "100.0")
Weight_Box.config(state="readonly")

#Exercise_List - Spinboxes
Ab_Exercises_Min = tkinter.Spinbox(Exercise_Data_Metrics, width=2, from_=0, to=100, state="readonly", increment=1,
                                   command=store_exercise_info)
Ab_Exercises_Min.place(x=151, y=110)
Ab_Exercises_Sec = tkinter.Spinbox(Exercise_Data_Metrics, width=2, from_=0, to=59, state="readonly", increment=1,
                                   command=store_exercise_info)
Ab_Exercises_Sec.place(x=223, y=110)

Bridges_Min = tkinter.Spinbox(Exercise_Data_Metrics, width=2, from_=0, to=100, state="readonly", increment=1,
                              command=store_exercise_info)
Bridges_Min.place(x=151, y=140)
Bridges_Sec = tkinter.Spinbox(Exercise_Data_Metrics, width=2, from_=0, to=59, state="readonly", increment=1,
                              command=store_exercise_info)
Bridges_Sec.place(x=223, y=140)

Burpees_Min = tkinter.Spinbox(Exercise_Data_Metrics, width=2, from_=0, to=100, state="readonly", increment=1,
                              command=store_exercise_info)
Burpees_Min.place(x=151, y=170)
Burpees_Sec = tkinter.Spinbox(Exercise_Data_Metrics, width=2, from_=0, to=59, state="readonly", increment=1,
                              command=store_exercise_info)
Burpees_Sec.place(x=223, y=170)

Crunches_Min = tkinter.Spinbox(Exercise_Data_Metrics, width=2, from_=0, to=100, state="readonly", increment=1,
                               command=store_exercise_info)
Crunches_Min.place(x=151, y=200)
Crunches_Sec = tkinter.Spinbox(Exercise_Data_Metrics, width=2, from_=0, to=59, state="readonly", increment=1,
                               command=store_exercise_info)
Crunches_Sec.place(x=223, y=200)

Jumping_Jacks_Min = tkinter.Spinbox(Exercise_Data_Metrics, width=2, from_=0, to=100, state="readonly", increment=1,
                                    command=store_exercise_info)
Jumping_Jacks_Min.place(x=151, y=230)
Jumping_Jacks_Sec = tkinter.Spinbox(Exercise_Data_Metrics, width=2, from_=0, to=59, state="readonly", increment=1,
                                    command=store_exercise_info)
Jumping_Jacks_Sec.place(x=223, y=230)

Lunges_Min = tkinter.Spinbox(Exercise_Data_Metrics, width=2, from_=0, to=100, state="readonly", increment=1,
                             command=store_exercise_info)
Lunges_Min.place(x=151, y=260)
Lunges_Sec = tkinter.Spinbox(Exercise_Data_Metrics, width=2, from_=0, to=59, state="readonly", increment=1,
                             command=store_exercise_info)
Lunges_Sec.place(x=223, y=260)

Mountain_Climbers_Min = tkinter.Spinbox(Exercise_Data_Metrics, width=2, from_=0, to=100, state="readonly", increment=1,
                                        command=store_exercise_info)
Mountain_Climbers_Min.place(x=151, y=290)
Mountain_Climbers_Sec = tkinter.Spinbox(Exercise_Data_Metrics, width=2, from_=0, to=59, state="readonly", increment=1,
                                        command=store_exercise_info)
Mountain_Climbers_Sec.place(x=223, y=290)

Push_Ups_Min = tkinter.Spinbox(Exercise_Data_Metrics, width=2, from_=0, to=100, state="readonly", increment=1,
                               command=store_exercise_info)
Push_Ups_Min.place(x=151, y=320)
Push_Ups_Sec = tkinter.Spinbox(Exercise_Data_Metrics, width=2, from_=0, to=59, state="readonly", increment=1,
                               command=store_exercise_info)
Push_Ups_Sec.place(x=223, y=320)

Sit_Ups_Min = tkinter.Spinbox(Exercise_Data_Metrics, width=2, from_=0, to=100, state="readonly", increment=1,
                              command=store_exercise_info)
Sit_Ups_Min.place(x=151, y=350)
Sit_Ups_Sec = tkinter.Spinbox(Exercise_Data_Metrics, width=2, from_=0, to=59, state="readonly", increment=1,
                              command=store_exercise_info)
Sit_Ups_Sec.place(x=223, y=350)

Squats_Min = tkinter.Spinbox(Exercise_Data_Metrics, width=2, from_=0, to=100, state="readonly", increment=1,
                             command=store_exercise_info)
Squats_Min.place(x=151, y=380)
Squats_Sec = tkinter.Spinbox(Exercise_Data_Metrics, width=2, from_=0, to=59, state="readonly", increment=1,
                             command=store_exercise_info)
Squats_Sec.place(x=223, y=380)

Sleeping_Hr = tkinter.Spinbox(Exercise_Data_Metrics, width=2, from_=0, to=100, state="readonly", increment=1,
                              command=store_exercise_info)
Sleeping_Hr.place(x=175, y=455)
Sleeping_Min = tkinter.Spinbox(Exercise_Data_Metrics, width=2, from_=0, to=59, state="readonly", increment=1,
                               command=store_exercise_info)
Sleeping_Min.place(x=243, y=455)

Watching_Television_Hr = tkinter.Spinbox(Exercise_Data_Metrics, width=2, from_=0, to=100, state="readonly", increment=1,
                                         command=store_exercise_info)
Watching_Television_Hr.place(x=175, y=485)
Watching_Television_Min = tkinter.Spinbox(Exercise_Data_Metrics, width=2, from_=0, to=59, state="readonly", increment=1,
                                          command=store_exercise_info)
Watching_Television_Min.place(x=243, y=485)

Writing_DeskWork_Hr = tkinter.Spinbox(Exercise_Data_Metrics, width=2, from_=0, to=100, state="readonly", increment=1,
                                      command=store_exercise_info)
Writing_DeskWork_Hr.place(x=175, y=515)
Writing_DeskWork_Min = tkinter.Spinbox(Exercise_Data_Metrics, width=2, from_=0, to=59, state="readonly", increment=1,
                                       command=store_exercise_info)
Writing_DeskWork_Min.place(x=243, y=515)

Walking_Household_Hr = tkinter.Spinbox(Exercise_Data_Metrics, width=2, from_=0, to=100, state="readonly", increment=1,
                                       command=store_exercise_info)
Walking_Household_Hr.place(x=175, y=545)
Walking_Household_Min = tkinter.Spinbox(Exercise_Data_Metrics, width=2, from_=0, to=59, state="readonly", increment=1,
                                        command=store_exercise_info)
Walking_Household_Min.place(x=243, y=545)

Walking_Reg_Hr = tkinter.Spinbox(Exercise_Data_Metrics, width=2, from_=0, to=100, state="readonly", increment=1,
                                 command=store_exercise_info)
Walking_Reg_Hr.place(x=175, y=575)
Walking_Reg_Min = tkinter.Spinbox(Exercise_Data_Metrics, width=2, from_=0, to=59, state="readonly", increment=1,
                                  command=store_exercise_info)
Walking_Reg_Min.place(x=243, y=575)

#trigger collapse of functions for Exercise_Log
polyfile_recordE()

#-------------------------------------------------------------------------------------------------------------
#Settings
clear_all = tkinter.Button(Settings, text="Clear All User Data") #for future use
clear_all.place(x=50, y=50)


def cleanup_operations():
    Diet_Data.delete("all")
    Diet_Data.create_text(450, 268, text="EXITING...")
    Diet_Data.update()
    cleanup_empty_directories()
    time.sleep(0.5)
    root.destroy()


root.protocol("WM_DELETE_WINDOW", cleanup_operations)

root.mainloop()