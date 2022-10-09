import xmltodict
import graphviz
import json
import random
import os
import shutil
from pprintpp import pprint as pp

def runxml(fname): 
    # with open('wk4.xml') as fd:
    with open(fname) as fd:
        doc = xmltodict.parse(fd.read())
    rn = random.randint(1,10000)
    rfilename = 'd-' + str(rn) + '-Diagraph.gv'
    dot = graphviz.Digraph(filename=rfilename,
                           comment='Workflow',
                           engine='dot',
                            graph_attr={
                                'label': 'Orthogonal edges',
                                'splines': 'ortho',
                                'nodesep': '1.0',
                                'pad': '1.0'})

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

    # print('>>> Initial action: ', init_action_name)
    # print('>>> initial action id: ', init_action_id)


    dot.node('-1','Início', {'color': 'lightblue', 'shape': 'box', 'style': 'filled'})
    dot.edge('-1',initial_action_target_status_id , xlabel = init_action_name, fontsize='10')


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
        if isinstance(doc['workflow']['common-actions']['action'], list):
            for common_action in doc['workflow']['common-actions']['action']:
                cm_ac_id = common_action['@id']
                cm_ac_name = common_action['@name']
                cm_ac_target= common_action['results']['unconditional-result']['@step']
                cm_ac = Common_transition(cm_ac_id, cm_ac_name, cm_ac_target)
                all_common_actions.append(cm_ac)
        if isinstance(doc['workflow']['common-actions']['action'], dict):
            common_action = doc['workflow']['common-actions']['action']
            cm_ac_id = common_action['@id']
            cm_ac_name = common_action['@name']
            cm_ac_target= common_action['results']['unconditional-result']['@step']
            cm_ac = Common_transition(cm_ac_id, cm_ac_name, cm_ac_target)
            all_common_actions.append(cm_ac)




    # Commom Actions
    for step in doc['workflow']['steps']['step']:
        # print("######################################################")
        # print("Entering the loop ...")
        # print(">> Step name: ", step['@name'])
        if 'actions' in step:
            if 'common-action' in step['actions']:
                # pp(step['actions']['common-action'])
                x = len(step['actions']['common-action'])
                # print(">>>> len(steps['actions']['common-action']) : ", x)
                if x == 1:
                    # print("***************************************************************")
                    # print(">>>> step['actions']['common-action']['@id'] : ", step['actions']['common-action']['@id'])
                    for ca2 in all_common_actions:
                        if ca2.id == step['actions']['common-action']['@id']:
                            # print(">>>>>> common action name : ", ca2.name)
                            dot.edge(step['@id'], ca2.target, xlabel = ca2.name, color = 'yellow', fontsize='10')
                    # print("***************************************************************")
                else:
                    for ca in range(x):
                        # print(">>>>> pp step")
                        # pp(step['actions']['common-action'])
                        # try:
                            # print(">>>>>> pp step ca")
                            # pp(step['actions']['common-action'][ca])
                            # print(">>>>>> end pp step ca")
                        # except BaseException as error:
                            # print("[ERROR] [ERROR] [ERROR] [ERROR] [ERROR]")
                            # print('An exception occurred: {}'.format(error))
                            # continue
                        for ca2 in all_common_actions:
                            # print(">>>>>> ca2.id : ", ca2.id, " ???  ", step['actions']['common-action'][ca]['@id'], " step['actions']['common-action'][ca]['@id']")
                            # print("types comparison")
                            # print(type(ca2.id))
                            # print(type(step['actions']['common-action'][ca]['@id']))
                            if ca2.id == step['actions']['common-action'][ca]['@id']:
                                # print(">>>>>> TRUE !!!! ")
                                # print(">>>>>> ca2.target : ", ca2.target)
                                dot.edge(step['@id'], ca2.target, xlabel = ca2.name, color = 'green', fontsize='10')
        # else:
            # print("There is no common-actions in step: ", step['@name'])

    # Global Actions
    dot.node('0', 'ALL', {'color': 'lightblue', 'shape': 'box', 'style': 'filled'})
    for global_action in all_global_transitions:
        # print('>>> Global action: ', global_action.name)
        for status in all_statuses:
            if status.id == global_action.target_id:
                dot.edge('0', status.id, xlabel = global_action.name, color = 'blue', fontsize = '10')


    def line():
        print("--------------------------------------------------------------------")

    all_single_transitions = []
    for step in doc['workflow']['steps']['step']:
        line()
        print("Entering the loop ...")
        print(">> Step name: ", step['@name'])
        if ('actions' in step) and ('action' in step['actions']):
            print(type(step['actions']['action']))
            if isinstance(step['actions']['action'], dict):
                dot.edge(step['@id'], step['actions']['action']['results']['unconditional-result']['@step'], xlabel = step['actions']['action']['@name'], color = 'red', fontsize='10')
            elif isinstance(step['actions']['action'], list):
                for act in step['actions']['action']:
                    dot.edge(step['@id'], act['results']['unconditional-result']['@step'], xlabel = act['@name'], color = 'purple', fontsize='10')
        else:
            print("There is no single actions in step: ", step['@name'])
        line()



    # for tr in all_single_transitions:
    #     print("##################################")
    #     print('>>>> tr.name: ', tr.name)
    #     print('>>>> tr.id: ', tr.id)
    #     print('>>>> tr.target_id: ', tr.target_id)
    #     print('>>>> tr.current_st_id: ', tr.current_st_id)
    #     dot.edge(tr.current_st_id, tr.target_id, xlabel = tr.name, color = 'red', fontsize = '10')

    # u = w.unflatten(stagger=3)
    # clean the static/images folder (macos will be a problem with files that have the same name)
    shutil.rmtree('./static/images/')
    os.mkdir('./static/images/')
    # end clear1
    dot = dot.unflatten(stagger=4)
    dot.render(directory='./static/images', format='pdf')
    print('filename: ' + dot.filename)
    print('filepath + pdf: ' + dot.filepath+'.pdf')
    return dot.filepath+'.pdf'
