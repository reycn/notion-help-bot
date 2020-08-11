import re
from termcolor import cprint

def output_clean(text):
    text = text.replace('（', '(').replace('）', ') ')
    text = text.replace('「', '“').replace('」', '”')
    text = text.replace('@', ' @')
    text = text.replace('：//', '://')
    text = text.replace('HTTPS：/ /', 'https://')
    # text = text.replace('/////', '\n')
    text = re.sub('\/{2,}', '', text)
    text = text.replace('@fanyi_bot ', '')
    return text


def output(result, end_str_id=1):
    # end_str = '\n\n`─────`\n🤖 By [中文翻译机器人](https://t.me/fanyi_bot)'
    end_str = ''
    if end_str_id == 2:
        end_str = ''
    msg_str = output_clean(result)
    try:
        cprint(
            '　' + msg_str.replace('\n', '').replace('\n', ' | ').replace(
                '🇺🇸', '').replace('🇨🇳', ''), 'cyan')
    except Exception as e:
        print('　' + msg_str.replace('\n', '').replace('\n', ' | ').replace(
            '🇺🇸', '').replace('🇨🇳', ''))
        cprint(e, 'white', 'on_red')
    msg_str += end_str
    return msg_str


def get_text(msg):
    if 'text' in msg:
        return msg['text']
    else:
        return msg['caption']


def inline_clean(text):
    text = text.replace('*', '\*')
    return (text)
