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
    ### 2.1 -> Initial actions
    ### 2.2 -> Global Actions
    ### 2.3 -> common actions
    ### 2.4 -> Steps
    ### also, I believe that not every item of the above list above will be present on every workflow
    ### So, I should export other workflows from different versions of Jira and check for the incidence of these 4 items
    ### on the exported workflows.
    ### TODO - update
    ### I was able to create and export a custom workflow that have all the 4 items mentioned above, so, we shold work on this
    #### Getting to work
    #### TODO 2.1 => Extract the initial actions
    ####
    ####
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


