import json
from pox.core import core
import pox.openflow.libopenflow_01 as of
from pox.lib.packet.ethernet import ethernet
from pox.lib.packet.ipv4 import ipv4
from pox.lib.packet.tcp import tcp
from pox.lib.packet.udp import udp
import os
RULES_FILE = os.path.join(os.path.dirname(__file__), "rules.json")
log = core.getLogger()


def load_rules(path=RULES_FILE):
    try:
        with open(path) as f:
            data = json.load(f)
            log.info(f"Se cargaron {len(data)} reglas desde {path}")
            return data
    except Exception as e:
        log.error(f"Error cargando reglas: {e}")
        return []

class FirewallDNS(object):
    def __init__(self, connection):
        self.connection = connection
        self.mac_to_port = {}
        self.rules = load_rules()
        connection.addListeners(self)

    def match_rule(self, packet):
        """
        Campos admitidos en cada regla:
          - src_mac, dst_mac (strings)
          - dl_type (int: 0x0800 para IPv4)
          - nw_proto (int: 6 TCP, 17 UDP)
          - tp_src, tp_dst (int: puerto de capa transporte)
        """
        eth = packet
        ip = packet.find('ipv4')
        tcp_p = packet.find('tcp')
        udp_p = packet.find('udp')
          
        for r in self.rules:
            # MAC origen
            if 'src_mac' in r and eth.src.toStr() != r['src_mac']:
                continue
            # MAC destino
            if 'dst_mac' in r and eth.dst.toStr() != r['dst_mac']:
                continue
            # EtherType
            if 'dl_type' in r and eth.type != r['dl_type']:
                continue
            # Protocolo IP
            if 'nw_proto' in r:
                if not ip or ip.protocol != r['nw_proto']:
                    continue
            # Puerto de transporte origen
            if 'tp_src' in r:
                if tcp_p and tcp_p.srcport != r['tp_src']:
                    continue
                if udp_p and udp_p.srcport != r['tp_src']:
                    continue
            # Puerto de transporte destino
            if 'tp_dst' in r:
                if tcp_p and tcp_p.dstport != r['tp_dst']:
                    continue
                if udp_p and udp_p.dstport != r['tp_dst']:
                    continue
            log.info(f"Regla aplicada: {r}")
            return True
        return False

    def _handle_PacketIn(self, event):
        packet = event.parsed
        if not packet.parsed:
            log.warning("Paquete no parseado")
            return

        in_port = event.port
        src = packet.src
        dst = packet.dst
        self.mac_to_port[src] = in_port

        # Check firewall rules
        if self.match_rule(packet):
            log.info(f"DROP {src} -> {dst}")
            return  # Descartar paquete

        # Forwarding L2 learning
        if dst in self.mac_to_port:
            out_port = self.mac_to_port[dst]
            msg = of.ofp_packet_out()
            msg.data = event.ofp
            msg.actions.append(of.ofp_action_output(port=out_port))
            msg.in_port = in_port
            self.connection.send(msg)
            log.debug(f"Forward {src}->{dst} via port {out_port}")
        else:
            msg = of.ofp_packet_out()
            msg.data = event.ofp
            msg.actions.append(of.ofp_action_output(port=of.OFPP_FLOOD))
            msg.in_port = in_port
            self.connection.send(msg)
            log.debug(f"Flood {src}->{dst}")


def launch():
    """Inicializa el firewall en cada switch al conectar."""
    def start_switch(event):
        log.info(f"Conexión de switch: {event.connection.dpid}")
        FirewallDNS(event.connection)
    core.openflow.addListenerByName("ConnectionUp", start_switch)
