import grpc
import data_pb2_grpc as pb2_grpc
import data_pb2 as pb2


class UnaryClient(object):
    """
    Client for gRPC functionality
    """

    def __init__(self):
        self.host = 'localhost'
        self.server_port = 50051

        self.channel = grpc.insecure_channel(
            '{}:{}'.format(self.host, self.server_port))

        self.stub = pb2_grpc.GreeterStub(self.channel)

    def get_url(self, message):
        message = pb2.HelloRequest(name=message)
        print(f'{message}')
        return self.stub.SayHello(message)


if __name__ == '__main__':
    client = UnaryClient()
    result = client.get_url(message="Hello Server you there?")
    print(f'{result}')