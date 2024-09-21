import numpy as np
import os
import re

n1 = 'INPUT'
n2 = 'OUTPUT'


inputs = []
output = []
nodes = []
gates = []


#Opens file\
filename = input('Enter a file name:')

with open(filename, 'r') as file: 
    
    for index, line in enumerate(file):
        left_param = line.find('(')
        right_param = line.find(')')
        
        if n1 in line:
         inputs.append(line[left_param+1])
        elif n2 in line:
         output.append(line[left_param+1])
    
        elif n1 not in line and n2 not in line and line not in ['\n','\r\n']: 
         nodes.append(line)


input_vector = np.array(input)
output_vector = np.array(output)
nodes_vector = np.array(nodes)

inputNode= []
outputNode = []
gateType = []


# Reads the nodes array to detect the outputs, inputs, and gates
for elements in nodes:
  left_param = elements.find('(')
  right_param = elements.find(')')
  equal = elements.find('=')
  space = elements.find(' ')
  comma = elements.find(',')
  
  #print(left_param)
  outputNode.append(elements[0:equal])
  gateType.append(elements[equal:left_param])
  inputNode.append(elements[left_param+1:right_param])

# Prints out the number of inputs, outputs, and nodes
print('Number of Inputs: ', len(inputs))
print('Number of Outputs: ', len(output))
print('Number of Nodes: ', len(nodes))
print('\n')

# Lists out which are the inputs, outputs, and nodes
print('List of Inputs:')
print('\n'.join(map(str, inputs)))
print('\n')
print('List of Outputs:')
print('\n'.join(map(str, output)))
print('\n')
print('List of Gate Nodes: ')  
i = 0
  
for index in nodes:
    comma = index.find(',')
    space = index.find(' ')
  
    outputNode.sort()   
  
    
    print((outputNode[i]),": output of", re.sub('[^A-Za-z0-9]+', '', gateType[i]), "gate, with", len(re.sub('[^A-Za-z0-9]+', '', inputNode[i])),"input(s):", inputNode[i],)
    i = i+1

f = open(filename, 'r')
lines = f.readlines()

print('\n' + '-' * 40 + '\n')

def parse_line(line, inputs, outputs, gates):
    line = line.strip()
  
    
    if line.startswith('INPUT(') and line.endswith(')'):
        inputs[line[6:-1]] = 0  # Level 0 for input nodes
        return
    
    if line.startswith('OUTPUT(') and line.endswith(')'):
        outputs[line[7:-1]] = {}
        return

    if '=' not in line:
        return

    left, right = line.split('=', 1)
    gate_name = left.strip()
    gate_info = right.strip()

    output_wire, remaining = gate_info.split('(', 1)
    remaining = remaining.rstrip(')')
    input_wires = remaining.split(',')

    gate_type = output_wire.strip()
    if len(input_wires) > 1:
        gate_type += f" ({len(input_wires)}-input)"
    
    gates[gate_name] = {
        'output_wire': output_wire.strip(),
        'gate_type': gate_type,
        'input_wires': [x.strip() for x in input_wires],
        'level': -1  # Initialize level as -1
    }


def compute_levels(inputs, gates):
    queue = list(inputs.keys())

  
    while queue:
        current = queue.pop(0)
      
        for gate_name, gate_info in gates.items():
            if current in gate_info['input_wires']:
             
                gate_info['level'] = max(gate_info['level'], inputs[current] + 1)
              
                if gate_info['level'] > inputs.get(gate_name, -1):
                    inputs[gate_name] = gate_info['level']
                 
                    queue.append(gate_name)



inputs = {}
outputs = {}
gates = {}

with open(filename, 'r') as file:
    for line in file:
        parse_line(line, inputs, outputs, gates)

# Compute levels for all gates
compute_levels(inputs, gates)

print("\nInput Node")
for node, level in inputs.items():
    if level == 0:
        print(f"Node {node}: Level 0")

print("\nOutput Nodes")
for node in outputs:
    print(f"Node {node}: Level {inputs.get(node, 'N/A')}")

print("\nGate Nodes")
for gate_name, gate_info in gates.items():
  
    print(f"Output: {gate_name}, Gate Type: {gate_info['gate_type']} Inputs: {', '.join(gate_info['input_wires'])}")
    print(f"Level: {gate_info['level']}\n")
    
