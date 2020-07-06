from bokeh.plotting import figure, show
from bokeh.layouts import column
from bokeh.embed import components, file_html
from bokeh.models import Range1d,LinearAxis,ColumnDataSource, LabelSet
from bokeh.models.tools import HoverTool
import pandas

def saps_bm(benchm_sel): 
    df_saps=select_data(benchm_sel)
    html=df_saps.to_html(escape=False,index=False)
    html=prepare_sort(html,benchm_sel)
    
    return html
    #return df_saps.to_html(escape=False,index=False)

def rperf_bm(benchm_sel):
    df_rperf=select_data(benchm_sel)
    html=df_rperf.to_html(escape=False,na_rep="n/a",index=False)
    html=prepare_sort(html,benchm_sel)
    
    return html
    #return df_rperf.to_html(escape=False,na_rep="n/a",index=False)

def cpw_bm(benchm_sel):
    df_cpw=select_data(benchm_sel)
    html=df_cpw.to_html(escape=False,na_rep="n/a",index=False)
    html=prepare_sort(html,benchm_sel)
    
    return html
    #return df_cpw.to_html(escape=False,na_rep="n/a",index=False)

def plot_bm(title, num_servers, bench_fields, labels,benchm_sel):
    df=select_data(benchm_sel)
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
        hover_tooltips = [(bench_fields[1], "@s_values2")]
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
        
        if graph_type == 0: #Somente gráficos de barra
            lista.append(plot1)
            lista.append(plot2)
        else:  #Monta os gráficos mistos (barras e linha)
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
    return graphs     

def select_data(benchmark_selected):
    if benchmark_selected == "saps":
        df=pandas.read_csv("sd.csv",sep=";",engine='python')
        cols=[4,5,10,11,12,14,15,16,17,18,19,20,22,23,24,25]
        df=df.drop(df.columns[cols],axis=1)
        df['Certification Number']=df[['Certification Number','Pdf Link']].astype(str).apply(lambda x: "<a href='" + x['Pdf Link'] + "' target='_blank'>" + x['Certification Number'] + "</a>",axis=1)
        df['tmp']=df.index
        df.insert(loc=0,column='Graph',value='')
        df['Graph']=df.tmp.apply(lambda x: "<input type='checkbox' name='server' id='" + str(x) + "' value=" + str(x)+ ">")
        df['saps_core']=round(df[['saps','Cores','Processors']].astype(float).apply(lambda x: x['saps']/x['Cores'] if x['Cores']>0 else x['saps']/x['Processors'],axis=1),1)
        df=df.drop(columns=['Pdf Link','tmp'],axis=1)
    elif benchmark_selected == "cpw":
        df=pandas.read_excel("power_benchmark.xlsx","CPW")
        df['tmp']=df.index
        df.insert(loc=0,column='Graph',value='')
        df['Graph']=df.tmp.apply(lambda x: "<input type='checkbox' name='server' id='" + "' value=" + str(x)+ ">")
        df.drop(columns='tmp',axis=1,inplace=True)
        df['CPW p/core']=round(df['CPW p/core'],2)
    else:
        df=pandas.read_excel("power_benchmark.xlsx","rPerf")
        df['tmp']=df.index
        df.insert(loc=0,column='Graph',value='')
        df['Graph']=df.tmp.apply(lambda x: "<input type='checkbox' name='server' id='" + "' value=" + str(x)+ ">")
        df.drop(columns='tmp',axis=1,inplace=True)
        df['rPerf p/core']=round(df['rPerf p/core'],2)
    return(df)


def filter_sap(benchm_sel,fcert_date,ftech_partner,fserver_name,fcpu_arch,fsockets):
    df=select_data(benchm_sel)
    filter1=df['Certification Date'].str.contains(fcert_date,case=False)
    filter2=df['Technology Partner'].str.contains(ftech_partner,case=False)
    filter3=df['Server Name'].str.contains(fserver_name,case=False)
    filter4=df['CPU Architecture'].str.contains(fcpu_arch,case=False)
    filter5=df['Processors'].apply(str).str.contains(fsockets,case=False)
    
    html=df[filter1 & filter2 & filter3 & filter4 & filter5].to_html(escape=False,index=False)
    html=prepare_sort(html,benchm_sel)

    return html
    #return df[filter1 & filter2 & filter3 & filter4 & filter5].to_html(escape=False,index=False)

