import linkerJSON

t = linkerJSON.Handler('../templates/template.json', '../templates/template2.json')
print( t.data[1] )