**Title:** Kubernetes Architecture & Networking Targeted Study Guide**Subject:** DevOps / Container Orchestration**Topics:**

*   Containerization Fundamentals
    
*   Kubernetes Control Plane Components
    
*   Network Routing & Security Vulnerabilities
    
*   Node-Level IP Assignment (CNI)
    
*   State Reconciliation (Controllers vs. Schedulers)
    

**Summary:** This study guide is tailored to reinforce core Kubernetes and Docker concepts, with a specialized focus on internal cluster architecture, state management, and network assignment. It clarifies the delegation of responsibilities within the Kubernetes Control Plane—specifically distinguishing between the API gateway, the scheduling mechanics, and the continuous reconciliation loops. Additionally, it highlights node-level network operations, detailing how IP addresses are assigned to individual Pods.

**Key Concepts:**

*   **State Reconciliation (The "Manager" vs. The "Host"):** Understanding the division of labor in the Control Plane is critical. The kube-scheduler is only responsible for evaluating node resources and deciding _where_ a new Pod should be placed. The kube-controller-manager is responsible for constantly monitoring the cluster to ensure the actual state matches the desired state (e.g., noticing a Pod crashed and commanding a replacement to be spun up).
    
*   **IP Address Management (IPAM) Delegation:** While the kube-apiserver acts as the central gateway and assigns virtual IPs to _Services_, it delegates Pod-level networking. The Container Network Interface (CNI) plugin (such as kindnet, Calico, or Flannel) operates on the individual nodes and is actively responsible for handing out specific IP addresses to Pods as they spin up.
    
*   **Internal Cryptography & Security:** Kubernetes operates on a zero-trust model. During initialization, tools like kubeadm mathematically generate a local 2048-bit RSA Root Certificate Authority (CA) to enforce mTLS encryption (via Port 443) for all internal API traffic, eliminating the need for external CAs.
    
*   **Cloud Networking Constraints:** Advanced networking topologies, such as Azure CNI, provision an IP for the node _plus_ pre-allocate a large pool of IPs for potential Pods. Deploying this into a shared, VM-heavy subnet is an anti-pattern that leads to rapid IP exhaustion.
    
*   **Routing Blackholes:** Internal Pod network configurations must strictly use Private IP spaces (RFC 1918). Using Public IP spaces (like 8.0.0.0/8) causes Kubernetes to intercept traffic meant for the actual public internet, dropping it into a routing blackhole.
    

**Vocabulary List:**

*   **kube-controller-manager:** The Control Plane component running continuous reconciliation loops to ensure the current cluster state (e.g., running replicas) matches the desired state declared in your YAML manifests.
    
*   **kube-scheduler:** The component that watches for newly created, unassigned Pods and selects a suitable Node for them to run on based on resource availability.
    
*   **CNI (Container Network Interface):** A standardized framework and set of plugins (like kindnet) that configure network interfaces for Linux containers and assign IP addresses to Pods.
    
*   **etcd:** The highly-available, distributed key-value store that acts as the absolute source of truth and database for all cluster state, configurations, and secrets.
    
*   **NodePort:** A Service type that exposes an application externally by opening a static, designated port (30000-32767) directly on the physical/virtual network interface of every Node in the cluster.
    

**Key Questions:**

*   Question 1: If a Pod crashes and the Deployment requested exactly 3 replicas, which specific Control Plane component detects the missing Pod and commands a new one to be created?
    
*   Question 2: Once a new Pod is commanded to be created, which component decides _which_ Node has enough CPU and RAM to host it?
    
*   Question 3: Why does the kube-apiserver not assign an IP address directly to a newly scheduled Pod, and what component performs this action instead?
    
*   Question 4: Explain why a network administrator must carve out a dedicated, isolated Virtual Network subnet specifically for an AKS cluster utilizing Azure CNI, rather than sharing it with existing Virtual Machines.
    
*   Question 5: What was the fundamental security flaw (CVE-2020-8554) that led to the deprecation of the externalIPs field in Kubernetes Services?