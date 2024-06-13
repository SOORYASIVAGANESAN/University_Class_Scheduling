import pandas as pd 

import gspread
from gspread_dataframe import set_with_dataframe


def builder(sheetid_source,a,b,c,d,e):
# reads data from gsheet 
    gc = gspread.service_account(filename = "/Users/soorya/Library/CloudStorage/GoogleDrive-sooryabizz@gmail.com/My Drive/Desktop/soorya/Visual Studio Code Soorya/credentials.json")
    sheet = gc.open_by_url(sheetid_source)

    #reading data from each worksheet
    Sub1 = sheet.worksheet(a)
    Sub2 = sheet.worksheet(b)
    Sub3 = sheet.worksheet(c)
    Sub4 = sheet.worksheet(d)
    results= sheet.worksheet(e)

    return(Sub1,Sub2,Sub3, Sub4, results)


sheetid_source= "https://docs.google.com/spreadsheets/d/1_AeNPbRYSO7jI4FRa5Ai3OV_TIf49rQZE2A8tuB7L5M/edit?usp=sharing"
a= 'ECON-UB 1'
b= 'STAT-UB 103'
c= 'MULT-UB 100'
d= 'CSCI-UA 2'
e= 'Output'
Sub1,Sub2,Sub3, Sub4, result_sheet = builder(sheetid_source,a,b,c,d,e)

# making dummy Output Schedule df, DO NOT delete this as it helps store initial variable for the for loops
dfSchedule = pd.DataFrame(columns = ['Monday','Tuesday','Wednesday','Thursday','Friday','Empty1','Empty2','Course_no','Subject','Proff.'],
        index = ['8-9:15','9:30-10:45','11a-12:15','12:30-1:45','2-3:15','3:30-4:45','4:55-6:10'])

# creating df for border in gsheets
dfBorder = pd.DataFrame(columns = ['#','#','#','#','#','#','#','#','#','#','#','#'])



#convert the worksheet into dataframe 
data = Sub1.get_all_values()
headers = data.pop(0)

dfSub1 = pd.DataFrame(data, columns=headers)

data = Sub2.get_all_values()
headers = data.pop(0)

dfSub2 = pd.DataFrame(data, columns=headers)

data = Sub3.get_all_values()
headers = data.pop(0)

dfSub3 = pd.DataFrame(data, columns=headers)

data = Sub4.get_all_values()
headers = data.pop(0)

dfSub4 = pd.DataFrame(data, columns=headers)

########################################################################################################
#no.of rows in dfsub_1
no_rows_dfSub1 = len(dfSub1.axes[0]) 
no_rows_dfSub2 = len(dfSub2.axes[0]) 
no_rows_dfSub3 = len(dfSub3.axes[0])  
no_rows_dfSub4 = len(dfSub4.axes[0])  

#no of rows and columns in dfschedule
no_rows_dfSchedule= len(dfSchedule.axes[0])
no_columns_dfschedule= len(dfSchedule.axes[1])

#course_no index
uniqueScheduleID_ind= 7
subject_courseno_ind= 8
subject_name_ind= 9
prof_ind=10

#initilizing which row to begin for each schedule in the 'Output' sheet
output_row= 1

#creating a dict to hold multip. schedules
dfSchedule_collection= {}

#creating a temporary collection for each schedule
dfSchedule_collection_temp= {}


#initilizing a flag to come out of all loops and return to the outermost loop
flag= False

#initilizing the stating row for Uniq. Schedule ID,	Course_no. ,	Subject,	Proff.
extra_ind= 2


