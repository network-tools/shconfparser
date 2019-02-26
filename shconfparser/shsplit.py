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
                ('vlan-interface brief', 'interfaces_vlan_brief'),
                ('brief', 'interfaces_brief'),
                ('int', 'interfaces'),
            ])
             ),
            (' switch', OrderedDict([
                ('detail', 'switch_detail'),
                ('service', 'switch_service_modules'),
                ('switch', 'switch')
            ])
             ),
            (' stack all', 'stack_all'),
            (' run', 'running'),
            (' ver', 'version'),
            (' lic', 'license'),
            (' inv', 'inventory'),
            (' vlan', OrderedDict([
                ('port all detail', 'vlan_port_all_detail'),
                ('vlan', 'vlan')
            ])),
            (' module', 'module'),
            (' mac add', 'mac_address_table'),
            (' power inline', 'power_inline'),
            (' flash', 'flash'),
            (' port trunk', 'port_trunk'),
            (' current-conf', 'current_config'),
            (' stp root', 'stp_root'),
            (' device', 'device'),
            (' ssh server status', 'ssh_server_status'),
            (' lldp', OrderedDict([
                ('neighbor-information list', 'lldp_neighbor_list')
            ])),
            (' dir', OrderedDict([
                ('/all', 'dir_all')
            ])),
            (' etherc', OrderedDict([
                ('su', 'etherchannel_summary')
            ]))
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
            line_lower = str(line).lower()
            result = re.search(pattern, line_lower)
            if result:
                key = self._find_command(result, self.key_dictionary)
                if key is not None:
                    self.shcmd_dict[key] = []
                else:
                    logging.error('Debug: {}'.format(line_lower))

            if key is not None:
                self.shcmd_dict[key].append(line.rstrip())
        return self.shcmd_dict
