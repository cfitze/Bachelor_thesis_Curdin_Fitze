import base64
import dash
from dash import dcc, html, callback, Output, Input
import plotly.express as px
import dash_bootstrap_components as dbc


dash.register_page(__name__, path='/bachelor-thesis', name='Bachelor Thesis', order=7) # is a subpage of the home page


# Define the layout for the PDF page
layout = html.Div([
    html.Div([
        html.H1("Bachelor Thesis", className="pages-header"),
        html.P("Willkommen bei der Bachelor Thesis von Curdin Fitze.", style={"text-align": "center"})
    ], style={"margin": "auto", "width": "50%"}),  # Centered text

    html.Iframe(src="data:application/pdf;base64," + base64.b64encode(open('Bachelor_Thesis_Applikation/assets/Bachelorthesis_EUT_P6_FS23_Curdin_Fitze-2.pdf', "rb").read()).decode('utf-8'),
                style={"width": "90%", "height": "700px", "zoom": "80%", 'margin-left': '5%'}),
                # style={"width": "100%", "height": "500px"})
])


# import dash
# from dash import dcc, html, callback, Output, Input
# import dash_bootstrap_components as dbc


# dash.register_page(__name__, path='/bachelor-thesis', name='Bachelor Thesis', order=4)  # is a subpage of the home page


# # Define the layout for the PDF page
# layout = html.Div([
#     html.Div([
#         html.H1("Bachelor Thesis", style={"text-align": "center", 'font-size': '35px', 'fontWeight': 'bold', 'fontFamily': 'Arial'}),
#         html.P("Willkommen bei der Bachelor Thesis von Curdin Fitze.", style={"text-align": "center"})
#     ], style={"margin": "auto", "width": "50%"}),  # Centered text

#     html.Div(
#         id="pdf-viewer",
#         className="pdf-viewer-container",
#         children=[
#             html.Div(
#                 id="pdf-contents",
#                 className="pdf-contents",
#                 style={"width": "100%", "height": "100%"},
#             )
#         ],
#     ),
# ])

# # Include CSS styles for the PDF viewer
# external_css = [
#     'https://cdnjs.cloudflare.com/ajax/libs/pdf.js/2.7.570/pdf.viewer.css'
# ]
# for css in external_css:
#     css.append_css({"external_url": css})

# # Include JavaScript files for the PDF viewer
# external_scripts = [
#     'https://cdnjs.cloudflare.com/ajax/libs/pdf.js/2.7.570/pdf.js'
# ]
# for script in external_scripts:
#     scripts.append_script({"external_url": script})

# # Update the PDF viewer content
# @callback(
#     Output("pdf-contents", "children"),
#     Input("pdf-viewer", "n_clicks"),
# )
# def update_pdf(n_clicks):
#     if n_clicks is not None and n_clicks > 0:
#         return html.Iframe(
#             src="/static/assets/Bachelorthesis_EUT_P6_FS23_Curdin_Fitze-2.pdf",
#             className="pdf-iframe",
#             style={"width": "100%", "height": "100%"},
#         )
#     else:
#         return None