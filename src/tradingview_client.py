"""
modulo responsavel pela comunicacao com o servidor
"""
import asyncio
from websockets.asyncio.client import connect

from config import URL, HEADERS, SYMBOLS, RECV_TIMEOUT
from protocol import generate_session, send_message, parse_messages


async def conectar():
    ws = await connect(
        URL,
        additional_headers=HEADERS,
    )

    await send_message(
        ws,
        "set_auth_token",
        ["unauthorized_user_token"],
    )

    quote_session = generate_session()

    await send_message(
        ws,
        "quote_create_session",
        [quote_session],
    )

    await send_message(
        ws,
        "quote_set_fields",
        [
            quote_session,
            "lp",
            "ch",
            "chp",
            "volume",
            "bid",
            "ask",
            "high_price",
            "low_price",
            "open_price",
            "prev_close_price",
            "description",
            "short_name",
        ],
    )

    return ws, quote_session


async def inscrever_ativos(ws, quote_session):
    for symbol in SYMBOLS:
        await send_message(
            ws,
            "quote_add_symbols",
            [quote_session, symbol],
        )

async def receber_mensagens(ws):
    while True:
        try:
            raw = await asyncio.wait_for(
                ws.recv(),
                timeout=RECV_TIMEOUT,
            )

        except asyncio.TimeoutError:
            continue

        for tipo, conteudo in parse_messages(raw):

            if tipo == "heartbeat":
                await ws.send(
                    f"~m~{len(conteudo)}~m~{conteudo}"
                )

            elif tipo == "json":
                yield conteudo