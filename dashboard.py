# import pandas as pd
# import plotly.express as px
# import plotly.graph_objects as go
# import dash
# import dash_bootstrap_components as dbc
# from dash import dcc, html, dash_table
# from dash.dependencies import Input, Output

# # --- 1. Data Loading and Preparation ---

# # Load the dataset
# try:
#     df = pd.read_csv('traffic_accidents.csv')
# except FileNotFoundError:
#     print("Error: 'traffic_accidents.csv' not found. Please place the file in the same directory as the script.")
#     exit()

# # Clean column names for easier access
# df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_').str.replace('(', '').str.replace(')', '')

# # Data type conversions and feature engineering
# df['crash_date'] = pd.to_datetime(df['crash_date'], errors='coerce')
# df['year'] = df['crash_date'].dt.year
# df = df.dropna(subset=['crash_date', 'crash_hour', 'crash_day_of_week', 'crash_month']) # Drop rows where essential date/time info is missing

# # Standardize boolean-like columns
# df['intersection_related_i'] = df['intersection_related_i'].fillna('N').apply(lambda x: 'Yes' if x.strip() == 'Y' else 'No')

# # Map day and month numbers to names for better readability
# day_map = {1: 'Sunday', 2: 'Monday', 3: 'Tuesday', 4: 'Wednesday', 5: 'Thursday', 6: 'Friday', 7: 'Saturday'}
# month_map = {1: 'Jan', 2: 'Feb', 3: 'Mar', 4: 'Apr', 5: 'May', 6: 'Jun', 7: 'Jul', 8: 'Aug', 9: 'Sep', 10: 'Oct', 11: 'Nov', 12: 'Dec'}
# df['day_of_week_name'] = df['crash_day_of_week'].map(day_map)
# df['month_name'] = df['crash_month'].map(month_map)


# # --- 2. Initialize the Dash App ---
# app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
# server = app.server

# # --- 3. Define App Layout ---

# # Reusable styles
# CARD_STYLE = {
#     "padding": "20px",
#     "border-radius": "10px",
#     "box-shadow": "0 4px 8px 0 rgba(0,0,0,0.2)",
#     "transition": "0.3s",
# }

# # --- Filter Controls ---
# controls = dbc.Card(
#     [
#         dbc.Row([
#             dbc.Col(html.H4("Filters"), width=12, className="mb-3")
#         ]),
#         dbc.Row([
#             dbc.Col(dcc.Dropdown(
#                 id='year-filter',
#                 options=[{'label': str(year), 'value': year} for year in sorted(df['year'].unique())],
#                 multi=True,
#                 placeholder='Select Year(s)'
#             ), md=4),
#             dbc.Col(dcc.Dropdown(
#                 id='month-filter',
#                 options=[{'label': month, 'value': num} for num, month in month_map.items()],
#                 multi=True,
#                 placeholder='Select Month(s)'
#             ), md=4),
#             dbc.Col(dcc.Dropdown(
#                 id='day-filter',
#                 options=[{'label': day, 'value': num} for num, day in day_map.items()],
#                 multi=True,
#                 placeholder='Select Day(s) of Week'
#             ), md=4),
#         ]),
#         dbc.Row([
#             dbc.Col(dcc.Dropdown(
#                 id='weather-filter',
#                 options=[{'label': i, 'value': i} for i in df['weather_condition'].unique() if pd.notna(i)],
#                 multi=True,
#                 placeholder='Select Weather Condition(s)'
#             ), md=4),
#             dbc.Col(dcc.Dropdown(
#                 id='lighting-filter',
#                 options=[{'label': i, 'value': i} for i in df['lighting_condition'].unique() if pd.notna(i)],
#                 multi=True,
#                 placeholder='Select Lighting Condition(s)'
#             ), md=4),
#             dbc.Col(dcc.Dropdown(
#                 id='surface-filter',
#                 options=[{'label': i, 'value': i} for i in df['roadway_surface_cond'].unique() if pd.notna(i)],
#                 multi=True,
#                 placeholder='Select Surface Condition(s)'
#             ), md=4),
#         ], className="mt-3"),
#         dbc.Row([
#              dbc.Col(dcc.Dropdown(
#                 id='intersection-filter',
#                 options=[{'label': 'Yes', 'value': 'Yes'}, {'label': 'No', 'value': 'No'}],
#                 placeholder='Intersection Related?'
#             ), md=4),
#         ], className="mt-3")
#     ],
#     body=True,
#     className="mb-4"
# )

# # --- App Layout ---
# app.layout = dbc.Container([
#     # Header
#     dbc.Row([
#         dbc.Col(html.H1("Chicago Traffic Accidents Dashboard", className="text-center text-primary mt-4 mb-4"), width=12)
#     ]),
#     # Filters
#     dbc.Row([
#         dbc.Col(controls, width=12)
#     ]),
#     # Tabs
#     dcc.Tabs(id="tabs", children=[
#         # --- Tab A: Overview ---
#         dcc.Tab(label='Home / Overview', children=[
#             dbc.Row([
#                 # KPI Cards
#                 dbc.Col(dbc.Card(id='kpi-total-crashes', style=CARD_STYLE), md=3, className="mt-4"),
#                 dbc.Col(dbc.Card(id='kpi-total-injuries', style=CARD_STYLE), md=3, className="mt-4"),
#                 dbc.Col(dbc.Card(id='kpi-injuries-per-crash', style=CARD_STYLE), md=3, className="mt-4"),
#                 dbc.Col(dbc.Card(id='kpi-intersection-pct', style=CARD_STYLE), md=3, className="mt-4"),
#             ]),
#             dbc.Row([
#                 dbc.Col(html.H4("Summary Table: Crashes by Day and Month", className="mt-5 mb-3"), width=12),
#                 dbc.Col(id='summary-table-container', width=12)
#             ])
#         ]),
#         # --- Tab B: Crash Timings ---
#         dcc.Tab(label='When Crashes Happen', children=[
#             dbc.Row([
#                 dbc.Col(dcc.Graph(id='bar-day-of-week'), md=6, className="mt-4"),
#                 dbc.Col(dcc.Graph(id='heatmap-hour-day'), md=6, className="mt-4"),
#             ]),
#             dbc.Row([
#                 dbc.Col(dcc.Graph(id='line-month'), width=12, className="mt-4"),
#             ])
#         ]),
#         # --- Tab C: Severity & Conditions ---
#         dcc.Tab(label='Severity & Conditions', children=[
#             dbc.Row([
#                 dbc.Col([
#                     dcc.Graph(id='box-injuries-surface'),
#                     html.P(id='box-caption', className="text-center fst-italic")
#                 ], md=6, className="mt-4"),
#                 dbc.Col([
#                     dcc.Graph(id='stacked-bar-crash-type'),
#                      html.P("Insight: Daylight hours see a higher proportion of rear-end and turning crashes, while nighttime crashes have a higher share of fixed object collisions.", className="text-center fst-italic")
#                 ], md=6, className="mt-4"),
#             ]),
#              dbc.Row([
#                 dbc.Col([
#                     dcc.Graph(id='scatter-units-injuries'),
#                     html.P("Takeaway: Crashes involving more vehicles tend to result in a higher number of total injuries, though many multi-vehicle incidents still result in zero injuries.", className="text-center fst-italic")
#                 ], width=12, className="mt-4"),
#             ])
#         ]),
#         # --- Tab D: Contributors & Locations ---
#         dcc.Tab(label='Contributors & Locations', children=[
#             dbc.Row([
#                 dbc.Col(dcc.Graph(id='bar-contrib-cause'), md=8, className="mt-4"),
#                 dbc.Col(dcc.Graph(id='pie-intersection'), md=4, className="mt-4"),
#             ])
#         ]),
#     ])
# ], fluid=True)


