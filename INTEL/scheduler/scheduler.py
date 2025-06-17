from ortools.sat.python import cp_model
import pandas as pd
import numpy as np
from typing import Dict, List, Tuple

class JobShopScheduler:
    def __init__(self):
        self.model = None
        self.solver = None
        self.jobs_data = None
        self.machines = None
        self.jobs = None
        self.horizon = 0
        
    def load_data(self, csv_path: str) -> None:
        """Load job data from CSV file."""
        self.jobs_data = pd.read_csv(csv_path)
        self.machines = sorted(self.jobs_data['MachineID'].unique())
        self.jobs = sorted(self.jobs_data['JobID'].unique())
        self.horizon = self.jobs_data['Duration'].sum()
        
    def create_model(self) -> None:
        """Create the constraint programming model."""
        self.model = cp_model.CpModel()
        self.solver = cp_model.CpSolver()
        
    def solve(self) -> Tuple[Dict, float]:
        """Solve the job-shop scheduling problem."""
        if self.jobs_data is None:
            raise ValueError("Please load data first using load_data()")
            
        self.create_model()
        
        # Create variables
        all_tasks = {}
        machine_to_intervals = {machine: [] for machine in self.machines}
        
        for _, row in self.jobs_data.iterrows():
            job_id = row['JobID']
            task_id = row['TaskID']
            machine_id = row['MachineID']
            duration = row['Duration']
            
            suffix = f'_{job_id}_{task_id}'
            start_var = self.model.NewIntVar(0, self.horizon, f'start{suffix}')
            end_var = self.model.NewIntVar(0, self.horizon, f'end{suffix}')
            
            interval_var = self.model.NewIntervalVar(
                start_var, duration, end_var, f'interval{suffix}')
            
            all_tasks[(job_id, task_id)] = {
                'start': start_var,
                'end': end_var,
                'interval': interval_var,
                'machine': machine_id,
                'duration': duration
            }
            
            machine_to_intervals[machine_id].append(interval_var)
        
        # Add constraints
        # 1. Machine constraints
        for machine in self.machines:
            self.model.AddNoOverlap(machine_to_intervals[machine])
        
        # 2. Job precedence constraints
        for job in self.jobs:
            job_tasks = self.jobs_data[self.jobs_data['JobID'] == job].sort_values('TaskID')
            for i in range(len(job_tasks) - 1):
                current_task = (job, job_tasks.iloc[i]['TaskID'])
                next_task = (job, job_tasks.iloc[i + 1]['TaskID'])
                self.model.Add(
                    all_tasks[current_task]['end'] <= all_tasks[next_task]['start']
                )
        
        # 3. Makespan objective
        obj_var = self.model.NewIntVar(0, self.horizon, 'makespan')
        self.model.AddMaxEquality(
            obj_var,
            [all_tasks[(job, task)]['end'] for job in self.jobs for task in self.jobs_data[self.jobs_data['JobID'] == job]['TaskID']]
        )
        self.model.Minimize(obj_var)
        
        # Solve the model
        status = self.solver.Solve(self.model)
        
        if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
            # Extract solution
            solution = {}
            for (job, task), task_data in all_tasks.items():
                solution[(job, task)] = {
                    'start': self.solver.Value(task_data['start']),
                    'end': self.solver.Value(task_data['end']),
                    'machine': task_data['machine'],
                    'duration': task_data['duration']
                }
            
            makespan = self.solver.Value(obj_var)
            return solution, makespan
        else:
            raise Exception('No solution found!')
    
    def calculate_machine_utilization(self, solution: Dict) -> Dict[str, float]:
        """Calculate machine utilization rates."""
        machine_times = {machine: 0 for machine in self.machines}
        makespan = max(task['end'] for task in solution.values())
        
        for task_data in solution.values():
            machine = task_data['machine']
            duration = task_data['duration']
            machine_times[machine] += duration
        
        utilization = {
            machine: (time / makespan) * 100 
            for machine, time in machine_times.items()
        }
        
        return utilization 