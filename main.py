"""
Script para monitorar cotações em tempo real com dados do trandingview
"""

# DEPENDENCIAS #
import random
import string
import json

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