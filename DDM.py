#Diet Data Metrics
import os
import tkinter
import time
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
Sleep_Data_Metrics = ttk.Frame(TabControl)
TabControl.add(Diet_Data_Metrics, text="Daily Log", padding=3)
TabControl.add(Sleep_Data_Metrics, text="Sleep Analysis", padding=3)
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
        hour_start = x_start_split[0]
        min_start = x_start_split[1]
        am_pm_start = x_start_split[2]
        real_time = True
        if hour_start == "":
            hour_start = 1
            min_start = "01"
            am_pm_start = "am"
        else:
            hour_start = int(x_start_split[0])

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
    while Time_datapoints != 0:
        Diet_Data.create_line(Time_x, 500, Time_x, 510, width=2, fill="lime")
        if real_time == True:
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


def weightcontrol_model_one():
    max_calories = 2600
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

def update_data_metrics():
    #clear canvas to intialize
    Diet_Data.delete("all")
    Diet_Data.update()
    bulid_axis()
    weightcontrol_model_one()

    day_fetch = str(Day.get())
    month_fetch = str(Month.get())
    year_fetch = str(Year.get())
    polyfile_dir = "/" + day_fetch + month_fetch + year_fetch
    wake_log = "/wake_log.txt"
    sleep_log = "/sleep_log.txt"
    if path.exists(polyfile + polyfile_dir + wake_log):
        Diet_Data.create_text(50, 50, text="Awoke at:")
        read_wake = open(polyfile + polyfile_dir + wake_log, "r", encoding='utf8')
        pull_wake = read_wake.read()
        read_wake.close()
        wake = pull_wake.split(":")
        Diet_Data.create_text(100, 50, text=(wake[0] + ":" + wake[1] + wake[2]))
    if path.exists(polyfile + polyfile_dir + sleep_log):
        Diet_Data.create_text(50, 70, text="Asleep at:")
        read_sleep = open(polyfile + polyfile_dir + sleep_log, "r", encoding='utf8')
        pull_sleep = read_sleep.read()
        read_sleep.close()
        sleep = pull_sleep.split(":")
        Diet_Data.create_text(100, 70, text=(sleep[0] + ":" + sleep[1] + sleep[2]))
    Diet_Data.update()

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
                                         font=("Times New Roman", 8), fill="cyan")
            Data_Log_Preview.create_text(110, 30, text=(split_wake[0] + ":" + split_wake[1] + split_wake[2]),
                                         font=("Times New Roman", 8), fill="cyan")
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
                                         font=("Times New Roman", 8), fill="cyan")
            Data_Log_Preview.create_text(110, 50, text=(split_sleep[0] + ":" + split_sleep[1] + split_sleep[2]),
                                         font=("Times New Roman", 8), fill="cyan")
            Data_Log_Preview.update()
            Asleep.delete(0, "end")
            Asleep.insert(0, (split_sleep[0] + ":" + split_sleep[1]))
            Asleep_amp.config(state="normal")
            Asleep_amp.delete(0, "end")
            Asleep_amp.insert(0, str((split_sleep[2])))
            Asleep_amp.config(state="readonly")

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
        Data_Log_Preview.create_text(170, 350, text=("Calorie Total = " + str(calorie_total)), fill="lime")
        Data_Log_Preview.update()
    update_data_metrics()


#Date Input
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

Day_Label = tkinter.Label(Diet_Data_Metrics, text="Day:").place(x=20, y=20)
Day = tkinter.Spinbox(Diet_Data_Metrics, width=3, from_=1, to=31, state="normal", command=polyfile_record)
Day.place(x=50, y=22)
Day.delete(0, "end")
Day.insert(0, day_get)
Day.config(state="readonly")

Month_Label = tkinter.Label(Diet_Data_Metrics, text="Month:").place(x=92, y=20)
Month = tkinter.Spinbox(Diet_Data_Metrics, width=10, values=("January", "February", "March", "April", "May", "June", "July", "August", "September", "October",
             "November", "December"), state="normal", command=polyfile_record)
Month.place(x=138, y=22)
Month_List = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October",
             "November", "December"]
Month.delete(0, "end")
Month.insert(0, Month_List[month_get-1])
Month.config(state="readonly")

