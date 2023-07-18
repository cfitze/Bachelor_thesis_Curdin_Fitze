import pickle
import dash
import pandas as pd
from dash import html, dcc
import dash_bootstrap_components as dbc





app = dash.Dash(__name__, use_pages=True, external_stylesheets=[dbc.themes.SPACELAB]) #, assets_folder='assets')

# #Import the data from the Excel file from Solextron via a pickle file
# import_excel = pickle.load(open("BA_23FS_Curdin_Fitze_5_7_9_11_13_TSextract.pickle", "rb"))

# # Get the column names of the imported Excel file
# columns_available = import_excel.columns.tolist()

# # columns_available_without_datetime_inital = columns_available[1:6]
# columns_available_without_datetime = columns_available[1:]

# # Convert DateTime column to datetime format
# datetime_column = pd.to_datetime(import_excel['DateTime'])

# # Create a new dataframe with only the DateTime column
# datetime_column_frame = import_excel.iloc[:,[0]]

# #Get the initial selected columns and the initail data without the DateTime column
# initial_selected_columns = ['Solar [kWh]','SelfConsumption [kWh]', 'Demand [kWh]', 'Net Grid Import/Export [kWh]', 'Battery [kWh]']  # Set the initial selected columns as a list
# initial_data_without_datetime = import_excel.iloc[:, 1:]  # Exclude the first column (DateTime)

# # Get the first and last dates from the DateTime column
# initial_first_date = import_excel['DateTime'].iloc[0]
# initial_last_date = import_excel['DateTime'].iloc[10000]


sidebar = dbc.Nav(
            [
                dbc.NavLink(
                    [
                        html.Div(page["name"], className="ms-2"),
                    ],
                    href=page["path"],
                    active="exact",
                )
                for page in dash.page_registry.values()
            ],
            vertical=True,
            pills=True,
            className="bg-light",
)



app.layout = dbc.Container([
    dbc.Row([
        dbc.Col(html.Div("Python Dash Application meiner Bachelor Thesis",
                         style={'fontSize':30, 'textAlign':'center'}))
    ]),

    html.Hr(),

    dbc.Row(
        [
            dbc.Col(
                [
                    sidebar
                ], xs=4, sm=4, md=2, lg=2, xl=2, xxl=2),

            dbc.Col(
                [
                    dash.page_container
                ], xs=8, sm=8, md=10, lg=10, xl=10, xxl=10)
        ]
    ),

    # Including the Store in the layout
    # dcc.Store(
    #     id='main_store', 
    #     data={
    #         'initial_data_without_datetime': initial_data_without_datetime.to_dict('records'),
    #         'datetime_column': datetime_column_frame.to_dict('records'),
    #         'initial_first_date': str(initial_first_date),
    #         'initial_last_date': str(initial_last_date),
    #         'initial_selected_columns': initial_selected_columns
    #     }
    # ),
], fluid=True)


if __name__ == "__main__":
    # app.run(port=9050, debug=True, dev_tools_ui=True)
    app.run(debug=True, dev_tools_ui=True)

    # debug=True, # port=8050, # host='0.0.0.0', # dev_tools_ui=True, ll dev_tools_hot_reload=True, # ev_tools_hot_reload_interval=1000,
    # dev_tools_silence_routes_logging=False,# mode='inline'# )
    # Run the Dash application
    # app.run_server(debug=True, mode='inline',dev_tools_ui=True,)



# import webapp2
# import webapp2_profiler

# class MainHandler(webapp2.RequestHandler):
#     def get(self):
#         # Your code logic here

# app = webapp2.WSGIApplication([
#     ('/', MainHandler),
# ], debug=True)

# app = webapp2_profiler.ProfilerWSGIMiddleware(app)