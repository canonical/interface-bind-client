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


class BindClientRequires(reactive.Endpoint):

    scope = reactive.scopes.GLOBAL

    @reactive.when('endpoint.{endpoint_name}.joined')
    def joined(self):
        reactive.set_flag(self.expand_name('{endpoint_name}.available'))

    def remove(self):
        reactive.clear_flag(self.expand_name('{endpoint_name}.available'))

    @reactive.when('endpoint.{endpoint_name}.broken')
    def broken(self):
        self.remove()

    @reactive.when('endpoint.{endpoint_name}.departed')
    def departed(self):
        self.remove()
