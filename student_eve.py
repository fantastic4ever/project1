from eve import Eve
import sys
import student_settings as ss
import json

#app = Eve(settings='student_settings.py')
# with open('student_config.txt', 'w') as outfile:
# 	json.dump(ss.my_settings, outfile)
with open('student_config.txt') as data_file:    
    my_settings = json.load(data_file)
app = Eve(settings=my_settings)

if __name__ == '__main__':
	if(len(sys.argv) == 3):
		app.run(host=sys.argv[1], port=int(sys.argv[2]))
	else:
		app.run()
