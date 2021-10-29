# 🤖 Abraham Baltazar Garcia Moreno 🐍
import json
import pandas

from pandas.io.json import json_normalize

def source(nat):
    if [x for i, x in nat['source'].items()] == True:
        return 'any'
    return [x for i, x in nat['source'].items()]


def filter_ipv4(rute):
    list = []
    with open(rute, 'r', encoding='utf-8') as data_json:
        data = json.load(data_json)

        for values in data:
            for key, value in values.items():
                if key == 'ipv4':
                    list.append(value)
    return list

def filter_data_nat(nat_list):
    nats = []
    nats_listdict = [
        {
            'name': nat['name'],
            'source':['any' if x == True else x for i, x in nat['source'].items()],            
            'translated_source':['Original' if x == True else x for i, x in nat['translated_source'].items()],           
            'destination':['any' if x == True else x for i, x in nat['destination'].items()],           
            'translated_destination':['any' if x == True else x for i, x in nat['translated_destination'].items()],
            'service':['any' if x == True else x for i, x in nat['service'].items()],           
            'translated_service':['Original' if x == True else x for i, x in nat['translated_service'].items()],
            'inbound':nat['inbound'],
            'outbound':nat['outbound'],
            'enable':nat['enable'],
            'comment':nat['comment']
        }
        for nat in nat_list if not 'SSO agent' in nat['comment'] if not 'NAT Policy' in nat['comment'] if not 'Auto-added' in nat['comment']]
    
    for nat in nats_listdict:
        nat_dict = {}
        for key, value in nat.items():
            if key == 'source' or key == 'translated_source' or key == 'destination' or key == 'translated_destination' or key == 'service' or key == 'translated_service' :
                value = ' '.join(map(str, value))
            nat_dict.update({key:value})
        nats.append(nat_dict)
    return nats

def get_objetcs_nat(nat_listdict):
    
    objects_listdict = []
    for nat_dict in nat_listdict:
        
        objects = []
        for key, value in nat_dict.items():
            
            if key == 'source' and str(value) != 'any' or key == 'translated_source' and str(value) != 'Original' or key == 'destination' and str(value) != 'any' or key == 'translated_destination' and str(value) != 'any' or key == 'translated_service' and str(value) != 'Original':
                objects.append(value)
        objects = ', '.join(map(str, objects))
        objects_listdict.append({'Objects':objects})  
    return objects_listdict





def open_service(rute):
    list = []
    with open(rute, 'r', encoding='utf-8') as data_json:
        data = json.load(data_json)

    return data


def get_nats(rute):
    nat_listdict = filter_ipv4(rute) # Retorna una lista de diccionarios
    nat_listdict = filter_data_nat(nat_listdict)
    return nat_listdict

def run():
    custumer = 'sisa'
    rute = custumer+'/json/nat.json'
    nats = get_nats(rute)
    objects = get_objetcs_nat(nats)
    # for value in objects:
    #     print( ' : ' + str(value))

    nats = json_normalize(nats) 
    objects = json_normalize(objects)
    with pandas.ExcelWriter(custumer +'/output.xlsx') as report: 
        nats.to_excel(report, sheet_name='NAT')
        objects.to_excel(report, sheet_name='OBJECTS AND GROUPS')
    

if __name__ == '__main__':
    run()
