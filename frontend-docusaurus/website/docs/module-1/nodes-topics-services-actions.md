---
sidebar_position: 3
sidebar_label: Nodes, Topics, Services, Actions
---

# Nodes, Topics, Services, Actions: The ROS 2 Communication Primitives

## 3.1 Understanding Nodes: The Executable Units

### Introduction

In ROS 2, a **Node** is the smallest independent unit of computation. Think of it as a single program that performs a specific task. By breaking down a complex robotic system into many smaller, specialized nodes, developers can achieve modularity, reusability, and easier debugging.

### Topic-by-topic explanation

#### What is a Node?

A node is an executable process that uses the ROS 2 client library (like `rclcpp` for C++ or `rclpy` for Python) to interact with the ROS 2 graph. Each node should ideally be responsible for a single, well-defined function.

*   **Modularity:** Instead of one giant program controlling everything, a robot's intelligence is distributed across many interconnected nodes. For example, one node might be responsible for reading camera data, another for detecting objects, and a third for controlling the robot's movement.
*   **Reusability:** A node developed for one robot might be easily reused on another robot if it performs a generic task (e.g., a PID controller node).
*   **Concurrency:** Multiple nodes can run concurrently, either on the same machine or distributed across different machines, leveraging parallel processing.

**Real-world Example:** Consider a simple mobile robot that needs to avoid obstacles. You might have:
*   A `lidar_driver_node` that reads data from the LiDAR sensor.
*   An `obstacle_detection_node` that processes LiDAR data to identify obstacles.
*   A `velocity_controller_node` that takes commands to move the robot.
*   A `safety_monitor_node` that receives obstacle warnings and overrides movement if necessary.

#### Creating a Simple Node (Conceptual Python Example)

While full code examples are beyond this overview, conceptually, creating a ROS 2 node in Python typically involves:

1.  **Importing `rclpy`:** The ROS 2 Python client library.
2.  **Initializing ROS 2:** Calling `rclpy.init()` to set up the ROS 2 context.
3.  **Creating a Node:** Instantiating `rclpy.node.Node` to create your node.
4.  **Spinning the Node:** Using `rclpy.spin()` to keep the node alive and process callbacks (like incoming messages).
5.  **Shutting down ROS 2:** Calling `rclpy.shutdown()` when the node exits.

```python
import rclpy
from rclpy.node import Node

class MinimalPublisher(Node):
    def __init__(self):
        super().__init__('minimal_publisher')
        # Node setup code goes here, e.g., create publishers/subscribers
        self.get_logger().info('MinimalPublisher Node has been started!')

def main(args=None):
    rclpy.init(args=args)
    minimal_publisher = MinimalPublisher()
    rclpy.spin(minimal_publisher) # Keep node alive
    minimal_publisher.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
```
*Description:* This Python snippet shows the basic structure of a ROS 2 node. It imports the necessary library, initializes ROS 2, creates a node instance, keeps it running, and then shuts down cleanly.

### Summary of Section 3.1

Nodes are the fundamental, modular building blocks of any ROS 2 application. They encapsulate specific functionalities, promoting a distributed and scalable approach to robot software development.

## 3.2 Topics: Asynchronous Data Flow

### Introduction

**Topics** are the most common way for nodes to exchange data in ROS 2. They implement a publish-subscribe communication model, ideal for streaming data where timely delivery of information (like sensor readings) is crucial, and a node might not care if every single message is received by every subscriber.

### Topic-by-topic explanation

#### Publish-Subscribe Model

*   **Publisher:** A node that sends messages to a specific topic. It doesn't need to know if anyone is listening.
*   **Subscriber:** A node that receives messages from a specific topic. It doesn't need to know who is publishing.
*   **Topic Name:** A unique identifier (e.g., `/camera/image_raw`, `/robot/cmd_vel`) that publishers send to and subscribers listen on.

**Key Characteristics:**
*   **Asynchronous:** Publishers send data without waiting for subscribers to acknowledge receipt.
*   **One-to-many communication:** One publisher can send data to multiple subscribers simultaneously.
*   **Decentralized (via DDS):** Publishers and subscribers discover each other directly via the DDS middleware.

**Real-world Example:** Imagine a news channel. The "news channel" is the topic. The "news anchor" is the publisher, broadcasting information. Many "viewers" are subscribers, watching the news without the anchor knowing who they are.

