#!/usr/bin/env python3
"""Modbus/TCP PLC simulator for the CEH OT range — deliberately UNAUTHENTICATED.

Speaks real Modbus/TCP with no login, no authorization, and no encryption —
exactly like a real PLC on the plant floor. Read holding registers (FC3) and
write them (FC6/FC16) with any client; that missing identity is the whole point.

  ⛔ LAB ONLY. Never point a Modbus client at a device you do not own on an
     isolated bench — a stray write can trip a safety system or damage equipment.

Host/port come from env so the container can bind 0.0.0.0 while a local run can
bind loopback:  MODBUS_HOST=127.0.0.1 MODBUS_PORT=5020 python3 server.py
"""
import os

from pymodbus.datastore import (
    ModbusSequentialDataBlock,
    ModbusServerContext,
    ModbusSlaveContext,
)
from pymodbus.server import StartTcpServer

HOST = os.environ.get("MODBUS_HOST", "0.0.0.0")
PORT = int(os.environ.get("MODBUS_PORT", "5020"))

# 100 registers of "process state" (all coil/register spaces share the block so
# FC1-6/15/16 all work). Start at zero so an FC6 write is an obvious change.
block = ModbusSequentialDataBlock(0, [0] * 100)
store = ModbusSlaveContext(di=block, co=block, ir=block, hr=block)
context = ModbusServerContext(slaves=store, single=True)

if __name__ == "__main__":
    print(f"Modbus/TCP simulator listening on {HOST}:{PORT} (no auth — lab only)",
          flush=True)
    StartTcpServer(context=context, address=(HOST, PORT))
