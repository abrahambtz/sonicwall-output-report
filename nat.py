# 🤖 Abraham Baltazar Garcia Moreno 🐍


import json

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
        read_object(object_list, nat_list)
        object_list = []


def read_object(objects, nat_data):

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
    values_objetcs = []
    objects_data = objects
    objects = objects + address_object + address_group
    
    for object in objects:
        for dict in objects_list:
            if dict['name'] == object:

                for key, value in dict.items():
                    if not key == 'uuid':
                        print(key + ' : ' + str(value))
                        values_objetcs.append({key:value})
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
    #print_pdf(nat_data,objects_data, values_objetcs, service_object, service_group)
    #print(nat_data)
    # print(objects_data)
    #print(values_objetcs)
    #print(service_object)
    #print(service_group)





















    # Queda pendiente obtener los servicios de la lista service_objects_list. 
    # Queda pendiente los servicios de server groups, recordar que server groups es un grupo de
    # de servicios y debemos encontrar los servicios que sean de ese grupo. (Validacion)

    # * Mejora de codigo *
   
def print_pdf(nats, objetcs, values_objetcs, service_object, service_group):
    # ###################################
    # Content
    fileName = 'ReportNAT-SISA.pdf'
    documentTitle = 'Reporte de nats'
    title = 'NAT'
    subTitle = 'The largest carnivorous marsupial'

    textLines = [
    'The Tasmanian devil (Sarcophilus harrisii) is',
    'a carnivorous marsupial of the family',
    'Dasyuridae.'
    ]

    image = 'tasmanianDevil.jpg'


    # ###################################

    # 0) Create document 
    

    pdf = canvas.Canvas(fileName)
    pdf.setTitle(documentTitle)
    count = 0
    c = 0
    object_list = []
    #for i in  
    for values in nats:
        pdf.drawString(100 ,700+ c, str(values))
        c +=20
        
    # for values in nats:
    #     for key, value in values.items():
            
    #         pdf.drawString(100,500+count, key)
    #         pdf.drawString(200,500+count, str(value))
    #         count += 20
    #         if key == 'source' and value != ['any'] or key == 'translated_source' and value != ['Original'] or key == 'destination' and value != ['any'] or key == 'translated_destination' and value != ['any'] or key == 'service' and value != ['any'] or key == 'translated_service' and value != ['Original']:
    #             object_list.append(' '.join(map(str, value)))
        
    #     print('----- Objects and Groups ---------')
    #     #pdf.drawString(700,100, object_list)
    #     object_list = []
    pdf.save()

def run():
    read_nat()


if __name__ == '__main__':
    run()
