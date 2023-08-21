import datetime as dt
from datetime import timedelta,datetime
import streamlit as st
col1, col2 = st.columns(2)
today=dt.date.today()+dt.timedelta(days=1)

day=today.strftime('%A')

hide = """
    <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
    </style>
"""
st.markdown(hide, unsafe_allow_html=True)


st.header(f"2nd B Time table for {day}")

time_table= {'Monday':['Computer','Hindi','CCA','English','Marathi','EVS','Maths'],
             'Tuesday':['Mass P.T','Hindi','English','Lib','Maths','EVS'],
             'Wednesday':['Computer','English','CCA','P.T','EVS','Maths'],
             'Thursday':['G.K','Maths','English','Activity','Hindi','EVS','ART'],
             'Friday':['VEDU','Hindi','Marathi','Music','Maths','P.T'],
             'Saturday':[],
             'Sunday':[]

            }


holiday_list=['2023-8-15','2023-8-29','2023-8-30','2023-9-07','2023-9-19','2023-9-28','2023-10-02','2023-10-24','2023-11-27','2024-1-15','2024-1-26','2024-2-19','2024-3-08','2024-3-25','2024-3-29']


with col1:
    def check_holiday():
        
        for holiday in holiday_list:
            
            if dt.date.today()+dt.timedelta(days=1)==datetime.strptime(holiday, '%Y-%m-%d').date():
                
              
                st.markdown('**_Tomorrow is Holiday_**.')
                break
            
            else:
                
                get_time_table(time_table)
                break
with col1:
    def activity_check():
        #today=dt.date.today()+dt.timedelta(days=1)
    
        first_day = dt.date(dt.date.today().year,dt.date.today().month, 1)
    
        day_offset = (3 - first_day.weekday()) % 7
        first_thursday = first_day + dt.timedelta(days=day_offset)
        third_thursday = first_thursday + dt.timedelta(weeks=2)
    
    
        second_thursday = first_thursday + dt.timedelta(days=7)
        fourth_thursday = third_thursday + dt.timedelta(days=7)
    
        if today==first_thursday or today==third_thursday:
            return'& its Sketing day.'
        elif today==second_thursday or today==fourth_thursday:
            return'& its Self-defense day.'
        else:
            return""
with col1:
    def get_time_table(time_table1):
            
    
            result=time_table1[day]
            if len(result)>=2:
                st.write('Total',str(len(result)),'periods.')
            else:
                   st.write('Tomorrow is holiday')
            st.table(result)  
            for sub in result:        
                if sub=='English':
                    st.write("Tomorrow is english period kindly carry colors.")
            if day=='Tuesday':
                st.write("Kindly wear PT uniform.")
            elif day=='Thursday':
                st.write(f"Kindly wear PT uniform  {activity_check()}")
                     
            st.write("Note:-Last update 14th Aug'23") 
with col2:
    def askme():
    
            st.title("Ask Me")
    
            prompt = st.chat_input("Which day's timetable do you need?")
    
            if prompt:
                prompt=prompt.title()
                if prompt in 'Monday':
                    st.write('Time table for Monday') 
                    st.table(time_table['Monday'])
                elif prompt in 'Tuesday':
                    st.write('Time table for Tuesday')
                    st.table(time_table['Tuesday'])
                elif prompt in 'Wednesday':
                    st.write('Time table for Wednesday')
                    st.table(time_table['Wednesday'])    
        
                elif prompt in 'Thursday':
                    st.write('Time table for Thursday')
                    st.table(time_table['Thursday'])
                elif prompt in 'Friday':
                    st.write('Time table for Friday')
                    st.table(time_table['Friday'])
                elif prompt in 'Saturday':
                    st.write("It's Holiday")
                elif prompt in 'Sunday':
                    st.write("It's Holiday")
                  
                
                else:
                    st.write('You written wrong day name')
               
if __name__ == '__main__':
    with col1:
        check_holiday()
    with col2:
        askme()

   
