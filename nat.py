# 🤖 Abraham Baltazar Garcia Moreno 🐍


import json
from typing import ValuesView
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

    
    
    # lista_nat = nat_list
    

    # nat_data = nat_list
    # objects = object_list
    # nats_list = filter_ipv4('kondinero/json/nat.json')
    # objects_list = filter_ipv4('kondinero/json/object.json')
    # groups_list = filter_ipv4('kondinero/json/groups.json')

    # service_groups_list = open_service('kondinero/json/service-groups.json')
    # service_objects_list = filter_ipv4('kondinero/json/service-object.json')

    # service_object = []
    # service_group = []

    # address_object = []
    # address_group = []
    # for object in objects:
    #     for dict in groups_list:
    #         if dict['name'] == object:
    #             for key, value in dict.items():
    #                 if key == 'address_object':
    #                     address_object = [x['name'] for x in value['ipv4']]
    #                     print('Grups:')
    #                     print(address_object, end='\n\n')
    #                 elif key == 'address_group':
    #                     address_group = [x['name'] for x in value['ipv4']]
    #                     print('Grups:')
    #                     print(address_group, end='\n\n')
    # values_objetcs = []
    # objects_data = objects
    # objects = objects + address_object + address_group
    
    # for object in objects:
    #     for dict in objects_list:
    #         if dict['name'] == object:

    #             for key, value in dict.items():
    #                 if not key == 'uuid':
    #                     print(key + ' : ' + str(value))
    #                     values_objetcs.append({key:value})
    #             print()
    # # print('hola')
    # # print(service_groups_list)
    # for object in objects:
    #     for dict in service_groups_list:
    #         for key, value in dict.items():
    #             if dict['name'] == object:
    #                 if key == 'service_object':
    #                     service_object = [x['name'] for x in value]
    #                     print('------- Service Object --------')
    #                     for i in service_object:
    #                         print(i)
    #                 elif key == 'service_group':
    #                     service_group = [x['name'] for x in value]
    #                     print(' ------ Service Groups --------')
    #                     for i in service_group:
    #                         print(i)
    # print(end='\n\n')
    # #print_pdf(nat_data,objects_data, values_objetcs, service_object, service_group)
    # #print(nat_data)
    # # print(objects_data) # List
    # # print(values_objetcs) # ListDict
    # # print(service_object) # List    
    # # print(service_group) # List
    
    # return(nat_data)


    # Queda pendiente obtener los servicios de la lista service_objects_list. 
    # Queda pendiente los servicios de server groups, recordar que server groups es un grupo de
    # de servicios y debemos encontrar los servicios que sean de ese grupo. (Validacion)

    # * Mejora de codigo *


def run():
    rute = 'kondinero/json/nat.json'
    nats = get_nats(rute)
    objects = get_objetcs_nat(nats)
    # for value in objects:
    #     print( ' : ' + str(value))

    nats = json_normalize(nats) 
    objects = json_normalize(objects)
    with pandas.ExcelWriter('output.xlsx') as report: 
        nats.to_excel(report, sheet_name='NAT')
        objects.to_excel(report, sheet_name='OBJECTS AND GROUPS')
    

if __name__ == '__main__':
    run()
