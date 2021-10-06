import json
from typing import Dict


def source(nat):
    if [x for i, x in nat['source'].items()] == True:
        return 'any'
    return [x for i, x in nat['source'].items()]


def open_file(rute):
    list = []
    with open(rute, 'r', encoding='utf-8') as data_json:
        data = json.load(data_json)

        for values in data:
            for key, value in values.items():
                if key == 'ipv4':
                    list.append(value)
    return list


def open_service(rute):
    list = []
    with open(rute, 'r', encoding='utf-8') as data_json:
        data = json.load(data_json)

    return data


def read_nat():

    rute = 'kondinero/json/nat.json'
    nat_list = open_file(rute)
    nat_list_g = [
        {
            'source_': nat['source'],
            'translated_source_':nat['translated_source'],
            'destination_':nat['destination'],
            'translated_destination_':nat['translated_destination'],
            'service_':nat['service'],
            'translated_service_':nat['translated_service']

        }
        for nat in nat_list if not 'SSO agent' in nat['comment'] if not 'NAT Policy' in nat['comment'] if not 'Auto-added' in nat['comment']]
    # if nat['comment']=='Auto-added X0:V100 outbound NAT Policy for X1 WAN'

    nat_list = [
        {
            'name': nat['name'],
            # 'source_':nat['source'],
            'source':['any' if x == True else x for i, x in nat['source'].items()],
            # 'translated_source_':nat['translated_source'],
            'translated_source':['Original' if x == True else x for i, x in nat['translated_source'].items()],
            # 'destination_':nat['destination'],
            'destination':['any' if x == True else x for i, x in nat['destination'].items()],
            # 'translated_destination_':nat['translated_destination'],
            'translated_destination':['any' if x == True else x for i, x in nat['translated_destination'].items()],
            # 'service_':nat['service'],
            'service':['any' if x == True else x for i, x in nat['service'].items()],
            # 'translated_service_':nat['translated_service'],
            'translated_service':['Original' if x == True else x for i, x in nat['translated_service'].items()],
            'inbound':nat['inbound'],
            'outbound':nat['outbound'],
            'enable':nat['enable'],
            'comment':nat['comment']
        }
        for nat in nat_list if not 'SSO agent' in nat['comment'] if not 'NAT Policy' in nat['comment'] if not 'Auto-added' in nat['comment']]
    # if nat['comment']=='Auto-added X0:V100 outbound NAT Policy for X1 WAN'

    object_list = []
    for values in nat_list:
        print('----- NAT ---------')

        for key, value in values.items():
            print(" " + key + " : " + str(value))
            if key == 'source' and value != ['any'] or key == 'translated_source' and value != ['Original'] or key == 'destination' and value != ['any'] or key == 'translated_destination' and value != ['any'] or key == 'service' and value != ['any'] or key == 'translated_service' and value != ['Original']:
                object_list.append(' '.join(map(str, value)))
        print('----- Objects and Groups ---------')
        print(object_list, end='\n\n')
        read_object(object_list)
        object_list = []


def read_object(objects):

    nats_list = open_file('kondinero/json/nat.json')
    objects_list = open_file('kondinero/json/object.json')
    groups_list = open_file('kondinero/json/groups.json')

    service_groups_list = open_service('kondinero/json/service-groups.json')
    service_objects_list = open_file('kondinero/json/service-object.json')

    service_object = []
    service_group = []

    address_object = []
    address_group = []
    for object in objects:
        for dict in groups_list:
            if dict['name'] == object:
                for key, value in dict.items():
                    if key == 'address_object':
                        address_object = [x['name'] for x in value['ipv4']]
                        print('Grups:')
                        print(address_object, end='\n\n')
                    elif key == 'address_group':
                        address_group = [x['name'] for x in value['ipv4']]
                        print('Grups:')
                        print(address_group, end='\n\n')

    objects = objects + address_object + address_group
    for object in objects:
        for dict in objects_list:
            if dict['name'] == object:

                for key, value in dict.items():
                    if not key == 'uuid':
                        print(key + ' : ' + str(value))
                print()
    # print('hola')
    # print(service_groups_list)
    for object in objects:
        for dict in service_groups_list:
            for key, value in dict.items():
                if dict['name'] == object:
                    if key == 'service_object':
                        service_object = [x['name'] for x in value]
                        print('------- Service Object --------')
                        for i in service_object:
                            print(i)
                    elif key == 'service_group':
                        service_group = [x['name'] for x in value]
                        print(' ------ Service Groups --------')
                        for i in service_group:
                            print(i)
    print(end='\n\n')
   


def run():
    read_nat()


if __name__ == '__main__':
    run()
