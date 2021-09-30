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


class BindClientProvides(reactive.Endpoint):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @reactive.when("endpoint.{endpoint_name}.joined")
    def joined(self):
        reactive.set_flag(self.expand_name("{endpoint_name}.connected"))

    # NOTE(gabrielcocenza): The framework doesn't pass arguments to the
    # handler using the decorator @when_any. That is why the methods
    # departed and broken are repetitive.
    @reactive.when("endpoint.{endpoint_name}.departed")
    def departed(self):
        reactive.clear_flag(self.expand_name("{endpoint_name}.connected"))

    @reactive.when("endpoint.{endpoint_name}.broken")
    def broken(self):
        reactive.clear_flag(self.expand_name("{endpoint_name}.connected"))

    def configure(self, port):
        """Configure the port to be used in the relation between units

        :param port: port to listen
        :type port: str
        """
        for relation in self.relations:
            relation.to_publish_raw['port'] = port
