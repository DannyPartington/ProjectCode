# -*- coding: utf-8 -*-
"""
Created on Mon May  6 16:59:20 2019

@author: Daniel
"""
#import library for reading Excel files
import pandas as pd
#import Library for arrays
import numpy as np
#import datetime for time arithemtic
import datetime

#function to calculate minutes between start and endtime
def timediff(start, end):
    
    start_H = (start.strftime("%H"))
    start_M = (start.strftime("%M"))
    start_S = (start.strftime("%S"))

    end_H = (end.strftime("%H"))
    end_M = (end.strftime("%M"))
    end_S = (end.strftime("%S"))
    
    diff = 60*(int(end_H) - int(start_H))
    diff = 60*(diff + (int(end_M) - int(start_M)))
    diff = diff + (int(end_S) - int(start_S))

    return(diff)


#Robustness function, calculating t-robustness
def Robustness(MinTime, SchedTime, t):
    if (len(MinTime) != len(SchedTime)):
        return 'ERROR, different list sizes'
    NumberOfDelays = 0
    for i in range(len(MinTime)):
        difference = int(SchedTime[i]) - int(MinTime[i])
        if ((difference - t) < 0):
            NumberOfDelays += 1
    percent_OfTrains = (len(SchedTime) - NumberOfDelays)/len(SchedTime) * 100
    return percent_OfTrains


#Feasibility function
def Feasibility(TPR, SPR, CrossingMatrix):
    
    return (realisable(TPR, SPR), Conflicts(CrossingMatrix) )
    

#Condition 2 of Feasibility
def Conflicts(CrossingMatrix):
    return 3
    
#COndition 1 of Feasibility
def realisable(TPR, SPR):
    
    if (len(TPR) != len(SPR)):
        return 'ERROR, different list sizes'
    PDList = []
    infeasible = 0
    for i in range(len(TPR)):
        difference = SPR[i] - TPR[i]
        if difference < 0:
            infeasible = 1
        percentage_diff = (difference/((SPR[i]))*100)
        PDList.append(percentage_diff)

    total = 0
    for j in range(len(PDList)):
        total = total + PDList[j]
    Average_PD =total/len(PDList)
    
    if infeasible > 0:
        return ['INFEASIBLE', Average_PD]
    return['FEASIBLE', Average_PD] 







#read in the C2C May17 timetable data and select the relevant collumns 
data = pd.read_excel(r'C:\Users\Daniel\Desktop\Project\CODE\C2C_May17v2.xlsx')
df = pd.DataFrame(data, columns = ['Location','From','To','MRTech [s]','SchedRT [s]', 'OccTime to','Train', 'MinDw [s]'])

#collect list of stations on the route between Fenchurch and Barking
FEN_BAR_Stations = ['BARKING','EHMEMUD','WHAMHL','GASFCTJ','GASFLP','LIMHSE','CRISTSJ','FENCHRS']

#convert the data into array form for manipulation
Feas_Data = df.values


#Code for running same methods on timetable with 10% less trains

#read out from Excel file containing Trains ran and store in a list 
UIC_List = pd.read_excel(r'C:\Users\Daniel\Desktop\Project\CODE\UIC406 - May17 SX - Limehouse to West Ham HL.xlsx')
TrainList = pd.DataFrame(UIC_List, columns = ['Train'])
TrainList = TrainList.values
TrainList = TrainList.tolist()


UIC_10Less_List = pd.read_excel(r'C:\Users\Daniel\Desktop\Project\CODE\UIC406 - May17 SX with 10% less trains - Limehouse to West Ham HL.xlsx')
Train_10Less_List = pd.DataFrame(UIC_10Less_List, columns = ['Train'])
Train_10Less_List = Train_10Less_List.values
Train_10Less_List = Train_10Less_List.tolist()






#create a list to store the train ID's of those taken out for the 10% less timetable
Trains_Taken_Out = []

#Compare trains in each simulation and add taken out ones into a list
for i in range(len(TrainList)):
    Match = False
    for j in range(len(Train_10Less_List)):
        if (TrainList[i] == Train_10Less_List[j]):
            Match = True
    if (Match == False):
        Trains_Taken_Out.append(str(TrainList[i]))
        
        
 
#Create Lists to store technical/scheduled times for different time periods in day
TechTime8_10 = []
SchedTime8_10 = []

TechTime10_4 = []
SchedTime10_4 = []

TechTime5_7 = []
SchedTime5_7 = []

TechTime24hr = []
SchedTime24hr = []

#Same again, but for trains that weren't taken out for the simulator with 10% less trains
Ten_Less_TechTime8_10 = []
Ten_Less_SchedTime8_10 = []

Ten_Less_TechTime10_4 = []
Ten_Less_SchedTime10_4 = []

