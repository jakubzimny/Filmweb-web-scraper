#!/var/www/html/wsgi/flask/bin/python3
import sys
sys.path.insert(0,"/var/www/html/wsgi")

from fw_stats import app 

if __name__ == "__main__":
    app.run(debug=True)
