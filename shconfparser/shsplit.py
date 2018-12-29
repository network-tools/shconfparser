import re, logging
from collections import OrderedDict


class ShowSplit:
    def __init__(self):
        self.shcmd_dict = OrderedDict()
        self.key_dictionary = OrderedDict([
            (' cdp ', OrderedDict([
                    ('det', 'cdp_neighbors_detail'),
                    ('nei', 'cdp_neighbors')
                    ])
             ),
            (' ip ', OrderedDict([
                ('int', 'ip_interface_brief'),
                ('route', 'ip_route'),
                ('arp', 'ip_arp'),
                ('pro', 'ip_protocols'),
                ])
             ),
            (' int', OrderedDict([
                ('sum', 'interface_summary'),
                ('des', 'interface_description'),
                ('stat', 'interface_status'),
                ('tran', 'interfaces_transceiver_properties'),
                ('cap', 'interfaces_capabilities'),
                ('int', 'interfaces'),
                ])
             ),
            (' switch', OrderedDict([
                ('detail', 'switch_detail'),
                ('service', 'switch_service_modules'),
                ('switch', 'switch')
                ])
             ),
            (' run', 'running'),
            (' ver', 'version'),
            (' inv', 'inventory'),
            (' vlan', 'vlan'),
            (' module', 'module'),
            (' mac add', 'mac_address_table'),
            (' power inline', 'power_inline'),
            (' flash', 'flash'),
        ])

    def _find_command(self, result, key_dict):
        for key, value in key_dict.items():
            if key in result.group(0):
                return self._find_command(result, value) if type(value) == OrderedDict else value
        logging.error('No key found for: {}'.format(result.group(0)))

    def split(self, lines, pattern=None):
        key = None
        pattern = r'.*#sh.*' if pattern is None else pattern
        if lines is None:
            return None

        for line in lines:
            result = re.search(pattern, line)
            if result:
                key = self._find_command(result, self.key_dictionary)
                if key is not None:
                    self.shcmd_dict[key] = []
                else:
                    logging.error('Debug: {}'.format(line))

            if key is not None:
                self.shcmd_dict[key].append(line)
        return self.shcmd_dict
