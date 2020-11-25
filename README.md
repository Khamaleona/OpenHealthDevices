# OpenHealthDevices

Repository created to store code related to Open Health Devices developed with Arduino and Python. This repository contains:

<ul>
  <li>Devices Folder</li>
  <li>questions.json</li>
  <li>sensor-template.txt</li>
  <li>main.py</li>
  <li>tools.py</li>
  <li>uploadGeneration.py</li>
</ul>

<hr>

<h2>Introduction</h2>

In order to make easier the task to build medical devices at home, we have developed this project for those users who are unfamiliar with programming and electronics. Usually, to build such devices we work with <a href="https://www.arduino.cc/en/Guide/Introduction">Arduino</a> components and its own <a href="https://www.arduino.cc/en/Main/Software">IDE</a> to create code files. 

What happens if you are a technological unexperienced user? What happens if you do not know how to program or even build a simple circuit? Don't panic, here we have the solution. The only thing you have to do is follow the instructions. 

<hr>

<h2>Prerequisites</h2>

First of all, you need to install a few elements: <a href="https://www.python.org/downloads/">Python</a> and <a href="https://arduino.github.io/arduino-cli/installation/">Arduino-CLI</a>.

<h3>Python Installation</h3>

<h4>Windows</h4>
The first step is to download the Python installer from its web page. Once we get it, we will execute it by double clicking on it. We just need to follow the installer instructions and check that the "Add Python to PATH" option is activated during the process. 

<h4>Linux</h4>
To do this, we need to execute the following commands:

1) First, we will install essential packages for compiling source code.
<br>```sudo apt install build-essential checkinstall```
<br>```sudo apt install libreadline-gplv2-dev libncursesw5-dev libssl-dev libsqlite3-dev tk-dev libgdbm-dev libc6-dev libbz2-dev libffi-dev zlib1g-dev```

2) Then, we will download the Python 3.9 source code from the official download site. 
<br>```cd /opt``` 
<br>```sudo wget https://www.python.org/ftp/python/3.9.0/Python-3.9.0.tgz```

3) Next, we will extract the downloaded source code and start the installation.
<br>```tar xzf Python-3.9.0.tgz```
<br>```cd Python-3.9.0```
<br>```sudo ./configure --enable-optimizations```

4) Now, everything is ready to install.
<br>```sudo make altinstall```

<h3>Arduino-CLI Installation</h3>

<h4>Windows</h4>
Again, we need to download the executable file from the Downloads web page and unzip it in a folder called "Arduino-CLI". Now, we must add the executable file path to the PATH environment variable. Once it is done, we can verify the installation openning a terminal and typing the arduino-cli command. 

<h4>Linux</h4>
As we did before, we need to run the following command to install Arduino-CLI in Linux systems.

```curl -fsSL https://raw.githubusercontent.com/arduino/arduino-cli/master/install.sh | sh```

Once you have those two installed, we can start the party. 

<hr>

<h2>How it works?</h2>

As you can see, there is a folder called "Devices" where we have added the source code of three devices and a general skeleton (for other sensors):

<ol>
  <li><b>GSR (Galvanic Skin Response) Sensor:</b> It measures the electrical conductance of the skin.</li>
  <li><b>MAX30100: </b>It measures blood preasure and blood oxygen level.</li>
  <li><b>TMP117: </b>It measures the body temperature.</li>
  <li><b>General: </b>It represents the main scheme suitable for every sensor.</li>
</ol>

Inside each sensor folder (we will call them <i>Modules</i>) you will find an image that shows the circuit scheme and the Arduino code file (.ino). Those files contains all the functionality you would need if you wanted to collect their measurements and store them into a web server. What happens if you want a simpler behaviour? Maybe you just want to read the measures and display them. We have already thought about it. 

Remember <b>main.py</b> file we have mentioned before? Here we have implemented everything. Inside each sensor folder, you can find <b>code_sensor.json</b> and <b>questions_sensor.json</b> files. They contain every piece of code necessary to generate your selected sensor. You can execute them using main.py file or codeGeneration.py (it is inside the sensor folder). It will ask you the details of your device and at the end, it will generate the <i>.ino</i> file that we will upload to the board later. These are the steps you need to follow to perform everything successfully:

<ul>
  <li>Open a terminal and run <i>tools.py</i> (you only need to do this the first time).</li>
  <li>If you want to upload code to board, build your circuit and connect them to your computer (here we have used the M5Stick-C board in our examples).</li>
  <li>Finally, run main.py (or sensorGenerator.py) and answer every question as detailed (it will run uploadGeneration.py too).</li>
</ul>

If everything was right, you will have your own medical device. Easy peasy lemon squeezy!

<hr>

<h2>Experimented Users</h2>

As you may have appreciated, we have developed this project based on the implemetation of templates. A template let you create things using an especific structure. Here, we have concieved an Arduino script creator system that uses a set of questions and code blocks to write those scripts following a template (<i>sensor-template.ino</i>). Our system allows users to generate custom files from the examples that we have constructed before. Furthermore, it allows them to generate files for any other type of sensors (users only need to complete them by indicating the type of sensor they will use).

Also, if you want to add a new sensor to our system, it's as simple as appending new code to <b>code.json</b> and <b>questions.json</b>. 