**ASCII Diagram: Topic Communication**

```
+------------+                               +------------+
|  Node A    | --publishes--> /sensor_data --subscribes--> |  Node B    |
| (Publisher)| --------message-----------> | (Subscriber)|
+------------+                               +------------+
      |
      | --publishes--> /sensor_data --subscribes--> +------------+
      |                                           |  Node C    |
      |                                           | (Subscriber)|
      +-------------------------------------------> +------------+
```

*Description:* Node A publishes data to the `/sensor_data` topic. Both Node B and Node C subscribe to `/sensor_data`, receiving the messages published by Node A.

#### Messages and Message Types

Messages are the data structures exchanged over topics. Each topic has an associated message type, which defines the structure and data types of the information it carries. ROS 2 uses `.msg` files to define these types.

*   **Strictly Typed:** Ensures consistency and type safety in communication.
*   **Common Message Types:** ROS 2 provides many standard message types (e.g., `std_msgs`, `sensor_msgs`, `geometry_msgs`).
*   **Custom Messages:** Developers can define their own custom message types if standard ones are insufficient.

**Example Message Definition (Conceptual `MyCustomMessage.msg`)**

```
# MyCustomMessage.msg
std_msgs/Header header
string name
float32 value
int32[] data_array
```

This message type defines a header, a string for a name, a float for a value, and an array of integers.

#### Quality of Service (QoS) Policies for Topics

QoS policies allow you to configure the behavior of topic communication to match the specific needs of your application.

*   **Reliability:**
    *   `BEST_EFFORT`: Messages are sent once; if lost, they are not re-sent. Fast, but unreliable. Good for high-frequency sensor data where missing a few readings is acceptable (e.g., video stream).
    *   `RELIABLE`: Messages are guaranteed to be delivered. Slower, but ensures all messages arrive. Critical for commands (e.g., motor control, emergency stop).
*   **Durability:**
    *   `VOLATILE`: Only sends messages to subscribers that are already connected.
    *   `TRANSIENT_LOCAL`: Stores a history of messages and sends them to new subscribers upon connection. Useful for sharing configuration data or the last known state.
*   **History:**
    *   `KEEP_LAST`: Only keeps the last N messages.
    *   `KEEP_ALL`: Keeps all messages (up to resource limits).
*   **Liveliness:** Defines how a subscriber knows if a publisher is still active.

### Summary of Section 3.2

Topics are the asynchronous backbone for data streaming in ROS 2, enabling flexible one-to-many communication between nodes. With strictly typed messages and configurable QoS policies, topics provide a powerful and adaptable mechanism for handling diverse data flow requirements in robotic systems.

## 3.3 Services: Synchronous Request-Response

### Introduction

While topics are excellent for streaming data, sometimes a node needs to request a specific task from another node and wait for a direct response. This is where **Services** come in. Services provide a synchronous, blocking request-response communication model, similar to a traditional function call.

### Topic-by-topic explanation

#### How Services Work

*   **Service Server:** A node that offers a service and responds to requests.
*   **Service Client:** A node that sends a request to a service server and waits for a response.
*   **Service Type:** Defined by `.srv` files, specifying both the request and response message structures.

**Key Characteristics:**
*   **Synchronous:** The client typically pauses execution until it receives a response from the server.
*   **One-to-one communication:** A client sends a request to a single server instance, and the server sends a response back to that client.
*   **Blocking:** Often used for operations that must complete before the client can proceed.

**Real-world Example:** Think of ordering food at a restaurant. You (client) make a request to the waiter (service server). You wait until the waiter brings your food (response) before you can eat.

**ASCII Diagram: Service Communication**

```
+------------+                  +------------+
|  Node A    | ---request--->   |  Node B    |
| (Client)   |                  | (Server)   |
+------------+                  +------------+
      ^                              |
      |                              | performs computation
      | ---response---               |
      +------------------------------+
```

*Description:* Node A (client) sends a request to Node B (server). Node B performs the requested computation and sends a response back to Node A. Node A typically waits for the response.

#### Defining a Service (Conceptual `AddTwoInts.srv`)

```
# AddTwoInts.srv
int64 a
int64 b
---
int64 sum
```

