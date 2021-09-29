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

from charms import reactive
import charmhelpers.contrib.network.ip as ch_net_ip


class BindClientProvides(reactive.Endpoint):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ingress_address = ch_net_ip.get_relation_ip(self.endpoint_name)

    def relation_ids(self):
        return [relation.relation_id for relation in self.relations]

    def set_ingress_address(self):
        for relation in self.relations:
            relation.to_publish_raw["ingress-address"] = self.ingress_address
            relation.to_publish_raw["private-address"] = self.ingress_address

    def available(self):
        return reactive.is_flag_set(
            self.expand_name("{endpoint_name}.available")
        )

    @reactive.when("endpoint.{endpoint_name}.joined")
    def joined(self):
        if not self.available():
            reactive.set_flag(self.expand_name("{endpoint_name}.available"))
            self.set_ingress_address()

    def remove(self):
        if self.available():
            reactive.clear_flag(self.expand_name("{endpoint_name}.available"))

    @reactive.when("endpoint.{endpoint_name}.broken")
    def broken(self):
        self.remove()

    @reactive.when("endpoint.{endpoint_name}.departed")
    def departed(self):
        self.remove()