# # --- 4. Define Callbacks ---
# @app.callback(
#     [
#         # Part A Outputs
#         Output('kpi-total-crashes', 'children'),
#         Output('kpi-total-injuries', 'children'),
#         Output('kpi-injuries-per-crash', 'children'),
#         Output('kpi-intersection-pct', 'children'),
#         Output('summary-table-container', 'children'),
#         # Part B Outputs
#         Output('bar-day-of-week', 'figure'),
#         Output('heatmap-hour-day', 'figure'),
#         Output('line-month', 'figure'),
#         # Part C Outputs
#         Output('box-injuries-surface', 'figure'),
#         Output('box-caption', 'children'),
#         Output('stacked-bar-crash-type', 'figure'),
#         Output('scatter-units-injuries', 'figure'),
#         # Part D Outputs
#         Output('bar-contrib-cause', 'figure'),
#         Output('pie-intersection', 'figure'),
#     ],
#     [
#         # Filter Inputs
#         Input('year-filter', 'value'),
#         Input('month-filter', 'value'),
#         Input('day-filter', 'value'),
#         Input('weather-filter', 'value'),
#         Input('lighting-filter', 'value'),
#         Input('surface-filter', 'value'),
#         Input('intersection-filter', 'value'),
#     ]
# )
# def update_dashboard(years, months, days, weather, lighting, surface, intersection):
#     dff = df.copy()

#     # Apply filters
#     if years:
#         dff = dff[dff['year'].isin(years)]
#     if months:
#         dff = dff[dff['crash_month'].isin(months)]
#     if days:
#         dff = dff[dff['crash_day_of_week'].isin(days)]
#     if weather:
#         dff = dff[dff['weather_condition'].isin(weather)]
#     if lighting:
#         dff = dff[dff['lighting_condition'].isin(lighting)]
#     if surface:
#         dff = dff[dff['roadway_surface_cond'].isin(surface)]
#     if intersection:
#         dff = dff[dff['intersection_related_i'] == intersection]
        
#     if dff.empty:
#         # Return empty figures and messages if no data matches filters
#         empty_fig = go.Figure().update_layout(title_text="No data for selected filters", xaxis={'visible': False}, yaxis={'visible': False})
#         no_data_kpi = dbc.CardBody([html.H4("N/A"), html.P("No Data")])
#         no_data_table = html.Div("No data to display in the table.")
#         return no_data_kpi, no_data_kpi, no_data_kpi, no_data_kpi, no_data_table, empty_fig, empty_fig, empty_fig, empty_fig, "", empty_fig, empty_fig, empty_fig, empty_fig

#     # --- Part A Calculations & Figures ---
#     total_crashes = len(dff)
#     total_injuries = dff['injuries_total'].sum()
#     injuries_per_crash = total_injuries / total_crashes if total_crashes > 0 else 0
#     intersection_pct = (dff['intersection_related_i'] == 'Yes').sum() / total_crashes * 100 if total_crashes > 0 else 0

#     kpi_crashes = dbc.CardBody([
#         html.H4(f"{total_crashes:,.0f}"),
#         html.P("Total Crashes")
#     ])
#     kpi_injuries = dbc.CardBody([
#         html.H4(f"{total_injuries:,.0f}"),
#         html.P("Total Injuries")
#     ])
#     kpi_ipc = dbc.CardBody([
#         html.H4(f"{injuries_per_crash:.2f}"),
#         html.P("Avg. Injuries / Crash")
#     ])
#     kpi_int_pct = dbc.CardBody([
#         html.H4(f"{intersection_pct:.1f}%"),
#         html.P("% Intersection-Related")
#     ])

#     # Summary Table
#     day_summary = dff['day_of_week_name'].value_counts().reset_index()
#     day_summary.columns = ['Day of Week', 'Total Crashes']
#     top_3_days = day_summary.nlargest(3, 'Total Crashes')['Day of Week'].tolist()
    
#     month_summary = dff.groupby('month_name')['crash_date'].count().reset_index()
#     month_summary.columns = ['Month', 'Total Crashes']
#     month_order = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
#     month_summary['Month'] = pd.Categorical(month_summary['Month'], categories=month_order, ordered=True)
#     month_summary = month_summary.sort_values('Month')
#     top_3_months = month_summary.nlargest(3, 'Total Crashes')['Month'].tolist()

#     summary_table = html.Div([
#         dbc.Row([
#             dbc.Col(dash_table.DataTable(
#                 data=day_summary.to_dict('records'),
#                 columns=[{'name': i, 'id': i} for i in day_summary.columns],
#                 style_cell={'textAlign': 'left'},
#                 style_data_conditional=[{
#                     'if': {'filter_query': '{{Day of Week}} = "{}"'.format(day)},
#                     'backgroundColor': '#D6EAF8', 'fontWeight': 'bold'
#                 } for day in top_3_days]
#             ), md=6),
#             dbc.Col(dash_table.DataTable(
#                 data=month_summary.to_dict('records'),
#                 columns=[{'name': i, 'id': i} for i in month_summary.columns],
#                 style_cell={'textAlign': 'left'},
#                  style_data_conditional=[{
#                     'if': {'filter_query': '{{Month}} = "{}"'.format(month)},
#                     'backgroundColor': '#D6EAF8', 'fontWeight': 'bold'
#                 } for month in top_3_months]
#             ), md=6)
#         ])
#     ])
    

