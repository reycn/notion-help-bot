import requests
import json
import demjson
from termcolor import cprint

def descipt_to_md(rich_text:str) -> str:
    rich_text = rich_text['properties']['消息']['rich_text']
    def parse_content(text:json) -> str:
        # print(text)
        if text['link']:
            url = text['link']['url']
            if url and url[0] == '/':
                url = 'https://www.notion.so' + url
            return f"[{text['content']}]({url})"
        else:
            return text['content']
    rich_text = ''.join([parse_content(i['text']) for i in rich_text])
    return rich_text

def fetch_commands(auth:str, db_id:str) -> dict:
    COMMANDS = []
    DB_URL = f'https://api.notion.com/v1/databases/{db_id}/query'
    CONT_TYPE = 'application/json'
    HEAD = {'Authorization': auth, \
            'Content-Type': CONT_TYPE,\
            'Notion-Version': '2021-05-13'}
    FILTER = '''{"filter":{"property":"启用", "checkbox":{"equals": true}}}'''.encode('utf-8')
    r = requests.post(DB_URL, headers=HEAD, data=FILTER)
    if r.status_code == 200:
        cprint(r.status_code, 'white', 'on_green')
        for result in r.json()['results']:
            COMMANDS.append([result['properties']['正则']['rich_text'][0]['plain_text'], descipt_to_md(result)])
        # print(COMMANDS)
        return COMMANDS
    else:
        err = json.loads(r.text)['message']
        cprint(f"{r.status_code}: {err}", 'white', 'on_red')
        return None


if __name__ == '__main__':
    try:
        cprint('Start running...', 'white', 'on_green')
        fetch_commands(auth=AUTH, db_id=DB_ID)
    except KeyboardInterrupt as k:
        cprint('\nKey pressed to interrupt...', 'white', 'on_red')
