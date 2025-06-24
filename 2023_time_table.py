import datetime as dt
from datetime import timedelta, datetime
import streamlit as st
import json
import pandas as pd

# Page configuration
st.set_page_config(
    page_title="📚 Smart School Organizer",
    page_icon="🎒",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for modern styling
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 10px;
        text-align: center;
        color: white;
        margin-bottom: 2rem;
    }
    
    .card {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        margin: 1rem 0;
        border-left: 4px solid #667eea;
    }
    
    .subject-card {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        padding: 1rem;
        border-radius: 8px;
        margin: 0.5rem 0;
        border-left: 4px solid #4CAF50;
    }
    
    .holiday-card {
        background: linear-gradient(135deg, #ffeaa7 0%, #fab1a0 100%);
        padding: 1.5rem;
        border-radius: 10px;
        text-align: center;
        color: #2d3436;
    }
    
    .bag-item {
        background: #e8f5e8;
        padding: 0.5rem 1rem;
        border-radius: 5px;
        margin: 0.2rem 0;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    
    .bag-item-missing {
        background: #ffe8e8;
        padding: 0.5rem 1rem;
        border-radius: 5px;
        margin: 0.2rem 0;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    
    .stats-container {
        display: flex;
        justify-content: space-around;
        margin: 1rem 0;
    }
    
    .stat-box {
        background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%);
        padding: 1rem;
        border-radius: 8px;
        text-align: center;
        min-width: 120px;
    }
    
    .activity-badge {
        background: #ff6b6b;
        color: white;
        padding: 0.3rem 0.8rem;
        border-radius: 20px;
        font-size: 0.8rem;
        margin-left: 0.5rem;
    }
    
    .uniform-alert {
        background: #fff3cd;
        border: 1px solid #ffeaa7;
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'bag_items' not in st.session_state:
    st.session_state.bag_items = []
if 'last_packed_date' not in st.session_state:
    st.session_state.last_packed_date = None

# Data
time_table = {
    'Monday': ['EVS-1', 'COMPUTER', 'MATHS', 'PT', 'MARATHI', 'ENGLISH', 'HINDI'],
    'Tuesday': ['EVS-1', 'SKATING', 'MATHS', 'DANCE', 'HINDI', 'ART', 'ENGLISH', 'MARATHI'],
    'Wednesday': ['EVS-1', 'COMPUTER', 'MATHS', 'HINDI', 'PT', 'LIBRARY', 'GK', 'ENGLISH'],
    'Thursday': ['MPT', 'ART', 'EVS-2', 'MATHS', 'HINDI', 'MARATHI', 'ENGLISH', 'ROBOTIC'],
    'Friday': ['EVS-2', 'MUSIC', 'MATHS', 'DANCE', 'L&N', 'VE'],
    'Saturday': [],
    'Sunday': []
}

# Common school items that students might need
common_school_items = [
    'Math Book', 'English Book', 'Hindi Book', 'Marathi Book', 'EVS Book', 'Computer Book',
    'GK Book', 'Art Book', 'Music Book', 'Value Education Book', 'Logic Book',
    'Math Notebook', 'English Notebook', 'Hindi Notebook', 'Marathi Notebook', 'EVS Notebook',
    'Computer Notebook', 'GK Notebook', 'Art Notebook', 'Music Notebook', 'General Notebook',
    'Pencil Box', 'Water Bottle', 'Tiffin Box', 'Geometry Box', 'Calculator',
    'Color Pencils', 'Sketch Pens', 'Crayons', 'Eraser', 'Sharpener', 'Scale',
    'Library Card', 'ID Card', 'Homework Diary', 'Time Table', 'Towel',
    'PT Uniform', 'Sports Shoes', 'Dance Shoes', 'Skating Shoes'
]

holiday_list = [
    '2024-08-15', '2024-08-29', '2024-08-30', '2024-09-07', '2024-09-19',
    '2024-09-28', '2024-10-02', '2024-10-24', '2024-11-27', '2025-01-15',
    '2025-01-26', '2025-02-19', '2025-03-08', '2025-03-25', '2025-03-29'
]

def get_tomorrow_info():
    tomorrow = dt.date.today() + dt.timedelta(days=1)
    day_name = tomorrow.strftime('%A')
    return tomorrow, day_name

def is_holiday(date):
    date_str = date.strftime('%Y-%m-%d')
    return date_str in holiday_list

def get_thursday_activity(date):
    first_day = dt.date(date.year, date.month, 1)
    day_offset = (3 - first_day.weekday()) % 7
    first_thursday = first_day + dt.timedelta(days=day_offset)
    
    weeks_diff = (date - first_thursday).days // 7
    week_number = weeks_diff + 1
    
    if week_number in [1, 3]:
        return 'Skating Day'
    elif week_number in [2, 4]:
        return 'Self-Defense Day'
    return ''

def get_subjects_for_day(day):
    return time_table.get(day, [])

def display_main_header():
    st.markdown("""
    <div class="main-header">
        <h1>📚 Smart School Bag Organizer - Class 4B</h1>
        <p>Your intelligent timetable and bag packing assistant</p>
    </div>
    """, unsafe_allow_html=True)

def display_timetable():
    st.header("📅 Tomorrow's Schedule")
    
    tomorrow, day_name = get_tomorrow_info()
    
    if is_holiday(tomorrow):
        st.markdown("""
        <div class="holiday-card">
            <h2>🎉 Tomorrow is a Holiday! 🎉</h2>
            <p>Enjoy your day off!</p>
        </div>
        """, unsafe_allow_html=True)
        return
    
    subjects = time_table.get(day_name, [])
    
    if not subjects:
        st.markdown("""
        <div class="holiday-card">
            <h2>🎉 No classes tomorrow! 🎉</h2>
            <p>It's a weekend - time to relax!</p>
        </div>
        """, unsafe_allow_html=True)
        return
    
    # Display date and day info
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f"""
        <div class="stat-box">
            <h3>{tomorrow.strftime('%d')}</h3>
            <p>{tomorrow.strftime('%B')}</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="stat-box">
            <h3>{day_name}</h3>
            <p>Tomorrow</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="stat-box">
            <h3>{len(subjects)}</h3>
            <p>Periods</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Display subjects
    st.subheader(f"📖 Subjects for {day_name}")
    
    for i, subject in enumerate(subjects, 1):
        activity_badge = ""
        if day_name == 'Thursday' and subject in ['MPT', 'PT']:
            activity = get_thursday_activity(tomorrow)
            if activity:
                activity_badge = f'<span class="activity-badge">{activity}</span>'
        
        st.markdown(f"""
        <div class="subject-card">
            <strong>Period {i}:</strong> {subject} {activity_badge}
        </div>
        """, unsafe_allow_html=True)
    
    # Uniform alerts
    if day_name == 'Tuesday' or (day_name == 'Thursday' and any(s in subjects for s in ['MPT', 'PT'])):
        st.markdown("""
        <div class="uniform-alert">
            <strong>👕 Uniform Reminder:</strong> Don't forget to wear PT uniform tomorrow!
        </div>
        """, unsafe_allow_html=True)

def display_bag_organizer():
    st.header("🎒 Smart Bag Organizer")
    
    tomorrow, day_name = get_tomorrow_info()
    
    if is_holiday(tomorrow) or not time_table.get(day_name):
        st.info("No need to pack bag - tomorrow is a holiday! 🎉")
        return
    
    tomorrow_subjects = get_subjects_for_day(day_name)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📚 Tomorrow's Subjects")
        
        # Display tomorrow's subjects
        if tomorrow_subjects:
            for i, subject in enumerate(tomorrow_subjects, 1):
                st.markdown(f"""
                <div class="subject-card">
                    <strong>Period {i}:</strong> {subject}
                </div>
                """, unsafe_allow_html=True)
        
        st.markdown("---")
        st.subheader("➕ Add Items to Bag")
        
        # Add items to bag using selectbox or multiselect
        available_items = [item for item in common_school_items if item not in st.session_state.bag_items]
        
        if available_items:
            selected_item = st.selectbox("Choose an item to add:", ["Select an item..."] + available_items)
            
            if selected_item != "Select an item..." and st.button("Add to Bag"):
                st.session_state.bag_items.append(selected_item)
                st.success(f"Added {selected_item} to bag!")
                st.rerun()
        else:
            st.info("All common items are already in your bag!")
        
        # Quick add buttons for common daily items
        st.write("**Quick Add:**")
        quick_items = ['Water Bottle', 'Tiffin Box', 'Pencil Box', 'Homework Diary', 'ID Card']
        
        cols = st.columns(3)
        for i, item in enumerate(quick_items):
            with cols[i % 3]:
                if item not in st.session_state.bag_items:
                    if st.button(f"➕ {item}", key=f"quick_{item}"):
                        st.session_state.bag_items.append(item)
                        st.success(f"Added {item}!")
                        st.rerun()
    
    with col2:
        st.subheader("🎒 Items in Your Bag")
        
        if st.session_state.bag_items:
            for item in st.session_state.bag_items:
                col_item, col_btn = st.columns([4, 1])
                with col_item:
                    st.markdown(f"""
                    <div class="bag-item">
                        <span>✅ {item}</span>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col_btn:
                    if st.button("🗑️", key=f"remove_{item}"):
                        st.session_state.bag_items.remove(item)
                        st.success(f"Removed {item}")
                        st.rerun()
        else:
            st.info("Your bag is empty. Start adding items!")
        
        # Bag status
        st.markdown(f"""
        <div class="card">
            <h4>📊 Bag Status</h4>
            <p><strong>Total Items in Bag:</strong> {len(st.session_state.bag_items)}</p>
            <p><strong>Subjects Tomorrow:</strong> {len(tomorrow_subjects)}</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Clear bag button
        if st.session_state.bag_items:
            if st.button("🗑️ Clear Entire Bag", type="secondary"):
                st.session_state.bag_items = []
                st.success("Bag cleared!")
                st.rerun()
        
        # Custom item input
        st.markdown("---")
        st.write("**Add Custom Item:**")
        custom_item = st.text_input("Enter item name:", placeholder="e.g., Special notebook")
        if custom_item and st.button("Add Custom Item"):
            if custom_item not in st.session_state.bag_items:
                st.session_state.bag_items.append(custom_item)
                st.success(f"Added {custom_item} to bag!")
                st.rerun()
            else:
                st.warning("Item already in bag!")

def display_weekly_view():
    st.header("📊 Weekly Overview")
    
    # Create a DataFrame for better visualization
    weekly_data = []
    for day, subjects in time_table.items():
        weekly_data.append({
            'Day': day,
            'Periods': len(subjects),
            'Subjects': ', '.join(subjects) if subjects else 'Holiday'
        })
    
    df = pd.DataFrame(weekly_data)
    st.dataframe(df, use_container_width=True)
    
    # Subject frequency chart
    st.subheader("📈 Subject Frequency")
    subject_count = {}
    for subjects in time_table.values():
        for subject in subjects:
            subject_count[subject] = subject_count.get(subject, 0) + 1
    
    if subject_count:
        st.bar_chart(subject_count)

def display_query_interface():
    st.header("🤔 Ask Me Anything")
    
    with st.container():
        query = st.text_input("Which day's timetable do you need?", placeholder="e.g., Monday, Tuesday...")
        
        if query:
            day = query.strip().title()
            if day in time_table:
                subjects = time_table[day]
                if subjects:
                    st.success(f"📅 Timetable for {day}:")
                    
                    # Display as a nice table
                    periods_data = []
                    for i, subject in enumerate(subjects, 1):
                        periods_data.append({'Period': i, 'Subject': subject})
                    
                    df = pd.DataFrame(periods_data)
                    st.table(df)
                    
                else:
                    st.info(f"🎉 {day} is a holiday!")
            else:
                st.error("❌ Please enter a valid day name (Monday to Sunday)")

def main():
    display_main_header()
    
    # Sidebar navigation
    st.sidebar.title("🧭 Navigation")
    page = st.sidebar.radio(
        "Go to:",
        ["📅 Tomorrow's Schedule", "🎒 Bag Organizer", "📊 Weekly View", "🤔 Ask Me"]
    )
    
    # Display current date and time
    st.sidebar.markdown("---")
    st.sidebar.markdown(f"📅 **Today:** {dt.date.today().strftime('%A, %B %d, %Y')}")
    
    st.sidebar.markdown(f"🕐 **Time:** {(dt.datetime.now() + timedelta(hours=5, minutes=30)).strftime('%I:%M %p')}")
    
    # Quick stats
    tomorrow, day_name = get_tomorrow_info()
    tomorrow_subjects = time_table.get(day_name, [])
    st.sidebar.markdown(f"📚 **Tomorrow:** {len(tomorrow_subjects)} periods")
    
    # Display selected page
    if page == "📅 Today's Schedule":
        display_timetable()
    elif page == "🎒 Bag Organizer":
        display_bag_organizer()
    elif page == "📊 Weekly View":
        display_weekly_view()
    elif page == "🤔 Ask Me":
        display_query_interface()
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #666; margin-top: 2rem;">
        <p>📚 Smart School Organizer - Class 4B | Last Updated: June 24, 2025</p>
        <p>Made with ❤️ for smart students</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == '__main__':
    main()
