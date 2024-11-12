def execute_script():
    import pm4py
    from pm4py.objects.conversion.wf_net.variants import to_powl
    from pm4py.objects.powl.obj import StrictPartialOrder, OperatorPOWL, Transition, SilentTransition
    from pm4py.objects.process_tree.obj import Operator

    # Define basic transitions
    A = Transition(label="A")
    B = Transition(label="B")
    C = Transition(label="C")
    D = Transition(label="D")
    E = Transition(label="E")
    F = Transition(label="F")
    G = Transition(label="G")
    H = Transition(label="H")
    I = Transition(label="I")
    J = Transition(label="J")
    K = Transition(label="K")
    L = Transition(label="L")
    M = Transition(label="M")

    # Define inner partial order PO_G: I and J must be executed before K
    PO_G_nodes = [I, J, K]
    PO_G = StrictPartialOrder(nodes=PO_G_nodes)
    PO_G.order.add_edge(I, K)
    PO_G.order.add_edge(J, K)

    # Define H as a choice between L and M
    H_choice = OperatorPOWL(operator=Operator.XOR, children=[L, M])

    # Define LOOP1: loop between PO_G and H_choice
    LOOP1 = OperatorPOWL(operator=Operator.LOOP, children=[PO_G, H_choice])

    # Define PO1: A and B must be executed before C and D
    PO1_nodes = [A, B, C, D]
    PO1 = StrictPartialOrder(nodes=PO1_nodes)
    PO1.order.add_edge(A, C)
    PO1.order.add_edge(A, D)
    PO1.order.add_edge(B, C)
    PO1.order.add_edge(B, D)

    # Define XOR1: choice between E and F
    XOR1 = OperatorPOWL(operator=Operator.XOR, children=[E, F])

    # Combine PO1, XOR1, and LOOP1 into the main partial order
    main_nodes = [PO1, XOR1, LOOP1]
    main_PO = StrictPartialOrder(nodes=main_nodes)
    main_PO.order.add_edge(PO1, XOR1)
    main_PO.order.add_edge(XOR1, LOOP1)

    # The resulting POWL model (main_PO) represents a complex process with nested partial orders

    #pm4py.view_powl(root, format="svg")
    print(main_PO)
    net, im, fm = pm4py.convert_to_petri_net(main_PO)
    #pm4py.view_petri_net(net, im, fm, format="svg")

    log = pm4py.play_out(net, im, fm)

    powl = to_powl.apply(net, im, fm)
    print(powl)
    net, im, fm = pm4py.convert_to_petri_net(powl)
    #pm4py.view_petri_net(net, im, fm, format="svg")

    fitness = pm4py.fitness_alignments(log, net, im, fm)
    print(fitness)


if __name__ == "__main__":
    execute_script()
