# "Reproduction of Joint Simon effects for non-human co-actors using the NAO Robot in a cooperative HRI task"

## Table of Content

0. Introduction
1. Hardware Requirements and Prerequisites
2. Software Requirements and Prerequisites
3. Deploying the Software Infrastructure for the Experiment
4. Physical Experiment Setup
5. Subjects
6. Executing the Experiment
7. Results
8. Literature

## Introduction

This experiment is a reproduction of the "Joint Simon effects for non-human co-actors" experiment 
by Stenzel et al. [1] which has also been further reviewed in [2]. In order to reproduce our experiment, 
please read this **guideline carefully** and execute the mentioned steps in the **correct** order. 
The theoretical background is described in the referenced literature.

In this particular study however, we pursue a twofold goal. 

A) we investigate how software intensive robotics experiments can be deployed and executed 
automatically (the software part) by **any** interested researcher. Why?

> The insufficient level of reproducibility of published experimental results has been identified 
as a core issue in the field of robotics in recent years. Why is that? First of
all, robotics focuses on the abstract concept of computation and the creation of 
technological artifacts, i.e., software that implements these concepts. Hence, before 
actually reproducing an experiment, the subject of investigation must be artificially
created, which is non-trivial given the inherent complexity. Second, robotics experiments 
usually include expensive and often customized hardware setups (robots), that are difficult
to operate for non-experts. Finally, there is no agreed upon set of methods in order to setup, 
execute, or (re-)conduct an experiment. To this end, we introduce an interdisciplinary and geographically
distributed collaboration project that aims at implementing good experimental methodology in 
interdisciplinary robotics research with respect to: a) reproducibility of required technical
artifacts, b) explicit and comprehensible experiment design, c) repeatable/reproducible experiment 
execution, and d) reproducible evaluation of obtained experiment data. The ultimate goal of this 
collaboration is to reproduce the same experiment in two different laboratories using the same 
systematic approach. [3]

