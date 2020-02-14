from bokeh.plotting import figure, output_file, show
from motion_detection import df
from bokeh.models import HoverTool, ColumnDataSource, PrintfTickFormatter


# Format the datetime for hover
df['Start_string'] = df['Start'].dt.strftime("%Y-%m-%d %H:%M:%S")
df['End_string'] = df['End'].dt.strftime("%Y-%m-%d %H:%M:%S")


# Convert pandas dataframe to columndatasource
cds = ColumnDataSource(df)

p = figure(x_axis_type='datetime', height=250, width=600)
p.quad(left='Start', right='End', top=1, bottom=0, source=cds)
p.yaxis.minor_tick_line_color = None
p.ygrid[0].ticker.desired_num_ticks = 1

hover = HoverTool(
    tooltips=[("Start", "@Start_string"), ("End", "@End_string")])
p.add_tools(hover)

output_file('Graph.html')

show(p)
