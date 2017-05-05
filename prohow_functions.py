import time
import sparql_queries as sp

# Competency questions

def Q1(task):
    return get_requirement_sets(task)

def Q2(task):
    return get_decomposition_sets(task)

def Q3(env):
    return get_tasks_in_env(env)

def Q4(env):
    return get_completed_tasks_in_env(env)

def Q5(env):
    return get_ready_tasks_in_env(env)

def Q6(env):
    return get_sub_environments_in_env(env)

def Q7_without_sub_env(env):
    return get_next_tasks_to_accomplish(env)

def Q7_with_sub_env(env):
    return get_next_tasks_to_accomplish_recursive(env)

def Q8(task):
    return create_checklists(task)

# Functions that can be directly answered by SPARQL queries

def get_steps(task):
    return sp.get_steps(task)

def get_methods(task):
    return sp.get_methods(task)

def get_requirements(task):
    return sp.get_requirements(task)

def get_sufficient_requirements(task):
    return sp.get_sufficient_requirements(task)

def get_super_environments(env):
    return sp.get_super_environments(env)

def get_effects(task):
    return sp.get_effects(task)

def get_super_tasks(task):
    return sp.get_super_tasks(task)

def get_tasks_in_env(env):
    return sp.get_tasks_in_env(env)

def get_completed_tasks_in_env(env):
    return sp.get_completed_tasks_in_env(env)

def get_sub_environments_in_env(env):
    return sp.get_sub_environments_in_env(env)

def get_task_ex_in_env(task,env):
    ex = sp.get_task_ex_in_env(task, env)
    if ex:
        for e in ex:
            return e
    return None

def get_goal(env):
    goal = sp.get_goal(env)
    if goal:
        for t in goal:
            return t
    return None

# Functions that can be directly answered by SPARQL queries

def get_requirement_sets(task):
    R_and = get_requirements(task)
    R_or = get_sufficient_requirements(task)
    R_sets = set()
    if R_and:
        R_sets.add(R_and)
    for r in R_or:
        R_new = set()
        R_new.add(r)
        R_sets.add(frozenset(R_new))
    return frozenset(R_sets)

def get_decomposition_sets(task):
    D_and = get_steps(task)
    D_or = get_methods(task)
    D_sets = set()
    if D_and:
        D_sets.add(D_and)
    for d in D_or:
        D_new = set()
        D_new.add(d)
        D_sets.add(frozenset(D_new))
    return frozenset(D_sets)

# An algorithm to determine whether a task $t$ is ready to be executed in an environment $e$.
def is_task_ready_in_env(task,env):
    if not is_environment_active(env):
        return False
    S = get_super_tasks(task)
    if S:
        B = False
        for s in S:
            if not B:
                B = is_task_ready_in_env(s,env)
        if not B:
            return False
    R_all = get_requirement_sets(task)
    if not R_all:
        return True
    C = get_completed_tasks_in_env(env)
    for R in R_all:
        if R <= C:
            return True
    return False

# An algorithm to determine whether an environment $a$ is active.
def is_environment_active(env):
    E_super = get_super_environments(env)
    if not E_super:
        return True
    g = get_goal(env)
    for super in E_super:
        if is_task_ready_in_env(g,super):
            return True
    return False


def get_ready_tasks_in_env(env):
    R = set()
    T = get_tasks_in_env(env)
    for t in T:
        if is_task_ready_in_env(t,env):
            R.add(t)
    return frozenset(R)

def get_next_tasks_to_accomplish(env):
    R = get_ready_tasks_in_env(env)
    C = get_completed_tasks_in_env(env)
    R_not_C = R-C
    return R_not_C

def get_next_tasks_to_accomplish_recursive(env):
    A = {}
    expand_map_wit_tasks_to_accomplish_in_subenv(env,A)
    return A

def expand_map_wit_tasks_to_accomplish_in_subenv(env,A):
    A[env] = get_next_tasks_to_accomplish(env)
    E = get_sub_environments_in_env(env)
    for s in E:
        t = s[0]
        if t in A[env]:
            a = s[1]
            expand_map_wit_tasks_to_accomplish_in_subenv(a,A)

def merge_pair_of_AS(A,B):
    if not A:
        return B
    if not B:
        return A
    M = set()
    for A_alternative in A:
        for B_alternative in B:
            M.add(frozenset(A_alternative | B_alternative))
    return frozenset(M)

def create_checklists(task):
    U = expand_checklist_requirements(frozenset([task]),frozenset([]))
    U_methods = set()
    M = get_methods(task)
    for m in M:
        for S in U:
            S_m = set()
            S_m = S_m | S
            S_m.add(m)
            S_m_all = expand_checklist_requirements(S_m,S)
            S_m_all = S_m_all | expand_checklist_steps(S_m_all,set([task]))
            U_methods = U_methods | S_m_all
    U = U | expand_checklist_steps(U,frozenset()) | U_methods
    O = set()
    for S in U:
        O.add(order_task_set(S))
    return O

