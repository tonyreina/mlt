#
# -*- coding: utf-8 -*-
#
# Copyright (c) 2018 Intel Corporation
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# SPDX-License-Identifier: EPL-2.0
#


import sys
from subprocess import Popen, PIPE
from termcolor import colored

from mlt.commands import Command
from mlt.utils import (config_helpers, localhost_helpers)
from mlt.utils.constants import (SYNC, SYNC_GET_APIS, SYNC_SET_APIS)


class SyncCommand(Command):
    def __init__(self, args):
        super(SyncCommand, self).__init__(args)
        if not localhost_helpers.check_local_install(SYNC):
            error_msg = "{} is not installed locally!".format(SYNC)
            print(colored(error_msg.decode("utf-8"), 'red'))
            sys.exit(1)

        self.config = config_helpers.load_config()

    def action(self):
        """Inspect and sync files from remote containers
           create      Create a new spec
           delete      Delete an existing spec
           doctor      Troubleshoot and verify your setup is correct.
           get         Get all specs.
           update      Update sync to the latest version.
           version     View the versions of both the local binary and remote
                       service.
           watch       Watch configured specs and start syncing files when
                       required.
        """
        for key, value in {k: self.args[k] for k in SYNC_GET_APIS}.items():
            if value:
                self._sync_get([key])
                return
        for key, value in {k: self.args[k] for k in SYNC_SET_APIS}.items():
            if value:
                if key == "watch":
                    self._sync_get([key, "-d"])
                elif key == "delete" and self.args['--sync-spec']:
                    self._sync_get([key, self.args['--sync-spec']])
                elif key == "create":
                    self._sync_set([])
                return

    def _sync_get(self, subcommand):
        # TODO: We need to make this call asyncronous,
        # I've done this in the past
        p = Popen(([SYNC] + subcommand), stdin=PIPE, stdout=PIPE,
                  stderr=PIPE)
        output, err = p.communicate()
        print(output.decode("utf-8"))
        if not p.returncode:
            print(colored(err.decode("utf-8"), 'red'))

    def _sync_set(self, subcommand):
        print("Not Implemented Yet!")