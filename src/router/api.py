from fastapi import APIRouter
from starlette.responses import FileResponse

router = APIRouter(prefix='/api')


@router.get('/missionlist')
async def api_missionlist():
    return FileResponse('../static/assets/missionlist.json', media_type='application/json')
