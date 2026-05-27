import plotly.graph_objects as gr
from plotly.subplots import make_subplots
import pandas as pd

def generate_candlestick_chart(df: pd.DataFrame, ticker_name: str):
    """Generates an institutional dual-pane candlestick chart with structural indicators."""
    fig = make_subplots(rows=2, cols=1, shared_xaxes=True, 
                        vertical_spacing=0.05, row_heights=[0.7, 0.3])
    
    # Candlestick
    fig.add_trace(gr.Candlestick(
        x=df.index, open=df['Open'], high=df['High'], low=df['Low'], close=df['Close'],
        name="Price Action"
    ), row=1, col=1)
    
    # Overlays
    if 'EMA20' in df.columns:
        fig.add_trace(gr.Scatter(x=df.index, y=df['EMA20'], line=dict(color='orange', width=1.5), name='EMA 20'), row=1, col=1)
    if 'EMA50' in df.columns:
        fig.add_trace(gr.Scatter(x=df.index, y=df['EMA50'], line=dict(color='cyan', width=1.5), name='EMA 50'), row=1, col=1)
    if 'EMA200' in df.columns:
        fig.add_trace(gr.Scatter(x=df.index, y=df['EMA200'], line=dict(color='red', width=2), name='EMA 200'), row=1, col=1)
        
    # Volume Bars
    colors = ['green' if row['Close'] >= row['Open'] else 'red' for _, row in df.iterrows()]
    fig.add_trace(gr.Bar(x=df.index, y=df['Volume'], marker_color=colors, name='Volume Output'), row=2, col=1)
    
    fig.update_layout(
        title=f"Institutional Analytical Layout: {ticker_name}",
        yaxis_title="Price (INR)",
        yaxis2_title="Volume",
        xaxis_rangeslider_visible=False,
        template="plotly_dark",
        height=600,
        margin=dict(l=10, r=10, t=40, b=10)
    )
    return fig