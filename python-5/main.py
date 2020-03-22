from datetime import datetime

records = [
    {'source': '48-996355555', 'destination': '48-666666666', 'end': 1564610974, 'start': 1564610674},
    {'source': '41-885633788', 'destination': '41-886383097', 'end': 1564506121, 'start': 1564504821},
    {'source': '48-996383697', 'destination': '41-886383097', 'end': 1564630198, 'start': 1564629838},
    {'source': '48-999999999', 'destination': '41-885633788', 'end': 1564697158, 'start': 1564696258},
    {'source': '41-833333333', 'destination': '41-885633788', 'end': 1564707276, 'start': 1564704317},
    {'source': '41-886383097', 'destination': '48-996384099', 'end': 1564505621, 'start': 1564504821},
    {'source': '48-999999999', 'destination': '48-996383697', 'end': 1564505721, 'start': 1564504821},
    {'source': '41-885633788', 'destination': '48-996384099', 'end': 1564505721, 'start': 1564504821},
    {'source': '48-996355555', 'destination': '48-996383697', 'end': 1564505821, 'start': 1564504821},
    {'source': '48-999999999', 'destination': '41-886383097', 'end': 1564610750, 'start': 1564610150},
    {'source': '48-996383697', 'destination': '41-885633788', 'end': 1564505021, 'start': 1564504821},
    {'source': '48-996383697', 'destination': '41-885633788', 'end': 1564626000, 'start': 1564647600}
]


def classify_by_phone_number(records):
    pass


def retorna_valores(records):
    lista_de_valores = []
    encargo_permanente = 0.36
    taxa_por_minuto = 0.09

    for i, each in enumerate(records):
        start = each['start']
        end = each['end']

        tempo_decorrido = end - start
        horario_inicio = datetime.fromtimestamp(start).hour
        horario_fim = datetime.fromtimestamp(end).hour

        if horario_inicio >= 6 and horario_inicio <= 22:
            lista_de_valores.append(encargo_permanente +
                                    taxa_por_minuto * tempo_decorrido)
        else:
            lista_de_valores.append(encargo_permanente)
    return lista_de_valores


if __name__ == "__main__":
    a = retorna_valores(records)
    print(a)
