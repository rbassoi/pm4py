from pm4py.algo.conformance.alignments.process_tree.variants.approximated import matrix_lp as approximated_matrix_lp
from pm4py.algo.conformance.alignments.process_tree.variants.approximated import original as approximated_original
from pm4py.algo.conformance.alignments.process_tree.variants import search_graph_pt

from pm4py.util import exec_utils
from enum import Enum

from typing import Optional, Dict, Any, Union, Tuple
from pm4py.objects.process_tree.obj import ProcessTree
from pm4py.objects.log.obj import EventLog, Trace
from pm4py.util import typing
from pm4py.objects.conversion.log import converter as log_converter
import pandas as pd


class Variants(Enum):
    APPROXIMATED_ORIGINAL = approximated_original
    APPROXIMATED_MATRIX_LP = approximated_matrix_lp
    SEARCH_GRAPH_PT = search_graph_pt


DEFAULT_VARIANT = Variants.SEARCH_GRAPH_PT


def apply(obj: Union[EventLog, Trace, pd.DataFrame], pt: ProcessTree, variant=DEFAULT_VARIANT, parameters: Optional[Dict[Any, Any]] = None) -> Union[typing.AlignmentResult, typing.ListAlignments]:
    """
    Align an event log or a trace with a process tree

    Parameters
    --------------
    obj
        Log / Trace
    pt
        Process tree
    variant
        Variant
    parameters
        Variant-specific parameters

    Returns
    --------------
    alignments
        Alignments
    """
    if parameters is None:
        parameters = {}

    return exec_utils.get_variant(variant).apply(obj, pt, parameters=parameters)
