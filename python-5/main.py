import time
from datetime import datetime

records = [
    {'source': '48-996355555', 'destination': '48-666666666',
     'end': 1564610974, 'start': 1564610674},

    {'source': '41-885633788', 'destination': '41-886383097',
     'end': 1564506121, 'start': 1564504821},

    {'source': '48-996383697', 'destination': '41-886383097',
     'end': 1564630198, 'start': 1564629838},

    {'source': '48-999999999', 'destination': '41-885633788',
     'end': 1564697158, 'start': 1564696258},

    {'source': '41-833333333', 'destination': '41-885633788',
     'end': 1564707276, 'start': 1564704317},

    {'source': '41-886383097', 'destination': '48-996384099',
     'end': 1564505621, 'start': 1564504821},

    {'source': '48-999999999', 'destination': '48-996383697',
     'end': 1564505721, 'start': 1564504821},

    {'source': '41-885633788', 'destination': '48-996384099',
     'end': 1564505721, 'start': 1564504821},

    {'source': '48-996355555', 'destination': '48-996383697',
     'end': 1564505821, 'start': 1564504821},

    {'source': '48-999999999', 'destination': '41-886383097',
     'end': 1564610750, 'start': 1564610150},

    {'source': '48-996383697', 'destination': '41-885633788',
     'end': 1564505021, 'start': 1564504821},

    {'source': '48-996383697', 'destination': '41-885633788',
     'end': 1564626000, 'start': 1564647600},

    # valores fake:
    # iniciada antes das 06h00 e finalizada apos as 06h00
    {'source': '48-996383697', 'destination': '41-885633788',
     'end': 1564563780, 'start': 1564563300},

    # iniciada antes das 22h00 e finalizada apos as 22h00
    {'source': '48-996383697', 'destination': '41-885633788',
     'end': 1564621500, 'start': 1564620900}
    # ------------
]


def classify_by_phone_number(records):
    pass


def get_charging_time(records):
    '''
     função :
     1.  obtem o dicionario contendo todos os dados de chamadas
     2.  extrai os dados de inicio e fim da chamada em unix timestamp
     3.  calcula os tempos de cobrança de acordo com a faixa horária
    '''

    encargo_permanente = 0.36
    taxa_por_minuto = 0.09
    charging_list = []

    # obtem o timestamp do horario das 06h00 e das 22h00 para o dia especifico
    billing_limits = get_billing_limits(records[0]['start'])

    # itera entre  os itens do dicionario
    for i, each in enumerate(records):
        start = each['start']
        end = each['end']

        horario_inicio = datetime.fromtimestamp(start).hour
        horario_termino = datetime.fromtimestamp(end).hour

        if horario_inicio < 6 and horario_termino >= 6:
            # chamada iniciada antes das 06h00 e finalizada após as 06h00
            tempo_cobranca = (end - billing_limits[0])/60
            result = encargo_permanente + (tempo_cobranca * taxa_por_minuto)
            result = round(result, 2)
            charging_list.append(result)

        elif horario_inicio < 22 and horario_termino >= 22:
            # chamada iniciada antes das 22h00 e finalizada após as 22h00
            tempo_cobranca = (billing_limits[1] - start)/60
            result = encargo_permanente + (tempo_cobranca * taxa_por_minuto)
            result = round(result, 2)
            charging_list.append(result)

        elif horario_inicio >= 6 and horario_inicio <= 22:
            # chamada ocorrida durante o horário de cobrança
            tempo_cobranca = (end - start)/60
            result = encargo_permanente + (tempo_cobranca * taxa_por_minuto)
            result = round(result, 2)
            charging_list.append(result)

    return charging_list


def get_billing_limits(start_time):
    '''
     retorna a concatenação do horário das 06h00 e das 22h00 com
     o dia específico no formato unix timestamp para entao ser
     computado no cálculo do tempo de cobrança (dentro deste limite)
    '''
    billing_limits = []

    time_string = datetime.fromtimestamp(start_time).strftime('%d%m%Y%H%M%S')

    for i in range(2):
        limit = 6 if i == 0 else 22
        # t = (YYYY, m, dd, HH, MM, S, 0, 0, 0)
        t = (int(time_string[4:8]), int(time_string[2:4]),
             int(time_string[0:2]), limit, 00, 00, 0, 0, 0)
        billing_limits.append(time.mktime(t))

    return tuple(billing_limits)


if __name__ == "__main__":
    # a = get_billing_time(records[0]['start'])
    a = get_charging_time(records)
    print(a)
    print(len(a))
