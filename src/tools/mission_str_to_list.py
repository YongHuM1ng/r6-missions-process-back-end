import json


def mission_str_to_list(mission_list: list) -> list:
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
    return mission_obj


# if __name__ == 'main':
#     with open('mission_list.txt', 'r', encoding='utf-8') as f:
#         mission_list = f.readlines()
#
#     with open('../data/mission_list.json', 'w', encoding='utf-8') as f:
#         # json.dump(mission_obj, f, ensure_ascii=False, indent=2)
#         json.dump(mission_obj, f, ensure_ascii=False, separators=(',', ':'))
