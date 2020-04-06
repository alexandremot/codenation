import time
from datetime import datetime
from operator import itemgetter

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
     'end': 1564626000, 'start': 1564647600}
]

# variáveis globais
encargo_permanente = 0.36
taxa_por_minuto = 0.09
slices = []
totals = []
values = []
source_list = []
lista_com_totais = []


def classify_by_phone_number(records):
    pass


def computa_cobranca(start_time):
    '''
     retorna a concatenação do horário das 06h00 e das 22h00 com
     o dia específico no formato unix timestamp (para calculo dos
     custos)
    '''
    inicio_termino_cobranca = []
    time_string = datetime.fromtimestamp(start_time).strftime('%d%m%Y%H%M%S')

    for i in range(2):
        limit = 6 if i == 0 else 22
        # formato de 't': (year, month, day, hour, min, sec, 0, 0, 0)
        t = (int(time_string[4:8]), int(time_string[2:4]),
             int(time_string[0:2]), limit, 00, 00, 0, 0, 0)
        inicio_termino_cobranca.append(time.mktime(t))
    return tuple(inicio_termino_cobranca)


def calcula_custo_de_ligacao(duracao_ligacao):
    '''
     retorna o custo da ligação, dada a duração em minutos como
     parâmetro de entrada
    '''
    custo_ligacao = encargo_permanente + (duracao_ligacao * taxa_por_minuto)
    custo_ligacao = round(custo_ligacao, 2)
    return custo_ligacao


def calcula_custos_totais(records):
    '''
     função :
     1.  obtem a lista contendo todos os dados de chamadas (records)
     2.  extrai os dados de inicio e fim da chamada em unix timestamp
     3.  calcula os tempos de cobrança de acordo com a faixa horária
    '''
    dict = {'source': '', 'total': ''}
    lista_custos_totais = []

    # obtem o timestamp do horario das 06h00 e das 22h00 para o dia especifico
    inicio_termino_cobranca = computa_cobranca(records[0]['start'])

    # itera entre os itens do dicionario
    for i, dict_item in enumerate(records):
        dict['source'] = dict_item['source']
        inicio = dict_item['start']
        termino = dict_item['end']

        # obtem o dia de início e término da ligação
        dia_inicio = datetime.fromtimestamp(inicio).day
        dia_termino = datetime.fromtimestamp(termino).day

        # considera apenas ligações que iniciam e terminam no mesmo dia
        if dia_inicio != dia_termino:
            pass
        else:
            # obtem os horários de início e de término da ligação
            horario_inicio = datetime.fromtimestamp(inicio).hour
            horario_termino = datetime.fromtimestamp(termino).hour

            if horario_inicio < 6 and horario_termino >= 6:
                # chamada iniciada antes das 06h00 e finalizada após as 06h00
                tempo_cobranca = (termino - inicio_termino_cobranca[0])/60
                custo = calcula_custo_de_ligacao(tempo_cobranca)

            elif horario_inicio < 22 and horario_termino >= 22:
                # chamada iniciada antes das 22h00 e finalizada após as 22h00
                tempo_cobranca = (inicio_termino_cobranca[1] - inicio)/60
                custo = calcula_custo_de_ligacao(tempo_cobranca)

            elif horario_inicio >= 6 and horario_inicio <= 22:
                # chamada ocorrida durante o horário de cobrança
                tempo_cobranca = (termino - inicio)/60
                custo = calcula_custo_de_ligacao(tempo_cobranca)

            else:
                # chamada ocorrida entre 22h01 e 05h59 (sem cobrança por min)
                tempo_cobranca = (termino - inicio)/60
                custo = encargo_permanente

            dict['total'] = custo
            lista_custos_totais.append(dict)
            # reseta o dicionario após operações
            dict = {key: '' for key in dict}
    return lista_custos_totais


def ordena_lista(dict_list):

    lista_ordenada_por_source = sorted(dict_list, key=itemgetter('source'))

    for item in lista_ordenada_por_source:
        source_list.append(item['source'])
        lista_com_totais.append(item['total'])
        sources_agrupados = list(dict.fromkeys(source_list))
    return lista_ordenada_por_source, lista_com_totais, sources_agrupados


def itens_repetidos_index(tuple):
    '''
     monta lista com relação dos itens repetidos
    '''
    records_list = tuple[0]
    source_unicos = tuple[2]

    for each in source_unicos:
        values.append([i for i, x in enumerate(records_list)
                      if records_list[i]['source'] == each])

    return values


def calcula_soma_dos_totais(values, tuple):

    source_unicos = tuple[2]
    records_list = tuple[0]

    for i, each in enumerate(source_unicos):
        totals.append([])
        x = values[i][0] + len(values[i])
        slices.append(records_list[values[i][0]:x])
    values = []

    for i, each in enumerate(slices):
        for any in each:
            totals[i].append(any['total'])

    for each in totals:
        values.append(sum(each))

    return values


def formata_dados(source, totais):
    '''
     gera dicionário a partir dos dados de source e totais
     ordenado do menor para o maior valor total
    '''
    return list(zip(source[2], totais))


if __name__ == "__main__":
    # converte timestamp e calcula custos
    lista_contendo_custos_totais = calcula_custos_totais(records)
    # organiza a lista pelo source
    lista_valores = ordena_lista(lista_contendo_custos_totais)
    # organiza a lista agrupando source repetidos
    index = itens_repetidos_index(lista_valores)
    # soma todos os totais de source agrupados
    index = calcula_soma_dos_totais(index, lista_valores)
    # formata a lista para apresentação final
    result_list = formata_dados(lista_valores, index)
    # imprime o resultado
    print(result_list)
