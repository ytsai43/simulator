import json
import urllib.request
import time
import numpy as np

## Input function: 
## -"status" --> "S" as Start Experiment || "R" as Running Experiment
## -"vars" --> list of pump's speed values for 2 hrs
## Output function:
## The returned list is composed by:
## - MetricValue which is the metric we want to minimize
## - List of List of hrs pressures for each node in the hydraulic system

def callWebService(status, vars):
    try:
        var_1 = float(vars[0])
        var_2 = float(vars[1])
        try:
            url = 'http://149.132.21.73:8080/EpanetWebServiceASU/EPANET/epanetService/'+str(status)+'&'+ str(var_1) +'&'+ str(var_2) +'&0&0&0&0&0&0&0&0&0&0&0&0&0&0&0&0&0&0&0&0&0&0&0&0&0&0&0&0&0&0&0&0&0&0&0&0&0&0&0&0&0&0&0&0&0&0&0&0&0&0&0&0&0&0&0&0&0&0&0&0&0&0&0&0&0&0&0&0&0&0'
            with urllib.request.urlopen(url) as response:
                html = response.read()
            tmp_html = html.decode("utf-8")  
            tmp_list = tmp_html.split("\n\n")
            dict_res = json.loads(tmp_list[1])
            list_nodes = eval(dict_res["List_Nodes"])
            pressures = list()
            for i in range(len(list_nodes)):
                name_node = list_nodes[i]
                pressures.append(dict_res[str(name_node)])
            return [dict_res["MetricValue"], np.matrix(pressures)]
        except:
            print("Webservice error: please contact the administrators")
    except:
        print("Error: input format exception")


## Script for calling the webservice
start = time.time()

## Example of start experiment of optimization simulation :
## Start calling webservice with input parameter as "S" and list of pump speed for 2 hrs
result = callWebService("S", [0.7, 0.6])
print(result)
print("-"*30)
## Running calling webservice with input parameter as "R" and list of pump speed for 2 hrs
result = callWebService("R", [0.2, 0.0])
print(result)
print("-"*30)

end = time.time()
print(end-start)

### IMPORTANT NOTE:
## If you receive from webservice this value : "1000000000.0" is because the proposed speed solution is not permissible