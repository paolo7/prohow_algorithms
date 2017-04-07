import rdflib
g=rdflib.Graph()
g.load('test_data.ttl', format="ttl")

prefixes = """PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
       PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
       PREFIX prohow: <http://w3id.org/prohow#>
       PREFIX owl: <http://www.w3.org/2002/07/owl#>
       PREFIX : <http://localhost:8890/test/>
       PREFIX oa: <http://www.w3.org/ns/oa#>
       PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
"""

def get_steps(task):
    result = set()
    for row in g.query(
            prefixes+"""
            SELECT ?o
            WHERE {
                <"""+task+"""> prohow:has_step ?o .
            }
            """):
        result.add(str(row["o"]))
    return frozenset(result)

def get_methods(task):
    result = set()
    for row in g.query(
            prefixes+"""
            SELECT ?o
            WHERE {
                <"""+task+"""> prohow:has_method ?o .
            }
            """):
        result.add(str(row["o"]))
    return frozenset(result)

def get_requirements(task):
    result = set()
    for row in g.query(
            prefixes+"""
            SELECT ?o
            WHERE {
                <"""+task+"""> prohow:requires ?o .
            }
            """):
        result.add(str(row["o"]))
    return frozenset(result)

def get_sufficient_requirements(task):
    result = set()
    for row in g.query(
            prefixes+"""
            SELECT ?o
            WHERE {
                <"""+task+"""> prohow:requires_one ?o .
            }
            """):
        result.add(str(row["o"]))
    return frozenset(result)

def get_effects(task):
    result = set()
    for row in g.query(
            prefixes+"""
            SELECT ?o
            WHERE {
                ?o prohow:has_method <"""+task+"""> .
            }
            """):
        result.add(str(row["o"]))
    return frozenset(result)

def get_super_tasks(task):
    result = set()
    for row in g.query(
            prefixes+"""
            SELECT ?o
            WHERE {
                ?o prohow:has_step <"""+task+"""> .
            }
            """):
        result.add(str(row["o"]))
    return frozenset(result)

def get_task_ex_in_env(task,env):
    result = set()
    for row in g.query(
            prefixes+"""
            SELECT ?ex
            WHERE {
                ?ex prohow:has_environment <"""+env+"""> .
                ?ex prohow:has_task <"""+task+"""> .
            } LIMIT 1
            """):
        result.add(str(row["ex"]))
    return frozenset(result)

def get_tasks_in_env(env):
    result = set()
    for row in g.query(
            prefixes+"""
            SELECT ?task
            WHERE {
                ?ex prohow:has_environment <"""+env+"""> .
                ?ex prohow:has_task ?task .
            }
            """):
        result.add(str(row["task"]))
    return frozenset(result)

def get_completed_tasks_in_env(env):
    result = set()
    for row in g.query(
            prefixes+"""
            SELECT ?task
            WHERE {
                ?ex prohow:has_environment <"""+env+"""> .
                ?ex prohow:has_task ?task .
                ?ex prohow:has_result prohow:complete .
            }
            """):
        result.add(str(row["task"]))
    return frozenset(result)

def get_sub_environments_in_env(env):
    result = set()
    for row in g.query(
            prefixes+"""
            SELECT ?task ?env
            WHERE {
                ?env prohow:sub_environment_of <"""+env+"""> .
                ?env prohow:has_goal ?task .
            }
            """):
        result.add((str(row["task"]),str(row["env"])))
    return frozenset(result)

def assert_triple(s,p,o):
    global g
    g.update('''INSERT DATA { <'''+s+'''> <'''+p+'''> <'''+o+'''> .  }''')

def update_database():
    global g
    num = -1
    # keep updating until the updates no longer result in new triples
    while len(g) != num:
        num = len(g)
        update_compl_method()
        update_compl_sub_env()
        update_compl_steps()
        update_compl_bindings()

def update_compl_method():
    g.update('''
            INSERT {
              ?ex prohow:has_result prohow:complete .
            }
            WHERE {
              ?ex prohow:has_environment ?env .
              ?ex prohow:has_task ?task .
              ?env prohow:has_goal ?task .
              ?task prohow:has_method ?method .
              ?m_ex prohow:has_environment ?env .
              ?m_ex prohow:has_task ?method .
              ?m_ex prohow:has_result prohow:complete .
            }
            ''')

def update_compl_sub_env():
    g.update('''
            INSERT {
              ?ex prohow:has_result prohow:complete .
            }
            WHERE {
              ?ex prohow:has_environment ?env .
              ?ex prohow:has_task ?task .
              ?sub_env prohow:sub_environment_of ?env .
              ?sub_env prohow:has_goal ?task .
              ?sub_ex prohow:has_environment ?sub_env .
              ?sub_ex prohow:has_task ?task .
              ?sub_ex prohow:has_result prohow:complete .
            }
            ''')

def update_compl_steps():
    g.update('''
            INSERT  {
              ?ex prohow:has_result prohow:complete .
            }
            WHERE {
              ?ex prohow:has_environment ?env .
              ?ex prohow:has_task ?task .
              ?task prohow:has_step ?step .
              MINUS {
                ?ex prohow:has_environment ?env .
                ?ex prohow:has_task ?task .
                ?task prohow:has_step ?s .
                FILTER NOT EXISTS {
                    ?exs prohow:has_task ?s .
                    ?exs prohow:has_environment ?env .
                    ?exs prohow:has_result prohow:complete .
                }
              }
            }
            ''')

def update_compl_bindings():
    g.update('''
            INSERT  {
              ?ex prohow:has_result prohow:complete .
            }
            WHERE {
              ?ex prohow:has_environment ?env .
              ?ex prohow:has_task ?task .
              ?task prohow:binds_to ?binding .
              ?ex_b prohow:has_task ?binding .
              ?ex_b prohow:result prohow:complete .
              ?ex_b prohow:has_environment ?env_b .
              ?env_b (prohow:sub_environment_of |
                      ^prohow:sub_environment_of)* ?env .
            }
            ''')
