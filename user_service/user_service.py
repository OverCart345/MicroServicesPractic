import grpc
from concurrent import futures
import time
import uuid
import sqlite3
import bcrypt
import jwt
import os

import user_pb2
import user_pb2_grpc

SECRET_KEY = os.environ.get("SECRET_KEY", "secret")

class UserService(user_pb2_grpc.UserServiceServicer):
    def __init__(self):
        self.conn = sqlite3.connect('users.db', check_same_thread=False)
        self.create_table()

    def create_table(self):
        c = self.conn.cursor()
        c.execute('''
            CREATE TABLE IF NOT EXISTS users (
                user_id TEXT PRIMARY KEY,
                username TEXT,
                email TEXT UNIQUE,
                password_hash TEXT,
                display_name TEXT,
                avatar_url TEXT,
                created_at INTEGER,
                updated_at INTEGER
            )
        ''')
        self.conn.commit()

    def Register(self, request, context):
        user_id = str(uuid.uuid4())
        hashed = bcrypt.hashpw(request.password.encode(), bcrypt.gensalt())
        ts = int(time.time())
        try:
            self.conn.execute(
                'INSERT INTO users VALUES (?, ?, ?, ?, ?, ?, ?, ?)',
                (user_id, request.username, request.email, hashed.decode(), request.username, "", ts, ts)
            )
            self.conn.commit()
        except sqlite3.IntegrityError:
            context.abort(grpc.StatusCode.ALREADY_EXISTS, "Email already registered")
        return user_pb2.RegisterResponse(user_id=user_id)

    def Login(self, request, context):
        c = self.conn.cursor()
        c.execute('SELECT user_id, password_hash FROM users WHERE email=?', (request.email,))
        row = c.fetchone()
        if not row or not bcrypt.checkpw(request.password.encode(), row[1].encode()):
            context.abort(grpc.StatusCode.UNAUTHENTICATED, "Invalid credentials")
        token = jwt.encode({"user_id": row[0], "iat": int(time.time())}, SECRET_KEY, algorithm="HS256")
        return user_pb2.LoginResponse(token=token)

    def GetProfile(self, request, context):
        c = self.conn.cursor()
        c.execute(
            'SELECT user_id, username, email, display_name, avatar_url, created_at, updated_at FROM users WHERE user_id=?',
            (request.user_id,)
        )
        row = c.fetchone()
        if not row:
            context.abort(grpc.StatusCode.NOT_FOUND, "User not found")
        return user_pb2.UserProfile(
            user_id=row[0], username=row[1], email=row[2],
            display_name=row[3], avatar_url=row[4], created_at=row[5], updated_at=row[6]
        )

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    user_pb2_grpc.add_UserServiceServicer_to_server(UserService(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    print("User Service (gRPC) started on 50051")
    server.wait_for_termination()

if __name__ == '__main__':
    serve()
