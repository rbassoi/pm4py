'''
    PM4Py – A Process Mining Library for Python
Copyright (C) 2024 Process Intelligence Solutions UG (haftungsbeschränkt)

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as
published by the Free Software Foundation, either version 3 of the
License, or any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see this software project's root or
visit <https://www.gnu.org/licenses/>.

Website: https://processintelligence.solutions
Contact: info@processintelligence.solutions
'''
# list of properties that can be associated to a Petri net or its entities


# distinguish Petri nets that are synchronous product nets
IS_SYNC_NET = "is_sync_net"
TRACE_NET_TRANS_INDEX = "trace_net_trans_index"
TRACE_NET_PLACE_INDEX = "trace_net_place_index"

ARCTYPE = "arctype"
INHIBITOR_ARC = "inhibitor"
RESET_ARC = "reset"
STOCHASTIC_ARC = "stochastic_arc"
TRANSPORT_ARC = "transport"

AGE_GUARD = "ageguard"  # or TIME_GUARD we only consider inclusive [ ] intervals
AGE_MIN = "agemin"  # we only consider inclusive [ ] intervals
AGE_MAX = "agemax"  # we only consider inclusive [ ] intervals
AGE_INVARIANT = "ageinvariant"
TRANSPORT_INDEX = "transportindex"

TRANS_GUARD = "guard"
WRITE_VARIABLE = "writeVariable"
READ_VARIABLE = "readVariable"
VARIABLES = "variables"