Year_Label = tkinter.Label(Diet_Data_Metrics, text="Year:").place(x=220, y=20)
Year = tkinter.Spinbox(Diet_Data_Metrics, width=4, from_=2020, to=2100, state="normal", command=polyfile_record)
Year.place(x=255, y=22)
Year.delete(0, "end")
Year.insert(0, year_get)
Year.config(state="readonly")

#Sleep data INPUT
sleep_section = tkinter.Canvas(Diet_Data_Metrics, width=340, height=65, background="lightblue")
sleep_section.place(x=5, y=60)
sleep_section.create_rectangle(190, 7, 325, 60,)

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
            else:
                Asleep.delete(0, "end")
                Asleep.insert(0, "invalid")
        else:
            Asleep.delete(0, "end")
            Asleep.insert(0, "invalid")
    except:
        Asleep.delete(0, "end")
        Asleep.insert(0, "invalid")

Awoke_at = tkinter.Label(Diet_Data_Metrics, text="Awoke at:").place(x=15, y=70)
Awoke = tkinter.Entry(Diet_Data_Metrics, width=10)
Awoke.place(x=80, y=70)
Awoke.insert(0, "12:00")
Awoke_amp = tkinter.Spinbox(Diet_Data_Metrics, width=3, values=("am", "pm"), state="readonly")
Awoke_amp.place(x=150, y=70)

Asleep_at = tkinter.Label(Diet_Data_Metrics, text="Asleep at:").place(x=15, y=100)
Asleep = tkinter.Entry(Diet_Data_Metrics, width=10)
Asleep.place(x=80, y=100)
Asleep.insert(0, "12:00")
Asleep_amp = tkinter.Spinbox(Diet_Data_Metrics, width=3, values=("am", "pm"), state="readonly")
Asleep_amp.place(x=150, y=100)

small_font = font.Font(family="TkDefaultFont", size=7)
Log_Wake_Time = tkinter.Button(Diet_Data_Metrics, width=18, text="Log Wake Time", command=Log_Wake)
Log_Wake_Time['font'] = small_font
Log_Wake_Time.place(x=204, y=70)

Log_Sleep_Time = tkinter.Button(Diet_Data_Metrics, width=18, text="Log Sleep Time", command=Log_Sleep)
Log_Sleep_Time['font'] = small_font
Log_Sleep_Time.place(x=204, y=95)

#Food Input
food_section = tkinter.Canvas(Diet_Data_Metrics, width=340, height=100, background="lightgreen")
food_section.place(x=5, y=130)
food_section.create_rectangle(215, 33, 335, 97, fill="lime")

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

Food_Name_Label = tkinter.Label(Diet_Data_Metrics, text="Food Name:").place(x=36, y=140)
Food_Name = tkinter.Entry(Diet_Data_Metrics, width=30)
Food_Name.place(x=115, y=140)

Calories_Label = tkinter.Label(Diet_Data_Metrics, text="Calorie Content:").place(x=15, y=170)
Calories = tkinter.Entry(Diet_Data_Metrics, width=8)
Calories.place(x=115, y=170)

Time_Consumed_Label = tkinter.Label(Diet_Data_Metrics, text="Time Consumed:").place(x=10, y=200)
Time = tkinter.Entry(Diet_Data_Metrics, width=9)
Time.place(x=115, y=200)
Time.insert(0, "12:00")
Time_amp = tkinter.Spinbox(Diet_Data_Metrics, width=3, values=("am", "pm"), state="readonly")
Time_amp.place(x=180, y=200)

Log_Food = tkinter.Button(Diet_Data_Metrics, text="Log Food Data", command=Log_Food_Data)
Log_Food.place(x=237, y=168)

Clear_Item = tkinter.Button(Diet_Data_Metrics, text="clear", command=ClearFood)
Clear_Item.place(x=265, y=198)

polyfile_record() #auto-creates a file directory and calls the log-screen to update

def cleanup_operations():
    Diet_Data.delete("all")
    Diet_Data.create_text(450, 268, text="EXITING...")
    Diet_Data.update()
    cleanup_empty_directories()
    time.sleep(2)
    root.destroy()


root.protocol("WM_DELETE_WINDOW", cleanup_operations)

root.mainloop()