B) We investigate if we can observe a JSE using a physiologically different robot (from Stenzel's experiment) 
without explicit belief manipulation of the subjects (cf. [2] "biologically inspired" vs. "machine like" robot).

## Step 1: Hardware Requirements and Prerequisites

In case you a not familiar with setting up a network, it might be helpful to ask 
someone in your lab who is experienced to help you setting it up. However, this is
a relatively easy task and hopefully well explained here.

Any recent standard NAO robot platform (acquired within the last 2-3 years) should suffice. 
The software interface to the robot is downward compatible to NAOQi 1.x.x in this experiment.

Furthermore, a recent desktop PC or laptop is required. The PC/laptop requires an
internet connection for our automated software installation &mdash; running the experiment does not 
require internet access.

At least two cpu cores, and 2 GB Ram (4 GB recommended) should suffice. Additionally, 
it is required that the robot and the laptop/PC are connected to the same network. 

We also strongly recommend a **wired** network connection for both, the robot 
and the laptop, you will need two cables. If there is absolutely no chance of establishing 
a wired connection, WiFi will also work. 

However, since WiFi usually introduces a higher latency and instability than a wired connection, 
we disadvise using it.

In order to test if the laptop/PC 'can talk to' the robot, simply plug a network cable
into the NAO (back of the head, open the service hatch first). Startup the laptop and connect
it to the **same** network, either via router or your local network infrastructure. 

As soon as the laptop is up and running, press the robot's chest button (single long press) 
to initiate the boot sequence. This will take a few minutes. When the NAO is ready (startup jingle is over) 
press the chest button of the robot again (single short press). The robot will tell you
its IP address. 

On the laptop/PC you can now ping the robot's IP, check if you get a "pong". 
It is also recommended to leave the power cord of the robot plugged during the experiment.

An example of the network setup is depicted below. Version A depicts a setup using
a dedicated router, Version B depicts a setup that uses the existing local network infrastructure, 
e.g., in your laboratory or office.

<img hspace="20" src="https://github.com/CentralLabFacilities/CentralLabFacilities.github.io/blob/master/images/network_setup_robot.png" width=630px>

In order to check if the network connection works, open a terminal and type:

<pre>
ping ROBOT_IP
</pre>

You should see something like this:

<pre>
ping 192.168.1.199
PING 192.168.1.199 (192.168.1.199) 56(84) bytes of data.
64 bytes from 192.168.1.199: icmp_seq=1 ttl=64 time=0.402 ms
64 bytes from 192.168.1.199: icmp_seq=2 ttl=64 time=0.328 ms
64 bytes from 192.168.1.199: icmp_seq=3 ttl=64 time=0.407 ms
...
</pre>

<img align="left" hspace="20" src="https://github.com/CentralLabFacilities/CentralLabFacilities.github.io/blob/master/images/pepper_cable.jpg" width=300px>
<img src="https://github.com/CentralLabFacilities/CentralLabFacilities.github.io/blob/master/images/pepper_power.jpg" width=300px>

The monitors used to present the stimuli to the robot and the subject (at Bielefeld University) was a 24-inch 
Dell U2412M with an 16:10 IPS panel and a resolution of 1920:1200 @ 60 Hz. The refresh rate of this type is 
8ms (gray to gray). The brightness was set to 100% (for this display type: 300 cd/m²). For this study, it is
important to have the same resolution, i.e., 1920:1200 and a display size of 24 inches.

The exact physical setup will be described later. These are just the prerequisites you need to check/test first.

## Step 2: Software Requirements and Prerequisites

In general, the software for this experiment has been designed and tested on Ubuntu Linux (16.04). 
**That's a prerequisite**. 

In case you a not familiar with Unix-like operating systems it might be helpful to ask 
someone in your lab who is experienced to help you setting up the infrastructure. If you have basic knowledge 
about Unix-like operating systems, the next steps will be a "piece of cake".
 
Download Ubuntu 16.04: https://www.ubuntu.com/download/desktop/contribute?version=16.04.3&architecture=amd64 
and install it on the experiment laptop/PC. Please note: do **not** use the Ubuntu Live version 
(option "Try Ubuntu" in the installer), please **select** "Install Ubuntu option" and proceed as explained 
in the Ubuntu installation routine. 

If you already have a machine with Ubuntu 16.04 installed, that meets the above requirements, check if you 
have sudo permissions, you will need them in the following steps.

Before proceeding installing the experiment software environment, please execute this in a terminal in order 
to get your system up-to-date.

<pre>
sudo apt-get update && sudo apt-get upgrade
sudo apt-get install software-properties-common
sudo apt-add-repository universe
sudo apt-get update && sudo apt-get upgrade
</pre>

When the update process is finished, please proceed. Note: since almost everything in this experiment
is done in a web browser (i.e. experiment installation, execution and orchestration) please use the
**Firefox** web browser that is shipped with Ubuntu &mdash; we verified every feature works with Firefox.

## Step 3: Deploying the Software Infrastructure for the Experiment

###  Step 3a: Bootstrapping the CITK

We are using the CITK [4] to install your experiment software environment. This is how it is bootstrapped.

First of all you will need to install the following dependencies in order to run CITK tools. Open a terminal and run the
command below. Important: in the next steps, make sure you always copy the **complete line**!

<pre>
sudo apt-get install openjdk-8-jdk curl python2.7 python2.7-dev python-setuptools git subversion maven build-essential build-essential cmake
</pre>

Download the jenkins-jse.tar.gz. In the remainder of this tutorial we will work with ~/citk/ as your installation $prefix.

<pre>
mkdir -p $HOME/citk/ && cd $HOME/citk/
wget --no-check-certificate https://ci.toolkit.cit-ec.de/job/jenkins-distribution/lastStableBuild/artifact/jenkins.tar.gz -O jenkins-jse.tar.gz
</pre>

Extract the archive.

<pre>
tar -xzvf jenkins-jse.tar.gz
cd jenkins
</pre>

Once the extraction is done, you need to configure a new user for Jenkins. Please **remember** the user and password, you will need it later!

<pre>
./create_user.sh
</pre>

Follow the required instructions in the terminal. Afterwards, Jenkins can be started as follows.

<pre>
./start_jenkins
</pre>

Now you may open the Jenkins Dashboard by opening https://localhost:8080/?auto_refresh=true in your browser.
Please **accept** the security exception and **add** the certificate.

You should see something similar to the picture below. Please login (top right corner) using the credentials you chose 
when executing the "./create_user" step. **Don't close** the terminal in which your Jenkins is running. 

You are all set for now!

![empty_jenkins](https://toolkit.cit-ec.uni-bielefeld.de/sites/toolkit.cit-ec.uni-bielefeld.de/files/tutorial_jenkins_new.jpg)

### Step 3b: Generate Distribution and Deploy

We are now going to the install all required software components. This includes the software that is required in order 
to control the robot, as well as experiment execution and data acquisition. Yay!

Please open a new terminal and execute the following steps.

<pre>
mkdir -p $HOME/citk/dist && cd $HOME/citk/dist
git clone https://opensource.cit-ec.de/git/citk .
git checkout d6bc5c98cec80aec28cc
</pre>

In the next step please substitute "{YOUR_USERNAME}" and "{YOUR_PASSWORD}" with the credentials you chose in
the "./create_user" step and execute the command line below.

<pre>
$HOME/citk/jenkins/job-configurator --on-error=continue -d $HOME/citk/dist/distributions/remotelab-nightly.distribution -m toolkit -D toolkit.volume=$HOME/citk/systems -u {YOUR_USERNAME} -a {YOUR_PASSWORD}
</pre>

There are two things to carefully check now:

**A)** You should see the following at the _end_ of the console output:

<pre>
START DEPLOY/PROJECT
  0.00 % DEPLOY/PROJECT
  0.00 % DEPLOY/PROJECT: aldebaran-naoqi-sdk-python27
 11.11 % DEPLOY/PROJECT: remotelabservice
 22.22 % DEPLOY/PROJECT: jsp-nao-calibrate
 33.33 % DEPLOY/PROJECT: jspsych
 44.44 % DEPLOY/PROJECT: fsmt
 55.56 % DEPLOY/PROJECT: pyscxml
 66.67 % DEPLOY/PROJECT: fsmt-exp-remotelab
 77.78 % DEPLOY/PROJECT: runnable-remotelab-jsp-nao-calibration
 88.89 % DEPLOY/PROJECT: runnable-remotelab-nao-physical-demo
100.00 % DEPLOY/PROJECT
END   DEPLOY/PROJECT, 4.548 seconds

START ORCHESTRATION
  0.00 % ORCHESTRATION: Configuring orchestration jobs
  0.00 % DEPLOY/VERSION
  0.00 % DEPLOY/VERSION: #VERSION orchestration:orchestration {1006BFE933}
  0.00 % DEPLOY/JOB
  0.00 % DEPLOY/JOB: #JOB orchestration:orchestration:orchestration {1006BFF123}
 33.33 % DEPLOY/JOB: #JOB orchestration:orchestration:prepare-hook/unix {1006C5E5C3}
 66.67 % DEPLOY/JOB: #JOB orchestration:orchestration:finish-hook/unix {1006D9AA63}
100.00 % DEPLOY/JOB
100.00 % DEPLOY/VERSION
100.00 % ORCHESTRATION
END   ORCHESTRATION, 0.875 seconds

START LIST-CREDENTIALS
END   LIST-CREDENTIALS, 0.000 seconds
</pre>

**B)** Please also check the console output for the following (you might need to scroll-up a little). 
If you **don't** see "missing platform dependency" (see below), you are all set.