Ten_Less_TechTime5_7 = []
Ten_Less_SchedTime5_7 = []

Ten_Less_TechTime24hr = []
Ten_Less_SchedTime24hr = []


#Lists to store total MinJourney & total sched times
SchedJourneyTimes = []
MinJourneyTimes = []

SchedJourneyTimes8_10 = []
MinJourneyTimes8_10 = []

SchedJourneyTimes10_4 = []
MinJourneyTimes10_4 = []

SchedJourneyTimes5_7 = []
MinJourneyTimes5_7 = []


Ten_Less_SchedJourneyTimes = []
Ten_Less_MinJourneyTimes = []

Ten_Less_SchedJourneyTimes8_10 = []
Ten_Less_MinJourneyTimes8_10 = []

Ten_Less_SchedJourneyTimes10_4 = []
Ten_Less_MinJourneyTimes10_4 = []

Ten_Less_SchedJourneyTimes5_7 = []
Ten_Less_MinJourneyTimes5_7 = []

#set an upper bound on time journeys to avoid amalgated trains contributing.
amalgamation = 1100

#A list to add ID's into so that we dont check same train journey twice
TrainsChecked = []

for i in range(Feas_Data.shape[0]):
    
    #Check if Train was taken out in 10% less simulation, if so, set Indicator to true
    TakenOut = False
    for t in range(len(Trains_Taken_Out)):
        if (str(Feas_Data[i][6]) in str(Trains_Taken_Out[t])):
            TakenOut = True
    
    #make sure the train looked at is a train travelling between SHoeburyness and Fenchurch St
    if( (Feas_Data[i][1] == 'SHBRYNS' and Feas_Data[i][2] == 'FENCHRS') or (Feas_Data[i][1] == 'FENCHRS' and Feas_Data[i][2] == 'SHBRYNS' )):
        if(Feas_Data[i][0] in FEN_BAR_Stations):
            
            
            if(Feas_Data[i][1] == 'SHBRYNS' and Feas_Data[i][2] == 'FENCHRS' and (Feas_Data[i][6] not in TrainsChecked)):
                
                j = i
                JourneyFin = False
                MinTimeTotal = 0
                
                
                #calculate technical and sheduled time for trains going from BARKING - FENCHURCH
                while(JourneyFin == False):
                    if(Feas_Data[j][0] == 'BARKING'):
                        StartTime = Feas_Data[j][5]
                    if (np.isnan(Feas_Data[j][3]) == False):
                        MinTimeTotal = MinTimeTotal + Feas_Data[j][3]
                        if(np.isnan(Feas_Data[j][7]) == False):
                             MinTimeTotal = MinTimeTotal+ int(Feas_Data[j][7])
                    if(Feas_Data[j][0] == 'FENCHRS'):
                        Endtime = Feas_Data[j][5]
                        JourneyFin = True
                    j = j+1
                JourneySchedTime = timediff(StartTime, Endtime)
                
                #only consider trains not going through amalgamation
                if(JourneySchedTime < amalgamation): 
                    
                    #add sched n tech times to list
                    MinJourneyTimes.append(MinTimeTotal)
                    SchedJourneyTimes.append(JourneySchedTime)
                    TrainsChecked.append(Feas_Data[i][6])
                    if(TakenOut == False):
                        Ten_Less_MinJourneyTimes.append(MinTimeTotal)
                        Ten_Less_SchedJourneyTimes.append(JourneySchedTime)
                        
                    
                    #add in tech and sched times to their correct time duration list    
                    if(isinstance(Feas_Data[i][5], datetime.time) == True):
                        if(datetime.time(8, 0, 0)<= Feas_Data[i][5] <= datetime.time(10, 0, 0)):
                            MinJourneyTimes8_10.append(MinTimeTotal)
                            SchedJourneyTimes8_10.append(JourneySchedTime)
                            #add to additional lists if the train wasnt removed for 10% less run
                            if (TakenOut == False):
                                Ten_Less_MinJourneyTimes8_10.append(MinTimeTotal)
                                Ten_Less_SchedJourneyTimes8_10.append(JourneySchedTime)
                            
                        if(datetime.time(10, 0, 0)<= Feas_Data[i][5] <= datetime.time(16, 0, 0)):
                            MinJourneyTimes10_4.append(MinTimeTotal)
                            SchedJourneyTimes10_4.append(JourneySchedTime)
                            #add to additional lists if the train wasnt removed for 10% less run
                            if(TakenOut == False):
                                Ten_Less_MinJourneyTimes10_4.append(MinTimeTotal)
                                Ten_Less_SchedJourneyTimes10_4.append(JourneySchedTime)
                            
                        if(datetime.time(17, 0, 0)<= Feas_Data[i][5] <= datetime.time(19, 0, 0)):
                            MinJourneyTimes5_7.append(MinTimeTotal)
                            SchedJourneyTimes5_7.append(JourneySchedTime)
                            #add to additional lists if the train wasnt removed for 10% less run
                            if(TakenOut == False):
                                Ten_Less_MinJourneyTimes5_7.append(MinTimeTotal)
                                Ten_Less_SchedJourneyTimes5_7.append(JourneySchedTime)
             
                                
            #calculate technical and sheduled time for trains going from FENCHURCH - BARKING
            if(Feas_Data[i][1] == 'FENCHRS' and Feas_Data[i][2] == 'SHBRYNS'):

                if not(str(Feas_Data[i][6]) in TrainsChecked):
                
                    j = i
                    JourneyFin = False
                    MinTimeTotal = 0
                    
                     #calculate technical and sheduled time for trains going from FENCHURCH - BARKING
                    while(JourneyFin == False):
                        if(Feas_Data[j][0] == 'FENCHRS'):
                            StartTime = Feas_Data[j][5]
                        if (np.isnan(Feas_Data[j][3]) == False):
                            MinTimeTotal = MinTimeTotal + Feas_Data[j][3]
                            if(np.isnan(Feas_Data[j][7]) == False):
                                 MinTimeTotal = MinTimeTotal+ int(Feas_Data[j][7])
                        if(Feas_Data[j][0] == 'BARKING'):
                            Endtime = Feas_Data[j][5]
                            JourneyFin = True
                        j = j+1
                    MinJourneyTimes.append(MinTimeTotal)
                    JourneySchedTime = timediff(StartTime, Endtime)

                    SchedJourneyTimes.append(JourneySchedTime)
                    TrainsChecked.append(Feas_Data[i][6])
                     #add to additional lists if the train wasnt removed for 10% less run
                    if(TakenOut == False):
                        Ten_Less_MinJourneyTimes.append(MinTimeTotal)
                        Ten_Less_SchedJourneyTimes.append(JourneySchedTime)
                    
                    #add in tech and sched times to their correct time duration list 
                    if(isinstance(Feas_Data[i][5], datetime.time) == True):
                        if(datetime.time(8, 0, 0)<= Feas_Data[i][5] <= datetime.time(10, 0, 0)):
                            MinJourneyTimes8_10.append(MinTimeTotal)
                            SchedJourneyTimes8_10.append(JourneySchedTime)
                             #add to additional lists if the train wasnt removed for 10% less run
                            if(TakenOut == False):
                                Ten_Less_MinJourneyTimes8_10.append(MinTimeTotal)
                                Ten_Less_SchedJourneyTimes8_10.append(JourneySchedTime)
                                
                        if(datetime.time(10, 0, 0)<= Feas_Data[i][5] <= datetime.time(16, 0, 0)):
                            MinJourneyTimes10_4.append(MinTimeTotal)
                            SchedJourneyTimes10_4.append(JourneySchedTime)
                             #add to additional lists if the train wasnt removed for 10% less run
                            if(TakenOut == False):
                                Ten_Less_MinJourneyTimes10_4.append(MinTimeTotal)
                                Ten_Less_SchedJourneyTimes10_4.append(JourneySchedTime)
                                
                        if(datetime.time(17, 0, 0)<= Feas_Data[i][5] <= datetime.time(19, 0, 0)):
                            MinJourneyTimes5_7.append(MinTimeTotal)
                            SchedJourneyTimes5_7.append(JourneySchedTime)
                             #add to additional lists if the train wasnt removed for 10% less run
                            if(TakenOut == False):
                                Ten_Less_MinJourneyTimes5_7.append(MinTimeTotal)
                                Ten_Less_SchedJourneyTimes5_7.append(JourneySchedTime)





