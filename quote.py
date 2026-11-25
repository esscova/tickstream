"""
responsável por atualizar e manter os dados das cotações que o programa recebe
"""
from dataclasses import dataclass, field

@dataclass
class Quote:
    symbol:str
    fields: dict = field(default_factory=dict)
    last_printed_price:float | None = None

    def update(self, values:dict) -> bool:
        self.fields.update(values)

        if 'lp' not in self.fields:
            return False

        current_price = self.fields['lp']
        if self.last_printed_price == current_price:
            return False

        self.last_printed_price = current_price
        return True


if __name__ == '__main__':

    quote = Quote(symbol="BMFBOVESPA:PETR4")
    print(quote.update({"short_name": "PETR4"}))
    print(quote.update({"lp": 32.50, "ch": 0.45}))
    print(quote.update({"bid": 32.49, "ask": 32.51}))
    print(quote.update({"lp": 32.50}))
    print(quote.update({"lp": 32.60}))

    print(quote.fields)