import prohow_functions as pf
import test_subroutines as sr

def test_env_active():
    return pf.is_environment_active("http://localhost:8890/test/e")

def test_env_active_1():
    return pf.is_environment_active("http://localhost:8890/test/e1")

def test_env_active_2():
    return pf.is_environment_active("http://localhost:8890/test/e_w")

def test_env_not_active():
    return not pf.is_environment_active("http://localhost:8890/test/e2")

def test_requirement_sets():
    expected = frozenset(
        [frozenset(["http://localhost:8890/test/ro"]),
         frozenset(["http://localhost:8890/test/r1","http://localhost:8890/test/r2"])
         ])
    found = pf.get_requirement_sets("http://localhost:8890/test/t")
    return expected == found

def test_requirement_sets2():
    expected = frozenset(
        [frozenset(["http://localhost:8890/test/s1"])])
    found = pf.get_requirement_sets("http://localhost:8890/test/s2")
    return expected == found

def test_requirement_sets3():
    expected = frozenset(
        [frozenset(["http://localhost:8890/test/a","http://localhost:8890/test/b"])
         ])
    found = pf.get_requirement_sets("http://localhost:8890/test/c")
    return expected == found

def test_requirement_sets4():
    expected = frozenset(
        [frozenset(["http://localhost:8890/test/y"]),frozenset(["http://localhost:8890/test/z"])
         ])
    found = pf.get_requirement_sets("http://localhost:8890/test/k")
    return expected == found

def test_ready_by_requirement_one():
    return True == pf.is_task_ready_in_env("http://localhost:8890/test/t", "http://localhost:8890/test/e")

def test_ready_by_super_task():
    return True == pf.is_task_ready_in_env("http://localhost:8890/test/s1","http://localhost:8890/test/e")

def test_ready_by_super_task_not_ready_by_req():
    return False == pf.is_task_ready_in_env("http://localhost:8890/test/s2","http://localhost:8890/test/e")

def test_ready_tasks_in_env():
    expected = frozenset(("http://localhost:8890/test/r1",
                         "http://localhost:8890/test/r2",
                         "http://localhost:8890/test/ro",
                         "http://localhost:8890/test/t",
                         "http://localhost:8890/test/s1",
                         "http://localhost:8890/test/m"))
    found = pf.get_ready_tasks_in_env("http://localhost:8890/test/e")
    return expected == found

def test_ready_tasks_in_env2():
    expected = frozenset(("http://localhost:8890/test/w",
                         "http://localhost:8890/test/x"))
    found = pf.get_ready_tasks_in_env("http://localhost:8890/test/e_w")
    return expected == found

def test_next_to_accomplish_in_env():
    expected = frozenset(("http://localhost:8890/test/r1",
                          "http://localhost:8890/test/r2",
                          "http://localhost:8890/test/t",
                          "http://localhost:8890/test/s1",
                          "http://localhost:8890/test/m"))
    found = pf.get_next_tasks_to_accomplish("http://localhost:8890/test/e")
    return expected == found

def test_next_to_accomplish_in_env2():
    expected = frozenset(("http://localhost:8890/test/w",
                          "http://localhost:8890/test/x"))
    found = pf.get_next_tasks_to_accomplish("http://localhost:8890/test/e_w")
    return expected == found

def test_next_to_accomplish_in_sub_env():
    expected = {
        "http://localhost:8890/test/e": frozenset(["http://localhost:8890/test/r1",
                          "http://localhost:8890/test/r2",
                          "http://localhost:8890/test/t",
                          "http://localhost:8890/test/s1",
                          "http://localhost:8890/test/m"]),
        "http://localhost:8890/test/e1": frozenset(["http://localhost:8890/test/m1"])
    }
    found = pf.get_next_tasks_to_accomplish_recursive("http://localhost:8890/test/e")
    return expected == found

def validate_checklists1():
    return sr.validate_checklist(pf,"http://localhost:8890/test/t")

def validate_checklists2():
    return sr.validate_checklist(pf,"http://localhost:8890/test/w")

