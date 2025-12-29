---
sidebar_position: 4
sidebar_label: Connecting Python Agents
---

# Connecting Python Agents to ROS 2

## 4.1 Setting Up Your Python Development Environment for ROS 2

### Introduction

Python is a widely used language in robotics due to its readability, extensive libraries, and rapid prototyping capabilities. ROS 2 offers excellent support for Python through its `rclpy` client library, making it straightforward to write nodes, publishers, subscribers, services, and actions. This section will guide you through setting up your environment and writing basic Python ROS 2 nodes.

### Topic-by-topic explanation

#### Prerequisites

Before you start writing Python ROS 2 nodes, ensure you have:

1.  **ROS 2 Installed:** Follow the official ROS 2 installation guide for your operating system (e.g., Ubuntu, Windows, macOS). Make sure to source your ROS 2 environment.
    *   **Example (Ubuntu):**
        ```bash
        source /opt/ros/{ROS_DISTRO}/setup.bash
        ```
        (Replace `{ROS_DISTRO}` with your ROS 2 distribution, e.g., `humble`, `iron`, `jazzy`).
2.  **Python 3:** ROS 2 primarily uses Python 3.
3.  **`pip` (Python Package Installer):** Used for managing Python packages.
4.  **`colcon` Build Tool:** ROS 2 uses `colcon` for building packages. It's usually installed with ROS 2, but you might need to install it separately (`pip install colcon-common-extensions`).

#### Creating a ROS 2 Workspace

A ROS 2 workspace is a directory where you develop, build, and install your ROS 2 packages.

1.  **Create a workspace directory:**
    ```bash
    mkdir -p ~/ros2_ws/src
    cd ~/ros2_ws
    ```
2.  **Initialize the workspace:**
    ```bash
    colcon build
    ```
    This command will build any existing packages in the `src` directory and set up the necessary environment files.
3.  **Source the workspace:**
    ```bash
    source install/setup.bash
    ```
    You should source your main ROS 2 installation first, then your workspace `setup.bash` file. It's recommended to add these lines to your `~/.bashrc` (or equivalent shell startup file) for convenience.

### Summary of Section 4.1

Setting up your Python development environment for ROS 2 involves ensuring ROS 2 is installed and sourced, having Python 3 and `pip`, and creating and sourcing a `colcon` workspace. This foundation allows you to begin developing your own Python-based ROS 2 applications.

## 4.2 Writing Your First Python Publisher Node

### Introduction

A publisher node sends messages to a topic. We'll create a simple "talker" node that publishes a "Hello World" message to a topic.

### Topic-by-topic explanation

#### Creating a Python Package

Inside your workspace `src` directory, create a new Python package.

1.  **Create package directory:**
    ```bash
    cd ~/ros2_ws/src
    ros2 pkg create --build-type ament_python my_python_pkg
    cd my_python_pkg
    ```
    This creates a `my_python_pkg` directory with basic package structure including `setup.py` and `package.xml`.

#### The Publisher Code (`talker.py`)

Create a file named `talker.py` inside `my_python_pkg/my_python_pkg/`.

```python
# ~/ros2_ws/src/my_python_pkg/my_python_pkg/talker.py

import rclpy
from rclpy.node import Node
from std_msgs.msg import String # Import the String message type

class Talker(Node):
    def __init__(self):
        super().__init__('talker_node') # Name of the node
        self.publisher_ = self.create_publisher(String, 'chatter', 10) # Topic name 'chatter'
        timer_period = 0.5  # seconds
        self.timer = self.create_timer(timer_period, self.timer_callback)
        self.i = 0
        self.get_logger().info('Talker node has been started and is publishing...')

    def timer_callback(self):
        msg = String()
        msg.data = 'Hello ROS 2 World: %d' % self.i
        self.publisher_.publish(msg)
        self.get_logger().info('Publishing: "%s"' % msg.data)
        self.i += 1

def main(args=None):
    rclpy.init(args=args) # Initialize ROS 2
    talker = Talker()     # Create the node
    rclpy.spin(talker)    # Keep the node alive
    talker.destroy_node() # Destroy node on shutdown
    rclpy.shutdown()      # Shut down ROS 2

if __name__ == '__main__':
    main()
```
*Description:* This Python code defines a `Talker` node that publishes string messages to the `chatter` topic every 0.5 seconds.

#### Modifying `setup.py`

To make your Python script executable as a ROS 2 node, you need to add an entry point in `setup.py`.

