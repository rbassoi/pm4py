def execute_script():
    import pm4py
    from pm4py.objects.conversion.wf_net.variants import to_powl

    log = pm4py.read_xes("../tests/input_data/receipt.xes")
    log = pm4py.filter_variants_top_k(log, 11)

    powl = pm4py.discover_powl(log)
    print(powl)
    net, im, fm = pm4py.convert_to_petri_net(powl)

    fitness = pm4py.fitness_alignments(log, net, im, fm)
    print(fitness)
    precision = pm4py.precision_alignments(log, net, im, fm)
    print(precision)

    powl2 = to_powl.apply(net, im, fm)
    print(powl2)
    net2, im2, fm2 = pm4py.convert_to_petri_net(powl2)

    fitness = pm4py.fitness_alignments(log, net2, im2, fm2)
    print(fitness)
    precision = pm4py.precision_alignments(log, net2, im2, fm2)
    print(precision)


if __name__ == "__main__":
    execute_script()
