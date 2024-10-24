import grpc
from grpc_health.v1 import health_pb2
from grpc_health.v1 import health_pb2_grpc

import sys
import time

if len(sys.argv) != 2:
    raise ValueError(f"Usage: {sys.argv[0]} SERVER_ADDRESS")

_LOG_EVERY_N = 30
_SLEEP_INTERVAL = 0.1

_SERVER = sys.argv[1]

timeout = 5

success = 0
failure = 0
counter = 0

while True:
    counter += 1
    with grpc.insecure_channel(_SERVER) as channel:
        stub = health_pb2_grpc.HealthStub(channel)
        req = health_pb2.HealthCheckRequest(service='')
        try:
            res = stub.Check(req, timeout=timeout)
            success += 1
            if counter % _LOG_EVERY_N == 0:
                print(f'{success=}, {failure=}')
        except grpc.RpcError as ex:
            code, details = ex.code(), ex.details()
            failure += 1
            if counter % _LOG_EVERY_N == 0:
                print(f'{success=}, {failure=}, {code=}, {details=}')
        time.sleep(_SLEEP_INTERVAL)
