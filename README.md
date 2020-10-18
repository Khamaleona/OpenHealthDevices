# OpenHealthDevices

Repository created to store code related to Open Health Devices developed with Arduino and Python. This repository contains:

<ul>
  <li>Examples Folder</li>
  <li>code.json</li>
  <li>questions.json</li>
  <li>sensor-template.ino</li>
  <li>sensorGenerator.py</li>
  <li>tools.py</li>
  <li>uploadGeneration.py</li>
</ul>

<hr>

<h2>Introduction</h2>

In order to make easier the task to build medical devices at home, we have developed this project for those users who are unfamiliar with programming and electronics. Usually, to build such devices we work with <a href="https://www.arduino.cc/en/Guide/Introduction">Arduino</a> components and its own <a href="https://www.arduino.cc/en/Main/Software">IDE</a> to create code files. 

What happens if you are a technological unexperienced user? What happens if you do not know how to program or even build a simple circuit? Don't panic, here we have the solution. 

We have written three Python scripts that will help you, the only thing you have to do is follow the instructions. 

<hr>

<h2>Prerequisites</h2>

First of all, you need to install a few elements, but do not worry, it will be easy. 

<ul>
  <li><a href="https://www.python.org/downloads/">Python</a></li>
  <li><a href="https://arduino.github.io/arduino-cli/installation/">Arduino-CLI</a></li>
</ul>

Once you have those two, we can start the party. 

<hr>

<h2>How it works?</h2>

As you can see, there is a folder called "Examples" where we have added the source code of three devices:

<ol>
  <li><b>GSR (Galvanic Skin Response) Sensor:</b> It measures the electrical conductance of the skin.</li>
  <li><b>MAX30100: </b>It measures blood preasure and blood oxygen level.</li>
  <li><b>TMP117: </b>It measures the body temperature.</li>
</ol>

Inside each sensor folder you will find an image that shows the circuit scheme and the Arduino code file (.ino). Those files contains all the functionality you would need if you wanted to collect their measurements and store them into a web server. What happens if you want a simpler behaviour? Maybe you just want to read the measures and display them. We have already thought about it. 

Remember <b>sensorGenerator.py</b> file we have mentioned before? Here we have implemented everything. Using <b>code.json</b> and <b>questions.json</b> files it will ask you the details of your device and at the end, it will generate the <i>.ino</i> file that we will upload to the board later. These are the steps you need to follow to perform everything successfully:

<ul>
  <li>Open a terminal and run <i>tools.py</i> (you only need to do this the first time).</li>
  <li>If you want to upload code to board, build your circuit and connect them to your computer (here we have used the M5Stick-C board in our examples).</li>
  <li>Finally, run sensorGenerator.py and answer every question as detailed (it will run uploadGeneration.py too).</li>
</ul>

If everything was right, you will have your own medical device. Easy peasy lemon squeezy!

<hr>

<h2>Experimented Users</h2>

As you may have appreciated, we have developed this project based on the implemetation of templates. A template let you create things using an especific structure. Here, we have concieved an Arduino script creator system that uses a set of questions and code blocks to write those scripts following a template (<i>sensor-template.ino</i>). Our system allows users to generate custom files from the examples that we have constructed before. Furthermore, it allows them to generate files for any other type of sensors (users only need to complete them by indicating the type of sensor they will use).

Also, if you want to add a new sensor to our system, it's as simple as appending new code to <b>code.json</b> and <b>questions.json</b>. 
