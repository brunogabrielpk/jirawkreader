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
    # dot.edge(step['@id'], status.id, label = ca2.name)


    # [WARN] It seems that when there is only one global transition, tha workflow -> global-actions -> action is treated as str
    all_global_transitions = []

    if 'global-actions' in doc['workflow']:
        if 'action' in doc['workflow']['global-actions']:
            if isinstance(doc['workflow']['global-actions']['action'], list):
                for g_act in doc['workflow']['global-actions']['action']:
                    g_act_id = g_act['@id']
                    g_act_name = g_act['@name']
                    g_act_target = g_act['results']['unconditional-result']['@step']
                    all_global_transitions.append(Global_transition(g_act_id, g_act_name, g_act_target))





        # pp(doc['workflow']['global-actions'])
        # # print(type(doc['workflow']['global-actions']))
        # # print("dict len below?")
        # gla_count = 0
        # # print(len(doc['workflow']['global-actions']['action']))
        # for item in doc['workflow']['global-actions']['action']:
        #     gla_count += 1
        # print("gla_count: ", gla_count)
        # if gla_count  == 1:
        #     if 'action' in doc['workflow']['global-actions']:
        #             print(" There action in global-actions:)")
        #             gl_t_id = doc['workflow']['global-actions']['action']['@id']
        #             gl_t_name = doc['workflow']['global-actions']['action']['@name']
        #             gl_t_target_id = doc['workflow']['global-actions']['action']['results']['unconditional-result']['@step']
        #             gl_t = Global_transition(gl_t_id, gl_t_name, gl_t_target_id)
        #             all_global_transitions.append(gl_t)
        # else:
        #     for x in doc['workflow']['global-actions']['action']:
        #         print(type(x))
        #         if 'action' in x:
        #             print(" There action in x :)")
        #             gl_t_id = x['action']['@id']
        #             gl_t_name = x['action']['@name']
        #             gl_t_target_id = x['action']['results']['unconditional-result']['@step']
        #             gl_t = Global_transition(gl_t_id, gl_t_name, gl_t_target_id)
        #             all_global_transitions.append(gl_t)


    all_common_actions = []
    if 'common-actions' in doc['workflow']:
        for common_action in doc['workflow']['common-actions']['action']:
            cm_ac_id = common_action['@id']
            cm_ac_name = common_action['@name']
            cm_ac_target= common_action['results']['unconditional-result']['@step']
            cm_ac = Common_transition(cm_ac_id, cm_ac_name, cm_ac_target)
            all_common_actions.append(cm_ac)
    # Draw all the common actions [DONE]
    for step in doc['workflow']['steps']['step']:
        if 'actions' in step:
            # print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>      step['actions']: ")
            # print(step['actions'])
            if 'common-action' in step['actions']:
                # print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> common-action : ")
                # print(step['actions']['common-action'])
                # print(">>>>> common action target")
                for ca2 in all_common_actions:
                    # print(">>> step['actions']['common-action']")
                    # print(step['actions']['common-action'])
                    for ca1 in step['actions']['common-action']:
                        #print(">>> type of ca1")
                        #print(type(ca1))
                        #print(">>> length of ca1")
                        #print(len(ca1))
                        if type(ca1) is dict:
                            if ca2.id == ca1['@id']:
                                #print("#$%#$%#$%#$%#$%#$%#$%#$%#$%#$%$#%#$%#$%#$%$#%#$%#$%#$%#$%")
                                #print(">>>> if ca2.id == ca1['@id']:")
                                #print(">>>ca2.id: ")
                                #print(ca2.id)
                                #print(">>>Status_name: ca2.target : ")
                                for status in all_statuses:
                                    if status.id == ca2.target:
                                        #print(status.name)
                                        dot.edge(step['@id'], status.id, xlabel = ca2.name)
                                        # dot.edge(step['@name'], status.name, ca2.name)
                                        #print(">>>ca1: ")
                                        #print(ca1)
                                        # print(">>> type(ca1)")
                                        # print(type(ca1))
                                        #print(">>>ca1['@id']: ")
                                        #print(ca1['@id'])
        # print("#########################")
        # print("#########################")

    # Draw the global actions [DONE]
    # Draw a node to represent "ALL" statuses

    dot.node('0', 'ALL', {'color': 'lightblue', 'shape': 'box', 'style': 'filled'})
    for global_action in all_global_transitions:
        # print(">>> global_action.id: ")
        # print(global_action.id)
        # print(">>> global_action.name: ")
        # print(global_action.name)
        # print(">>> global_action.target_id: ")
        # print(global_action.target_id)
        for status in all_statuses:
            if status.id == global_action.target_id:
                dot.edge('0', status.id, xlabel = global_action.name)



    all_single_transitions = []
    for step in doc['workflow']['steps']['step']:
        sg_tr_c_st_id = step['@id']
        sg_tr_c_st_name = step['@name']
        if 'actions' in step:
            # print(type(step['actions']))
            if 'action' in step['actions']:
                # print(type(step['actions']['action']))
                # pp(step['actions']['action'])
                for list_item in step['actions']['action']:
                    if type(list_item) is dict:
                        # print(type(list_item))
                        # pp(list_item)
                        sg_tr_id = list_item['@id']
                        sg_tr_name = list_item['@name']
                        sg_tr_target_id = list_item['results']['unconditional-result']['@step']
                        sg_tr = Single_transition(sg_tr_id, sg_tr_name, sg_tr_target_id, sg_tr_c_st_id, sg_tr_c_st_name)
                        all_single_transitions.append(sg_tr)


    for tr in all_single_transitions:
        # print("Single transition data: ")
        # print(tr.id)
        # print(tr.name)
        # print(tr.target_id)
        # print(tr.current_st_id)
        # print(tr.current_st_name)
        dot.edge(tr.current_st_id, tr.target_id, xabel = tr.name)

    dot.render(directory='./static/images', format='jpg')
    print('filename: ' + dot.filename)
    print('filepath + jpg: ' + dot.filepath+'.jpg')
    return dot.filepath+'.jpg'


