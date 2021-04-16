import requests
import json
import decouple


def apiCutFunction(imgUrl):
    url = "https://background-removal.p.rapidapi.com/remove"
    img = 'image_url=' + imgUrl
    apiKey = decouple.config('RAPPID_API_KEY2')
    headers = {
        'content-type': "application/x-www-form-urlencoded",
        'x-rapidapi-key': apiKey,
        'x-rapidapi-host': "background-removal.p.rapidapi.com"
    }

    response = requests.post(url, data=img, headers=headers)

    result = json.loads(response.text)
    print(result['response']['image_url'])
    return(result['response']['image_url'])