<pre>
  10 missing platform dependencies:
    python-requests python-sphinx wmctrl libssl-dev libffi-dev libzmq-dev libxml2-dev libxslt1-dev zlib1g-dev python-tk
</pre>

If missing dependencies are reported in the console output you **need to** install them:

<pre>
sudo apt-get install [list of reported packages]
Example: sudo apt-get install python-requests python-sphinx wmctrl libssl-dev libffi-dev libzmq-dev libxml2-dev libxslt1-dev zlib1g-dev python-tk
</pre>

Hint: You can safely ignore other warnings (other mentioned problems). 
In the unlikely case something is wrong in general &mdash; please contact us.

Now, go back to your browser: https://localhost:8080/?auto_refresh=true you should see something similar to the image below:
 
![jenkins_done](https://github.com/CentralLabFacilities/CentralLabFacilities.github.io/blob/master/images/remote_lab_jobs.png)

In order to deploy (install) the entire software system, the **only** thing you need to do is to click the stopwatch icon
next to the build job named:

**"remotelab-nightly-toolkit-orchestration"**

![jenkins_trigger](https://github.com/CentralLabFacilities/CentralLabFacilities.github.io/blob/master/images/trigger_job.png)

The Jenkins will redirect you to another page that displays a dialog "ageLimit ...". Press the _blue_ build button.

![jenkins_age_limit](https://github.com/CentralLabFacilities/CentralLabFacilities.github.io/blob/master/images/age_limit.png)

In general, to get back to the overview page, simply click the top left Jenkins icon. Our CITK toolchain will now install all required software components for you _automagically_. 

You can watch the status, and what is currently being installed, on left side of the Jenkins in the so called
Build Queue

![jenkins_queue](https://github.com/CentralLabFacilities/CentralLabFacilities.github.io/blob/master/images/build_queue.png)

When it's done (can take up to 10 minutes), all except for two, jobs in your Jenkins instance should turn from _grey_
&mdash; haven't been built yet &mdash; to _blue_ &mdash; successfully build & installed. 

NOTE: You only need to install the complete system **once**.

![jenkins_complete](https://github.com/CentralLabFacilities/CentralLabFacilities.github.io/blob/master/images/jenkins_done_complete.png)

There will be  **TWO** grey jobs: 

- a) "runnable-remotelab-jsp-nao-calibration-master-runnable-toolkit-remotelab-nightly" 
- b) "runnable-remotelab-nao-physical-demo-master-runnable-toolkit-remotelab-nightly"

These jobs will be used later on to:

- a) actually **CALIBRATE** the robot 
- b) **RUN** your experiment!

How _cool_ is that? We will now setup the physical part of the experiment.

## Step 4: Physical Experiment Setup

Because two NAOS were available at Bielefeld, a symmetrical setup was originally set up in an otherwise empty office.

Having two NAOs available is not given in every laboratory, thus we will describe a setup using just **one** NAO 
in the following. The setup is easily adjustable by moving the robot from one side to another depending on the chosen 
position (see Step 6) of the subject (human).

<img align="left" hspace="20" src="https://github.com/CentralLabFacilities/CentralLabFacilities.github.io/blob/master/images/pepper_setup_table.jpg" width=300px>
<img src="https://github.com/CentralLabFacilities/CentralLabFacilities.github.io/blob/master/images/pepper_press.jpg" width=300px>

The viewing distance is taken from the original Stenzel paper (approx. 80cm). The NAO kneels next to the participants on 
a table or chair. The barycenter of the robot is approximately at elbow height of a sitting subject.

The participant and the robot each have their own keyboard of _identical_ type. The keyboards are directly adjacent 
(touching) and on the _same level_. 

The posture of the robot's hand above the keyboard is predefined and will be individually set up using a calibration program 
that will be introduced in the next step. Calibration is necessary because there might be differences in the positioning of the 
robot in different lab setups and the angles of the NAO's motors might deviate from robot to robot. The robot's head is turned 
towards the screen to indicate that the robot is looking at it.

## Step 5: Calibration procedure

During calibration, the robot's stiffness **needs to be released**. If the motors are stiff (e.g. arms cannot be moved easily), 
release the stiffness with two short chest button presses.

It is assumed that the robot is powered on and already connected to the network as described in Step 1.
Assuming you set up the experiment exactly as described above you should check the robot's IP one last time. 
You can do this by pressing the chest button, the robot will tell you its IP. Remember the address, e.g., 192.168.1.30. 
Write it down, you will **need it** in the next steps.

During the calibration procedure the arm postures for the key press movement (left and right side), needed in
the experiment, will be recorded and saved.

If you have to move the robot (because, e.g., it is also used by others) you should mark the exact foot
position on the table/chair with tape. Additionally, you have to set the robot to a stable hip-roll position, so 
that it does not fall over. Remember the approximate angle.

During the calibration procedure there are four postures recorded: 

- _prepose_ 
- _safepose_
- _keyrelease_
- _keypress_.

The posture recording is, again, triggered via a so called _build job_ (in the Jenkins browser window) Please, 
switch to the Jenkins in your browser window:
 
https://localhost:8080/?auto_refresh=true

Log in (if not logged in) and trigger the job below by pressing the stopwatch icon next to the job:
 
**"runnable-remotelab-jsp-nao-calibration-master-runnable-toolkit-remotelab-nightly"**

<img src="https://github.com/CentralLabFacilities/CentralLabFacilities.github.io/blob/master/images/calibration_job.png">

Wait a few seconds until a new program/application pops up and follow the instructions that appear in the application 
window. First enter the IP (of your robot!), the port is 9559.

<img src="https://github.com/CentralLabFacilities/CentralLabFacilities.github.io/blob/master/images/calibration_ip.png">

You will be asked if you want to record postures for the left or right arm and then to move the easily moveable 
arms (not stiffened) to the positions as depicted in the application according to your setup.

Please execute the calibration for the left and right arm, i.e., trigger the job two times: 

- 1st time for left arm
- 2nd time for right arm

<img src="https://github.com/CentralLabFacilities/CentralLabFacilities.github.io/blob/master/images/calibration_procedure.png" width=500px>

Great, you are done! Now you can basically run the experiment.

## Step 6: Executing the Experiment

It is assumed that you either just calibrated the robot or, if you resume the experiment from day to day,
set up the NAO exactly like the last time you calibrated, remember: always use, e.g., tape to mark the robots position.

Switch to the Jenkins in your browser (you need to be logged in):

https://localhost:8080/?auto_refresh=true.

Next, trigger the job ...

**"runnable-remotelab-nao-physical-demo-master-runnable-toolkit-remotelab-nightly**"

<img src="https://github.com/CentralLabFacilities/CentralLabFacilities.github.io/blob/master/images/run_experiment.png">

... and enter the IP and port (default: 9559) of the robot in the small popup window and confirm the dialog.

<img src="https://github.com/CentralLabFacilities/CentralLabFacilities.github.io/blob/master/images/run_experiment_config.png">

Now, in another browser window or a new browser tab enter the following address into the address bar, this will load
the actual experiment implemented by utilizing jsPsych [5]: 

http://localhost:5000/

You should see the first experiment setup slide! You don't need to enter anything on this slide, click _submit answers_.

<img src="https://github.com/CentralLabFacilities/CentralLabFacilities.github.io/blob/master/images/study_init_screen.png" width=500px>

On the next slide, you have to choose on which side the robot is kneeling. Choose right or left and &mdash; 
congratulations &mdash; the setup is done! 

<img src="https://github.com/CentralLabFacilities/CentralLabFacilities.github.io/blob/master/images/left_right.png" width=300px>

The robot should stiffen and move the correct arm towards the keyboard. This should be done before the subject enters 
the room or sees the robot.

Now, you can get the subject and start the experiment! Again, the subject should not be present during the setup of the robot.

In general, you don't need to re-run/trigger the experiment build job *per participant*. After each trial the browser 
window will return to its initial state (new subject).

The build job will keep running until you **explicitly** stop it using the "[x]" button next to the running job 
(in the Build Queue), you shut down the Jenkins, you shut down the laptop, or after a maximum of **24 hrs**. 

<img src="https://github.com/CentralLabFacilities/CentralLabFacilities.github.io/blob/master/images/experiment_runs.png" width=300px>

When you're done for the day, you **may** shut down everything. When you continue the next day, you just need to: 

- a) physically setup the NAO (if it has been moved for instance) 
- b) start the Jenkins using the "./start_jenkins" script like you have done it before
- c) trigger the "runnable-remotelab-nao-physical-demo-master-runnable-toolkit-remotelab-nightly" build job
- d) open another tab an go to http://localhost:5000/

