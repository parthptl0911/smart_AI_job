import plotly.figure_factory as ff
import plotly.graph_objects as go
from typing import Dict, List
import pandas as pd

class ScheduleVisualizer:
    @staticmethod
    def create_gantt_chart(solution: Dict) -> go.Figure:
        """Create a Gantt chart from the scheduling solution."""
        df = []
        for (job, task), task_data in solution.items():
            df.append(dict(
                Task=f'Machine {task_data["machine"]}',
                Start=task_data['start'],
                Finish=task_data['end'],
                Resource=f'Job {job}',
                Description=f'Task {task}'
            ))
        
        df = pd.DataFrame(df)
        
        jobs = set(df['Resource'])
        colors = {
            job: f'rgb({(i * 50) % 255}, {(i * 100) % 255}, {(i * 150) % 255})'
            for i, job in enumerate(sorted(jobs))
        }
        
        fig = ff.create_gantt(
            df,
            colors=colors,
            index_col='Resource',
            show_colorbar=True,
            group_tasks=True,
            showgrid_x=True,
            showgrid_y=True
        )
        
        fig.update_layout(
            title='Job Shop Schedule Gantt Chart',
            xaxis_title='Time',
            yaxis_title='Machine',
            height=400
        )
        
        return fig
    
    @staticmethod
    def create_utilization_chart(utilization: Dict[str, float]) -> go.Figure:
        """Create a bar chart showing machine utilization rates."""
        machines = list(utilization.keys())
        rates = list(utilization.values())
        
        fig = go.Figure(data=[
            go.Bar(
                x=machines,
                y=rates,
                text=[f'{rate:.1f}%' for rate in rates],
                textposition='auto',
            )
        ])
        
        fig.update_layout(
            title='Machine Utilization Rates',
            xaxis_title='Machine',
            yaxis_title='Utilization Rate (%)',
            yaxis_range=[0, 100],
            height=400
        )
        
        return fig
    
    @staticmethod
    def create_comparison_chart(before: Dict[str, float], after: Dict[str, float]) -> go.Figure:
        """Create a comparison chart of utilization rates before and after optimization."""
        machines = list(before.keys())
        before_rates = list(before.values())
        after_rates = list(after.values())
        
        fig = go.Figure(data=[
            go.Bar(
                name='Before Optimization',
                x=machines,
                y=before_rates,
                text=[f'{rate:.1f}%' for rate in before_rates],
                textposition='auto',
            ),
            go.Bar(
                name='After Optimization',
                x=machines,
                y=after_rates,
                text=[f'{rate:.1f}%' for rate in after_rates],
                textposition='auto',
            )
        ])
        
        fig.update_layout(
            title='Machine Utilization Comparison',
            xaxis_title='Machine',
            yaxis_title='Utilization Rate (%)',
            yaxis_range=[0, 100],
            barmode='group',
            height=400
        )
        
        return fig 