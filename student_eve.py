from eve import Eve
import sys
import util

app = Eve(settings=util.get_eve_setting('student', 'current'))

if __name__ == '__main__':
	if(len(sys.argv) == 3):
		app.run(host=sys.argv[1], port=int(sys.argv[2]))
	else:
		app.run()
