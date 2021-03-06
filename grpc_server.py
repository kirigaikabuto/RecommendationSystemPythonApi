import data_pb2_grpc
import data_pb2
from concurrent import futures
import grpc
from app import getCollaborativeFilteringRecommendation, getContentBasedRecommendations, \
    getSpecialContentBasedRecommendations


class Greeter(data_pb2_grpc.GreeterServicer):

    def CollaborativeRecommendation(self, request, context):
        elements = getCollaborativeFilteringRecommendation(request.userId, request.movieId,
                                                           getContentBasedRecommendations(request.movieId,
                                                                                          count=request.count))
        return data_pb2.ReqResponse(movies=elements)

    def ContentBasedRecommendation(self, request, context):
        elements = getSpecialContentBasedRecommendations(request.movieId, count=request.count)
        return data_pb2.ReqResponse(movies=elements)


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    data_pb2_grpc.add_GreeterServicer_to_server(Greeter(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    serve()