#printout all results directly from outputs of functions
print('Robustness Results:')        
print('All day, t = 30:',Robustness(MinJourneyTimes,SchedJourneyTimes, 30))
print('All day, t = 60:',Robustness(MinJourneyTimes,SchedJourneyTimes, 60))
print('All day, t = 90:',Robustness(MinJourneyTimes,SchedJourneyTimes, 90))
print('All day, t = 120:',Robustness(MinJourneyTimes,SchedJourneyTimes, 120))

#new line
print('')
print('8-10, t = 30:',Robustness(MinJourneyTimes8_10,SchedJourneyTimes8_10, 30))
print('8-10, t = 60:',Robustness(MinJourneyTimes8_10,SchedJourneyTimes8_10, 60))
print('8-10, t = 90:',Robustness(MinJourneyTimes8_10,SchedJourneyTimes8_10, 90))
print('8-10, t = 120:',Robustness(MinJourneyTimes8_10,SchedJourneyTimes8_10, 120))

#new line
print('')
print('10-4, t = 30:',Robustness(MinJourneyTimes10_4,SchedJourneyTimes10_4, 30))
print('10-4, t = 60:',Robustness(MinJourneyTimes10_4,SchedJourneyTimes10_4, 60))
print('10-4, t = 90:',Robustness(MinJourneyTimes10_4,SchedJourneyTimes10_4, 90))
print('10-4, t = 120:',Robustness(MinJourneyTimes10_4,SchedJourneyTimes10_4, 120))

