import grpc
from grpc_health.v1 import health
from grpc_health.v1 import health_pb2
from grpc_health.v1 import health_pb2_grpc
from grpc_reflection.v1alpha import reflection

from concurrent import futures

import sys

if len(sys.argv) != 2:
    raise ValueError(f"Usage: {sys.argv[0]} SERVER_ADDRESS")

_LISTEN_ADDRESS = sys.argv[1]

_PORT = 50051
_THREAD_POOL_SIZE = 256

server = grpc.server(
    futures.ThreadPoolExecutor(max_workers=_THREAD_POOL_SIZE)
)

server.add_insecure_port(_LISTEN_ADDRESS)

# Create a health check servicer. We use the non-blocking implementation
# to avoid thread starvation.
health_servicer = health.HealthServicer(
    experimental_non_blocking=True,
    experimental_thread_pool=futures.ThreadPoolExecutor(
        max_workers=_THREAD_POOL_SIZE
    ),
)

health_servicer.set("", health_pb2.HealthCheckResponse.SERVING)


health_pb2_grpc.add_HealthServicer_to_server(health_servicer, server)

services = (reflection.SERVICE_NAME, health.SERVICE_NAME)
reflection.enable_server_reflection(services, server)

server.start()
print(f"Listening on {_LISTEN_ADDRESS}")
server.wait_for_termination()
