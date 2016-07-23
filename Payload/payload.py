import requests

def geturlwithparams(useridexcel) :
    userdata = {"userid":useridexcel}
    resp = requests.post('http://jsonplaceholder.typicode.com/posts', data=userdata)
    return resp