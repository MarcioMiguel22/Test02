from Guia_de_transporte.models import GuiaDeTransporte

# Array de dicionários com os dados para inserir
dados = [
    {
        "item": "Logística",
        "descricao": "13/12/2022 Pág. 1",
        "unidade": "UN",
        "quantidade": 0,
        "peso": 0,
        "volume": 0
    },
    {
        "item": "0101032",
        "descricao": "0101033 0101034 0101035",
        "unidade": "UN",
        "quantidade": 0,
        "peso": 0,
        "volume": 0
    },
    {
        "item": "AGRAFES",
        "descricao": "A-20 SIMES REDE ELETROSOLDADA ARAME ZINCADO N12 2,7 ESTICADOR RAMADA ZIN-",
        "unidade": "UN",
        "quantidade": 0,
        "peso": 0,
        "volume": 0
    }
]

# Iterar sobre o array e criar instâncias do modelo
for dado in dados:
    GuiaDeTransporte.objects.create(
        item=dado["item"],
        descricao=dado["descricao"],
        unidade=dado["unidade"],
        quantidade=dado["quantidade"],
        peso=dado["peso"],
        volume=dado["volume"]
    )

print("Dados inseridos com sucesso!")