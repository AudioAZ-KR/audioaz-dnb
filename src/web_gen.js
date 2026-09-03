
/* DBSD 웹 생성기 — arraycalc_gen.py의 1:1 JS 이식. 브라우저 단독으로 .dbpr 생성. */
(function(){
'use strict';
var LINE={KSL:['KSL8',118,'KSL12',121],XSL:['XSL8',137,'XSL12',140],Y:['Y8',98,'Y12',99],'Y-Series':['Y8',98,'Y12',99],GSL:['GSL8',110,'GSL12',113],V:['V8',73,'V12',76],CCL:['CCL8',153,'CCL12',156],J:['J8',92,'J12',93],A:['AL60',124,'AL90',128],T:['T10',50,'T10',50]};
var POINT={E8:['E8-50x90',39,'E-Series'],'E-Series':['E8-50x90',39,'E-Series'],E12:['E12-80x50',40,'E-Series'],E6:['E6-100x55',56,'E-Series'],E5:['E5',72,'E-Series'],E4:['E4',71,'E-Series'],V10P:['V10P-110x40',91,'V-Series'],V7P:['V7P-40x75',90,'V-Series'],Y10P:['Y10P-110x40',82,'Y-Series'],Y7P:['Y7P-40x75',81,'Y-Series'],M4:['M4-act-70x50',37,'Monitors'],M2:['M2',21,'Monitors'],M6:['M6-50x80',54,'Monitors'],'44S':['44S-30x90',134,'xS-Series'],'24S':['24S-75x45',105,'xS-Series'],Q1:['Q1',38,'Q-Series'],U7:['U7-55x80',151,'U-Series'],U5:['U5-90x60',150,'U-Series'],U3:['U3-100x65',149,'U-Series'],'8S':['8S',59,'xS-Series'],'5S':['5S',58,'xS-Series']};
var SUB={'SL-SUB':['SL-SUB',114,'SL-SUB'],'SL-GSUB':['SL-SUB',114,'SL-SUB'],'KSL-SUB':['KSL-SUB',131,'KSL'],'V-SUB':['V-SUB',75,'V-Series'],'V-GSUB':['V-SUB',75,'V-Series'],'Y-SUB':['Y-SUB',88,'Y-Series'],'J-SUB':['J-SUB',34,'J-Series'],'J-INFRA':['J-INFRA',47,'J-Series'],B22:['B22-SUB',101,'SUBs'],B8:['B8-SUB',122,'SUBs'],B6:['B6-SUB',83,'SUBs'],B4:['B4-SUB',52,'SUBs'],E12SUB:['E12-SUB',15,'E-Series'],E15SUB:['E15-SUB',41,'E-Series'],'21S':['21S-SUB',107,'xS-Series'],'18S':['18S-SUB',66,'xS-Series'],'CCL-SUB':['CCL-SUB',159,'CCL'],'Q-SUB':['Q-SUB',3,'Q-Series'],'T-SUB':['T-SUB',51,'T-Series'],'27S':['27S-SUB',67,'xS-Series'],'12S':['12S-SUB',68,'xS-Series'],'XSL-SUB':['XSL-SUB',141,'XSL'],'XSL-GSUB':['XSL-SUB',141,'XSL']};
var SUB_INTEG_ID={'XSL-SUB':142,'XSL-GSUB':142};
var ALT={E12D:'E12',E18SUB:'E15SUB',Q7:'Q1',Q10:'Q1'};
var CAB_NAME={118:'KSL8',121:'KSL12',137:'XSL8',140:'XSL12',98:'Y8',99:'Y12',110:'GSL8',113:'GSL12',73:'V8',76:'V12',153:'CCL8',156:'CCL12',92:'J8',93:'J12',124:'AL60',128:'AL90',50:'T10',39:'E8-50x90',40:'E12-80x50',56:'E6-100x55',72:'E5',71:'E4',91:'V10P-110x40',90:'V7P-40x75',82:'Y10P-110x40',81:'Y7P-40x75',37:'M4-act-70x50',21:'M2',54:'M6-50x80',134:'44S-30x90',105:'24S-75x45',59:'8S',58:'5S',38:'Q1',151:'U7-55x80',150:'U5-90x60',149:'U3-100x65',114:'SL-SUB',75:'V-SUB',88:'Y-SUB',131:'KSL-SUB',159:'CCL-SUB',34:'J-SUB',47:'J-INFRA',101:'B22-SUB',122:'B8-SUB',83:'B6-SUB',52:'B4-SUB',15:'E12-SUB',41:'E15-SUB',107:'21S-SUB',66:'18S-SUB',148:'B10N-SUB',163:'B12-SUB',3:'Q-SUB',141:'XSL-SUB',142:'XSL-SUB'};
var SYS={KSL:'KSL',GSL:'GSL',XSL:'XSL',V:'V-Series',Y:'Y-Series','Y-Series':'Y-Series',T:'T-Series',A:'A-Series',J:'J-Series',CCL:'CCL',E8:'E-Series','E-Series':'E-Series'};
var SPLAY_MAX={KSL:10,GSL:7,XSL:14,V:14,Y:14,'Y-Series':14,CCL:14,J:7,A:40,T:15};  // 공식 예제 전수 실측(260723)
var FLY_MAX={KSL:24,GSL:24,XSL:24,V:24,Y:24,'Y-Series':24,CCL:24,J:24,A:16,T:16};
var STACK_MAX=8, STK_MAX={GSL:6,KSL:6,J:6};
var R1_TABLES=['ViewTypes','ControlTypes','TargetTypes','Views','Controls','Groups','Pictures','Scenes','SceneValues'];
var FCOL=[10,7,4,2,8,15,6,11,12,3];
var CH2_IDS={118:1,121:1,110:1,113:1,137:1,140:1,92:1,93:1,37:1,114:1,131:1,34:1,47:1,141:1,142:1};  // 바이앰프(2ch/통)
var CH2_LINK2={118:1,121:1,137:1,140:1,92:1,93:1};  // Line/Arc 세팅으로 채널쌍당 2통 허용(KSL/XSL/J 매뉴얼). GSL·서브·M4는 1 고정
// 1ch 모델 채널당 최대 병렬 통수(예제 실측 최대 + 매뉴얼). 미등록=1 안전.
var LINK1_MAX={39:2,40:2,56:2,72:2,71:2,134:2,105:2,59:3,58:4,151:2,150:2,149:2,
 98:2,99:2,73:2,76:2,124:2,128:2,50:2,153:2,156:2,91:2,90:2,82:2,81:2,
 38:2,3:2,75:2,88:2,122:2,83:2,52:2,15:2,41:2,107:2,66:2,159:2,
 21:1,54:1,101:1};
// 프레임별 플라잉 한계(공식 페이지, XSL만 모드 구분 공표)
var FRAME_LIMITS={XSL:{comp:24,ten:22,mount:12}};
// 스피커별 호환 앰프(공식 ExampleProjects 전수 추출, 260723). 첫 항목=교체 기본값.
var AMP_OK={
 118:['D90','D80','D40'],121:['D90','D80','D40'],110:['D90','D80'],113:['D90','D80'],
 137:['D40','D80','D90','40D'],140:['D40','D80','D90','40D'],73:['D80','D40','D90','40D'],76:['D80','D40','D90','40D'],
 98:['D80','D40','30D'],99:['D80','D40','30D'],92:['D80','D90'],93:['D80','D90'],
 124:['D40','D20','D80','30D'],128:['D40','D20','D80','30D'],50:['D80','D20','10D'],
 153:['D40'],156:['D40'],159:['D40'],
 91:['D40','D90','40D','30D'],90:['D80','D20','D90','30D'],
 82:['D80','D40','D20','D90','30D','40D'],81:['D40','D20','D80','30D','40D'],
 39:['D20','D40','D80','10D','30D','5D','40D'],40:['D20','D80','10D'],
 56:['D20','10D','5D'],72:['D20','10D'],71:['D20','10D'],
 37:['D40','D80','D90','40D'],21:['D80','30D'],54:['D80','30D'],
 134:['D20','D40','10D','5D'],105:['D20','30D'],59:['D20','D80','10D','30D','5D'],
 58:['D20','D12','10D','5D'],38:['D80'],3:['D80'],
 114:['D90','D80'],131:['D80','D40','D90','40D'],75:['D80','D40','D20','30D','40D'],
 88:['D80','D20','30D'],34:['D80','30D'],47:['D80'],101:['D80'],
 122:['D20','10D','5D'],83:['D20','D80','30D'],52:['D20','D12','D80','30D'],
 15:['D20','10D'],41:['D20','10D'],107:['D20','30D','40D'],66:['D20','30D'],
 51:['D80','D20','10D'],67:['D20','30D','40D'],68:['D20','30D'],159:['D40'],160:['D40'],141:['D40','D80','D90','40D'],142:['D40','D80','D90','40D']};
// 데이터 출처·검증일 — 갱신 시 재확인 대상 추적. window.DBSD_SOURCES로 노출.
var DATA_PROV={
 AMP_OK:{source:'공식 ExampleProjects 전수(Cabinets⋈Devices) + V8/XSL8 제품 페이지 대조',verified:'2026-07-23',note:'V8+D90은 제품 페이지 목록엔 없고 성능표·D90 페이지·예제 근거(supported)'},
 CH2_IDS:{source:'예제 전수 실측(캐비닛 채널 배치)',verified:'2026-07-23'},
 CH2_LINK2:{source:'KSL/XSL/J/GSL/KSL-SUB 매뉴얼 Operation 표(Cabinets per pair)',verified:'2026-07-23'},
 SPLAY_MAX:{source:'예제 전수 실측 SplayAngle 최대값',verified:'2026-07-23'},
 FLY_MAX:{source:'매뉴얼 통수(컴프레션 기준) — 프레임/텐션 세분은 ArrayCalc 확인',verified:'2026-07-22'},
 CAB_H:{source:'예제 이웃 캐비닛 3D 간격 중앙값 실측',verified:'2026-07-23'},
 OutputMode:{source:'예제 통계(바이앰프 704/709=8, 1ch 622/656=0)',verified:'2026-07-23'},
 SNAP_PROPS:{source:'Y-Series 예제 채널별 스냅샷 속성 세트',verified:'2026-07-23'},
 LINK1_MAX:{source:'예제 실측 채널당 최대 통수 + 매뉴얼(Y 2/ch 등)',verified:'2026-07-23'},
 FRAME_LIMITS:{source:'XSL8 제품 페이지(컴프레션 24/텐션 22/마운팅 12) — 타 시리즈는 24 단일 공표',verified:'2026-07-23'}};
if(typeof window!=='undefined')window.DBSD_SOURCES=DATA_PROV;
function ampFix(part,sid,amp){
  var ok=AMP_OK[sid];
  if(!ok||ok.indexOf(amp)>=0)return amp;
  warn('⚠ '+part+': '+amp+'는 이 스피커 미지원 → '+ok[0]+'로 자동 교체');
  return ok[0];
}
var PART_SUBNET={'MAIN':1,'G.SUB':2,'Front fill':3,'DELAY':4,'CENTER':5,'OUT':6};
function subnetOf(part){for(var k in PART_SUBNET){if(part.indexOf(k)===0||part.toUpperCase().indexOf(k)===0)return PART_SUBNET[k];}return 7;}
function R(v,d){var m=Math.pow(10,d);return Math.round((+v)*m)/m;}
function sysOf(m){return SYS[m]!==undefined?SYS[m]:m;}
// 캐비닛 높이(m) — 공식 예제 이웃 캐비닛 3D 간격 중앙값 실측(260723). 미등록은 0.34.
var CAB_H={GSL:0.394,KSL:0.332,XSL:0.285,J:0.362,V:0.311,Y:0.257,'Y-Series':0.257,A:0.33,T:0.20,CCL:0.21};
function cabH(fam){return CAB_H[fam]!==undefined?CAB_H[fam]:0.34;}
// 플라잉 프레임(ArrayCalc 저장본 역산): 유효 픽 데이터면 틸트·1점식 파일저장 가능(크래시 방지)
var FRAME_NAME={GSL:'GSLFlyingFrame',KSL:'KSLFlyingFrame',XSL:'XSLFlyingFrame',V:'VFlyingFrame',Y:'YFlyingFrame',J:'JFlyingFrame',A:'AFlyingFrame',T:'TFlyingFrame',CCL:'CCLFlyingFrame'};
var FRAME_GEO={GSL:[0.10825,0.04,32],KSL:[0.01,0.0404,25],XSL:[-0.046,0.033619,21],Y:[-0.024,0.016,44],V:[-0.02019,0.018,39],J:[-0.028,0.024671,38],A:[-0.0151,0.0174,27],T:[-0.025,0.014,36],CCL:[-0.016,0.016381,42]};   // [A, pitch, rear홀] X_local=A-pitch*hole · XSL=ArrayCalc 실측(260728)
var COG_BASE={GSL:0.42,KSL:0.29,XSL:0.20,Y:0.15,V:0.217,J:0.307,A:0.21,T:0.143,CCL:0.189};                     // 싱글홀 CoG 보정 · XSL 단일홀6.016 역산
var CAB_W={GSL:79.9375,KSL:56.744,XSL:39.0,Y:20.35,V:33.278,J:63.9,A:21.225,T:10.545,CCL:16.435}, FRAME_W={GSL:72.0,KSL:62.0,XSL:31.3,Y:18.62,V:30.0,J:44.0,A:20.0,T:15.0,CCL:24.0};  // TotalWeight=통수×통무게+프레임(ArrayCalc 로드시 재계산)
var SUB_H={'SL-SUB':0.52,'KSL-SUB':0.45,'V-SUB':0.54,'Y-SUB':0.31,'J-SUB':0.72,'J-INFRA':0.72,'CCL-SUB':0.30,'T-SUB':0.27,'XSL-SUB':0.56,'B22-SUB':0.63,'B8-SUB':0.30,'B6-SUB':0.30,'B4-SUB':0.22,'E12-SUB':0.36,'E15-SUB':0.44,'21S-SUB':0.63,'18S-SUB':0.54,'27S-SUB':0.72,'12S-SUB':0.36};
var SUB_KG={'SL-SUB':61,'KSL-SUB':39,'V-SUB':41,'Y-SUB':24,'J-SUB':63,'J-INFRA':66,'CCL-SUB':22,'T-SUB':23,'XSL-SUB':40,'B22-SUB':98,'B8-SUB':24,'B6-SUB':16,'B4-SUB':13,'E12-SUB':24,'E15-SUB':32,'21S-SUB':71,'18S-SUB':44,'27S-SUB':83,'12S-SUB':21};
function subH(name){return SUB_H[name]!==undefined?SUB_H[name]:0.5;}
var LINE_SERIES={GSL:'SL',KSL:'SL',XSL:'SL',V:'V',Y:'Y',J:'J',A:'A',T:'T',CCL:'CCL'};
var COMPAT_SUB={GSL:['SL-SUB','SL-GSUB'],KSL:['KSL-SUB'],XSL:['XSL-SUB','XSL-GSUB'],V:['V-SUB','V-GSUB'],Y:['Y-SUB'],J:['J-SUB','J-INFRA'],T:['T-SUB'],CCL:['CCL-SUB']};  // 프레임 폭 일치 전용(GSL↔SL-SUB, KSL↔KSL-SUB, XSL↔XSL-SUB 교차불가)
function sameSeries(lm,sm){return (COMPAT_SUB[lm]||[]).indexOf(sm)>=0;}
var W_=[];
function warn(w){if(W_.indexOf(w)<0)W_.push(w);}
function altOf(m){if(ALT[m]!==undefined){warn('ℹ '+m+': ArrayCalc 예제에 없는 모델 → '+ALT[m]+'(으)로 대체');return ALT[m];}return m;}
function clampLine(mdl,boxcount,splays,mount){
  var lim=(mount==='stack')?(STK_MAX[mdl]||STACK_MAX):(FLY_MAX[mdl]||16);
  var bc=Math.trunc(+boxcount);
  var n=Math.max(1,Math.min(bc,lim));
  if(bc>lim)warn('⚠ '+mdl+' '+(mount==='stack'?'그라운드스택':'플라잉')+' '+boxcount+'통 → 구성 한계(매뉴얼 최대 통수) '+lim+'통으로 제한');
  var fl=FRAME_LIMITS[mdl];
  if(fl&&mount!=='stack'&&n>fl.ten)
    warn('ℹ '+mdl+' '+n+'통: 컴프레션 모드 최대 '+fl.comp+'통 기준 — 텐션 모드는 최대 '+fl.ten+'통, 마운팅 프레임은 '+fl.mount+'통 (ArrayCalc Rigging Plot 확인)');
  var smax=SPLAY_MAX[mdl]!==undefined?SPLAY_MAX[mdl]:10, over=false, sp=[];
  (splays||[]).forEach(function(s){var v=Math.max(0,Math.min(+s,smax));over=over||(+s>smax);sp.push(v);});
  if(over)warn('⚠ '+mdl+' 스플레이 '+smax+'° 초과 → '+smax+'°로 제한');
  sp=sp.slice(0,n); while(sp.length<n)sp.push(0);
  return [n,sp];
}
function variants(n,nm){var split=Math.max(1,Math.round(n*0.6)),out=[];for(var i=0;i<n;i++)out.push(i<split?[nm[0],nm[1]]:[nm[2],nm[3]]);return out;}
function applyManualVariants(bx,nm,mv){
  if(!mv)return bx;
  var pair=[[nm[0],nm[1]],[nm[2],nm[3]]];
  for(var i=0;i<Math.min(bx.length,mv.length);i++)bx[i]=pair[mv[i]?1:0];
  return bx;
}
function fam(part){if(/\sL$/.test(part))return[part.slice(0,-2),'LEFT'];if(/\sR$/.test(part))return[part.slice(0,-2),'RIGHT'];return[part,'MONO'];}
function b64u8(b64){var bin=atob(b64),u=new Uint8Array(bin.length);for(var i=0;i<bin.length;i++)u[i]=bin.charCodeAt(i);return u;}
function r1dec(v){return (v&&typeof v==='object'&&v.__b64__)?b64u8(v.__b64__):v;}

function Builder(){this.sql=['BEGIN;'];this.dev=10;this.cid=100;this.sg=1;this.ap=1;this.ff=1;this.parts={};this.order=[];this.subseq={};this.devinfo={};}
// 유효 픽 데이터로 플라잉 프레임 기록(홀·좌표 유효 + LoadBeamPosition='standard' → 크래시 방지)
Builder.prototype.flyingFrame=function(sg,mdl,horiz,ox,oy,oz,single,cogHole,ncab,tilt){
  var geo=FRAME_GEO[mdl]; if(!geo) return;   // 미검증 시리즈 → 프레임 생략(ArrayCalc 자동생성)
  var A=geo[0],pitch=geo[1],rear=geo[2], h=(horiz||0)*Math.PI/180;
  var ch=Math.max(1,Math.min(rear-1,Math.round(cogHole)));   // 1점식/CoG 홀 클램프
  var fh=0;                                                  // 2점식 프론트홀=0(맨앞) → CoG straddle → 하중 유효
  function pk(hole){var xl=A-pitch*hole;return [ox+xl*Math.cos(h),oy+xl*Math.sin(h),0.025+pitch*hole];}
  var f=pk(fh),r=pk(rear),s=pk(ch);
  var srh=single?ch:-1;                                      // SinglePickPointHole: 1점식만 실홀
  var tw=(ncab>0)?R(ncab*(CAB_W[mdl]||60)+(FRAME_W[mdl]||65),4):-1;
  var ffid=this.ff++, disp=FRAME_NAME[mdl].replace('FlyingFrame',' Flying frame');
  this.sql.push("INSERT INTO FlyingFrames(FlyingFrameId,Type,Name,DisplayName,SourceGroupId,PositionIndex,FrameAngle,FrontPickPointHole,RearPickPointHole,SinglePickPointHole,TotalWeight,FrontPickPointWeight,RearPickPointWeight,FrontPickPointWeightZeroDegrees,RearPickPointWeightZeroDegrees,FrontPickX,FrontPickY,RearPickX,RearPickY,SinglePickX,SinglePickY,FrontPickPointPosition,RearPickPointPosition,SinglePickPointPosition,OriginX,OriginY,OriginZ,LoadBeamPosition) VALUES("
    +ffid+",2,'"+FRAME_NAME[mdl]+"','"+disp+"',"+sg+",1,"+R(-(tilt||0),2)+","+fh+","+rear+","+srh+","+tw+",-1,-1,-1,-1,"
    +R(f[0],6)+","+R(f[1],6)+","+R(r[0],6)+","+R(r[1],6)+","+R(s[0],6)+","+R(s[1],6)+","
    +R(f[2],4)+","+R(r[2],4)+","+R(s[2],4)+","+R(ox,2)+","+R(oy,2)+","+R(oz,2)+",'standard');");
};
Builder.prototype.reg=function(part,dev,ch){if(!this.parts[part]){this.parts[part]=[];this.order.push(part);}this.parts[part].push([dev,ch]);};
Builder.prototype.unitOf=function(part){
  var um=this.unitmap||{};
  function g(key,dsn,dst){ var v=um[key]||{}; dst=dst||1;
    var sn=Math.max(1,Math.min(63,Math.trunc(+v.sn)||dsn));
    var st=Math.max(1,Math.min(63,Math.trunc(+v.st)||dst));
    return [sn,st]; }
  var pu=String(part).toUpperCase(), um2=this.unitmap||{};
  var T=[['MAIN L',['MAIN L','MAIN'],1,1],['MAIN R',['MAIN R','MAIN'],2,1],['MAIN',['MAIN L','MAIN'],1,1],
         ['G.SUB L',['G.SUB L','G.SUB'],3,1],['G.SUB R',['G.SUB R','G.SUB'],4,1],['G.SUB',['G.SUB L','G.SUB'],3,1],
         ['FRONT FILL',['Front fill'],5,1],
         ['DELAY L',['DELAY L','DELAY'],6,1],['DELAY R',['DELAY R','DELAY'],7,1],['DELAY',['DELAY L','DELAY'],6,1],
         ['CENTER',['CENTER'],8,1],
         ['OUT L',['OUT L','OUT'],9,1],['OUT R',['OUT R','OUT'],10,1],['OUT',['OUT L','OUT'],9,1]];
  for(var i=0;i<T.length;i++){ if(pu.indexOf(T[i][0])===0){
    var keys=T[i][1];
    for(var j=0;j<keys.length;j++){ if(um2[keys[j]]) return g(keys[j],T[i][2],T[i][3]); }
    return g(keys[keys.length-1],T[i][2],T[i][3]); } }
  return g('CUSTOM',11);
};
Builder.prototype.newdev=function(model,part,ch2){
  var d=this.dev++;var e=this.sql;
  var u=this.unitOf(part), sn=u[0], st=u[1];
  this.subseq[sn]=Math.max(this.subseq[sn]===undefined?(st-1):this.subseq[sn], st-1);
  var seq=this.subseq[sn]+1; this.subseq[sn]=seq;
  var label=part+' '+sn+'.'+(seq<10?'0':'')+seq;
  e.push("INSERT INTO Devices(DeviceId,Model,RemoteIdSubnet,RemoteIdDevice,Name) VALUES("+d+",'"+model+"',"+sn+","+seq+",'"+label+"');");
  e.push("INSERT INTO DevicesAmplifier(DeviceId,InputMode,OutputMode) VALUES("+d+",0,"+(ch2?8:0)+");");
  this.devinfo[d]={label:label,model:model,chn:{},cnt:{},dms:(this._dms===undefined?0.3:this._dms)};
  return d;
};
Builder.prototype.chname=function(d,lead,pair,label){
  this.devinfo[d].chn[lead]=label;
  (this.devinfo[d].leads=this.devinfo[d].leads||[]).push(lead);
  if(pair)this.devinfo[d].chn[pair]=label;
};
Builder.prototype.flushdev=function(){
  var e=this.sql;
  for(var d in this.devinfo){
    var info=this.devinfo[d], names=[1,2,3,4].map(function(ch){return info.chn[ch]||'';});
    e.push("INSERT INTO AmplifierChannels(DeviceId,AmplifierChannel,Name) VALUES("+d+",1,'"+names[0]+"'),("+d+",2,'"+names[1]+"'),("+d+",3,'"+names[2]+"'),("+d+",4,'"+names[3]+"');");
    for(var ch=1;ch<=4;ch++){
      if(info.chn[ch]&&(ch===1||info.chn[ch-1]!==info.chn[ch]))
        e.push("INSERT INTO PatchIOChannels(DeviceId,Type,PortNumber,Name,Protocol) VALUES("+d+",1,"+ch+",'"+info.chn[ch]+"',5);");
    }
  }
  this.flushsnap();
};
// 스냅샷 — ArrayCalc가 채널 입력소스(Config_InputEnable)를 여기서 읽음. 공식 Y-Series 예제 채널 속성 세트 재현.
var SNAP_PROPS=[['Config_InputEnable1','1.0'],['Config_InputEnable2','0.0'],['Config_InputEnable3','0.0'],
  ['Config_InputEnable4','0.0'],['Config_InputEnable5','0'],['Config_InputEnable6','0'],
  ['Config_InputEnable7','0'],['Config_InputEnable8','0'],
  ['Config_LoadMatchSpeakerCount','1'],['Config_LoadMatchCableLength','30'],
  ['Config_LoadMatchCableCrossSection','4.0'],['Config_DelayOn','1'],['ChStatus_MsDelay','0.3'],
  ['Config_Mute','0'],['Config_PotiLevel','0.0'],
  ['Config_Filter1','0'],['Config_Filter2','0'],['Config_Filter3','0']];
var SNAP_PROPS_SMALL=[['Config_InputEnable1','1.0'],['Config_InputEnable2','0'],['Config_InputEnable3','0'],
 ['Config_InputEnable4','0'],['Config_InputEnable5','0.0'],['Config_InputEnable6','0.0'],
 ['Config_InputEnable7','0.0'],['Config_InputEnable8','0.0'],
 ['Config_DelayOn','1'],['Config_Mute','0'],['Config_PotiLevel','0.0'],
 ['Config_Filter1','0'],['Config_Filter2','0'],['Config_Filter3','0'],['ChStatus_MsDelay','0.3']];
var SMALL_AMPS={'D20':1,'D40':1};   // LoadMatch 미탑재 — D90식 세트 넣으면 ArrayCalc가 입력을 못 읽음(260903 오라클)

Builder.prototype.flushsnap=function(){
  var e=this.sql;
  var sd=this.snapdate||'';
  var created=sd?('20'+sd.slice(0,2)+'-'+sd.slice(2,4)+'-'+sd.slice(4,6)+'T00:00:00.000Z'):'2026-01-01T00:00:00.000Z';
  e.push("INSERT INTO Snapshots(SnapshotId,Type,Name,Comment,CreatedOn) VALUES(1,0,'ArrayCalc snapshot','Snapshot created automatically by ArrayCalc','"+created+"');");
  var svid=1;
  for(var d in this.devinfo){
    var info=this.devinfo[d];
    var small=!!SMALL_AMPS[info.model];
    if(small){
      e.push("INSERT INTO SnapshotValues(SnapshotValueId,SnapshotId,SnapshotTargetType,Value,TargetId,TargetNode,TargetProperty,TargetRecord) VALUES("+(svid++)+",1,0,1,"+d+",0,'Input_Digital_Mode',1);");
      e.push("INSERT INTO SnapshotValues(SnapshotValueId,SnapshotId,SnapshotTargetType,Value,TargetId,TargetNode,TargetProperty,TargetRecord) VALUES("+(svid++)+",1,0,2,"+d+",0,'Input_Digital_Mode',3);");
    }
    var props=small?SNAP_PROPS_SMALL:SNAP_PROPS;
    var leads=(info.leads||[]).slice().sort(function(a,b){return a-b;}).filter(function(v,i,arr){return i===0||arr[i-1]!==v;});
    for(var i=0;i<leads.length;i++){
      for(var j=0;j<props.length;j++){
        var v=props[j][1];
        if(props[j][0]==='Config_LoadMatchSpeakerCount')v=String(info.cnt[leads[i]]||1);
        else if(props[j][0]==='ChStatus_MsDelay')v=String(info.dms===undefined?0.3:info.dms);
        e.push("INSERT INTO SnapshotValues(SnapshotValueId,SnapshotId,SnapshotTargetType,Value,TargetId,TargetNode,TargetProperty,TargetRecord) VALUES("+(svid++)+",1,0,"+v+","+d+","+leads[i]+",'"+props[j][0]+"',0);");
      }
    }
  }
};
Builder.prototype.sgroup=function(o){ // {typ,name,system,amp,sym,mounting,ox,oy,oz,frame,horiz,nxt,ordr,singleRig}
  var sg=this.sg++;var e=this.sql;
  var ordr=(o.ordr===undefined||o.ordr===null)?sg:o.ordr;
  var srp=(o.singleRig===undefined||o.singleRig===null)?'NULL':String(o.singleRig|0);  // 1점식=1(primary)/0(mirror)
  e.push("INSERT INTO SourceGroups(SourceGroupId,Type,Name,OrderIndex,RemarkableChangeDate,NextSourceGroupId,ArrayProcessingEnable,ArraySightId,LinkMode,Symmetric,Mounting,RelativeDelay) VALUES("+sg+","+o.typ+",'"+o.name+"',"+ordr+",0,"+(o.nxt||0)+",0,0,0,"+(o.sym||0)+","+(o.mounting===undefined?1:o.mounting)+",NULL);");
  e.push("INSERT INTO SourceGroupsAdditionalData(SourceGroupId,System,HorizontalAiming,StackedFrameAngle,HasPrevious,DefaultRemoteIdSubnet,DefaultRemoteIdDevice,ShowRigging,SelectedArrayProcessingSlotNumber,BoxType,NominalDispersionAngle,OriginX,OriginY,OriginZ,HeightLowestEdge,VerticalAimingAngle,CompressionModeEnable,CompressionForce,CompressionGrabLinkPosition,MaxLoadTension,MaxLoadTensionBGV,MaxLoadCompression,MaxLoadCompressionBGV,DefaultAmplifierType,RearRiggingPoint,FrontRiggingPoint,SingleRiggingPoint) VALUES("+sg+",'"+o.system+"',"+(o.horiz||0)+","+(o.frame||0)+","+(o.ordr===-1?1:0)+",0,1,1,NULL,'',0,"+(o.ox||0)+","+(o.oy||0)+","+(o.oz||0)+",NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'"+o.amp+"',NULL,NULL,"+srp+");");
  if(o.typ===1){ // 라인어레이: AP 슬롯 기본 10개 — 없으면 열 때 경고
    for(var slot=1;slot<=10;slot++){
      var apid=this.ap++;
      var nm2=(slot===1)?'Bypass':'';
      var cm2=(slot===1)?'This slot is reserved for bypassing ArrayProcessing.':'';
      e.push("INSERT INTO ArrayProcessingSlots(ArrayProcessingSlotId,SourceGroupId,Slot,Name,Comment,SessionId,CreatedOn,Flags) VALUES("+apid+","+sg+","+slot+",'"+nm2+"','"+cm2+"','','1970-01-01T01:00:00.000',1);");
      e.push("INSERT INTO ArrayProcessingSlotsAdditionalData(ArrayProcessingSlotId,Slope1,Slope2,Slope3,Point1X,Point2X,Temperature,Humidity,VenueObjectIdSelected,PowerGlory,SourceGroupTargetProfile) VALUES("+apid+",0.0,-3.0,-3.0,0.0,0.0,293.16,60.0,1,0.5,'');");
    }
  }
  return sg;
};
Builder.prototype.cab=function(dv,ch,spk,sg,pos,h,v,x,y,z,splay,delay){
  delay=delay||0;
  var c=this.cid++;var nm=CAB_NAME[spk]||'Linear';var e=this.sql;
  e.push("INSERT INTO Cabinets(CabinetId,DeviceId,AmplifierChannel,SpeakerId,SourceGroupId,PositionIndex,OrderIndex,HorizontalAngle,VerticalAngle,RotationAngle,PivotAngle,Linked,OriginX,OriginY,OriginZ,HornRotationAngle) VALUES("+c+","+dv+","+ch+","+spk+","+sg+","+pos+",1,"+h+","+v+",0,0,0,"+x+","+y+","+z+",0);");
  e.push("INSERT INTO CabinetsAdditionalData(CabinetId,Name,ControllerSetup,SplayAngle,AlignmentToSubArrayTestPoint,CabinetsPerPosition,CompressionState,DraftSignalSourceDeviceId,DraftSignalSourceChannelNumber,Delay,Mute,Level,Switch1,Switch2,Switch3,Switch4,Switch5,PreviousObjectString,NextObjectString) VALUES("+c+",'"+nm+"',0,"+splay+",0,1,0,NULL,NULL,"+delay+",0,0,0,0,0,-5.5,0.5,NULL,NULL);");
};
Builder.prototype.placeSubsTop=function(sg,spk,subn,amp,part,topz,subH_,sideY,ox,link,posStart){
  amp=ampFix(part,spk,amp);
  var ch2=!!CH2_IDS[spk], lk=ch2?1:Math.max(1,Math.trunc(+(link||1))), cap=ch2?2:4*lk;
  var d=null,slot=0,grp=0,z=topz;
  for(var i=0;i<subn;i++){
    if(slot%cap===0){d=this.newdev(amp,part,ch2);slot=0;}
    var lead=ch2?(Math.floor(slot/lk)*2+1):(Math.floor(slot/lk)+1), pair=ch2?(lead+1):0;
    if(slot%lk===0){grp++; this.chname(d,lead,pair,part+' '+(grp<10?'0':'')+grp);}
    this.devinfo[d].cnt[lead]=(this.devinfo[d].cnt[lead]||0)+1;
    slot++;
    this.cab(d,lead,spk,sg,posStart+i,0,0,R(-i*0.02,2),sideY,R(z,2),0);this.reg(part,d,lead);z-=subH_;
  }
  return R(z,2);
};
Builder.prototype.lineArray=function(name,system,amp,sideY,topz,tilt,boxes,splays,mount,ox,horiz,gname,nxt,sym,ordr,link,dms,subtop,rigpts){
  mount=mount||'flown';ox=ox||0;horiz=horiz||0;nxt=nxt||0;sym=sym||0;rigpts=(rigpts===undefined?'2':String(rigpts));
  var stack=(mount==='stack'),n0=boxes.length;
  var chH=cabH(system);                                   // 모델별 캐비닛 높이(실측)
  // 통합 행잉 서브(플라잉 전용): 서브가 최상단, 라인어레이는 그 아래로 낮춤
  var subN=(subtop&&!stack)?subtop.n:0, subH_=subN?subtop.h:0;
  var lineTop=subN?R(topz-(subN*subH_+0.3),2):topz;
  var oz=stack?0:topz;
  var hle=stack?0.3:Math.max(R(lineTop-n0*chH-0.3,2),0.2);
  amp=ampFix(name,boxes[0][1],amp);   // 스피커-앰프 호환 자동 교정 (sgroup보다 먼저 — DefaultAmplifierType 일치)
  this._dms=(dms===undefined?0.3:dms);
  if(Math.trunc(+(link||1))>1&&CH2_LINK2[boxes[0][1]])
    warn('ℹ '+name+': 링크 1:2(Line/Arc 세팅) — 앰프에서 Line/Arc 셋업 선택 필요, ArrayProcessing 사용 불가');
  var _single=(rigpts==='1'&&!stack);
  var _srp=(_single&&ordr!==-1)?1:(_single?0:null);   // 1점식 primary=1, mirror(ordr=-1)=0, dual=null
  var sg=this.sgroup({typ:1,name:(gname||name),system:sysOf(system),amp:amp,sym:sym,mounting:stack?1:0,ox:ox,oy:sideY,oz:oz,frame:stack?tilt:0,horiz:horiz,nxt:nxt,ordr:ordr,singleRig:_srp});
  var pos0=1;
  if(subN){ this.placeSubsTop(sg,subtop.spk,subN,subtop.amp,subtop.part,topz,subH_,sideY,ox,subtop.link||1,pos0); pos0+=subN; }
  var n=boxes.length,d=null,z=stack?1.4:lineTop,cum=0,slot=0,grp=0,cums=[];
  var ch2=!!CH2_IDS[boxes[0][1]];
  var lk=ch2?(CH2_LINK2[boxes[0][1]]?Math.min(Math.trunc(+(link||1)),2):1):Math.max(1,Math.trunc(+(link||1)));
  if(lk<1)lk=1;
  var cap=ch2?2*lk:4*lk;
  for(var i=0;i<n;i++){
    var bid=boxes[i][1];
    if(slot%cap===0){d=this.newdev(amp,name,ch2);slot=0;}
    var lead=ch2?(Math.floor(slot/lk)*2+1):(Math.floor(slot/lk)+1), pair=ch2?(lead+1):0;
    if(slot%lk===0){grp++; this.chname(d,lead,pair,name+' '+(grp<10?'0':'')+grp);}
    this.devinfo[d].cnt[lead]=(this.devinfo[d].cnt[lead]||0)+1;
    slot++;
    var sp_i,v;
    if(stack){
      sp_i=((n-1-i)<splays.length)?splays[n-1-i]:0;cum+=sp_i;v=-(tilt-cum);
      this.cab(d,lead,bid,sg,pos0+i,0,R(v,1),R(-i*0.02,2),sideY,R(z,2),R(sp_i,1));this.reg(name,d,lead);z+=chH;
    }else{
      sp_i=(i<splays.length)?splays[i]:0;cum+=sp_i;v=-(tilt+cum);
      this.cab(d,lead,bid,sg,pos0+i,0,R(v,1),R(-i*0.02,2),sideY,R(z,2),R(sp_i,1));this.reg(name,d,lead);z-=chH;cums.push(cum);
    }
  }
  var _fs=(FRAME_GEO[system]?system:system.replace('-Series',''));   // 프레임은 모델키(Y) 기준 — sysOf는 'Y-Series'라 매칭 실패했었음
  if(!stack&&FRAME_GEO[_fs]){                    // 플라잉 프레임 기록(유효 픽 → 크래시 방지)
    var A=FRAME_GEO[_fs][0],pitch=FRAME_GEO[_fs][1];
    var x=0,cxs=0;                               // 캐비닛 체인(스플레이 아크) 재구성 → CoG 전후위치
    for(var ci=0;ci<cums.length;ci++){var dx=chH*Math.sin(cums[ci]*Math.PI/180);cxs+=x+0.5*dx;x+=dx;}
    var cogx=cums.length?cxs/cums.length:0;
    var cogHole=(cogx+(COG_BASE[_fs]||0.4)-0.025)/pitch;
    this.flyingFrame(sg,_fs,horiz,ox,sideY,oz,_single,cogHole,subN+n,tilt);
  }
  return sg;
};
Builder.prototype.pointRow=function(name,system,amp,spk,ys,zpos,aim,xpos,sym,link,dms,horiz){
  horiz=+(horiz||0);
  xpos=xpos||0;sym=sym||0;
  amp=ampFix(name,spk,amp); this._dms=(dms===undefined?0.3:dms);
  var sg=this.sgroup({typ:2,name:name,system:system,amp:amp,sym:sym});var d=null,slot=0,grp=0;
  var ch2=!!CH2_IDS[spk];
  var lk=ch2?(CH2_LINK2[spk]?Math.min(Math.trunc(+(link||1)),2):1):Math.max(1,Math.trunc(+(link||1)));
  if(lk<1)lk=1;
  var cap=ch2?2*lk:4*lk;
  for(var i=0;i<ys.length;i++){
    if(slot%cap===0){d=this.newdev(amp,name,ch2);slot=0;}
    var lead=ch2?(Math.floor(slot/lk)*2+1):(Math.floor(slot/lk)+1), pair=ch2?(lead+1):0;
    if(slot%lk===0){grp++; this.chname(d,lead,pair,name+' '+(grp<10?'0':'')+grp);}
    this.devinfo[d].cnt[lead]=(this.devinfo[d].cnt[lead]||0)+1;
    slot++;
    var _h=R(ys[i]<0?horiz:(ys[i]>0?-horiz:horiz),1);
    this.cab(d,lead,spk,sg,i+1,_h,R(aim,1),R(xpos,2),R(ys[i],2),R(zpos,2),0);this.reg(name,d,lead);
  }
  return sg;
};
Builder.prototype.subStack=function(name,system,amp,spk,positions,sym,link,dms){
  amp=ampFix(name,spk,amp); this._dms=(dms===undefined?0.3:dms);
  var sg=this.sgroup({typ:3,name:name,system:system,amp:amp,sym:sym||0});var d=null,slot=0,grp=0;
  var ch2=!!CH2_IDS[spk];
  var lk=ch2?(CH2_LINK2[spk]?Math.min(Math.trunc(+(link||1)),2):1):Math.max(1,Math.trunc(+(link||1)));
  if(lk<1)lk=1;
  var cap=ch2?2*lk:4*lk;
  for(var i=0;i<positions.length;i++){
    var p=positions[i], hang=p.length>3?p[3]:0, dly=p.length>4?p[4]:0;
    if(slot%cap===0){d=this.newdev(amp,name,ch2);slot=0;}
    var lead=ch2?(Math.floor(slot/lk)*2+1):(Math.floor(slot/lk)+1), pair=ch2?(lead+1):0;
    if(slot%lk===0){grp++; this.chname(d,lead,pair,name+' '+(grp<10?'0':'')+grp);}
    this.devinfo[d].cnt[lead]=(this.devinfo[d].cnt[lead]||0)+1;
    slot++;
    this.cab(d,lead,spk,sg,i+1,hang,0,R(p[0],2),R(p[1],2),R(p[2],2),0.5,dly);this.reg(name,d,lead);
  }
  return sg;
};
Builder.prototype.pointStackCombo=function(mname,msys,mspk,ys,mz,maim,mx,sname,ssys,sspk,sbox,slink,x_sub,subh,amp,sym){
  // 포인트-스택 메인 + 서브를 한 앰프(≤4채널)에. 비바이앰프 전용. 서브 링크 반영(채널당 slink통 Z스택).
  sym=(sym===undefined?1:sym);
  var d=this.newdev(amp,'MAIN',false),lead=1;
  var sgm=this.sgroup({typ:2,name:mname,system:msys,amp:amp,sym:sym});
  var sgs=this.sgroup({typ:3,name:sname,system:ssys,amp:amp,sym:sym});
  var mCh=ys.length; slink=Math.max(1,Math.trunc(slink)); var sCh=sbox?Math.ceil(sbox/slink):0, spos=0;
  // 채널 순서: 측별 탑→서브 인터리브(A=L탑,B=L서브,C=R탑,D=R서브) — 4코어 A/B·C/D로 측당 통합 결선
  for(var i=0;i<Math.max(mCh,sCh);i++){
    if(i<mCh){
      var ml=(mCh===2)?(mname+' '+(ys[i]<0?'L':'R')):(mname+' '+(i+1<10?'0':'')+(i+1));
      this.chname(d,lead,0,ml);this.devinfo[d].cnt[lead]=(this.devinfo[d].cnt[lead]||0)+1;
      this.cab(d,lead,mspk,sgm,i+1,0,R(maim,1),R(mx,2),R(ys[i],2),R(mz,2),0);this.reg(mname,d,lead);lead++;
    }
    if(i<sCh){
      var sy=(i<mCh)?ys[i]:ys[i%mCh];
      var sl=(sCh===2)?(sname+' '+(sy<0?'L':'R')):(sname+' '+(i+1<10?'0':'')+(i+1));
      this.chname(d,lead,0,sl);   // 채널명 1회, 링크된 서브 여러 통을 이 채널에
      var _nc=Math.min(slink, sbox-i*slink);
      for(var k=0;k<_nc;k++){ spos++; this.devinfo[d].cnt[lead]=(this.devinfo[d].cnt[lead]||0)+1;
        this.cab(d,lead,sspk,sgs,spos,0,0,R(x_sub,2),R(sy,2),R(k*subh,2),0.5);this.reg(sname,d,lead); }
      lead++;
    }
  }
  return [sgm,sgs];
};

function injectParamVenue(db,spec){
  var vp=spec.venue;
  if(vp&&vp.length){
    db.run("DELETE FROM VenueObjectPoints");db.run("DELETE FROM VenueObjects");
    var COLS=[4294901760,4294945280,4283282175,4288335154],BLK=4278190080;
    vp.forEach(function(q,i){
      var _w=+(q.w||0),_yc=+(q.yc||0),hf=R((q.wf!==undefined?+q.wf:_w)/2,2),hb=R((q.wb!==undefined?+q.wb:_w)/2,2),ycf=R(+(q.ycf!==undefined?q.ycf:_yc),2),ycb=R(+(q.ycb!==undefined?q.ycb:_yc),2),d=R(+q.d,2),z0=R(+q.z0,2),z1=R(+q.z1,2);
      var nm=String(q.n||('Plane '+(i+1))).replace(/'/g,'');
      db.run("INSERT INTO VenueObjects VALUES(?,?,1,1,1,1,1,1.2,?,?,?,0,0,0,0,0,1,1,1,?,0)",[i+1,nm,COLS[i%COLS.length],BLK,R(+q.x,2),i+1]);
      [[0,ycf+hf,z0],[d,ycb+hb,z1],[d,ycb-hb,z1],[0,ycf-hf,z0]].forEach(function(pt,j){
        db.run("INSERT INTO VenueObjectPoints VALUES(?,?,?,?,?)",[i+1,j,pt[0],pt[1],pt[2]]);
      });
    });
    return;
  }
  var st=(spec._state)||{};
  var D=+(st.depth||36),W=+(st.width||24);
  var hw=R(W/2,2),d1=R(D*0.6,2),d2=R(D-d1,2);
  db.run("DELETE FROM VenueObjectPoints");db.run("DELETE FROM VenueObjects");
  var RED=4294901760,ORG=4294945280,BLK=4278190080;
  db.run("INSERT INTO VenueObjects VALUES(1,'Audience Front',1,1,1,1,1,1.2,?,?,2,0,0,0,0,0,1,1,1,1,0)",[RED,BLK]);
  [[0,hw,0],[d1,hw,0],[d1,-hw,0],[0,-hw,0]].forEach(function(p,i){db.run("INSERT INTO VenueObjectPoints VALUES(1,?,?,?,?)",[i,p[0],p[1],p[2]]);});
  db.run("INSERT INTO VenueObjects VALUES(2,'Audience Rear',1,1,1,1,1,1.2,?,?,?,0,0,0,0,0,1,1,1,2,0)",[ORG,RED,R(2+d1,2)]);
  [[0,hw,0],[d2,hw,2.5],[d2,-hw,2.5],[0,-hw,0]].forEach(function(p,i){db.run("INSERT INTO VenueObjectPoints VALUES(2,?,?,?,?)",[i,p[0],p[1],p[2]]);});
}

function r1Overview(db,b,A){
  var order=b.order; if(!order.length||!A)return;
  R1_TABLES.forEach(function(t){
    var r=db.exec("SELECT 1 FROM sqlite_master WHERE type='table' AND name='"+t+"'");
    if(!r.length)db.run(A.create[t]);
  });
  Object.keys(A.enums).forEach(function(t){
    A.enums[t].forEach(function(row){
      var r=row.map(r1dec);
      db.run("INSERT OR IGNORE INTO "+t+" VALUES("+r.map(function(){return '?';}).join(',')+")",r);
    });
  });
  db.run("DELETE FROM Views");db.run("DELETE FROM Controls");db.run("DELETE FROM Groups");
  A.sysviews.rows.forEach(function(row){
    var r=row.map(r1dec);
    db.run("INSERT INTO Views("+A.sysviews.cols.join(',')+") VALUES("+r.map(function(){return '?';}).join(',')+")",r);
  });
  if(A.tv){A.tv.rows.forEach(function(row){
    var r=row.map(r1dec);
    try{db.run("INSERT OR IGNORE INTO TableVersions("+A.tv.cols.join(',')+") VALUES("+r.map(function(){return '?';}).join(',')+")",r);}catch(e){}
  });}
  var cols=A.ccols;
  var T={};Object.keys(A.controls).forEach(function(k){var d={};Object.keys(A.controls[k]).forEach(function(c){d[c]=r1dec(A.controls[k][c]);});T[k]=d;});
  var ctl=1;
  function put(t,ov){
    if(!t)return;
    var d={};Object.keys(t).forEach(function(c){d[c]=t[c];});
    Object.keys(ov||{}).forEach(function(c){d[c]=ov[c];});
    d.ControlId=ctl++;d.ViewId=1000;
    db.run("INSERT INTO Controls("+cols.join(',')+") VALUES("+cols.map(function(){return '?';}).join(',')+")",cols.map(function(c){return d[c]===undefined?null:d[c];}));
  }
  db.run("INSERT INTO Groups(GroupId,Name,ParentId,TargetId,TargetChannel,Type,Flags) VALUES(1,'Groups',0,0,-1,0,1)");
  db.run("INSERT INTO Groups(GroupId,Name,ParentId,TargetId,TargetChannel,Type,Flags) VALUES(2,'Master',1,0,-1,0,0)");
  var gid=3,fams={},famOrder=[];
  order.forEach(function(pname){
    var chans=b.parts[pname];
    var fc=fam(pname),fm=fc[0],col=fc[1];
    if(!fams[fm]){
      db.run("INSERT INTO Groups(GroupId,Name,ParentId,TargetId,TargetChannel,Type,Flags) VALUES(?,?,2,0,-1,0,0)",[gid,fm]);
      fams[fm]={gid:gid,sides:[]};famOrder.push(fm);gid++;
    }
    var f=fams[fm];
    db.run("INSERT INTO Groups(GroupId,Name,ParentId,TargetId,TargetChannel,Type,Flags) VALUES(?,?,?,0,-1,0,0)",[gid,pname,f.gid]);
    var sgid=gid;gid++;
    chans.forEach(function(dc){
      db.run("INSERT INTO Groups(GroupId,Name,ParentId,TargetId,TargetChannel,Type,Flags) VALUES(?,?,?,?,?,1,0)",[gid,pname+' d'+dc[0]+'.'+dc[1],sgid,dc[0],dc[1]]);gid++;
    });
    f.sides.push([col,sgid,chans[0][0],chans[0][1]]);
  });
  var x0=16,xs=[],cx0=x0;
  famOrder.forEach(function(fm){
    var ncol=Math.max(1,fams[fm].sides.length);xs.push([cx0,ncol]);cx0+=ncol*175+34;
  });
  var xr=cx0+16, W=xr+350+16, H=1080;
  var Z=Math.min(80,Math.trunc(1920*80/Math.max(W,1920)));
  db.run("INSERT INTO Views(ViewId,Type,Name,Icon,Flags,HomeViewIndex,NaviBarIndex,HRes,VRes,ZoomLevel) VALUES(1000,1000,'Overview','',6,0,1,?,?,?)",[W,H,Z]);
  var firstDev=b.parts[order[0]][0][0];
  famOrder.forEach(function(fm,i){
    var hx=xs[i][0],ncol=xs[i][1],c=FCOL[i%FCOL.length],f=fams[fm],g=f.gid;
    if(ncol>=2){
      put(T.frame,{PosX:hx,PosY:16,Width:ncol*175,DisplayName:fm,MainColor:c});
      put(T.mute,{PosX:hx+13,PosY:56,TargetId:g});
      put(T.fader,{PosX:hx+96,PosY:46,TargetId:g});
      put(T.cut,{PosX:hx+237,PosY:56,TargetId:g});
      put(T.cpl,{PosX:hx+237,PosY:86,TargetId:g});
      put(T.dsw,{PosX:hx+237,PosY:146,TargetId:g});
      put(T.rdel,{PosX:hx+237,PosY:176,TargetId:g});
    }else{
      put(T.frame,{PosX:hx,PosY:16,Width:175,DisplayName:fm,MainColor:c});
      put(T.mute,{PosX:hx+13,PosY:56,TargetId:g});
      put(T.fader,{PosX:hx+75,PosY:46,Width:90,TargetId:g});
      put(T.cut,{PosX:hx+13,PosY:146,Width:52,TargetId:g});
      put(T.dsw,{PosX:hx+13,PosY:176,Width:52,TargetId:g});
    }
    f.sides.forEach(function(sd,k){
      var col=sd[0],sgid=sd[1],dv=sd[2],ch=sd[3],cx=hx+k*175;
      put(T.colfr,{PosX:cx+1,PosY:253,DisplayName:col,MainColor:c});
      put(T.mute,{PosX:cx+63,PosY:300,TargetId:sgid});
      put(T.isp,{PosX:cx+37,PosY:380,TargetId:dv,TargetChannel:ch});
      put(T.gr,{PosX:cx+81,PosY:380,TargetId:dv,TargetChannel:ch});
      put(T.ovl,{PosX:cx+126,PosY:380,TargetId:dv,TargetChannel:ch});
      put(T.min,{PosX:cx+52,PosY:444,TargetId:dv,TargetChannel:ch});
      put(T.mgr,{PosX:cx+122,PosY:444,TargetId:dv,TargetChannel:ch});
      put(T.peak,{PosX:cx+43,PosY:867,TargetId:dv,TargetChannel:ch});
    });
  });
  put(T.frame,{PosX:xr,PosY:16,DisplayName:'Master',MainColor:14});
  put(T.mute,{PosX:xr+12,PosY:56,TargetId:2});
  put(T.fader,{PosX:xr+95,PosY:46,TargetId:2});
  put(T.power,{PosX:xr+250,PosY:56,TargetId:2});
  put(T.infofr,{PosX:xr,PosY:253,DisplayName:'Information'});
  put(T.mv,{PosX:xr+177,PosY:322,TargetId:firstDev,TargetChannel:0});
  put(T.mf,{PosX:xr+177,PosY:353,TargetId:firstDev,TargetChannel:0});
  put(T.mp,{PosX:xr+177,PosY:384,TargetId:firstDev,TargetChannel:0});
  put(T.comfr,{PosX:xr,PosY:468,DisplayName:'Comments'});
  // 브랜딩 텍스트(txt1/txt2) 미삽입 — 참고 기반 디자인이라 서명 제외 (v1.92)
}

function roundTrip(db,spec){
  // 생성 .dbpr 재파싱 → spec 대조. 파일 생성 정확성 검증 — 음향·리깅 검증 아님.
  var checks=[];
  var _w=W_.slice();   // 역검증 중 경고 중복 방지
  function ck(name,okv,detail){checks.push({name:name,ok:!!okv,detail:detail||''});}
  function q1(sql){var r=db.exec(sql);return (r.length&&r[0].values.length)?r[0].values[0][0]:0;}
  try{
    var cnt={},r=db.exec("SELECT s.Name,COUNT(*) FROM SourceGroups s JOIN Cabinets c ON c.SourceGroupId=s.SourceGroupId GROUP BY s.SourceGroupId");
    if(r.length)r[0].values.forEach(function(v){cnt[v[0]]=(cnt[v[0]]||0)+v[1];});
    var m=spec.main||{},su=spec.sub||{},exp={};
    if(m.type==='line'&&LINE[m.mdl]){var cl=clampLine(m.mdl,m.box,m.splay,m.mount||'flown');exp['MAIN']=cl[0]*2;}
    else if(m.type==='point')exp['MAIN']=2;
    var _smrt=su.mdl?altOf(su.mdl):null;
    var _integRt=(su.pos==='flown'&&su.flyMode==='stacked'&&SUB[_smrt]&&m.type==='line'&&LINE[m.mdl]&&sameSeries(m.mdl,su.mdl));
    if(SUB[_smrt]){
      if(_integRt)exp['MAIN']=(exp['MAIN']||0)+Math.ceil(Math.trunc(+(su.box||2))/2)*2;   // 통합: 서브가 MAIN 그룹
      else exp['G.SUB']=Math.max(1,Math.trunc(+(su.box||2)))+(su.fSubOn?Math.trunc(+(su.fSubBox||0)):0);
    }
    [['front','Front fill'],['center','CENTER'],['out','OUT'],['delay','DELAY']].forEach(function(kv){
      var v=spec[kv[0]]||{}; if(!v.on)return;
      var nb=Math.trunc(+(v.box||1))||1, part=kv[1];
      if(v.type==='line'){
        var mdl=altOf(v.mdl);
        if(LINE[mdl]){var cl2=clampLine(mdl,nb,v.splay,v.mount||'flown');exp[part]=cl2[0]*((part==='OUT'||part==='DELAY')?2:1);}
      }else{
        var pm={'Front fill':nb,'CENTER':1,'OUT':2,'DELAY':2}[part];
        exp[{'CENTER':'Center','OUT':'Out','DELAY':'Delay'}[part]||part]=pm;
      }
    });
    for(var part in exp)ck(part+' 캐비닛 수',(cnt[part]||0)===exp[part],(cnt[part]||0)+'/'+exp[part]);
    var bad=0,rr=db.exec("SELECT DISTINCT d.Model,c.SpeakerId FROM Devices d JOIN Cabinets c ON c.DeviceId=d.DeviceId");
    if(rr.length)rr[0].values.forEach(function(v){var okl=AMP_OK[v[1]];if(okl&&okl.indexOf(v[0])<0)bad++;});
    ck('앰프-스피커 호환',bad===0,bad?('위반 '+bad+'건'):'전 장치 OK');
    var viol=0,mx=0,rc=db.exec("SELECT SpeakerId,COUNT(*) FROM Cabinets GROUP BY DeviceId,AmplifierChannel,SpeakerId");
    if(rc.length)rc[0].values.forEach(function(v){
      var sid=v[0],n=v[1];
      var lim=CH2_IDS[sid]?(CH2_LINK2[sid]?2:1):(LINK1_MAX[sid]!==undefined?LINK1_MAX[sid]:1);
      if(n>lim)viol++; if(n>mx)mx=n;
    });
    ck('채널(쌍)당 통수 한계(모델별)',viol===0,viol?('위반 '+viol+'건'):('최대 '+mx+'통/채널 · 전 모델 허용 내'));
    var badp=q1("SELECT COUNT(*) FROM SourceGroups s JOIN SourceGroupsAdditionalData a USING(SourceGroupId) WHERE s.OrderIndex=-1 AND a.HasPrevious!=1 AND s.Type IN(1,2,3)");
    ck('L/R 대칭쌍 링크',badp===0,'');
    var leads=q1("SELECT COUNT(DISTINCT DeviceId||'/'||AmplifierChannel) FROM Cabinets");
    var sv=q1("SELECT COUNT(*) FROM SnapshotValues WHERE TargetProperty='Config_InputEnable1' AND Value=1.0");
    ck('채널 입력소스(스냅샷)',leads?sv>=leads:true,sv+'/'+leads);
    var cfg=su.cfg;
    if(cfg==='endfire'||cfg==='arc'||cfg==='cardioid'){
      var nbs=Math.trunc(+(su.box||0))||0;
      var mn={arc:3,endfire:2,cardioid:3}[cfg];
      var got,applied,det;
      if(cfg==='cardioid'){
        got=q1("SELECT COUNT(*) FROM Cabinets c JOIN SourceGroups s ON s.SourceGroupId=c.SourceGroupId WHERE s.Name='G.SUB' AND c.HorizontalAngle=180");
        applied=got>0; det='반전 '+got+'통';
      }else{
        got=q1("SELECT COUNT(*) FROM CabinetsAdditionalData ca JOIN Cabinets c USING(CabinetId) JOIN SourceGroups s ON s.SourceGroupId=c.SourceGroupId WHERE s.Name='G.SUB' AND ca.Delay>0");
        applied=got>0; det='딜레이 '+got+'통';
      }
      if(nbs<mn)ck('서브 배열 요청('+cfg+')',false,'최소 '+mn+'통 필요('+nbs+'통) → L/R 스택 폴백 — 경고 표시됨');
      else ck('서브 배열 요청('+cfg+')',applied,applied?det:'미적용!');
    }
  }catch(e){ck('역검증 실행',false,String(e).slice(0,80));}
  W_.length=0; Array.prototype.push.apply(W_,_w);
  var allok=checks.every(function(c){return c.ok;});
  return {ok:allok,checks:checks};
}
function build(db,spec){
  injectParamVenue(db,spec);
  var vr=db.exec("SELECT min(p.X+o.OriginX),max(p.X+o.OriginX),max(abs(p.Y+o.OriginY)) FROM VenueObjectPoints p JOIN VenueObjects o USING(VenueObjectId)");
  var row=(vr.length&&vr[0].values[0][0]!==null)?vr[0].values[0]:[0,22,15];
  var vx0=row[0],vx1=row[1],vy=row[2];
  var xF=0;                                          // 무대앞 고정 — 관객면 이동과 독립 (v1.88)
  var zM=+(((spec._state)||{}).trim||9);
  // 플라잉 서브 stacked: 메인 라인어레이를 서브 컬럼만큼 낮춤
  var _sub=spec.sub||{}, _subDrop=0, _subStackFly=false;
  if(_sub.pos==='flown'&&_sub.flyMode==='stacked'){
    var _sm2=_sub.mdl?altOf(_sub.mdl):null;
    if(SUB[_sm2]){var _snb=Math.trunc(+(_sub.box||2)),_sper=Math.ceil(_snb/2),_sh=subH(SUB[_sm2][0]);_subDrop=R(_sper*_sh+0.3,2);_subStackFly=true;}
  }
  // 통합 행잉 판정: 플라잉 stacked + 같은 시리즈 → 서브를 메인 그룹에 통합
  var _m0=spec.main||{}, _s0=spec.sub||{};
  var _integrated=(_subStackFly&&SUB[_sm2]&&_m0.type==='line'&&LINE[_m0.mdl]&&sameSeries(_m0.mdl,_s0.mdl));
  if(_subStackFly&&SUB[_sm2]&&!_integrated&&_m0.type==='line')
    warn('ℹ 통합 행잉 해제 — '+_m0.mdl+'의 통합 호환 서브는 '+((COMPAT_SUB[_m0.mdl]||[]).join('/')||'없음')+'. '+_s0.mdl+'는 프레임이 달라 통합 불가 → 서브를 별도 플라잉(좌우 컬럼)으로 생성');
  var zMtop=zM;   // 통합 행잉은 lineArray가 subtop로 낮춤(이중 낮춤 방지)
  var _dd=(spec.delay||{}).dist;
  var xD=R(_dd?((vx0-2)+ +_dd):(vx0+0.52*(vx1-vx0)),1);   // 딜레이 X: 무대앞(메인 위치) 기준 거리 또는 홀 중간
  var yM=R(vy*0.55,1);
  var yO=R(vy*0.82,1);
  // ── 스피커 위치 오버라이드(spec.spkPos, 베뉴 편집기 드래그) — 없으면 자동 공식 ──
  var _ovp=spec.spkPos||{};
  function _op(part,key,dflt){ var p=_ovp[part]||{}; var v=p[key]; if(v===undefined||v===null)return dflt; v=+v; return isFinite(v)?R(v,2):dflt; }
  var xM=_op('main','x',xF),   yMn=_op('main','y',yM);
  var xS=_op('sub','x',xF),    ySb=_op('sub','y',yM);
  var xFf=_op('front','x',null), yFf=_op('front','y',0);
  var xDl=_op('delay','x',xD), yDl=_op('delay','y',yM);
  var xC=_op('center','x',xF), yC=_op('center','y',0);
  var xO=_op('out','x',xF),    yOt=_op('out','y',yO);
  var b=new Builder();
  b.unitmap=spec.unitIds||{};
  b.snapdate=String(spec.date||'');  // 스냅샷 CreatedOn(결정적 — 파이썬과 패리티)
  var m=spec.main||{}, _combo=false;   // 포인트-스택 통합 앰프 여부(서브 별도생성 스킵 판정)
  if(m.type==='line'&&LINE[m.mdl]){
    var mnt=m.mount||'flown';var cl=clampLine(m.mdl,m.box,m.splay,mnt);var n=cl[0],sp=cl[1];var bx=applyManualVariants(variants(n,LINE[m.mdl]),LINE[m.mdl],m.variants);
    var mh=+(m.horiz||0);var nl=b.sg;
    var _subtop=null,_mgrpAmp=m.amp||'D90';
    if(_integrated){var _per=Math.ceil(Math.trunc(+(_s0.box||2))/2);
      var _integspk=(SUB_INTEG_ID[_sm2]!==undefined)?SUB_INTEG_ID[_sm2]:SUB[_sm2][1];
      // 한 소스 그룹=한 앰프. 메인·서브 공통 앰프로 통일(서브 미지원 앰프 강제 시 amp_fix가 되돌려 혼재→빨간 에러 방지).
      var _mainamp=m.amp||'D90', _subAmps=AMP_OK[SUB[_sm2][1]]||[], _mainAmps=AMP_OK[LINE[m.mdl][1]]||[];
      if(_subAmps.indexOf(_mainamp)>=0){_mgrpAmp=_mainamp;}
      else{var _common=_mainAmps.filter(function(a){return _subAmps.indexOf(a)>=0;});
        if(_common.length){_mgrpAmp=_common[0];warn('ℹ 통합 행잉: 한 그룹=한 앰프 → '+m.mdl+'+'+_s0.mdl+' 공통 앰프 '+_mgrpAmp+'로 통일 ('+_s0.mdl+'는 '+_mainamp+' 미지원, '+m.mdl+' 시스템 표준 앰프)');}
        else{_integrated=false;warn('⚠ 통합 행잉 해제: '+m.mdl+'('+_mainamp+')와 '+_s0.mdl+'가 공통 앰프 없음 → 서브를 별도 G.SUB 그룹으로 생성(메인 앰프 유지)');}}
      if(_integrated)_subtop={spk:_integspk,n:_per,amp:_mgrpAmp,part:'G.SUB',h:subH(SUB[_sm2][0]),link:_s0.link||1};}
    b.lineArray('MAIN L',m.mdl,_mgrpAmp,-yMn,zMtop,m.tilt||0,bx,sp,mnt,xM,mh,'MAIN',nl+1,0,null,m.link||1,0.3,_subtop,m.rigPts||'2');
    b.lineArray('MAIN R',m.mdl,_mgrpAmp, yMn,zMtop,m.tilt||0,bx,sp,mnt,xM,-mh,'MAIN',0,0,-1,m.link||1,0.3,(_subtop?{spk:_subtop.spk,n:_subtop.n,amp:_subtop.amp,part:_subtop.part,h:_subtop.h,link:_subtop.link}:null),m.rigPts||'2');
  }else if(m.type==='point'){
    var mm0=altOf(m.mdl);
    if(POINT[mm0]){
      var pu0=POINT[mm0];
      // 포인트소스 M20 폴 스택(서브 위): 높이 = 받침 서브 스택 + 폴대 길이(+ 캐비닛 반높이 근사)
      var _st0=spec._state||{},zPt=zM;
      if(m.mount==='stack'){
        var _sm0=(spec.sub||{}).mdl,_sma=_sm0?altOf(_sm0):null,_subh=(_sma&&SUB[_sma])?subH(SUB[_sma][0]):0.5;
        var _psn=Math.max(1,Math.ceil((+((spec.sub||{}).box||2))/2)),_polem=(+(_st0.poleH||1100))/1000;  // 받침 서브 = SUB 섹션 측당 통수
        zPt=R(_psn*_subh+_polem+0.2,2);
        warn('ℹ 포인트소스 폴 스택: '+m.mdl+'를 '+(_sm0||'서브')+' '+_psn+'통(측당) 위 M20 폴('+_polem.toFixed(2)+'m)에 스택 → 높이 '+zPt+'m. 받침 서브는 서브우퍼 섹션에서 설정.');
      }
      // ── 포인트-스택 메인 + 서브 ≤4채널 → 앰프 1대 통합. 채널 기준(서브 링크 반영: 서브ch=ceil(통수/링크)) ──
      var _cs=spec.sub||{},_csm=_cs.mdl?altOf(_cs.mdl):null,_sbox=Math.trunc(+(_cs.box||0)),_slink=Math.max(1,Math.trunc(+(_cs.link||1)));
      var _ys=[-yMn,yMn],_mch=_ys.length, _subch=_sbox?Math.ceil(_sbox/_slink):0;
      var _mbi=!!CH2_IDS[pu0[1]],_sbi=SUB[_csm]?!!CH2_IDS[SUB[_csm][1]]:true;
      var _common=SUB[_csm]?(AMP_OK[pu0[1]]||[]).filter(function(a){return (AMP_OK[SUB[_csm][1]]||[]).indexOf(a)>=0;}):[];
      _combo=(m.mount==='stack'&&!!SUB[_csm]&&_sbox>=1&&(_mch+_subch)<=4&&_common.length>0&&!_mbi&&!_sbi);
      if(_combo){
        var _camp=_common[0];
        b.pointStackCombo('MAIN',pu0[2],pu0[1],_ys,zPt,m.tilt||0,xM,'G.SUB',SUB[_csm][2],SUB[_csm][1],_sbox,_slink,xM,subH(SUB[_csm][0]),_camp,1);
        warn('ℹ 통합 앰프: '+m.mdl+' '+_mch+'통 + '+_cs.mdl+' '+_sbox+'통(링크1:'+_slink+'→'+_subch+'ch) = '+(_mch+_subch)+'채널 → '+_camp+' 1대(측당 탑+서브 A/B·C/D).');
      }else{
        b.pointRow('MAIN',pu0[2],m.amp||'D80',pu0[1],_ys,zPt,m.tilt||0,xM,1,m.link||1);
      }
    }else warn('메인 '+m.mdl+' 미보유→건너뜀');
  }else if(m.type==='line')warn('메인 '+m.mdl+' 미보유→건너뜀');
  var s=spec.sub||{};
  var _sm=s.mdl?altOf(s.mdl):null;
  if(s.mdl&&!SUB[_sm])warn('⚠ '+s.mdl+': ArrayCalc SpeakerId 미확보 → 서브 생성 생략. ArrayCalc에서 '+s.mdl+' 소스를 하나 만들어 저장한 .dbpr을 주시면 정식 추가합니다.');
  if(SUB[_sm]&&(_integrated||_combo)){ /* 통합 행잉 or 포인트-스택 통합앰프: 서브 이미 처리됨 */ }
  else if(SUB[_sm]){
    var smdl=_sm;var su=SUB[smdl];var sid=su[1],ssys=su[2];
    var nb=Math.trunc(+(s.box||2)),half=Math.floor(nb/2),pos=[];
    var flown=(s.pos==='flown');
    var zs=flown?zM:0;
    var cfg=s.cfg||'stack', C=343.0, side, cnt, k2;
    if(flown){
      // ── 플라잉 서브 배치 모드 ──
      var fmo=s.flyMode||'integrated';
      var _shh=subH(SUB[smdl][0]);
      if(fmo==='behind'){
        var xb=R(xS-2.0,1);
        if(nb===1)pos.push([xb,0,zs]);
        else for(var kb=0;kb<nb;kb++)pos.push([xb,R((-1+2*kb/(nb-1))*(ySb*0.75),2),zs]);
        warn('ℹ G.SUB 플라잉(메인 뒤 별도): 무대 뒤 센터 브로드사이드 서브 어레이 — 정렬·커버리지는 ArrayCalc 확인');
      }else if(fmo==='stacked'){
        [-1,1].forEach(function(side){
          var cnt=half+((side<0&&nb%2)?1:0);
          for(var k=0;k<cnt;k++)pos.push([xS,side*ySb,R(zM-k*_shh,2)]);
        });
        var _tk=SUB_KG[SUB[smdl][0]]||40, _ps=Math.ceil(nb/2);
        warn('ℹ G.SUB 플라잉(서브 위·어레이 아래): 좌우 메인 위 서브 컬럼 + 라인어레이 아래로 통합 행잉. 측당 서브 '+_ps+'통(~'+(_tk*_ps)+'kg)+어레이 하중이 한 모터에 걸림 — ArrayCalc에서 각 그룹 Load 합산 확인');
      }else{
        [-1,1].forEach(function(side){
          var cnt=half+((side<0&&nb%2)?1:0);
          for(var k=0;k<cnt;k++)pos.push([xS,side*ySb,R(zs-k*_shh,2)]);
        });
        warn('ℹ G.SUB 플라잉(메인과 함께): 좌우 메인 옆 서브 컬럼 — 라인어레이와 통합 행잉, ArrayCalc에서 카디오이드/정렬 확인');
      }
    }
    var _min={arc:3,endfire:2,cardioid:3}[cfg];
    if((!flown)&&_min&&nb<_min)warn('⚠ '+cfg+' 배열은 최소 '+_min+'통 필요 — '+nb+'통이라 일반 L/R 스택으로 생성됨 (통수를 늘리면 '+cfg+' 적용)');
    if(flown){/* flyMode 처리됨 */}
    else if(cfg==='endfire'&&nb>=2){
      // 엔드파이어: 간격 = c/4f(1/4 파장). 목표 주파수 spec.sub.efFreq(기본 69Hz→1.24m). 앞 캐비닛에 간격/음속 딜레이.
      var f0=+(s.efFreq||69)||69, gap=R(C/(4.0*f0),2);
      [-1,1].forEach(function(side){
        var cnt=half+((side<0&&nb%2)?1:0);
        for(var k=0;k<cnt;k++)pos.push([R(xS-gap*k,2),side*ySb,zs,0,R(gap*k/C,6)]);
      });
      warn('ℹ G.SUB 엔드파이어 '+f0+'Hz: 간격 '+gap+'m(c/4f)·전방 딜레이 — 기하 초기값, 주파수별 결과는 ArrayCalc에서 확인');
    }else if((!flown)&&cfg==='arc'&&nb>=3){
      var Rv=Math.max(8.0,ySb*2.0);
      for(var k3=0;k3<nb;k3++){
        var y=(nb>1)?(-1+2*k3/(nb-1))*ySb:0;
        var dly=(Math.sqrt(Rv*Rv+y*y)-Rv)/C;
        pos.push([xS,R(y,2),zs,0,R(dly,6)]);
      }
      warn('ℹ G.SUB 아크: 가상 반경 딜레이 커브 반영 — 커버리지는 ArrayCalc에서 확인');
    }else if((!flown)&&cfg==='cardioid'&&nb>=3){
      [-1,1].forEach(function(side){
        var cnt=half+((side<0&&nb%2)?1:0);
        for(var k=0;k<cnt;k++){
          var rev=(k%3===1);
          pos.push([xS,side*(ySb+0.6*k),zs,rev?180:0,0]);
        }
      });
      warn('ℹ G.SUB 카디오이드: 3통당 1통 후방 반전 배치 — 전용 CSA 셋업·딜레이는 앰프/ArrayCalc에서 설정');
    }else if(!flown){
      for(var k=0;k<half;k++)pos.push([xS,-ySb-0.6*k,zs]);
      for(k=0;k<half;k++)pos.push([xS, ySb+0.6*k,zs]);
      if(nb%2)pos.push([xS,0,zs]);
    }
    if(!pos.length)pos=[[xS,0,zs]];
    // 프론트 서브(무대 앞 분산)
    if(s.fSubOn){
      var fn=Math.trunc(+(s.fSubBox||3))||3;
      var hw2=Math.max(2.0,ySb*0.7);
      for(var k4=0;k4<fn;k4++){
        var y2=(fn>1)?(-1+2*k4/(fn-1))*hw2:0;
        pos.push([R(xS+0.6,2),R(y2,2),0]);
      }
    }
    if(s.stereo){
      var posL=pos.filter(function(p){return p[1]<=0;}), posR=pos.filter(function(p){return p[1]>0;});
      if(posL.length)b.subStack('G.SUB L',ssys,s.amp||'D90',sid,posL,0,s.link||1);
      if(posR.length)b.subStack('G.SUB R',ssys,s.amp||'D90',sid,posR,0,s.link||1);
    } else b.subStack('G.SUB',ssys,s.amp||'D90',sid,pos,1,s.link||1);
  }else if(s.mdl)warn('서브 '+s.mdl+' 미보유→건너뜀');
  var f=spec.front||{};
  if(f.on){
    var fm2=altOf(f.mdl);
    if(f.type==='point'&&POINT[fm2]){
      var pu=POINT[fm2];var pid=pu[1],psys=pu[2];var nb2=Math.trunc(+(f.box||6));
      var _stw=(spec._state||{}).stageW;
      var hw=_stw?R(Math.max(2.0,(+_stw)/2.0-0.5),1):R(yM*0.8,1);var ys=[];
      if(nb2>1){for(var i2=0;i2<nb2;i2++)ys.push(R(-hw+2*hw*i2/(nb2-1),2));}else ys=[0];
      var faim=-((+f.aim||0)!==0?(+f.aim):30);   // +=하향/−=상향(부호 존중), 0=기본 30↓
      b.pointRow('Front fill',psys,f.amp||'D20',pid,ys.map(function(_y){return R(_y+yFf,2);}),R(+(f.height||1.2),2),faim,(xFf!==null?xFf:xF),1,f.link||1);
    }else if(f.type==='line'&&LINE[fm2]){
      var nb3=Math.trunc(+(f.box||6));var bx3=applyManualVariants(variants(nb3,LINE[fm2]),LINE[fm2],f.variants);
      b.lineArray('Front fill',fm2,f.amp||'D80',yFf,R(+(f.height||2.5),2),f.aim||0,bx3,f.splay||Array(nb3).fill(0),'flown',(xFf!==null?xFf:0),0,null,0,0,null,f.link||1,0.3,null,f.rigPts||'2');
    }else warn('프론트필 '+fm2+' 미보유→건너뜀');
  }
  var d=spec.delay||{};
  if(d.on){
    var dm=d.mdl,ht=+(d.height||7);
    if(d.type==='line'&&LINE[dm]){
      var dmnt=d.mount||'flown';var cl2=clampLine(dm,d.box||8,d.splay,dmnt);var nb4=cl2[0],sp2=cl2[1];var bx4=applyManualVariants(variants(nb4,LINE[dm]),LINE[dm],d.variants);
      var ndl=b.sg;
      var dms_=(d.alignMs!==undefined&&d.alignMs!==null)?R(+d.alignMs,1):R((xDl-xM)/343.0*1000+0.3,1);
      b.lineArray('DELAY L',dm,d.amp||'D40',-yDl,ht,d.aim||0,bx4,sp2,dmnt,xDl,+(d.horiz||0),'DELAY',ndl+1,0,null,d.link||1,dms_);
      b.lineArray('DELAY R',dm,d.amp||'D40', yDl,ht,d.aim||0,bx4,sp2,dmnt,xDl,-(+(d.horiz||0)),'DELAY',0,0,-1,d.link||1,dms_);
    }else if(d.type==='point'&&POINT[altOf(dm)]){
      var dm2=altOf(dm);var pu2=POINT[dm2];
      b.pointRow('Delay',pu2[2],d.amp||'D40',pu2[1],[-yDl,yDl],ht,d.aim||0,xDl,1,d.link||1,(d.alignMs!==undefined&&d.alignMs!==null)?R(+d.alignMs,1):R((xDl-xM)/343.0*1000+0.3,1),+(d.horiz||0));
    }else warn('딜레이 '+dm+' 미보유→건너뜀');
  }
  var c=spec.center||{};
  if(c.on){
    var cm=c.mdl;
    if(c.type==='line'&&LINE[cm]){
      var cl3=clampLine(cm,c.box||6,c.splay,'flown');var nb5=cl3[0],sp3=cl3[1];var bx5=applyManualVariants(variants(nb5,LINE[cm]),LINE[cm],c.variants);
      var zc=R(+(c.height||zM),1);
      b.lineArray('CENTER',cm,c.amp||'D80',yC,zc,c.aim||0,bx5,sp3,'flown',xC,+(c.horiz||0),null,0,1,null,c.link||1,0.3,null,c.rigPts||'2');
    }else if(POINT[altOf(cm)]){
      var cm2=altOf(cm);var pu3=POINT[cm2];
      b.pointRow('Center',pu3[2],c.amp||'D80',pu3[1],[yC],R(+(c.height||zM),1),c.aim||0,xC,1,c.link||1,0.3,+(c.horiz||0));
    }else warn('센터필 '+cm+' 미보유→건너뜀');
  }
  var o=spec.out||{};
  if(o.on){
    var om=o.mdl;
    if(o.type==='line'&&LINE[om]){
      var omnt=o.mount||'flown';
      var cl4=clampLine(om,o.box||6,o.splay,omnt);var nb6=cl4[0],sp4=cl4[1];var bx6=applyManualVariants(variants(nb6,LINE[om]),LINE[om],o.variants);
      var oh=+(o.horiz||0);var no=b.sg;
      b.lineArray('OUT L',om,o.amp||'D80',-yOt,R(zM-0.5,1),o.tilt||0,bx6,sp4,omnt,xO,oh,'OUT',no+1,0,null,o.link||1,0.3,null,o.rigPts||'2');
      b.lineArray('OUT R',om,o.amp||'D80', yOt,R(zM-0.5,1),o.tilt||0,bx6,sp4,omnt,xO,-oh,'OUT',0,0,-1,o.link||1,0.3,null,o.rigPts||'2');
    }else if(POINT[altOf(om)]){
      var om2=altOf(om);var pu4=POINT[om2];
      b.pointRow('Out',pu4[2],o.amp||'D80',pu4[1],[-yOt,yOt],R(zM-0.5,1),o.tilt||0,xO,1,o.link||1);
    }else warn('아웃필 '+om+' 미보유→건너뜀');
  }
  // ── 커스텀 스피커 그룹(spec.customs) — 탭 + 로 추가한 자유 스피커 ──
  (spec.customs||[]).forEach(function(cu,ci){
    try{
      var cnm=String(cu.name||('CUSTOM '+(ci+1))).slice(0,24).replace(/'/g,'');
      var ctp=cu.type||'point', cmdl=cu.mdl, cn=Math.max(1,Math.trunc(+cu.box||1));
      var cx=R(xF+(+cu.x||0),2), cyv=+cu.y||0, cz=+(cu.z===undefined?5:cu.z), cam=+(cu.aim||0);
      var csym=(cu.sym===undefined?true:!!cu.sym)?1:0, clk=Math.max(1,Math.trunc(+cu.link||1)), camp=cu.amp||'D40';
      if(ctp==='line'&&LINE[cmdl]){
        var cmt=cu.mount||'flown', crg=String(cu.rigPts||'2'), chz=+(cu.horiz||0);
        var cl9=clampLine(cmdl,cn,cu.splay,cmt), cn2=cl9[0], csp=cl9[1];
        var bxc=variants(cn2,LINE[cmdl]);
        if(csym){ var nxc=b.sg;
          b.lineArray(cnm+' L',cmdl,camp,-Math.abs(cyv),cz,cam,bxc,csp,cmt,cx,chz,cnm,nxc+1,0,null,clk,0.3,null,crg);
          b.lineArray(cnm+' R',cmdl,camp, Math.abs(cyv),cz,cam,bxc,csp,cmt,cx,-chz,cnm,0,0,-1,clk,0.3,null,crg);
        } else b.lineArray(cnm,cmdl,camp,cyv,cz,cam,bxc,csp,cmt,cx,chz,null,0,0,null,clk,0.3,null,crg);
      } else if(ctp==='sub'&&SUB[cmdl]){
        var su9=SUB[cmdl], pos2=[], half2=Math.floor(cn/2), cz0=Math.max(0,cz);
        if(csym){ for(var k=0;k<half2;k++)pos2.push([cx,-Math.abs(cyv)-0.6*k,cz0]);
          for(k=0;k<half2;k++)pos2.push([cx, Math.abs(cyv)+0.6*k,cz0]);
          if(cn%2)pos2.push([cx,0,cz0]); }
        else { for(var k2=0;k2<cn;k2++)pos2.push([cx,cyv+0.6*k2,cz0]); }
        b.subStack(cnm,su9[2],camp,su9[1],pos2,csym,clk);
      } else {
        var cm2=POINT[cmdl]?cmdl:altOf(cmdl);
        if(POINT[cm2]){ var pu9=POINT[cm2];
          var ys2=csym?[-Math.abs(cyv),Math.abs(cyv)]:[cyv];
          b.pointRow(cnm,pu9[2],camp,pu9[1],ys2,cz,cam,cx,csym,clk,0.3,+(cu.horiz||0));
        } else warn('커스텀 '+cnm+': 모델 '+cmdl+' 미보유→건너뜀');
      }
    }catch(e){ warn('커스텀 그룹 실패('+(cu.name||'?')+'): '+e); }
  });
  b.flushdev();
  b.sql.push('COMMIT;');
  db.exec(b.sql.join('\n'));
  return b;
}

/* 진입점: spec + {SQL, baseBytes, r1assets} → {ok,fileName,bytes,cabinets,warnings} */
window.DBSD_WEBGEN=function(spec,env){
  W_=[];
  var db=new env.SQL.Database(env.baseBytes);
  try{
    var b=build(db,spec);
    // AzSpec 임베드 제거(v1.93) — ArrayCalc 재저장 "Failed to copy table(s)" 오류 원인. 읽기(임포트)는 유지.
    r1Overview(db,b,env.r1assets);
    var okr=db.exec('PRAGMA integrity_check;');
    var ok=okr.length&&okr[0].values[0][0]==='ok';
    var cnt=db.exec('SELECT COUNT(*) FROM Cabinets')[0].values[0][0];
    var rt=roundTrip(db,spec);
    var bytes=db.export();
    var name=((spec.projName||'AudioAZ')+' '+(spec.ver||'v.1')+'('+(spec.date||'')+').dbpr');
    return {ok:ok,fileName:name,bytes:bytes,cabinets:cnt,warnings:W_.slice(),roundtrip:rt};
  }finally{ db.close(); }
};
})();