def validate_checklists3():
    return sr.validate_checklist(pf,"http://localhost:8890/test/c")

def validate_checklists4():
    return sr.validate_checklist(pf,"http://localhost:8890/test/a")

def validate_checklists5():
    return sr.validate_checklist(pf,"http://localhost:8890/test/k")

def validate_checklists6():
    return sr.validate_checklist(pf,"http://localhost:8890/test/y")

def validate_checklists_with_primitives():
    return sr.validate_checklist_primitive(pf,frozenset(["http://localhost:8890/test/s1","http://localhost:8890/test/s2",
                                                         "http://localhost:8890/test/r1","http://localhost:8890/test/r2"])
                              , "http://localhost:8890/test/t", True)

def validate_checklists_with_primitives1():
    return sr.validate_checklist_primitive(pf,frozenset(["http://localhost:8890/test/s1","http://localhost:8890/test/s2",
                                                         "http://localhost:8890/test/ro"])
                              , "http://localhost:8890/test/t", True)

def validate_checklists_with_primitives2():
    return sr.validate_checklist_primitive(pf,frozenset(["http://localhost:8890/test/t","http://localhost:8890/test/t",
                                                         "http://localhost:8890/test/r1","http://localhost:8890/test/r2"])
                              , "http://localhost:8890/test/t", True)

def validate_checklists_with_primitives3():
    return sr.validate_checklist_primitive(pf,frozenset(["http://localhost:8890/test/c","http://localhost:8890/test/a",
                                                         "http://localhost:8890/test/z", "http://localhost:8890/test/x",
                                                         "http://localhost:8890/test/b","http://localhost:8890/test/k"])
                              , "http://localhost:8890/test/w", True)

def validate_checklists_with_primitives4():
    return sr.validate_checklist_primitive(pf,frozenset(["http://localhost:8890/test/c","http://localhost:8890/test/a",
                                                         "http://localhost:8890/test/y", "http://localhost:8890/test/x",
                                                         "http://localhost:8890/test/b","http://localhost:8890/test/k"])
                              , "http://localhost:8890/test/w", True)

def validate_checklists_with_primitives5():
    return sr.validate_checklist_primitive(pf,frozenset(["http://localhost:8890/test/b","http://localhost:8890/test/w"])
                              , "http://localhost:8890/test/w", True)

def validate_checklists_with_primitives_false():
    return sr.validate_checklist_primitive(pf,frozenset(
        ["http://localhost:8890/test/sa1", "http://localhost:8890/test/s2", "http://localhost:8890/test/r1",
         "http://localhost:8890/test/r2"])
                              , "http://localhost:8890/test/t", False)

def validate_checklists_with_primitives_false2():
    return sr.validate_checklist_primitive(pf, frozenset(
        ["http://localhost:8890/test/r1", "http://localhost:8890/test/s2", "http://localhost:8890/test/s1"])
                                           , "http://localhost:8890/test/t", False)

def validate_checklists_with_primitives_false3():
    return sr.validate_checklist_primitive(pf, frozenset(
        ["http://localhost:8890/test/t", "http://localhost:8890/test/s2", "http://localhost:8890/test/s1"])
                                           , "http://localhost:8890/test/m", False)

def validate_checklists_with_primitives_false4():
    return sr.validate_checklist_primitive(pf,frozenset(["http://localhost:8890/test/c","http://localhost:8890/test/a",
                                                         "http://localhost:8890/test/y", "http://localhost:8890/test/z",
                                                         "http://localhost:8890/test/b","http://localhost:8890/test/k"])
                              , "http://localhost:8890/test/w", False)

def validate_checklists_with_primitives_false5():
    return sr.validate_checklist_primitive(pf,frozenset(["http://localhost:8890/test/x","http://localhost:8890/test/a",
                                                         "http://localhost:8890/test/y", "http://localhost:8890/test/z",
                                                         "http://localhost:8890/test/b","http://localhost:8890/test/k"])
                              , "http://localhost:8890/test/w", False)

#def test_checklist_generation():
#    checklists = pf.create_checklists("http://localhost:8890/test/t")
#    for checklist in checklists
