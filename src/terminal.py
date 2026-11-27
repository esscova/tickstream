"""
modulo responsavel pela apresentacao das cotacoes no terminal
"""



def formatar(valor, fmt):
    try:
        return fmt.format(valor)
    except (ValueError, TypeError):
        return "N/D"


def exibir_cotacao(symbol: str, dados: dict) -> None:
    nome = dados.get("short_name", symbol)

    preco = formatar(dados.get("lp"), "{:.2f}")
    variacao = formatar(dados.get("ch"), "{:+.2f}")
    variacao_percentual = formatar(dados.get("chp"), "{:+.2f}%")

    volume = formatar(dados.get("volume"), "{:,.0f}")
    maxima = formatar(dados.get("high_price"), "{:.2f}")
    minima = formatar(dados.get("low_price"), "{:.2f}")

    print(
        f"{nome:<8} "
        f"Preço: {preco:>8} "
        f"Variação: {variacao:>8} "
        f"({variacao_percentual:>8}) "
        f"Volume: {volume:>10} "
        f"Máx: {maxima:>8} "
        f"Mín: {minima:>8}"
    )

if __name__ == '__main__':

    dados = {
        "short_name": "PETR4",
        "lp": 32.50,
        "ch": 0.45,
        "chp": 1.40,
        "volume": 1500000,
        "high_price": 33.00,
        "low_price": 31.90,
    }

    exibir_cotacao("BMFBOVESPA:PETR4", dados)
