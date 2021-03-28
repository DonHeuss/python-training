###############################################################################
#                                   Earthquake.py                             #
#DFH

###############################################################################

###############################################################################
#                                Import Libraries                             #
###############################################################################
import subprocess
import sys
import os
import getpass
import math

import requests
import json
import datetime as dt
import time
from dateutil import tz
from datetime import datetime

###############################################################################
#                                Global Variables                             #
###############################################################################
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

class fg:
    black = '\033[30m'
    red = '\033[31m'
    green = '\033[32m'
    orange = '\033[33m'
    blue = '\033[34m'
    purple = '\033[35m'
    cyan = '\033[36m'
    lightgrey = '\033[37m'
    darkgrey = '\033[90m'
    lightred = '\033[91m'
    lightgreen = '\033[92m'
    yellow = '\033[93m'
    lightblue = '\033[94m'
    pink = '\033[95m'
    lightcyan = '\033[96m'
    white = '\033[97m'
 
class bg:
    black = '\033[40m'
    red = '\033[41m'
    green = '\033[42m'
    orange = '\033[43m'
    blue = '\033[44m'
    purple = '\033[45m'
    cyan = '\033[46m'
    lightgrey = '\033[47m'
  
#Make the whole code 3.x.x compatable
if sys.version[0]=="3" : raw_input = input



app_state = "OPEN"
app_selected = "0"


#message
msg_description = ""

#colors
clrLabels = fg.white + bg.blue
clrDataLine = fg.green + bcolors.BOLD + bg.blue
clrDataLineSelected = fg.yellow + bg.blue
clrMsgLabel = fg.lightred + bg.blue
clrMsgValue = fg.yellow + bg.blue
clrInput = fg.lightgreen + bg.blue
clrInstruction = fg.yellow + bcolors.BOLD + bg.blue
#List display
page_divider = " =============================================================================="
max_line = 30
max_col = 80
display_len = 20

#calling URL
app_url = "https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/"
app_mag = ""
app_interval = ""

app_mag_title = ""
app_interval_title = ""

app_mag_index = 4
app_interval_index = 0
##############################################################################
#                                    Classes                                 #
##############################################################################
#*****************************************************************************
# Class: DisplayLine
#*****************************************************************************
class DisplayLine:
    
    #-----------------------
    #-- Properties
    #-----------------------
    #-- id
    def set_id(self, id):  self.__id = id
    def get_id(self):  return self.__id

    #-- item
    def set_item(self,item): self.__item = item
    def get_item(self): return self.__item
    
    #-- type
    def set_type(self,type): self.__type = type
    def get_type(self): return self.__type
    
    
    #-- selected
    def set_selected(self,selected): self.__selected = selected
    def get_selected():  return self.__selected
    
    
    
    #-----------------------
    #-- Constructor
    #-----------------------
    def __init__(self,id="",item="",type=""):
        self.__id = id
        self.__item = item
        self.__type = type
        self.__selected = "F"
    
    #-----------------------
    #-- Methods
    #-----------------------
   
    
#*****************************************************************************
# Class: DisplayList
#*****************************************************************************
class DisplayList:
    
    #-----------------------
    #-- Properties
    #-----------------------
    #-- set_records
    def set_record(self,DisplayLine):
        self.__arrlist.append(DisplayLine)
        
    #-- get_records
    def get_records(self):
        self.__records = self.__arrlist
        return self.__records
    
    
    #-----------------------
    #-- Constructor
    #-----------------------
    def __init__(self): self.__arrlist = []
    
    #-----------------------
    #-- Methods
    #-----------------------
    #-- get_record
    def get_record(self,index):
        return self.__arrlist[index]
        
    #-- get_count
    def get_record_count(self):
        return len(self.__arrlist)
    

##############################################################################
#                                 Screen Functions                           #
##############################################################################
#=============================================================================
#== function: user_entry
#=============================================================================
def user_entry(user_instruction):
    ####
    # Local Variables
    ####
        
    char=raw_input(clrInstruction+" Enter (" + user_instruction + "): " + clrInput)           
    
    return char
        
#=============================================================================
#== function: screen_pos
#=============================================================================
def screen_pos(text_in, x_pos, y_pos, color_in):
    x=int(x_pos)
    y=int(y_pos)
    if x>=255 : x=255
    if y>=255 : y=255
    if x<=0 : x = 0
    if y<=0 : y = 0
    HORIZ=str(x)
    VERT=str(y)
    
    txtDis = color_in + text_in + bcolors.ENDC
    print("\033[" + VERT + ";" + HORIZ + "f" + txtDis)

