************************
Controlling Franka & ROS
************************

Starting ROS to control Franka
==============================

.. TODO decide if we are using this commented section.

.. The image below describes how we plan to control the Arm using Python. To be able to write a successful Python program, we must first understand how ROS works: how to publish and listen on topics.
..
.. .. figure:: _static/franka_programming_interface.png
..     :align: center
..     :figclass: align-center
..
..     Interfacing Python with FRANKA.

Using a single workstation
--------------------------

To use ROS to control the Franka arm from one workstation, you need to have the master node running for ROS. To do this, it can be done in a seperate terminal window (run ``roscore`` in the command line), or from Python with::

  import subprocess
  roscore = subprocess.Popen('roscore')
  time.sleep(1)  # wait a bit to be sure the roscore is really launched

From this point, you can now run the subscriber node.

Networking with other workstations
----------------------------------

Instead of running the master node and subscriber nodes on your own workstation, these can be running on the main workstation in the lab instead. This means that libfranka won't need to be installed on your specific workstation.

To communicate over the lab network you need to change two main ROS variables. Firstly you need to find the IP address of your computer when connected to the lab network (via ethernet). To do this you can use ``ifconfig`` in a terminal window to give you your ``<ip_address_of_pc>``.

You then need to run the following two commands in your terminal window (substitute in you IP address)::

  export ROS_MASTER_URI=http://192.168.0.77:11311
  export ROS_IP=<ip_address_of_pc>

As you will see, this is connecting you to the static IP address of the main Franka workstation, ``192.168.0.77``. In order for you to continue with running a Python publisher, you need to ensure that roscore and the subscriber is running on the main workstation.

.. note:: That this configuration of assigning IP addresses to ROS_MASTER_URI and ROS_IP is non-permanent, and is only active for the terminal window you are working in. This has to be repeated for every window you use to run rospy. Alternatively you can add these commands to your bashrc.

Running the subscriber
======================

Once roscore is running, the subsciber has to run in the background to convert the ros messages into Franka commands and execute. For this, execute the subscriber binary file.

.. warning:: This file is currently only compiled to run with libfranka 0.1.0 (you can check your current libfranka version with ``rosversion libfranka`` in the terminal).

.. tip:: Sometimes there is an '*error with no active exception*' thrown by this executable. This can sometimes be solved by simply manually moving the arm using the buttons.

Using the publisher
===================

.. todo:: Add the information on motion and gripper publishing.

**Example**

Assuming you are writing a script (``script.py``) that wants to use control franka, the files should be stored as::

    .
    ├── README.md
    ├── franka
    │   ├── __init__.py
    │   ├── franka_control_ros.py
    │   ├── franka_controller_sub
    │   ├── franka_controller_sub.cpp
    │   ├── print_joint_positions
    │   └── print_joint_positions.cpp
    └── script.py

To use the ``FrankaRos`` class in your own Python script would look something like this:

.. code-block:: python

   from franka.franka_control_ros import FrankaRos

   franka = FrankaRos(debug_flag=True)
   # we set the flag true to get prints to the console about what FrankaRos is doing

   franka.move_to(x=0.26, y=-0.4, z=0.36, speed=0.1)
   # we tell the arm to go to a specific point in robot space

.. automodule:: franka.franka_control_ros
  :members:
  :undoc-members:

Using Franka without ROS
========================

.. note:: **This method is deprecated**. It is now recommended you use ROS to control the Arm using a Python publisher. It is best you stick with the method detailed above.

Setting Permissions
-------------------

To control the Franka Arm, Fabian and Petar have written a small collection of C++ files which can be compiled to run as executables and control the Franka Arm using libfranka.

You need to ensure you have set the correct permissions for libfranka. You can check that in :ref:`setting-permissions`.

Downloading the C++ Executables and Python Class
------------------------------------------------

Now that you have libfranka set up properly you can get use the C++ files provided. These resources can be found in the ``/franka`` `directory`_ of the repository. Firstly, go to your project directory in the terminal by using ``cd <project_dir>``. If you have already downloaded the files before and are replacing them with an up-to-date version, run ``rm -rf franka/`` first. To download the necessary folder, run::

  svn export https://github.com/nebbles/DE3-ROB1-CHESS/trunk/franka

.. _`directory`: https://github.com/nebbles/DE3-ROB1-CHESS/tree/master/franka

Once this directory is downloaded into your project directory, you need to change directory and then make the binaries executable::

  cd franka/
  chmod a+x franka*
  chmod a-x *.cpp

.. warning::
  This next command will move the FRANKA. **Make sure you have someone in charge of the external activation device (push button)**.

These binaries can now be used from the command line to control the Arm::

  ./franka_move_to_relative <ip_address> <delta_X> <delta_Y> <delta_Z>

Alternatively, you can control the Arm using the easy custom Python class ``Caller`` (see below).

Python-Franka API with ``franka_control.py``
--------------------------------------------

The Python-FRANKA module (``franka_control.py``) is designed to allow easy access to the C++ controller programs provided by Petar. The provided Python module is structured as follows.

.. automodule:: franka.archive.franka_control
  :members:
  :undoc-members:

**Example**

To use the ``FrankaControl`` class in your own Python script would look something like this:

.. code-block:: python

   from franka.franka_control import FrankaControl

   arm = FrankaControl(debug_flag=True)
   # we set the flag true to get prints to the console about what Caller is doing

   arm.move_relative(dx=0.1, dy=0.0, dz=-0.3)
   # we tell teh arm to move down by 30cm and along x away from base by 10cm

.. note::
  This example code assumes you are following the general project structure guide. See below for more information. The code above would be called from a main script such as ``run.py``.

General Structure of Project
----------------------------

The structure of the project is important to ensure that importing between modules works properly and also seperates externally maintained code from your own. An example of a project tree is::

  .
  ├── LICENSE.txt
  ├── README.md
  ├── run.py
  ├── __init__.py
  ├── docs
  │   ├── Makefile
  │   ├── build
  │   ├── make.bat
  │   └── source
  ├── franka
  │   ├── __init__.py
  │   ├── franka_control.py
  │   ├── franka_get_current_position
  │   ├── franka_get_current_position.cpp
  │   ├── franka_move_to_absolute
  │   ├── franka_move_to_absolute.cpp
  │   ├── franka_move_to_relative
  │   └── franka_move_to_relative.cpp
  ├── my_modules
  │   ├── module1.py
  │   ├── module2.py
  │   ├── module3.py
  │   ├── __init__.py
  └── test_script.py

Additional Resources
====================

https://frankaemika.github.io/docs/getting_started.html#operating-the-robot
