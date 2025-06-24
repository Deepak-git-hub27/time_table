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

# Custom CSS for mobile-optimized styling with dark/light theme compatibility
st.markdown("""
<style>
    /* Mobile-first design with compact cards */
    .main-header {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        padding: 1rem;
        border-radius: 8px;
        text-align: center;
        color: white;
        margin-bottom: 1rem;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.3);
    }
    
    .main-header h1 {
        font-size: 1.2rem;
        margin-bottom: 0.5rem;
    }
    
    .main-header p {
        font-size: 0.9rem;
        margin: 0;
    }
    
    .card {
        background: rgba(255, 255, 255, 0.95);
        color: #333;
        padding: 0.8rem;
        border-radius: 6px;
        box-shadow: 0 2px 6px rgba(0, 0, 0, 0.15);
        margin: 0.5rem 0;
        border: 1px solid #667eea;
        backdrop-filter: blur(10px);
        font-size: 0.9rem;
    }
    
    /* Dark theme support */
    [data-theme="dark"] .card,
    .stApp[data-theme="dark"] .card {
        background: rgba(50, 50, 50, 0.95);
        color: #ffffff;
        border: 1px solid #8a9bff;
    }
    
    .subject-card {
        background: rgba(245, 247, 250, 0.95);
        color: #2c3e50;
        padding: 0.6rem;
        border-radius: 6px;
        margin: 0.3rem 0;
        border: 1px solid #4CAF50;
        font-weight: 500;
        box-shadow: 0 1px 4px rgba(0, 0, 0, 0.1);
        font-size: 0.85rem;
    }
    
    /* Dark theme for subject cards */
    [data-theme="dark"] .subject-card,
    .stApp[data-theme="dark"] .subject-card {
        background: rgba(70, 70, 70, 0.95);
        color: #ffffff;
        border: 1px solid #66bb6a;
    }
    
    .holiday-card {
        background: linear-gradient(135deg, #ffeaa7 0%, #fab1a0 100%);
        padding: 1rem;
        border-radius: 8px;
        text-align: center;
        color: #2d3436;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
        border: 1px solid #fdcb6e;
        margin: 0.5rem 0;
    }
    
    .holiday-card h2 {
        font-size: 1.3rem;
        margin-bottom: 0.5rem;
    }
    
    .bag-item {
        background: rgba(232, 245, 232, 0.95);
        color: #2e7d32;
        padding: 0.5rem 0.7rem;
        border-radius: 6px;
        margin: 0.2rem 0;
        display: flex;
        justify-content: space-between;
        align-items: center;
        border: 1px solid #4caf50;
        font-weight: 500;
        font-size: 0.85rem;
    }
    
    /* Dark theme for bag items */
    [data-theme="dark"] .bag-item,
    .stApp[data-theme="dark"] .bag-item {
        background: rgba(46, 125, 50, 0.3);
        color: #c8e6c9;
        border: 1px solid #66bb6a;
    }
    
    .bag-item-missing {
        background: rgba(255, 232, 232, 0.95);
        color: #c62828;
        padding: 0.5rem 0.7rem;
        border-radius: 6px;
        margin: 0.2rem 0;
        display: flex;
        justify-content: space-between;
        align-items: center;
        border: 1px solid #f44336;
        font-weight: 500;
        font-size: 0.85rem;
    }
    
    /* Dark theme for missing items */
    [data-theme="dark"] .bag-item-missing,
    .stApp[data-theme="dark"] .bag-item-missing {
        background: rgba(198, 40, 40, 0.3);
        color: #ffcdd2;
        border: 1px solid #ef5350;
    }
    
    .stats-container {
        display: flex;
        justify-content: space-around;
        margin: 0.5rem 0;
        gap: 0.5rem;
    }
    
    .stat-box {
        background: rgba(168, 237, 234, 0.9);
        color: #006064;
        padding: 0.8rem;
        border-radius: 8px;
        text-align: center;
        min-width: 70px;
        box-shadow: 0 2px 6px rgba(0, 0, 0, 0.1);
        border: 1px solid #4dd0e1;
        font-weight: bold;
        font-size: 0.8rem;
    }
    
    .stat-box h3 {
        font-size: 1.1rem;
        margin-bottom: 0.2rem;
    }
    
    .stat-box p {
        font-size: 0.7rem;
        margin: 0;
    }
    
    /* Dark theme for stat boxes */
    [data-theme="dark"] .stat-box,
    .stApp[data-theme="dark"] .stat-box {
        background: rgba(0, 96, 100, 0.4);
        color: #b2ebf2;
        border: 1px solid #26c6da;
    }
    
    .activity-badge {
        background: #ff6b6b;
        color: white;
        padding: 0.2rem 0.6rem;
        border-radius: 15px;
        font-size: 0.7rem;
        margin-left: 0.5rem;
        font-weight: bold;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.2);
    }
    
    .uniform-alert {
        background: rgba(255, 243, 205, 0.95);
        color: #e65100;
        border: 1px solid #ffc107;
        padding: 0.8rem;
        border-radius: 6px;
        margin: 0.5rem 0;
        font-weight: 500;
        box-shadow: 0 1px 4px rgba(0, 0, 0, 0.1);
        font-size: 0.85rem;
    }
    
    /* Dark theme for uniform alert */
    [data-theme="dark"] .uniform-alert,
    .stApp[data-theme="dark"] .uniform-alert {
        background: rgba(255, 193, 7, 0.2);
        color: #fff3e0;
        border: 1px solid #ffb300;
    }
    
    /* Mobile-first responsive design */
    @media (max-width: 768px) {
        .main-header {
            padding: 0.8rem;
        }
        
        .main-header h1 {
            font-size: 1.1rem;
        }
        
        .main-header p {
            font-size: 0.8rem;
        }
        
        .subject-card, .bag-item, .bag-item-missing {
            padding: 0.5rem;
            margin: 0.2rem 0;
            font-size: 0.8rem;
        }
        
        .card {
            padding: 0.6rem;
            font-size: 0.85rem;
        }
        
        .stat-box {
            padding: 0.6rem;
            min-width: 60px;
            font-size: 0.75rem;
        }
        
        .stat-box h3 {
            font-size: 1rem;
        }
        
        .stat-box p {
            font-size: 0.65rem;
        }
        
        .stats-container {
            gap: 0.3rem;
        }
        
        .activity-badge {
            padding: 0.15rem 0.4rem;
            font-size: 0.65rem;
            margin-left: 0.3rem;
        }
        
        .uniform-alert {
            padding: 0.6rem;
            font-size: 0.8rem;
        }
        
        .holiday-card {
            padding: 0.8rem;
        }
        
        .holiday-card h2 {
            font-size: 1.1rem;
        }
        
        .holiday-card p {
            font-size: 0.85rem;
        }
    }
    
    /* Extra small screens (phones in portrait) */
    @media (max-width: 480px) {
        .main-header h1 {
            font-size: 1rem;
        }
        
        .main-header p {
            font-size: 0.75rem;
        }
        
        .subject-card, .bag-item, .bag-item-missing {
            padding: 0.4rem;
            font-size: 0.75rem;
        }
        
        .card {
            padding: 0.5rem;
            font-size: 0.8rem;
        }
        
        .stat-box {
            padding: 0.5rem;
            min-width: 55px;
            font-size: 0.7rem;
        }
        
        .stat-box h3 {
            font-size: 0.9rem;
        }
        
        .stat-box p {
            font-size: 0.6rem;
        }
        
        .activity-badge {
            padding: 0.1rem 0.3rem;
            font-size: 0.6rem;
        }
        
        .uniform-alert {
            padding: 0.5rem;
            font-size: 0.75rem;
        }
        
        .holiday-card h2 {
            font-size: 1rem;
        }
        
        .holiday-card p {
            font-size: 0.8rem;
        }
    }
    
    /* Ensure text is always readable with mobile optimization */
    .card h3, .card h4, .card p {
        color: inherit;
        margin: 0.3rem 0;
    }
    
    .card h4 {
        font-size: 0.95rem;
    }
    
    /* Better contrast for dark backgrounds */
    [data-theme="dark"] .main-header,
    .stApp[data-theme="dark"] .main-header {
        box-shadow: 0 2px 8px rgba(255, 255, 255, 0.1);
    }
    
    /* Mobile-optimized buttons */
    .stButton > button {
        border-radius: 6px;
        font-weight: 500;
        transition: all 0.3s ease;
        padding: 0.4rem 0.8rem;
        font-size: 0.85rem;
    }
    
    /* Compact sidebar for mobile */
    .css-1d391kg {
        padding: 0.5rem;
    }
    
    /* Mobile-optimized selectbox and inputs */
    .stSelectbox > div > div {
        font-size: 0.85rem;
    }
    
    .stTextInput > div > div > input {
        font-size: 0.85rem;
        padding: 0.5rem;
    }
    
    /* Compact dataframe for mobile */
    .dataframe {
        font-size: 0.8rem;
    }
    
    /* Mobile-optimized radio buttons */
    .stRadio > div {
        font-size: 0.85rem;
    }
    
    /* Compact info/success/warning messages */
    .stAlert {
        padding: 0.5rem;
        font-size: 0.85rem;
    }
    
    /* Custom scrollbar - thinner for mobile */
    ::-webkit-scrollbar {
        width: 4px;
    }
    
    ::-webkit-scrollbar-track {
        background: rgba(0, 0, 0, 0.1);
        border-radius: 2px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: rgba(102, 126, 234, 0.6);
        border-radius: 2px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: rgba(102, 126, 234, 0.8);
    }
    
    /* Compact footer */
    .footer-text {
        font-size: 0.75rem;
        color: #666;
    }
    
    /* Remove excessive margins on mobile */
    @media (max-width: 768px) {
        .block-container {
            padding: 0.5rem;
        }
        
        h1, h2, h3 {
            margin-bottom: 0.5rem;
        }
        
        .stMarkdown {
            margin-bottom: 0.3rem;
        }
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
    if page == "📅 Tomorrow's Schedule":
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
    <div style="text-align: center; margin-top: 1rem;" class="footer-text">
        <p>📚 Smart School Organizer - Class 4B</p>
        <p>Made with ❤️ for smart students</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == '__main__':
    main()
