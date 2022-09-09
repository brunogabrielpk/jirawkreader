import xmltodict
import graphviz

def runxml(fname): 
    # with open('wk4.xml') as fd:
    with open(fname) as fd:
        doc = xmltodict.parse(fd.read())

    dot = graphviz.Digraph(comment='Workflow')
    init_action = doc['workflow']['initial-actions']['action']['@name']
    init_target_action = doc['workflow']['initial-actions']['action']['results']['unconditional-result']['@step']
    dot.node(init_action, init_action, {'color': 'lightblue', 'shape': 'box', 'style': 'filled'})
    for status in doc['workflow']['steps']['step']:
        # print(status['@name'])
        st_name = status['@name']
        st_id = status['@id']
        dot.node(st_id, st_name, {'color': 'lightblue', 'shape': 'box', 'style': 'filled'})

    dot.edge(init_action, init_target_action)
    for status in doc['workflow']['steps']['step']:
        st_id = status['@id']
        st_target_id = status['actions']['action']['results']['unconditional-result']['@step']
        label = status['actions']['action']['@name']
        dot.edge(st_id, st_target_id, label = label)

    dot.render(directory='./static/images', format='jpg')  
    print('filename: '+dot.filename)
    print('filepath + jpg: '+dot.filepath+'.jpg')
    return dot.filepath+'.jpg'