#=============================================================================
#== function: screen_header
#=============================================================================
def screen_header(title, sub_title ):
    
    title_offset = int((max_col - len(title))/2)+1
    sub_title_offset = int((max_col - len(sub_title))/2)+1

    screen_pos(title, title_offset,1,clrLabels)
    screen_pos(sub_title, sub_title_offset,2,clrLabels)
    screen_pos(page_divider, 1,3,clrLabels)

#=============================================================================
#== function: screen_header
#=============================================================================
def screen_footer(record_count, page_select,msg_in,cur_page,nbr_pages):

 
    page_count = "Page " + str(cur_page) + " of " + str(nbr_pages)
    
    if nbr_pages == 1 : page_select = ""
    elif cur_page == 1 : page_select = "        Next >"
    elif cur_page == nbr_pages : page_select = "< Prev"
    else: page_select = "< Prev / Next >"


    screen_pos(page_divider, 1, max_line - 3, clrLabels)
    screen_pos(page_count, 65, max_line - 2, clrLabels)
    screen_pos(page_select, 30, max_line - 2, clrLabels)
    screen_pos("MSG: ", 2, max_line - 1, clrLabels)
    screen_pos(msg_in, 7, max_line - 1, clrMsgValue)




#=============================================================================
#== function: display_screen_list
#=============================================================================
def display_screen_list(displayList, title, sub_title):
    ####
    # Global Variables
    ####
    global msg_description
    global app_state
    global app_selected
    
    ####
    # Local Variables
    ####
    cur_page = 1
    page_select = ""
    msg_in = msg_description
 
    ####
    # Determine Number of pages
    ####
    float_pages = float(displayList.get_record_count()) / display_len
    int_pages = int(displayList.get_record_count() / display_len)
    nbr_pages = int_pages
    if float_pages > float(int_pages): nbr_pages = int_pages + 1
    if nbr_pages == 0 : nbr_pages = 1
    
    ####
    # Display Lines
    ####
    while True:
        os.system('setterm -background blue -foreground green -store')
        os.system('clear')
        
        ####
        # Display list on screen
        ####
        screen_header(title,sub_title)
        
        ####
        # Data Lines
        ####
        display_start = (cur_page * display_len) -  display_len 
        display_stop = display_start + display_len
        if display_stop > displayList.get_record_count() : display_stop = displayList.get_record_count()

        offset = 4
        y_pos = 1
        if displayList.get_record_count() == 0 :
            msg_in = "No Record founds"
        else:
            screen_pos("     MAG                   LOCATION                      DATE/TIME (LOCAL)",3,offset,clrLabels)
            screen_pos("    ----- --------------------------------------------- -------------------",3,offset+1,clrLabels)
            for x in range(display_start, display_stop):
                y_pos = y_pos + 1
                screen_pos(displayList.get_record(x).get_id() + " " + displayList.get_record(x).get_item(),3,offset+y_pos,clrDataLine)
              
        ####
        # Footer
        ####
        screen_footer(displayList.get_record_count(), page_select,msg_in,cur_page,nbr_pages)
       
        ####
        # Process then answer
        ####
        user_instruction = "X:Exit, T:Interval, M:Magnitude, F:Refresh "
        ans = user_entry(user_instruction)

        if ans.isdigit():
             if int(ans) >= 1 and int(ans) <= displayList.get_record_count():
                return ans
             
        elif str.upper(ans) == ">":
            #Next Page
            if cur_page < nbr_pages: cur_page = cur_page + 1
             
        elif str.upper(ans) == "<":
            #Prev page
            if cur_page > 1: cur_page = cur_page - 1
                
        elif str.upper(ans) == "F":
            app_state = "OPEN"
            break

        elif str.upper(ans) == "X":
            app_state = "EXIT"
            break
        elif str.upper(ans) == "T":
            app_state = "TIME"
            break
        elif str.upper(ans) == "M":
            app_state = "MAG"
            break
        
    return "0"


