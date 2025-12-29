---
sidebar_position: 2
sidebar_label: ROS 2 Architecture
---

# ROS 2 Architecture

## 2.1 The Pillars of ROS 2 Architecture

### Introduction

Understanding the architecture of ROS 2 is crucial for developing robust and scalable robotic applications. Unlike ROS 1's master-slave communication model, ROS 2 adopts a decentralized, distributed architecture based on DDS (Data Distribution Service). This fundamental shift provides enhanced real-time capabilities, improved security, and better support for multi-robot systems and diverse operating environments.

### Topic-by-topic explanation

#### Data Distribution Service (DDS) - The Communication Backbone

At the heart of ROS 2's architecture is the **Data Distribution Service (DDS)**. DDS is an open international standard for publish-subscribe communication, designed for real-time systems. It manages all communication between nodes in ROS 2, eliminating the need for a central master.

*   **Decentralized Discovery:** Nodes (DDS Participants) automatically discover each other without a central broker. This improves robustness and scalability.
*   **Quality of Service (QoS) Policies:** DDS allows fine-grained control over communication parameters, such as reliability, durability, and liveliness, critical for real-time applications.
    *   **Reliability:** Guarantees message delivery, even if network conditions are poor.
    *   **Durability:** Ensures subscribers receive data even if they join after a publisher has started sending messages.
    *   **Liveliness:** Detects if a publisher or subscriber is still active.
*   **Transport Flexibility:** DDS abstracts the underlying transport layer, allowing ROS 2 to work over various network types (UDP, TCP, shared memory) and even different DDS implementations (e.g., Fast RTPS, Cyclone DDS).

**Real-world Example:** Imagine a swarm of delivery drones. Each drone needs to communicate its position and status to other drones and a central command. With DDS, each drone can publish its status, and other drones can subscribe. If one drone's communication temporarily drops, DDS QoS can ensure that critical messages are resent or that others are aware of its absence without a central server coordinating everything.

#### ROS 2 Client Libraries (RCL)

The ROS 2 Client Libraries (RCL) provide the APIs that developers use to write ROS 2 applications in various programming languages (e.g., `rclcpp` for C++, `rclpy` for Python). These libraries act as an interface between your application code and the underlying DDS implementation.

*   **Abstraction Layer:** RCL abstracts away the complexities of DDS, allowing developers to focus on robot logic rather than low-level communication protocols.
*   **Language Bindings:** Provides idiomatic interfaces for common ROS 2 concepts (nodes, topics, services, actions) in different languages.
*   **Consistent API:** Ensures a consistent programming model across various programming languages.

**ASCII Diagram: ROS 2 Layered Architecture**

```
+------------------------------------+
|        ROS 2 Application Code      |
|  (Your Nodes: C++, Python, etc.)  |
+------------------------------------+
|          ROS 2 Client Libraries (RCL)        |
|    (e.g., rclcpp, rclpy - language-specific)  |
+------------------------------------+
|    ROS Middleware Interface (RMW)  |
|    (Abstracts DDS implementations) |
+------------------------------------+
|      Data Distribution Service (DDS)       |
|    (e.g., Fast RTPS, Cyclone DDS)  |
+------------------------------------+
|           Operating System         |
|      (Linux, Windows, macOS, RTOS) |
+------------------------------------+
|              Hardware              |
+------------------------------------+
```

*Description:* This diagram shows the layered architecture of ROS 2. Your application code interacts with RCL, which uses RMW to interface with the chosen DDS implementation, which in turn communicates over the operating system and hardware. This modularity allows different layers to be swapped out without affecting others.

#### ROS Middleware Interface (RMW)

The ROS Middleware Interface (RMW) is another crucial abstraction layer in ROS 2. It sits between the ROS client libraries (RCL) and the specific DDS implementation.

*   **Middleware Agnostic:** RMW allows you to switch between different DDS vendors (e.g., Fast RTPS, Cyclone DDS) without changing your application code. This is vital for flexibility and tailoring performance to specific use cases.
*   **Pluggable Design:** Different RMW implementations exist for different DDS vendors, enabling a truly plug-and-play middleware.

### Summary of Section 2.1

The ROS 2 architecture is built upon the robust, decentralized Data Distribution Service (DDS) for communication, abstracting its complexities through the ROS Client Libraries (RCL) and the ROS Middleware Interface (RMW). This layered design provides flexibility, real-time capabilities, and enhanced security, making ROS 2 suitable for a wide range of modern robotic applications across various platforms.

## 2.2 Core Concepts within ROS 2 Architecture

### Introduction

Beyond the communication backbone, ROS 2 introduces and refines several core concepts that empower developers to build sophisticated robotic systems.

