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


def parse_messages(raw: str) -> list:
    messages = []
    pos = 0

    while True:
        start = raw.find("~m~", pos)

        if start == -1:
            break

        len_start = start + 3
        len_end = raw.find("~m~", len_start)

        if len_end == -1:
            break

        try:
            length = int(raw[len_start:len_end])
        except ValueError:
            pos = len_end
            continue

        content_start = len_end + 3
        content = raw[content_start:content_start + length]

        if content.startswith("~h~"):
            messages.append(("heartbeat", content))
        else:
            try:
                messages.append(("json", json.loads(content)))
            except json.JSONDecodeError:
                messages.append(("raw", content))

        pos = content_start + length

    return messages

if __name__ == '__main__':
    # Simula uma mensagem JSON no formato do TradingView
    conteudo = '{"m":"qsd","p":["session",{"n":"PETR4","v":{"lp":32.50}}]}'

    mensagem = f"~m~{len(conteudo)}~m~{conteudo}"
    heartbeat = "~m~5~m~~h~123"

    resultado = parse_messages(mensagem)

    print(parse_messages(heartbeat))
    print(resultado)