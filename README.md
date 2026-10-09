# 🌐 Software-Defined Network (SDN) & Custom Firewall

> Implementation of a Software-Defined Networking (SDN) environment using Mininet, OpenFlow, and a custom POX controller with integrated JSON-based firewall filtering rules.

---

## 🚀 About the Project
This project simulates a programmable network topology to evaluate control and data plane behaviors. It features a custom SDN controller built on POX that enforces granular security policies through dynamic, JSON-defined filtering rules, validated via real-time traffic analysis using Wireshark.

## 🛠️ Tech Stack
* **Simulation:** Mininet
* **Controller:** POX (OpenFlow Protocol)
* **Configuration:** JSON (Firewall rules)
* **Testing & Analysis:** Iperf, Wireshark, Bash

---

## ⚙️ Getting Started & Execution

Follow these steps to set up and run the simulation locally.

**1. Start the SDN Controller (POX)**
```bash
$ . add_firewall_to_pox.sh firewall.py
$ source poxenv/bin/activate
$ ./pox/pox.py firewall
```

**2. Launch the Mininet Topology**
```bash
$ sudo mn --custom topologia.py --topo mytopo,n=4 --controller remote --mac --arp
h1 wireshark &
```


**3. Testing & Validation**

***Test 1: General Connectivity***
```bash
pingall
```

***Test 2: TCP Traffic Blocking (Port 80)***
```bash
h2 iperf -s -p 80 &
h1 iperf -c 10.0.0.2 -p 80
```

***Test 3: UDP Traffic Blocking (Port 5001)***
```bash
h2 iperf -s -u -p 5001 &
h1 iperf -c 10.0.0.2 -u -p 5001
```