def filter_power(benchm_sel,fmodel,fserver_name,fcpu_arch,fsockets):
    df=select_data(benchm_sel)
    filter1=df['Model-Type'].str.contains(fmodel,case=False)
    filter2=df['Nickname'].str.contains(fserver_name,case=False)
    filter3=df['CPU Arch'].str.contains(fcpu_arch,case=False)
    filter4=df['Sockets'].apply(str).str.contains(fsockets,case=False)
    
    html=df[filter1 & filter2 & filter3 & filter4].to_html(escape=False,index=False)
    html=prepare_sort(html,benchm_sel)

    return html
    #return df[filter1 & filter2 & filter3 & filter4].to_html(escape=False,index=False)

def prepare_sort(html_out,benchmark):
    html_tmp=html_out
    if benchmark == "saps":
        repl_dict={"<table border":"<table id='bm_table' border",
            "<th>Certification Number</th>":"<th onclick='sortTable(1)'>Certification Number</th>",
            "<th>Certification Date</th>":"<th onclick='sortTable(2)'>Certification Date</th>",
            "<th>Technology Partner</th>":"<th onclick='sortTable(3)'>Technology Partner</th>",
            "<th>Server Name</th>":"<th onclick='sortTable(4)'>Server Name</th>",
            "<th>CPU Architecture</th>":"<th onclick='sortTable(5)'>CPU Architecture</th>",
            "<th>CPU Speed</th>":"<th onclick='sortTable(6)'>CPU Speed</th>",
            "<th>Processors</th>":"<th onclick='sortTable(7)'>Processors</th>",
            "<th>Cores</th>":"<th onclick='sortTable(8)'>Cores</th>",
            "<th>saps</th>":"<th onclick='sortTable(9)'>saps</th>",
            "<th>saps_core</th>":"<th onclick='sortTable(10)'>saps_core</th>"}
    elif benchmark == "cpw":
        repl_dict={"<table border":"<table id='bm_table' border",
                "<th>Model-Type</th>":"<th onclick='sortTable(1)'>Model-Type</th>",
                "<th>Nickname</th>":"<th onclick='sortTable(2)'>Nickname</th>",
                "<th>CPU Arch</th>":"<th onclick='sortTable(3)'>CPU Arch</th>",
                "<th>Sockets</th>":"<th onclick='sortTable(4)'>Sockets</th>",
                "<th>Cores per Socket</th>":"<th onclick='sortTable(5)'>Cores per Socket</th>",
                "<th>Total Cores</th>":"<th onclick='sortTable(6)'>Total Cores</th>",
                "<th>GHz</th>":"<th onclick='sortTable(7)'>GHz</th>",
                "<th>CPW</th>":"<th onclick='sortTable(8)'>CPW</th>",
                "<th>CPW p/core</th>":"<th onclick='sortTable(9)'>CPW p/core</th>"}
    else:
        repl_dict={"<table border":"<table id='bm_table' border",
                "<th>Model-Type</th>":"<th onclick='sortTable(1)'>Model-Type</th>",
                "<th>Nickname</th>":"<th onclick='sortTable(2)'>Nickname</th>",
                "<th>CPU Arch</th>":"<th onclick='sortTable(3)'>CPU Arch</th>",
                "<th>Sockets</th>":"<th onclick='sortTable(4)'>Sockets</th>",
                "<th>Cores per Socket</th>":"<th onclick='sortTable(5)'>Cores per Socket</th>",
                "<th>Total Cores</th>":"<th onclick='sortTable(6)'>Total Cores</th>",
                "<th>GHz</th>":"<th onclick='sortTable(7)'>GHz</th>",
                "<th>SMT1 rPerf</th>":"<th onclick='sortTable(8)'>SMT1 rPerf</th>",
                "<th>SMT2 rPerf</th>":"<th onclick='sortTable(9)'>SMT2 rPerf</th>",
                "<th>SMT4 rPerf</th>":"<th onclick='sortTable(10)'>SMT4 rPerf</th>",
                "<th>SMT8 rPerf</th>":"<th onclick='sortTable(11)'>SMT8 rPerf</th>",
                "<th>rPerf</th>":"<th onclick='sortTable(12)'>rPerf</th>",
                "<th>rPerf p/core</th>":"<th onclick='sortTable(13)'>rPerf p/core</th>"}

    for key in repl_dict:
        html_tmp=html_tmp.replace(key,repl_dict[key])
        
    return(html_tmp)
