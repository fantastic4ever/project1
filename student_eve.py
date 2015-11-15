from eve import Eve
import sys
import util

def get_student_num_setting(student_num):
	student_setting = util.get_student_setting_template()
	student_setting['DOMAIN'][student_num] = {}
	student_setting['DOMAIN'][student_num]['schema'] = util.get_eve_schema('student')
	student_setting['DOMAIN'][student_num]['additional_lookup'] = {
            'url': 'regex("[\w]+")',
            'field': 'uni'
            }
	return student_setting

if __name__ == '__main__':
	if(len(sys.argv) == 4):
		student_num = 'student' + str(int(sys.argv[3]))
		app = Eve(settings=get_student_num_setting(student_num))
		app.run(host=sys.argv[1], port=int(sys.argv[2]))
