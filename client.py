import grpc
import user_pb2
import user_pb2_grpc

channel = grpc.insecure_channel("localhost:50051")
stub = user_pb2_grpc.UserServiceStub(channel)

request = user_pb2.UserRequest(name="Alice")
response = stub.GetUserInfo(request)

print(f"Nome: {response.name}, Idade: {response.age}")