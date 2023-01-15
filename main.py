import json
from fastapi import FastAPI
from fastapi.responses import Response
import uvicorn
from models.AppleService import AppleService
import logging
logging.basicConfig(filename='app.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s')
"""
Fast api service to create a an API to talk to the AppleScraper service
"""
app = FastAPI()
appleService = AppleService()


@app.get("/top100appleapps")
async def get_top_100_apps():
    """
    a method to get the top 100 free apple apps from the service
    :return: Json Response with all apps data
    """
    results = appleService.get_top_100_apps()
    return Response(content=json.dumps(results, indent=2), status_code=200, media_type="application/json")


@app.get("/App/{app_name}")
def get_app(app_name: str):
    """
    an endpoint to get a specific app data
    :param app_name: app to retrieve data for
    :return:
    """
    appData = appleService.get_app(app_name)
    return Response(content=json.dumps(appData, indent=2), status_code=200, media_type="application/json")


if __name__ == "__main__":
    """
    run the Fast Api Server
    """
    uvicorn.run(app=app, host='0.0.0.0', port=8000)