#     # --- Part B Figures ---
#     # Bar Chart: Day of Week
#     day_counts = dff['day_of_week_name'].value_counts().sort_values(ascending=False)
#     highest_day = day_counts.index[0]
#     fig_bar_day = px.bar(
#         day_counts,
#         x=day_counts.index,
#         y=day_counts.values,
#         labels={'x': 'Day of Week', 'y': 'Number of Crashes'},
#         text_auto=True
#     )
#     fig_bar_day.update_layout(
#         title_text=f'<b>Crashes by Day of Week ({highest_day} Has the Most)</b>',
#         xaxis={'categoryorder':'total descending'}
#     )
    
#     # Heatmap: Hour vs Day
#     heatmap_data = dff.groupby(['crash_hour', 'day_of_week_name']).size().reset_index(name='count')
#     heatmap_pivot = heatmap_data.pivot_table(index='crash_hour', columns='day_of_week_name', values='count').fillna(0)
#     day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
#     heatmap_pivot = heatmap_pivot.reindex(columns=day_order)
#     peak_val = heatmap_pivot.max().max()
#     peak_hour, peak_day = heatmap_pivot.stack().idxmax()
    
#     fig_heatmap = px.imshow(
#         heatmap_pivot,
#         labels=dict(x="Day of Week", y="Hour of Day", color="Crash Count"),
#         y=heatmap_pivot.index,
#         x=heatmap_pivot.columns
#     )
#     fig_heatmap.add_annotation(x=peak_day, y=peak_hour,
#         text=f"Peak: {int(peak_val)}", showarrow=True, arrowhead=1, bgcolor="#ff7f0e")
#     fig_heatmap.update_layout(title_text='<b>Heatmap of Crashes by Hour and Day of Week</b>')

#     # Line Chart: Month
#     month_counts = dff.groupby(['year', 'month_name']).size().reset_index(name='counts')
#     month_counts['month_name'] = pd.Categorical(month_counts['month_name'], categories=month_order, ordered=True)
#     month_counts = month_counts.sort_values(['year', 'month_name'])

#     fig_line_month = px.line(
#         month_counts,
#         x='month_name',
#         y='counts',
#         color='year',
#         markers=True,
#         labels={'counts': 'Number of Crashes', 'month_name': 'Month'}
#     )
#     fig_line_month.update_layout(title_text='<b>Crashes by Month Over Time</b>')


#     # --- Part C Figures ---
#     # Box Plot
#     fig_box = px.box(
#         dff[dff['injuries_total'] < dff['injuries_total'].quantile(0.99)], # Remove extreme outliers for readability
#         x='roadway_surface_cond',
#         y='injuries_total',
#         labels={'roadway_surface_cond': 'Roadway Surface Condition', 'injuries_total': 'Total Injuries'},
#         points=False
#     )
#     median_injuries = dff.groupby('roadway_surface_cond')['injuries_total'].median().idxmax()
#     box_caption_text = f"The highest median number of injuries occurs on '{median_injuries}' surfaces."
#     fig_box.update_layout(title_text='<b>Injury Severity by Roadway Surface Condition</b>')

#     # Stacked Bar
#     lighting_crash_type = dff.groupby(['lighting_condition', 'first_crash_type']).size().reset_index(name='count')
#     totals = lighting_crash_type.groupby('lighting_condition')['count'].sum().reset_index(name='total')
#     lighting_crash_type = lighting_crash_type.merge(totals, on='lighting_condition')
#     lighting_crash_type['percentage'] = (lighting_crash_type['count'] / lighting_crash_type['total']) * 100
#     top_crash_types = dff['first_crash_type'].value_counts().nlargest(5).index
#     fig_stacked_bar = px.bar(
#         lighting_crash_type[lighting_crash_type['first_crash_type'].isin(top_crash_types)],
#         x='lighting_condition',
#         y='percentage',
#         color='first_crash_type',
#         labels={'lighting_condition': 'Lighting Condition', 'percentage': '% of Crashes'},
#         barmode='stack'
#     )
#     fig_stacked_bar.update_layout(title_text='<b>Crash Type Distribution by Lighting Condition (%)</b>')

#     # Scatter Plot
#     fig_scatter = px.scatter(
#         dff,
#         x='num_units',
#         y='injuries_total',
#         trendline='ols',
#         labels={'num_units': 'Number of Vehicles Involved', 'injuries_total': 'Total Injuries'}
#     )
#     fig_scatter.update_layout(title_text='<b>Injuries vs. Number of Vehicles Involved</b>')


#     # --- Part D Figures ---
#     # Horizontal Bar
#     cause_counts = dff['prim_contributory_cause'].value_counts().nlargest(10).sort_values(ascending=True)
#     top_cause = cause_counts.index[-1]
#     fig_bar_cause = px.bar(
#         cause_counts,
#         x=cause_counts.values,
#         y=cause_counts.index,
#         orientation='h',
#         text_auto=True
#     )
#     fig_bar_cause.update_layout(
#         title_text=f"<b>Top 10 Crash Causes (Top Cause: {top_cause})</b>",
#         xaxis_title='Number of Crashes',
#         yaxis_title='Primary Contributory Cause',
#         margin=dict(l=250)
#     )

#     # Pie Chart
#     intersection_counts = dff['intersection_related_i'].value_counts()
#     fig_pie = px.pie(
#         values=intersection_counts.values,
#         names=intersection_counts.index,
#         hole=0.4,
#         color_discrete_sequence=px.colors.sequential.Blues_r
#     )
#     fig_pie.update_layout(
#         title_text="<b>What % of crashes are intersection-related?</b>",
#         annotations=[dict(text=f'{intersection_pct:.1f}%', x=0.5, y=0.5, font_size=20, showarrow=False)]
#     )

#     return (
#         kpi_crashes, kpi_injuries, kpi_ipc, kpi_int_pct, summary_table,
#         fig_bar_day, fig_heatmap, fig_line_month,
#         fig_box, box_caption_text, fig_stacked_bar, fig_scatter,
#         fig_bar_cause, fig_pie
#     )

# # --- 5. Run the App ---
# if __name__ == '__main__':
#     app.run(debug=True)

# import pandas as pd
# import plotly.express as px
# import plotly.graph_objects as go
# import dash
# import dash_bootstrap_components as dbc
# from dash import dcc, html, dash_table
# from dash.dependencies import Input, Output

# # --- 1. Data Loading and Preparation ---

# # Load the dataset
# try:
#     df = pd.read_csv('traffic_accidents.csv')
# except FileNotFoundError:
#     print("Error: 'traffic_accidents.csv' not found. Please place the file in the same directory as the script.")
#     exit()

# # Clean column names for easier access
# df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_').str.replace('(', '').str.replace(')', '')

