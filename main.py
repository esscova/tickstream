import asyncio

from tradingview_client import (
    conectar,
    inscrever_ativos,
    receber_mensagens,
)

from quote import Quote
from terminal import exibir_cotacao




async def main():
    ws, quote_session = await conectar()

    try:
        await inscrever_ativos(ws, quote_session)

        print("Conectado ao TradingView.")
        print("Aguardando cotações...\n")

        cotacoes = {}

        async for mensagem in receber_mensagens(ws):

            if mensagem.get("m") != "qsd":
                continue

            parametros = mensagem.get("p", [])

            if len(parametros) < 2:
                continue

            payload = parametros[1]

            symbol = payload.get("n")
            dados = payload.get("v", {})

            if not symbol or not isinstance(dados, dict):
                continue

            quote = cotacoes.setdefault(
                symbol,
                Quote(symbol=symbol),
            )

            if quote.update(dados):
                exibir_cotacao(symbol, quote.fields)

    finally:
        await ws.close()
        await ws.wait_closed()


if __name__ == "__main__":
    try:
        asyncio.run(main())

    except KeyboardInterrupt:
        print("\nMonitoramento encerrado.")

