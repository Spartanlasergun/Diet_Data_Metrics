#Diet Data Metrics
import os
import tkinter
import time
import math
from tkinter import *
from tkinter import font
from os import path
from datetime import datetime
from tkinter import ttk #for notebook module

#Build Main Window
root = tkinter.Tk()
root.geometry('1280x640')
root.title('Health Data Metrics')
root.resizable(0, 0)

#Setup Notebook
TabControl = ttk.Notebook(root)
Diet_Data_Metrics = ttk.Frame(TabControl)
Nutrition_Data_Metrics = ttk.Frame(TabControl)
Exercise_Data_Metrics = ttk.Frame(TabControl)
Anthropometric_Data_Log = ttk.Frame(TabControl)
Cognitive_Data_Log = ttk.Frame(TabControl)
Statistical_Analysis = ttk.Frame(TabControl)
User_Settings = ttk.Frame(TabControl)
TabControl.add(Diet_Data_Metrics, text="Main Log", padding=3)
TabControl.add(Nutrition_Data_Metrics, text="Nutrition Log", padding=3)
TabControl.add(Exercise_Data_Metrics, text="Exercise Log", padding=3)
TabControl.add(Anthropometric_Data_Log, text="Anthropometric Data Log", padding=3)
TabControl.add(Cognitive_Data_Log, text="Cognitive Data Log", padding=3)
TabControl.add(Statistical_Analysis, text="Statistical Analysis", padding=3)
TabControl.add(User_Settings, text="User Settings", padding=3)
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
                if (time_cycle != start_cycle) and (time_hr < 12):
                    start_cycle = time_cycle
                    cycle_factor = cycle_factor + 1
                if (time_cycle == start_cycle) and (start_hr == 12):
                    start_hr = 0
                time_hr_mag = (time_hr + (12*cycle_factor)) - start_hr
                time_min_mag = time_min - start_min
                x_val = 50 + (time_hr_mag*50) + ((time_min_mag/60)*50)
                food_data_points.append(str(x_val) + ":" + str(y_val))

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
                                  fill="green")
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
                        sleep_hr = 24 + sleep_hr
                    else:
                        sleep_hr = sleep_hr + 12
                    if hour_start == 12:
                        hour_start = 0
                    hour_start = hour_start + 12
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
            for data in water_data:
                split = data.split(":")
                water_hr = int(split[0])
                water_min = int(split[1])
                water_cycle = split[2]
                water_amount = int(split[3])
                #determine hour and min magnitude
                if (water_cycle == start_cycle) and (water_hr < start_hr):
                    hr_mag = abs((water_hr +24) - start_hr)
                    min_mag = water_min - start_min
                    if min_mag < 0:
                        hr_mag = hr_mag - 1
                        min_mag = min_mag + 60
                elif water_cycle == start_cycle:
                    if water_hr == 12:
                        hr_mag = ((water_hr + 12) - start_hr)
                    else:
                        hr_mag = abs(water_hr - start_hr)
                    min_mag = water_min - start_min
                    if min_mag < 0:
                        hr_mag = hr_mag - 1
                        min_mag = min_mag + 60
                else:
                    if water_hr < 12:
                        hr_mag = (water_hr + 12) - start_hr
                    else:
                        hr_mag = water_hr - start_hr
                    min_mag = water_min - start_min
                    if min_mag < 0:
                        hr_mag = hr_mag - 1
                        min_mag = min_mag + 60

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
    Diet_Data.update()
    if Hydro == 1:
        Keep_Hydrated()
    Wake_Duration()
    Calculate_BMI()
    #show averages
    if Average_Calc == 1:
        plot_food_averages()
    bulid_axis()
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
    Data_Log_Preview.update()
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
            Data_Log_Preview.update()
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
Age.insert(0, "24")
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

#Nutrition Data Metrics Canvas Declarations
Macronutrients = tkinter.Canvas(Nutrition_Data_Metrics, width=340, height=250, background="lightgreen")
Macronutrients.place(x=695, y=60)

Vitamins = tkinter.Canvas(Nutrition_Data_Metrics, width=340, height=540, background="skyblue2")
Vitamins.place(x=350, y=60)

Elements = tkinter.Canvas(Nutrition_Data_Metrics, width=340, height=540, background="mistyrose2")
Elements.place(x=5, y=60)

#Nutrition Data Display - Pie Chart
Nutrition_Display = tkinter.Canvas(Nutrition_Data_Metrics, width=336, height=280, background="grey", bd=2, relief='sunken')
Nutrition_Display.place(x=695, y=315)

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