Voila, you're all set again.

## Subjects

Subjects were recruited via advertisements that were spread at the nearby campus. The advertisment informed that we invite 
people over 18 years to participate in a co-operational study that takes about 45min and that participation would be 
reimbursed with 8€. 

In order to not bias participants, the robot was not mentioned neither illustrated in the advertisment. Although most 
students were familiar with CITEC-related research and might have anticipated that the study was somehow related to robotics.

### Assignment to Experimental Conditions and Documentation

It is important that equal numbers of participants in total and ideally of males and females are tested per condition 
(left, right). Therefore, the experimenter assigned the participant to a condition in the browser 
(participant sits left or right to the robot) **before** she/he entered the room.

Furthermore, it it important to document how many participants were assigned to each condition and whether they were male 
or female. That's why **lists were prepared in advance** to document the participant's unique id, condition, participant's 
gender, experimenter's name, and further comments to report whether everything went well or whether there were any difficulties.
 
For instance, technical issues or participant- or experimenter-related issues. The assignment of participants to the 
experimental conditions and the documentation of the course of the study is very important. **Please prepare in advance!**

Below you can find an example of a possible documentation and list that you can use as a template.

| Position      | Gender        | UID   | Comment    | Experimenter |
| ------------- |:-------------:| :----:| ----------:| ----------:  |
| left          | male          | abc1  | none       |  Florian     |
| right         | female        | bcd3  | seems tired|  Florian     |
| left          | ...           | ...   | ...        |  ...         |
| right         | ...           | ...   | ...        |  ...         |
| left          | ...           | ...   | ...        |  ...         |


