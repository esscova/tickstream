"""
Script para monitorar cotações em tempo real com dados do trandingview
"""

# DEPENDENCIAS #
import random
import string
import json
from websockets.asyncio.client import connect
import asyncio
import time
from datetime import datetime

# CONSTANTES #
TICKERS = [
    "BMFBOVESPA:ALOS3",
    "BMFBOVESPA:BBAS3",
    "BMFBOVESPA:BBDC3",
    "BMFBOVESPA:BBSE3",
    "BMFBOVESPA:CPFE3",
    "BMFBOVESPA:CXSE3",
    "BMFBOVESPA:EGIE3",
    "BMFBOVESPA:GGBR4",
    "BMFBOVESPA:ITUB3",
    "BMFBOVESPA:KLBN4",
    "BMFBOVESPA:SUZB3",
    "BMFBOVESPA:TAEE4",
    "BMFBOVESPA:VIVT3",
]

URL = (
    "wss://widgetdata.tradingview.com/socket.io/websocket"
    "?from=embed-widget/market-quotes/bovespa/"
)

HEADERS = {
    "Origin": "https://www.tradingview-widget.com",
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    ),
}

RECV_TIMEOUT = 5        # segundos sem mensagem antes de avisar
STATUS_INTERVAL = 10    # segundos entre os relatórios de status

# AUXILIARES #
def generate_session() -> str:
    """Cria um identificador aleatório para a sessão de cotações"""
    return "qs_" + "".join(random.choices(string.ascii_lowercase, k=12))

async def send_message(ws, method:str, params:list) -> None:
    """
    Monta e envia uma mensagem no protocolo do TradingView
    
    Args:
        ws: objeto retornado pela função `connect`
        method: ação a ser executada pelo servidor
        params: lista de argumentos para method
    """
    msg = json.dumps({"m":method, "p":params}) # -> json 
    await ws.send(f"~m~{len(msg)}~m~{msg}") # framing do protocolo

def parse_messages(raw:str) -> list[tuple]:
    """
    Recebe o texto que chegou do websocket e separa 'heartbeat', 'json' e 'raw'
    """
    messages = []
    pos = 0

    while True:
        start = raw.find('~m~',pos)
        if start == -1:
            break

        len_start = start + 3
        len_end  = raw.find('~m~', len_start)
        if len_end == -1:
            break

        try:
            length = int(raw[len_start:len_end])
        except ValueError:
            pos = len_end
            continue

        content_start = len_end + 3
        content = raw[content_start:content_start + length]

        if content.startswith('~h~'):
            messages.append(('heartbeat', content))
        else:
            try:
                messages.append(('json', json.loads(content)))
            except json.JSONDecodeError:
                messages.append(('raw', content))
        pos = content_start + length

    return messages

def formatar(valor, fmt:str) -> str:
    return format(valor, fmt) if valor is not None else 'N/D'

async def monitorar() -> None:
    print('Conectando...')

    async with connect(
        uri=URL,
        additional_headers=HEADERS,
        ping_interval=None, #tradingview ja usa o proprio heartbeat :: ~h~
        open_timeout=10,
    ) as ws:
        print('Conectado!\n')

        await send_message(ws, 'set_auth_token', ['unauthorized_user_token'])
        await asyncio.sleep(.3)

        session = generate_session()
        await send_message(ws, 'quote_create_session', [session])
        await asyncio.sleep(.3)

        await send_message(ws, 'quote_set_fields', [
            session, 'lp', 'ch', 'volume', 'bid', 'ask',
            'high_price', 'low_price', 'open_price', 'prev_close_price',
            'description', 'short_name',
        ])
        await asyncio.sleep(.3)

        print(f'Inscrevendo {len(TICKERS)} ativos...')
        for ticker in TICKERS:
            await send_message(ws, 'quote_add_symbols', [session, ticker])
            await asyncio.sleep(.08)
        print('\n=== MONITORANDO COTAÇÕES ===\n')

        cotacoes:dict[str, dict]      = {}
        ultimo_preco:dict[str, float] = {}
        contador = 0
        ultimo_status = time.monotonic()

        while True:
            try:
                raw = await asyncio.wait_for(ws.recv(), timeout=RECV_TIMEOUT)
            except asyncio.TimeoutError:
                print(
                    f'[{datetime.now():%H:%M:%S}]'
                    f'Nenhuma mensagem recebida nos últimos {RECV_TIMEOUT} segundos.'
                )
                continue
            
            contador += 1
            if time.monotonic() - ultimo_status >= STATUS_INTERVAL:
                print(
                    f'[{datetime.now():%H:%M:%S}]'
                    f'Mensagens recebidas: {contador}.'
                )
                contador = 0
                ultimo_status = time.monotonic()

            if isinstance(raw, bytes):
                raw = raw.decode('utf-8', errors='replace')

            for tipo, content in parse_messages(raw):
                # responder heartbeat
                if tipo == 'heartbeat':
                    await ws.send(f'~m~{len(content)}~m~{content}')
                    continue

                # processar cotacoes
                if(tipo != 'json' 
                   or not isinstance(content, dict)
                   or content.get('m') != 'qsd'
                ):
                    continue

                payload = content['p'][1]
                symbol  = payload.get('n','')
                dados   = payload.get('v',{})
                estado = cotacoes.setdefault(symbol, {})
                estado.update(dados)

                if 'lp' not in estado:
                    continue
                preco = estado['lp']

                if ultimo_preco.get(symbol) == preco:
                    continue
                ultimo_preco[symbol] = preco

                var_txt = formatar(estado.get('ch'), ',+.2f')
                pct_txt = (f'{estado["chp"]:+.2f}%' if estado.get('chp') is not None else 'N/D')
                vol_txt = formatar(estado.get('volume'), ',.0f')
                bid_txt = formatar(estado.get('bid'), ',.2f')
                ask_txt = formatar(estado.get('ask'), ',.2f')

                print(
                    f"[{datetime.now():%H:%M:%S}] "
                    f"{symbol.replace('BMFBOVESPA:', ''):6} | "
                    f"Preço: R$ {preco:.2f} | "
                    f"Var.: {var_txt} ({pct_txt}) | "
                    f"Bid: {bid_txt} | "
                    f"Ask: {ask_txt} | "
                    f"Volume: {vol_txt}"
                )

# MAIN #
def main() -> None:
    try:
        asyncio.run(monitorar())
    except KeyboardInterrupt:
        print('\nEncerrando o monitoramento.')
    except Exception as e:
        print(f'Erro: {type(e).__name__}: {e}')

if __name__ == '__main__':
    main()