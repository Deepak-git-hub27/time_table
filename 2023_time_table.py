#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import datetime as dt
from datetime importhttp://localhost:8888/notebooks/2023_time_table.ipynb# timedelta
time_table= {'Monday':['Computer','Hindi','CCA','English','Marathi','EVS','Maths'],
             'Tuesday':['P.T','Hindi','English','Lib','Maths','EVS'],
             'Wednesday':['Computer','English','CCA','English','P.T','EVS','Maths'],
             'Thursday':['G.K','Maths','English','Activity','Hindi','EVS','ART'],
             'Friday':['VEDU','Hindi','Marathi','Music','Maths','P.T'],
             'Saturday':['Holiday'],
             'Sunday':['Holiday'],
             
            }

def get_time_table(time_table):
    
    today=dt.date.today()+dt.timedelta(days=1)
    day=today.strftime('%A')
    result=time_table[day]
    print(day + ' time table total',len(result),'periods.')
    
    return result
    print('If english period then carry colors')
    
    
get_time_table()

