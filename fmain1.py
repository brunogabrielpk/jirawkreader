import xmltodict
import graphviz

def runxml(fname): 
    # with open('wk4.xml') as fd:
    with open(fname) as fd:
        doc = xmltodict.parse(fd.read())

    dot = graphviz.Digraph(comment='Workflow')
    ##################
    ### Option 2 - treat both types of workflows as one thing, so I'll need to extract all info
    ### regardless of the type
    ### For now, I believe that are 4 types of information present on the workflows
    ### [DONE] 2.1 -> Initial actions
    ### 2.2 -> Global Actions
    ### 2.3 -> common actions
    ### 2.4 -> Steps
    ### also, I believe that not every item of the above list above will be present on every workflow
    ### So, I should export other workflows from different versions of Jira and check for the incidence of these 4 items
    ### on the exported workflows.
    ### TODO - update
    ### I was able to create and export a custom workflow that have all the 4 items mentioned above, so, we shold work on this
    #### Getting to work...
    #### [DONE] Extracting and drawing all status of the workflow
    class Statuses:
        def __init__(self, id, name):
            self.id = id
            self.name = name

    class Global_transition:
        def __init__(self, id, name, target_status_name):
            self.id = id
            self.name = name
            self.target = target_status_name

    class Common_transition:
        def __init__(self, id, name, target):
            self.id = id
            self.name = name
            self.target = target


    print("######### Status Name and Status ID #########")
    # all status of the workflow
    all_statuses = []
    for status in doc['workflow']['steps']['step']:
        #print(status['@name'])
        st_name = status['@name']
        st_id = status['@id']
        st = Statuses(st_id, st_name)
        all_statuses.append(st)
        dot.node(st_id, st_name, {'color': 'lightblue', 'shape': 'box', 'style': 'filled'})


    for x in all_statuses:
        print("Status name: "+ x.name+" , Status id: "+ x.id)
    #### [DONE] 2.1 => Extract the initial actions
    init_act = doc['workflow']['initial-actions']['action']
    init_action_id = init_act['@id']
    init_action_name = init_act['@name']
    initial_action_target_status = init_act['results']['unconditional-result']['@status']

    print('######### INITIAL ACTIONS#########')
    print('Initial Action ID: ' + init_action_id)
    print('Initial Action Name: ' + init_action_name)
    print('Initial actions target status: ' + initial_action_target_status)

    ##### [TODO] - Test, if possible, with workflow that has multiple initial actions
    #### 2.2 => Extract the global actions
    print("##### Global actions #####")
    # print(doc['workflow']['global-actions']['action']['@id'])
    all_global_transitions = []

    print("All global actions struct")
    print(all_global_transitions)
    print("doc['workflow']['global-actions']) length: ")
    print(len(doc['workflow']['global-actions']))
    for x in doc['workflow']['global-actions']['action']:
        print('x : ')
        print(x['@id'])
        print(x['@name'])
        gl_t_id = x['@id']
        gl_t_name = x['@name']
        print(x['results']['unconditional-result']['@status'])
        # gl_tg_st_id = x['results']['unconditional-result']['@status']
        # gl_t_tg_st_name = all_statuses[gl_tg_st_id].name
        # gl_t = Global_transition(gl_t_id, gl_t_name)
        # all_global_transitions.append(gl_t)

    print("All-Global-Transition : ")
    print(all_global_transitions)
    for item in all_global_transitions:
        print("Global transition id: " + item.id)
        print("Global transition name: " + item.name)
        print("Global transition target status: " + item.target)
    ### 2.2 => [TODO] draw the global actions
    ### 2.3 => [IN PROGRESS] Extract commom actions/transitions
    all_common_actions = []
    for common_action in doc['workflow']['common-actions']['action']:
        cm_ac_id = common_action['@id']
        cm_ac_name = common_action['@name']
        cm_ac_target= common_action['results']['unconditional-result']['@step']
        cm_ac = Common_transition(cm_ac_id, cm_ac_name, cm_ac_target)
        all_common_actions.append(cm_ac)

    print("All common actions (below):")
    print(all_common_actions)
    print("Loop trough common actions list:")
    for ca in all_common_actions:
        print(ca.id)
        print(ca.name)
        print(ca.target)

    ### 2.4 => Extract and draw common actions (transitions) per statuses
    for status in all_statuses:
        print("Status: " + status.name)
        for step in doc['workflow']['steps']['step']:
            if status.id == step['@id']:
                # print("Steoin the 'workflow >> steps' loop: ")
                # print(step)
                print("step >> actions")
                print(step['actions'])

    ### End Option 2
    ###################
    ### OLD code ###
    # init_action = doc['workflow']['initial-actions']['action']['@name']
    # init_target_action = doc['workflow']['initial-actions']['action']['results']['unconditional-result']['@step']
    # dot.node(init_action, init_action, {'color': 'lightblue', 'shape': 'box', 'style': 'filled'})

    # for status in doc['workflow']['steps']['step']:
    #     # print(status['@name'])
    #     st_name = status['@name']
    #     st_id = status['@id']
    #     dot.node(st_id, st_name, {'color': 'lightblue', 'shape': 'box', 'style': 'filled'})

    # dot.edge(init_action, init_target_action)
    # for status in doc['workflow']['steps']['step']:
    #     st_id = status['@id']
    #     st_target_id = status['actions']['action']['results']['unconditional-result']['@step']
    #     label = status['actions']['action']['@name']
    #     dot.edge(st_id, st_target_id, label = label)
    ## End Old Code ###
    ###################
    dot.render(directory='./static/images', format='jpg')  
    print('filename: ' + dot.filename)
    print('filepath + jpg: ' + dot.filepath+'.jpg')
    return dot.filepath+'.jpg'