# # Data type conversions and feature engineering
# df['crash_date'] = pd.to_datetime(df['crash_date'], errors='coerce')
# df['year'] = df['crash_date'].dt.year
# df = df.dropna(subset=['crash_date', 'crash_hour', 'crash_day_of_week', 'crash_month']) # Drop rows where essential date/time info is missing

# # Standardize boolean-like columns
# df['intersection_related_i'] = df['intersection_related_i'].fillna('N').apply(lambda x: 'Yes' if x.strip() == 'Y' else 'No')

# # Map day and month numbers to names for better readability
# day_map = {1: 'Sunday', 2: 'Monday', 3: 'Tuesday', 4: 'Wednesday', 5: 'Thursday', 6: 'Friday', 7: 'Saturday'}
# month_map = {1: 'Jan', 2: 'Feb', 3: 'Mar', 4: 'Apr', 5: 'May', 6: 'Jun', 7: 'Jul', 8: 'Aug', 9: 'Sep', 10: 'Oct', 11: 'Nov', 12: 'Dec'}
# df['day_of_week_name'] = df['crash_day_of_week'].map(day_map)
# df['month_name'] = df['crash_month'].map(month_map)


# # --- 2. Initialize the Dash App ---
# app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
# server = app.server

# # --- 3. Define App Layout ---

# # Reusable styles
# CARD_STYLE = {
#     "padding": "20px",
#     "border-radius": "10px",
#     "box-shadow": "0 4px 8px 0 rgba(0,0,0,0.2)",
#     "transition": "0.3s",
# }

# # --- Filter Controls ---
# controls = dbc.Card(
#     [
#         dbc.Row([
#             dbc.Col(html.H4("Filters"), width=12, className="mb-3")
#         ]),
#         dbc.Row([
#             dbc.Col(dcc.Dropdown(
#                 id='year-filter',
#                 options=[{'label': str(year), 'value': year} for year in sorted(df['year'].unique())],
#                 multi=True,
#                 placeholder='Select Year(s)'
#             ), md=4),
#             dbc.Col(dcc.Dropdown(
#                 id='month-filter',
#                 options=[{'label': month, 'value': num} for num, month in month_map.items()],
#                 multi=True,
#                 placeholder='Select Month(s)'
#             ), md=4),
#             dbc.Col(dcc.Dropdown(
#                 id='day-filter',
#                 options=[{'label': day, 'value': num} for num, day in day_map.items()],
#                 multi=True,
#                 placeholder='Select Day(s) of Week'
#             ), md=4),
#         ]),
#         dbc.Row([
#             dbc.Col(dcc.Dropdown(
#                 id='weather-filter',
#                 options=[{'label': i, 'value': i} for i in df['weather_condition'].unique() if pd.notna(i)],
#                 multi=True,
#                 placeholder='Select Weather Condition(s)'
#             ), md=4),
#             dbc.Col(dcc.Dropdown(
#                 id='lighting-filter',
#                 options=[{'label': i, 'value': i} for i in df['lighting_condition'].unique() if pd.notna(i)],
#                 multi=True,
#                 placeholder='Select Lighting Condition(s)'
#             ), md=4),
#             dbc.Col(dcc.Dropdown(
#                 id='surface-filter',
#                 options=[{'label': i, 'value': i} for i in df['roadway_surface_cond'].unique() if pd.notna(i)],
#                 multi=True,
#                 placeholder='Select Surface Condition(s)'
#             ), md=4),
#         ], className="mt-3"),
#         dbc.Row([
#              dbc.Col(dcc.Dropdown(
#                 id='intersection-filter',
#                 options=[{'label': 'Yes', 'value': 'Yes'}, {'label': 'No', 'value': 'No'}],
#                 placeholder='Intersection Related?'
#             ), md=4),
#         ], className="mt-3")
#     ],
#     body=True,
#     className="mb-4"
# )

# # --- App Layout ---
# app.layout = dbc.Container([
#     # Header
#     dbc.Row([
#         dbc.Col(html.H1("Chicago Traffic Accidents Dashboard", className="text-center text-primary mt-4 mb-4"), width=12)
#     ]),
#     # Filters
#     dbc.Row([
#         dbc.Col(controls, width=12)
#     ]),
#     # Tabs
#     dcc.Tabs(id="tabs", children=[
#         # --- Tab A: Overview ---
#         dcc.Tab(label='Home / Overview', children=[
#             dbc.Row([
#                 # KPI Cards
#                 dbc.Col(dbc.Card(id='kpi-total-crashes', style=CARD_STYLE), md=3, className="mt-4"),
#                 dbc.Col(dbc.Card(id='kpi-total-injuries', style=CARD_STYLE), md=3, className="mt-4"),
#                 dbc.Col(dbc.Card(id='kpi-injuries-per-crash', style=CARD_STYLE), md=3, className="mt-4"),
#                 dbc.Col(dbc.Card(id='kpi-intersection-pct', style=CARD_STYLE), md=3, className="mt-4"),
#             ]),
#             dbc.Row([
#                 dbc.Col(html.H4("Summary Table: Crashes by Day and Month", className="mt-5 mb-3"), width=12),
#                 dbc.Col(id='summary-table-container', width=12)
#             ])
#         ]),
#         # --- Tab B: Crash Timings ---
#         dcc.Tab(label='When Crashes Happen', children=[
#             dbc.Row([
#                 dbc.Col(dcc.Graph(id='bar-day-of-week'), md=6, className="mt-4"),
#                 dbc.Col(dcc.Graph(id='heatmap-hour-day'), md=6, className="mt-4"),
#             ]),
#             dbc.Row([
#                 dbc.Col(dcc.Graph(id='line-month'), width=12, className="mt-4"),
#             ])
#         ]),
#         # --- Tab C: Severity & Conditions ---
#         dcc.Tab(label='Severity & Conditions', children=[
#             dbc.Row([
#                 dbc.Col([
#                     dcc.Graph(id='box-injuries-surface', style={'height': '500px'}),
#                     html.P(id='box-caption', className="text-center fst-italic")
#                 ], md=6, className="mt-4"),
#                 dbc.Col([
#                     dcc.Graph(id='stacked-bar-crash-type', style={'height': '500px'}),
#                      html.P("Insight: Daylight hours see a higher proportion of rear-end and turning crashes, while nighttime crashes have a higher share of fixed object collisions.", className="text-center fst-italic")
#                 ], md=6, className="mt-4"),
#             ]),
#              dbc.Row([
#                 dbc.Col([
#                     dcc.Graph(id='scatter-units-injuries', style={'height': '500px'}),
#                     html.P("Takeaway: Crashes involving more vehicles tend to result in a higher number of total injuries, though many multi-vehicle incidents still result in zero injuries.", className="text-center fst-italic")
#                 ], width=12, className="mt-4"),
#             ])
#         ]),
#         # --- Tab D: Contributors & Locations ---
#         dcc.Tab(label='Contributors & Locations', children=[
#             dbc.Row([
#                 dbc.Col(dcc.Graph(id='bar-contrib-cause'), md=8, className="mt-4"),
#                 dbc.Col(dcc.Graph(id='pie-intersection'), md=4, className="mt-4"),
#             ])
#         ]),
#     ])
# ], fluid=True)


