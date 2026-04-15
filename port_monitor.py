from pox.core import core
import pox.openflow.libopenflow_01 as of
import datetime

log = core.getLogger()

port_status = {}

def _handle_ConnectionUp(event):
    log.info("✅ Switch Connected")

def _handle_PortStatus(event):
    port = event.ofp.desc.port_no
    timestamp = datetime.datetime.now()

    # Detect UP/DOWN
    if event.ofp.desc.state == 0:
        state = "UP"
    else:
        state = "DOWN"

    port_status[port] = state

    msg = f"[{timestamp}] 🚨 PORT {port} {state}"

    print(msg)

    # Log to file
    with open("port_status.log", "a") as f:
        f.write(msg + "\n")

    # Display all ports
    print("Current Status:")
    for p, s in port_status.items():
        print(f"Port {p}: {s}")

def launch():
    core.openflow.addListenerByName("ConnectionUp", _handle_ConnectionUp)
    core.openflow.addListenerByName("PortStatus", _handle_PortStatus)
