import requests
import json
from prompt_toolkit import prompt
from prompt_toolkit.completion import WordCompleter
from prompt_toolkit.completion import Completer, Completion
from datetime import datetime, timezone

customer_url = "http://localhost:8013/openapi"
driver_url = "http://localhost:8016/openapi"

customer_base_url = "http://localhost:8013"
driver_base_url = "http://localhost:8016"
which_api_we_are_using = "customer"


default_ridesearch_request = {
    "fareProductType": "ONE_WAY",
    "contents": {
        "origin": {
            "address": {
                "area": "8th Block Koramangala",
                "areaCode": "560047",
                "building": "Juspay Buildings",
                "city": "Bangalore",
                "country": "India",
                "door": "#444",
                "street": "18th Main",
                "state": "Karnataka"
            },
            
            "gps": {
                "lat": 12.846907,
                "lon": 77.556936
            }
        },
        "destination": {
            "address": {
                "area": "6th Block Koramangala",
                "areaCode": "560047",
                "building": "Juspay Apartments",
                "city": "Bangalore",
                "country": "India",
                "door": "#444",
                "street": "18th Main",
                "state": "Karnataka"
            },
            "gps": {
                "lat": 12.846907,
                "lon": 77.566936
            }
        }
    }
}

def set_which_api_we_are_using(api):
    global which_api_we_are_using
    which_api_we_are_using = api

def isAffirmative(x):
    if x == "yes" or x == "Y" or x == "y" or x == "1" or x == "Yes" or x == "":
        return True
    else:
        return False

def isNegative(x):
    if x == "no" or x == "N" or x == "n" or x == "0" or x == "No":
        return True
    else:
        return False

    
# customer_object = {
#     path : "",
#     type : "",
#     request_body : []
#     parameters : []
# }

customer_api_data = []
driver_api_data = []

all_customer_api = []

# Custom completer class
class MyCompleter(Completer):
    def __init__(self, completions):
        super().__init__()
        self.completions = completions

    def get_completions(self, document, complete_event):
        
        text = document.text

        for completion in self.completions:
            if completion in text:
                yield Completion(completion, start_position=-len(text))


def isTrue(verdict):
    if verdict == "False" or verdict == "F" or verdict == "f" or verdict == "false" or verdict == "0":
        return False
    else:
        return True

# return (input_in_proper_form,is_success)
def input_sanitizer(inp,type_of_input):
    if type_of_input == 'boolean':
        return (isTrue(inp),True)
    elif type_of_input == 'string':
        return (str(inp),True)
    elif type_of_input == 'integer':
        try:
            return (int(inp),True)
        except:
            print("[-] Write input in proper form ( " + str(type_of_input) + " ) " )
            print("")
            return (inp,False)
    elif type_of_input == 'double':
        try:
            return (float(inp),True)
        except:
            print("[-] Write input in proper form ( " + str(type_of_input) + " ) " )
            print("")
            return (inp,False)

# return type = {'name' : 'value','name':value}

def query_parameter_filler(query_parameter_list,data):
    required_query_parameters = [parameter for parameter in query_parameter_list if parameter.get('required') == True ]
    non_required_query_parameters = [parameter for parameter in query_parameter_list if parameter.get('required') == False ]
    answers = {}
    print("") 
    print("==> Fill mandatory query parameters")
    print("") 

    for parameter in required_query_parameters:
        ip = ""
        if data.get(str(parameter.get('name'))) == None:
            prompt = "> Enter " + str(parameter.get('name')) + " ( " + str(parameter.get('type')) + ") : "
            ip = input(prompt)
        else:
            prompt = "> Enter " + str(parameter.get('name')) + " ( " + str(parameter.get('type')) + " ) ( default " + str(data.get(str(parameter.get('name')))) + ") : "
            ip = input(prompt)

            if ip == "":
                ip = data.get(str(parameter.get('name')))
        

        (sanitized_input,isSuccess) = input_sanitizer(ip,str(parameter.get('type')))

        while isSuccess == False:
            (sanitized_input,isSuccess) = input_sanitizer(ip,str(parameter.get('type')))

        answers[str(parameter.get('name'))] = sanitized_input

    if len(non_required_query_parameters) > 0:
        answer = input("> Want to add non required parameters: ")

        while isAffirmative(answer):
            print("")
            print("[+] Which one ?")
            print("")

            for i in range(len(non_required_query_parameters)):
                print("[" + str(i) + "] " + str(non_required_query_parameters[i].get('name')))

            print("")

            idx = input("> ")

            if idx == "":
                break
            else:
                index = int(idx)

            value = input("Enter the value of " + str(non_required_query_parameters[index].get('name')) + " ( " + str(non_required_query_parameters[index].get('type')) + " ) " + " : ")

            (sanitized_input,isSuccess) = input_sanitizer(value,non_required_query_parameters[index].get('type'))

            answers[str(non_required_query_parameters[index].get('name'))] = sanitized_input

            answer = input("> Wanna add more : ")

    return answers

