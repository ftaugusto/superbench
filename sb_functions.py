from bokeh.plotting import figure, show
from bokeh.layouts import column
from bokeh.embed import components, file_html
from bokeh.models import Range1d,LinearAxis,ColumnDataSource, LabelSet
from bokeh.models.tools import HoverTool
from bokeh.resources import CDN
import pandas

df=""

def saps_bm():
    global df

    df=pandas.read_csv("sd.csv",sep=";",engine='python')
    cols=[4,5,10,11,12,14,15,16,17,18,19,20,22,23,24,25]
    df=df.drop(df.columns[cols],axis=1)
    df['Certification Number']=df[['Certification Number','Pdf Link']].astype(str).apply(lambda x: "<a href='" + x['Pdf Link'] + "' target='_blank'>" + x['Certification Number'] + "</a>",axis=1)
    df['tmp']=df.index
    df.insert(loc=0,column='Graph',value='')
    df['Graph']=df.tmp.apply(lambda x: "<input type='checkbox' name='server' id='" + str(x) + "' value=" + str(x)+ ">")
    df['saps_core']=round(df[['saps','Cores','Processors']].astype(float).apply(lambda x: x['saps']/x['Cores'] if x['Cores']>0 else x['saps']/x['Processors'],axis=1),1)
    df=df.drop(columns=['Pdf Link','tmp'],axis=1)
    return df.to_html(escape=False,index=False)

def rperf_bm():
    global df

    df=pandas.read_excel("power_benchmark.xlsx","rPerf")
    df['tmp']=df.index
    df.insert(loc=0,column='Graph',value='')
    df['Graph']=df.tmp.apply(lambda x: "<input type='checkbox' name='server' id='" + "' value=" + str(x)+ ">")
    df.drop(columns='tmp',axis=1,inplace=True)
    df['rPerf p/core']=round(df['rPerf p/core'],2)
    return df.to_html(escape=False,na_rep="n/a",index=False)

def cpw_bm():
    global df

    df=pandas.read_excel("power_benchmark.xlsx","CPW")
    df['tmp']=df.index
    df.insert(loc=0,column='Graph',value='')
    df['Graph']=df.tmp.apply(lambda x: "<input type='checkbox' name='server' id='" + "' value=" + str(x)+ ">")
    df.drop(columns='tmp',axis=1,inplace=True)
    df['CPW p/core']=round(df['CPW p/core'],2)
    return df.to_html(escape=False,na_rep="n/a",index=False)