# # --- 4. Define Callbacks ---
# @app.callback(
#     [
#         # Part A Outputs
#         Output('kpi-total-crashes', 'children'),
#         Output('kpi-total-injuries', 'children'),
#         Output('kpi-injuries-per-crash', 'children'),
#         Output('kpi-intersection-pct', 'children'),
#         Output('summary-table-container', 'children'),
#         # Part B Outputs
#         Output('bar-day-of-week', 'figure'),
#         Output('heatmap-hour-day', 'figure'),
#         Output('line-month', 'figure'),
#         # Part C Outputs
#         Output('box-injuries-surface', 'figure'),
#         Output('box-caption', 'children'),
#         Output('stacked-bar-crash-type', 'figure'),
#         Output('scatter-units-injuries', 'figure'),
#         # Part D Outputs
#         Output('bar-contrib-cause', 'figure'),
#         Output('pie-intersection', 'figure'),
#     ],
#     [
#         # Filter Inputs
#         Input('year-filter', 'value'),
#         Input('month-filter', 'value'),
#         Input('day-filter', 'value'),
#         Input('weather-filter', 'value'),
#         Input('lighting-filter', 'value'),
#         Input('surface-filter', 'value'),
#         Input('intersection-filter', 'value'),
#     ]
# )
# def update_dashboard(years, months, days, weather, lighting, surface, intersection):
#     dff = df.copy()

#     # Apply filters
#     if years:
#         dff = dff[dff['year'].isin(years)]
#     if months:
#         dff = dff[dff['crash_month'].isin(months)]
#     if days:
#         dff = dff[dff['crash_day_of_week'].isin(days)]
#     if weather:
#         dff = dff[dff['weather_condition'].isin(weather)]
#     if lighting:
#         dff = dff[dff['lighting_condition'].isin(lighting)]
#     if surface:
#         dff = dff[dff['roadway_surface_cond'].isin(surface)]
#     if intersection:
#         dff = dff[dff['intersection_related_i'] == intersection]
        
#     if dff.empty:
#         # Return empty figures and messages if no data matches filters
#         empty_fig = go.Figure().update_layout(title_text="No data for selected filters", xaxis={'visible': False}, yaxis={'visible': False})
#         no_data_kpi = dbc.CardBody([html.H4("N/A"), html.P("No Data")])
#         no_data_table = html.Div("No data to display in the table.")
#         return no_data_kpi, no_data_kpi, no_data_kpi, no_data_kpi, no_data_table, empty_fig, empty_fig, empty_fig, empty_fig, "", empty_fig, empty_fig, empty_fig, empty_fig

#     # --- Part A Calculations & Figures ---
#     total_crashes = len(dff)
#     total_injuries = dff['injuries_total'].sum()
#     injuries_per_crash = total_injuries / total_crashes if total_crashes > 0 else 0
#     intersection_pct = (dff['intersection_related_i'] == 'Yes').sum() / total_crashes * 100 if total_crashes > 0 else 0

#     kpi_crashes = dbc.CardBody([
#         html.H4(f"{total_crashes:,.0f}"),
#         html.P("Total Crashes")
#     ])
#     kpi_injuries = dbc.CardBody([
#         html.H4(f"{total_injuries:,.0f}"),
#         html.P("Total Injuries")
#     ])
#     kpi_ipc = dbc.CardBody([
#         html.H4(f"{injuries_per_crash:.2f}"),
#         html.P("Avg. Injuries / Crash")
#     ])
#     kpi_int_pct = dbc.CardBody([
#         html.H4(f"{intersection_pct:.1f}%"),
#         html.P("% Intersection-Related")
#     ])

#     # Summary Table
#     day_summary = dff['day_of_week_name'].value_counts().reset_index()
#     day_summary.columns = ['Day of Week', 'Total Crashes']
#     top_3_days = day_summary.nlargest(3, 'Total Crashes')['Day of Week'].tolist()
    
#     month_summary = dff.groupby('month_name')['crash_date'].count().reset_index()
#     month_summary.columns = ['Month', 'Total Crashes']
#     month_order = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
#     month_summary['Month'] = pd.Categorical(month_summary['Month'], categories=month_order, ordered=True)
#     month_summary = month_summary.sort_values('Month')
#     top_3_months = month_summary.nlargest(3, 'Total Crashes')['Month'].tolist()

#     summary_table = html.Div([
#         dbc.Row([
#             dbc.Col(dash_table.DataTable(
#                 data=day_summary.to_dict('records'),
#                 columns=[{'name': i, 'id': i} for i in day_summary.columns],
#                 style_cell={'textAlign': 'left'},
#                 style_data_conditional=[{
#                     'if': {'filter_query': '{{Day of Week}} = "{}"'.format(day)},
#                     'backgroundColor': '#D6EAF8', 'fontWeight': 'bold'
#                 } for day in top_3_days]
#             ), md=6),
#             dbc.Col(dash_table.DataTable(
#                 data=month_summary.to_dict('records'),
#                 columns=[{'name': i, 'id': i} for i in month_summary.columns],
#                 style_cell={'textAlign': 'left'},
#                  style_data_conditional=[{
#                     'if': {'filter_query': '{{Month}} = "{}"'.format(month)},
#                     'backgroundColor': '#D6EAF8', 'fontWeight': 'bold'
#                 } for month in top_3_months]
#             ), md=6)
#         ])
#     ])
    

#     # --- Part B Figures ---
#     # Bar Chart: Day of Week
#     day_counts = dff['day_of_week_name'].value_counts().sort_values(ascending=False)
#     highest_day = day_counts.index[0]
#     fig_bar_day = px.bar(
#         day_counts,
#         x=day_counts.index,
#         y=day_counts.values,
#         labels={'x': 'Day of Week', 'y': 'Number of Crashes'},
#         text_auto=True
#     )
#     fig_bar_day.update_layout(
#         title_text=f'<b>Crashes by Day of Week ({highest_day} Has the Most)</b>',
#         xaxis={'categoryorder':'total descending'}
#     )
    
