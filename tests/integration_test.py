#!/usr/bin/env python3
import time, sys, os, json
import grpc
import msgpack
import requests

# Add service modules to path
dir_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(os.path.join(dir_root, 'user_service'))
sys.path.append(os.path.join(dir_root, 'transaction_service'))
sys.path.append(os.path.join(dir_root, 'report_service'))

import user_pb2, user_pb2_grpc
import transaction_pb2, transaction_pb2_grpc
import report_pb2, report_pb2_grpc

# Endpoints
USER_GRPC = 'localhost:50051'
TRANSACTION_GRPC = 'localhost:50052'
TRANSACTION_HTTP_BASE = 'http://localhost:50053/mp/tx'
REPORT_GRPC = 'localhost:50054'


def performance_test_add(n=100):
    user_stub = user_pb2_grpc.UserServiceStub(grpc.insecure_channel(USER_GRPC))
    # ensure user exists
    resp = user_stub.Register(user_pb2.RegisterRequest(username='perf', email=f'perf{int(time.time())}@example.com', password='pass'))
    user_id = resp.user_id

    tx_stub = transaction_pb2_grpc.TransactionServiceStub(grpc.insecure_channel(TRANSACTION_GRPC))
    # gRPC
    start = time.time()
    for i in range(n):
        tx_stub.AddTransaction(transaction_pb2.AddTransactionRequest(
            user_id=user_id, amount=1.0, currency='USD', type=transaction_pb2.TransactionType.INCOME,
            category='test', description='', timestamp=int(time.time())
        ))
    grpc_dur = time.time() - start

    # HTTP/MessagePack
    start = time.time()
    for i in range(n):
        data = {
            'user_id': user_id, 'amount': 1.0, 'currency': 'USD', 'type': 0,
            'category': 'test', 'description': '', 'timestamp': int(time.time())
        }
        requests.post(
            TRANSACTION_HTTP_BASE + '/add',
            data=msgpack.packb(data, use_bin_type=True),
            headers={'Content-Type': 'application/msgpack'}
        )
    mp_dur = time.time() - start

    print(f'Add {n} tx: gRPC={grpc_dur:.3f}s, MsgPack HTTP={mp_dur:.3f}s')
    return user_id


def integration_flow():
    # 1. Registration & login
    user_stub = user_pb2_grpc.UserServiceStub(grpc.insecure_channel(USER_GRPC))
    reg = user_stub.Register(user_pb2.RegisterRequest(username='test', email='test@example.com', password='pass'))
    uid = reg.user_id
    print('Registered user_id:', uid)

    login = user_stub.Login(user_pb2.LoginRequest(email='test@example.com', password='pass'))
    print('Login token length:', len(login.token))

    profile = user_stub.GetProfile(user_pb2.GetProfileRequest(user_id=uid))
    print('Profile:', {'username': profile.username, 'email': profile.email})

    # 2. Add and list transactions via HTTP/MessagePack
    tx_id = transaction_pb2_grpc.TransactionServiceStub(
        grpc.insecure_channel(TRANSACTION_GRPC)
    ).AddTransaction(
        transaction_pb2.AddTransactionRequest(
            user_id=uid, amount=5.5, currency='EUR', type=transaction_pb2.TransactionType.EXPENSE,
            category='food', description='lunch', timestamp=int(time.time())
        )
    ).transaction_id
    print('Added transaction via gRPC, id:', tx_id)

    # HTTP list
    data = {'user_id': uid, 'from_ts': 0, 'to_ts': int(time.time())}
    resp = requests.post(
        TRANSACTION_HTTP_BASE + '/list',
        data=msgpack.packb(data, use_bin_type=True),
        headers={'Content-Type': 'application/msgpack'}
    )
    items = msgpack.unpackb(resp.content, raw=False)['items']
    print('Transactions count via HTTP:', len(items))

    # 3. Report
    rpt = report_pb2_grpc.ReportServiceStub(
        grpc.insecure_channel(REPORT_GRPC)
    )
    gen = rpt.GenerateReport(report_pb2.ReportRequest(user_id=uid, from_ts=0, to_ts=int(time.time())))
    print('Generated report id:', gen.report_id)
    data = rpt.GetReport(report_pb2.GetReportRequest(report_id=gen.report_id))
    payload = json.loads(data.payload)
    print('Report summary:', {k: payload[k] for k in ['total_income', 'total_expense']})


if __name__ == '__main__':
    print('\n--- Integration Flow ---')
    integration_flow()
    print('\n--- Performance Test ---')
    performance_test_add(100)
