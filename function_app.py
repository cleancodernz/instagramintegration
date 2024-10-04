import json
import azure.functions as func
import requests
import logging

app = func.FunctionApp(http_auth_level=func.AuthLevel.FUNCTION)

@app.route(route="instagramintegration")
def instagramintegration(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    # You'll need to handle getting an access token either via OAuth2 flow or store a long-lived access token.
    access_token = "<YOUR_INSTAGRAM_ACCESS_TOKEN>"

    images = get_instagram_media(access_token)
    if images:
        return func.HttpResponse(
            body=json.dumps(images),
            mimetype="application/json",
            status_code=200
        )
    else:
        return func.HttpResponse(
            body="Failed to retrieve images",
            status_code=500
        )

    # name = req.params.get('name')
    # if not name:
    #     try:
    #         req_body = req.get_json()
    #     except ValueError:
    #         pass
    #     else:
    #         name = req_body.get('name')

    # if name:
    #     return func.HttpResponse(f"Hello, {name}. This HTTP triggered function executed successfully.")
    # else:
    #     return func.HttpResponse(
    #          "This HTTP triggered function executed successfully. Pass a name in the query string or in the request body for a personalized response.",
    #          status_code=200
    #     )
    
# Function to get media from Instagram Graph API
def get_instagram_media(access_token):
    url = f'https://graph.instagram.com/me/media?fields=id,media_type,media_url&access_token={access_token}'
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        media = data.get('data', [])
        images = [item['media_url'] for item in media if item['media_type'] == 'IMAGE']
        return images
    else:
        logging.error(f"Failed to fetch Instagram media: {response.status_code}")
        return []