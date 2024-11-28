# syntax=docker/dockerfile:1
FROM osrf/ros:humble-desktop-full

# create a regular user, switch to it, cd to its home
RUN useradd -ms /bin/bash user
RUN adduser user sudo
RUN echo 'user:user' | chpasswd
RUN echo '%sudo ALL=(ALL) NOPASSWD:ALL' >> /etc/sudoers
USER user

# otherwise autocompletion is broken with apt
RUN sudo rm /etc/apt/apt.conf.d/docker-clean

# install useful sw
RUN sudo apt-get update && sudo apt-get install -y \
    vim  \ 
    nano \
    wget \
    bash-completion \
    iputils-ping \
    libxcb-cursor-dev \
    openssh-client \
    gedit \
    cmake-curses-gui \
    gitg git-gui \
    clang \
    locate \
    gdb \
    meld \
    nautilus \
    && sudo rm -rf /var/lib/apt/lists/*


# XBot deps
RUN sudo apt-get update && sudo apt-get install -y \
    ros-humble-srdfdom \
    ros-humble-geometric-shapes \
    ros-humble-moveit-msgs \
    && sudo rm -rf /var/lib/apt/lists/*


#install xbot binaries TODO


# Clone Doosan model
RUN mkdir -p ~/ws/src && \
    cd ws/src && \
    git clone https://github.com/magician-project/iit-doosan-ros-pkg $$ \
    cd .. && colcon build

WORKDIR /home/user

SHELL [ "/bin/bash", "-ic" ]



# source ros and xbot
RUN echo source /opt/ros/$ROS_DISTRO/setup.bash >> /home/user/.bashrc
RUN echo source /opt/xbot/setup.bash >> /home/user/.bashrc

# ros2 configuration (cyclonedds, custom sysctl rules, ...)
#RUN echo "export RMW_IMPLEMENTATION=rmw_cyclonedds_cpp" >> /home/user/.bashrc

CMD ["/bin/bash"]