### Topic-by-topic explanation

#### Nodes: The Building Blocks

Just like in ROS 1, **Nodes** are the fundamental computational units in ROS 2. Each node is an executable program that performs a specific task.

*   **Independence:** Nodes operate independently but collaborate by communicating.
*   **Modularity:** Promotes breaking down complex robot behaviors into smaller, manageable, and reusable components.
*   **Example:** A camera driver node, an object detection node, a motor control node.

#### Topics: Asynchronous Data Streaming

**Topics** are named buses over which nodes exchange messages asynchronously. This is the primary mechanism for streaming data in ROS 2.

*   **Publish-Subscribe Model:** One node "publishes" messages to a topic, and any number of other nodes can "subscribe" to that topic to receive the messages.
*   **Data Types:** Messages exchanged over topics have defined data types (e.g., `sensor_msgs/msg/Image`, `geometry_msgs/msg/Twist`).
*   **QoS Profiles:** Each topic communication can have specific QoS settings (reliability, durability, history, etc.) tailored to its needs. For example, a camera image topic might prioritize speed (best-effort QoS) over guaranteed delivery, while a robot's emergency stop command topic would prioritize guaranteed delivery (reliable QoS).

**Real-world Example:** A robot's LiDAR sensor node publishes laser scan data to a `/scan` topic. A navigation node subscribes to this `/scan` topic to build a map and avoid obstacles.

#### Services: Synchronous Request/Response

**Services** provide a synchronous request/response mechanism between nodes. When one node (the client) needs a specific task performed by another node (the server) and expects a direct result, it uses a service.

*   **Blocking Call:** The client node typically blocks until it receives a response or a timeout occurs.
*   **Defined Request/Response Types:** Services have clearly defined request and response message types.
*   **Example:** A client node might request a server node to "GetMap" and wait for the map data as a response.

#### Actions: Long-Running Goal-Oriented Tasks

**Actions** are a new concept in ROS 2 (building upon similar ideas in ROS 1) designed for long-running, goal-oriented tasks that provide continuous feedback and can be preempted.

*   **Goal, Feedback, Result:** An action consists of a Goal (what you want to achieve), Feedback (updates on the progress), and a Result (the final outcome).
*   **Preemptable:** A client can cancel an ongoing action if needed.
*   **Example:** A robot arm moving to a specific pose. The client sends a goal (target pose), receives feedback (current arm position), and gets a result (success/failure). If an obstacle appears, the client can preempt the action.

#### Parameters: Dynamic Configuration

**Parameters** allow nodes to expose configurable values that can be changed dynamically at runtime, or configured before startup.

*   **Key-Value Pairs:** Parameters are typically key-value pairs (e.g., `camera_node.exposure_time = 0.01`).
*   **Dynamic Reconfiguration:** Parameters can be updated while a node is running, allowing for real-time tuning without restarting the node.

#### Node Lifecycles: Managed States

ROS 2 introduces **Managed Nodes** with defined **Lifecycles**, allowing for more robust and predictable system management. Nodes can transition through various states (e.g., `unconfigured`, `inactive`, `active`, `finalized`).

*   **Predictable Behavior:** Ensures components are initialized and finalized in a controlled manner.
*   **Error Handling:** Provides mechanisms to gracefully handle errors and transition to safe states.
*   **Example:** A node might start in `unconfigured`, then `configure()` to `inactive`, then `activate()` to `active` to start processing data.

### Summary of Section 2.2

ROS 2's architecture encompasses nodes for modularity, topics for asynchronous data streaming with configurable QoS, services for synchronous request/response, and actions for long-running, preemptable tasks. Parameters enable dynamic configuration, while node lifecycles provide robust state management, all contributing to a highly flexible and reliable framework for complex robotic systems.

## Practical Exercises / Thinking Questions

1.  **DDS in Action:** Research one specific DDS QoS policy (e.g., `History`, `Deadline`, `Liveliness`). Explain what it does, why it's important, and provide a robotic use case where it would be critical.
2.  **Service vs. Action:** You need to implement a function for your robot:
    *   Reading the current battery level.
    *   Navigating to a goal location across a room, providing updates during the movement.
    Which ROS 2 communication mechanism (Topic, Service, or Action) would you use for each, and why?
3.  **Designing a Node:** Imagine you are building a simple "Obstacle Avoidance" node for a mobile robot. What kind of inputs (topics, services, parameters) would this node likely subscribe to or use? What outputs (topics, services, actions) would it provide?
4.  **RMW vs. RCL:** Explain in your own words the difference between the ROS 2 Client Library (RCL) and the ROS Middleware Interface (RMW). Why is having both beneficial for the ROS 2 ecosystem?