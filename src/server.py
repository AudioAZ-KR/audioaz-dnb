#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""d&b System Designer 로컬 앱 서버 — designer.html UI 제공 + /generate 로 .dbpr 직접 생성."""
import http.server, socketserver, json, os, socket, threading, webbrowser, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import arraycalc_gen as gen

RES = os.path.dirname(os.path.abspath(__file__))

class H(http.server.SimpleHTTPRequestHandler):
    def __init__(self,*a,**k): super().__init__(*a, directory=RES, **k)
    def log_message(self,*a): pass
    def do_GET(self):
        if self.path in ('/','','/designer.html','/index.html'):
            # 아티팩트 플랫폼이 붙여주던 HTML 스켈레톤(+UTF-8 charset)을 로컬에서도 붙여 한글 깨짐 방지
            try:
                html=open(os.path.join(RES,'designer.html'),encoding='utf-8').read()
            except Exception as e:
                self.send_error(500,str(e)); return
            page=('<!doctype html><html lang="ko"><head><meta charset="utf-8">'
                  '<meta name="viewport" content="width=device-width,initial-scale=1">'
                  '<title>d&b System Designer</title>'
                  '<style>*{box-sizing:border-box}html,body{margin:0}</style></head><body>'
                  +html+'</body></html>')
            body=page.encode('utf-8')
            self.send_response(200)
            self.send_header('Content-Type','text/html; charset=utf-8')
            self.send_header('Content-Length',str(len(body)))
            self.end_headers(); self.wfile.write(body); return
        return super().do_GET()
    def do_POST(self):
        if self.path=='/generate':
            try:
                n=int(self.headers.get('Content-Length',0))
                spec=json.loads(self.rfile.read(n))
                dl=bool(spec.pop('_download',False))    # 원격 접속자는 파일을 브라우저로 받음
                res=gen.generate_from_spec(spec)
                # 설정(전체 상태+spec)을 .dbpr과 같은 이름의 .json으로 함께 저장 → '설정 열기'로 복원
                try:
                    sp=res['path']; jp=(sp[:-5] if sp.lower().endswith('.dbpr') else sp)+'.json'
                    open(jp,'w',encoding='utf-8').write(json.dumps(spec,ensure_ascii=False,indent=2))
                except Exception: pass
                if dl:
                    data=open(res['path'],'rb').read()
                    from urllib.parse import quote
                    self.send_response(200)
                    self.send_header('Content-Type','application/octet-stream')
                    self.send_header('Content-Disposition',"attachment; filename*=UTF-8''"+quote(res['file']))
                    self.send_header('X-Gen-Info',quote(json.dumps({'cabinets':res['cabinets'],'warnings':res['warnings']})))
                    self.send_header('Content-Length',str(len(data)))
                    self.end_headers(); self.wfile.write(data); return
                try: os.system("open -R '%s'" % res['path'].replace("'","'\\''"))
                except Exception: pass
                out={'ok':res['ok'],'file':res['file'],'cabinets':res['cabinets'],'warnings':res['warnings'],'folder':os.path.dirname(res['path'])}
            except Exception as e:
                out={'ok':False,'error':str(e)}
            body=json.dumps(out).encode('utf-8')
            self.send_response(200); self.send_header('Content-Type','application/json; charset=utf-8')
            self.send_header('Content-Length',str(len(body))); self.end_headers(); self.wfile.write(body)
        else:
            self.send_response(404); self.end_headers()

def free_port():
    for p in range(8765,8800):
        s=socket.socket()
        try: s.bind(('127.0.0.1',p)); s.close(); return p
        except OSError: s.close()
    return 8765

def main():
    service = bool(os.environ.get('DBSD_NOOPEN'))   # 서비스(로그인 자동실행) 모드: 브라우저 자동열기 끔, 고정포트 8765
    port = 8765 if service else free_port()
    socketserver.TCPServer.allow_reuse_address=True
    # 로컬 Mac에서만 접근 허용. 인증 없는 UI를 LAN 전체에 노출하지 않는다.
    httpd=socketserver.ThreadingTCPServer(('127.0.0.1',port),H)
    url=f"http://127.0.0.1:{port}"
    try:
        lan=socket.gethostbyname(socket.gethostname())
    except Exception: lan=None
    if lan and not lan.startswith('127.'):
        print(f"같은 와이파이에서 접속: http://{lan}:{port}", flush=True)
    if not service:
        threading.Timer(0.7, lambda: webbrowser.open(url)).start()
    print("d&b System Designer →", url, ("(서비스 모드)" if service else "(Ctrl+C로 종료)"), flush=True)
    print("출력 폴더:", gen.FOLDER, flush=True)
    try: httpd.serve_forever()
    except KeyboardInterrupt: pass

if __name__=='__main__': main()
