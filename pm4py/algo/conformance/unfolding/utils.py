from typing import Set
from pm4py import Marking, PetriNet
from pm4py.algo.conformance.unfolding.obj.branching_process import BranchingProcess
from pm4py.objects.petri_net.utils.petri_utils import add_arc_from_to


def add_final_state(net: PetriNet, fm: Marking, cost_function: dict[PetriNet.Transition, int]):
    """
    Adds a final transition `tr` extending from the final marking of the given net and a final place `pr` following `tr`.
    cost of the final transition is set to 0.
    Args:
        net (): petri net to be extended
        fm (): final marking of the given net
        cost_function (): cost function to be updated

    Returns:
        void
    """

    # print(f'adding final state from {fm.keys()} to tr')

    final_places: Set[PetriNet.Place] = set(fm.keys())

    tr = PetriNet.Transition(preset=final_places, name='tr', label='tr')
    tp = PetriNet.Place(preset={tr}, name='pr', label='pr')

    for fp in final_places:
        add_arc_from_to(fp, tr, net)

    add_arc_from_to(tr, tp, net)

    net.places.add(tp)
    net.transitions.add(tr)

    cost_function.update({tr: 0})

    return tr, tp

class UnfoldingAlignment:
    def __init__(self, final_events: Set[BranchingProcess.OccurrenceNet.Event]=None, lowest_cost: int=None):
        self.final_events = set() if final_events is None else final_events
        self.lowest_cost = lowest_cost

class UnfoldingAlignmentResult:
    def __init__(self, alignment: UnfoldingAlignment, num_cutoffs,
                 generated_prefix: BranchingProcess.OccurrenceNet = None,
                 total_duration: float = 0):
        self.final_events = alignment.final_events
        self.alignment_costs = alignment.lowest_cost
        self.num_cutoffs = num_cutoffs
        self.total_duration = total_duration
        self.generated_prefix = generated_prefix
        self.final_event_name = list(map(lambda x: x.name, alignment.final_events))
