# Phase V: Advanced Cloud Native Architecture

## Concept
In Phase V, we evolve the Todo application into an event-driven system using **Kafka** for messaging and **Dapr** for building distributed microservices.

## Architecture
- **Kafka**: Acts as the message broker. When a task is created or completed, an event is published.
- **Dapr (Distributed Application Runtime)**: Simplifies interaction with Kafka and state stores using sidecars.
- **Event Flow**:
  1. User interacts with UI.
  2. Backend Service processes request and publishes a `task-event` to Kafka via Dapr sidecar.
  3. (Optional) A worker service subscribes to `task-event` to perform background processing (e.g., sending reminders).

## Planned Components
- **Dapr Sidecar**: To be added to Kubernetes pods for both Frontend and Backend.
- **Kafka Cluster**: Deployed in Kubernetes or used as a managed service (e.g., Upstash).
- **Pub/Sub Configuration**: `pubsub.yaml` manifest for Dapr to connect to Kafka.

## Acceptance Criteria
- [ ] Application successfully publishes events to a message bus.
- [ ] Dapr sidecars are integrated into the K8s deployment manifests.
- [ ] Scalability: The system can handle asynchronous spikes in task creation.