#     # Heatmap: Hour vs Day
#     heatmap_data = dff.groupby(['crash_hour', 'day_of_week_name']).size().reset_index(name='count')
#     heatmap_pivot = heatmap_data.pivot_table(index='crash_hour', columns='day_of_week_name', values='count').fillna(0)
#     day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
#     heatmap_pivot = heatmap_pivot.reindex(columns=day_order)
#     peak_val = heatmap_pivot.max().max()
#     peak_hour, peak_day = heatmap_pivot.stack().idxmax()
    
#     fig_heatmap = px.imshow(
#         heatmap_pivot,
#         labels=dict(x="Day of Week", y="Hour of Day", color="Crash Count"),
#         y=heatmap_pivot.index,
#         x=heatmap_pivot.columns
#     )
#     fig_heatmap.add_annotation(x=peak_day, y=peak_hour,
#         text=f"Peak: {int(peak_val)}", showarrow=True, arrowhead=1, bgcolor="#ff7f0e")
#     fig_heatmap.update_layout(title_text='<b>Heatmap of Crashes by Hour and Day of Week</b>')

#     # Line Chart: Month
#     month_counts = dff.groupby(['year', 'month_name']).size().reset_index(name='counts')
#     month_counts['month_name'] = pd.Categorical(month_counts['month_name'], categories=month_order, ordered=True)
#     month_counts = month_counts.sort_values(['year', 'month_name'])

#     fig_line_month = px.line(
#         month_counts,
#         x='month_name',
#         y='counts',
#         color='year',
#         markers=True,
#         labels={'counts': 'Number of Crashes', 'month_name': 'Month'}
#     )
#     fig_line_month.update_layout(title_text='<b>Crashes by Month Over Time</b>')


#     # --- Part C Figures ---
#     # Box Plot
#     fig_box = px.box(
#         dff[dff['injuries_total'] < dff['injuries_total'].quantile(0.99)], # Remove extreme outliers for readability
#         x='roadway_surface_cond',
#         y='injuries_total',
#         labels={'roadway_surface_cond': 'Roadway Surface Condition', 'injuries_total': 'Total Injuries'},
#         points=False
#     )
#     median_injuries = dff.groupby('roadway_surface_cond')['injuries_total'].median().idxmax()
#     box_caption_text = f"The highest median number of injuries occurs on '{median_injuries}' surfaces."
#     fig_box.update_layout(title_text='<b>Injury Severity by Roadway Surface Condition</b>')

#     # Stacked Bar
#     lighting_crash_type = dff.groupby(['lighting_condition', 'first_crash_type']).size().reset_index(name='count')
#     totals = lighting_crash_type.groupby('lighting_condition')['count'].sum().reset_index(name='total')
#     lighting_crash_type = lighting_crash_type.merge(totals, on='lighting_condition')
#     lighting_crash_type['percentage'] = (lighting_crash_type['count'] / lighting_crash_type['total']) * 100
#     top_crash_types = dff['first_crash_type'].value_counts().nlargest(5).index
#     fig_stacked_bar = px.bar(
#         lighting_crash_type[lighting_crash_type['first_crash_type'].isin(top_crash_types)],
#         x='lighting_condition',
#         y='percentage',
#         color='first_crash_type',
#         labels={'lighting_condition': 'Lighting Condition', 'percentage': '% of Crashes'},
#         barmode='stack'
#     )
#     fig_stacked_bar.update_layout(title_text='<b>Crash Type Distribution by Lighting Condition (%)</b>')

#     # Scatter Plot
#     fig_scatter = px.scatter(
#         dff,
#         x='num_units',
#         y='injuries_total',
#         # trendline='ols', # This line requires the 'statsmodels' package. Commented out to prevent error.
#         labels={'num_units': 'Number of Vehicles Involved', 'injuries_total': 'Total Injuries'}
#     )
#     fig_scatter.update_layout(title_text='<b>Injuries vs. Number of Vehicles Involved</b>')


#     # --- Part D Figures ---
#     # Horizontal Bar
#     cause_counts = dff['prim_contributory_cause'].value_counts().nlargest(10).sort_values(ascending=True)
#     top_cause = cause_counts.index[-1]
#     fig_bar_cause = px.bar(
#         cause_counts,
#         x=cause_counts.values,
#         y=cause_counts.index,
#         orientation='h',
#         text_auto=True
#     )
#     fig_bar_cause.update_layout(
#         title_text=f"<b>Top 10 Crash Causes (Top Cause: {top_cause})</b>",
#         xaxis_title='Number of Crashes',
#         yaxis_title='Primary Contributory Cause',
#         margin=dict(l=250)
#     )

#     # Pie Chart
#     intersection_counts = dff['intersection_related_i'].value_counts()
#     fig_pie = px.pie(
#         values=intersection_counts.values,
#         names=intersection_counts.index,
#         hole=0.4,
#         color_discrete_sequence=px.colors.sequential.Blues_r
#     )
#     fig_pie.update_layout(
#         title_text="<b>What % of crashes are intersection-related?</b>",
#         annotations=[dict(text=f'{intersection_pct:.1f}%', x=0.5, y=0.5, font_size=20, showarrow=False)]
#     )

#     return (
#         kpi_crashes, kpi_injuries, kpi_ipc, kpi_int_pct, summary_table,
#         fig_bar_day, fig_heatmap, fig_line_month,
#         fig_box, box_caption_text, fig_stacked_bar, fig_scatter,
#         fig_bar_cause, fig_pie
#     )

# # --- 5. Run the App ---
# if __name__ == '__main__':
#     app.run(debug=True)


import pandas as pd
import plotly.express as px
import dash
import dash_bootstrap_components as dbc
from dash import dcc, html
from dash.dependencies import Input, Output

# --- Data Loading and Preparation ---
# Load the dataset directly from the local Excel file in the project folder
df = pd.read_excel('traffic_accidents.xlsx', engine='openpyxl')

# Clean column names for easier access
df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_').str.replace('(', '').str.replace(')', '')

# Convert crash_date to datetime and extract year, month, and day of week
df['crash_date'] = pd.to_datetime(df['crash_date'], errors='coerce')
df['year'] = df['crash_date'].dt.year
df['month'] = df['crash_date'].dt.month
df['day_of_week'] = df['crash_date'].dt.day_name()

# Convert intersection_related_i to a more readable format
df['intersection_related_i'] = df['intersection_related_i'].apply(lambda x: 'Yes' if x == 'Y' else 'No')

# --- App Initialization ---
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server # Expose the server for Render

