import string
import time
from collections import defaultdict

from loguru import logger
from src.data import DATA_DIR
from src.utils.io import read_json


class InstaChatDecoder:
    
    def __init__(self, chat_json):
        """
        """
        # load chat data
        logger.info(f"Loading chat data from {chat_json}")
        self.chat_data = read_json(DATA_DIR / 'message_1.json')

        self.fa_translate = read_json(DATA_DIR / 'fa_translate.json')
        self.emoji = read_json(DATA_DIR / 'emoji_translate.json')

    def emoji_replace(self, txt):
        for k in self.emoji.keys():
            txt = txt.replace(k, self.emoji[k])
        return txt
    
    def word_translator(self, txt, unknown_replacement = False):
        allowed_letters = string.ascii_letters + '''-><*+!_:..’'"@#''' + "".join(self.emoji.values())
        i = 0
        decoded = ''
        while i < len(txt):
            if txt[i] == ' ':
                i += 1
                decoded += ' '
                continue
            if txt[i] == '\n':
                i += 1
                decoded += ' '
                continue
                    
            if txt[i] in allowed_letters:
                decoded += txt[i]
                i += 1
                continue

            # (Removed) because som characer are 4, 6 or 8 item combined
            # item = txt[i:i+4]
            # if self.chat_data.get(item):
            #     decoded += self.chat_data[item]
            #     i += 4
            #     continue

            item = txt[i:i+2]
            rep_item = item
            if unknown_replacement:
                rep_item = unknown_replacement
            decoded += self.chat_data.get(item, rep_item)
            i += 2
        return decoded


    def translator(self):
        result = defaultdict(list)
        for msg in self.chat_data['messages']:
            if not msg.get('content'):
                continue
            if "sent an attachment." in msg['content']:
                continue
            if msg['content'] == 'Liked a message':
                continue
            result['messages'].append({
                'sender_name': self.word_translator(msg['sender_name']," "),
                # 'timestamp_ms': msg['timestamp_ms'],
                'timestamp_ms': time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(msg['timestamp_ms'] / 1000)),
                'content': self.word_translator(self.emoji_replace(msg['content']), ' ')})
        return result


if __name__ == "__main__":
    insta_chat = InstaChatDecoder(chat_json=DATA_DIR / 'message_1.json')
    insta_chat.translator()

    print("*********************************************Done!*********************************************")
