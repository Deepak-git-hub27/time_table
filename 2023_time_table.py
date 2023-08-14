#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import datetime as dt
from datetime import timedelta
import streamlit as st

st.write("Your School Time table")

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
    st.write(day + ' time table total',len(result),'periods.')
    
    return result
    st.write('If english period then carry colors')
    
    
get_time_table(time_table)