# --- Controls Layout ---
controls = dbc.Card(
    [
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.Label("Year"),
                        dcc.Dropdown(
                            id='year-filter',
                            options=[{'label': str(year), 'value': year} for year in sorted(df['year'].unique())],
                            multi=True,
                            placeholder="Select Year(s)"
                        ),
                    ],
                    md=2
                ),
                dbc.Col(
                    [
                        html.Label("Month"),
                        dcc.Dropdown(
                            id='month-filter',
                            options=[{'label': str(month), 'value': month} for month in sorted(df['month'].unique())],
                            multi=True,
                            placeholder="Select Month(s)"
                        ),
                    ],
                    md=2
                ),
                dbc.Col(
                    [
                        html.Label("Day of Week"),
                        dcc.Dropdown(
                            id='day-filter',
                            options=[{'label': day, 'value': day} for day in df['day_of_week'].unique()],
                            multi=True,
                            placeholder="Select Day(s)"
                        ),
                    ],
                    md=2
                ),
                dbc.Col(
                    [
                        html.Label("Intersection Related"),
                        dcc.Dropdown(
                            id='intersection-filter',
                            options=[{'label': i, 'value': i} for i in df['intersection_related_i'].unique()],
                            placeholder="Yes/No"
                        ),
                    ],
                    md=2
                ),
                 dbc.Col(
                    [
                        html.Label("Lighting Condition"),
                        dcc.Dropdown(
                            id='lighting-filter',
                            options=[{'label': i, 'value': i} for i in df['lighting_condition'].unique()],
                            placeholder="Select Lighting"
                        ),
                    ],
                    md=2
                ),
                 dbc.Col(
                    [
                        html.Label("Weather"),
                        dcc.Dropdown(
                            id='weather-filter',
                            options=[{'label': i, 'value': i} for i in df['weather_condition'].unique()],
                            placeholder="Select Weather"
                        ),
                    ],
                    md=2
                ),
            ]
        )
    ],
    body=True,
    className="mb-4"
)

# --- App Layout ---
app.layout = dbc.Container([
    # Header
    dbc.Row([
        dbc.Col(html.H1("Chicago Traffic Accidents Dashboard", className="text-center text-primary mt-4 mb-4"), width=12)
    ]),
    # Filters
    dbc.Row([
        dbc.Col(controls, width=12)
    ]),

    # Tabs
    dcc.Tabs(id="tabs", children=[
        # --- Tab A: Overview ---
        dcc.Tab(label='Overview', children=[
            dbc.Row(
                [
                    dbc.Col(dbc.Card(id='kpi-total-crashes', className="text-center p-3"), md=3),
                    dbc.Col(dbc.Card(id='kpi-total-injuries', className="text-center p-3"), md=3),
                    dbc.Col(dbc.Card(id='kpi-injuries-per-crash', className="text-center p-3"), md=3),
                    dbc.Col(dbc.Card(id='kpi-intersection-related', className="text-center p-3"), md=3),
                ], className="mt-4"
            ),
            dbc.Row(
                [
                    dbc.Col(dcc.Graph(id='summary-table-day'), md=6),
                    dbc.Col(dcc.Graph(id='summary-table-month'), md=6),
                ], className="mt-4"
            )
        ]),

        # --- Tab B: When Crashes Happen ---
        dcc.Tab(label='When Crashes Happen', children=[
            dbc.Row([
                dbc.Col(dcc.Graph(id='bar-day-of-week'), md=6, className="mt-4"),
                dbc.Col(dcc.Graph(id='heatmap-hour-day'), md=6, className="mt-4"),
            ]),
             dbc.Row([
                dbc.Col(dcc.Graph(id='line-month'), width=12, className="mt-4"),
            ])
        ]),

        # --- Tab C: Severity & Conditions ---
        dcc.Tab(label='Severity & Conditions', children=[
            dbc.Row([
                dbc.Col([
                    dcc.Graph(id='box-injuries-surface', style={'height': '500px'}),
                    html.P(id='box-caption', className="text-center fst-italic")
                ], md=6, className="mt-4"),
                dbc.Col([
                    dcc.Graph(id='stacked-bar-crash-type', style={'height': '500px'}),
                     html.P("Insight: Daylight hours see a higher proportion of rear-end and turning crashes, while nighttime crashes have a higher share of fixed object collisions.", className="text-center fst-italic")
                ], md=6, className="mt-4"),
            ]),
             dbc.Row([
                dbc.Col([
                    dcc.Graph(id='scatter-units-injuries', style={'height': '500px'}),
                    html.P("Takeaway: Crashes involving more vehicles tend to result in a higher number of total injuries, though many multi-vehicle incidents still result in zero injuries.", className="text-center fst-italic")
                ], width=12, className="mt-4"),
            ])
        ]),
        # --- Tab D: Contributors & Locations ---
        dcc.Tab(label='Contributors & Locations', children=[
            dbc.Row([
                dbc.Col(dcc.Graph(id='bar-top-causes'), md=8, className="mt-4"),
                dbc.Col(dcc.Graph(id='pie-intersection'), md=4, className="mt-4"),
            ])
        ])
    ])
], fluid=True)


