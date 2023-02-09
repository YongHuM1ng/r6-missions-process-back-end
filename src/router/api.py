from fastapi import APIRouter
from starlette.responses import FileResponse

router = APIRouter(prefix='/api')


@router.get('/mission_list')
async def api_mission_list():
    return FileResponse('src/data/mission_list.json', media_type='application/json')