#Nutrition Data Metrics Macronutrients Input
def Draw_Macronutrients():
    Macronutrients.create_text(110, 20, text="MACRONUTRIENTS", font=("Comic Sans MS", 10))
    Macronutrients.create_rectangle(3, 3, 341, 251, width=2, outline="grey") #Border
    Macronutrients.create_text(280, 20, text="          Dietary\nReference Intakes",
                         font=("Comic Sans MS", 8))
    Macronutrients.create_line(220, 0, 220, 185)
    Macronutrients.create_line(0, 35, 340, 35)
    Macronutrients.create_line(0, 65, 340, 65)
    Macronutrients.create_line(0, 95, 340, 95)
    Macronutrients.create_line(0, 125, 340, 125)
    Macronutrients.create_line(0, 155, 340, 155)
    Macronutrients.create_line(0, 185, 340, 185)
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
Protein = tkinter.Spinbox(Nutrition_Data_Metrics, width=4, from_=0, to=200, increment=1, state="readonly",
                          command=Draw_Nutrition_Log)
Protein.place(x=815, y=100)

Carbohydrate = tkinter.Spinbox(Nutrition_Data_Metrics, width=4, from_=0, to=500, increment=1, state="readonly",
                          command=Draw_Nutrition_Log)
Carbohydrate.place(x=815, y=130)

Fiber = tkinter.Spinbox(Nutrition_Data_Metrics, width=4, from_=0, to=150, increment=1, state="readonly",
                          command=Draw_Nutrition_Log)
Fiber.place(x=815, y=160)

Linoleic_Acid = tkinter.Spinbox(Nutrition_Data_Metrics, width=4, from_=0, to=200, increment=1, state="readonly",
                          command=Draw_Nutrition_Log)
Linoleic_Acid.place(x=815, y=190)

Alpha_Linoleic_Acid = tkinter.Spinbox(Nutrition_Data_Metrics, width=4, from_=0, to=20, increment=0.1, state="readonly",
                          command=Draw_Nutrition_Log)
Alpha_Linoleic_Acid.place(x=815, y=220)

#Nutrition Data Metrics Vitamins Input
def Draw_Vitamins():
    Vitamins.create_rectangle(3, 3, 340, 540, width=2, outline="grey") #Border
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
Vitamin_A.place(x=475, y=100)

Vitamin_C = tkinter.Spinbox(Nutrition_Data_Metrics, width=4, from_=0, to=2000, increment=1, state="readonly",
                            command=Draw_Nutrition_Log)
Vitamin_C.place(x=475, y=130)

Vitamin_D = tkinter.Spinbox(Nutrition_Data_Metrics, width=4, from_=0, to=100, increment=0.1, state="readonly",
                            command=Draw_Nutrition_Log)
Vitamin_D.place(x=475, y=160)

Vitamin_E = tkinter.Spinbox(Nutrition_Data_Metrics, width=4, from_=0, to=100, increment=1, state="readonly",
                            command=Draw_Nutrition_Log)
Vitamin_E.place(x=475, y=190)

Vitamin_K = tkinter.Spinbox(Nutrition_Data_Metrics, width=4, from_=0, to=500, increment=1, state="readonly",
                            command=Draw_Nutrition_Log)
Vitamin_K.place(x=475, y=220)

Thiamin = tkinter.Spinbox(Nutrition_Data_Metrics, width=4, from_=0, to=20, increment=0.1, state="readonly",
                            command=Draw_Nutrition_Log)
Thiamin.place(x=475, y=250)

Riboflavin = tkinter.Spinbox(Nutrition_Data_Metrics, width=4, from_=0, to=20, increment=0.1, state="readonly",
                            command=Draw_Nutrition_Log)
Riboflavin.place(x=475, y=280)

Niacin = tkinter.Spinbox(Nutrition_Data_Metrics, width=4, from_=0, to=100, increment=1, state="readonly",
                            command=Draw_Nutrition_Log)
Niacin.place(x=475, y=310)

Vitamin_B6 = tkinter.Spinbox(Nutrition_Data_Metrics, width=4, from_=0, to=20, increment=0.1, state="readonly",
                            command=Draw_Nutrition_Log)
Vitamin_B6.place(x=475, y=340)

Folate = tkinter.Spinbox(Nutrition_Data_Metrics, width=4, from_=0, to=2000, increment=5, state="readonly",
                            command=Draw_Nutrition_Log)
Folate.place(x=475, y=370)

Vitamin_B12 = tkinter.Spinbox(Nutrition_Data_Metrics, width=4, from_=0, to=20, increment=0.1, state="readonly",
                            command=Draw_Nutrition_Log)
