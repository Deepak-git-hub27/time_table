import datetime as dt
from datetime import timedelta
import streamlit as st

today=dt.date.today()+dt.timedelta(days=1)
day=today.strftime('%A')

st.title(f"Your School 2nd B Time table for {day}")

time_table= {'Monday':['Computer','Hindi','CCA','English','Marathi','EVS','Maths'],
             'Tuesday':['P.T','Hindi','English','Lib','Maths','EVS'],
             'Wednesday':['Computer','English','CCA','English','P.T','EVS','Maths'],
             'Thursday':['G.K','Maths','English','Activity','Hindi','EVS','ART'],
             'Friday':['VEDU','Hindi','Marathi','Music','Maths','P.T'],
             'Saturday':['Holiday'],
             'Sunday':['Holiday'],
             
            }
def get_time_table(time_table1):
    
   # today=dt.date.today()+dt.timedelta(days=1)
   # day=today.strftime('%A')
    result=time_table1[day]
    
    st.write('Total',str(len(result)),'periods.')
   
    st.table(result)  
    for sub in result:        
        if sub=='English':
            st.write("Tomorrow is english period kindly carry colors.")
    if day=='Tuesday'or'Thursday':
        st.write("Kindly wear PT uniform.")
             
    st.write("Note:-Last update 14th Aug'23") 


get_time_table(time_table)

