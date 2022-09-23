import xmltodict
import graphviz
import json
from pprintpp import pprint as pp

def runxml(fname): 
    # with open('wk4.xml') as fd:
    with open(fname) as fd:
        doc = xmltodict.parse(fd.read())

    dot = graphviz.Digraph(comment='Workflow',
                           engine='dot',
                           graph_attr={
                               'label': 'Orthogonal edges',
                               'splines': 'ortho',
                               'nodesep': '0.5'})

    class Statuses:
        def __init__(self, id, name):
            self.id = id
            self.name = name

    class Global_transition:
        def __init__(self, id, name, target_status_id):
            self.id = id
            self.name = name
            self.target_id = target_status_id

    class Common_transition:
        def __init__(self, id, name, target):
            self.id = id
            self.name = name
            self.target = target

    class Single_transition:
        def __init__(self, id, name, target_id, c_st_id, c_st_name):
            self.id = id
            self.name = name
            self.target_id = target_id
            self.current_st_id = c_st_id
            self.current_st_name = c_st_name


    all_statuses = []
    for status in doc['workflow']['steps']['step']:
        #print(status['@name'])
        st_name = status['@name']
        st_id = status['@id']
        st = Statuses(st_id, st_name)
        all_statuses.append(st)
        dot.node(st_id, st_name, {'color': 'lightblue', 'shape': 'box', 'style': 'filled'})

    init_act = doc['workflow']['initial-actions']['action']
    init_action_id = init_act['@id']
    init_action_name = init_act['@name']
    initial_action_target_status_id = init_act['results']['unconditional-result']['@step']

    print('>>> Initial action: ', init_action_name)
    print('>>> initial action id: ', init_action_id)


    dot.node('-1','Início', {'color': 'lightblue', 'shape': 'box', 'style': 'filled'})
    dot.edge('-1',initial_action_target_status_id , xlabel = init_action_name)


    all_global_transitions = []

    if 'global-actions' in doc['workflow']:
        if 'action' in doc['workflow']['global-actions']:
            if isinstance(doc['workflow']['global-actions']['action'], list):
                for g_act in doc['workflow']['global-actions']['action']:
                    g_act_id = g_act['@id']
                    g_act_name = g_act['@name']
                    g_act_target = g_act['results']['unconditional-result']['@step']
                    all_global_transitions.append(Global_transition(g_act_id, g_act_name, g_act_target))


    all_common_actions = []
    if 'common-actions' in doc['workflow']:
        for common_action in doc['workflow']['common-actions']['action']:
            cm_ac_id = common_action['@id']
            cm_ac_name = common_action['@name']
            cm_ac_target= common_action['results']['unconditional-result']['@step']
            cm_ac = Common_transition(cm_ac_id, cm_ac_name, cm_ac_target)
            all_common_actions.append(cm_ac)


    # Printing all the common actions
    for x in all_common_actions:
        print('>>> Common action: ', x.name)
        print('>>> Common action id: ', x.id)
        print('>>> Common action target: ', x.target)

    for step in doc['workflow']['steps']['step']:
        if 'actions' in step:
            print('>>> Actions in step =>  Current step: ', step['@name'])
            if 'common-action' in step['actions']:
                if isinstance(step['actions']['common-action'], list):
                    for common_action in step['actions']['common-action']:
                        print(">>>> common_action: ", common_action, ">> common_action['id'] : ", common_action['@id'])
                        for ca in all_common_actions:
                            if ca.id == common_action['@id']:
                                print(">>>>>> common_action['id'] : ", common_action['@id'], ">> ca.id : ", ca.id)
                                dot.edge(step['@id'], ca.target, xlabel = ca.name)
                        # dot.edge(step['@id'], common_action['@id'], xlabel = "aaaaaaaaaa")

    dot.node('0', 'ALL', {'color': 'lightblue', 'shape': 'box', 'style': 'filled'})
    for global_action in all_global_transitions:
        # print('>>> Global action: ', global_action.name)
        for status in all_statuses:
            if status.id == global_action.target_id:
                dot.edge('0', status.id, xlabel = global_action.name)



    all_single_transitions = []
    for step in doc['workflow']['steps']['step']:
        sg_tr_c_st_id = step['@id']
        sg_tr_c_st_name = step['@name']
        if 'actions' in step:
            if 'action' in step['actions']:
                for list_item in step['actions']['action']:
                    if type(list_item) is dict:
                        sg_tr_id = list_item['@id']
                        sg_tr_name = list_item['@name']
                        sg_tr_target_id = list_item['results']['unconditional-result']['@step']
                        sg_tr = Single_transition(sg_tr_id, sg_tr_name, sg_tr_target_id, sg_tr_c_st_id, sg_tr_c_st_name)
                        all_single_transitions.append(sg_tr)


    for tr in all_single_transitions:
        dot.edge(tr.current_st_id, tr.target_id, xabel = tr.name)

    dot.render(directory='./static/images', format='jpg')
    print('filename: ' + dot.filename)
    print('filepath + jpg: ' + dot.filepath+'.jpg')
    return dot.filepath+'.jpg'


