from django.http import HttpResponse
from django.shortcuts import render
from django.template import Context
from demo.TimeSeries import SearchTSDTW,SearchTSED,QueryIndex
import json

def index(request):
    return render(request,'index.html')
def compute(request):
    query = request.GET.get('query',None)
    select = request.GET.get("Sex",None)
    query = query.split(',')
    query = [float(i) for i in query]
    dict = {}
    if select=="dtw":
        dict["query"] = SearchTSDTW.make(query)
    elif select == "ed":
        dict["query"] = SearchTSED.make(query)
    else:
        dict["query"] = QueryIndex.make(query)
    #t = get_template('front/index.html')
    context = {
        "query":query,
        "seq": dict["query"]["Seq"],
        "time":dict["query"]["Time"],
        "dtw": dict["query"]["DTW"],
        "start": dict["query"]["Start"],
        "end":dict["query"]["End"],
        "orderNumber":dict["query"]["OrderNumber"]
    }
    return render(request,'index.html', context)
    # 传递数据给json var result = {{result|safe}};
    # return HttpResponse(json.dumps(dict))