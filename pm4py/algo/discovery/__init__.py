from pm4py.algo.discovery import dfg, alpha, inductive, transition_system, log_skeleton, footprints, minimum_self_distance, performance_spectrum, temporal_profile, batches, heuristics
import pkgutil

if pkgutil.find_loader("pandas"):
    from pm4py.algo.discovery import correlation_mining
