# tickstream

Monitor de cotações em tempo real da B3 (Bovespa) usando o WebSocket do TradingView. O script assina uma lista de ativos e imprime no terminal preço, variação, bid, ask e volume de cada um, sempre que o preço muda.

## Funcionalidades

- Conexão direta ao WebSocket de cotações do TradingView, sem chave de API
- Inscrição em vários ativos da B3 ao mesmo tempo
- Resposta automática aos heartbeats do protocolo
- Exibição apenas quando o preço muda, para evitar linhas repetidas
- Aviso quando nenhuma mensagem chega dentro do tempo limite
- Relatório periódico com a quantidade de mensagens recebidas

## Requisitos

- Python 3.10 ou superior
- Conexão com a internet

## Instalação

```bash
git clone https://github.com/esscova/tickstream.git
cd tickstream
python -m venv .venv
source .venv/bin/activate    # Windows: .venv\Scripts\activate
pip install websockets
```

## Uso

```bash
python main.py
```

Saída de exemplo:

```text
Conectando...
Conectado!

Inscrevendo 13 ativos...

=== MONITORANDO COTAÇÕES ===

[13:12:04] VIVT3  | Preço: R$ 54.20 | Var.: +0.35 (+0.65%) | Bid: 54.19 | Ask: 54.21 | Volume: 1,234,567
```

Para encerrar, pressione `Ctrl+C`.

## Configuração

As principais configurações ficam no topo de `main.py`:

| Constante | Descrição | Padrão |
|---|---|---|
| `TICKERS` | Lista de ativos no formato `BMFBOVESPA:CODIGO` | 13 ações da B3 |
| `RECV_TIMEOUT` | Segundos sem mensagem antes de avisar | `5` |
| `STATUS_INTERVAL` | Segundos entre os relatórios de status | `10` |

Para acompanhar outro ativo, adicione o código à lista no formato `BMFBOVESPA:CODIGO`, por exemplo `"BMFBOVESPA:PETR4"`.

## Como funciona

1. Abre a conexão WebSocket com o TradingView, usando o cabeçalho de origem do widget público.
2. Cria uma sessão de cotações e pede os campos desejados (preço, variação, bid, ask, volume etc.).
3. Inscreve cada ativo da lista.
4. Recebe as mensagens, separa o protocolo (`~m~tamanho~m~conteúdo`) e atualiza o estado de cada ativo.

## Avisos

- Este projeto usa um endpoint não documentado do TradingView, pensado para o widget público. Ele pode mudar ou deixar de funcionar sem aviso.
- Os dados podem ter atraso e não são indicados para decisões de investimento. Use-os apenas como referência.
- O script não faz negociação, só exibe cotações.

## Estrutura

```text
tickstream/
└── main.py
```

