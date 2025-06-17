import streamlit as st
import pandas as pd
import sys
import os

# Add parent directory to path to import our modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scheduler.scheduler import JobShopScheduler
from visualization.visualizer import ScheduleVisualizer

st.set_page_config(
    page_title="Smart AI Job-Shop Scheduler",
    page_icon="⚙️",
    layout="wide"
)

st.title("⚙️ Smart AI Job-Shop Scheduler for SMEs")

# Initialize session state
if 'scheduler' not in st.session_state:
    st.session_state.scheduler = JobShopScheduler()
if 'visualizer' not in st.session_state:
    st.session_state.visualizer = ScheduleVisualizer()
if 'solution' not in st.session_state:
    st.session_state.solution = None
if 'makespan' not in st.session_state:
    st.session_state.makespan = None
if 'utilization' not in st.session_state:
    st.session_state.utilization = None

# File uploader
uploaded_file = st.file_uploader("Upload your job data (CSV)", type=['csv'])

if uploaded_file is not None:
    # Save uploaded file temporarily
    with open("temp_data.csv", "wb") as f:
        f.write(uploaded_file.getvalue())
    
    # Load data
    try:
        st.session_state.scheduler.load_data("temp_data.csv")
        st.success("Data loaded successfully!")
        
        # Display raw data
        st.subheader("Raw Job Data")
        st.dataframe(pd.read_csv("temp_data.csv"))
        
        # Run optimization button
        if st.button("Run Optimizer"):
            with st.spinner("Optimizing schedule..."):
                # Get solution
                solution, makespan = st.session_state.scheduler.solve()
                st.session_state.solution = solution
                st.session_state.makespan = makespan
                
                # Calculate utilization
                utilization = st.session_state.scheduler.calculate_machine_utilization(solution)
                st.session_state.utilization = utilization
                
                st.success(f"Optimization complete! Makespan: {makespan} time units")
        
        # Display results if available
        if st.session_state.solution is not None:
            st.subheader("Optimized Schedule")
            
            # Create tabs for different visualizations
            tab1, tab2 = st.tabs(["Gantt Chart", "Utilization Analysis"])
            
            with tab1:
                gantt_fig = st.session_state.visualizer.create_gantt_chart(st.session_state.solution)
                st.plotly_chart(gantt_fig, use_container_width=True)
            
            with tab2:
                util_fig = st.session_state.visualizer.create_utilization_chart(st.session_state.utilization)
                st.plotly_chart(util_fig, use_container_width=True)
            
            # Display solution details
            st.subheader("Detailed Schedule")
            schedule_data = []
            for (job, task), task_data in st.session_state.solution.items():
                schedule_data.append({
                    'Job': job,
                    'Task': task,
                    'Machine': task_data['machine'],
                    'Start Time': task_data['start'],
                    'End Time': task_data['end'],
                    'Duration': task_data['duration']
                })
            
            st.dataframe(pd.DataFrame(schedule_data).sort_values(['Job', 'Task']))
    
    except Exception as e:
        st.error(f"Error: {str(e)}")
    
    finally:
        # Clean up temporary file
        if os.path.exists("temp_data.csv"):
            os.remove("temp_data.csv")

else:
    st.info("Please upload a CSV file to begin. The file should have columns: JobID, TaskID, MachineID, Duration")
    
    # Display sample data format
    st.subheader("Sample Data Format")
    sample_data = pd.DataFrame({
        'JobID': [1, 1, 1, 2, 2, 2],
        'TaskID': [1, 2, 3, 1, 2, 3],
        'MachineID': ['M1', 'M2', 'M3', 'M2', 'M1', 'M3'],
        'Duration': [3, 2, 4, 4, 2, 3]
    })
    st.dataframe(sample_data) 