# Expand check-list tasks S with their requirements, excluding the tasks in A
def expand_checklist_requirements(S,A):
    A_new = set()
    A_new = A_new | A
    S_new = set()
    S_new = S_new | S
    T = set()
    T.add(frozenset(S_new))
    # for all the tasks in S not already considered (not in A)
    # find their requirements and merge them in the solution T
    for t in S_new:
        if not t in A_new:
            R = get_requirement_sets(t)
            if R:
                T = set(merge_pair_of_AS(T,frozenset(R)))
    # add all the tasks in S in A_new to record that they have been used
    A_new = A_new | S
    T_copy = set(T)
    for P in T_copy:
        if not frozenset(P) <= frozenset(A_new):
            P_expanded = expand_checklist_requirements(P,A_new)
            # remove the not-expanded set P before adding its expanded version
            T_to_remove = set()
            for P1 in T:
                if frozenset(P1) == frozenset(P):
                    T_to_remove.add(P1)
            for T_r in T_to_remove:
                T.remove(T_r)
                #T = frozenset(T) - frozenset(P)
            T = T | P_expanded
    return T

def order_task_set(S):
    L = []
    S_left = set()
    S_left = S_left | S
    while S_left:
        A = set([])
        for element in L:
            A = A |element
        O = set()
        O_is_empty = True
        for t in S_left:
            R_satisfied = False
            R = get_requirement_sets(t)
            R_sup = set()
            S_tasks = get_super_tasks(t)
            for t_super in S_tasks:
                t_super_req = get_requirement_sets(t_super)
                R_sup.update(merge_pair_of_AS(R,t_super_req))
            if R_sup:
                R = R_sup
            if not R:
                R_satisfied = True
            else:
                for r in R:
                    if A and frozenset(r) <= frozenset(A):
                        R_satisfied = True
            if R_satisfied == True:
                O.add(t)
                O_is_empty = False
        if O_is_empty:
            raise ValueError('The set of tasks contains a deadlock, or missing requirements, it cannot be ordered.')
        L.append(frozenset(O))
        S_left = S_left - O
    return tuple(L)

def expand_checklist_steps(S_previous_all,K):
    S_new_all = set()
    for S_pre in S_previous_all:
        for t in S_pre:
            if not t in K:
                T_steps = get_steps(t)
                if T_steps and not frozenset(T_steps) <= frozenset(S_pre):
                    S_new_exp = expand_checklist_requirements(S_pre | T_steps,S_pre)
                    S_new_all = S_new_all | S_new_exp
                    S_new_all = S_new_all | expand_checklist_steps(S_new_exp,K | set([t]))
    return S_new_all

# Custom method for local minting of URIs
# In a real implementation the localhost domain should be changed into a safe proprietary one
URI_mint_index = 0
def mint_URI():
    global URI_mint_index
    URI_mint_index += 1
    return "http://localhost:8890/mint/"+str(URI_mint_index)+"/"+str(int(round(time.time() * 1000)))

def materialise_checklist(S,t):
    e = mint_URI()
    sp.assert_triple(e,"http://w3id.org/prohow#has_goal",t)
    S_flat = set()
    contains_sets = False
    for s in S:
        if isinstance(s, (list, tuple, set, frozenset)):
            contains_sets = True
    if contains_sets:
        for s in S:
            S_flat.update(s)
    else:
        S_flat = set(S)
    for s in S_flat:
        ex = mint_URI()
        sp.assert_triple(ex, "http://w3id.org/prohow#has_environment", e)
        sp.assert_triple(ex, "http://w3id.org/prohow#has_task", s)
    return e

def update_database():
    sp.update_database()

def validate_checklist(L,e,t):
    for S in L:
        for x in S:
            if not is_task_ready_in_env(x,e):
                return False
            ex = get_task_ex_in_env(x,e)
            if not ex is None:
                sp.assert_triple(ex,"http://w3id.org/prohow#has_result","http://w3id.org/prohow#complete")
                sp.update_database()
    C = get_completed_tasks_in_env(e)
    if t in C:
        return True
    else:
        return False

# An algorithm to validate whether a primitive task set $A$ is sufficient to complete a check-list $e$ having a list of tasks $L$ and goal $t$.
def validate_checklist_with_primitives(A,L,e,t):
    for S in L:
        for x in (S & A):
            if is_task_ready_in_env(x,e):
                ex = get_task_ex_in_env(x,e)
                if not ex is None:
                    sp.assert_triple(ex,"http://w3id.org/prohow#has_result","http://w3id.org/prohow#complete")
                    sp.update_database()
    C = get_completed_tasks_in_env(e)
    if t in C:
        return True
    else:
        return False
