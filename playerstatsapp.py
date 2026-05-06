from dash import Dash, dcc, html, Input, Output
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd

app = Dash(__name__, suppress_callback_exceptions=True)
server = app.server

dark = {
    'plot_bgcolor': '#1a1a2e',
    'paper_bgcolor': '#0d0d1a',
    'font': {'color': 'white'}
}

df = pd.read_csv("players_data-2025_2026.csv")
df = df.dropna(subset=['Player', 'Pos'])
df['Player'] = df['Player'].str.title().str.strip()
df['Pos'] = df['Pos'].str.title().str.strip()

# Attacking Stats
top_goals = df[['Player', 'Gls']].sort_values('Gls', ascending=False).head(10)
top_assists = df[['Player', 'Ast']].sort_values('Ast', ascending=False).head(10)
top_ga = df[['Player', 'G+A']].sort_values('G+A', ascending=False).head(10)
total_shots = df[['Player', 'Sh']].sort_values('Sh', ascending=False).head(10)
goals_ps = df[df['Sh'] >= 20][['Player', 'G/Sh']].sort_values('G/Sh', ascending=False).head(10)
total_crosses = df[['Player', 'Crs']].sort_values('Crs', ascending=False).head(10)

# Defensive Stats

top_tackles = df[['Player', 'TklW']].sort_values('TklW', ascending=False).head(10)
top_interceps = df[['Player', 'Int']].sort_values('Int', ascending=False).head(10)
top_foulsdrawn = df[['Player', 'Fld']].sort_values('Fld', ascending=False).head(10)
top_foulscom = df[['Player', 'Fls']].sort_values('Fls', ascending=False).head(10)


# Goalkeeper Stats
gk_df = df[df['Pos'] == 'Gk']
top_saves = gk_df[['Player', 'Saves']].sort_values('Saves', ascending=False).head(10)
top_savepct = gk_df[gk_df['SoTA'] >= 20][['Player', 'Save%']].sort_values('Save%', ascending=False).head(10)
top_cs = gk_df[['Player', 'CS']].sort_values('CS', ascending=False).head(10)
top_ga_gk = gk_df[['Player', 'GA']].sort_values('GA', ascending=False).head(10)


# Attacking Radar chart data - normalised
categories = ['Gls', 'Ast', 'G+A', 'Sh', 'SoT', 'G/Sh']
radar_df = df[['Player'] + categories].fillna(0).copy()
for cat in categories:
    max_val = df[cat].max()
    radar_df[cat] = (radar_df[cat] / max_val) * 100

# Defensive radar - normalised
def_categories = ['TklW', 'Int', 'Fld', 'Fls', 'CrdY']
def_radar_df = df[['Player'] + def_categories].fillna(0).copy()
for cat in def_categories:
    max_val = df[cat].max()
    def_radar_df[cat] = (def_radar_df[cat] / max_val) * 100

# GK radar - normalised
gk_categories = ['Saves', 'Save%', 'CS', 'GA', 'GA90']
gk_radar_df = gk_df[['Player'] + gk_categories].fillna(0).copy()
for cat in gk_categories:
    max_val = gk_df[cat].max()
    gk_radar_df[cat] = (gk_radar_df[cat] / max_val) * 100

# Charts
fig_top_tackles = px.bar(top_tackles, x='Player', y='TklW', title='Top Tackles',
                         color='TklW', color_continuous_scale='purples')
fig_top_tackles.update_layout(dark)

fig_top_intercepts = px.bar(top_interceps, x='Player', y='Int', title='Top Interceptions',
                         color='Int', color_continuous_scale='purples')
fig_top_intercepts.update_layout(dark)

fig_top_foulsd = px.bar(top_foulsdrawn, x='Player', y='Fld', title='Most Fouls Drawn',
                         color='Fld', color_continuous_scale='purples')
fig_top_foulsd.update_layout(dark)

fig_top_foulscom = px.bar(top_foulscom, x='Player', y='Fls', title='Most Fouls Commited',
                         color='Fls', color_continuous_scale='purples')
fig_top_foulscom.update_layout(dark)

fig_goals = px.bar(top_goals, x='Player', y='Gls', title='Top Scorers',
                   color='Gls', color_continuous_scale='purples')
fig_goals.update_layout(dark)

fig_assists = px.bar(top_assists, x='Player', y='Ast', title='Top Assists',
                     color='Ast', color_continuous_scale='blues')
fig_assists.update_layout(dark)

fig_ga = px.bar(top_ga, x='Player', y='G+A', title='Top Goals + Assists',
                color='G+A', color_continuous_scale='purples')
fig_ga.update_layout(dark)

fig_total_shots = px.bar(total_shots, x='Player', y='Sh', title='Top Shots',
                         color='Sh', color_continuous_scale='purples')
fig_total_shots.update_layout(dark)

fig_total_crosses = px.bar(total_crosses, x='Player', y='Crs', title='Total Crosses',
                           color='Crs', color_continuous_scale='purples')
fig_total_crosses.update_layout(dark)

