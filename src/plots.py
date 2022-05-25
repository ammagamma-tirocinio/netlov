import streamlit as st
import plotly.graph_objects as go
from dataset_preparation import compute_quantile
from config import *

def quantile_line(melt_id,fig):
    y_pos = [0, 0.2]
    colors_line = [red + '1)', green + '1)']
    labels = ['reference', 'current']

    for q in [0.25, 0.5, 0.75]:
        temp_quant = compute_quantile(melt_id, q, METRIC)
        for el, col in enumerate(list(temp_quant.columns)):
            fig.add_trace(go.Scatter(x=np.array(list(temp_quant.index)) + y_pos[el], y=temp_quant[col],
                                     name='quantile ' + str(q) + ' ' + labels[el],
                                     mode='lines+markers', line={'color': colors_line[el], 'width': 1}))
    return fig

def grafico1(current_melt_id, reference_melt_id,melt_id):
    y_pos = [0, 0.2]
    plot = [reference_melt_id,current_melt_id]
    labels = ['reference','current']
    colors = [blu_ammagamma + str(alpha)+')', yellow+str(alpha)+')']
    style = ['circle', 'x']

    layout = go.Layout(title='MAPE for each gruop of prediction: period ' +
                             str(plot[1]['dat_trasporto'].iloc[0].strftime("%Y-%m-%d")),
                       xaxis=dict(title='Days',
                                  range=[0, 15]),
                       yaxis=dict(title='MAPE',
                                  range=[0, 400]),
                       autosize=False,
                       width=1000,
                       height=500)
    fig = go.Figure(layout=layout)
    for el in range(2):
        fig.add_trace(go.Scatter(x=plot[el]['steps'] + y_pos[el], y=plot[el][METRIC], name=labels[el],
                                 mode='markers', marker={
                'symbol': style[el],
                'size': 8,
                'color': colors[el] + str(alpha) + ')',
                'line': dict(color=colors[el] + '1)', width=1)}, ))
    fig.update_layout(xaxis_showgrid=False, xaxis_zeroline=False)
    fig = quantile_line(melt_id, fig)
    st.plotly_chart(fig)

def grafico2(current_melt_id, reference_melt_id):
    y_pos = [-0.17, 0.17]
    style = ['circle','x']
    plot = [reference_melt_id, current_melt_id]
    labels = ['reference','current']
    colors = [blu_ammagamma + '1)', yellow +'1)']

    layout = go.Layout(title='MAPE for each gruop of prediction: period ' +
                             str(plot[1]['dat_trasporto'].iloc[0].strftime("%Y-%m-%d")),
                       xaxis=dict(title='Days',
                                  range=[0, 15]),
                       yaxis=dict(title='MAPE',
                                  range=[0, 400]),
                       autosize=False,
                       width=1300,
                       height=400)
    fig = go.Figure(layout=layout)
    for el in range(2):
        fig.add_trace(go.Box(x=plot[el]['steps'] + y_pos[el], y=plot[el][METRIC], name=labels[el],
                             fillcolor=colors[el] + '0.8)', width=0.3, marker={
                'symbol': style[el],
                'size': 5,
                'color': colors[el] + str(alpha) + ')',
                'line': dict(color= colors[el]+ '1)',width=1)} ))

    fig.update_layout(xaxis_showgrid=False, xaxis_zeroline=False)
    st.plotly_chart(fig)

def grafico3(current_melt_id, reference_melt_id,melt_id):
    plot = [reference_melt_id, current_melt_id]
    y_pos = [-0.05, 0.05]
    labels = ['reference', 'current']
    colors = [blu_ammagamma + str(alpha) + ')', yellow + str(alpha) + ')']
    side = ['negative', 'positive']
    style = ['circle', 'x']


    layout = go.Layout(title='MAPE for each gruop of prediction: period ' +
                             str(plot[1]['dat_trasporto'].iloc[0].strftime("%Y-%m-%d")),
                       xaxis=dict(title='Days',
                                  range=[0, 15]),
                       yaxis=dict(title='MAPE',
                                  range=[0, 400]),
                       autosize=False,

                       width=1000,
                       height=500)
    fig = go.Figure(layout=layout)

    for i, ref in enumerate(['past_year', 'current_year']):
        fig.add_trace(go.Violin(x=melt_id['steps'][melt_id['reference'] == ref] + y_pos[i],
                                y=melt_id[METRIC][melt_id['reference'] == ref],
                                legendgroup=labels[i], scalegroup=labels[i], name=labels[i],
                                side=side[i],
                                fillcolor=colors[i] + '0.8)',
                                width=0.8,
                                line={'color': colors[i] + '1)'},
                                marker={'symbol': style[i],
                                        'size': 5,
                                        'color': colors[i] + str(alpha) + ')',
                                        'line': dict(color=colors[i] + '1)', width=1)}))
    fig.update_traces(meanline_visible=True, jitter=0, scalemode='count')
    fig = quantile_line(melt_id, fig)
    st.plotly_chart(fig)

