import datetime as dt
from datetime import timedelta,datetime
import streamlit as st

today=dt.date.today()+dt.timedelta(days=1)
day=today.strftime('%A')
hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True) 

st.header(f"2nd B Time table for {day}")

time_table= {'Monday':['Computer','Hindi','CCA','English','Marathi','EVS','Maths'],
             'Tuesday':['P.T','Hindi','English','Lib','Maths','EVS'],
             'Wednesday':['Computer','English','CCA','P.T','EVS','Maths'],
             'Thursday':['G.K','Maths','English','Activity','Hindi','EVS','ART'],
             'Friday':['VEDU','Hindi','Marathi','Music','Maths','P.T'],
             'Saturday':['Holiday'],
             'Sunday':['Holiday'],
             

            }


holiday_list=['2023-8-15','2023-8-29','2023-8-30','2023-9-07','2023-9-19','2023-9-28','2023-10-02','2023-10-24','2023-11-27','2024-1-15','2024-1-26','2024-2-19','2024-3-08','2024-3-25','2024-3-29']
    
def check_holiday():
    
    for holiday in holiday_list:
        
        if dt.date.today()+dt.timedelta(days=1)==datetime.strptime(holiday, '%Y-%m-%d').date():
            
          
            st.markdown('**_Tomorrow is Holiday_**.')
            break
        
        else:
            
            get_time_table(time_table)
            break
    
def get_time_table(time_table1):
    

    result=time_table1[day]
    
    st.write('Total',str(len(result)),'periods.')
   
    st.table(result)  
    for sub in result:        
        if sub=='English':
            st.write("Tomorrow is english period kindly carry colors.")
    if day=='Tuesday':
        st.write("Kindly wear PT uniform.")
    elif day=='Thursday':
        st.write("Kindly wear PT uniform.")
             
    st.write("Note:-Last update 14th Aug'23") 


if __name__ == '__main__':
    
    check_holiday()
    
