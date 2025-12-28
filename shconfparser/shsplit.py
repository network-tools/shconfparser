"""Show command splitter module.

This module provides the ShowSplit class for splitting combined show command
outputs into individual commands.
"""

import logging
import re
from collections import OrderedDict
from typing import List, Optional, Union


class ShowSplit:
    """Splitter for network device show command outputs.

    This class intelligently splits combined show command outputs into
    separate commands based on command patterns.

    Attributes:
        shcmd_dict: OrderedDict mapping command names to their output lines
        key_dictionary: Command pattern to name mapping
    """

    def __init__(self) -> None:
        """Initialize the ShowSplit with command patterns."""
        self.shcmd_dict: OrderedDict[str, List[str]] = OrderedDict()
        self.key_dictionary: OrderedDict[str, Union[str, OrderedDict]] = OrderedDict(
            [
                (" cdp ", OrderedDict([("det", "cdp_neighbors_detail"), ("nei", "cdp_neighbors")])),
                (
                    " ip ",
                    OrderedDict(
                        [
                            ("int", "ip_interface_brief"),
                            ("route", "ip_route"),
                            ("arp", "ip_arp"),
                            ("pro", "ip_protocols"),
                        ]
                    ),
                ),
                (
                    " int",
                    OrderedDict(
                        [
                            ("sum", "interface_summary"),
                            ("des", "interface_description"),
                            ("stat", "interface_status"),
                            ("tran", "interfaces_transceiver_properties"),
                            ("cap", "interfaces_capabilities"),
                            ("vlan-interface brief", "interfaces_vlan_brief"),
                            ("brief", "interfaces_brief"),
                            ("int", "interfaces"),
                        ]
                    ),
                ),
                (
                    " switch",
                    OrderedDict(
                        [
                            ("detail", "switch_detail"),
                            ("service", "switch_service_modules"),
                            ("switch", "switch"),
                        ]
                    ),
                ),
                (" stack all", "stack_all"),
                (" run", "running"),
                (" ver", "version"),
                (" lic", "license"),
                (" inv", "inventory"),
                (
                    " vlan",
                    OrderedDict([("port all detail", "vlan_port_all_detail"), ("vlan", "vlan")]),
                ),
                (" module", "module"),
                (" mac add", "mac_address_table"),
                (" power inline", "power_inline"),
                (" flash", "flash"),
                (" port trunk", "port_trunk"),
                (" current-conf", "current_config"),
                (" stp root", "stp_root"),
                (" device", "device"),
                (" ssh server status", "ssh_server_status"),
                (" lldp", OrderedDict([("neighbor-information list", "lldp_neighbor_list")])),
                (" dir", OrderedDict([("/all", "dir_all")])),
                (" etherc", OrderedDict([("su", "etherchannel_summary")])),
            ]
        )

    def _find_command(
        self, result: re.Match[str], key_dict: OrderedDict[str, Union[str, OrderedDict]]
    ) -> Optional[str]:
        """Recursively find command name from matched pattern.

        Args:
            result: Regex match object containing the command line
            key_dict: Dictionary of command patterns and names

        Returns:
            Command name if found, None otherwise
        """
        for key, value in key_dict.items():
            if key in result.group(0):
                if isinstance(value, OrderedDict):
                    return self._find_command(result, value)
                return value
        logging.error(f"No key found for: {result.group(0)}")
        return None

    def split(
        self, lines: Optional[List[str]], pattern: Optional[str] = None
    ) -> Optional[OrderedDict[str, List[str]]]:
        """Split combined show command output into separate commands.

        Args:
            lines: List of output lines from show commands
            pattern: Regex pattern to identify command lines (default: r'.*#sh.*')

        Returns:
            OrderedDict mapping command names to their output lines,
            or None if lines is None

        Example:
            >>> splitter = ShowSplit()
            >>> lines = ['switch#show version', 'Cisco IOS...']
            >>> result = splitter.split(lines)
            >>> result['version']
            ['switch#show version', 'Cisco IOS...']
        """
        key: Optional[str] = None
        pattern = r".*#sh.*" if pattern is None else pattern

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
                    logging.error(f"Debug: {line_lower}")

            if key is not None:
                self.shcmd_dict[key].append(line.rstrip())

        return self.shcmd_dict
