#Diet Data Metrics
import os
import tkinter
import time
import math
from tkinter import font
from os import path
from datetime import datetime
from tkinter import ttk #for notebook module

#Build Main Window
root = tkinter.Tk()
root.geometry('1280x640')
root.title('Diet Data Metrics')
root.resizable(0, 0)

#Setup Notebook
TabControl = ttk.Notebook(root)
Diet_Data_Metrics = ttk.Frame(TabControl)
Nutrition_Data_Metrics = ttk.Frame(TabControl)
TabControl.add(Diet_Data_Metrics, text="Main Log", padding=3)
TabControl.add(Nutrition_Data_Metrics, text="Nutrition Log", padding=3)
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

#Weight Controls
Weight_Control_Canvas = tkinter.Canvas(Diet_Data_Metrics, width=360, height=50, background="pink")
Weight_Control_Canvas.place(x=680, y=5)

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
                if am_pm_start == "pm":
                    hour_start = hour_start + 12
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
    bulid_axis()
    Wake_Duration()
    Calculate_BMI()
    #show averages
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

#Nutrition Data Metrics Date Setup
DayN = tkinter.Spinbox(Nutrition_Data_Metrics, width=3, from_=1, to=31, state="normal")
DayN.place(x=50, y=22)
DayN.delete(0, "end")
DayN.insert(0, day_get)
DayN.config(state="readonly")

MonthN = tkinter.Spinbox(Nutrition_Data_Metrics, width=10, values=("January", "February", "March", "April", "May", "June", "July", "August", "September", "October",
             "November", "December"), state="normal")
MonthN.place(x=154, y=22)
MonthN_List = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October",
             "November", "December"]
MonthN.delete(0, "end")
MonthN.insert(0, Month_List[month_get-1])
MonthN.config(state="readonly")

YearN = tkinter.Spinbox(Nutrition_Data_Metrics, width=4, from_=2020, to=2100, state="normal")
YearN.place(x=293, y=22)
YearN.delete(0, "end")
YearN.insert(0, year_get)
YearN.config(state="readonly")

#Nutrition Data Metrics Macronutrients Input
Macronutrients = tkinter.Canvas(Nutrition_Data_Metrics, width=340, height=200, background="lightsalmon")
Macronutrients.place(x=5, y=60)
Macronutrients.create_text(170, 20, text="MACRONUTRIENTS", font=("Comic Sans MS", 10))
Macronutrients.create_text(95, 50, text="Protein:", font=("Comic Sans MS", 10))
Macronutrients.create_text(75, 80, text="Carbohydrate:", font=("Comic Sans MS", 10))
Macronutrients.create_text(99, 110, text="Fiber:", font=("Comic Sans MS", 10))
Macronutrients.create_text(76, 140, text="Linoleic Acid:", font=("Comic Sans MS", 10))
Macronutrients.create_text(70, 170, text="α-Linoleic Acid:", font=("Comic Sans MS", 10))

Protein = tkinter.Spinbox(Nutrition_Data_Metrics, width=3, from_=0, to=200, state="readonly")
Protein.place(x=127, y=101)

#Nutrition Data Metrics Vitamins Input
Vitamins = tkinter.Canvas(Nutrition_Data_Metrics, width=340, height=500, background="skyblue3")
Vitamins.place(x=350, y=5)
Vitamins.create_text(170, 20, text="VITAMINS", font=("Comic Sans MS", 10))
Vitamins.create_text(70, 50, text="Vitamin A:", font=("Comic Sans MS", 10))
Vitamins.create_text(70, 80, text="Vitamin C:", font=("Comic Sans MS", 10))
Vitamins.create_text(70, 110, text="Vitamin D:", font=("Comic Sans MS", 10))
Vitamins.create_text(70, 140, text="Vitamin E:", font=("Comic Sans MS", 10))
Vitamins.create_text(70, 170, text="Vitamin K:", font=("Comic Sans MS", 10))
Vitamins.create_text(70, 200, text="Thiamin:", font=("Comic Sans MS", 10))
Vitamins.create_text(70, 230, text="Riboflavin:", font=("Comic Sans MS", 10))
Vitamins.create_text(70, 260, text="Niacin:", font=("Comic Sans MS", 10))
Vitamins.create_text(70, 290, text="Vitamin B6:", font=("Comic Sans MS", 10))
Vitamins.create_text(70, 320, text="Folate:", font=("Comic Sans MS", 10))
Vitamins.create_text(70, 350, text="Vitamin B12:", font=("Comic Sans MS", 10))
Vitamins.create_text(70, 380, text="Pantothenic Acid:", font=("Comic Sans MS", 10))
Vitamins.create_text(70, 410, text="Biotin:", font=("Comic Sans MS", 10))
Vitamins.create_text(70, 440, text="Choline:", font=("Comic Sans MS", 10))


#Nutrition Data Metrics Elements Input
Elements = tkinter.Canvas(Nutrition_Data_Metrics, width=340, height=250, background="mistyrose2")
Elements.place(x=695, y=5)

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

small_font = font.Font(family="Comic Sans MS", size=8)
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

smaller_font = font.Font(family="Comic Sans MS", size=6, weight="bold")
Male = tkinter.Checkbutton(Diet_Data_Metrics, text="Male", command=H_2)
Male['font'] = smaller_font
Male.place(x=920, y=10)
Male.select()

Female = tkinter.Checkbutton(Diet_Data_Metrics, text="Female", command=H_1)
Female['font'] = smaller_font
Female.place(x=916, y=33)

#Show Averages
Average_Calc = 1
def Calc_Averages():
    global Average_Calc
    if Average_Calc == 1:
        Average_Calc = 0
    else:
        Average_Calc = 1
    update_data_metrics()

Show_Averages = tkinter.Checkbutton(Diet_Data_Metrics, text="Plot Averages", command=Calc_Averages)
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

Show_Guides = tkinter.Checkbutton(Diet_Data_Metrics, text="Display Guides", command=Display_Guides)
Show_Guides['font'] = small_font
Show_Guides.place(x=150, y=200)

#Plot Hydration
Hydro = 0
def Plot_Hydration():
    global Hydro
    if Hydro == 0:
        Hydro = 1
    else:
        Hydro = 0
    update_data_metrics()

plot_hydro = tkinter.Checkbutton(Diet_Data_Metrics, text="Plot\nHydration", command=Plot_Hydration)
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

def cleanup_operations():
    Diet_Data.delete("all")
    Diet_Data.create_text(450, 268, text="EXITING...")
    Diet_Data.update()
    cleanup_empty_directories()
    time.sleep(0.5)
    root.destroy()


root.protocol("WM_DELETE_WINDOW", cleanup_operations)

root.mainloop()