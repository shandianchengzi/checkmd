import requests

def checkUrl(url):
    try:
        response = requests.get(url)
        status_code = response.status_code
        status_text = response.reason
        # redirect but OK
        if response.history and status_code == 200:
            status_code = response.history[0].status_code
            status_text = response.url
        return status_code, status_text
    except requests.exceptions.RequestException as e:
        return 0, e