# --- Callback for Interactivity ---
@app.callback(
    [
        Output('kpi-total-crashes', 'children'),
        Output('kpi-total-injuries', 'children'),
        Output('kpi-injuries-per-crash', 'children'),
        Output('kpi-intersection-related', 'children'),
        Output('summary-table-day', 'figure'),
        Output('summary-table-month', 'figure'),
        Output('bar-day-of-week', 'figure'),
        Output('heatmap-hour-day', 'figure'),
        Output('line-month', 'figure'),
        Output('box-injuries-surface', 'figure'),
        Output('box-caption', 'children'),
        Output('stacked-bar-crash-type', 'figure'),
        Output('scatter-units-injuries', 'figure'),
        Output('bar-top-causes', 'figure'),
        Output('pie-intersection', 'figure')
    ],
    [
        Input('year-filter', 'value'),
        Input('month-filter', 'value'),
        Input('day-filter', 'value'),
        Input('intersection-filter', 'value'),
        Input('lighting-filter', 'value'),
        Input('weather-filter', 'value')
    ]
)
def update_dashboard(years, months, days, intersection, lighting, weather):
    dff = df.copy()

    # Apply filters
    if years:
        dff = dff[dff['year'].isin(years)]
    if months:
        dff = dff[dff['month'].isin(months)]
    if days:
        dff = dff[dff['day_of_week'].isin(days)]
    if intersection:
        dff = dff[dff['intersection_related_i'] == intersection]
    if lighting:
        dff = dff[dff['lighting_condition'] == lighting]
    if weather:
        dff = dff[dff['weather_condition'] == weather]

    # --- Handle No Data ---
    if dff.empty:
        no_data_fig = {
            "layout": {
                "xaxis": {"visible": False},
                "yaxis": {"visible": False},
                "annotations": [{
                    "text": "No data for selected filters",
                    "xref": "paper", "yref": "paper",
                    "showarrow": False, "font": {"size": 20}
                }]
            }
        }
        no_data_kpi = [html.H3("N/A"), html.P("No Data")]
        return no_data_kpi, no_data_kpi, no_data_kpi, no_data_kpi, no_data_fig, no_data_fig, no_data_fig, no_data_fig, no_data_fig, no_data_fig, "", no_data_fig, no_data_fig, no_data_fig, no_data_fig

    # --- Calculations ---
    total_crashes = len(dff)
    total_injuries = dff['injuries_total'].sum()
    injuries_per_crash = total_injuries / total_crashes if total_crashes > 0 else 0
    intersection_pct = (dff['intersection_related_i'] == 'Yes').mean() * 100

    # --- Part A: Overview ---
    kpi_crashes = [html.H3(f"{total_crashes:,}"), html.P("Total Crashes")]
    kpi_injuries = [html.H3(f"{int(total_injuries):,d}"), html.P("Total Injuries")]
    kpi_inj_per_crash = [html.H3(f"{injuries_per_crash:.2f}"), html.P("Avg. Injuries / Crash")]
    kpi_intersect = [html.H3(f"{intersection_pct:.1f}%"), html.P("% Intersection-Related")]

    # Summary Tables
    day_summary = dff['day_of_week'].value_counts().nlargest(3)
    month_summary = dff['month'].value_counts().nlargest(3)

    fig_summary_day = px.bar(day_summary, title="<b>Top 3 Days by Crashes</b>", text_auto=True)
    fig_summary_month = px.bar(month_summary, title="<b>Top 3 Months by Crashes</b>", text_auto=True)

    # --- Part B: When Crashes Happen ---
    # Bar Chart Day of Week
    day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    day_counts = dff['day_of_week'].value_counts().reindex(day_order)
    highest_day = day_counts.idxmax()
    fig_bar_day = px.bar(
        day_counts,
        x=day_counts.index,
        y=day_counts.values,
        labels={'x': 'Day of Week', 'y': 'Number of Crashes'},
        text_auto=True
    )
    fig_bar_day.update_layout(title_text=f'<b>Crashes by Day of Week (Highest: {highest_day})</b>')


    # Heatmap
    heatmap_data = dff.groupby(['crash_hour', 'day_of_week']).size().reset_index(name='count')
    heatmap_pivot = heatmap_data.pivot_table(index='crash_hour', columns='day_of_week', values='count').reindex(columns=day_order)
    peak_cell = heatmap_data.loc[heatmap_data['count'].idxmax()]
    fig_heatmap = px.imshow(
        heatmap_pivot,
        labels=dict(x="Day of Week", y="Hour of Day", color="Crash Count"),
        y=heatmap_pivot.index,
        x=heatmap_pivot.columns,
        title="<b>Crash Heatmap: Hour vs. Day of Week</b>"
    )
    fig_heatmap.add_annotation(x=peak_cell['day_of_week'], y=peak_cell['crash_hour'],
                               text=f"Peak: {int(peak_cell['count'])}", showarrow=True, arrowhead=1)

    # Line Chart
    month_counts = dff.groupby('month').size()
    fig_line_month = px.line(
        x=month_counts.index,
        y=month_counts.values,
        labels={'x': 'Month', 'y': 'Number of Crashes'},
        title='<b>Crashes by Month</b>',
        markers=True
    )

    # --- Part C: Severity & Conditions ---
    # Box Plot
    highest_median_surface = dff.groupby('roadway_surface_cond')['injuries_total'].median().idxmax()
    box_caption_text = f"The highest median injury count occurs on '{highest_median_surface}' surfaces."
    fig_box = px.box(
        dff,
        x='roadway_surface_cond',
        y='injuries_total',
        labels={'roadway_surface_cond': 'Roadway Surface Condition', 'injuries_total': 'Total Injuries'},
        title='<b>Injury Severity by Roadway Surface Condition</b>'
    )

    # Stacked Bar
    crash_type_by_light = dff.groupby(['lighting_condition', 'first_crash_type']).size().unstack(fill_value=0)
    crash_type_pct = crash_type_by_light.div(crash_type_by_light.sum(axis=1), axis=0) * 100
    fig_stacked_bar = px.bar(
        crash_type_pct,
        x=crash_type_pct.index,
        y=crash_type_pct.columns,
        labels={'x': 'Lighting Condition', 'y': 'Percentage of Crashes'},
        barmode='stack'
    )
    fig_stacked_bar.update_layout(title_text='<b>Crash Type Distribution by Lighting Condition (%)</b>')

    # Scatter Plot
    fig_scatter = px.scatter(
        dff,
        x='num_units',
        y='injuries_total',
        trendline='ols',
        labels={'num_units': 'Number of Vehicles Involved', 'injuries_total': 'Total Injuries'},
        title='<b>Total Injuries vs. Number of Vehicles Involved</b>'
    )

    # --- Part D: Contributors & Locations ---
    # Horizontal Bar
    top_10_causes = dff['prim_contributory_cause'].value_counts().nlargest(10).sort_values(ascending=True)
    top_cause = top_10_causes.index[-1]
    fig_bar_causes = px.bar(
        top_10_causes,
        x=top_10_causes.values,
        y=top_10_causes.index,
        orientation='h',
        text_auto=True
    )
    fig_bar_causes.update_layout(
        title_text=f'<b>Top 10 Primary Crash Causes (#1: {top_cause})</b>',
        xaxis_title='Number of Crashes',
        yaxis_title='Primary Cause'
    )

    # Pie Chart
    intersection_counts = dff['intersection_related_i'].value_counts()
    fig_pie = px.pie(
        intersection_counts,
        names=intersection_counts.index,
        values=intersection_counts.values,
        title='<b>What % of crashes are intersection-related?</b>',
        hole=0.4
    )
    fig_pie.update_traces(textinfo='percent+label')

    return (
        kpi_crashes, kpi_injuries, kpi_inj_per_crash, kpi_intersect,
        fig_summary_day, fig_summary_month,
        fig_bar_day, fig_heatmap, fig_line_month,
        fig_box, box_caption_text, fig_stacked_bar, fig_scatter,
        fig_bar_causes, fig_pie
    )

# --- Run the App ---
if __name__ == '__main__':
    app.run(debug=True)


