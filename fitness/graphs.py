from plotly.offline import plot
import plotly.graph_objs as go
from plotly.graph_objs import Scatter, Bar


def fitness_graph(queryset, ex_name):
    fig = go.Figure()

    fig.add_trace(Scatter(
        x=[query.date_performed for query in queryset],
        y=[query.weight for query in queryset],
        name='Weight',
        line=dict(color='royalblue', width=2, dash='dot')
    ))
    fig.add_trace(Bar(
        x=[query.date_performed for query in queryset],
        y=[query.reps for query in queryset],
        name='Reps',
    ))
    fig.update_layout(
        title={'text': f'{ex_name.name} Progress',
               'y': 0.9,
               'x': 0.5,
               },
        xaxis_title='Time',
        yaxis_title='Weight (lbs)',
        font=dict(
            size=17,
            color='#007777'
        ),
        xaxis_tickangle=-25,
    )
    return plot(fig, output_type='div')