fig_goals_ps = px.bar(goals_ps, x='Player', y='G/Sh', title='Goals per Shots',
                      color='G/Sh', color_continuous_scale='blues')
fig_goals_ps.update_layout(dark)

fig_saves = px.bar(top_saves, x='Player', y='Saves', title='Most Saves',
                   color='Saves', color_continuous_scale='blues')
fig_saves.update_layout(dark)

fig_savepct = px.bar(top_savepct, x='Player', y='Save%', title='Best Save % (min 20 shots faced)',
                     color='Save%', color_continuous_scale='greens')
fig_savepct.update_layout(dark)

fig_cs = px.bar(top_cs, x='Player', y='CS', title='Most Clean Sheets',
                color='CS', color_continuous_scale='blues')
fig_cs.update_layout(dark)

fig_ga_gk = px.bar(top_ga_gk, x='Player', y='GA', title='Goals Conceded',
                   color='GA', color_continuous_scale='reds')
fig_ga_gk.update_layout(dark)

# Layout
app.layout = html.Div([

    html.H1("Football Player Stats 2025/26", style={'textAlign': 'center', 'padding': '20px', 'color': 'white'}),

    dcc.Tabs(id='tabs', value='attacking', children=[
        dcc.Tab(label='Attacking', value='attacking', style={'backgroundColor': '#1a1a2e', 'color': 'white'},
                selected_style={'backgroundColor': '#38003c', 'color': 'white'}),
        dcc.Tab(label='Defensive', value='defensive', style={'backgroundColor': '#1a1a2e', 'color': 'white'},
                selected_style={'backgroundColor': '#38003c', 'color': 'white'}),
        dcc.Tab(label='Goalkeeper', value='goalkeeper', style={'backgroundColor': '#1a1a2e', 'color': 'white'},
                selected_style={'backgroundColor': '#38003c', 'color': 'white'}),
    ]),

    html.Div(id='tab-content')

], style={'backgroundColor': '#0d0d1a', 'minHeight': '100vh'})

# Tab callback
@app.callback(
    Output('tab-content', 'children'),
    Input('tabs', 'value')
)
def render_tab(tab):
    if tab == 'attacking':
        return html.Div([
            html.Div([
                dcc.Graph(figure=fig_goals, style={'width': '50%'}),
                dcc.Graph(figure=fig_assists, style={'width': '50%'}),
            ], style={'display': 'flex'}),
            html.Div([
                dcc.Graph(figure=fig_ga, style={'width': '50%'}),
                dcc.Graph(figure=fig_total_shots, style={'width': '50%'}),
            ], style={'display': 'flex'}),
            html.Div([
                dcc.Graph(figure=fig_total_crosses, style={'width': '50%'}),
                dcc.Graph(figure=fig_goals_ps, style={'width': '50%'}),
            ], style={'display': 'flex'}),
            html.Hr(style={'borderColor': '#444', 'margin': '30px 0'}),
            html.H2("Player Comparison", style={'color': 'white', 'padding': '0 20px'}),
            html.Div([
                dcc.Dropdown(
                    id='player-selector',
                    options=[{'label': p, 'value': p} for p in sorted(df['Player'].unique())],
                    value=df.nlargest(5, 'Gls')['Player'].tolist(),
                    multi=True,
                    placeholder='Search and select players...',
                    style={'backgroundColor': '#1a1a2e', 'color': 'white', 'width': '100%'}
                ),
                dcc.Graph(id='radar-chart', style={'height': '600px', 'width': '100%'}),
            ], style={'padding': '20px'}),
        ])

    elif tab == 'defensive':
        return html.Div([
            html.Div([
                dcc.Graph(figure=fig_top_tackles, style={'width': '50%'}),
                dcc.Graph(figure=fig_top_intercepts, style={'width': '50%'}),
            ], style={'display': 'flex'}),
            html.Div([
                dcc.Graph(figure=fig_top_foulsd, style={'width': '50%'}),
                dcc.Graph(figure=fig_top_foulscom, style={'width': '50%'}),
            ], style={'display': 'flex'}),
            html.Hr(style={'borderColor': '#444', 'margin': '30px 0'}),
            html.H2("Defensive Player Comparison", style={'color': 'white', 'padding': '0 20px'}),
            html.Div([
                dcc.Dropdown(
                    id='def-player-selector',
                    options=[{'label': p, 'value': p} for p in sorted(df['Player'].unique())],
                    value=df.nlargest(5, 'TklW')['Player'].tolist(),
                    multi=True,
                    placeholder='Search and select players...',
                    style={'backgroundColor': '#1a1a2e', 'color': 'white', 'width': '100%'}
                ),
                dcc.Graph(id='def-radar-chart', style={'height': '600px', 'width': '100%'}),
            ], style={'padding': '20px'}),
        ])
    elif tab == 'goalkeeper':
        return html.Div([
            html.Div([
                dcc.Graph(figure=fig_saves, style={'width': '50%'}),
                dcc.Graph(figure=fig_savepct, style={'width': '50%'}),
            ], style={'display': 'flex'}),
            html.Div([
                dcc.Graph(figure=fig_cs, style={'width': '50%'}),
                dcc.Graph(figure=fig_ga_gk, style={'width': '50%'}),
            ], style={'display': 'flex'}),
            html.Hr(style={'borderColor': '#444', 'margin': '30px 0'}),
            html.H2("Goalkeeper Comparison", style={'color': 'white', 'padding': '0 20px'}),
            html.Div([
                dcc.Dropdown(
                    id='gk-player-selector',
                    options=[{'label': p, 'value': p} for p in sorted(gk_df['Player'].unique())],
                    value=gk_df.nlargest(5, 'Saves')['Player'].tolist(),
                    multi=True,
                    placeholder='Search and select goalkeepers...',
                    style={'backgroundColor': '#1a1a2e', 'color': 'white', 'width': '100%'}
                ),
                dcc.Graph(id='gk-radar-chart', style={'height': '600px', 'width': '100%'}),
            ], style={'padding': '20px'}),
        ])

