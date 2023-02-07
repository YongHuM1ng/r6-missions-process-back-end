from fastapi import FastAPI
from starlette.responses import FileResponse
from starlette.staticfiles import StaticFiles
import src.router.api as api

app = FastAPI()

app.mount('/static', StaticFiles(directory='src/static', html=True))
app.mount('/assets', StaticFiles(directory='src/static/assets', html=True))
app.include_router(api.router)


@app.get('/')
async def index():
    return FileResponse('src/static/index.html', media_type='text/html')


# @app.get('/api/missionlist')
# async def api_missionlist():
#     return FileResponse('static/assets/missionlist.json', media_type='application/json')
