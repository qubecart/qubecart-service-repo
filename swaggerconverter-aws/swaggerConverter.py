from flask import Flask, jsonify, request
from flask_restful import Resource,Api
import yaml
import io
import json
import os
import os.path
from os.path import join
import sys
import copy
import time
from time import gmtime, strftime
#import swagmanmock

app = Flask(__name__)


@app.route('/msqube/convertswagger/', methods=['POST'])
def testdata():
    data = request.get_json()
    file_url = str(data['file'])
    config_file = str(data['config_file'])
    swagger_file = str(data['swagger_file'])
    
    filecontent = []
    servercontent = []

    final_file = (swagger_file +".yaml")
    #clear file:
    if os.path.exists(str(final_file)):
        os.remove(str(final_file))

    #insertion data yaml
    with open(config_file,'r') as server_yaml:
        serverdecoded = json.dumps(yaml.load(server_yaml))
        serverdecoded = json.loads(serverdecoded)
        servercontent.append(serverdecoded)
    
    servercontent = servercontent[0]

    #inserted data yaml:
    with open(file_url,'r') as f:
        content = json.dumps(yaml.safe_load(f))
        content = json.loads(content)
        filecontent.append(content)
    
    filecontent = filecontent[0]
    #for paths :
    pathscript = filecontent['paths']
    pathresult = pathoperation(pathscript,servercontent)
    
    #finaljson
    finaljson = {"components":filecontent['components'],"info":filecontent['info'],"openapi":filecontent['openapi'],"servers":servercontent['servers'],"paths":pathresult,"x-amazon-apigateway-gateway-responses":servercontent['x-amazon-apigateway-gateway-responses']}
    finaldata = [filecontent['components'],filecontent['info'],filecontent['openapi'],servercontent['servers'],pathresult,servercontent['x-amazon-apigateway-gateway-responses']]
    finalkeys = ["components","info","openapi","servers","paths","x-amazon-apigateway-gateway-responses"]

    for i in range(0,len(finaldata)):
        data= {finalkeys[i]:finaldata[i]}
        with open(final_file, 'a+') as file:
            documents = yaml.dump(data, file)
    print(f"file written : {final_file}")
    current_time = time.strftime("%Y-%m-%d %H:%M:%S", gmtime())
    print(current_time)
    io.open(final_file, 'r')
    return(jsonify(finaljson))


def pathoperation(pathscript,servercontent):
   
    descriptioninp = servercontent['description']
    headersinp = servercontent['headers']
    post_summary_xamazon = servercontent['x-amazon-apigateway-integration']
    post_method_options = servercontent['options']
    print("options =",post_method_options)
    path_keys_1 = list(pathscript.keys())
    for i in range(0,len(path_keys_1)):
        pathurl = path_keys_1[i]        #Getting Pathkeys
        print("Path URL = ",pathurl)
        pathmethod = list(pathscript[pathurl].keys())[0]        #Getting URL Method
        print("method = ",pathmethod)
        path_keys_3 = list(pathscript[pathurl][pathmethod].keys())
        print(pathscript[pathurl][pathmethod]['responses']['200']['content'])
        content200 = pathscript[pathurl][pathmethod]['responses']['200'].pop('content')
        print("content =",content200)
        desc200 = pathscript[pathurl][pathmethod]['responses']['200'].pop('description')
        appkeys = ['description','headers','content']
        copy_headersinp=copy.deepcopy(headersinp)               #Avoiding Shallow Copy
        appvals = [descriptioninp,copy_headersinp,content200]
        file200 = dict(zip(appkeys,appvals))
        pathscript[pathurl][pathmethod]['responses']['200'] = file200

        pathsummary = pathscript[pathurl][pathmethod]['summary']
        copy_post_summary_xamazon = copy.deepcopy(post_summary_xamazon)
        copy_post_summary_xamazon['httpMethod']=str(pathmethod).upper()
        copy_post_summary_xamazon['uri']=str(pathsummary)
        pathscript[pathurl][pathmethod]['x-amazon-apigateway-integration'] = copy_post_summary_xamazon


        pathref = pathscript[pathurl][pathmethod]['responses']['200']['content']['application/json']['schema']['$ref']
        copy_post_method_options = copy.deepcopy(post_method_options)
        copy_post_method_options['responses']['200']['content']['application/json']['schema']['$ref'] = pathref
        copy_post_method_options['x-amazon-apigateway-integration']['responses']['default']['responseParameters']['method.response.header.Access-Control-Allow-Methods'] = "'"+str(pathmethod).upper()+",OPTIONS'"
        pathscript[pathurl]['options'] = copy_post_method_options

    return(pathscript)
        
if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0",port="5000")
