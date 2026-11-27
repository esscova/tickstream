"""
configurações do projeto
"""

SYMBOLS = [
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