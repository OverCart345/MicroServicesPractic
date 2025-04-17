import grpc
from concurrent import futures
import sqlite3
import uuid
import time
import json
import requests
import msgpack
import os

from report_service.proto import report_pb2, report_pb2_grpc

TRANSACTION_HTTP_URL = os.environ.get("TRANSACTION_HTTP_URL", "http://localhost:50053")

class ReportServiceImpl(report_pb2_grpc.ReportServiceServicer):
    def __init__(self):
        self.conn = sqlite3.connect('reports.db', check_same_thread=False)
        self.create_table()

    def create_table(self):
        c = self.conn.cursor()
        c.execute('''
            CREATE TABLE IF NOT EXISTS reports (
                report_id TEXT PRIMARY KEY,
                user_id TEXT,
                generated_at INTEGER,
                from_ts INTEGER,
                to_ts INTEGER,
                total_income REAL,
                total_expense REAL,
                by_category TEXT,
                payload BLOB
            )
        ''')
        self.conn.commit()

    def GenerateReport(self, request, context):
        user_id, from_ts, to_ts = request.user_id, request.from_ts, request.to_ts
        data = {'user_id': user_id, 'from_ts': from_ts, 'to_ts': to_ts}
        res = requests.post(
            f"{TRANSACTION_HTTP_URL}/mp/tx/list",
            data=msgpack.packb(data, use_bin_type=True),
            headers={'Content-Type': 'application/msgpack'}
        )
        items = msgpack.unpackb(res.content, raw=False)['items']
        total_income = total_expense = 0
        by_category = {}
        for tx in items:
            amt = tx['amount']
            typ = tx['type']
            cat = tx['category']
            if typ == 0:
                total_income += amt
            else:
                total_expense += amt
            by_category[cat] = by_category.get(cat, 0) + amt
        report_id = str(uuid.uuid4())
        generated_at = int(time.time())
        payload_dict = {
            'user_id': user_id,
            'from_ts': from_ts,
            'to_ts': to_ts,
            'total_income': total_income,
            'total_expense': total_expense,
            'by_category': by_category
        }
        payload_bytes = json.dumps(payload_dict).encode()
        c = self.conn.cursor()
        c.execute('INSERT INTO reports VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)',
                  (report_id, user_id, generated_at, from_ts, to_ts,
                   total_income, total_expense, json.dumps(by_category), payload_bytes))
        self.conn.commit()
        return report_pb2.ReportResponse(report_id=report_id)

    def GetReport(self, request, context):
        c = self.conn.cursor()
        c.execute(
            'SELECT user_id, generated_at, total_income, total_expense, by_category, payload '
            'FROM reports WHERE report_id=?', (request.report_id,)
        )
        row = c.fetchone()
        if not row:
            context.abort(grpc.StatusCode.NOT_FOUND, "Report not found")
        user_id, generated_at, total_income, total_expense, by_category_json, payload = row
        by_category = json.loads(by_category_json)
        return report_pb2.ReportData(
            report_id=request.report_id,
            user_id=user_id,
            generated_at=generated_at,
            total_income=total_income,
            total_expense=total_expense,
            by_category=by_category,
            payload=payload
        )

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    report_pb2_grpc.add_ReportServiceServicer_to_server(ReportServiceImpl(), server)
    server.add_insecure_port('[::]:50054')
    server.start()
    print("Report Service (gRPC) started on 50054")
    server.wait_for_termination()

if __name__ == "__main__":
    serve()
