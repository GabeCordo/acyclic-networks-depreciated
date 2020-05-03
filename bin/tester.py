from pynodetor.utils import linkerJSON

t = linkerJSON.Handler('../templates/index.json', '../templates/log.json')
print( t.data[0] )