for i in range(no_rows_dfSub2):
        
        # if there is atleat 1 fully built schedule present then re-assign the indentation stating row for Uniq. Schedule ID,	Course_no. ,	Subject,	Proff.
        if len(dfSchedule_collection) >= 1:
             extra_ind = 2
        else:
             print("dfSchedulecollection does not have a schedule yet")
        
        print(" ################################################################################")
        print("here ", no_rows_dfSub2)
        print("me ",i)

        subject_name= dfSub2.loc[i][0] 
        subject_course_no= dfSub2.loc[i][1]
        print(subject_course_no)
        subject_day= dfSub2.loc[i][2]

        if subject_day == 'TR':
            sub_day1= "Tuesday"
            sub_day2= "Wednesday"
        
        elif subject_day== 'MW':
            sub_day1= 'Monday'
            sub_day2= 'Wednesday'

        elif subject_day=='M':
            sub_day1= 'Monday'
            sub_day2= None

        elif subject_day== 'T':
            sub_day1= 'Tuesday'
            sub_day2= None

        elif subject_day== 'W':
            sub_day1= 'Wednesday'
            sub_day2= None
        
        elif subject_day== 'R':
            sub_day1= 'Thursday'
            sub_day2= None

        else:
            sub_day1= 'Friday'
            sub_day2= None

        subject_time= dfSub2.loc[i][3]   

        subject_prof= dfSub2.loc[i][4]
        subject_prof_rating_default = float(dfSub2.loc[i][5])
        subject_status= dfSub2.loc[i][7]


        if subject_prof_rating_default >= 3.9 and subject_status== "Open":
                
                #unique schedule_no for each schedule data frame
                schedule_no= int(subject_course_no)**2
                dfSchedule_collection[schedule_no]= pd.DataFrame(columns = ['Monday','Tuesday','Wednesday','Thursday','Friday','Empty1','Empty2','Uniq. Schedule ID','Course_no','Subject','Proff.'],
                index = ['8-9:15','9:30-10:45','11a-12:15','12:30-1:45','2-3:15','3:30-4:45','4:55-6:10'])

        else:
             continue

        for j in (dfSub1, dfSub4):
                    print("###############################################################")
                    
                    #the VARIABLE NAME is subject_"""""_default because these subjects only have one class (csci ua 3 and ECON algebra)  
                    subject_name_default= j.loc[0][0] 

                    subject_course_no_default= j.loc[0][1]
                    subject_day_default=j.loc[0][2]

                    if subject_day_default == 'TR':
                        sub_day1_default= "Tuesday"
                        sub_day2_default= "Wednesday"
                    
                    elif subject_day_default== 'MW':
                        sub_day1_default= 'Monday'
                        sub_day2_default= 'Wednesday'

                    elif subject_day_default=='M':
                        sub_day1_default= 'Monday'
                        sub_day2_default= None

                    elif subject_day_default== 'T':
                        sub_day1_default= 'Tuesday'
                        sub_day2_default= None

                    elif subject_day_default== 'W':
                        sub_day1_default= 'Wednesday'
                        sub_day2_default= None
                    
                    elif subject_day_default== 'R':
                        sub_day1_default= 'Thursday'
                        sub_day2_default= None

                    else:
                        sub_day1_default= 'Friday'
                        sub_day2_default= None

                    subject_time_default= j.loc[0][3]   

                    subject_prof_default= j.loc[0][4]



                    for x in range (no_rows_dfSchedule):
                            #checking if the time of class = row of dfschedule
                            if dfSchedule_collection[schedule_no].index[x] == subject_time_default:
                                
                                for d in range( no_columns_dfschedule):
                                    #checking if the day of class = column of dfschedule
                                    if dfSchedule_collection[schedule_no].columns[d]== sub_day1_default:

                                        dfSchedule_collection[schedule_no].loc[dfSchedule.index[x]][d]= subject_name_default

                                        if sub_day2_default == None:
                                            pass

                                        else:
                                            dfSchedule_collection[schedule_no].loc[dfSchedule.index[x]][d+2]= subject_name_default

                                        print(extra_ind)
                                        
                                        dfSchedule_collection[schedule_no].loc[dfSchedule.index[extra_ind]][subject_courseno_ind]=subject_course_no_default
                                        dfSchedule_collection[schedule_no].loc[dfSchedule.index[extra_ind]][subject_name_ind]=subject_name_default
                                        dfSchedule_collection[schedule_no].loc[dfSchedule.index[extra_ind]][prof_ind]=subject_prof_default
                                        #dfSchedule_collection[schedule_no].loc[dfSchedule.index[extra_ind]][uniqueScheduleID_ind]=schedule_no
                                        extra_ind= extra_ind+1
                                        print(extra_ind)
                                        #print(dfSchedule_collection[schedule_no].loc[dfSchedule.index[5]])
                                        #print(dfSchedule_collection[schedule_no])

                                    else:
                                        pass
                            else:
                                pass


        #..............Below is the continuation for dfSub2 ...............

        print("######################")
        for x in range (no_rows_dfSchedule):
                
            #checking if the time of class = row of dfschedule
            if dfSchedule_collection[schedule_no].index[x] == subject_time:
                
                for j in range( no_columns_dfschedule):

                    #checking if the day of class = column of dfschedule
                    if dfSchedule_collection[schedule_no].columns[j]== sub_day1:

                        print("######################")
                        print(dfSchedule_collection[schedule_no].isnull().loc[dfSchedule.index[x]][j])
                        #check if the specific date and time is empty... if "if" condition is True then the cell is empty
                        if dfSchedule_collection[schedule_no].isnull().loc[dfSchedule.index[x]][j] == True:

                            dfSchedule_collection[schedule_no].loc[dfSchedule.index[x]][j]= subject_name

                            if sub_day2 == None:
                                pass

                            else:
                                dfSchedule_collection[schedule_no].loc[dfSchedule.index[x]][j+2]= subject_name


                            dfSchedule_collection[schedule_no].loc[dfSchedule.index[extra_ind]][subject_courseno_ind]=subject_course_no
                            dfSchedule_collection[schedule_no].loc[dfSchedule.index[extra_ind]][subject_name_ind]=subject_name
                            dfSchedule_collection[schedule_no].loc[dfSchedule.index[extra_ind]][prof_ind]=subject_prof
                            #dfSchedule_collection[schedule_no].loc[dfSchedule.index[extra_ind]][uniqueScheduleID_ind]=schedule_no
                            print(extra_ind)
                            extra_ind= extra_ind+1



                            ########################################################################################

                            #Getting the data of last Subject from gsheets
                            for b in range(no_rows_dfSub3):
                                
                                if len(dfSchedule_collection_temp) >= 1:
                                    extra_ind = 5


                                flag= True
                                print("........................Getting data for last subject.................................")
                                print(" ################################################################################")
                                print("here ", no_rows_dfSub3)
                                print("me ",b)

                                subject_name= dfSub3.loc[b][0] 
                                subject_course_no= dfSub3.loc[b][1]
                                print(subject_course_no)
                                subject_day= dfSub3.loc[b][2]

                                if subject_day == 'TR':
                                    sub_day1= "Tuesday"
                                    sub_day2= "Wednesday"
                                
                                elif subject_day== 'MW':
                                    sub_day1= 'Monday'
                                    sub_day2= 'Wednesday'

                                elif subject_day=='M':
                                    sub_day1= 'Monday'
                                    sub_day2= None

                                elif subject_day== 'T':
                                    sub_day1= 'Tuesday'
                                    sub_day2= None

                                elif subject_day== 'W':
                                    sub_day1= 'Wednesday'
                                    sub_day2= None
                                
                                elif subject_day== 'R':
                                    sub_day1= 'Thursday'
                                    sub_day2= None

                                else:
                                    sub_day1= 'Friday'
                                    sub_day2= None

                                subject_time= dfSub3.loc[b][3]   

                                subject_prof= dfSub3.loc[b][4]
                                subject_prof_rating_default = float(dfSub3.loc[b][5])
                                subject_status= dfSub3.loc[b][7]


                                if subject_prof_rating_default >= 4.3 and subject_status== "Open":

                                    for x in range (no_rows_dfSchedule):

                                        #checking if the time of the subject = row of dfschedule
                                        if dfSchedule_collection[schedule_no].index[x] == subject_time:
                                            
                                            for j in range( no_columns_dfschedule):

                                                #checking if the day of the subject = row of dfschedule
                                                if dfSchedule_collection[schedule_no].columns[j]== sub_day1:

                                                    #check if the specific date and time is empty... if "if" condition is True then the cell is empty
                                                    print(dfSchedule_collection[schedule_no].isnull().loc[dfSchedule.index[x]][j] == True)

                                                    if dfSchedule_collection[schedule_no].isnull().loc[dfSchedule.index[x]][j] == True:

                                                        #changing the schedule number (Unique schedule number) because each schedule should have a unique number 
                                                        # it will the sum of the square of classes which have more than one class. in our case it wil be Stat UB 103 and Mult UB 100

                                                        updated_schedule_no= schedule_no + (int(subject_course_no) ** 2)

                                                        print(schedule_no)
                                                        print("yo mama honey singh")
                                                        print(updated_schedule_no)

                                                        #Clons df_collection[scheduleno] into another temp df_collection with new key
                                                        dfSchedule_collection_temp[updated_schedule_no]= dfSchedule_collection[schedule_no].copy(deep=True)



                                                        # adding the MULT-UB class into the schedule
                                                        dfSchedule_collection_temp[updated_schedule_no].loc[dfSchedule.index[x]][j]= subject_name

                                                        if sub_day2 == None:
                                                            pass

                                                        else:
                                                            # adding the MULT-UB class into the schedule
                                                            dfSchedule_collection_temp[updated_schedule_no].loc[dfSchedule.index[x]][j+2]= subject_name

                                                        dfSchedule_collection_temp[updated_schedule_no].loc[dfSchedule.index[extra_ind]][subject_courseno_ind]=subject_course_no
                                                        dfSchedule_collection_temp[updated_schedule_no].loc[dfSchedule.index[extra_ind]][subject_name_ind]=subject_name
                                                        dfSchedule_collection_temp[updated_schedule_no].loc[dfSchedule.index[extra_ind]][prof_ind]=subject_prof
                                                        dfSchedule_collection_temp[updated_schedule_no].loc[dfSchedule.index[extra_ind]][uniqueScheduleID_ind]=updated_schedule_no
                                                        print(extra_ind)
                                                        extra_ind= extra_ind+1
                                                        
                                                        print(extra_ind)
                                                        print('i AM HERE')

                                                        #write the subject schedule into the sheet called "Output" in gsheets
                                                        set_with_dataframe(result_sheet, dfSchedule_collection_temp[updated_schedule_no],row= output_row, include_index= True)
                                                        output_row= output_row + 8

                                                        set_with_dataframe(result_sheet, dfBorder,row= output_row, include_index= True)
                                                        output_row= output_row + 1


                                                        #print(dfSchedule_collection[updated_schedule_no].loc[dfSchedule.index[x]])
                                                        #print(dfSchedule_collection[updated_schedule_no])
                                                        flag= True
                                                        break

                                                    else:
                                                        flag= True
                                                        break

                                                else:
                                                    pass
                                            
                                            # end of For loop
                                            if flag == True:
                                                flag= False
                                                break
                                            
                                        else:
                                            pass

                                    # end of For loop

                                else:
                                    print("ICI ici  yeeeeeee ICI ici")
                                    continue
                        
                                print("je suis ici")
                            
                            # end of For loop
                            flag= True
                            break
                            # innermost DfSub ends here

                            
###########################################                            ##################################################
                        else:
                            flag= True
                            break

                    else:
                        pass

                if flag == True:
                    flag= False
                    break
                
            else:
                print('i am right here HOWDY')
                pass
        
        

