# MARS-Programming-Autonomy

This repository shall hold the code running on the NVidia Jetson TX2. The purpose of the code will be to perform high-level evaluations of sensory data, updating its conceptions of the environment around it, planning a trajectory to achieve a goal, and sending commands to the Arduinos to interpret. This will be a catkin workspace, with ROS functioning as the middleware tying all the scripts we write together into a cohesive whole.

## Clone or pull from this repository

Because this repository uses git submodules to link vendor libraries, special care must be taken when cloning or pulling content from it.

To clone this repository:

```bash
git clone --recurse-submodules https://github.com/VolsungaSaga/MARS-Programming-Autonomy
```

To pull updates from this repository:

```bash
git pull --recurse-submodules
```

After either of these actions, you need to pull from each submodule and checkout their master branch

```bash
git submodule foreach "git pull origin master && git checkout master"
```

Or you can `cd` into project root directory and `sh update.sh`.
