"""Functions for interfacing with Google Chrome extension"""
import requests

def get_twitter_handle():
    #get from server
    get_response = requests.get('http://localhost:3000/input/')
    json_response = get_response.json()

    #return handle
    return(json_response['handle'])

def update_server_data(data):
    myobj = {
        "mtc": data[0],
        "num_mentions": data[1],
        "mtc_esg": data[2],
        "esg_av": data[3]
    }

    # update
    put_response = requests.put('http://localhost:3000/data/1/', json=myobj)
    print("Update STATUS:", put_response.status_code)
