import requests
import json
import time
from prompt_toolkit import prompt
from prompt_toolkit.completion import WordCompleter
from prompt_toolkit.completion import Completer, Completion
from datetime import datetime, timezone
import subprocess
import sys
import random

driver_normal_auth_succeed = True
customer_normal_auth_succeed = True

customer_base_url = "http://localhost:8013"
driver_base_url = "http://localhost:8016"

which_api_we_are_using = "customer"

customer_url = "http://localhost:8013/openapi"
driver_url = "http://localhost:8016/openapi"

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

default_ride_start_request = {
    "rideOtp": "0000",
    "point": {
        "lat": 12.959849,
        "lon": 77.611269
    }
}

default_ride_end_request = {
    "point": {
        "lat": 12.959849,
        "lon": 77.611269
    }
}

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

# return type = {'name' : 'value','name': 'value'}

def query_parameter_filler(path,query_parameter_list,data):

    (body,isRequestBodyException,isQueryParamException) = handle_openapi_exception(path,data,"")

    if isQueryParamException:
        return body

    required_query_parameters = [parameter for parameter in query_parameter_list if parameter.get('required') == True ]
    non_required_query_parameters = [parameter for parameter in query_parameter_list if parameter.get('required') == False ]
    answers = {}

    for parameter in required_query_parameters:
        (sanitized_input,isSuccess) = input_sanitizer(data.get(str(parameter.get('name'))),str(parameter.get('type')))
        answers[str(parameter.get('name'))] = sanitized_input

    return answers

