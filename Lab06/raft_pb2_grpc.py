# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

import raft_pb2 as raft__pb2


class RaftServiceStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.RequestVote = channel.unary_unary(
                '/RaftService/RequestVote',
                request_serializer=raft__pb2.RequestVoteRequest.SerializeToString,
                response_deserializer=raft__pb2.RequestVoteResponse.FromString,
                )
        self.AppendEntries = channel.unary_unary(
                '/RaftService/AppendEntries',
                request_serializer=raft__pb2.AppendEntriesRequest.SerializeToString,
                response_deserializer=raft__pb2.AppendEntriesResponse.FromString,
                )
        self.GetLeader = channel.unary_unary(
                '/RaftService/GetLeader',
                request_serializer=raft__pb2.GetLeaderRequest.SerializeToString,
                response_deserializer=raft__pb2.GetLeaderResponse.FromString,
                )
        self.Suspend = channel.unary_unary(
                '/RaftService/Suspend',
                request_serializer=raft__pb2.SuspendRequest.SerializeToString,
                response_deserializer=raft__pb2.SuspendResponse.FromString,
                )
        self.SetVal = channel.unary_unary(
                '/RaftService/SetVal',
                request_serializer=raft__pb2.SetValRequest.SerializeToString,
                response_deserializer=raft__pb2.SetValResponse.FromString,
                )
        self.GetVal = channel.unary_unary(
                '/RaftService/GetVal',
                request_serializer=raft__pb2.GetValRequest.SerializeToString,
                response_deserializer=raft__pb2.GetValResponse.FromString,
                )


class RaftServiceServicer(object):
    """Missing associated documentation comment in .proto file."""

    def RequestVote(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def AppendEntries(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetLeader(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def Suspend(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def SetVal(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetVal(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_RaftServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'RequestVote': grpc.unary_unary_rpc_method_handler(
                    servicer.RequestVote,
                    request_deserializer=raft__pb2.RequestVoteRequest.FromString,
                    response_serializer=raft__pb2.RequestVoteResponse.SerializeToString,
            ),
            'AppendEntries': grpc.unary_unary_rpc_method_handler(
                    servicer.AppendEntries,
                    request_deserializer=raft__pb2.AppendEntriesRequest.FromString,
                    response_serializer=raft__pb2.AppendEntriesResponse.SerializeToString,
            ),
            'GetLeader': grpc.unary_unary_rpc_method_handler(
                    servicer.GetLeader,
                    request_deserializer=raft__pb2.GetLeaderRequest.FromString,
                    response_serializer=raft__pb2.GetLeaderResponse.SerializeToString,
            ),
            'Suspend': grpc.unary_unary_rpc_method_handler(
                    servicer.Suspend,
                    request_deserializer=raft__pb2.SuspendRequest.FromString,
                    response_serializer=raft__pb2.SuspendResponse.SerializeToString,
            ),
            'SetVal': grpc.unary_unary_rpc_method_handler(
                    servicer.SetVal,
                    request_deserializer=raft__pb2.SetValRequest.FromString,
                    response_serializer=raft__pb2.SetValResponse.SerializeToString,
            ),
            'GetVal': grpc.unary_unary_rpc_method_handler(
                    servicer.GetVal,
                    request_deserializer=raft__pb2.GetValRequest.FromString,
                    response_serializer=raft__pb2.GetValResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'RaftService', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class RaftService(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def RequestVote(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/RaftService/RequestVote',
            raft__pb2.RequestVoteRequest.SerializeToString,
            raft__pb2.RequestVoteResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def AppendEntries(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/RaftService/AppendEntries',
            raft__pb2.AppendEntriesRequest.SerializeToString,
            raft__pb2.AppendEntriesResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def GetLeader(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/RaftService/GetLeader',
            raft__pb2.GetLeaderRequest.SerializeToString,
            raft__pb2.GetLeaderResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def Suspend(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/RaftService/Suspend',
            raft__pb2.SuspendRequest.SerializeToString,
            raft__pb2.SuspendResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def SetVal(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/RaftService/SetVal',
            raft__pb2.SetValRequest.SerializeToString,
            raft__pb2.SetValResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def GetVal(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/RaftService/GetVal',
            raft__pb2.GetValRequest.SerializeToString,
            raft__pb2.GetValResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
