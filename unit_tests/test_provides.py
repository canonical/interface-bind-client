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

import charms_openstack.test_utils as test_utils
import mock
import provides


class TestRegisteredHooks(test_utils.TestRegisteredHooks):

    def test_hooks(self):
        defaults = []
        hook_set = {
            "when": {
                "joined": ("endpoint.{endpoint_name}.joined",),
            },
            "when_any": {
                "departed_or_broken": (
                    "endpoint.{endpoint_name}.departed",
                    "endpoint.{endpoint_name}.broken",
                ),
            }
        }
        # test that the hooks were registered
        self.registered_hooks_test_helper(provides, hook_set, defaults)


class TestBindClientProvides(test_utils.PatchHelper):

    def setUp(self):
        super().setUp()
        self._patches = {}
        self._patches_start = {}
        self.patch_object(provides, "clear_flag")
        self.patch_object(provides, "set_flag")

        self.fake_unit = mock.MagicMock()
        self.fake_unit.unit_name = "designate-bind/0"

        self.fake_relation_id = "bind-client:3"
        self.fake_relation = mock.MagicMock()
        self.fake_relation.relation_id = self.fake_relation_id
        self.fake_relation.units = [self.fake_unit]

        self.ep_name = "bind-client"
        self.ep = provides.BindClientProvides(
            self.ep_name, [self.fake_relation_id])
        self.ep.relations[0] = self.fake_relation

    def tearDown(self):
        self.ep = None
        for k, v in self._patches.items():
            v.stop()
            setattr(self, k, None)
        self._patches = None
        self._patches_start = None

    def test_joined(self):
        self.ep.joined()
        self.set_flag.assert_called_once_with(
            "{}.connected".format(self.ep_name)
        )

    def test_departed_or_broken(self):
        self.ep.departed_or_broken()
        _calls = [
            mock.call("ip", None),
            mock.call("port", None),
        ]
        self.clear_flag.assert_called_once_with(
            "{}.connected".format(self.ep_name)
        )
        self.fake_relation.to_publish_raw.__setitem__.assert_has_calls(_calls)

    def test_configure(self):
        self.ep.configure('10.152.183.98', '1234')
        _calls = [
            mock.call("ip", '10.152.183.98'),
            mock.call("port", '1234'),
        ]
        self.fake_relation.to_publish_raw.__setitem__.assert_has_calls(_calls)
