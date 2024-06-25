from pm4py import PetriNet, Marking
from pm4py.algo.conformance.unfolding.unfold import UnfoldingAlgorithm
from pm4py.algo.conformance.unfolding.unfold_improved import UnfoldingAlgorithmImproved
from pm4py.objects.petri_net.utils.align_utils import SKIP, construct_standard_cost_function


def unfold_sync_net(sync_net: PetriNet, initial_marking: Marking, final_marking: Marking, cost_function: dict = None,
                    improved: bool = True):

    if cost_function is None:
        cost_function = construct_standard_cost_function(sync_net, SKIP)

    if not improved:
        algo = UnfoldingAlgorithm(sync_net, initial_marking, final_marking, cost_function)
    else:
        algo = UnfoldingAlgorithmImproved(True, sync_net, initial_marking, final_marking, cost_function)

    return algo.search()
