# Flask webapp/API testing application for Openshift


##### RUN LOCALLY:
* place project folder in <code>/opt/app-root/src</code>
* create/activate a virtual environment in project root
* <code>pip3 install -r requirements.txt</code>
* run <code>python3 wsgi.py</code>
* navigate to http://127.0.0.1:5000


##### RUN LOCALLY WITH GUNICORN:
* place project folder in <code>/opt/app-root/src</code>
* create/activate a virtual environment in project root
* <code>pip3 install -r requirements.txt</code>
* <code>gunicorn -c gunicorn_config.py wsgi:application</code>
* navigate to http://0.0.0.0:80


##### RUN TESTS:
from project root execute:<br>
<code>python3 -m pytest -rsA tests/</code>





<hr>
<b>Author: James Loye Colley 2020</b><br>
