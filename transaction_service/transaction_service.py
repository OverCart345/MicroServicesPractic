import grpc
from concurrent import futures
import sqlite3
import uuid
import time
import threading
from flask import Flask, request, Response
import msgpack

from transaction_service.proto import transaction_pb2, transaction_pb2_grpc

class TransactionService:
    def __init__(self):
        self.conn = sqlite3.connect('transactions.db', check_same_thread=False)
        self.create_table()

    def create_table(self):
        c = self.conn.cursor()
        c.execute('''
            CREATE TABLE IF NOT EXISTS transactions (
                transaction_id TEXT PRIMARY KEY,
                user_id TEXT,
                amount REAL,
                currency TEXT,
                type INTEGER,
                category TEXT,
                description TEXT,
                timestamp INTEGER
            )
        ''')
        self.conn.commit()

    def add_transaction(self, user_id, amount, currency, tx_type, category, description, timestamp):
        tx_id = str(uuid.uuid4())
        c = self.conn.cursor()
        c.execute(
            'INSERT INTO transactions VALUES (?, ?, ?, ?, ?, ?, ?, ?)',
            (tx_id, user_id, amount, currency, tx_type, category, description, timestamp)
        )
        self.conn.commit()
        return tx_id

    def list_transactions(self, user_id, from_ts, to_ts):
        c = self.conn.cursor()
        c.execute(
            'SELECT transaction_id, user_id, amount, currency, type, category, description, timestamp '
            'FROM transactions WHERE user_id=? AND timestamp BETWEEN ? AND ?',
            (user_id, from_ts, to_ts)
        )
        return c.fetchall()

class TransactionGRPC(transaction_pb2_grpc.TransactionServiceServicer):
    def __init__(self, service):
        self.service = service

    def AddTransaction(self, request, context):
        tx_id = self.service.add_transaction(
            request.user_id,
            request.amount,
            request.currency,
            request.type,
            request.category,
            request.description,
            request.timestamp
        )
        return transaction_pb2.AddTransactionResponse(transaction_id=tx_id)

    def ListTransactions(self, request, context):
        rows = self.service.list_transactions(request.user_id, request.from_ts, request.to_ts)
        items = []
        for row in rows:
            items.append(transaction_pb2.Transaction(
                transaction_id=row[0],
                user_id=row[1],
                amount=row[2],
                currency=row[3],
                type=row[4],
                category=row[5],
                description=row[6],
                timestamp=row[7]
            ))
        return transaction_pb2.ListResponse(items=items)


def serve_grpc(service):
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    transaction_pb2_grpc.add_TransactionServiceServicer_to_server(TransactionGRPC(service), server)
    server.add_insecure_port('[::]:50052')
    server.start()
    print("Transaction Service (gRPC) started on 50052")
    return server


def serve_http(service):
    app = Flask(__name__)

    @app.route('/mp/tx/add', methods=['POST'])
    def mp_add():
        data = msgpack.unpackb(request.data, raw=False)
        tx_id = service.add_transaction(
            data['user_id'], data['amount'], data['currency'], data['type'], data['category'], data['description'], data['timestamp']
        )
        packed = msgpack.packb({'transaction_id': tx_id}, use_bin_type=True)
        return Response(packed, mimetype='application/msgpack')

    @app.route('/mp/tx/list', methods=['POST'])
    def mp_list():
        data = msgpack.unpackb(request.data, raw=False)
        rows = service.list_transactions(data['user_id'], data['from_ts'], data['to_ts'])
        txs = []
        for row in rows:
            txs.append({
                'transaction_id': row[0],
                'user_id': row[1],
                'amount': row[2],
                'currency': row[3],
                'type': row[4],
                'category': row[5],
                'description': row[6],
                'timestamp': row[7]
            })
        packed = msgpack.packb({'items': txs}, use_bin_type=True)
        return Response(packed, mimetype='application/msgpack')

    app.run(host='0.0.0.0', port=50053)

if __name__ == '__main__':
    service = TransactionService()
    grpc_server = serve_grpc(service)
    http_thread = threading.Thread(target=serve_http, args=(service,))
    http_thread.daemon = True
    http_thread.start()
    grpc_server.wait_for_termination()