# return (isException,body)
def handle_openapi_exception(path,data):

    request_body = {}

    if path == '/ui/driver/location':
        pt_lat = 12.846907
        pt_lon = 77.556936
        ts = datetime.utcnow().replace(tzinfo=timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
        
        ip = input("> Enter lat (default " + str(pt_lat) + " ) : ")

        if ip != "":
            (pt_lat,isSuccess) = sanitized_input(ip,'double')

        ip = input("> Enter lon (default " + str(pt_lon) + " ) : ")

        if ip != "":
            (pt_lon,isSuccess) = sanitized_input(ip,'double')

        
        return ([
                {
                    "pt": {
                        "lat": pt_lat,
                        "lon": pt_lon
                    },
                    "ts": ts
                }
            ],True)

    return ({},False)




def request_body_filler(initial_prompt,req_body,api_object,index,data,path):

    (body,isException) = handle_openapi_exception(path,data)

    if isException:
        print("")
        print("[-] This is an exception")
        print("")
        print(body)
        return body

    if req_body == None:
        print("[-] Empty request body")
        return {}

    all_properties_list = []

    for x in req_body.get('properties'):
        all_properties_list.append(x)

    non_required_properties = []
    
    if req_body.get("required") != None:
        non_required_properties = result = [x for x in all_properties_list if x not in req_body.get("required")]

    body = {}

    if req_body.get("required") != None:
        for param in req_body.get("required"):
            if str(req_body.get('properties').get(param).get('type')) != 'object':
                prompt_statement = "> Enter " + param + " ( " + initial_prompt + str(req_body.get('properties').get(param).get('type')) + " ) : "
                if data.get(param) != None:
                    prompt_statement += "( default " + str(data.get(param)) + " ) : "
                
                inp = input(prompt_statement)
                
                if inp == "" and data.get(param) != None:
                    body[param] = data.get(param)

                elif str(req_body.get('properties').get(param).get('type')) == 'number':    
                    body[param] = float(inp)
                
                elif str(req_body.get('properties').get(param).get('type')) == 'boolean':
                    body[param] = bool(inp)
                else:
                    body[param] = inp
            else:
                body[param] = request_body_filler(initial_prompt + " [ " + param + " ] " ,req_body.get("properties").get(param),api_object,index,data,path)

    if non_required_properties != None:
        answer = input("> Want to add any non required properties : ")

        while isAffirmative(answer):
            print("")
            print("[+] Which one ?")
            print("")

            for i in range(len(non_required_properties)):
                print("[" + str(i) + "] " + non_required_properties[i])

            print("")

            idx = input("> ")

            if idx == "":
                break
            else:
                index = int(idx)

            value = input("Enter the value of " + non_required_properties[index] + " : ")

            body[non_required_properties[index]] = value

            answer = input("> Wanna add more : ")

    print("")
    print("==> Your request is ")
    print("")
    print(beautify_json(body))

    return body

def one_of_request_body_sorter(req_body):

    if req_body == None or len(req_body) == 0 or req_body[0] == None or req_body[0].get('oneOf') == None:
        return req_body
    
    else :
        listy = []
        for x in range(len(req_body[0].get('oneOf'))):
            listy.append(req_body[0].get('oneOf')[0])
        return listy


def auth_and_verify(data,api_data,base_url):

    if which_api_we_are_using == "customer":

        (data,found) = url_runner('/v2/auth',data,api_data,base_url)
        (data,found) = url_runner('/v2/auth/{authId}/verify',data,api_data,base_url)
        return data
    elif which_api_we_are_using == "driver":
        (data,found) = url_runner('/ui/auth',data,api_data,base_url)
        (data,found) = url_runner('/ui/auth/{authId}/verify',data,api_data,base_url)
        return data


def get_object_from_schema_reference(request_body,open_api_json):
    for content in request_body:
        for appjson in request_body.get(content):
            for schema in request_body.get(content).get(appjson):
                for ref in request_body.get(content).get(appjson).get(schema):
                    return open_api_json["components"]["schemas"].get(str(request_body.get(content).get(appjson).get(schema).get(ref)).split("/")[3])

def get_object_from_ref(ref,open_api_json):
    return open_api_json["components"]["schemas"].get(str(ref.split("/")[3]))

def all_ref_remover(request_body,open_api_json):

    if request_body == None:
        return request_body

    if type(request_body) != dict and type(request_body) != list:
        return request_body

    for key in request_body:

        if type(request_body.get(key)) == dict and request_body.get(key).get('$ref') != None:
            obj = get_object_from_ref(request_body.get(key).get('$ref'),open_api_json)
            request_body[key] = obj

        if type(request_body.get(key)) == dict :
            request_body[key] = all_ref_remover(request_body.get(key),open_api_json)

        elif type(request_body.get(key)) == list :
            for l in range(len(request_body.get(key))):
                request_body[key][l] = all_ref_remover(request_body.get(key)[l],open_api_json)
        
    return request_body

def make_curl_request(url,request_type,request_body,base_url,data,query_parameters):

    print("")
    print("==> Hitting " + base_url + url )
    print("")

    api_key = data.get("token")
    headers = {"token": api_key}

    if request_type == "get":
        response = requests.get(base_url + url,headers=headers,params=query_parameters)
        try:
            return response.json()
        except:
            return response.text

    elif request_type == "post":
        response = requests.post(base_url + url,json=request_body,headers=headers,params=query_parameters)
        try:
            return response.json()
        except:
            return response.text

    elif request_type == "put":
        response = requests.put(base_url + url,json=request_body,headers=headers,params=query_parameters)
        try:
            return response.json()
        except:
            return response.text

    elif request_type == "delete":
        response = requests.delete(base_url + url,json=request_body,headers=headers,params=query_parameters)
        try:
            return response.json()
        except:
            return response.text

def beautify_json(json_text):
    try:
        beautified_json = json.dumps(json_text, indent=4)
        return beautified_json
    except json.JSONDecodeError:
        return None

def config_loader(url):
    final_list = []
    open_api_json = make_curl_request(url,"get","","",{},{})
    api_data = open_api_json["paths"]

    for path in api_data: 
        api_instance = {}
        api_instance["url_path"] = path

        req_body = []

        for rt in api_data[path]:
            api_instance["request_type"] = rt

            for content in api_data[path][rt]:
                if content == "parameters":
                    api_instance["parameters"] = api_data[path][rt][content]
                elif content == "requestBody":
                    req_body.append(all_ref_remover(get_object_from_schema_reference(api_data[path][rt][content],open_api_json),open_api_json))

            break

        api_instance["request_body"] = one_of_request_body_sorter(req_body)
        
        final_list.append(api_instance)

    return final_list

def url_runner(url,data,api_data,base_url):
    print("")
    print("==> url is ",url)
    print("")
    for api_object in api_data:
        if api_object['url_path'] == url:
            request_body = {}
            path_contents = api_object['url_path'].split('/')
            
            for c in range(len(path_contents)):
                if "{" in path_contents[c]:
                    if data.get(path_contents[c][1:-1]) != None and data.get(path_contents[c][1:-1]) != "":
                        y = input("> Default " + str(path_contents[c][1:-1]) + " exists press yes if you wanna use that ( " + data.get(path_contents[c][1:-1]) + " ) :")
                        if isAffirmative(y):
                            path_contents[c] = data.get(path_contents[c][1:-1])
                        else:
                            x = input("> Enter " + path_contents[c][1:-1] + " : ")
                            path_contents[c] = x
                    else:
                        x = input("> Enter " + path_contents[c][1:-1] + " : ")
                        path_contents[c] = x

            api_object['url_path'] = '/'.join(path_contents)

            parametersList = api_object.get("parameters")

            # queryParametersList = [{
            #     'name' : 'paramter name',
            #     'type' : 'parameter type'
            #     'required' : Bool
            # }]

            queryParametersList = []
            if parametersList and len(parametersList) > 0:
                for parameter in parametersList:
                    if parameter.get('in') == 'query':
                        parameter_object = {
                            'name' : parameter.get('name'),
                            'type' : parameter.get('schema').get('type'),
                            'required' : parameter.get('required')
                        }
                        queryParametersList.append(parameter_object)
            
            # print(queryParametersList)

            # parameter object = [{'name','value'}]
            parameterObjects = query_parameter_filler(queryParametersList,data)

            if len(api_object.get("request_body")) == 0:  
                response = make_api_call_on_success(api_object,data,None,base_url,parameterObjects)
                (data,should_show_response) = response_parser(data,response,api_data,base_url)                  
                if should_show_response:
                    print("")
                    print("==> Fetching the response")
                    print("") 
                    print(beautify_json(response))
                    print("")

                          
            else:
                print(" ==> Type your request")
                print("")
                index = 0

                if len(api_object.get("request_body")) > 1:

                    inp = input("There are " + str(len(api_object.get("request_body"))) + " ways to make a request , Pick one (default 0) : ")

                    if inp == "":
                        index = 0
                    else:
                        index = int(inp)
                
                if data.get(api_object['url_path']) != None:
                        x = input("Default request exists write yes if you want to use that : ")
                        if isAffirmative(x):
                            request_body = data.get(api_object['url_path'])
                        else:
                            request_body = request_body_filler("",api_object.get("request_body")[index],api_object,index,data,api_object['url_path'])
                else:
                    request_body = request_body_filler("",api_object.get("request_body")[index],api_object,index,data,api_object['url_path'])
                
                response = make_api_call_on_success(api_object,data,request_body,base_url,parameterObjects)
                (data,should_show_response) = response_parser(data,response,api_data,base_url)                  
                if should_show_response:
                    print("")
                    print("==> Fetching the response")
                    print("") 
                    print(beautify_json(response))
                    print("")

            

            

            return (data,True)
    return (data,False)

def api_runner():
    print("")
    customer_api_data = config_loader(customer_url)
    driver_api_data = config_loader(driver_url)

    found_the_api_object = False
    retry = True

    customer_data = {
        "merchantId" : "NAMMA_YATRI",
        "mobileNumber" : "9999999999",
        "mobileCountryCode" : "+91",
        "otp": "7891",
        "deviceToken": "8e83b5dc-99a0-4306-b90d-2345f3050972",
        "fareProductType": "ONE_WAY",
        "/v2/rideSearch" : default_ridesearch_request,
        "token" : "",
        "authId" : "",
        "autoAssignEnabled" : False
    }
    driver_data = {
        "mobileNumber" : "6666666666",
        "mobileCountryCode": "+91",
        "merchantId": "favorit0-0000-0000-0000-00000favorit",
        "otp": "7891",
        "deviceToken": "8e83b5dc-99a0-4306-b90d-2345f3050972",
        "active" : True
    }

    available_paths = []
    data_currently_in_use = customer_data
    apis_currently_in_use = customer_api_data
    base_url = customer_base_url
    for i in range(len(apis_currently_in_use)) : 
        available_paths.append(apis_currently_in_use[i]['url_path'])

    completer = WordCompleter(available_paths)
    suggested_url = ""

    while found_the_api_object == False or retry == True:
        if suggested_url != "":
            url = suggested_url
        else:
            url = prompt("> Enter the URL to make the cURL request: ", completer=completer)

            if url == "other":
                if (which_api_we_are_using) == "customer":
                    print("")
                    print("==> Switching to Driver")
                    customer_data = data_currently_in_use
                    data_currently_in_use = driver_data
                    apis_currently_in_use = driver_api_data
                    set_which_api_we_are_using("driver")
                    base_url = driver_base_url
                    available_paths = []
                    for i in range(len(apis_currently_in_use)) : 
                        available_paths.append(apis_currently_in_use[i]['url_path'])
                    completer = WordCompleter(available_paths)
                elif (which_api_we_are_using) == "driver":
                    print("")
                    print("==> Switching to Customer")
                    driver_data = data_currently_in_use
                    data_currently_in_use = customer_data
                    apis_currently_in_use = customer_api_data
                    set_which_api_we_are_using("customer")
                    base_url = customer_base_url
                    available_paths = []
                    for i in range(len(apis_currently_in_use)) : 
                        available_paths.append(apis_currently_in_use[i]['url_path'])
                    completer = WordCompleter(available_paths)
                
                
         
        (data_currently_in_use,found_the_api_object) = url_runner(url,data_currently_in_use,apis_currently_in_use,base_url)

        if found_the_api_object == True:
            suggested_url = ""

        if found_the_api_object == False:
            suggest = []
            
            for i in range(len(available_paths)):
                if url.lower() in available_paths[i].lower():
                    suggest.append(available_paths[i])

            if len(suggest) == 0:
                print("[-] No API path found")
                print("")
            else:
                print("[-] URL path is not present in the code perhaps you meant ")
                print("")
                for i in range(len(suggest)):
                    print("[" + str(i) + "]",suggest[i])
                print("")
                suggestion_user = input("> Enter the index of the API (default 0): ")

                if suggestion_user == "":
                    suggestion_number = 0
                    suggested_url = suggest[suggestion_number]
                else:
                    suggestion_number = int(suggestion_user)
                    suggested_url = suggest[suggestion_number]
                    
                print("")
        else:
            # retry = isAffirmative(input("[+] Wanna run again : "))
            found_the_api_object = False

def response_parser(data,response,api_data,base_url):
    print("")
    if (type(response) != str and response.get("errorCode") == "INVALID_TOKEN") or (type(response) != str and response.get("errorMessage") == "Header \"token\" is missing" ) :
        answer = input("[+] Token is not present shall I generate for you : ")

        if isAffirmative(answer):
            return (auth_and_verify(data,api_data,base_url),False)

    try:
        for x in response:
            data[x] = response[x]
            print("[+] Added ",x,"=",str(response[x]),"in data")

            if x == "estimates" and len(response[x]) > 0:
                data["estimateId"] = response[x][0].get("id")
                print("[+] Added estimateId =",response[x][0].get("id"))
            elif x == "selectedQuotes" and len(response[x]) > 0:
                data["quoteId"] = response[x][0].get("id")
                print("[+] Added quoteId =",response[x][0].get("id"))
            elif x == "searchRequestsForDriver" and len(response[x]) > 0: 
                data["searchRequestId"] = response[x][0].get("searchRequestId")
                print("[+] Added searchRequestId = ",data["searchRequestId"])
            elif x == "list" and len(response[x]) > 0:
                rides = response[x]
                rideList = next((ride for ride in rides if ride['status'] == 'NEW'), None)
                data["rideId"] = rideList['id'] if rideList else None
                print("[+] Added rideId = ",data["rideId"])
        return (data,True)
    except:
        return (data,True)
       
def make_api_call_on_success(api_object,data,request,base_url,query_parameters):
    return make_curl_request(api_object.get('url_path'),api_object.get('request_type'),request,base_url,data,query_parameters)

def main():
    try:
        api_runner()
    except KeyboardInterrupt:
        print("")
        print("[+] See ya !")



if __name__ == "__main__":
    main()

