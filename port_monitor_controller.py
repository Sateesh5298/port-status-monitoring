from ryu.base import app_manager
from ryu.controller import ofp_event
from ryu.controller.handler import MAIN_DISPATCHER, CONFIG_DISPATCHER
from ryu.controller.handler import set_ev_cls
from ryu.ofproto import ofproto_v1_3
import datetime

class PortMonitor(app_manager.RyuApp):
    OFP_VERSIONS = [ofproto_v1_3.OFP_VERSION]

    def __init__(self, *args, **kwargs):
        super(PortMonitor, self).__init__(*args, **kwargs)
        self.port_status = {}

    @set_ev_cls(ofp_event.EventOFPSwitchFeatures, CONFIG_DISPATCHER)
    def switch_features_handler(self, ev):
        print("✅ Switch Connected")

    @set_ev_cls(ofp_event.EventOFPPortStatus, MAIN_DISPATCHER)
    def port_status_handler(self, ev):
        msg = ev.msg
        port_no = msg.desc.port_no

        timestamp = datetime.datetime.now()

        # Detect UP/DOWN
        if msg.desc.state == 0:
            state = "UP"
        else:
            state = "DOWN"

        self.port_status[port_no] = state

        log_msg = f"[{timestamp}] PORT {port_no} {state}"

        print("🚨 ALERT:", log_msg)

        # Save log
        with open("port_status.log", "a") as f:
            f.write(log_msg + "\n")

        # Display status
        print("Current Port Status:")
        for p, s in self.port_status.items():
            print(f"Port {p}: {s}")
