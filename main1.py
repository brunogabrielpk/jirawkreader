import xmltodict
import graphviz
import sys

with open(sys.argv[1]) as fd:  #get the file as a parameter
    doc = xmltodict.parse(fd.read())

dot = graphviz.Digraph(comment='Workflow', format='png', filename=sys.argv[1])
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
    st_target_id =status['actions']['action']['results']['unconditional-result']['@step']
    dot.edge(st_id, st_target_id)

dot.view()



# # Create the object
# dot = graphviz.Graph(comment='Example')

# # add nodes
# dot.node('db1', 'input A', {'color': 'aquamarine'}, style='filled')
# dot.node('db2', 'input B', {'color': 'aquamarine'}, style='filled')
# dot.node('db3', 'input C', {'color': 'aquamarine'}, style='filled')

# dot.node('B', 'transformation', shape='box', style='filled', color='lightblue')
# dot.node('C', 'output', shape='cylinder', style='filled', color='red')

# # add edges
# for n in ['db1', 'db2', 'db3']:
#     dot.edge(n, 'B')

# dot.edge('B', 'C')
