DevOps Training: Session 1 Comprehensive Report
===============================================

**Subject:** Docker & Kubernetes Architecture, Networking, and Deployment**OS Environment:** Windows (WSL 2)**Session Status:** Completed

Page 1: Executive Summary
-------------------------

This document serves as the comprehensive report and study guide for Session 1 of our DevOps training program. The session successfully transitioned from fundamental containerization concepts using Docker to advanced local Kubernetes orchestration using kind (Kubernetes in Docker).

Crucially, the training progressed beyond surface-level deployment commands into advanced architectural paradigms. We explored the internal Control Plane mechanics, TLS encryption, IP allocation strategies (CNI), and real-world networking routing vulnerabilities.

### Key Milestones Achieved:

1.  Configured a native Linux container environment on Windows using WSL 2.
    
2.  Authored, built, and deployed a custom Python web server image.
    
3.  Pushed the custom image to Docker Hub (Container Registry).
    
4.  Bootstrapped a single-node Kubernetes cluster using kind.
    
5.  Analyzed the internal components of the Kubernetes kube-system namespace.
    
6.  Deployed a declarative YAML manifest utilizing Deployments and various Service types.
    
7.  Investigated advanced networking topologies, IP exhaustion, and security CVEs.
    

Page 2: Part 1 - Containerization with Docker
---------------------------------------------

### 2.1 The Core Concepts

We began by stripping away the complexity of code and focusing on the underlying infrastructure of a container.

*   **Docker Image:** A read-only template or blueprint containing the application code, runtime, libraries, and dependencies (e.g., python:3.11-slim).
    
*   **Docker Container:** A live, running, writable instance of that image.
    

### 2.2 Practical Implementation

We containerized a lightweight Python web server without relying on heavy web frameworks to keep the focus on the containerization process.

**Application Code (app.py):**

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML`   from http.server import SimpleHTTPRequestHandler, HTTPServer  class MyHandler(SimpleHTTPRequestHandler):      def do_GET(self):          self.send_response(200)          self.send_header("Content-type", "text/html")          self.end_headers()          self.wfile.write(b"  Hello World! Docker is working! ===============================  ")  server = HTTPServer(('0.0.0.0', 5000), MyHandler)  server.serve_forever()   `

**Dockerfile Configuration (The Blueprint):**

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML`   FROM python:3.11-slim  WORKDIR /app  COPY app.py .  EXPOSE 5000  CMD ["python", "app.py"]   `

### 2.3 The Docker CLI Pipeline

1.  **Build:** docker build -t my-first-app . (Compiles the Dockerfile into an image).
    
2.  **Run:** docker run -d -p 8080:5000 my-first-app (Maps host port 8080 to container port 5000).
    
3.  **Registry Push:** Authenticated with docker login, tagged the image (docker tag /my-first-app:v1), and pushed it to Docker Hub for global availability.
    

Page 3: Part 2 - Kubernetes (K8s) Orchestration & Control Plane
---------------------------------------------------------------

### 3.1 Cluster Provisioning

The local cluster was provisioned using **kind (Kubernetes IN Docker)** via Docker Desktop.

*   **Why kind?** It is the modern standard over legacy kubeadm single-node setups. It offers faster provisioning and better multi-node simulation using Docker containers to mock physical hardware nodes.
    

### 3.2 Unmasking the System Containers (The Brain of K8s)

By exposing system containers, we analyzed the kube-system namespace components that maintain the cluster's state:

Component

Function

Analogy

**kube-apiserver**

The central gateway. All kubectl commands and internal components communicate strictly through this API via Port 443.

The Receptionist

**etcd**

The highly-available key-value store database containing all cluster state and secrets.

The Vault

**kube-scheduler**

Evaluates node resources (CPU/RAM) and assigns newly created Pods to optimal nodes.

The Seating Host

**kube-controller-manager**

The reconciliation loop that ensures the current cluster state matches the desired state.

The Manager on Duty

**coredns**

Internal DNS server translating Service names to virtual IPs.

The Phonebook

**kube-proxy**

Maintains network routing rules via iptables/IPVS on nodes.

The Traffic Cop

**kindnet (CNI)**

The specific networking plugin deployed by kind to manage Pod IP assignments.

The Plumber

### 3.3 Internal Security & Encryption (mTLS)

*   **The Default 443 Port:** The default kubernetes service runs on port 443 to enforce strict HTTPS encryption.
    