#=============================================================================
#== function: display_screen_list
#=============================================================================
def display_screen_detail(objData, title, sub_title):
    ####
    # Global Variables
    ####
    global msg_description
    global app_state
    global app_selected
    
    ####
    # Local Variables
    ####
    cur_page = 1
    page_select = ""
    msg_in = msg_description
 
    ####
    # Determine Number of pages
    ####
    nbr_pages = 1
    
    ####
    # Display Lines
    ####
    while True:
        os.system('setterm -background blue -foreground green -store')
        os.system('clear')
        
        ####
        # Display list on screen
        ####
        screen_header(title,sub_title)
 
 
 
        #time format
        time1 = objData['properties']['time']
        utc =  get_coordinated_universal_time(time1)
        local = get_local_time(utc)
        strUtc = str(utc.strftime('%d/%m/%Y %H:%M:%S'))
        strLocal = str(local.strftime('%d/%m/%Y %H:%M:%S'))
        tz = str(objData['properties']['tz'])
        
        
        objCorrdinates = objData['geometry']['coordinates']
        strLongitude = str(objCorrdinates[0])
        strLatitude = str(objCorrdinates[1])
        strDepth =  str(objCorrdinates[2]) + " KM"

        strMag = str(objData['properties']['mag'])

        ####
        # Data Lines
        ####
        offset = 4

        #Time
        pos_time = 4
        screen_pos("TIME",2,pos_time,clrLabels)
        screen_pos("LOCAL    :" ,5,pos_time+1,clrLabels)
        screen_pos("UTC      :",5,pos_time+2,clrLabels)
        screen_pos("TIME ZONE:",5,pos_time+3,clrLabels)
        screen_pos(strLocal,16,pos_time+1,clrDataLine)
        screen_pos(strUtc,16,pos_time+2,clrDataLine)
        screen_pos(tz,16,pos_time+3,clrDataLine)
        
        
        #Locatiion
        pos_loc = 12
        screen_pos("LOCATION ",2,pos_loc,clrLabels)
        screen_pos("PLACE    :",5,pos_loc+1,clrLabels)    
        screen_pos("LONGITUDE:",5,pos_loc+2,clrLabels)
        screen_pos("LATITUDE :",5,pos_loc+3,clrLabels)
        screen_pos("DEPTH    :",5,pos_loc+4,clrLabels)
                  
        
        screen_pos(objData['properties']['place'],16,pos_loc+1,clrDataLine)
        screen_pos(strLongitude,16,pos_loc+2,clrDataLine)
        screen_pos(strLatitude,16,pos_loc+3,clrDataLine)
        screen_pos(strDepth,16,pos_loc+4,clrDataLine)
        
        
        #MAGNITUDE
        pos_mag = 20
        screen_pos("MAGNITUDE",2,pos_mag,clrLabels)
        screen_pos("MAG      :",5,pos_mag+1,clrLabels)
        screen_pos("MAG TYPE :",5,pos_mag+2,clrLabels)
        screen_pos("TYPE     :",5,pos_mag+3,clrLabels)
        
        
        screen_pos(strMag,16,pos_mag+1,clrDataLine)
        screen_pos(objData['properties']['magType'],16,pos_mag+2,clrDataLine)
        screen_pos(objData['properties']['type'],16,pos_mag+3,clrDataLine)
        
                
        ####
        # Footer
        ####
        screen_footer(1, page_select,msg_in,cur_page,nbr_pages)
       
        ####
        # Process then answer
        ####
        user_instruction = "X:Exit, T:Interval, M:Magnitude, F:Refresh "
        ans = user_entry(user_instruction)

        if ans.isdigit():
             if int(ans) >= 1 and int(ans) <= 1:
                return ans
             
        elif str.upper(ans) == ">":
            #Next Page
            if cur_page < nbr_pages: cur_page = cur_page + 1
             
        elif str.upper(ans) == "<":
            #Prev page
            if cur_page > 1: cur_page = cur_page - 1
                
        elif str.upper(ans) == "F":
            app_state = "OPEN"
            break

        elif str.upper(ans) == "X":
            app_state = "EXIT"
            break
        elif str.upper(ans) == "T":
            app_state = "TIME"
            break
        elif str.upper(ans) == "M":
            app_state = "MAG"
            break
        
    return "0"
##############################################################################
#                                     Applications                           #
##############################################################################

#=============================================================================
#== function: display_screen
#=============================================================================
def test_screen():
    print("Test Screen")
 
#=============================================================================
#== function: get_coordinated_universal_time
#=============================================================================
def get_coordinated_universal_time(timeIn):
    utc_datetime = dt.datetime.utcfromtimestamp(timeIn / 1000.)
    return utc_datetime
        
#=============================================================================
#== function: get_local_time
#=============================================================================
def get_local_time(utc_in):
    from_zone = tz.tzutc()
    to_zone = tz.tzlocal()
    utc = utc_in.replace(tzinfo=from_zone)
    local_time = utc.astimezone(to_zone)
    return local_time 
 
#=============================================================================
#== function: get_eq_data
#=============================================================================
def get_eq_features():
    
    app_param = magList.get_record(app_mag_index).get_type() + "_" + intervalList.get_record(app_interval_index).get_type()
    AppURL = app_url + app_param + ".geojson"
    
    
    r = requests.get(AppURL)
    earthquake = r.json()
    features = earthquake['features']

   #Clean data
    for feature in features:
        if str(feature['properties']['mag']).upper()  == 'NONE':
            feature['properties']['mag'] = 0

    #sort on magnitude
    features_sort = sorted(features, key=lambda k : k['properties'].get('mag',0),reverse = True)
    
    return features_sort