# Radar callback
@app.callback(
    Output('radar-chart', 'figure'),
    Input('player-selector', 'value')
)
def update_radar(selected_players):
    if not selected_players:
        selected_players = df.nlargest(5, 'Gls')['Player'].tolist()

    filtered = radar_df[radar_df['Player'].isin(selected_players)]

    fig = go.Figure()
    for _, row in filtered.iterrows():
        original = df[df['Player'] == row['Player']][categories].fillna(0).iloc[0]

        fig.add_trace(go.Scatterpolar(
            r=[row[cat] for cat in categories],
            theta=categories,
            fill='toself',
            name=row['Player'],
            opacity=0.6,
            hovertemplate='<b>' + row['Player'] + '</b><br>' +
                          '<br>'.join([f'{cat}: {round(float(original[cat]), 2)}' for cat in categories]) +
                          '<extra></extra>'
        ))
    fig.update_layout(
        dark,
        polar=dict(
            radialaxis=dict(visible=True, color='white', range=[0, 100]),
            angularaxis=dict(color='white'),
            bgcolor='#1a1a2e'
        ),
        title='Player Comparison',
        showlegend=True,
        legend=dict(
            orientation='h',
            yanchor='bottom',
            y=-0.2,
            xanchor='center',
            x=0.5,
            font=dict(color='white')
        )
    )
    return fig

@app.callback(
    Output('def-radar-chart', 'figure'),
    Input('def-player-selector', 'value')
)
def update_def_radar(selected_players):
    if not selected_players:
        selected_players = df.nlargest(5, 'TklW')['Player'].tolist()

    filtered = def_radar_df[def_radar_df['Player'].isin(selected_players)]

    fig = go.Figure()
    for _, row in filtered.iterrows():
        original = df[df['Player'] == row['Player']][def_categories].fillna(0).iloc[0]

        fig.add_trace(go.Scatterpolar(
            r=[row[cat] for cat in def_categories],
            theta=def_categories,
            fill='toself',
            name=row['Player'],
            opacity=0.6,
            hovertemplate='<b>' + row['Player'] + '</b><br>' +
                          '<br>'.join([f'{cat}: {round(float(original[cat]), 2)}' for cat in def_categories]) +
                          '<extra></extra>'
        ))
    fig.update_layout(
        dark,
        polar=dict(
            radialaxis=dict(visible=True, color='white', range=[0, 100]),
            angularaxis=dict(color='white'),
            bgcolor='#1a1a2e'
        ),
        title='Defensive Player Comparison',
        showlegend=True,
        legend=dict(
            orientation='h',
            yanchor='bottom',
            y=-0.2,
            xanchor='center',
            x=0.5,
            font=dict(color='white')
        )
    )
    return fig

@app.callback(
    Output('gk-radar-chart', 'figure'),
    Input('gk-player-selector', 'value')
)
def update_gk_radar(selected_players):
    if not selected_players:
        selected_players = gk_df.nlargest(5, 'Saves')['Player'].tolist()

    filtered = gk_radar_df[gk_radar_df['Player'].isin(selected_players)]

    fig = go.Figure()
    for _, row in filtered.iterrows():
        original = gk_df[gk_df['Player'] == row['Player']][gk_categories].fillna(0).iloc[0]

        fig.add_trace(go.Scatterpolar(
            r=[row[cat] for cat in gk_categories],
            theta=gk_categories,
            fill='toself',
            name=row['Player'],
            opacity=0.6,
            hovertemplate='<b>' + row['Player'] + '</b><br>' +
                          '<br>'.join([f'{cat}: {round(float(original[cat]), 2)}' for cat in gk_categories]) +
                          '<extra></extra>'
        ))
    fig.update_layout(
        dark,
        polar=dict(
            radialaxis=dict(visible=True, color='white', range=[0, 100]),
            angularaxis=dict(color='white'),
            bgcolor='#1a1a2e'
        ),
        title='Goalkeeper Comparison',
        showlegend=True,
        legend=dict(
            orientation='h',
            yanchor='bottom',
            y=-0.2,
            xanchor='center',
            x=0.5,
            font=dict(color='white')
        )
    )
    return fig

if __name__ == '__main__':
    app.run(debug=True)