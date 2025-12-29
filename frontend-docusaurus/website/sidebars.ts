import type {SidebarsConfig} from '@docusaurus/plugin-content-docs';

const sidebars: SidebarsConfig = {
  tutorialSidebar: [
    'intro',
    {
      type: 'category',
      label: 'Module 1: ROS 2 — Robotic Nervous System',
      items: [
        'module-1/what-is-ros-2',
        'module-1/nodes-topics-services-actions',
        'module-1/ros-2-architecture',
        'module-1/connecting-python-agents',
        'module-1/understanding-urdf',
      ],
    },
    {
      type: 'category',
      label: 'Module 2: Digital Twin (Gazebo & Unity)',
      items: [
        'module-2/the-concept-of-a-digital-twin',
        'module-2/physics-in-gazebo',
        'module-2/sensor-simulation',
        'module-2/unity-for-hri',
        'module-2/simulation-vs-real-world',
      ],
    },
    {
      type: 'category',
      label: 'Module 3: NVIDIA Isaac Platform',
      items: [
        'module-3/overview-of-nvidia-isaac',
        'module-3/isaac-sim',
        'module-3/synthetic-data-generation',
        'module-3/isaac-ros',
        'module-3/visual-slam',
        'module-3/nav2',
      ],
    },
    {
      type: 'category',
      label: 'Module 4: Vision-Language-Action (VLA)',
      items: [
        'module-4/what-is-vla',
        'module-4/voice-to-text',
        'module-4/language-to-plan',
        'module-4/plan-to-ros-2-actions',
        'module-4/safety-and-constraints',
      ],
    },
    'capstone',
    'hardware',
  ],
};

export default sidebars;