*   **Certificate Authority (CA):** kubeadm dynamically generates a 2048-bit RSA Root CA during cluster creation and signs client certificates for components. Stored locally in /etc/kubernetes/pki/.
    
*   **Authentication:** Pods authenticate using JWT ServiceAccount tokens automatically mounted at /var/run/secrets/kubernetes.io/serviceaccount/.
    

Page 4: Part 3 - Deployments, Services, and IP Management
---------------------------------------------------------

### 4.1 Declarative Deployment

We authored a unified YAML manifest (k8s-manifest.yaml) to deploy the custom Python image with high availability (2 replicas).

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML`   apiVersion: apps/v1  kind: Deployment  metadata:    name: my-python-app  spec:    replicas: 2    selector:      matchLabels:        app: python-web    template:      metadata:        labels:          app: python-web      spec:        containers:        - name: web-container          image: /my-first-app:v1          ports:          - containerPort: 5000   `

### 4.2 Service Types Explored

We iteratively tested multiple routing strategies:

1.  **ClusterIP (Default):** Internal-only routing. Tested initially via kubectl port-forward.
    
2.  **LoadBalancer:** Requests a cloud-provider load balancer. Docker Desktop simulates this locally.
    
3.  **NodePort (30000-32767):** Opens a static port on the physical Node's IP. _Local Constraint noted:_ On Windows kind, the Node's IP is buried in a WSL2 Docker network (e.g., 172.18.x.x).
    

### 4.3 The Origin of IP Pools (CIDR Blocks)

IP addresses in K8s are mathematically divided software-defined networks (SDN).

*   **Source:** Hardcoded RFC 1918 private subnets in the kind source code.
    
*   **Service IPs (10.96.0.0/12):** Assigned by the kube-apiserver upon Service creation.
    
*   **Pod IPs (10.244.0.0/16):** The kube-controller-manager assigns a /24 block to a Node. The CNI (kindnet) then actively assigns individual IPs to Pods from that block.
    

Page 5: Part 4 - Advanced Architecture Case Studies
---------------------------------------------------

Based on our architectural Q&A, here are the real-world scenarios analyzed:

### Case Study A: The Deprecation of externalIPs (CVE-2020-8554)

*   **Scenario:** While configuring the ExternalIP Service YAML, the system flagged the feature as deprecated in K8s v1.36.
    
*   **Analysis:** The externalIPs array is vulnerable to a severe Man-In-The-Middle (MITM) exploit. K8s does not verify IP ownership. In a multi-tenant cluster, a malicious actor can create a service using a victim's IP in the externalIPs field.
    
*   **Outcome:** kube-proxy blindly updates routing rules, hijacking the victim's traffic and routing it to the attacker's pods.
    
*   **Resolution:** The industry has deprecated externalIPs. Modern routing now relies on Cloud Provider LoadBalancers, bare-metal IP managers (like MetalLB), or the new Gateway API.
    

### Case Study B: The Azure AKS VNet Conflict

*   **Scenario:** An enterprise wants to deploy an Azure Kubernetes Service (AKS) cluster utilizing Azure CNI directly into an existing subnet that heavily hosts standard Virtual Machines (VMs).
    
*   **Analysis:** Azure CNI provisions an IP for the node _plus_ pre-allocates IPs for maximum potential Pods (often ~110 per node).
    
*   **Outcome:** Dropping AKS into a shared subnet instantly triggers **IP Exhaustion**. VMs fail to scale, and AKS fails to schedule pods due to a lack of available IP addresses. Furthermore, conflicting Network Security Group (NSG) rules can occur.
    
*   **Resolution:** Kubernetes clusters must always be deployed into dedicated, isolated subnets within the Virtual Network.
    

### Case Study C: Public IPs in the Pod CIDR (Routing Blackholes)

*   **Scenario:** A network engineer mistakenly configures kubeadm to use 8.0.0.0/8 (Public IP space) for the internal Pod network.
    
*   **Analysis:** Google owns 8.8.8.8 (Public DNS). When a container tries to reach the public internet at 8.8.8.8, Kubernetes intercepts the traffic, believing the IP belongs to a local Pod inside the cluster.
    
*   **Outcome:** The traffic drops into a "routing blackhole," severing the cluster's ability to reach critical external internet resources.
    
*   **Resolution:** Always adhere to RFC 1918 Private IP spaces (10.x.x.x, 172.16.x.x, 192.168.x.x) to prevent overlapping with the public WAN.
    

**\[MARKER: END OF SESSION 1\]**