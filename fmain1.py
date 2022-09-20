import xmltodict
import graphviz

def runxml(fname): 
    # with open('wk4.xml') as fd:
    with open(fname) as fd:
        doc = xmltodict.parse(fd.read())

    dot = graphviz.Digraph(comment='Workflow')


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
    initial_action_target_status = init_act['results']['unconditional-result']['@status']


    all_global_transitions = []

    for x in doc['workflow']['global-actions']['action']:
        gl_t_id = x['@id']
        gl_t_name = x['@name']
        gl_t_target_id = x['results']['unconditional-result']['@step']
        gl_t = Global_transition(gl_t_id, gl_t_name, gl_t_target_id)
        all_global_transitions.append(gl_t)


    all_common_actions = []
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
                                        dot.edge(step['@id'], status.id, label = ca2.name)
                                        # dot.edge(step['@name'], status.name, ca2.name)
                                        #print(">>>ca1: ")
                                        #print(ca1)
                                        # print(">>> type(ca1)")
                                        # print(type(ca1))
                                        #print(">>>ca1['@id']: ")
                                        #print(ca1['@id'])
        print("#########################")
        print("#########################")

    # Draw the global actions [IN PROGRESS]
    # Draw a node to represent "ALL" statuses

    dot.node('0', 'ALL', {'color': 'lightblue', 'shape': 'box', 'style': 'filled'})
    for global_action in all_global_transitions:
        print(">>> global_action.id: ")
        print(global_action.id)
        print(">>> global_action.name: ")
        print(global_action.name)
        print(">>> global_action.target_id: ")
        print(global_action.target_id)
        for status in all_statuses:
            if status.id == global_action.target_id:
                dot.edge('0', status.id, label = global_action.name)




    #print("Checking all nodes id's")
    #for x in all_statuses:
    #    print(">>> x.id: ")
    #    print(x.id)


    dot.render(directory='./static/images', format='jpg')  
    print('filename: ' + dot.filename)
    print('filepath + jpg: ' + dot.filepath+'.jpg')
    return dot.filepath+'.jpg'


