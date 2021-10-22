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

from charms.reactive import (
    Endpoint,
    clear_flag,
    set_flag,
    when,
    when_any,
)


class BindClientProvides(Endpoint):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @when("endpoint.{endpoint_name}.joined")
    def joined(self):
        set_flag(self.expand_name("{endpoint_name}.connected"))

    @when_any(
        "endpoint.{endpoint_name}.departed",
        "endpoint.{endpoint_name}.broken"
    )
    def departed_or_broken(self):
        self.configure(None, None)
        clear_flag(self.expand_name("{endpoint_name}.connected"))

    def configure(self, ip, port):
        """Configure IP and port to be used in the relation between units.

        :param ip: IP passed to bind exporter to listen
        :type ip: str
        :param port: port to listen
        :type port: str
        """
        for relation in self.relations:
            relation.to_publish_raw['ip'] = ip
            relation.to_publish_raw['port'] = port
