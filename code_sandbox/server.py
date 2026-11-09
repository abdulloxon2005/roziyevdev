"""
Sandbox HTTP xizmati (production uchun alohida konteynerda ishga tushiriladi).

    python -m code_sandbox.server --host 0.0.0.0 --port 8080

So'rov:
    POST /run
    Authorization: Bearer <CODE_SANDBOX_TOKEN>
    {"code": "...", "files": {...}, "entry": "main.py", "stdin": "..."}

Javob: executor.run_python() natijasi (JSON).

Faqat standart kutubxona ishlatiladi — konteynerga qo'shimcha paket o'rnatish shart emas.
"""
import argparse
import hmac
import json
import os
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

from .executor import Status, result, run_python

MAX_BODY_BYTES = 512 * 1024
TOKEN = os.environ.get('CODE_SANDBOX_TOKEN', '')


class Handler(BaseHTTPRequestHandler):
    server_version = 'code-sandbox/1.0'

    def _send(self, status_code, payload):
        body = json.dumps(payload, ensure_ascii=False).encode('utf-8')
        self.send_response(status_code)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.send_header('Content-Length', str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, fmt, *args):  # foydalanuvchi kodi loglarga tushmasin
        pass

    def do_GET(self):
        if self.path == '/health':
            return self._send(200, {'status': 'ok'})
        return self._send(404, {'detail': 'not found'})

    def do_POST(self):
        if self.path != '/run':
            return self._send(404, {'detail': 'not found'})
        auth = self.headers.get('Authorization', '')
        expected = f'Bearer {TOKEN}'
        if not TOKEN or not hmac.compare_digest(auth.encode(), expected.encode()):
            return self._send(401, {'detail': 'unauthorized'})
        try:
            length = int(self.headers.get('Content-Length', '0'))
        except ValueError:
            length = 0
        if length <= 0 or length > MAX_BODY_BYTES:
            return self._send(413, result(Status.INVALID, stderr="So'rov hajmi noto'g'ri."))
        try:
            job = json.loads(self.rfile.read(length).decode('utf-8'))
        except (ValueError, UnicodeDecodeError):
            return self._send(400, result(Status.INVALID, stderr="JSON noto'g'ri."))
        if not isinstance(job, dict):
            return self._send(400, result(Status.INVALID, stderr="JSON noto'g'ri."))

        res = run_python(
            job.get('code'),
            files=job.get('files') if isinstance(job.get('files'), dict) else None,
            entry=job.get('entry') or 'main.py',
            stdin=job.get('stdin') or '',
        )
        return self._send(200, res)


def main():
    parser = argparse.ArgumentParser(description='Python code sandbox HTTP service')
    parser.add_argument('--host', default='0.0.0.0')
    parser.add_argument('--port', type=int, default=8080)
    args = parser.parse_args()
    if not TOKEN:
        raise SystemExit('CODE_SANDBOX_TOKEN muhit o\'zgaruvchisi o\'rnatilmagan.')
    httpd = ThreadingHTTPServer((args.host, args.port), Handler)
    httpd.daemon_threads = True
    print(f'code-sandbox listening on {args.host}:{args.port}', flush=True)
    httpd.serve_forever()


if __name__ == '__main__':
    main()
