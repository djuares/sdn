from mininet.topo import Topo

class MyTopo(Topo):
    def __init__(self, n=3, **opts):  # Valor por defecto 3
        """Topología en cadena con N switches y hosts en extremos
        
        Args:
            n: número de switches (debe ser >= 2)
        """
        Topo.__init__(self, **opts)
        
        if n < 2:
            raise ValueError("El número de switches debe ser al menos 2")

        # Switches
        switches = []
        for i in range(1, n+1):
            switch = self.addSwitch('s%d' % i)
            switches.append(switch)
        
        # Switches en cadena
        for i in range(n-1):
            self.addLink(switches[i], switches[i+1])
        
        # Hosts en extremos
        h1 = self.addHost('h1')
        h2 = self.addHost('h2')
        h3 = self.addHost('h3')
        h4 = self.addHost('h4')
        
        # Conectar hosts a switches 
        self.addLink(h1, switches[0])
        self.addLink(h2, switches[0])
        self.addLink(h3, switches[-1])
        self.addLink(h4, switches[-1])

topos = {'mytopo': (lambda n=3: MyTopo(n))}

