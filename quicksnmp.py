from pysnmp import hlapi


def get(target, oids, credentials, port=161, engine=hlapi.SnmpEngine(), context=hlapi.ContextData()):
    handler = hlapi.getCmd(
        engine,
        credentials,
        hlapi.UdpTransportTarget((target, port)),
        context,
        *construct_object_types(oids)
    )
    return fetch(handler, 1)[0]


def construct_object_types(list_of_oids):
    object_types = []
    for oid in list_of_oids:
        object_types.append(hlapi.ObjectType(hlapi.ObjectIdentity(oid)))
    return object_types


def fetch(handler, count):
    result = []
    for i in range(count):
        try:
            error_indication, error_status, error_index, var_binds = next(handler)
            if not error_indication and not error_status:
                items = {}
                for var_bind in var_binds:
                    items[str(var_bind[0])] = cast(var_bind[1])
                result.append(items)
            else:
                raise RuntimeError('Got SNMP error: {0}'.format(error_indication))
        except StopIteration:
            break
    return result


def cast(value):
    try:
        return int(value)
    except (ValueError, TypeError):
        try:
            return float(value)
        except (ValueError, TypeError):
            try:
                return str(value)
            except (ValueError, TypeError):
                pass
    return value


hlapi.CommunityData('public')
ip_dict = get('192.168.198.131', ['1.3.6.1.2.1.6.15.0','1.3.6.1.2.1.6.10.0','1.3.6.1.2.1.6.11.0','1.3.6.1.2.1.6.6.0','1.3.6.1.2.1.6.12.0','1.3.6.1.2.1.6.9.0','1.3.6.1.2.1.6.8.0','1.3.6.1.2.1.6.5.0'], hlapi.CommunityData('public'))
print(ip_dict)

import pandas as pd
test_ip_df = pd.DataFrame(ip_dict.values())
print(test_ip_df)

