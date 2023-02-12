import json
from typing import Union
import os
from fastapi import Cookie, APIRouter, Body, Query
from starlette.responses import FileResponse

router = APIRouter(prefix='/api')
with open('src/data/token_index.json', 'r') as f:
    token_index = json.load(f)


@router.get('/mission_list')
async def api_mission_list(token: Union[str, None] = Cookie(default=None)):
    return FileResponse('src/data/mission_list.json', media_type='application/json', filename='114514')


@router.get('/token/verify')
async def api_token_verify(token: Union[str, None] = Cookie(default=None)):
    return token in token_index.values()


@router.get('/token/set')
async def api_token_set(qq: str, token: str):
    if qq in token_index:
        os.rename(f'src/data/cards/{token_index[qq]}.json', f'src/data/cards/{token}.json')
    token_index[qq] = token
    with open('src/data/token_index.json', 'w') as ff:
        json.dump(token_index, ff)
    return True


@router.get('/cards/get')
async def api_cards_get(token: Union[str, None] = Cookie(default=None)):
    try:
        with open(f'src/data/cards/{token}.json', 'r') as ff:
            cards = json.load(ff)
    except FileNotFoundError:
        with open(f'src/data/cards/{token}.json', 'w') as ff:
            cards = {'index': [], 'cards': {}}
            json.dump(cards, ff)
    for i in range(len(cards['index'])):
        cards['index'][i] = {'id': cards['index'][i]}
    return cards


@router.post('/cards/index')
async def api_cards_index(data: dict = Body(),
                          token: Union[str, None] = Cookie(default=None)):
    with open(f'src/data/cards/{token}.json', 'r') as ff:
        cards = json.load(ff)
    cards['index'] = data['data']
    with open(f'src/data/cards/{token}.json', 'w') as ff:
        json.dump(cards, ff)


@router.get('/cards/add')
async def api_cards_add(id_: str = Query(alias='id'),
                        token: Union[str, None] = Cookie(default=None)):
    with open(f'src/data/cards/{token}.json', 'r') as ff:
        cards = json.load(ff)
    cards['index'].insert(0, id_)
    cards['cards'][id_] = {"mission": "no-mission", "target": 0}
    with open(f'src/data/cards/{token}.json', 'w') as ff:
        json.dump(cards, ff)


@router.get('/cards/del')
async def api_cards_del(id_: str = Query(alias='id'),
                        token: Union[str, None] = Cookie(default=None)):
    with open(f'src/data/cards/{token}.json', 'r') as ff:
        cards = json.load(ff)
    cards['index'].remove(id_)
    cards['cards'].pop(id_)
    with open(f'src/data/cards/{token}.json', 'w') as ff:
        json.dump(cards, ff)


@router.post('/cards/modify')
async def api_cards_modify(id_: str = Body(alias="id"), data: dict = Body(),
                           token: Union[str, None] = Cookie(default=None)):
    with open(f'src/data/cards/{token}.json', 'r') as ff:
        cards = json.load(ff)
    cards['cards'][id_] = data
    with open(f'src/data/cards/{token}.json', 'w') as ff:
        json.dump(cards, ff)
