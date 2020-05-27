from flask import Flask,render_template,request,redirect
from bokeh.plotting import figure, output_file, show
from bokeh.layouts import column
from sb_functions import saps_bm, rperf_bm, cpw_bm,plot_bm, filter_sap, filter_power

app=Flask(__name__)

@app.route("/", methods=("POST", "GET"))
def index():
    return render_template("index.html",bm_selected="saps")

@app.route("/filter", methods=("POST", "GET"))
def filter():
    global benchmark_table
    if bm_selected == 'saps':
        fcert_date=" ".join(request.form["cer_date"].strip().split())
        ftech_partner=" ".join(request.form["tech_partner"].strip().split())
        fserver_name=" ".join(request.form["server_name"].strip().split())
        fcpu_arch=" ".join(request.form["cpu_arch"].strip().split())
        benchmark_table=filter_sap(fcert_date,ftech_partner,fserver_name,fcpu_arch)
        return render_template("index.html",benchmark_table=benchmark_table, bm_selected=bm_selected,
        benchmark_title=benchmark_title,cer_value=fcert_date,
        tech_value=ftech_partner,server_value=fserver_name,cpu_value=fcpu_arch)
    else:
        fmodel=" ".join(request.form["model"].strip().split())
        fserver_name=" ".join(request.form["server_name"].strip().split())
        fcpu_arch=" ".join(request.form["cpu_arch"].strip().split())
        benchmark_table=filter_power(fmodel,fserver_name,fcpu_arch)
        return render_template("index.html",benchmark_table=benchmark_table, bm_selected=bm_selected,
        benchmark_title=benchmark_title,model_value=fmodel,
        server_value=fserver_name,cpu_value=fcpu_arch)

@app.route("/plot_graph", methods=("POST", "GET"))
def plot_graph():
    servers=request.form.getlist("server")
    
    if len(servers) == 0:
        return render_template("index.html",benchmark_table=benchmark_table, bm_selected=bm_selected,benchmark_title=benchmark_title)

    if bm_selected == 'saps':
        plot_title="SAPs Benchmark"
        fields=["saps_core","saps"]
        data_labels=["Server Name","Processors","Cores","CPU Speed"]
    elif bm_selected == 'cpw':
        plot_title="Power Systems CPW Benchmark"
        fields=["CPW p/core","CPW"]
        data_labels=["Nickname","Sockets","Total Cores","GHz"]
    else:
        plot_title="Power Systems rPerf Benchmark"
        data_labels=["Nickname","Sockets","Total Cores","GHz"]
        fields=["rPerf p/core","rPerf"]

    graphs_to_plot=plot_bm(plot_title,servers,fields,data_labels)
    show(column(graphs_to_plot))
  
    return render_template("index.html",benchmark_table=benchmark_table, bm_selected=bm_selected,benchmark_title=benchmark_title)

@app.route("/show_benchmark", methods=['POST','GET'])
def show_benchmark():
    global bm_selected
    global benchmark_table
    global benchmark_title

    bm_selected=request.form["benchmark"]
    if bm_selected == 'saps':
        benchmark_title="<h5>Current benchmark: SAPs</h5>"
        benchmark_table=saps_bm()
    elif bm_selected == 'cpw':
        benchmark_title="<h5>Current benchmark: Power Systems CPW</h5>"
        benchmark_table=cpw_bm()
    else:
        benchmark_title="<h5>Current benchmark: Power Systems rPerf</h5>"
        benchmark_table=rperf_bm()

    return render_template("index.html",benchmark_table=benchmark_table,bm_selected=bm_selected,benchmark_title=benchmark_title)

if __name__ == '__main__':
    app.debug=True
    app.run()