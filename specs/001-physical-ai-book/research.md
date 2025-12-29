# Research for Physical AI & Humanoid Robotics Book

This document records the research and decisions made to resolve the "NEEDS CLARIFICATION" items from the implementation plan.

## 1. Testing Frameworks

### Decision

- **Frontend (Docusaurus/React)**: Jest and React Testing Library.
- **Backend (FastAPI)**: Pytest.

### Rationale

- **Jest and React Testing Library**: These are the industry standard for testing React applications. They are well-documented, have a large community, and integrate well with Docusaurus.
- **Pytest**: Pytest is the most popular testing framework for Python. It has a simple syntax, powerful features, and a rich ecosystem of plugins that work well with FastAPI.

### Alternatives Considered

- **Frontend**: Mocha, Chai, Enzyme. These are also good options, but Jest and React Testing Library are more commonly used with modern React.
- **Backend**: Unittest. Unittest is part of the Python standard library, but Pytest is generally considered more powerful and easier to use.

## 2. Performance Goals

### Decision

- **Chatbot**:
    - p95 latency for a response should be under 3 seconds.
    - The system should handle at least 10 concurrent users without significant degradation in performance.
- **Translation**:
    - p95 latency for a chapter translation should be under 5 seconds.

### Rationale

- These goals are a reasonable starting point for a good user experience. They are ambitious enough to ensure a responsive system, but not so strict that they will be impossible to achieve with the chosen technology stack. These goals can be revisited and adjusted as the project progresses.

### Alternatives Considered

- Stricter performance goals were considered, but it was decided to start with these and iterate. Less strict goals were also considered, but this might lead to a poor user experience.