```python
# ~/ros2_ws/src/my_python_pkg/setup.py
# ... (existing imports and setup_requires)

entry_points={
    'console_scripts': [
        'talker = my_python_pkg.talker:main', # Add this line
    ],
},
# ... (rest of the setup.py)
```
*Description:* This modification tells `colcon` how to find and run your `talker.py` script as an executable named `talker`.

#### Building Your Package

Navigate to your workspace root and build your package:

```bash
cd ~/ros2_ws
colcon build --packages-select my_python_pkg
```

#### Sourcing and Running the Publisher

After building, source your workspace (if you haven't already in the current terminal) and run the node:

```bash
source install/setup.bash
ros2 run my_python_pkg talker
```

You should see messages being published in your terminal.

### Summary of Section 4.2

Writing a Python publisher node involves creating a ROS 2 Python package, coding the node to import necessary libraries and create a publisher, modifying `setup.py` for executability, building the package, and finally, sourcing and running the node to see its output.

## 4.3 Writing Your First Python Subscriber Node

### Introduction

A subscriber node receives messages from a topic. We'll create a "listener" node that subscribes to the "chatter" topic and prints the messages it receives.

### Topic-by-topic explanation

#### The Subscriber Code (`listener.py`)

Create a file named `listener.py` inside `my_python_pkg/my_python_pkg/`.

```python
# ~/ros2_ws/src/my_python_pkg/my_python_pkg/listener.py

import rclpy
from rclpy.node import Node
from std_msgs.msg import String # Import the String message type

class Listener(Node):
    def __init__(self):
        super().__init__('listener_node') # Name of the node
        self.subscription = self.create_subscription(
            String,
            'chatter', # Topic name 'chatter'
            self.listener_callback,
            10)
        self.subscription  # prevent unused variable warning
        self.get_logger().info('Listener node has been started and is subscribing...')

    def listener_callback(self, msg):
        self.get_logger().info('I heard: "%s"' % msg.data)

def main(args=None):
    rclpy.init(args=args) # Initialize ROS 2
    listener = Listener() # Create the node
    rclpy.spin(listener)  # Keep the node alive
    listener.destroy_node() # Destroy node on shutdown
    rclpy.shutdown()      # Shut down ROS 2

if __name__ == '__main__':
    main()
```
*Description:* This Python code defines a `Listener` node that subscribes to the `chatter` topic and prints each received string message.

#### Modifying `setup.py` (Again)

Add a new entry point for the `listener.py` script in `setup.py`.

```python
# ~/ros2_ws/src/my_python_pkg/setup.py
# ... (existing imports and setup_requires)

entry_points={
    'console_scripts': [
        'talker = my_python_pkg.talker:main',
        'listener = my_python_pkg.listener:main', # Add this new line
    ],
},
# ... (rest of the setup.py)
```

#### Building and Running the Subscriber

Re-build your package (or just the new script if you're comfortable) and then run the listener:

```bash
cd ~/ros2_ws
colcon build --packages-select my_python_pkg

# In a new terminal (after sourcing ROS 2 and workspace)
source install/setup.bash
ros2 run my_python_pkg listener
```

Now, if you run both the `talker` and `listener` nodes in separate terminals (after sourcing the environment in each), you should see the `listener` printing the "Hello ROS 2 World" messages from the `talker`.

### Summary of Section 4.3

Creating a Python subscriber node follows a similar pattern to a publisher: write the Python script using `rclpy` to create a subscription and a callback function, update `setup.py` with the new entry point, build the package, and then run the subscriber node, observing its interaction with the publisher.

## Practical Exercises / Thinking Questions

1.  **Experiment with QoS:** Modify the `talker.py` and `listener.py` examples to use different QoS profiles (e.g., `BEST_EFFORT` vs. `RELIABLE`). Observe how message loss or guaranteed delivery affects the output, especially if you briefly stop and restart the listener.
2.  **Custom Message Exercise:**
    *   Create a `.msg` file for a simple custom message (e.g., `CustomCoord.msg` with `float32 x`, `float32 y`).
    *   Generate a new ROS 2 package for this custom message type.
    *   Create a publisher and subscriber in Python that use your new custom message type.
3.  **Introspection Tools:** Use ROS 2 command-line tools like `ros2 topic list`, `ros2 topic echo /chatter`, and `ros2 node list` while your `talker` and `listener` nodes are running. Explain what each command tells you about your running ROS 2 system.
4.  **Error Handling (Conceptual):** How would you modify the `listener.py` code to handle a scenario where the `chatter` topic suddenly stops publishing for an extended period? What kind of logging or notification would be appropriate?