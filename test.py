# Deeper Systems RL Challenge
# 26 March 2021.

import json


def main():
    with open('source_file_2.json') as json_file:
        data = json.load(json_file)

    s_Data = sorted(data, key=lambda x: abs(0 - x['priority']))

    managers = {} # json1 dump
    watchers = {} # json2 dump

    for item in s_Data:
        for manager in item['managers']:
            if not manager in managers:
                managers[manager] = []
            managers[manager].append(item['name'])

        for watcher in item['watchers']:
            if not watcher in watchers:
                watchers[watcher] = []
            watchers[watcher].append(item['name'])

    with open('managers.json', 'w') as managers_json:
        json.dump(managers, managers_json)

    with open('watchers.json', 'w') as watchers_json:
        json.dump(watchers, watchers_json)

main()