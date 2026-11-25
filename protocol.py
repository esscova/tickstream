"""
modulo responsável por lidar com o protocolo de comunicação 
utilizado pelo projeto para conversar com o tradingview 
concentra as funções responsáveis por preparar e interpretar as mensagens
"""

import json
import random
import string

def generate_session() -> str:
    return 'qs_' + ''.join(
        random.choices(string.ascii_lowercase, k=12)
    )

def encode_messsage(method:str, params:list) -> str:
    message = json.dumps({'m':method, 'p':params})
    return f'~m~{len(message)}~m~{message}'

async def send_message(ws, method:str, params:list) -> None:
    message = encode_messsage(method, params)
    await ws.send(message)

if __name__ == '__main__':
    session = generate_session()
    print(session)
    print(len(session))

    message = encode_messsage(
        'set_auth_token',
        ['unauthorized_user_token']
    )
    print(message)