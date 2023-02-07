from fastapi import FastAPI
from starlette.responses import FileResponse
from starlette.staticfiles import StaticFiles

app = FastAPI(docs_url=None, redoc_url=None)

app.mount('/static', StaticFiles(directory='static', html=True))
app.mount('/assets', StaticFiles(directory='static/assets', html=True))


@app.get('/')
async def _():
    return FileResponse('static/index.html', media_type='text/html')


@app.get('/api/missionlist')
async def _():
    return FileResponse('assets/missionlist.json', media_type='application/json')
