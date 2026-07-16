# Modbus/TCP PLC simulator for the CEH OT range.
# pymodbus is pinned so the datastore/server API stays stable across rebuilds.
FROM python:3.12-slim

RUN pip install --no-cache-dir "pymodbus==3.6.9"

COPY server.py /server.py

EXPOSE 5020
CMD ["python", "/server.py"]
