# Flask webapp/API testing application


##### RUN LOCALLY:
* place project folder in <code>/var/www/</code> on *NIX systems
* create/activate a virtual environment in project root
* <code>pip3 install -r requirements.txt</code>
* run <code>python3 bu_app.py</code>
* navigate to http://127.0.0.1:5000


##### DOCKER:
* enter the hostname in the Apache config file, <code>flask_apache.conf</code><br>
* build the Dockerfile from within the project's directory:<br>
<code>docker build -t bu_cicd_example:latest .</code>

* run the container with the webapp:<br>
<code>docker run -d -it -p 80:80 bu_cicd_example</code>

* visit http://&lt;hostname&gt; or http://&lt;hostname&gt;:80 from
a browser or any device's browser on the network


##### RUN TESTS:
from project root execute:<br>
<code>python3 -m pytest -rsA tests/</code>





<hr>
<b>Author: James Loye Colley 2020</b><br>
