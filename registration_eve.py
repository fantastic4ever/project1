from eve import Eve
import sys

app = Eve(settings='registration_settings.py')
 
if __name__ == '__main__':
    if (len(sys.argv) == 3):
    	app.run(host = sys.argv[1], port = int(sys.argv[2]))