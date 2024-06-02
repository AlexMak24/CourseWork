########################################################################################################################
# IMPORT # IMPORT # IMPORT # IMPORT # IMPORT # IMPORT # IMPORT # IMPORT # IMPORT # IMPORT # IMPORT # IMPORT # IMPORT # I
########################################################################################################################

# importing libraries
import plotly.graph_objs as go
from plotly.subplots import make_subplots


########################################################################################################################
# GET SHARED PLOT # GET SHARED PLOT # GET SHARED PLOT # GET SHARED PLOT # GET SHARED PLOT # GET SHARED PLOT # GET SHARED
########################################################################################################################

# function: getting graph figure of two axes
# input: name, [times], [[{}, {}, ... (graphs)], [], [], ... (subplots)]
def get_shared_plot(name, x, y):

    # calculating number of plots
    n_plots = len(y)

    # getting subplot titles
    subplot_titles = []
    for plot in y:
        subplot_titles.append(plot[0]['name'])

    # creating subplot figure
    fig = make_subplots(rows=n_plots, cols=1, shared_xaxes=True, vertical_spacing=0.03, subplot_titles=subplot_titles)

    # creating plots
    i = 1
    for plot in y:
        for graph in plot:
            fig.add_trace(go.Scatter(x=x, y=graph['data'], name=graph['name']), row=i, col=1)
            if graph['log']:
                fig.update_yaxes(type='log', row=i, col=1)
        i += 1

    # updating layout
    fig.update_layout(title_text=name)

    # return
    return fig


########################################################################################################################
# ADD DOT # ADD DOT # ADD DOT # ADD DOT # ADD DOT # ADD DOT # ADD DOT # ADD DOT # ADD DOT # ADD DOT # ADD DOT # ADD DOT
########################################################################################################################

# function: adding dot on already created graph
def add_dots(plot, dots):
    for dot in dots:
        plot.add_trace(
            go.Scatter(
                name=dot['name'],
                x=[dot['x']],
                y=[dot['y']],
                mode='markers',
                marker=dict(color=dot['color'], size=10)
            ),
            row=dot['row'],
            col=1
        )


########################################################################################################################
# END # END # END # END # END # END # END # END # END # END # END # END # END # END # END # END # END # END # END # END
########################################################################################################################