# return (body,isRequestBodyException,isQueryParamException)
def handle_openapi_exception(path,data,rideOtp):

    request_body = {}

    if path == '/ui/driver/location':
        pt_lat = 12.846907
        pt_lon = 77.556936
        ts = datetime.utcnow().replace(tzinfo=timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

        return ([
                {
                    "pt": {
                        "lat": pt_lat,
                        "lon": pt_lon
                    },
                    "ts": ts
                }
            ],True,False)
    elif path == '/v2/rideBooking/list' or path == '/ui/driver/ride/list':
        return ({'onlyActive' : True},False,True)

    elif path.startswith("/ui/driver/ride/") and path.endswith("/start"):
        default_ride_start_request["rideOtp"] = rideOtp
        print("ride start request is ",default_ride_start_request)
        return (default_ride_start_request,True,False)

    elif path.startswith("/ui/driver/ride/") and path.endswith("/end"):
        return (default_ride_end_request,True,False) 

    return ({},False,False)




def request_body_filler(initial_prompt,req_body,api_object,index,data,path,driver_data):

    (body,isRequestBodyException,isQueryParamException) = handle_openapi_exception(path,data,driver_data.get("rideOtp"))

    if isRequestBodyException:
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
                body[param] = data.get(param)
            else:
                body[param] = request_body_filler(initial_prompt + " [ " + param + " ] " ,req_body.get("properties").get(param),api_object,index,data,path,driver_data)

    # print(beautify_json(body))
    return body

def one_of_request_body_sorter(req_body):

    if req_body == None or len(req_body) == 0 or req_body[0] == None or req_body[0].get('oneOf') == None:
        return req_body
    
    else :
        listy = []
        for x in range(len(req_body[0].get('oneOf'))):
            listy.append(req_body[0].get('oneOf')[0])
        return listy

def loader(prompt,delay):
    underscores = '-' * 10 * delay  # Number of underscores to display
    delay_between_frame = 0.1  # Delay between each frame
    
    
    for i in range(len(underscores)):
        spaces = ' ' * (len(underscores) - i - 1)
        sys.stdout.write('\r' + prompt + " (" + underscores[:i] + '>' + spaces + ")")
        sys.stdout.flush()
        time.sleep(delay_between_frame)

def ride_flow(customer_api_data,driver_api_data):

    found = url_runner('/ui/auth',customer_api_data,driver_api_data,"driver")
    found = url_runner('/ui/auth/{authId}/verify',customer_api_data,driver_api_data,"driver")
    found = url_runner('/ui/driver/setActivity',customer_api_data,driver_api_data,"driver")
    found = url_runner('/ui/driver/location',customer_api_data,driver_api_data,"driver")
    found = url_runner('/ui/driver/profile',customer_api_data,driver_api_data,"driver")

    found = url_runner('/v2/auth',customer_api_data,driver_api_data,"customer")
    found = url_runner('/v2/auth/{authId}/verify',customer_api_data,driver_api_data,"customer")
    found = url_runner('/v2/rideSearch',customer_api_data,driver_api_data,"customer")
    # time.sleep(3)
    loader("Getting estimates",5)
    found = url_runner('/v2/rideSearch/{searchId}/results',customer_api_data,driver_api_data,"customer")
    found = url_runner('/v2/estimate/{estimateId}/select2',customer_api_data,driver_api_data,"customer")

    loader("Getting nearby ride request",5)
    found = url_runner('/ui/driver/nearbyRideRequest',customer_api_data,driver_api_data,"driver")
    found = url_runner('/ui/driver/searchRequest/quote/offer',customer_api_data,driver_api_data,"driver")

    loader("Getting quotes",5)
    found = url_runner('/v2/estimate/{estimateId}/quotes',customer_api_data,driver_api_data,"customer")
    found = url_runner('/v2/rideSearch/quotes/{quoteId}/confirm',customer_api_data,driver_api_data,"customer")
    loader("Getting rides ",5)
    found = url_runner('/v2/rideBooking/list',customer_api_data,driver_api_data,"customer")
    found = url_runner('/ui/driver/ride/list',customer_api_data,driver_api_data,"driver")
    found = url_runner('/ui/driver/ride/{rideId}/start',customer_api_data,driver_api_data,"driver")
    found = url_runner('/ui/driver/ride/{rideId}/end',customer_api_data,driver_api_data,"driver")





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

    try:
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
    except:
        print("[+] I am not able to hit " + base_url + url + " is the server running ? ")
        raise Error("Not able to hit the url")

def beautify_json(json_text):
    try:
        beautified_json = json.dumps(json_text, indent=4)
        return beautified_json
    except json.JSONDecodeError:
        return None

def config_loader(url):
    final_list = []
    try:
        open_api_json = make_curl_request(url,"get","","",{},{})
    except:
        raise Error("Not able to hit the url")
        return
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

# url_path,customer_data,driver_data,customer_api_data,driver_api_data,customer_base_url,driver_base_url

def url_runner(url,customer_api_data,driver_api_data,which_entity):
    print("")
    print("==> url is ",url)
    print("")

    data = None
    api_data = None
    base_url = None
    other_entity_data = None

    if which_entity == "driver":
        api_data = driver_api_data
        data = driver_data
        base_url = driver_base_url
        other_entity_data = customer_data
    elif which_entity == "customer":
        api_data = customer_api_data
        data = customer_data
        base_url = customer_base_url
        other_entity_data = driver_data

    # if url == '/v2/auth/{authId}/verify':
    #     print("which entity is ",which_entity)
    #     print("api_data is ",api_data)

    for api_object in api_data:

        if api_object['url_path'] == url:
            request_body = {}
            path_contents = api_object['url_path'].split('/')
            
            for c in range(len(path_contents)):
                if "{" in path_contents[c]:
                    path_contents[c] = data.get(path_contents[c][1:-1])


            final_path = '/'.join(path_contents)

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
            parameterObjects = query_parameter_filler(final_path,queryParametersList,data)

            response = None
            request_body = None
            if len(api_object.get("request_body")) != 0:  
                print("")
                index = 0

                if data.get(final_path) != None:
                        request_body = data.get(final_path)
                else:
                    request_body = request_body_filler("",api_object.get("request_body")[index],api_object,index,data,final_path,driver_data)
                
            response = make_api_call_on_success(final_path,api_object,data,request_body,base_url,parameterObjects)
                                  
                

            (data,other_entity_data,should_show_response) = response_parser(data,response,api_data,base_url,other_entity_data,which_entity,customer_api_data,driver_api_data,url)

            if should_show_response:
                print("")
                print("==> Fetching the response")
                print("") 
                print(beautify_json(response))
                print("")

            
            return True
    
    print("[-] I was not able to hit the url")
    return False

def api_runner():
    print("")
    try:
        customer_api_data = config_loader(customer_url)
        driver_api_data = config_loader(driver_url)
        ride_flow(customer_api_data,driver_api_data)
    except:
        return
         
    # (data_currently_in_use,found_the_api_object) = url_runner(url,data_currently_in_use,apis_currently_in_use,base_url)

def rescuer(response,which_entity,customer_api_data,driver_api_data,url_path):

    if not isinstance(response, dict):
        return False



    if response.get("errorCode") == "HITS_LIMIT_EXCEED":
        inp = input("> Hits limit is reached shall I flush redis ? ")

        if isAffirmative(inp):
            print("[+] Flushed Redis Main Cluster")
            subprocess.run(["redis-cli", "-p", "6379", "FLUSHALL"])

            # Flushing Redis Cluster 1
            print("[+] Flushed Redis Cluster 1")
            subprocess.run(["redis-cli", "-p", "30001", "FLUSHALL"])

            # Flushing Redis Cluster 2
            print("[+] Flushed Redis Cluster 2")
            subprocess.run(["redis-cli", "-p", "30002", "FLUSHALL"])

            # Flushing Redis Cluster 3
            print("[+] Flushed Redis Cluster 3")
            subprocess.run(["redis-cli", "-p", "30003", "FLUSHALL"])
            
            if which_entity == "customer":
                found = url_runner('/v2/auth',customer_api_data,driver_api_data,"customer")

            elif which_entity == "driver":
                found = url_runner('/ui/auth',customer_api_data,driver_api_data,"driver")
            
            return False


    elif response.get("errorMessage") == "ACTIVE_BOOKING_ALREADY_PRESENT":
        inp = input("> Active booking is present shall I change the customer number ? ")
        if isAffirmative(inp):
            customer_data["mobileNumber"] = str(random.randrange(10**9, 10**10))
            found = url_runner('/v2/auth',customer_api_data,driver_api_data,"customer")
            found = url_runner('/v2/auth/{authId}/verify',customer_api_data,driver_api_data,"customer")
            found = url_runner('/v2/rideSearch',customer_api_data,driver_api_data,"customer")
            loader("Getting estimates",5)
            found = url_runner('/v2/rideSearch/{searchId}/results',customer_api_data,driver_api_data,"customer")

            return False

    elif response.get("estimates") == []:
        inp = print("Estimates are not coming, please ensure driver offer allocator is running ")

        inp = input("> Shall I rerun the request : ")

        if isAffirmative(inp):
            found = url_runner('/v2/rideSearch',customer_api_data,driver_api_data,"customer")
            loader("Getting estimates",5)
            found = url_runner('/v2/rideSearch/{searchId}/results',customer_api_data,driver_api_data,"customer")
        else:
            inp = input("> Shall I register a driver and put it into that location : ")

            if isAffirmative(inp):
                driver_number = str(random.randrange(10**9, 10**10))
                driver_data["mobileNumber"] = driver_number
                print("[+] Registering the driver with ",driver_data["mobileNumber"])
                print("")
                subprocess.run(f"python3 /Users/juspay/NammaYatriMagic/register-driver.py " + driver_number, shell=True)
                found = url_runner('/ui/auth',customer_api_data,driver_api_data,"driver")
                found = url_runner('/ui/auth/{authId}/verify',customer_api_data,driver_api_data,"driver")
                found = url_runner('/ui/driver/setActivity',customer_api_data,driver_api_data,"driver")
                found = url_runner('/ui/driver/location',customer_api_data,driver_api_data,"driver")
                found = url_runner('/ui/driver/profile',customer_api_data,driver_api_data,"driver")
                found = url_runner('/v2/rideSearch',customer_api_data,driver_api_data,"customer")
                loader("Getting estimates",5)
                found = url_runner('/v2/rideSearch/{searchId}/results',customer_api_data,driver_api_data,"customer")
        return False
    
    elif response.get("errorCode") == "INTERNAL_ERROR":
        inp = input("> Internal error is coming shall I rerun the request : ")

        if isAffirmative(inp):
            found = url_runner(url_path,customer_api_data,driver_api_data,which_entity)
        return False
    return True



def response_parser(data,response,api_data,base_url,other_entity_data,which_entity,customer_api_data,driver_api_data,url_path):

    isAllGood = rescuer(response,which_entity,customer_api_data,driver_api_data,url_path)

    
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

                if which_entity == "driver":
                    rides = response[x]
                    rideList = next((ride for ride in rides if ride['status'] == 'NEW'), None)
                    data["rideId"] = rideList['id'] if rideList else None
                    print("[+] Added rideId = ",data["rideId"])
                elif which_entity == "customer":
                    bookings = response[x]
                    bookingObject = next((booking for booking in bookings if booking['status'] == 'TRIP_ASSIGNED'), None)
                    other_entity_data["rideOtp"] = bookingObject['rideList'][0]['rideOtp'] if bookingObject else None
                    print("[+] Added rideOtp = ",other_entity_data["rideOtp"])



        
        return (data,other_entity_data,isAllGood)
    except:
        return (data,other_entity_data,isAllGood)
       
def make_api_call_on_success(final_path,api_object,data,request,base_url,query_parameters):
    return make_curl_request(final_path,api_object.get('request_type'),request,base_url,data,query_parameters)

def main():
    try:
        api_runner()
    except KeyboardInterrupt:
        print("")
        print("[+] See ya !")

if __name__ == "__main__":
    main()

