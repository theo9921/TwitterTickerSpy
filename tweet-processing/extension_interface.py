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
        "Most tweeted company": data[0],
        "# of mentions": data[1],
        "ESG of most tweeted company": data[2],
        "Average ESG": data[3]
    }

    # update
    put_response = requests.put('http://localhost:3000/data/1/', json=myobj)
    print("Update STATUS:", put_response.status_code)