#new line
print('')
print('5-7, t = 30:',Robustness(MinJourneyTimes5_7,SchedJourneyTimes5_7, 30))
print('5-7, t = 60:',Robustness(MinJourneyTimes5_7,SchedJourneyTimes5_7, 60))
print('5-7, t = 90:',Robustness(MinJourneyTimes5_7,SchedJourneyTimes5_7, 90))
print('5-7, t = 120:',Robustness(MinJourneyTimes5_7,SchedJourneyTimes5_7, 120))





print('')
print('Robustness Results for 10% less trains:')
print('All day, t = 30:',Robustness(Ten_Less_MinJourneyTimes,Ten_Less_SchedJourneyTimes, 30))
print('All day, t = 60:',Robustness(Ten_Less_MinJourneyTimes,Ten_Less_SchedJourneyTimes, 60))
print('All day, t = 90:',Robustness(Ten_Less_MinJourneyTimes,Ten_Less_SchedJourneyTimes, 90))
print('All day, t = 120:',Robustness(Ten_Less_MinJourneyTimes,Ten_Less_SchedJourneyTimes, 120))

#new line
print('')
print('8-10, t = 30:',Robustness(Ten_Less_MinJourneyTimes8_10,Ten_Less_SchedJourneyTimes8_10, 30))
print('8-10, t = 60:',Robustness(Ten_Less_MinJourneyTimes8_10,Ten_Less_SchedJourneyTimes8_10, 60))
print('8-10, t = 90:',Robustness(Ten_Less_MinJourneyTimes8_10,Ten_Less_SchedJourneyTimes8_10, 90))
print('8-10, t = 120:',Robustness(Ten_Less_MinJourneyTimes8_10,Ten_Less_SchedJourneyTimes8_10, 120))

#new line
print('')
print('10-4, t = 30:',Robustness(Ten_Less_MinJourneyTimes10_4,Ten_Less_SchedJourneyTimes10_4, 30))
print('10-4, t = 60:',Robustness(Ten_Less_MinJourneyTimes10_4,Ten_Less_SchedJourneyTimes10_4, 60))
print('10-4, t = 90:',Robustness(Ten_Less_MinJourneyTimes10_4,Ten_Less_SchedJourneyTimes10_4, 90))
print('10-4, t = 120:',Robustness(Ten_Less_MinJourneyTimes10_4,Ten_Less_SchedJourneyTimes10_4, 120))

#new line
print('')
print('5-7, t = 30:',Robustness(Ten_Less_MinJourneyTimes5_7,Ten_Less_SchedJourneyTimes5_7, 30))
print('5-7, t = 60:',Robustness(Ten_Less_MinJourneyTimes5_7,Ten_Less_SchedJourneyTimes5_7, 60))
print('5-7, t = 90:',Robustness(Ten_Less_MinJourneyTimes5_7,Ten_Less_SchedJourneyTimes5_7, 90))
print('5-7, t = 120:',Robustness(Ten_Less_MinJourneyTimes5_7,Ten_Less_SchedJourneyTimes5_7, 120))


print('24 hour feasibility results:')    
print(realisable(MinJourneyTimes,SchedJourneyTimes))

#new line
print('')
print('8-10 feasibility results:') 
print(realisable(MinJourneyTimes8_10,SchedJourneyTimes8_10))

#new line
print('')
print('10-4 feasibility results:') 
print(realisable(MinJourneyTimes10_4,SchedJourneyTimes10_4))

#new line
print('')
print('5-7 feasibility results:') 
print(realisable(MinJourneyTimes5_7,SchedJourneyTimes5_7))



print('')
print('10 Percent Less')
print('24 hour feasibility results:')    
print(realisable(Ten_Less_MinJourneyTimes,Ten_Less_SchedJourneyTimes))

#new line
print('')
print('8-10 feasibility results:') 
print(realisable(Ten_Less_MinJourneyTimes8_10,Ten_Less_SchedJourneyTimes8_10))

#new line
print('')
print('10-4 feasibility results:') 
print(realisable(Ten_Less_MinJourneyTimes10_4,Ten_Less_SchedJourneyTimes10_4))

#new line
print('')
print('5-7 feasibility results:') 
print(realisable(Ten_Less_MinJourneyTimes5_7,Ten_Less_SchedJourneyTimes5_7))







    
