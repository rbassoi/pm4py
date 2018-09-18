from pm4py.models.petri import visualize
from pm4py.algo.tokenreplay import factory as token_replay
from pm4py.algo.tokenreplay.data_structures import performance_map
from pm4py import log as log_lib
from pm4py import util as pmutil
from pm4py.filtering.tracelog.variants import variants_filter as variants_module

PARAM_ACTIVITY_KEY = pmutil.constants.PARAMETER_CONSTANT_ACTIVITY_KEY
PARAM_TIMESTAMP_KEY = pmutil.constants.PARAMETER_CONSTANT_TIMESTAMP_KEY

PARAMETERS = [PARAM_ACTIVITY_KEY, PARAM_TIMESTAMP_KEY]

def get_decorations(log, net, initial_marking, final_marking, parameters=None, measure="frequency"):
    """
    Calculate decorations in order to annotate the Petri net

    Parameters
    -----------
    log
        Trace log
    net
        Petri net
    initial_marking
        Initial marking
    final_marking
        Final marking
    parameters
        Parameters associated to the algorithm
    measure
        Measure to represent on the process model (frequency/performance)

    Returns
    ------------
    decorations
        Decorations to put on the process model
    """
    if parameters is None:
        parameters = {}

    aggregationMeasure = None
    if "aggregationMeasure" in parameters:
        aggregationMeasure = parameters["aggregationMeasure"]

    activity_key = parameters[
            PARAM_ACTIVITY_KEY] if PARAM_ACTIVITY_KEY in parameters else log_lib.util.xes.DEFAULT_NAME_KEY
    timestamp_key = parameters[PARAM_TIMESTAMP_KEY] if PARAM_TIMESTAMP_KEY in parameters else "time:timestamp"

    variants_idx = variants_module.get_variants_from_log_trace_idx(log, attribute_key=activity_key)
    variants = variants_module.convert_variants_trace_idx_to_trace_obj(log, variants_idx)

    parameters_TR = {pmutil.constants.PARAMETER_CONSTANT_ACTIVITY_KEY: activity_key, "variants": variants}

    # do the replay
    [traceIsFit, traceFitnessValue, activatedTransitions, placeFitness, reachedMarkings, enabledTransitionsInMarkings] = \
        token_replay.apply(log, net, initial_marking, final_marking, parameters=parameters_TR)

    element_statistics = performance_map.single_element_statistics(log, net, initial_marking,
                                                                   activatedTransitions,
                                                                   activity_key=activity_key,
                                                                   timestamp_key=timestamp_key)
    aggregated_statistics = performance_map.aggregate_statistics(element_statistics, measure=measure,
                                                                 aggregationMeasure=aggregationMeasure)

    return aggregated_statistics

def apply_frequency(net, initial_marking, final_marking, log=None, aggregated_statistics=None, parameters=None):
    """
    Apply method for Petri net visualization (useful for recall from factory; it calls the graphviz_visualization method)
    adding frequency representation obtained by token replay

    Parameters
    -----------
    net
        Petri net
    initial_marking
        Initial marking
    final_marking
        Final marking
    log
        (Optional) trace log
    parameters
        Algorithm parameters (including the activity key used during the replay, and the timestamp key)

    Returns
    -----------
    viz
        Graph object
    """
    if aggregated_statistics is None:
        if log is not None:
            aggregated_statistics = get_decorations(log, net, initial_marking, final_marking, parameters=parameters, measure="frequency")
    return visualize.apply(net, initial_marking, final_marking, parameters=parameters, decorations=aggregated_statistics)

def apply_performance(net, initial_marking, final_marking, log=None, aggregated_statistics=None, parameters=None):
    """
    Apply method for Petri net visualization (useful for recall from factory; it calls the graphviz_visualization method)
    adding performance representation obtained by token replay

    Parameters
    -----------
    net
        Petri net
    initial_marking
        Initial marking
    final_marking
        Final marking
    log
        (Optional) trace log
    parameters
        Algorithm parameters (including the activity key used during the replay, and the timestamp key)

    Returns
    -----------
    viz
        Graph object
    """
    if aggregated_statistics is None:
        if log is not None:
            aggregated_statistics = get_decorations(log, net, initial_marking, final_marking, parameters=parameters, measure="performance")
    return visualize.apply(net, initial_marking, final_marking, parameters=parameters, decorations=aggregated_statistics)