## Procedure

The experiment consists of two parts. First, participants did an interactive task with NAO robot. 
Second, they filled in a survey.

At the beginning, each participant is welcomed to the room where the study takes place (the robot has to be 
prepared **before that**). 

Participants were asked to take seat and to turn off their mobile phone or set it to flight mode. The robot was introduced 
as if it was just another participant, but without further description or details. Participants were told that the 
study instructions would be displayed on the screen when the experiment starts. As described in the previous step, the study 
was initiated (left, right) by the operator during the first setup slides. This resulted in the robot's motors being turned 
on and stiffened. The robot's hand next to the participant moved to the initial position over to the space bar to introduce 
the robot's ability to move to the participant. Participants were asked to follow the instructions on the screen and to contact the 
experimenter in case they had questions or if the experiment was done.

After doing the interactive task, participants were told to contact the experimenter next door and to complete the survey. 
To do so, participants were seated next door and completed an online survey.

After the experiment, participants were informed (debriefed) that the aim of the study was to test the joint simon 
effect with an anthropomorphic robot and all further questions were answered.

## Results

At the end of each trial, the last slide asks you to download the experiment data as a .csv file with the **unique id** 
of the participant as **file name**.

<img src="https://github.com/CentralLabFacilities/CentralLabFacilities.github.io/blob/master/images/download.png">

Please store this file on your computer and regularly **backup your data**! Note the unique id in your
documentation table (see above)!

<img src="https://github.com/CentralLabFacilities/CentralLabFacilities.github.io/blob/master/images/file_download.png">

If you ever forget to store the data or refresh the browser before downloading, you can still download the file 
at the beginning of the next trail.
 
## Literature

- [1] https://www.ncbi.nlm.nih.gov/pubmed/22866762
- [2] http://journal.frontiersin.org/article/10.3389/fpsyg.2014.00974/full
- [3] https://pub.uni-bielefeld.de/publication/2910475
- [4] https://pub.uni-bielefeld.de/publication/2904605
- [5] https://link.springer.com/article/10.3758/s13428-014-0458-y
