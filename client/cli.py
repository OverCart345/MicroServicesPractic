#!/usr/bin/env python3
import click
import grpc
import sys, os, time, json

# Настраиваем пути для protobuf-модулей
BASE_DIR = os.path.dirname(__file__)
sys.path.append(os.path.abspath(os.path.join(BASE_DIR, '../user_service')))
sys.path.append(os.path.abspath(os.path.join(BASE_DIR, '../transaction_service')))
sys.path.append(os.path.abspath(os.path.join(BASE_DIR, '../report_service')))

import user_pb2, user_pb2_grpc
import transaction_pb2, transaction_pb2_grpc
import report_pb2, report_pb2_grpc

# Адреса сервисов
USER_GRPC = os.environ.get('USER_GRPC_URL', 'localhost:50051')
TRANSACTION_GRPC = os.environ.get('TRANSACTION_GRPC_URL', 'localhost:50052')
REPORT_GRPC = os.environ.get('REPORT_GRPC_URL', 'localhost:50054')

@click.group()
def cli():
    """CLI for Microservices App"""
    pass

@cli.command()
@click.option('--username', prompt=True)
@click.option('--email', prompt=True)
@click.option('--password', prompt=True, hide_input=True, confirmation_prompt=True)
def register(username, email, password):
    channel = grpc.insecure_channel(USER_GRPC)
    stub = user_pb2_grpc.UserServiceStub(channel)
    resp = stub.Register(user_pb2.RegisterRequest(username=username, email=email, password=password))
    click.echo(f"Registered user_id: {resp.user_id}")

@cli.command()
@click.option('--email', prompt=True)
@click.option('--password', prompt=True, hide_input=True)
def login(email, password):
    channel = grpc.insecure_channel(USER_GRPC)
    stub = user_pb2_grpc.UserServiceStub(channel)
    resp = stub.Login(user_pb2.LoginRequest(email=email, password=password))
    click.echo(f"Token: {resp.token}")

@cli.command()
@click.option('--user-id', prompt='User ID')
def profile(user_id):
    channel = grpc.insecure_channel(USER_GRPC)
    stub = user_pb2_grpc.UserServiceStub(channel)
    resp = stub.GetProfile(user_pb2.GetProfileRequest(user_id=user_id))
    click.echo(json.dumps({
        'user_id': resp.user_id,
        'username': resp.username,
        'email': resp.email,
        'display_name': resp.display_name,
        'avatar_url': resp.avatar_url,
        'created_at': resp.created_at,
        'updated_at': resp.updated_at
    }, indent=2))

@cli.command()
@click.option('--user-id', prompt='User ID')
@click.option('--amount', prompt=True, type=float)
@click.option('--currency', prompt=True)
@click.option('--type', 'tx_type', prompt=True, type=click.Choice(['INCOME', 'EXPENSE']), default='INCOME')
@click.option('--category', prompt=True)
@click.option('--description', default='')
@click.option('--timestamp', default=lambda: int(time.time()), type=int)
def add_tx(user_id, amount, currency, tx_type, category, description, timestamp):
    channel = grpc.insecure_channel(TRANSACTION_GRPC)
    stub = transaction_pb2_grpc.TransactionServiceStub(channel)
    ttype = transaction_pb2.AddTransactionRequest.Type.Value(tx_type)
    resp = stub.AddTransaction(transaction_pb2.AddTransactionRequest(
        user_id=user_id, amount=amount, currency=currency,
        type=ttype, category=category, description=description, timestamp=timestamp
    ))
    click.echo(f"Transaction ID: {resp.transaction_id}")

@cli.command()
@click.option('--user-id', prompt='User ID')
@click.option('--from-ts', prompt='From timestamp', type=int)
@click.option('--to-ts', prompt='To timestamp', type=int)
def list_tx(user_id, from_ts, to_ts):
    channel = grpc.insecure_channel(TRANSACTION_GRPC)
    stub = transaction_pb2_grpc.TransactionServiceStub(channel)
    resp = stub.ListTransactions(transaction_pb2.ListRequest(user_id=user_id, from_ts=from_ts, to_ts=to_ts))
    out = []
    for tx in resp.items:
        out.append({
            'transaction_id': tx.transaction_id,
            'amount': tx.amount,
            'currency': tx.currency,
            'type': transaction_pb2.Transaction.Type.Name(tx.type),
            'category': tx.category,
            'description': tx.description,
            'timestamp': tx.timestamp
        })
    click.echo(json.dumps(out, indent=2))

@cli.command()
@click.option('--user-id', prompt='User ID')
@click.option('--from-ts', prompt='From timestamp', type=int)
@click.option('--to-ts', prompt='To timestamp', type=int)
def gen_report(user_id, from_ts, to_ts):
    channel = grpc.insecure_channel(REPORT_GRPC)
    stub = report_pb2_grpc.ReportServiceStub(channel)
    resp = stub.GenerateReport(report_pb2.ReportRequest(user_id=user_id, from_ts=from_ts, to_ts=to_ts))
    click.echo(f"Report ID: {resp.report_id}")

@cli.command()
@click.option('--report-id', prompt='Report ID')
def get_report(report_id):
    channel = grpc.insecure_channel(REPORT_GRPC)
    stub = report_pb2_grpc.ReportServiceStub(channel)
    resp = stub.GetReport(report_pb2.GetReportRequest(report_id=report_id))
    data = json.loads(resp.payload)
    click.echo(json.dumps({
        'report_id': resp.report_id,
        'user_id': resp.user_id,
        'generated_at': resp.generated_at,
        'total_income': resp.total_income,
        'total_expense': resp.total_expense,
        'by_category': resp.by_category,
        'payload': data
    }, indent=2))

if __name__ == '__main__':
    cli()
