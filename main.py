import asyncio
from tradingview_client import conectar, inscrever_ativos


async def main():
    ws, quote_session = await conectar()

    try:
        await inscrever_ativos(ws, quote_session)

        print("Conectado ao TradingView.")
        print("Ativos inscritos com sucesso.")

        await asyncio.Future()

    finally:
        await ws.close()
        await ws.wait_closed()

if __name__ == "__main__":
    try:
        asyncio.run(main())

    except KeyboardInterrupt:
        print("\nMonitoramento encerrado.")
