# Copyright 2021 Canonical Ltd
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#  http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# NOTE(gabrielcocenza): The files provides.py and requires.py
# are basically using the same code for the handlers. Currently,
# the reactive framework is not able to recognise handlers from
# a parent class that child classes could inherit.

from charms import reactive


class BindClientRequires(reactive.Endpoint):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @reactive.when('endpoint.{endpoint_name}.joined')
    def joined(self):
        reactive.set_flag(self.expand_name('{endpoint_name}.connected'))

    @reactive.when("endpoint.{endpoint_name}.departed")
    def departed(self):
        reactive.clear_flag(self.expand_name("{endpoint_name}.connected"))

    @reactive.when("endpoint.{endpoint_name}.broken")
    def broken(self):
        reactive.clear_flag(self.expand_name("{endpoint_name}.connected"))

    def get_config(self):
        """
        Returns a dict containing the ip and ports for the stats channel
        for each unit in the relation. The default value for port is 8053
        and IP is 127.0.0.1 .

        The return value is a dict of the following form::
            {
                'unit_name': {
                    'stats-port': port_of_designate_bind_unit,
                    'stats-ip': ip_of_designate_bind_unit
                },
                # ...
            }
        """
        configs = {}
        for relation in self.relations:
            for unit in relation.joined_units:
                unit_name = unit.unit_name
                configs.setdefault(
                    unit_name, {"stats-port": "8053", "stats-ip": "127.0.0.1"}
                )
                data = unit.received_raw
                port = data.get('stats-port')
                ip = data.get('stats-ip')
                if port and ip:
                    configs[unit_name] = {'stats-port': port, 'stats-ip': ip}

        return configs
