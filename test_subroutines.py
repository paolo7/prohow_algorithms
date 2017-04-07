def validate_checklist(pf,task):
    checklists = pf.create_checklists(task)
    for checklist in checklists:
        e = pf.materialise_checklist(checklist, task)
        success = pf.validate_checklist(checklist, e, task)
        if not success:
            return False
    return True

def validate_checklist_primitive(pf,primitives,task,should_be_correct):
    checklists = pf.create_checklists(task)
    success_found = False
    for checklist in checklists:
        e = pf.materialise_checklist(checklist, task)
        success_found = success_found | pf.validate_checklist_with_primitives(primitives, checklist, e, task)
    return success_found == should_be_correct
