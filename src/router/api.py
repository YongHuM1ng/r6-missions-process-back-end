import json
import os
from typing import Union

from fastapi import Cookie, APIRouter, Body, Query
from starlette.responses import FileResponse

router = APIRouter(prefix='/api')
with open('src/data/token_index.json', 'r') as f:
    token_index = json.load(f)

with open('src/data/mission_add_list.json', 'r') as f:
    mission_add_list = json.load(f)


@router.get('/mission_list')
async def api_mission_list():
    return FileResponse('src/data/mission_list.json', media_type='application/json')


@router.get('/mission_list_text')
async def api_mission_list_text():
    return FileResponse('src/data/mission_list.txt', media_type='text/plain')


@router.post('/mission_list_text_update')
async def api_mission_list_text_update(data: dict = Body()):
    data['text'] = data['text'].rstrip()
    with open('src/data/mission_list.txt', 'w', encoding='utf-8') as ff:
        ff.write(data['text'].replace('\r', ''))
    mission_list = data['text'].split()
    mission_obj = []
    for i in range(len(mission_list) // 3):
        mission_obj.append({
            'id': f'ms{i}',
            'data': {
                'name': mission_list[3 * i].replace('\n', '')[:mission_list[3 * i].index('|')] if '|' in mission_list[
                    3 * i] else mission_list[3 * i].replace('\n', ''),
                'about': mission_list[3 * i].replace('\n', '')[mission_list[3 * i].index('|') + 1:] if '|' in
                                                                                                       mission_list[
                                                                                                           3 * i] else '',
                'desc': mission_list[3 * i + 1].replace('\n', ''),
                'target': int(mission_list[3 * i + 2].replace('\n', ''))
            }
        })
        if mission_obj[i]['data']['about'] == '':
            mission_obj[i]['data'].pop('about')
    with open('src/data/mission_list.json', 'w', encoding='utf-8') as ff:
        json.dump(mission_obj, ff, ensure_ascii=False, separators=(',', ':'))


@router.post('/mission_list_add')
async def api_mission_list_add(token: Union[str, None] = Cookie(default=None), data: dict = Body()):
    data['qq'] = next(key for key, value in token_index.items() if value == token)
    mission_add_list.append(data)
    with open('src/data/mission_add_list.json', 'w') as ff:
        json.dump(mission_add_list, ff)


@router.post('/mission_list_overlay')
async def api_mission_list_overlay(data: dict = Body()):
    mission_add_list.clear()
    for i in data['data']:
        mission_add_list.append(i)
    with open('src/data/mission_add_list.json', 'w') as ff:
        json.dump(mission_add_list, ff)


@router.get('/mission_list_add_get')
async def api_mission_list_add_get():
    return mission_add_list


@router.get('/token/verify')
async def api_token_verify(token: Union[str, None] = Cookie(default=None)):
    return token in token_index.values()


@router.get('/token/set')
async def api_token_set(qq: str, token: str):
    if qq in token_index:
        os.rename(f'src/data/cards/{token_index[qq]}.json', f'src/data/cards/{token}.json')
    token_index[qq] = token
    with open('src/data/mission_add_list.json', 'w') as ff:
        json.dump(token_index, ff)


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