This service definition specifies that the request part consists of two `int64` numbers (`a` and `b`), and the response part consists of a single `int64` number (`sum`). The `---` separates the request from the response.

### Summary of Section 3.3

Services provide a crucial synchronous request-response mechanism in ROS 2, allowing nodes to perform one-off, blocking calls to other nodes. This is ideal for tasks that require an immediate result before the requesting node can continue its operation.

## 3.4 Actions: Goal-Oriented Tasks with Feedback

### Introduction

For long-running tasks that need continuous feedback on their progress and the ability to be cancelled (preempted), ROS 2 offers **Actions**. Actions are a more complex communication pattern designed for goal-oriented behaviors that extend over time, such as navigating to a distant point or moving a robotic arm.

### Topic-by-topic explanation

#### How Actions Work: Goal, Feedback, Result

Actions are built upon three main parts, defined in a `.action` file:

1.  **Goal:** The initial request sent by the client to the action server, specifying what needs to be done.
2.  **Feedback:** Continuous updates sent by the action server back to the client, indicating the current progress of the long-running task.
3.  **Result:** The final outcome of the action, sent once the task is completed (successfully or not).

**Key Characteristics:**
*   **Asynchronous (with feedback):** The client sends a goal and can continue other tasks while receiving feedback.
*   **Preemptable:** The client can send a request to cancel the goal at any time. The server tries to gracefully stop the execution.
*   **Goal-oriented:** Designed for tasks with a clear objective and a defined completion state.

**Real-world Example:** Consider commanding a robotic arm to pick up an object from a table.
*   **Goal:** "Pick up the red cube."
*   **Feedback:** "Arm moving towards cube...", "Gripper closing...", "Lift 5cm..." (continuous updates on arm position, gripper status).
*   **Result:** "Success: Red cube picked up" or "Failure: Obstacle detected".
*   **Preemption:** If a person walks into the arm's path, you might preempt the "pick up" action immediately.

**ASCII Diagram: Action Communication**

```
+-----------+                   +-------------+
|  Client   | --- Goal -------> |    Server   |
| (Node A)  | <--- Feedback --- |   (Node B)  |
|           | <--- Result ----- |             |
|           | <--- Cancel ----- |             |
+-----------+                   +-------------+
```

*Description:* The Client sends a Goal to the Server. The Server works on the Goal, sending periodic Feedback to the Client. Once done, it sends a Result. The Client can also send a Cancel request to the Server at any time.

#### Defining an Action (Conceptual `MoveRobot.action`)

```
# MoveRobot.action
# Goal
float32 target_x
float32 target_y
---
# Result
bool success
string message
---
# Feedback
float32 current_x
float32 current_y
float32 distance_remaining
```

This action definition specifies the `target_x` and `target_y` coordinates as the goal, a `success` flag and `message` as the result, and `current_x`, `current_y`, `distance_remaining` as continuous feedback during execution.

### Summary of Section 3.4

Actions provide a sophisticated mechanism for handling long-running, goal-oriented tasks in ROS 2. By incorporating goals, continuous feedback, and results, along with preemption capabilities, actions are essential for building responsive and robust behaviors in complex robotic systems like navigation and manipulation.

## Practical Exercises / Thinking Questions

1.  **Communication Method Selection:** For each of the following scenarios, determine whether a ROS 2 Topic, Service, or Action would be the most appropriate communication method, and explain why:
    *   A robot's camera continuously publishing live video frames.
    *   Requesting the robot to turn on its headlights for a brief moment.
    *   Commanding a mobile robot to drive a specific path, providing progress updates, and allowing for emergency stops.
    *   A weather station node providing the current temperature every minute.
    *   Changing a robot's maximum speed parameter.
2.  **Custom Message/Service/Action Design:** You want to create a system for a robot to water plants. Design a custom ROS 2 message, service, or action for this task. Clearly define its purpose and the data types it would involve.
3.  **QoS Impact:** Explain how choosing `BEST_EFFORT` reliability for a topic versus `RELIABLE` reliability might impact a robot's behavior in:
    *   Receiving odometry (position) data from wheels.
    *   Receiving commands to open or close a gripper.
4.  **Node Collaboration:** Describe how two or three different nodes might use a combination of topics, services, and actions to collaborate on a single complex task, such as a robot picking up a specific object. Draw a simple ASCII diagram illustrating their interactions.