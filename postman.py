import requests
import json
from prompt_toolkit import prompt
from prompt_toolkit.completion import WordCompleter
from prompt_toolkit.completion import Completer, Completion

customer_url = "http://localhost:8013/openapi"
driver_url = "http://localhost:8016/openapi"

customer_base_url = "http://localhost:8013"
driver_base_url = "http://localhost:8016"


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


def request_body_filler(initial_prompt,req_body,api_object,index,data,path):
    # print("request body iz",req_body)

    all_properties_list = []

    for x in req_body.get('properties'):
        all_properties_list.append(x)

    # print(all_properties_list)

    non_required_properties = result = [x for x in all_properties_list if x not in req_body.get("required")]

    # print(non_required_properties)

    

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
    (data,found) = url_runner('/v2/auth',data,api_data,base_url)
    (data,found) = url_runner('/v2/auth/{authId}/verify',data,api_data,base_url)
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

def make_curl_request(url,request_type,request_body,base_url,data):

    print("")
    print("==> Hitting " + base_url + url )
    print("")

    api_key = data.get("token")
    headers = {"token": api_key}

    if request_type == "get":
        response = requests.get(base_url + url,headers=headers)
        try:
            return response.json()
        except:
            return response.text

    elif request_type == "post":
        response = requests.post(base_url + url,json=request_body,headers=headers)
        try:
            return response.json()
        except:
            return response.text

    elif request_type == "put":
        response = requests.put(base_url + url,json=request_body,headers=headers)
        try:
            return response.json()
        except:
            return response.text

    elif request_type == "delete":
        response = requests.delete(base_url + url,json=request_body,headers=headers)
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
    open_api_json = make_curl_request(url,"get","","",{})
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
                # print(path_contents[c])
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

            if len(api_object.get("request_body")) == 0:  
                response = make_api_call_on_success(api_object,data,None,base_url)
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
                
                response = make_api_call_on_success(api_object,data,request_body,base_url)
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
        "deviceToken": "8e83b5dc-99a0-4306-b90d-2345f3050972"
    }

    available_paths = []
    data_currently_in_use = customer_data
    apis_currently_in_use = customer_api_data
    which_api_we_are_using = "customer"
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
                if which_api_we_are_using == "customer":
                    print("==> Switching to Driver")
                    customer_data = data_currently_in_use
                    data_currently_in_use = driver_data
                    apis_currently_in_use = driver_api_data
                    which_api_we_are_using = "driver"
                    base_url = driver_base_url
                    available_paths = []
                    for i in range(len(apis_currently_in_use)) : 
                        available_paths.append(apis_currently_in_use[i]['url_path'])
                    completer = WordCompleter(available_paths)
                elif which_api_we_are_using == "driver":
                    print("==> Switching to Customer")
                    driver_data = data_currently_in_use
                    data_currently_in_use = customer_data
                    apis_currently_in_use = customer_api_data
                    which_api_we_are_using = "customer"
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
    if type(response) != str and response.get("errorCode") == "INVALID_TOKEN":
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
        return (data,True)
    except:
        return (data,True)
       
def make_api_call_on_success(api_object,data,request,base_url):
    return make_curl_request(api_object.get('url_path'),api_object.get('request_type'),request,base_url,data)

def main():
    api_runner()



if __name__ == "__main__":
    main()

