import sys
import tempfile
from enum import Enum

import pulp
from pulp import LpProblem, LpMinimize, LpVariable, LpStatus, value, lpSum
from pm4py.util import exec_utils


class Parameters(Enum):
    REQUIRE_ILP = "require_ilp"
    INTEGRALITY = "integrality"
    BOUNDS = "bounds"


MIN_THRESHOLD = 1e-12
MAX_NUM_CONSTRAINTS = 7  # Maximum safe number of constraints (log10)


# Solver function to maintain compatibility with different versions of PuLP
if hasattr(pulp, "__version__"):
    # New interface
    from pulp import PULP_CBC_CMD

    def solver(prob):
        return PULP_CBC_CMD(msg=0).solve(prob)
else:
    # Old interface
    def solver(prob):
        return prob.solve()


def get_variable_name(index):
    """
    Generates a variable name with leading zeros to ensure consistent length.

    Parameters
    ----------
    index : int
        The index of the variable.

    Returns
    -------
    str
        A string representing the variable name with leading zeros.
    """
    return str(index).zfill(MAX_NUM_CONSTRAINTS)


def apply(c, Aub, bub, Aeq=None, beq=None, parameters=None):
    """
    Solves a linear programming problem using PuLP.

    Parameters
    ----------
    c : array_like
        Coefficients for the objective function.
    Aub : array_like
        Coefficient matrix for inequality (less than or equal to) constraints.
    bub : array_like
        Right-hand side vector for inequality constraints.
    Aeq : array_like, optional
        Coefficient matrix for equality constraints.
    beq : array_like, optional
        Right-hand side vector for equality constraints.
    parameters : dict, optional
        Additional parameters for the solver. Can include:
        - 'require_ilp': bool indicating if all variables should be integer.
        - 'integrality': list of ints (0 or 1) indicating variable integrality.
        - 'bounds': list of tuples specifying (lowBound, upBound) for variables.

    Returns
    -------
    pulp.LpProblem
        The solved linear programming problem.
    """
    if parameters is None:
        parameters = {}

    # Get parameters
    require_ilp = parameters.get("require_ilp", False)
    integrality = parameters.get("integrality", None)
    bounds = parameters.get("bounds", None)

    # Initialize the problem
    prob = LpProblem("LP_Problem", LpMinimize)

    # Define decision variables
    num_vars = Aub.shape[1]

    # Validate integrality and bounds lists
    if integrality is not None and len(integrality) != num_vars:
        raise ValueError("Length of 'integrality' list must be equal to the number of variables.")
    if bounds is not None and len(bounds) != num_vars:
        raise ValueError("Length of 'bounds' list must be equal to the number of variables.")

    x_vars = []

    for i in range(num_vars):
        var_name = f"x_{get_variable_name(i)}"

        # Determine variable bounds
        lb = None
        ub = None
        if bounds is not None:
            lb, ub = bounds[i]
            # Convert 'None' strings to actual None
            lb = None if lb == 'None' else lb
            ub = None if ub == 'None' else ub

        # Determine variable category (continuous or integer)
        if integrality is not None:
            # Use integrality list
            cat = 'Integer' if integrality[i] else 'Continuous'
        elif require_ilp:
            # All variables are integer
            cat = 'Integer'
        else:
            # All variables are continuous
            cat = 'Continuous'

        x_vars.append(LpVariable(var_name, lowBound=lb, upBound=ub, cat=cat))

    # Build the objective function
    objective_expr = lpSum(
        c[j] * x_vars[j] for j in range(len(c)) if abs(c[j]) >= MIN_THRESHOLD
    )
    prob += objective_expr, "Objective"

    # Add inequality constraints
    for i in range(Aub.shape[0]):
        constraint_expr = lpSum(
            Aub[i, j] * x_vars[j] for j in range(num_vars) if abs(Aub[i, j]) >= MIN_THRESHOLD
        )
        prob += (constraint_expr <= bub[i]), f"Inequality_Constraint_{get_variable_name(i)}"

    # Add equality constraints, if any
    if Aeq is not None and beq is not None:
        for i in range(Aeq.shape[0]):
            constraint_expr = lpSum(
                Aeq[i, j] * x_vars[j] for j in range(num_vars) if abs(Aeq[i, j]) >= MIN_THRESHOLD
            )
            constraint_name = f"Equality_Constraint_{get_variable_name(i)}"
            prob += (constraint_expr == beq[i]), constraint_name

    # Optionally write the LP problem to a temporary file (can be omitted)
    with tempfile.NamedTemporaryFile(suffix='.lp', delete=False) as tmp_file:
        prob.writeLP(tmp_file.name)

    # Solve the problem
    solver(prob)

    return prob


def get_prim_obj_from_sol(sol, parameters=None):
    """
    Retrieves the objective value from the solved LP problem.

    Parameters
    ----------
    sol : pulp.LpProblem
        The solved LP problem.
    parameters : dict, optional
        Additional parameters (not used in this function).

    Returns
    -------
    float
        The value of the objective function.
    """
    return value(sol.objective)


def get_points_from_sol(sol, parameters=None):
    """
    Retrieves the values of the decision variables from the solved LP problem.

    Parameters
    ----------
    sol : pulp.LpProblem
        The solved LP problem.
    parameters : dict, optional
        Additional parameters that may include:
        - 'maximize': bool indicating if the problem is maximization.
        - 'return_when_none': bool indicating if default values should be returned when no solution is found.
        - 'var_corr': dict containing variable correlations (used to determine the length of the output list).

    Returns
    -------
    list or None
        A list of variable values if the solution is optimal, otherwise None or default values.
    """
    if parameters is None:
        parameters = {}

    maximize = parameters.get("maximize", False)
    return_when_none = parameters.get("return_when_none", False)
    var_corr = parameters.get("var_corr", {})

    if LpStatus[sol.status] == "Optimal":
        # Extract variable values from the solution
        return [v.varValue for v in sol.variables()]
    elif return_when_none:
        # Return a list of default values if no solution is found
        default_value = sys.float_info.max if maximize else sys.float_info.min
        return [default_value] * len(var_corr)
    else:
        return None
