#!/usr/bin/env python3
"""골든 테스트 — 배포 전 10초 안전망.
검증: ①생성 성공+무결성 ②FlyingFrames crash-critical 필드 ③베뉴 폴리곤 ④파이썬↔JS 패리티(jsc).
사용: python3 tests/run_tests.py
"""
import os,sys,json,sqlite3,subprocess,tempfile
HERE=os.path.dirname(os.path.abspath(__file__)); ROOT=os.path.dirname(HERE)
sys.path.insert(0,os.path.join(ROOT,"src"))
import arraycalc_gen as g
JSC="/System/Library/Frameworks/JavaScriptCore.framework/Versions/A/Helpers/jsc"
FAIL=[]
def check(name,cond,detail=""):
    print(("  OK " if cond else "  FAIL ")+name+((" -- "+str(detail)) if (detail and not cond) else ""))
    if not cond: FAIL.append(name)

SPEC={"projName":"GOLD","ver":"v.t","date":"260101",
 "main":{"type":"line","mdl":"KSL","box":12,"amp":"D90","link":1,"tilt":8,"mount":"flown","rigPts":"2","horiz":12,"splay":[0,0,0,0,0,1,1,1,1,1,2,2]},
 "sub":{"mdl":"SL-SUB","box":2,"amp":"D90","link":1,"pos":"ground","cfg":"stack","fSubOn":False,"fSubBox":0},
 "front":{"on":True,"type":"point","mdl":"E8","box":6,"amp":"D20","link":1,"aim":-30,"splay":[]},
 "delay":{"on":True,"type":"line","mdl":"XSL","box":6,"amp":"D40","link":1,"dist":30,"alignMs":99.5,"aim":24,"mount":"flown","rigPts":"2","height":3,"splay":[0,0,1,2,3,4]},
 "center":{"on":True,"type":"line","mdl":"Y","box":8,"amp":"D80","link":1,"height":12,"aim":12,"rigPts":"2","splay":[0,0,1,2,3,4,5,6]},
 "out":{"on":True,"type":"line","mdl":"Y","box":8,"amp":"D80","link":1,"mount":"flown","tilt":16,"horiz":0,"rigPts":"2","splay":[0,0,0,1,2,2,3,4]},
 "venue":[{"n":"T1","x":2,"d":20,"w":30,"wf":10,"wb":30,"yc":0,"ycf":5,"ycb":-2,"z0":0,"z1":2.5}],
 "_state":{"projName":"GOLD","projVer":"v.t","trim":9,"depth":40,"width":30,"stageW":12,
   "cOn":True,"oOn":True,"dOn":True,"fOn":True,"cType":"line","oType":"line","dtype":"line",
   "cMdl":"Y","oMdl":"Y","dMdl":"XSL","cHeight":12,"cHeightAuto":False,"maintype":"manual","mMdl":"KSL","mBox":12,"mBoxAuto":False}}

print("1) 생성+무결성")
tmp=tempfile.mkdtemp()
r=g.generate_from_spec(SPEC,tmp)
check("생성 성공",r["ok"])
c=sqlite3.connect(r["path"])
check("무결성 ok",c.execute("PRAGMA integrity_check").fetchone()[0]=="ok")

print("2) FlyingFrames crash-critical")
ff={}
for row in c.execute("SELECT sg.Name,ff.Name,ff.FrameAngle,ff.FrontPickPointHole,ff.RearPickPointHole,ff.TotalWeight,ff.LoadBeamPosition FROM FlyingFrames ff JOIN SourceGroups sg ON sg.SourceGroupId=ff.SourceGroupId"):
    ff.setdefault(row[0],[]).append(row)
exp={"MAIN":("KSLFlyingFrame",-8.0,0,25),"DELAY":("XSLFlyingFrame",-24.0,0,21),
     "CENTER":("YFlyingFrame",-12.0,0,44),"OUT":("YFlyingFrame",-16.0,0,44)}
for grp,(nm,ang,fh,rh) in exp.items():
    rows=ff.get(grp,[])
    check(grp+" 프레임 존재",len(rows)>=1)
    for row in rows:
        check(grp+" 프레임 필드 유효",
              row[1]==nm and abs(row[2]-ang)<0.01 and row[3]==fh and row[4]==rh and row[5]>0 and row[6]=="standard",
              "실제: %s %s f%s/r%s TW%s %s"%(row[1],row[2],row[3],row[4],row[5],row[6]))

print("3) 베뉴 폴리곤 (사다리꼴+앞/뒤중심)")
pts=list(c.execute("SELECT X,Y,Z FROM VenueObjectPoints WHERE VenueObjectId=1 ORDER BY PointIndex"))
check("앞모서리 Y=10/0",abs(pts[0][1]-10)<0.01 and abs(pts[3][1]-0)<0.01, pts)
check("뒷모서리 Y=13/-17",abs(pts[1][1]-13)<0.01 and abs(pts[2][1]+17)<0.01, pts)
check("z램프 0→2.5",abs(pts[0][2])<0.01 and abs(pts[1][2]-2.5)<0.01)

print("4) 파이썬<->JS 패리티 (FlyingFrames)")
if os.path.exists(JSC):
    spec_f=os.path.join(tmp,"spec.json"); json.dump(SPEC,open(spec_f,"w"))
    harness=(
      "var window={};load(WEBGEN);var rec=[];"
      "function DB(b){} DB.prototype.run=function(s){rec.push(String(s));};"
      "DB.prototype.exec=function(s){rec.push(String(s));"
      "if(/integrity_check/.test(s))return[{values:[['ok']]}];"
      "if(/COUNT/.test(s))return[{values:[[0]]}];"
      "if(/min\\(p\\.X/.test(s))return[{values:[[0,22,15]]}];return[];};"
      "DB.prototype.export=function(){return new Uint8Array(0);};DB.prototype.close=function(){};"
      "var spec=JSON.parse(read(SPECF));"
      "try{window.DBSD_WEBGEN(spec,{SQL:{Database:DB},baseBytes:new Uint8Array(0),r1assets:null});}catch(e){print('ERR '+e);}"
      "var out=[];rec.forEach(function(b){String(b).split(String.fromCharCode(10)).forEach(function(l){"
      "if(/INSERT INTO FlyingFrames/.test(l)){var v=l.slice(l.indexOf('VALUES(')+7).split(',');"
      "out.push(v[2]+'|'+v[6]+'|'+v[7]+'|'+v[8]);}});});"
      "print(out.join(String.fromCharCode(10)));")
    wg=os.path.join(ROOT,"src","web_gen.js")
    res=subprocess.run([JSC,"-e","var WEBGEN='%s';var SPECF='%s';%s"%(wg,spec_f,harness)],capture_output=True,text=True)
    js_lines=[l for l in res.stdout.strip().split(chr(10)) if "|" in l]
    py_lines=[]
    for row in c.execute("SELECT Name,FrameAngle,FrontPickPointHole,RearPickPointHole FROM FlyingFrames ORDER BY FlyingFrameId"):
        py_lines.append("'%s'|%g|%d|%d"%(row[0],row[1],row[2],row[3]))
    check("프레임 수 일치 py%d=js%d"%(len(py_lines),len(js_lines)),len(py_lines)==len(js_lines))
    check("프레임 값 일치",sorted(py_lines)==sorted(js_lines),"py:%s js:%s"%(sorted(py_lines)[:3],sorted(js_lines)[:3]))
else:
    print("  ! jsc 없음 -- 패리티 스킵")

print()
if FAIL: print("FAILED %d:"%len(FAIL),FAIL); sys.exit(1)
print("ALL PASS"); sys.exit(0)
