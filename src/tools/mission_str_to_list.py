import json

mission_obj = []

with open('missionlist.txt', 'r', encoding='utf-8') as f:
    mission_list = f.readlines()
for i in range(len(mission_list) // 3):
    mission_obj.append({
        'id': f'ms{i}',
        'data': {
            'name': mission_list[3 * i].replace('\n', ''),
            'desc': mission_list[3 * i + 1].replace('\n', ''),
            'target': int(mission_list[3 * i + 2].replace('\n', ''))
        }
    })
with open('missionlist.json', 'w', encoding='utf-8') as f:
    json.dump(mission_obj, f, ensure_ascii=False, indent=2)
