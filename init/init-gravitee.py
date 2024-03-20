import requests
import json
from os import listdir, getcwd

host_name = "host.docker.internal:8083"

base_url = "http://%s/management/organizations/DEFAULT/environments/DEFAULT" % host_name

bearer_token = "b74d25cf-131d-4b13-8d25-cf131deb132e"

specs_dir = getcwd() + "/api-specs/"

all_specs = listdir(specs_dir)

print(all_specs)


headers = {
    'Authorization' : "Basic YWRtaW46YWRtaW4=",
    'accept' : "application/json"
}

#test connection to gravitee
get_response = requests.get(url= "http://%s/management/v1/organizations/DEFAULT" % host_name,
                        headers= headers)

post_response = requests.get(url= base_url + "/apis",
                        headers= headers)

print(get_response.status_code)
print(get_response.content)

#post the oracle financials json
with open(specs_dir + "Oracle_cloud_finance_openapi_INVOICES.json") as financials:
    financials_content = {
        'format': "API",
        'type': "inline",
        'payload' : financials.read(),
        "with_documentation": True,
        "with_path_mapping": True,
        "with_policy_paths": False,
        "with_policies": [
        ]
    }
#post the petstore json
with open(specs_dir + "PetstoreSwagger.json") as petstore:
    petstore_content = {
        'format': "API",
        'type': "inline",
        'payload' : petstore.read(),
        "with_documentation": True,
        "with_path_mapping": True,
        "with_policy_paths": False,
        "with_policies": [
        ]
    }
    post_financials = requests.post(url=base_url + "/apis/import/swagger",
                                    headers= headers,
                                    json= financials_content)
    post_petstore = requests.post(url=base_url + "/apis/import/swagger",
                                    headers= headers,
                                    json= petstore_content)
    
    create_app_url = "http://%s/management/organizations/DEFAULT/environments/DEFAULT/applications" % host_name
    
    # create an app that consumes the oracle financials api
    financials_app_content = {
        "name": "Oracle Financials",
        "description": "This app allows access to the oracle financials set of api's.",
        "api_key_mode": "UNSPECIFIED",
        
    }
    financials_application = requests.post(url = create_app_url, headers= headers, json = financials_app_content)

    # create an app that consumes the petstore api
    petstore_app_content = {
        "name": "Petstore App",
        "description": "This app allows access to the petstore set of api's.",
        "api_key_mode": "UNSPECIFIED",
        
    }
    petstore_application = requests.post(url = create_app_url, headers= headers, json = petstore_app_content)

    # app to access both petstore and oracle financials api
    petstore_financials_app_content = {
        "name": "Petstore App",
        "description": "This app allows access to the petstore set of api's.",
        "api_key_mode": "UNSPECIFIED",
        
    }
    petstore_financials_application = requests.post(url = create_app_url, headers= headers, json = petstore_financials_app_content)
    

    financials_api_id =  json.loads(post_financials.content)["id"]
    petstore_api_id = json.loads(post_petstore.content)["id"]
    plans_url = "http://%s/management/organizations/DEFAULT/environments/DEFAULT/apis/%s/plans" % (host_name,financials_api_id)
    financials_plans_content = {
        "name": "Financials Exclusive Plan",
        "description": "Plan to allow access to the oracle financials api exclusively",
        "validation": "AUTO",
        "type": "API",
        "status": "PUBLISHED",
        "flow": {},
        "paths": None,
        "security": "KEY_LESS"
    }
    financials_plan = requests.post(url = create_app_url, headers= headers, json = financials_plans_content)
    print(financials_plan.status_code)








'''
    print(post_financials.status_code)
    print(post_petstore.status_code)
    print(financials_application.status_code)
    print(petstore_application.status_code)
    print(petstore_financials_application.status_code)
'''
r = requests.Response()
r.status_code = 400
