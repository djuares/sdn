**1. SDN**
```bash
$ . add_firewall_to_pox.sh firewall.py
$ source poxenv/bin/activate
$ ./pox/pox.py firewall
```

**2. MININET**
```bash
$ sudo mn --custom topologia.py --topo mytopo,n=4 --controller remote --mac --arp
h1 wireshark &
```


**3. PRUEBA DE REGLAS**

***Bloque comunicacion entre 2 hosts***
```bash
pingall
```

***Bloqueo comunicacion TCP al puerto 80***
```bash
h2 iperf -s -p 80 &
h1 iperf -c 10.0.0.2 -p 80
```

***Bloqueo comunicacion TCP al puerto 80***
```bash
h2 iperf -s -u -p 5001 &
h1 iperf -c 10.0.0.2 -u -p 5001
```