#=============================================================================
#== function: get_eq_earthquakes
#=============================================================================
def get_eq_earthquakes():
    
    app_param = magList.get_record(app_mag_index).get_type() + "_" + intervalList.get_record(app_interval_index).get_type()
    AppURL = app_url + app_param + ".geojson"
    
    
    r = requests.get(AppURL)
    earthquakes = r.json()
    #feachers = earthquake['features']
    #feachers_sort = sorted(feachers, key=lambda k : k['properties'].get('mag',0),reverse = True)
    return earthquakes

#=============================================================================
#== function: set_intervals
#=============================================================================
def get_intervals():
    dataList = DisplayList()
    
    dataList.set_record(DisplayLine("  1", "Past Hour","hour"))
    dataList.set_record(DisplayLine("  2", "Past Day","day"))
    dataList.set_record(DisplayLine("  3", "Past 7 Days","week"))
    dataList.set_record(DisplayLine("  4", "Past 30 Days","month"))
    
    return dataList

#=============================================================================
#== function: set_intervals
#=============================================================================
def get_mags():
    dataList = DisplayList()
    
    dataList.set_record(DisplayLine("  1", "Significant Earthquakes","significant"))
    dataList.set_record(DisplayLine("  2", "M4.5+ Earthquakes","4.5"))
    dataList.set_record(DisplayLine("  3", "M2.5+ Earthquakes","2.5"))
    dataList.set_record(DisplayLine("  4", "M1.0+ Earthquakes","1.0"))
    dataList.set_record(DisplayLine("  5", "All Earthquakes","all"))
    
    return dataList

#=============================================================================
#== function: set_intervals
#=============================================================================
def get_earthquakes():
    
    dataList = DisplayList()    
      
    eq_features = get_eq_features()
 
 
    rowcount = 0
    for eq_feature in eq_features:
        mag = eq_feature['properties']['mag']
        place = eq_feature['properties']['place']
        time1 = eq_feature['properties']['time']
        utc =  get_coordinated_universal_time(time1)
        local = get_local_time(utc)
        
        
        strLocal = str(local.strftime('%d/%m/%Y %H:%M:%S'))
        rowcount = rowcount + 1
        strRow = str(rowcount).rjust(3,' ')
        strMag = f"{mag:.2f}"
        strPlace = place[:45]
        
        dataList.set_record(DisplayLine(strRow, strMag.ljust(5,' ') + " " + strPlace.ljust(45,' ') + " " + strLocal , "MENU"))


    return dataList
##############################################################################
#                                      Main                                  #
##############################################################################
####
# Initialize
####
displayList = DisplayList()
intervalList = get_intervals()
magList = get_mags()

####
#  Execute Main
####
result_ans = "0"

while True:
    url_param = magList.get_record(app_mag_index).get_type() + "_" + intervalList.get_record(app_interval_index).get_type()
    sub_title = magList.get_record(app_mag_index).get_item() + " for " + intervalList.get_record(app_interval_index).get_item()


    if app_state == "OPEN":
        eq_features = get_earthquakes()
        result_ans = display_screen_list(eq_features,"EARTHQUAKES",sub_title)
        if result_ans != "0" : app_state = "DETAIL"
  
    elif app_state == "MAG":
        result_ans = display_screen_list(magList,"EARTHQUAKES","Magnitude")
        app_mag_index = int(result_ans)-1
        app_state = "OPEN"
    
    
    elif app_state == "TIME":
        result_ans = display_screen_list(intervalList,"EARTHQUAKES","Time Interval")
        app_interval_index = int(result_ans)-1
        app_state = "OPEN"
       
  
    elif app_state == "DETAIL":
        eq_features = get_eq_features()
        result_ans = display_screen_detail(eq_features[int(result_ans)-1],"EARTHQUAKES","Detail Information")
                
                
                
    elif app_state == "EXIT":
        print(bcolors.ENDC)
        os.system('clear')
        break


# app_param = magList.get_record(app_mag_index).get_type() + "_" + intervalList.get_record(app_interval_index).get_type()
# AppURL = app_url + app_param + ".geojson"
# print(AppURL)

# eqList = get_eq_features()
# rowcount = 0
# for eq_feature in eqList:
#     mag = eq_feature['properties']['mag']
#     place = eq_feature['properties']['place']
#     time1 = eq_feature['properties']['time']
#     utc =  get_coordinated_universal_time(time1)
#     local = get_local_time(utc)
#     
#     
#     strLocal = str(local.strftime('%d/%m/%Y %H:%M:%S'))
#     rowcount = rowcount + 1
#     strRow = str(rowcount).rjust(3,' ')
#     #strMag = f"{mag:.2f}"
#     strMag = str(mag)
#     
#     
#     print(rowcount, mag , "  " , place.ljust(50,' ') )
#     print("    ", f"{float(mag):.2f}" )