Vitamin_B12.place(x=475, y=400)

Pantothenic_Acid = tkinter.Spinbox(Nutrition_Data_Metrics, width=4, from_=0, to=50, increment=0.1, state="readonly",
                            command=Draw_Nutrition_Log)
Pantothenic_Acid.place(x=475, y=430)

Biotin = tkinter.Spinbox(Nutrition_Data_Metrics, width=4, from_=0, to=200, increment=1, state="readonly",
                            command=Draw_Nutrition_Log)
Biotin.place(x=475, y=460)

Choline = tkinter.Spinbox(Nutrition_Data_Metrics, width=4, from_=0, to=2000, increment=5, state="readonly",
                            command=Draw_Nutrition_Log)
Choline.place(x=475, y=490)

#Nutrition Data Metrics Elements Input
def Draw_Elements():
    Elements.create_rectangle(3, 3, 340, 540, width=2, outline="grey") #Border
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
    Elements.create_line(0, 485, 340, 485)
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
Calcium.place(x=120, y=100)

Chromium = tkinter.Spinbox(Nutrition_Data_Metrics, width=4, from_=0, to=100, increment=1, state="readonly",
                           command=Draw_Nutrition_Log)
Chromium.place(x=120, y=130)

Copper = tkinter.Spinbox(Nutrition_Data_Metrics, width=4, from_=0, to=2000, increment=5, state="readonly",
                         command=Draw_Nutrition_Log)
Copper.place(x=120, y=160)

Fluoride = tkinter.Spinbox(Nutrition_Data_Metrics, width=4, from_=0, to=20, increment=1, state="readonly",
                           command=Draw_Nutrition_Log)
Fluoride.place(x=120, y=190)

Iodine = tkinter.Spinbox(Nutrition_Data_Metrics, width=4, from_=0, to=200, increment=1, state="readonly",
                         command=Draw_Nutrition_Log)
Iodine.place(x=120, y=220)

Iron = tkinter.Spinbox(Nutrition_Data_Metrics, width=4, from_=0, to=50, increment=0.1, state="readonly",
                       command=Draw_Nutrition_Log)
Iron.place(x=120, y=250)

Magnesium = tkinter.Spinbox(Nutrition_Data_Metrics, width=4, from_=0, to=1000, increment=5, state="readonly",
                            command=Draw_Nutrition_Log)
Magnesium.place(x=120, y=280)

Manganese = tkinter.Spinbox(Nutrition_Data_Metrics, width=4, from_=0, to=10, increment=0.1, state="readonly",
                            command=Draw_Nutrition_Log)
Manganese.place(x=120, y=310)

Molybdenum = tkinter.Spinbox(Nutrition_Data_Metrics, width=4, from_=0, to=100, increment=1, state="readonly",
                             command=Draw_Nutrition_Log)
Molybdenum.place(x=120, y=340)

Phosphorus = tkinter.Spinbox(Nutrition_Data_Metrics, width=4, from_=0, to=1200, increment=5, state="readonly",
                             command=Draw_Nutrition_Log)
Phosphorus.place(x=120, y=370)

Selenium = tkinter.Spinbox(Nutrition_Data_Metrics, width=4, from_=0, to=150, increment=1, state="readonly",
                           command=Draw_Nutrition_Log)
Selenium.place(x=120, y=400)

Zinc = tkinter.Spinbox(Nutrition_Data_Metrics, width=4, from_=0, to=50, increment=1, state="readonly",
                       command=Draw_Nutrition_Log)
Zinc.place(x=120, y=430)

Potassium = tkinter.Spinbox(Nutrition_Data_Metrics, width=4, from_=0, to=5000, increment=5, state="readonly",
                            command=Draw_Nutrition_Log)
Potassium.place(x=120, y=460)

Sodium = tkinter.Spinbox(Nutrition_Data_Metrics, width=4, from_=0, to=9999, increment=5, state="readonly",
                         command=Draw_Nutrition_Log)
Sodium.place(x=120, y=490)

Chloride = tkinter.Spinbox(Nutrition_Data_Metrics, width=4, from_=0, to=10, increment=0.1, state="readonly",
                           command=Draw_Nutrition_Log)
Chloride.place(x=120, y=520)

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

def cleanup_operations():
    Diet_Data.delete("all")
    Diet_Data.create_text(450, 268, text="EXITING...")
    Diet_Data.update()
    cleanup_empty_directories()
    time.sleep(0.5)
    root.destroy()


root.protocol("WM_DELETE_WINDOW", cleanup_operations)

root.mainloop()