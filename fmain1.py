import xmltodict
import graphviz

def runxml(fname): 
    # with open('wk4.xml') as fd:
    with open(fname) as fd:
        doc = xmltodict.parse(fd.read())

    dot = graphviz.Digraph(comment='Workflow')
    ##################
    ### TODO ###
    ### [DEPRECATED] 1 => Recognize the type of workflow: JSW or JSM
    ### [DEPRECATED] 2 => For each workflow, extract all the statuses and define the inital status
    ### [DEPRECATED] 3 => For each workflow, extract the transitions, the commom ones and the unique to each status
    ### [DEPRECATED] 4 => Build the workflow image
    ##################
    
    ###################
    ### Option 1 -  Identify the workflow Status ###
    ### [DEPRECATED][DONE] - Substep 1 -> create a folder to store examples of workflows
    ### [DEPRECATED] Identify the Workflow type
    #### [DEPRECATED] What differ JSM from JSW workflows ?
    #### [DEPRECATED] the only difference I've noticed (for Jira 9.2 local environment) is the presence of a meta attribute on the
    #### [DEPRECATED] xml file named "gh.version". I was unable to find this meta attribute on the JSM workflow.
    #### [DEPRECATED] Maybe, it worth to consider making a logic that cover both types of workflows.
    #### [DEPRECATED] IF not, proceed with the steps below (treat these step)
    ##### [DEPRECATED] IF workflow == JSW ###
    ###### [DEPRECATED] Extract statuses and initial status
    ###### [DEPRECATED] Extract unique and commom transitions
    ##### [DEPRECATED] IF workflow == JSM ###
    ###### [DEPRECATED] Extract statuses and initial status
    ###### [DEPRECATED] Extract unique and commom transitions
    ### [DEPRECATED] End Option 1 ####
    ###################
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
        def __init__(self, id, name):
            self.id = id
            self.name = name

    class Common_transition:
        def __init__(self, id, name, target):
            self.id = id
            self.name = name
            self.target = target


    print("######### Status Name and Status ID #########")
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
    if len(doc['workflow']['global-actions']):
        gl_t_id = doc['workflow']['global-actions']['action']['@id']
        gl_t_name = doc['workflow']['global-actions']['action']['@name']
        gl_t = Global_transition(gl_t_id, gl_t_name)
        all_global_transitions.append(gl_t)

    print("All-Global-Transition : ")
    print(all_global_transitions)
    print(all_global_transitions[0].id)
    print(all_global_transitions[0].name)


    ##### [TODO] - Test, if possible, with workflow that has multiple Global-Actions
    ### 2.3 => [TODO] Extract commom actions/transitions

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