def plot_bm(title, num_servers, bench_fields, labels):
    
    global df
    benchmark1=[]
    server_label=[]
    bench_label1=[]
    benchmark2=[]
    bench_label2=[]
    lista=[]
    y_overlimit=0.15

    for n,idx_server in zip(range(len(num_servers)),num_servers):
        i=int(idx_server)
        benchmark1.append(df[bench_fields[0]][i])
        bench_label1.append(str(df[bench_fields[0]][i]))
        benchmark2.append(df[bench_fields[1]][i])
        bench_label2.append(str(df[bench_fields[1]][i]))
        server_label.append(str(n+1) + ": " + str(df[labels[0]][i]) + " / " + str(df[labels[3]][i]) + " / " + str(int(df[labels[1]][i])) + "/" + str(df[labels[2]][i]))
        
    source = ColumnDataSource(data=dict(g_y=benchmark1,
                                        g_y2=benchmark2,
                                        s_values1=bench_label1,
                                        x_l=server_label,s_values2=bench_label2))

    for graph_type in range(2):
        hover=HoverTool()
        hover_tooltips = [
                        (bench_fields[0], "@s_values1")
                    ]
        #plot1 = figure(x_range=server_label,title=title, plot_width=800, plot_height=600,toolbar_location=None, tooltips=hover_tooltips)
        plot1 = figure(x_range=server_label,title=title, plot_width=800, plot_height=600,toolbar_location=None)
        hover.tooltips = hover_tooltips
        plot1.add_tools(hover)
        plot1.vbar(x='x_l', top='g_y', width=0.5,source=source,fill_alpha=0.4)
        plot1.y_range = Range1d(0,max(benchmark1) * (1 + y_overlimit))
        labels = LabelSet(x='x_l', y='g_y', text='g_y', level='glyph', text_font_size='8px',
                    x_offset=-15, y_offset=0, source=source, render_mode='canvas')
        plot1.add_layout(labels)
        plot1.left[0].formatter.use_scientific = False
        plot1.xaxis.major_label_orientation = 'vertical'
        plot1.yaxis.axis_label = bench_fields[0]
        
        hover=HoverTool()
        hover_tooltips = [
                        (bench_fields[1], "@s_values2")
                    ]
        plot2 = figure(x_range=server_label,title=title, plot_width=800, plot_height=600,toolbar_location=None)
        hover.tooltips = hover_tooltips
        plot2.add_tools(hover)
        plot2.vbar(x='x_l', top='g_y2', width=0.5,source=source,fill_alpha=0.4)
        plot2.y_range = Range1d(0,max(benchmark2) * (1 + y_overlimit))
        labels = LabelSet(x='x_l', y='g_y2', text='g_y2', level='glyph', text_font_size='8px',
                    x_offset=-15, y_offset=0, source=source, render_mode='canvas')
        plot2.add_layout(labels)
        plot2.left[0].formatter.use_scientific = False
        plot2.xaxis.major_label_orientation = 'vertical'
        plot2.yaxis.axis_label = bench_fields[1]
        
        if graph_type == 0:
            lista.append(plot1)
            lista.append(plot2)
        else:
            hover=HoverTool()
            hover_tooltips = [
                        (bench_fields[0], "@s_values1"),
                        (bench_fields[1], "@s_values2")
                    ]
            hover.tooltips = hover_tooltips
            plot1.add_tools(hover)
            plot1.extra_y_ranges = {bench_fields[1]: Range1d(start=0, end=max(benchmark2)*(1 + y_overlimit))} 
            plot1.add_layout(LinearAxis(y_range_name=bench_fields[1], axis_label=bench_fields[1]), 'right')
            plot1.line(x='x_l', y='g_y2',source=source, line_width=2,y_range_name=bench_fields[1], color='red')
            plot1.circle(x='x_l', y='g_y2',source=source,y_range_name=bench_fields[1], color='red',size=6)
            labels2 = LabelSet(x='x_l', y='g_y2', text='g_y2', level='glyph', text_font_size='8px',
                        x_offset=-15, y_offset=0, source=source, render_mode='canvas',y_range_name=bench_fields[1],text_color='red')
            plot1.add_layout(labels2)
            plot1.right[0].formatter.use_scientific = False

            plot2.add_tools(hover)
            plot2.extra_y_ranges = {bench_fields[0]: Range1d(start=0, end=max(benchmark1)*(1 + y_overlimit))} 
            plot2.add_layout(LinearAxis(y_range_name=bench_fields[0], axis_label=bench_fields[0]), 'right')
            plot2.line(x='x_l', y='g_y',source=source, line_width=2,y_range_name=bench_fields[0], color='red')
            plot2.circle(x='x_l', y='g_y',source=source,y_range_name=bench_fields[0], color='red',size=6)
            labels2 = LabelSet(x='x_l', y='g_y', text='g_y', level='glyph', text_font_size='8px',
                        x_offset=-15, y_offset=0, source=source, render_mode='canvas',y_range_name=bench_fields[0],text_color='red')
            plot2.add_layout(labels2)
            plot2.right[0].formatter.use_scientific = False
            lista.append(plot1)
            lista.append(plot2)

    #html = file_html(lista, CDN, "Benchmarks Plot")
    script, div = components(lista)
    newdiv=""

    for division in div:
        newdiv=newdiv + division.replace("\n","")

    graphs=[script,newdiv]
    #print(type(script)) 
    #print(type(div))  
    return graphs     
    #return html
    #return lista

def filter_sap(fcert_date,ftech_partner,fserver_name,fcpu_arch):
    
    filter1=df['Certification Date'].str.contains(fcert_date,case=False)
    filter2=df['Technology Partner'].str.contains(ftech_partner,case=False)
    filter3=df['Server Name'].str.contains(fserver_name,case=False)
    filter4=df['CPU Architecture'].str.contains(fcpu_arch,case=False)
    
    return df[filter1 & filter2 & filter3 & filter4].to_html(escape=False,index=False)

def filter_power(fmodel,fserver_name,fcpu_arch):
    
    filter1=df['Model-Type'].str.contains(fmodel,case=False)
    filter2=df['Nickname'].str.contains(fserver_name,case=False)
    filter3=df['CPU Arch'].str.contains(fcpu_arch,case=False)
    
    return df[filter1 & filter2 & filter3].to_html(escape=False,index=False)