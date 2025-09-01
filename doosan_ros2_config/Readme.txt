```bash
export ROS2_IP="10.24.x.x"  # if not in .bashrc already
mkdir build && cd build
cmake .. -DROS2_IP=$ROS2_IP  # this generates the xml file for CycloneDDS with the correct network address
sudo cmake --install . --component sysctl_rules  # install sysctl rules for optimized kernel configuration
sudo sysctl --system  # reload kernel configuration
cd ..
source dds/cyclonedds/setup.bash  # add to .bashrc for convenience
```
