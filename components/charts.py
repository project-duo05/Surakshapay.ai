import plotly.express as px
import plotly.graph_objects as go

def plot_transactions_over_time(df):
    df_grouped = df.set_index('timestamp').resample('H').size().reset_index(name='count')
    fig = px.line(df_grouped, x='timestamp', y='count', title='Transaction Volume Over Time', 
                  template='plotly_dark')
    fig.update_traces(line=dict(color='#00d4ff', width=3))
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=20, r=20, t=40, b=20),
        xaxis=dict(showline=True, showgrid=False, linecolor="#151b28"),
        yaxis=dict(showline=True, showgrid=True, gridcolor="#151b28", linecolor="#151b28")
    )
    return fig

def plot_fraud_distribution(df):
    counts = df['is_fraud'].value_counts()
    labels = ['Normal', 'Fraud']
    values = [counts.get(0, 0), counts.get(1, 0)]
    
    fig = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.6)])
    fig.update_traces(
        marker=dict(colors=['#00d4ff', '#ff3366'], line=dict(color='#0a0e17', width=2)),
        hoverinfo='label+percent', textinfo='none'
    )
    fig.update_layout(
        title='Transaction Distribution',
        template='plotly_dark',
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=20, r=20, t=40, b=20),
        showlegend=True,
        legend=dict(orientation="h", yanchor="bottom", y=-0.2, xanchor="center", x=0.5)
    )
    
    # Add annotation in the center
    fig.add_annotation(
        text=f"Total: {len(df)}",
        x=0.5, y=0.5, font_size=16, showarrow=False, font_color="#e2e8f0"
    )
    return fig

def plot_amount_distribution(df):
    fig = px.box(df, x="is_fraud", y="amount", points="all",
                 title='Amount Distribution by Class', log_y=True,
                 color="is_fraud", color_discrete_map={0: "#00d4ff", 1: "#ff3366"},
                 template='plotly_dark')
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=20, r=20, t=40, b=20),
        xaxis=dict(showgrid=False, title='Class (0: Normal, 1: Fraud)'),
        yaxis=dict(showgrid=True, gridcolor="#151b28", title='Amount (Log Scale)'),
        showlegend=False
    )
    return fig

def plot_anomaly_score_distribution(scores, class_labels=None):
    if class_labels is not None:
        df = pd.DataFrame({'Score': scores, 'Class': ['Fraud' if c == 1 else 'Normal' for c in class_labels]})
        fig = px.histogram(df, x='Score', color='Class', 
                           color_discrete_map={'Normal': '#00d4ff', 'Fraud': '#ff3366'},
                           barmode='overlay', title='Anomaly Score Distribution',
                           template='plotly_dark', opacity=0.7)
    else:
        fig = px.histogram(scores, title='Anomaly Score Distribution', 
                           color_discrete_sequence=['#00d4ff'],
                           template='plotly_dark')
    
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=20, r=20, t=40, b=20),
        xaxis_title='Anomaly Score',
        yaxis_title='Count'
    )
    return fig

def plot_feature_importance(importances_df):
    fig = px.bar(importances_df, x='Importance', y='Feature', orientation='h',
                 title='Feature Importance (Isolation Forest)',
                 template='plotly_dark',
                 color='Importance',
                 color_continuous_scale='Blues')
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=20, r=20, t=40, b=20),
        yaxis={'categoryorder': 'total ascending'}
    )
    return fig

def plot_scatter_anomalies(df, feature_x, feature_y, predictions):
    plot_df = df.copy()
    plot_df['Prediction'] = ['Anomaly' if p == 1 else 'Normal' for p in predictions]
    fig = px.scatter(plot_df, x=feature_x, y=feature_y, color='Prediction',
                     color_discrete_map={'Normal': '#0f52ba', 'Anomaly': '#ef4444'},
                     title=f'Scatter plot ({feature_x} vs {feature_y})',
                     template='plotly_white', opacity=0.7)
    
    fig.update_traces(marker=dict(size=8, line=dict(width=1, color='DarkSlateGrey')))
    fig.update_layout(
        plot_bgcolor='#ffffff',
        paper_bgcolor='#ffffff',
        margin=dict(l=20, r=20, t=40, b=20),
        xaxis=dict(showgrid=True, gridcolor='#f1f5f9', zerolinecolor='#cbd5e1'),
        yaxis=dict(showgrid=True, gridcolor='#f1f5f9', zerolinecolor='#cbd5e1')
    )
    return fig

def plot_confusion_matrix(y_true, y_pred):
    from sklearn.metrics import confusion_matrix
    cm = confusion_matrix(y_true, y_pred)
    # create heatmap
    fig = go.Figure(data=go.Heatmap(
        z=cm,
        x=['Predicted Normal', 'Predicted Fraud'],
        y=['True Normal', 'True Fraud'],
        colorscale='Blues',
        text=cm,
        texttemplate="%{text}",
        hoverinfo='skip'
    ))
    fig.update_layout(
        title='Confusion Matrix',
        template='plotly_dark',
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=20, r=20, t=40, b=20)
    )
    return fig
