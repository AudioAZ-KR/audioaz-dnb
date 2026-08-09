#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""AudioAZ ArrayCalc 생성기 — spec dict → 열리는 .dbpr. 베이스/베뉴는 d&B R1 File 폴더 참조."""
import os, sqlite3, shutil, datetime, math
def R(v,d=0):
    "JS Math.round와 동일한 반올림(floor(x+0.5)) — 웹 생성기와 바이트 단위 일치 보장"
    m=10**d
    return math.floor(float(v)*m+0.5)/m if d else math.floor(float(v)+0.5)

# base/venue는 이 스크립트와 같은 폴더(~/.dbdesigner, 비보호)에서 읽음 → 자동실행(launchd)도 접근 가능
HERE  = os.path.dirname(os.path.abspath(__file__))
BASE  = os.path.join(HERE, "Untitled_2.dbpr")
FOLDER = os.path.expanduser("~/ArrayCalc")   # 출력 폴더(Desktop 밖, TCC 비보호)

LINE = {'KSL':('KSL8',118,'KSL12',121),'XSL':('XSL8',137,'XSL12',140),
        'Y':('Y8',98,'Y12',99),'Y-Series':('Y8',98,'Y12',99),
        'GSL':('GSL8',110,'GSL12',113),'V':('V8',73,'V12',76),
        'CCL':('CCL8',153,'CCL12',156),
        'J':('J8',92,'J12',93),                 # J-Series
        'A':('AL60',124,'AL90',128),            # A-Series (상단 AL60/하단 AL90)
        'T':('T10',50,'T10',50)}                # T-Series(단일 기종)
# 포인트: id → (이름, SpeakerId, System문자열) — System은 예제 실측(틀리면 크래시)
POINT = {'E8':('E8-50x90',39,'E-Series'),'E-Series':('E8-50x90',39,'E-Series'),
         'E12':('E12-80x50',40,'E-Series'),'E6':('E6-100x55',56,'E-Series'),
         'E5':('E5',72,'E-Series'),'E4':('E4',71,'E-Series'),
         'V10P':('V10P-110x40',91,'V-Series'),'V7P':('V7P-40x75',90,'V-Series'),
         'Y10P':('Y10P-110x40',82,'Y-Series'),'Y7P':('Y7P-40x75',81,'Y-Series'),
         'M4':('M4-act-70x50',37,'Monitors'),'M2':('M2',21,'Monitors'),'M6':('M6-50x80',54,'Monitors'),
         '44S':('44S-30x90',134,'xS-Series'),'24S':('24S-75x45',105,'xS-Series'),
         'Q1':('Q1',38,'Q-Series'),
         'U7':('U7-55x80',151,'U-Series'),'U5':('U5-90x60',150,'U-Series'),'U3':('U3-100x65',149,'U-Series'),
         '8S':('8S',59,'xS-Series'),'5S':('5S',58,'xS-Series'),
         }
# 서브: id → (이름, SpeakerId, System문자열)
SUB   = {'SL-SUB':('SL-SUB',114,'SL-SUB'),'SL-GSUB':('SL-SUB',114,'SL-SUB'),
         'KSL-SUB':('KSL-SUB',131,'KSL'),
         'V-SUB':('V-SUB',75,'V-Series'),'V-GSUB':('V-SUB',75,'V-Series'),
         'Y-SUB':('Y-SUB',88,'Y-Series'),
         'J-SUB':('J-SUB',34,'J-Series'),'J-INFRA':('J-INFRA',47,'J-Series'),
         'B22':('B22-SUB',101,'SUBs'),'B8':('B8-SUB',122,'SUBs'),
         'B6':('B6-SUB',83,'SUBs'),'B4':('B4-SUB',52,'SUBs'),
         'E12SUB':('E12-SUB',15,'E-Series'),'E15SUB':('E15-SUB',41,'E-Series'),
         '21S':('21S-SUB',107,'xS-Series'),'18S':('18S-SUB',66,'xS-Series'),
         'CCL-SUB':('CCL-SUB',159,'CCL'),'Q-SUB':('Q-SUB',3,'Q-Series'),
         'T-SUB':('T-SUB',51,'T-Series'),'27S':('27S-SUB',67,'xS-Series'),'12S':('12S-SUB',68,'xS-Series'),
         'XSL-SUB':('XSL-SUB',141,'XSL'),'XSL-GSUB':('XSL-SUB',141,'XSL')}
# 통합 행잉(Type-1 라인어레이 그룹) 전용 SpeakerId — 단독(Type-3)과 다름(사용자 ArrayCalc 파일 실측 260725)
SUB_INTEG_ID={'XSL-SUB':142,'XSL-GSUB':142}
# 예제에 SpeakerId가 없는 모델 → 같은 계열 최근접으로 대체(+경고). 조용히 사라지는 것 방지.
ALT = {'E12D':'E12','E18SUB':'E15SUB',
       'Q7':'Q1','Q10':'Q1',
       }   # XSL-SUB은 SpeakerId 미확인 — 임의 대체 안 함(사용자 지적). 네이티브 파일로 정식 추가 예정                # 12.8.2엔 Q1만 존재(네이티브 실측) → Q계열 요청은 Q1로
CAB_NAME = {118:'KSL8',121:'KSL12',137:'XSL8',140:'XSL12',98:'Y8',99:'Y12',110:'GSL8',
            113:'GSL12',73:'V8',76:'V12',153:'CCL8',156:'CCL12',92:'J8',93:'J12',
            124:'AL60',128:'AL90',50:'T10',
            39:'E8-50x90',40:'E12-80x50',56:'E6-100x55',72:'E5',71:'E4',
            91:'V10P-110x40',90:'V7P-40x75',82:'Y10P-110x40',81:'Y7P-40x75',
            37:'M4-act-70x50',21:'M2',54:'M6-50x80',134:'44S-30x90',105:'24S-75x45',
            59:'8S',58:'5S',38:'Q1',151:'U7-55x80',150:'U5-90x60',149:'U3-100x65',
            114:'SL-SUB',75:'V-SUB',88:'Y-SUB',131:'KSL-SUB',159:'CCL-SUB',
            34:'J-SUB',47:'J-INFRA',101:'B22-SUB',122:'B8-SUB',83:'B6-SUB',52:'B4-SUB',
            15:'E12-SUB',41:'E15-SUB',107:'21S-SUB',66:'18S-SUB',148:'B10N-SUB',163:'B12-SUB',3:'Q-SUB',141:'XSL-SUB',142:'XSL-SUB'}
# ArrayCalc가 인식하는 시리즈(System) 문자열 — 모델id와 다름 주의(V→V-Series 등). 잘못되면 크래시.
SYS = {'KSL':'KSL','GSL':'GSL','XSL':'XSL','V':'V-Series','Y':'Y-Series','Y-Series':'Y-Series',
       'T':'T-Series','A':'A-Series','J':'J-Series','CCL':'CCL','E8':'E-Series','E-Series':'E-Series'}
def sysOf(m): return SYS.get(m, m)
# 캐비닛 높이(m) — 공식 예제 이웃 캐비닛 3D 간격 중앙값 실측(260723). 미등록은 0.34.
CAB_H = {'GSL':0.394,'KSL':0.332,'XSL':0.285,'J':0.362,'V':0.311,'Y':0.257,'Y-Series':0.257,'A':0.33,'T':0.20,'CCL':0.21}
def cab_h(fam): return CAB_H.get(fam,0.34)
# 서브 플라잉 컬럼 세로 높이(m) — 매뉴얼 치수 근사(하중·위치 초기값, ArrayCalc가 정밀 재계산)
SUB_H = {'SL-SUB':0.52,'KSL-SUB':0.45,'V-SUB':0.54,'Y-SUB':0.31,'J-SUB':0.72,'J-INFRA':0.72,'CCL-SUB':0.30,'T-SUB':0.27,
         'XSL-SUB':0.56,'B22-SUB':0.63,'B8-SUB':0.30,'B6-SUB':0.30,'B4-SUB':0.22,'E12-SUB':0.36,'E15-SUB':0.44,
         '21S-SUB':0.63,'18S-SUB':0.54,'27S-SUB':0.72,'12S-SUB':0.36}
# 서브 대표 무게(kg) — 통합 행잉 하중 안내용(매뉴얼 근사)
SUB_KG = {'SL-SUB':61,'KSL-SUB':39,'V-SUB':41,'Y-SUB':24,'J-SUB':63,'J-INFRA':66,'CCL-SUB':22,'T-SUB':23,
          'XSL-SUB':40,'B22-SUB':98,'B8-SUB':24,'B6-SUB':16,'B4-SUB':13,'E12-SUB':24,'E15-SUB':32,
          '21S-SUB':71,'18S-SUB':44,'27S-SUB':83,'12S-SUB':21}
def sub_h(name): return SUB_H.get(name,0.5)
# 통합 행잉(같은 프레임) 호환 — 라인어레이별 전용 서브만(예제 실측: KSL그룹=KSL-SUB, J=J-SUB).
# KSL≠XSL: 같은 SL-Series여도 프레임이 달라 통합 불가(사용자 지적). SL-SUB(대형)은 GSL/KSL 공용.
LINE_SERIES={'GSL':'SL','KSL':'SL','XSL':'SL','V':'V','Y':'Y','J':'J','A':'A','T':'T','CCL':'CCL'}
# 통합 행잉 호환 = 프레임 폭 일치(같은 리깅에 함께 걸림). d&b 공식: 각 라인어레이는 자기 폭 전용 서브만 통합 비행.
# SL-SUB/GSUB=GSL 폭(≈1046mm, "GSL8/12용, 메인과 동일 폭"), KSL-SUB=KSL 폭(1000mm, "KSL과 동일 폭·혼합 어레이"), XSL-SUB=XSL 폭.
# → GSL↔SL-SUB, KSL↔KSL-SUB, XSL↔XSL-SUB 교차 불가(폭 다름). A-Series는 전용 통합 비행 서브 없음(생략).
COMPAT_SUB={
 'GSL':['SL-SUB','SL-GSUB'],
 'KSL':['KSL-SUB'],
 'XSL':['XSL-SUB','XSL-GSUB'],
 'V':['V-SUB','V-GSUB'],
 'Y':['Y-SUB'],
 'J':['J-SUB','J-INFRA'],
 'T':['T-SUB'],
 'CCL':['CCL-SUB'],
}
def same_series(line_mdl, sub_mdl):
    return sub_mdl in COMPAT_SUB.get(line_mdl, [])
warnings = []

# 바이앰프(캐비닛당 2채널, ch1+2/ch3+4 페어) SpeakerId — 예제 전수 실측
CH2_IDS={118,121,110,113,137,140,92,93,37,114,131,34,47,141,142}   # KSL/GSL/XSL/J 라인, M4, SL-SUB/KSL-SUB/J-SUB/J-INFRA/XSL-SUB
CH2_LINK2={118,121,137,140,92,93}   # 바이앰프 중 Line/Arc 세팅으로 채널쌍당 2통 허용(KSL/XSL/J 매뉴얼 실측). GSL·SL계열 서브·M4는 1 고정
# 1ch 모델 채널당 최대 병렬 통수(예제 실측 최대 + 매뉴얼). 미등록=1 안전.
LINK1_MAX={39:2,40:2,56:2,72:2,71:2,134:2,105:2,59:3,58:4,151:2,150:2,149:2,
 98:2,99:2,73:2,76:2,124:2,128:2,50:2,153:2,156:2,91:2,90:2,82:2,81:2,
 38:2,3:2,75:2,88:2,122:2,83:2,52:2,15:2,41:2,107:2,66:2,159:2,
 21:1,54:1,101:1}
# 프레임별 플라잉 한계(공식 페이지, XSL만 모드 구분 공표): {컴프레션, 텐션, 마운팅프레임}
FRAME_LIMITS={'XSL':{'comp':24,'ten':22,'mount':12}}
# 스피커별 호환 앰프(공식 ExampleProjects 전수 추출, 260723). 첫 항목=교체 기본값.
AMP_OK={
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
 51:['D80','D20','10D'],67:['D20','30D','40D'],68:['D20','30D'],159:['D40'],160:['D40'],141:['D40','D80','D90','40D'],142:['D40','D80','D90','40D'],
}
# 데이터 출처·검증일 — 갱신 시 무엇을 재확인해야 하는지 추적 (v1.17)
DATA_PROV={
 'AMP_OK':      {'source':'공식 ExampleProjects 전수(Cabinets⋈Devices) + V8/XSL8 제품 페이지 대조','verified':'2026-07-23',
                 'note':'V8+D90은 제품 페이지 앰프 목록엔 없고 성능표·D90 페이지·예제에 근거(supported)'},
 'CH2_IDS':     {'source':'예제 전수 실측(캐비닛 채널 배치)','verified':'2026-07-23'},
 'CH2_LINK2':   {'source':'KSL/XSL/J/GSL/KSL-SUB 매뉴얼 Operation 표(Cabinets per pair)','verified':'2026-07-23'},
 'SPLAY_MAX':   {'source':'예제 전수 실측 SplayAngle 최대값','verified':'2026-07-23'},
 'FLY_MAX':     {'source':'매뉴얼 통수(컴프레션 모드 기준) — 프레임/텐션별 세분은 ArrayCalc 확인','verified':'2026-07-22'},
 'CAB_H':       {'source':'예제 이웃 캐비닛 3D 간격 중앙값 실측','verified':'2026-07-23'},
 'OutputMode':  {'source':'예제 통계(바이앰프 704/709=8, 1ch 622/656=0)','verified':'2026-07-23'},
 'SNAP_PROPS':  {'source':'Y-Series 예제 채널별 스냅샷 속성 세트','verified':'2026-07-23'},
 'LINK1_MAX':   {'source':'예제 실측 채널당 최대 통수 + 매뉴얼(Y 2/ch 등)','verified':'2026-07-23'},
 'FRAME_LIMITS':{'source':'XSL8 제품 페이지(컴프레션 24/텐션 22/마운팅 12) — 타 시리즈는 24 단일 공표','verified':'2026-07-23'},
}
def amp_fix(part,sid,amp):
    """스피커에 안 맞는 앰프면 호환 기본값으로 자동 교체(+경고)."""
    ok=AMP_OK.get(sid)
    if not ok or amp in ok: return amp
    w=f"⚠ {part}: {amp}는 이 스피커 미지원 → {ok[0]}로 자동 교체"
    if w not in warnings: warnings.append(w)
    return ok[0]
# 파트별 리모트 서브넷(유닛 ID = 서브넷.번호) — 현장 지시용 체계
PART_SUBNET={'MAIN':1,'G.SUB':2,'Front fill':3,'DELAY':4,'CENTER':5,'OUT':6}
def subnet_of(part):
    for k,v in PART_SUBNET.items():
        if part.startswith(k) or part.upper().startswith(k): return v
    return 7

# ── 안전 한계(매뉴얼 실측) — 절대 초과 생성 금지. 초과분은 하드 클램프 + 경고. ──
# 인터캐비닛 최대 스플레이(°)
SPLAY_MAX = {'KSL':10,'GSL':7,'XSL':14,'V':14,'Y':14,'Y-Series':14,'CCL':14,'J':7,'A':40,'T':15}   # 공식 예제 전수 실측(260723)
# 프레임 구조상 최대 통수(플라잉). 실제 하중은 ArrayCalc가 로드 시 재계산(리깅 NULL)해 green/red로 표시 = 최종 권위.
FLY_MAX   = {'KSL':24,'GSL':24,'XSL':24,'V':24,'Y':24,'Y-Series':24,'CCL':24,'J':24,'A':16,'T':16}
STACK_MAX = 8
STK_MAX = {'GSL':6,'KSL':6,'J':6}   # 나머지 8
def clamp_line(mdl, boxcount, splays, mount):
    lim = STK_MAX.get(mdl,STACK_MAX) if mount=='stack' else FLY_MAX.get(mdl,16)
    n = max(1, min(int(boxcount), lim))
    if int(boxcount) > lim:
        warnings.append(f"⚠ {mdl} {'그라운드스택' if mount=='stack' else '플라잉'} {boxcount}통 → 구성 한계(매뉴얼 최대 통수) {lim}통으로 제한")
    fl=FRAME_LIMITS.get(mdl)
    if fl and mount!='stack' and n>fl['ten']:
        w=f"ℹ {mdl} {n}통: 컴프레션 모드 최대 {fl['comp']}통 기준 — 텐션 모드는 최대 {fl['ten']}통, 마운팅 프레임은 {fl['mount']}통 (ArrayCalc Rigging Plot 확인)"
        if w not in warnings: warnings.append(w)
    smax = SPLAY_MAX.get(mdl,10); over=False; sp=[]
    for s in (splays or []):
        v=max(0.0,min(float(s),smax)); over=over or float(s)>smax; sp.append(v)
    if over: warnings.append(f"⚠ {mdl} 스플레이 {smax}° 초과 → {smax}°로 제한")
    sp=(sp[:n]+[0.0]*n)[:n]
    return n, sp

def alt(mdl,kind):
    if mdl in ALT:
        w=f"ℹ {mdl}: ArrayCalc 예제에 없는 모델 → {ALT[mdl]}(으)로 대체"
        if w not in warnings: warnings.append(w)
        return ALT[mdl]
    return mdl

def variants(n,n8,i8,n12,i12):
    split=max(1,R(n*0.6)); return [(n8,i8) if i<split else (n12,i12) for i in range(n)]

def apply_manual_variants(bx, nm, mv):
    "UI에서 통별 8/12 수동 지정(variants: 0=상단기종/1=하단기종 배열)이 오면 자동 배분 위에 덮어씀"
    if not mv: return bx
    pair=[(nm[0],nm[1]),(nm[2],nm[3])]
    for i in range(min(len(bx),len(mv))):
        bx[i]=pair[1 if mv[i] else 0]
    return bx

# 시리즈별 플라잉 프레임 이름(ArrayCalc 예제 실측)
FRAME_NAME={'GSL':'GSLFlyingFrame','KSL':'KSLFlyingFrame','XSL':'XSLFlyingFrame','V':'VFlyingFrame','Y':'YFlyingFrame','J':'JFlyingFrame','A':'AFlyingFrame','T':'TFlyingFrame','CCL':'CCLFlyingFrame'}
# 프레임 홀 지오메트리(ArrayCalc 저장본에서 역산, 좌표 1e-16 일치): (A, pitch, rear홀)
#   X_local(hole)=A-pitch*hole ,  Position=0.025+pitch*hole ,  절대좌표는 수평조준각으로 회전
# 미검증 시리즈는 여기 없으면 프레임 안 씀(안전 베이스라인) — 크래시 방지.
FRAME_GEO={'GSL':(0.10825,0.04,32),'KSL':(0.01,0.0404,25),'XSL':(-0.046,0.033619,21),'Y':(-0.024,0.016,44),'V':(-0.02019,0.018,39),'J':(-0.028,0.024671,38),'A':(-0.0151,0.0174,27),'T':(-0.025,0.014,36),'CCL':(-0.016,0.016381,42)}   # Y: ArrayCalc 실측(260728) rear44,pitch0.016   # XSL: ArrayCalc 자동프레임 실측(260728) X_local(0)=-0.046,X_local(21)=-0.752
# 싱글픽 홀 = 프레임 앞끝 기준 CoG 위치 → 홀. CoG는 스플레이 아크로 계산, 시리즈별 베이스오프셋 보정
# (ArrayCalc 저장본 3점 대조: FRONT→12, CENTER→14, OUT→15 모두 ±1홀 이내)
COG_BASE={'GSL':0.42,'KSL':0.29,'XSL':0.20,'Y':0.15,'V':0.217,'J':0.307,'A':0.21,'T':0.143,'CCL':0.189}   # XSL: 단일홀6.016 역산(260728), 1점식 XSL용(듀얼은 무관)
# TotalWeight = 통수×통무게 + 프레임무게 (ArrayCalc 저장본 역산: GSL 9/12/25통 → 79.9375/통 +72 프레임, 정확일치)
CAB_W={'GSL':79.9375,'KSL':56.744,'XSL':39.0,'Y':20.35,'V':33.278,'J':63.9,'A':21.225,'T':10.545,'CCL':16.435}; FRAME_W={'GSL':72.0,'KSL':62.0,'XSL':31.3,'Y':18.62,'V':30.0,'J':44.0,'A':20.0,'T':15.0,'CCL':24.0}   # KSL은 OUT 16통(969.9)로 캘리브레이션 · XSL은 6통 265.292로(ArrayCalc가 로드시 재계산하므로 근사값)
class Builder:
    def __init__(self): self.sql=["BEGIN;"]; self.dev=10; self.cid=100; self.sg=1; self.ap=1; self.ff=1; self.parts={}; self.subseq={}; self.devinfo={}
    def flying_frame(self,sg,mdl,horiz,ox,oy,oz,single,cog_hole,ncab=0,tilt=0):
        """유효 픽 데이터로 플라잉 프레임 기록(크래시 방지: 홀·좌표 유효 + LoadBeamPosition='standard').
        single=True→1점식(SinglePickPointHole 지정), False→2점식(front/rear). 좌표는 항상 유효값 기록.
        ncab: 이 그룹 통수(TotalWeight 계산용, −1이면 ArrayCalc가 하중 'invalid' 표시).
        tilt: 어레이 전체 조준각(도). ArrayCalc는 캐비닛 절대각을 FrameAngle+스플레이누적으로 재계산하므로
              FrameAngle=-tilt로 써야 베이스 틸트가 적용됨(0이면 스플레이만 적용, 틸트 소실)."""
        import math
        geo=FRAME_GEO.get(mdl)
        if not geo: return   # 지오메트리 미검증 시리즈 → 프레임 생략(ArrayCalc가 자동생성, 안전)
        A,pitch,rear=geo
        h=math.radians(horiz or 0)
        ch=cog_hole
        ch=max(1,min(rear-1,int(round(ch))))          # 1점식/CoG 홀 클램프
        # 2점식 프론트홀=0(맨앞) — CoG보다 항상 앞이라 두 픽이 CoG를 straddle → 하중 항상 유효.
        # (front=rear//2로 두면 GSL에서 CoG 뒤로 가 프론트픽 음하중=invalid. ArrayCalc 자동값도 front0)
        fh=0
        def pk(hole):
            xl=A-pitch*hole
            return (ox+xl*math.cos(h), oy+xl*math.sin(h), 0.025+pitch*hole)
        fx,fy,fpos=pk(fh); rx,ry,rpos=pk(rear); sx,sy,spos=pk(ch)
        srh=(ch if single else -1)                    # SinglePickPointHole: 1점식일 때만 실홀, 2점식은 -1
        tw=(R(ncab*CAB_W.get(mdl,60.0)+FRAME_W.get(mdl,65.0),4) if ncab>0 else -1)   # TotalWeight(하중 유효화)
        ff=self.ff; self.ff+=1; disp=FRAME_NAME.get(mdl).replace('FlyingFrame',' Flying frame')
        self.sql.append("INSERT INTO FlyingFrames(FlyingFrameId,Type,Name,DisplayName,SourceGroupId,PositionIndex,FrameAngle,FrontPickPointHole,RearPickPointHole,SinglePickPointHole,TotalWeight,FrontPickPointWeight,RearPickPointWeight,FrontPickPointWeightZeroDegrees,RearPickPointWeightZeroDegrees,FrontPickX,FrontPickY,RearPickX,RearPickY,SinglePickX,SinglePickY,FrontPickPointPosition,RearPickPointPosition,SinglePickPointPosition,OriginX,OriginY,OriginZ,LoadBeamPosition) VALUES("
            f"{ff},2,'{FRAME_NAME.get(mdl)}','{disp}',{sg},1,{R(-float(tilt or 0),2)},{fh},{rear},{srh},{tw},-1,-1,-1,-1,"
            f"{R(fx,6)},{R(fy,6)},{R(rx,6)},{R(ry,6)},{R(sx,6)},{R(sy,6)},"
            f"{R(fpos,4)},{R(rpos,4)},{R(spos,4)},{R(ox,2)},{R(oy,2)},{R(oz,2)},'standard');")
    def reg(self,part,dev,ch):
        self.parts.setdefault(part,[]).append((dev,ch))
    def newdev(self,model,part,ch2=False):
        """파트 서브넷 기반 유닛ID(예: MAIN → 1.01,1.02…)와 이름을 자동 부여. 바이앰프는 OutputMode=8(2-Way Active)."""
        d=self.dev; self.dev+=1; e=self.sql.append
        sn=subnet_of(part)
        seq=self.subseq.get(sn,0)+1; self.subseq[sn]=seq
        label=f"{part} {sn}.{seq:02d}"
        e(f"INSERT INTO Devices(DeviceId,Model,RemoteIdSubnet,RemoteIdDevice,Name) VALUES({d},'{model}',{sn},{seq},'{label}');")
        e(f"INSERT INTO DevicesAmplifier(DeviceId,InputMode,OutputMode) VALUES({d},0,{8 if ch2 else 0});")
        self.devinfo[d]={'label':label,'model':model,'chn':{},'cnt':{},'dms':getattr(self,'_dms',0.3)}
        return d
    def chname(self,d,lead,pair,label):
        """채널 이름 + 입력패치(리드 포트만) 기록 — flushdev에서 일괄 INSERT."""
        self.devinfo[d]['chn'][lead]=label
        self.devinfo[d].setdefault('leads',[]).append(lead)
        if pair: self.devinfo[d]['chn'][pair]=label
    def flushdev(self):
        e=self.sql.append
        for d,info in self.devinfo.items():
            names=[info['chn'].get(ch,'') for ch in (1,2,3,4)]
            vals=",".join(f"({d},{ch},'{names[ch-1]}')" for ch in (1,2,3,4))
            e(f"INSERT INTO AmplifierChannels(DeviceId,AmplifierChannel,Name) VALUES {vals};")
            leads=sorted(set(ch for ch in info['chn'] if info['chn'][ch] and (ch==1 or info['chn'].get(ch-1)!=info['chn'][ch])))
            for ch in leads:
                e(f"INSERT INTO PatchIOChannels(DeviceId,Type,PortNumber,Name,Protocol) VALUES({d},1,{ch},'{info['chn'][ch]}',5);")
        self.flushsnap()
    # ── 스냅샷: ArrayCalc가 채널 입력소스(Config_InputEnable)·상태를 여기서 읽음.
    #    없으면 Project report에 'No input source selected for channel' 경고(1ch 모델들, 260723 실측).
    #    공식 Y-Series 예제의 채널별 속성 세트를 그대로 재현(입력 1=아날로그 A 활성).
    SNAP_PROPS=[('Config_InputEnable1','1.0'),('Config_InputEnable2','0.0'),('Config_InputEnable3','0.0'),
        ('Config_InputEnable4','0.0'),('Config_InputEnable5','0'),('Config_InputEnable6','0'),
        ('Config_InputEnable7','0'),('Config_InputEnable8','0'),
        ('Config_LoadMatchSpeakerCount','1'),('Config_LoadMatchCableLength','30'),
        ('Config_LoadMatchCableCrossSection','4.0'),('Config_DelayOn','1'),('ChStatus_MsDelay','0.3'),
        ('Config_Mute','0'),('Config_PotiLevel','0.0'),
        ('Config_Filter1','0'),('Config_Filter2','0'),('Config_Filter3','0')]
    def flushsnap(self):
        e=self.sql.append
        created=f"20{self.snapdate[0:2]}-{self.snapdate[2:4]}-{self.snapdate[4:6]}T00:00:00.000Z" if getattr(self,'snapdate',None) else "2026-01-01T00:00:00.000Z"
        e(f"INSERT INTO Snapshots(SnapshotId,Type,Name,Comment,CreatedOn) VALUES(1,0,'ArrayCalc snapshot','Snapshot created automatically by ArrayCalc','{created}');")
        svid=1
        for d,info in self.devinfo.items():
            for ch in sorted(set(info.get('leads',[]))):
                for prop,val in self.SNAP_PROPS:
                    if prop=='Config_LoadMatchSpeakerCount': val=str(info['cnt'].get(ch,1))
                    elif prop=='ChStatus_MsDelay': val=str(info.get('dms',0.3))
                    e(f"INSERT INTO SnapshotValues(SnapshotValueId,SnapshotId,SnapshotTargetType,Value,TargetId,TargetNode,TargetProperty,TargetRecord) VALUES({svid},1,0,{val},{d},{ch},'{prop}',0);")
                    svid+=1
    def sgroup(self,typ,name,system,amp,sym=0,mounting=1,ox=0,oy=0,oz=0,frame=0,hle=0,horiz=0,nxt=0,ordr=None,single_rig=None,rear_rig=None,front_rig=None):
        sg=self.sg; self.sg+=1; e=self.sql.append
        e(f"INSERT INTO SourceGroups(SourceGroupId,Type,Name,OrderIndex,RemarkableChangeDate,NextSourceGroupId,ArrayProcessingEnable,ArraySightId,LinkMode,Symmetric,Mounting,RelativeDelay) VALUES({sg},{typ},'{name}',{sg if ordr is None else ordr},0,{nxt},0,0,0,{sym},{mounting},NULL);")
        # 리깅 하중 필드는 NULL로 유지 — 값을 채우면 ArrayCalc가 플라잉 하중계산을 시도하다 프레임 없어서 크래시.
        # ArrayCalc가 로드 시 스스로 재계산하게 둠(기프티드 파일이 이 방식으로 정상 오픈).
        _srp=('NULL' if single_rig is None else str(int(single_rig)))   # 1점식(rigPts=1)이면 1
        # PROBE: 픽 홀 번호(RearRiggingPoint/FrontRiggingPoint)만 지정 → FlyingFrames 행 없이 틸트 유도 시험.
        _rr=('NULL' if rear_rig is None else str(int(rear_rig)))
        _fr=('NULL' if front_rig is None else str(int(front_rig)))
        e(f"INSERT INTO SourceGroupsAdditionalData(SourceGroupId,System,HorizontalAiming,StackedFrameAngle,HasPrevious,DefaultRemoteIdSubnet,DefaultRemoteIdDevice,ShowRigging,SelectedArrayProcessingSlotNumber,BoxType,NominalDispersionAngle,OriginX,OriginY,OriginZ,HeightLowestEdge,VerticalAimingAngle,CompressionModeEnable,CompressionForce,CompressionGrabLinkPosition,MaxLoadTension,MaxLoadTensionBGV,MaxLoadCompression,MaxLoadCompressionBGV,DefaultAmplifierType,RearRiggingPoint,FrontRiggingPoint,SingleRiggingPoint) VALUES({sg},'{system}',{horiz},{frame},{1 if ordr==-1 else 0},0,1,1,NULL,'',0,{ox},{oy},{oz},NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'{amp}',{_rr},{_fr},{_srp});")
        if typ==1:   # 라인어레이: AP 슬롯 기본 10개(공식 예제 기본값) — 없으면 열 때 경고 뜸
            for slot in range(1,11):
                apid=self.ap; self.ap+=1
                nm2='Bypass' if slot==1 else ''
                cm2='This slot is reserved for bypassing ArrayProcessing.' if slot==1 else ''
                e(f"INSERT INTO ArrayProcessingSlots(ArrayProcessingSlotId,SourceGroupId,Slot,Name,Comment,SessionId,CreatedOn,Flags) VALUES({apid},{sg},{slot},'{nm2}','{cm2}','','1970-01-01T01:00:00.000',1);")
                e(f"INSERT INTO ArrayProcessingSlotsAdditionalData(ArrayProcessingSlotId,Slope1,Slope2,Slope3,Point1X,Point2X,Temperature,Humidity,VenueObjectIdSelected,PowerGlory,SourceGroupTargetProfile) VALUES({apid},0.0,-3.0,-3.0,0.0,0.0,293.16,60.0,1,0.5,'');")
        return sg
    def cab(self,dv,ch,spk,sg,pos,h,v,x,y,z,splay,delay=0):
        c=self.cid; self.cid+=1; nm=CAB_NAME.get(spk,'Linear'); e=self.sql.append
        e(f"INSERT INTO Cabinets(CabinetId,DeviceId,AmplifierChannel,SpeakerId,SourceGroupId,PositionIndex,OrderIndex,HorizontalAngle,VerticalAngle,RotationAngle,PivotAngle,Linked,OriginX,OriginY,OriginZ,HornRotationAngle) VALUES({c},{dv},{ch},{spk},{sg},{pos},1,{h},{v},0,0,0,{x},{y},{z},0);")
        e(f"INSERT INTO CabinetsAdditionalData(CabinetId,Name,ControllerSetup,SplayAngle,AlignmentToSubArrayTestPoint,CabinetsPerPosition,CompressionState,DraftSignalSourceDeviceId,DraftSignalSourceChannelNumber,Delay,Mute,Level,Switch1,Switch2,Switch3,Switch4,Switch5,PreviousObjectString,NextObjectString) VALUES({c},'{nm}',0,{splay},0,1,0,NULL,NULL,{delay},0,0,0,0,0,-5.5,0.5,NULL,NULL);")
    def place_subs_top(self,sg,spk,subn,amp,part,topz,subH,side_y,ox,link,pos_start):
        """통합 행잉: 라인어레이 그룹(sg) 최상단에 서브 캐비닛 배치(별도 앰프 디바이스). 서브 아래 z 반환."""
        amp=amp_fix(part,spk,amp)
        ch2=(spk in CH2_IDS); lk=1 if ch2 else max(1,int(link or 1)); cap=2 if ch2 else 4*lk
        d=None; slot=0; grp=0; z=topz
        for i in range(subn):
            if slot%cap==0: d=self.newdev(amp,part,ch2); slot=0
            lead=(slot//lk*2+1) if ch2 else (slot//lk+1); pair=(lead+1) if ch2 else 0
            if slot%lk==0:
                grp+=1; self.chname(d,lead,pair,f"{part} {grp:02d}")
            self.devinfo[d]['cnt'][lead]=self.devinfo[d]['cnt'].get(lead,0)+1
            slot+=1
            self.cab(d,lead,spk,sg,pos_start+i,0,0,R(-i*0.02,2),side_y,R(z,2),0); self.reg(part,d,lead); z-=subH
        return R(z,2)
    def line_array(self,name,system,amp,side_y,topz,tilt,boxes,splays,mount='flown',ox=0,horiz=0,gname=None,nxt=0,sym=0,ordr=None,link=1,dms=0.3,subtop=None,rigpts='2'):
        amp=amp_fix(name,boxes[0][1],amp)   # 스피커-앰프 호환 자동 교정
        self._dms=dms
        if int(link or 1)>1 and boxes[0][1] in CH2_LINK2:
            w=f"ℹ {name}: 링크 1:2(Line/Arc 세팅) — 앰프에서 Line/Arc 셋업 선택 필요, ArrayProcessing 사용 불가"
            if w not in warnings: warnings.append(w)
        stack=(mount=='stack'); n0=len(boxes)
        ch_=cab_h(system)                                          # 모델별 캐비닛 높이(실측)
        # 통합 행잉 서브(플라잉 전용): 서브가 최상단, 라인어레이는 그 아래로 낮춤
        subN=(subtop['n'] if (subtop and not stack) else 0); subH_=(subtop['h'] if subN else 0)
        line_top=(R(topz-(subN*subH_+0.3),2) if subN else topz)
        oz=(0 if stack else topz)                                  # 그룹 원점=프레임/트림(서브가 여기 매달림)
        hle=(0.3 if stack else max(R(line_top - n0*ch_ - 0.3,2),0.2))   # 최하단 통 높이
        # ArrayCalc는 SourceGroup 원점으로 배치 → 어레이 위치를 여기서 지정(X 깊이, Y 좌우, Z 높이/비행점)
        # 1점식(rigPts=1) 플라잉 → SingleRiggingPoint=1(primary)/0(mirror). Dual/스택 → NULL.
        # (유효 FlyingFrames와 함께여야 크래시 없음 — ArrayCalc 저장본으로 검증됨)
        _single=(str(rigpts)=='1' and not stack)
        _srp=(1 if (_single and ordr!=-1) else (0 if _single else None))   # mirror(ordr=-1)는 0
        sg=self.sgroup(1,gname or name,sysOf(system),amp,sym=sym,mounting=(1 if stack else 0),ox=ox,oy=side_y,oz=oz,frame=(tilt if stack else 0),hle=hle,horiz=horiz,nxt=nxt,ordr=ordr,single_rig=_srp)
        pos0=1
        if subN:                                                  # 같은 그룹 최상단에 서브 → ArrayCalc 통합 행잉·통합 하중
            self.place_subs_top(sg,subtop['spk'],subN,subtop['amp'],subtop['part'],topz,subH_,side_y,ox,subtop.get('link',1),pos0)
            pos0+=subN
        n=len(boxes); d=None; z=(1.4 if stack else line_top); cum=0; slot=0; grp=0; cums=[]
        ch2=(boxes[0][1] in CH2_IDS)
        lk=(min(int(link or 1),2) if boxes[0][1] in CH2_LINK2 else 1) if ch2 else max(1,int(link or 1))
        cap=2*lk if ch2 else 4*lk                                 # 디바이스당 캐비닛 수(병렬 링크 반영)
        for i,(bn,bid) in enumerate(boxes):
            if slot%cap==0: d=self.newdev(amp,name,ch2); slot=0
            if ch2: lead=(slot//lk)*2+1; pair=lead+1
            else:   lead=slot//lk+1; pair=0
            if slot%lk==0:
                grp+=1; self.chname(d,lead,pair,f"{name} {grp:02d}")
            self.devinfo[d]['cnt'][lead]=self.devinfo[d]['cnt'].get(lead,0)+1
            slot+=1
            if stack:                                            # 바닥부터 위로, 상단으로 갈수록 위 향함(상향 라운드)
                sp_i=splays[n-1-i] if (n-1-i)<len(splays) else 0; cum+=sp_i; v=-(tilt-cum)
                self.cab(d,lead,bid,sg,pos0+i,0,R(v,1),R(-i*0.02,2),side_y,R(z,2),R(sp_i,1)); self.reg(name,d,lead); z+=ch_
            else:                                                # 플라잉: 상단부터 아래로 걸림
                sp_i=splays[i] if i<len(splays) else 0; cum+=sp_i; v=-(tilt+cum)
                self.cab(d,lead,bid,sg,pos0+i,0,R(v,1),R(-i*0.02,2),side_y,R(z,2),R(sp_i,1)); self.reg(name,d,lead); z-=ch_; cums.append(cum)
        _fs=(system if system in FRAME_GEO else system.replace('-Series',''))   # 프레임은 모델키(Y) 기준 — sysOf는 'Y-Series'라 매칭 실패했었음
        if not stack and _fs in FRAME_GEO:              # 플라잉 프레임 기록(유효 픽 → 크래시 방지)
            import math
            A,pitch,_rear=FRAME_GEO[_fs]
            x=0.0; cxs=0.0                              # 캐비닛 체인(스플레이 아크) 재구성 → CoG 전후방 위치
            for cc in cums:
                dx=ch_*math.sin(math.radians(cc)); cxs+=x+0.5*dx; x+=dx
            cogx=(cxs/len(cums)) if cums else 0.0
            cog_hole=(cogx+COG_BASE.get(_fs,0.4)-0.025)/pitch    # 프레임 앞끝 기준 CoG위치 → 싱글홀
            self.flying_frame(sg,_fs,horiz,ox,side_y,oz,single=(str(rigpts)=='1'),cog_hole=cog_hole,ncab=subN+n,tilt=tilt)
        return sg
    def point_row(self,name,system,amp,spk,ys,zpos,aim,xpos=0.0,sym=0,link=1,dms=0.3,horiz=0):
        amp=amp_fix(name,spk,amp); self._dms=dms
        # 포인트 열: 폭(Y)으로 퍼지고, 깊이(X)=xpos 고정, 높이(Z)=zpos. (기존 X/Y 축 뒤바뀜 버그 수정)
        sg=self.sgroup(2,name,system,amp,sym=sym); d=None; slot=0; grp=0
        ch2=(spk in CH2_IDS)
        lk=(min(int(link or 1),2) if spk in CH2_LINK2 else 1) if ch2 else max(1,int(link or 1))
        cap=2*lk if ch2 else 4*lk
        for i,y in enumerate(ys):
            if slot%cap==0: d=self.newdev(amp,name,ch2); slot=0
            if ch2: lead=(slot//lk)*2+1; pair=lead+1
            else:   lead=slot//lk+1; pair=0
            if slot%lk==0:
                grp+=1; self.chname(d,lead,pair,f"{name} {grp:02d}")
            self.devinfo[d]['cnt'][lead]=self.devinfo[d]['cnt'].get(lead,0)+1
            slot+=1
            _h=R(horiz if y<0 else (-horiz if y>0 else horiz),1)   # 토우: L=+, R=-(안쪽), 단일=그대로
            self.cab(d,lead,spk,sg,i+1,_h,R(aim,1),R(xpos,2),R(y,2),R(zpos,2),0); self.reg(name,d,lead)
        return sg
    def sub_stack(self,name,system,amp,spk,positions,ox=0,oy=0,sym=0,link=1,dms=0.3):
        amp=amp_fix(name,spk,amp); self._dms=dms
        sg=self.sgroup(3,name,system,amp,ox=ox,oy=oy,sym=sym); d=None; slot=0; grp=0
        ch2=(spk in CH2_IDS)
        lk=(min(int(link or 1),2) if spk in CH2_LINK2 else 1) if ch2 else max(1,int(link or 1))
        cap=2*lk if ch2 else 4*lk
        for i,pt in enumerate(positions):
            x,y,z=pt[0],pt[1],pt[2]; hang=pt[3] if len(pt)>3 else 0; dly=pt[4] if len(pt)>4 else 0
            if slot%cap==0: d=self.newdev(amp,name,ch2); slot=0
            if ch2: lead=(slot//lk)*2+1; pair=lead+1
            else:   lead=slot//lk+1; pair=0
            if slot%lk==0:
                grp+=1; self.chname(d,lead,pair,f"{name} {grp:02d}")
            self.devinfo[d]['cnt'][lead]=self.devinfo[d]['cnt'].get(lead,0)+1
            slot+=1
            self.cab(d,lead,spk,sg,i+1,hang,0,R(x,2),R(y,2),R(z,2),0.5,dly); self.reg(name,d,lead)
        return sg
    def point_stack_combo(self,mname,msys,mspk,ys,mz,maim,mx,sname,ssys,sspk,sbox,slink,x_sub,subh,amp,sym=1):
        """포인트-스택 메인 + 서브를 한 앰프(≤4채널)에 통합. 비바이앰프 전용.
        서브 링크 반영: 서브채널=ceil(sbox/slink), 채널당 slink통을 측 밑에 Z스택. 반환 (메인 sgroup, 서브 sgroup)."""
        d=self.newdev(amp,'MAIN',False); lead=1
        sgm=self.sgroup(2,mname,msys,amp,sym=sym)   # 메인 포인트 소스그룹
        sgs=self.sgroup(3,sname,ssys,amp,sym=sym)   # 서브 소스그룹
        mCh=len(ys); slink=max(1,int(slink)); sCh=(-(-int(sbox)//slink)) if sbox else 0; spos=0
        # 채널 순서: 측별 탑→서브 인터리브(A=L탑,B=L서브,C=R탑,D=R서브) — 4코어 A/B·C/D로 측당 통합 결선
        for i in range(max(mCh,sCh)):
            if i<mCh:
                y=ys[i]; lbl=(f"{mname} "+('L' if y<0 else 'R')) if mCh==2 else f"{mname} {i+1:02d}"
                self.chname(d,lead,0,lbl); self.devinfo[d]['cnt'][lead]=self.devinfo[d]['cnt'].get(lead,0)+1
                self.cab(d,lead,mspk,sgm,i+1,0,R(maim,1),R(mx,2),R(y,2),R(mz,2),0); self.reg(mname,d,lead); lead+=1
            if i<sCh:
                sy=ys[i] if i<mCh else ys[i%mCh]
                lbl=(f"{sname} "+('L' if sy<0 else 'R')) if sCh==2 else f"{sname} {i+1:02d}"
                self.chname(d,lead,0,lbl)   # 채널명 1회, 링크된 서브 여러 통을 이 채널에
                _nc=min(slink, int(sbox)-i*slink)
                for k in range(_nc):
                    spos+=1; self.devinfo[d]['cnt'][lead]=self.devinfo[d]['cnt'].get(lead,0)+1
                    self.cab(d,lead,sspk,sgs,spos,0,0,R(x_sub,2),R(sy,2),R(k*subh,2),0.5); self.reg(sname,d,lead)
                lead+=1
        return sgm,sgs


# ── R1 원격 오버뷰 — AudioAZ+Gadget.dbpr(사용자 원본)을 디자인 도너로 그대로 재현. ──
R1_DONOR_NAME="AudioAZ+Gadget.dbpr"
R1_TABLES=['ViewTypes','ControlTypes','TargetTypes','Views','Controls','Groups','Pictures','Scenes','SceneValues']
def _fam(part):
    if part.endswith(' L'): return part[:-2],'LEFT'
    if part.endswith(' R'): return part[:-2],'RIGHT'
    return part,'MONO'
def _r1dec(v):
    if isinstance(v,dict) and '__b64__' in v:
        import base64; return base64.b64decode(v['__b64__'])
    return v
def r1_overview(con,cur,parts):
    if not parts: return
    fp=os.path.join(HERE,'r1_assets.json')
    if not os.path.exists(fp):
        warnings.append("R1 오버뷰 건너뜀: r1_assets.json 없음"); return
    import json as _json
    A=_json.load(open(fp,encoding='utf-8'))
    for t in R1_TABLES:
        if not cur.execute("SELECT 1 FROM sqlite_master WHERE type='table' AND name=?",(t,)).fetchone():
            cur.execute(A['create'][t])
    for t,rows in A['enums'].items():
        for r in rows:
            r=[_r1dec(v) for v in r]
            cur.execute(f"INSERT OR IGNORE INTO {t} VALUES({','.join('?'*len(r))})",r)
    cur.execute("DELETE FROM Views"); cur.execute("DELETE FROM Controls"); cur.execute("DELETE FROM Groups")
    sv=A['sysviews']
    for r in sv['rows']:
        r=[_r1dec(v) for v in r]
        cur.execute(f"INSERT INTO Views({','.join(sv['cols'])}) VALUES({','.join('?'*len(r))})",r)
    if A.get('tv'):
        for r in A['tv']['rows']:
            r=[_r1dec(v) for v in r]
            try: cur.execute(f"INSERT OR IGNORE INTO TableVersions({','.join(A['tv']['cols'])}) VALUES({','.join('?'*len(r))})",r)
            except Exception: pass
    cols=A['ccols']
    T={k:{c:_r1dec(v) for c,v in d.items()} for k,d in A['controls'].items()}
    ctl=[1]
    def put(t,**ov):
        if not t: return
        d=dict(t); d.update(ov); d['ControlId']=ctl[0]; ctl[0]+=1; d['ViewId']=1000
        cur.execute(f"INSERT INTO Controls({','.join(cols)}) VALUES({','.join('?'*len(cols))})",[d[c] for c in cols])
    # 그룹 트리: Groups > Master > 패밀리 > 사이드 > 채널 리프
    cur.execute("INSERT INTO Groups(GroupId,Name,ParentId,TargetId,TargetChannel,Type,Flags) VALUES(1,'Groups',0,0,-1,0,1)")
    cur.execute("INSERT INTO Groups(GroupId,Name,ParentId,TargetId,TargetChannel,Type,Flags) VALUES(2,'Master',1,0,-1,0,0)")
    gid=3; fams={}   # fam -> {'gid':g,'sides':[(label,sidegid,dev,ch)]}
    for pname,chans in parts.items():
        fam,col=_fam(pname)
        if fam not in fams:
            cur.execute("INSERT INTO Groups(GroupId,Name,ParentId,TargetId,TargetChannel,Type,Flags) VALUES(?,?,2,0,-1,0,0)",(gid,fam))
            fams[fam]={'gid':gid,'sides':[]}; gid+=1
        f=fams[fam]
        cur.execute("INSERT INTO Groups(GroupId,Name,ParentId,TargetId,TargetChannel,Type,Flags) VALUES(?,?,?,0,-1,0,0)",(gid,pname,f['gid']))
        sgid=gid; gid+=1
        for dv,ch in chans:
            cur.execute("INSERT INTO Groups(GroupId,Name,ParentId,TargetId,TargetChannel,Type,Flags) VALUES(?,?,?,?,?,1,0)",(gid,f"{pname} d{dv}.{ch}",sgid,dv,ch)); gid+=1
        f['sides'].append((col,sgid,chans[0][0],chans[0][1]))
    famlist=list(fams.items())
    FCOL=[10,7,4,2,8,15,6,11,12,3]
    # 한 페이지 압축: 파트별 폭 = 컬럼수*175(+34 갭). 1컬럼 파트는 좁은 헤더(175).
    x0=16; xs=[]; cx0=x0
    for fam,f in famlist:
        ncol=max(1,len(f['sides'])); xs.append((cx0,ncol)); cx0+=ncol*175+34
    xr=cx0+16                                        # 우측 정보 컬럼 x
    W=xr+350+16; H=1080
    Z=min(80,int(1920*80/max(W,1920)))               # 전체가 한 화면에 들어오게 줌 자동
    cur.execute("INSERT INTO Views(ViewId,Type,Name,Icon,Flags,HomeViewIndex,NaviBarIndex,HRes,VRes,ZoomLevel) VALUES(1000,1000,'Overview','',6,0,1,?,?,?)",(W,H,Z))
    first_dev=list(parts.values())[0][0][0]
    for i,(fam,f) in enumerate(famlist):
        (hx,ncol)=xs[i]; c=FCOL[i%len(FCOL)]; g=f['gid']
        if ncol>=2:                                  # 풀 헤더(원본 지오메트리)
            put(T['frame'],PosX=hx,PosY=16,Width=ncol*175,DisplayName=fam,MainColor=c)
            put(T['mute'], PosX=hx+13,PosY=56,TargetId=g)
            put(T['fader'],PosX=hx+96,PosY=46,TargetId=g)
            put(T['cut'],  PosX=hx+237,PosY=56,TargetId=g)
            put(T['cpl'],  PosX=hx+237,PosY=86,TargetId=g)
            put(T['dsw'],  PosX=hx+237,PosY=146,TargetId=g)
            put(T['rdel'], PosX=hx+237,PosY=176,TargetId=g)
        else:                                        # 좁은 헤더(뮤트+페이더+CUT+Delay)
            put(T['frame'],PosX=hx,PosY=16,Width=175,DisplayName=fam,MainColor=c)
            put(T['mute'], PosX=hx+13,PosY=56,TargetId=g)
            put(T['fader'],PosX=hx+75,PosY=46,Width=90,TargetId=g)
            put(T['cut'],  PosX=hx+13,PosY=146,Width=52,TargetId=g)
            put(T['dsw'],  PosX=hx+13,PosY=176,Width=52,TargetId=g)
        for k,(col,sgid,dv,ch) in enumerate(f['sides']):
            cx=hx+k*175
            put(T['colfr'],PosX=cx+1,PosY=253,DisplayName=col,MainColor=c)
            put(T['mute'], PosX=cx+63,PosY=300,TargetId=sgid)
            put(T['isp'],  PosX=cx+37,PosY=380,TargetId=dv,TargetChannel=ch)
            put(T['gr'],   PosX=cx+81,PosY=380,TargetId=dv,TargetChannel=ch)
            put(T['ovl'],  PosX=cx+126,PosY=380,TargetId=dv,TargetChannel=ch)
            put(T['min'],  PosX=cx+52,PosY=444,TargetId=dv,TargetChannel=ch)
            put(T['mgr'],  PosX=cx+122,PosY=444,TargetId=dv,TargetChannel=ch)
            put(T['peak'], PosX=cx+43,PosY=867,TargetId=dv,TargetChannel=ch)
    # 우측: Master 헤더 + Information + Comments (원본 배치)
    put(T['frame'],PosX=xr,PosY=16,DisplayName='Master',MainColor=14)
    put(T['mute'], PosX=xr+12,PosY=56,TargetId=2)
    put(T['fader'],PosX=xr+95,PosY=46,TargetId=2)
    put(T['power'],PosX=xr+250,PosY=56,TargetId=2)
    put(T['infofr'],PosX=xr,PosY=253,DisplayName='Information')
    put(T['mv'],PosX=xr+177,PosY=322,TargetId=first_dev,TargetChannel=0)
    put(T['mf'],PosX=xr+177,PosY=353,TargetId=first_dev,TargetChannel=0)
    put(T['mp'],PosX=xr+177,PosY=384,TargetId=first_dev,TargetChannel=0)
    put(T['comfr'],PosX=xr,PosY=468,DisplayName='Comments')
    put(T['txt1'],PosX=xr+20,PosY=530)
    put(T['txt2'],PosX=xr+122,PosY=560)
    con.commit()

def inject_param_venue(cur,spec):
    """베뉴 생성 — spec.venue(도면 에디터 평면 리스트)가 있으면 그대로, 없으면 UI 치수 기본형(전면 플랫+후면 라케이드)."""
    vp=spec.get('venue')
    if vp:
        cur.execute("DELETE FROM VenueObjectPoints"); cur.execute("DELETE FROM VenueObjects")
        COLS=[4294901760,4294945280,4283282175,4288335154]; BLK=4278190080
        for i,q in enumerate(vp):
            _w=float(q.get('w',0) or 0); _yc=float(q.get('yc',0) or 0)
            hf=R(float(q.get('wf',_w))/2,2); hb=R(float(q.get('wb',_w))/2,2)                     # 사다리꼴(앞/뒤폭)
            ycf=R(float(q.get('ycf',_yc)),2); ycb=R(float(q.get('ycb',_yc)),2)                   # 앞/뒤 중심 분리(자유 사각형)
            d=R(float(q['d']),2)
            z0=R(float(q['z0']),2); z1=R(float(q['z1']),2)
            nm=str(q.get('n') or f'Plane {i+1}').replace("'","")
            cur.execute("INSERT INTO VenueObjects VALUES(?,?,1,1,1,1,1,1.2,?,?,?,0,0,0,0,0,1,1,1,?,0)",
                        (i+1,nm,COLS[i%len(COLS)],BLK,R(float(q['x']),2),i+1))
            for j,(x,y,z) in enumerate([(0,ycf+hf,z0),(d,ycb+hb,z1),(d,ycb-hb,z1),(0,ycf-hf,z0)]):
                cur.execute("INSERT INTO VenueObjectPoints VALUES(?,?,?,?,?)",(i+1,j,x,y,z))
        return
    st=spec.get('_state') or {}
    D=float(st.get('depth') or 36); W=float(st.get('width') or 24)
    hw=R(W/2,2); d1=R(D*0.6,2); d2=R(D-d1,2)
    cur.execute("DELETE FROM VenueObjectPoints"); cur.execute("DELETE FROM VenueObjects")
    RED=4294901760; ORG=4294945280; BLK=4278190080
    cur.execute("INSERT INTO VenueObjects VALUES(1,'Audience Front',1,1,1,1,1,1.2,?,?,2,0,0,0,0,0,1,1,1,1,0)",(RED,BLK))
    for i,(x,y,z) in enumerate([(0,hw,0),(d1,hw,0),(d1,-hw,0),(0,-hw,0)]):
        cur.execute("INSERT INTO VenueObjectPoints VALUES(1,?,?,?,?)",(i,x,y,z))
    cur.execute("INSERT INTO VenueObjects VALUES(2,'Audience Rear',1,1,1,1,1,1.2,?,?,?,0,0,0,0,0,1,1,1,2,0)",(ORG,RED,R(2+d1,2)))
    for i,(x,y,z) in enumerate([(0,hw,0),(d2,hw,2.5),(d2,-hw,2.5),(0,-hw,0)]):
        cur.execute("INSERT INTO VenueObjectPoints VALUES(2,?,?,?,?)",(i,x,y,z))

def build(spec,outpath):
    if os.path.exists(outpath): os.remove(outpath)
    shutil.copy(BASE,outpath)
    con=sqlite3.connect(outpath); cur=con.cursor()
    inject_param_venue(cur,spec)
    # 배치 좌표를 실제 베뉴 관객석 범위에서 계산(하드코딩 금지) — X=깊이(앞0→뒤), Y=폭(±)
    vr=cur.execute("SELECT min(p.X+o.OriginX),max(p.X+o.OriginX),max(abs(p.Y+o.OriginY)) FROM VenueObjectPoints p JOIN VenueObjects o USING(VenueObjectId)").fetchone()
    vx0,vx1,vy=(vr if vr and vr[0] is not None else (0.0,22.0,15.0))
    x_front=R(vx0-2,1)                     # 무대 앞(관객석 2m 앞 어레이 라인)
    z_main=float((spec.get('_state') or {}).get('trim') or 9)   # 플라잉 높이 = UI 트림
    # 플라잉 서브 stacked(서브 위·라인어레이 아래): 메인 라인어레이를 서브 컬럼 높이만큼 낮춰 건다
    _sub=spec.get('sub',{}); _sub_drop=0.0; _sub_stack_fly=False
    if _sub.get('pos')=='flown' and _sub.get('flyMode')=='stacked':
        _sm2=alt(_sub.get('mdl'),'sub') if _sub.get('mdl') else None
        if _sm2 in SUB:
            _snb=int(_sub.get('box',2)); _sper=(_snb+1)//2       # 측당 서브 수(위에 쌓임)
            _sh=sub_h(SUB[_sm2][0]); _sub_drop=R(_sper*_sh+0.3,2); _sub_stack_fly=True
    # 통합 행잉 판정: 플라잉 stacked + 같은 시리즈 → 서브를 메인 그룹에 통합(z는 line_array가 subtop로 조정)
    _m0=spec.get('main',{}); _s0=spec.get('sub',{})
    _integrated = (_sub_stack_fly and _sm2 in SUB and _m0.get('type')=='line'
                   and _m0.get('mdl') in LINE and same_series(_m0.get('mdl'), _s0.get('mdl')))
    if _sub_stack_fly and (_sm2 in SUB) and not _integrated and _m0.get('type')=='line':
        warnings.append(f"ℹ 통합 행잉 해제 — {_m0.get('mdl')}의 통합 호환 서브는 {'/'.join(COMPAT_SUB.get(_m0.get('mdl'),[])) or '없음'}. {_s0.get('mdl')}는 프레임이 달라 통합 불가 → 서브를 별도 플라잉(좌우 컬럼)으로 생성")
    z_main_top=z_main   # 통합 행잉은 line_array가 subtop로 낮춤(이중 낮춤 방지)
    _dd=(spec.get('delay') or {}).get('dist')
    x_delay=R(((vx0-2)+float(_dd)) if _dd else vx0+0.52*(vx1-vx0),1)   # 딜레이 X: 무대앞(메인 위치) 기준 거리 또는 홀 중간
    y_main =R(vy*0.55,1)                    # 메인 L/R 폭
    y_out  =R(vy*0.82,1)                    # 아웃필: 바깥 객석
    # ── 스피커 위치 오버라이드(spec.spkPos, 베뉴 편집기 드래그) — 없으면 자동 공식 ──
    _ovp=spec.get('spkPos') or {}
    def _op(part,key,dflt):
        p=_ovp.get(part) or {}
        v=p.get(key)
        try: return R(float(v),2) if v is not None else dflt
        except Exception: return dflt
    xM=_op('main','x',x_front);   yMn=_op('main','y',y_main)
    xS=_op('sub','x',x_front);    ySb=_op('sub','y',y_main)
    xFf=_op('front','x',None);    yFf=_op('front','y',0.0)
    xDl=_op('delay','x',x_delay); yDl=_op('delay','y',y_main)
    xC=_op('center','x',x_front); yC=_op('center','y',0.0)
    xO=_op('out','x',x_front);    yOt=_op('out','y',y_out)
    b=Builder()
    b.snapdate=str(spec.get('date') or '')  # 스냅샷 CreatedOn(결정적 — JS와 패리티)
    m=spec.get('main',{}); _combo=False   # 포인트-스택 통합 앰프 여부(서브 별도생성 스킵 판정)
    if m.get('type')=='line' and m.get('mdl') in LINE:
        mnt=m.get('mount','flown'); n,sp=clamp_line(m['mdl'],m['box'],m.get('splay'),mnt); nm=LINE[m['mdl']]; bx=apply_manual_variants(variants(n,*nm),nm,m.get('variants'))
        mh=float(m.get('horiz',0) or 0); _nl=b.sg
        _subtop=None; _mgrp_amp=m.get('amp','D90')
        if _integrated:
            _per=(int(_s0.get('box',2))+1)//2
            _integ_spk=SUB_INTEG_ID.get(_sm2, SUB[_sm2][1])   # 통합 전용 SpeakerId(있으면)
            # 한 소스 그룹 = 한 앰프 모델(ArrayCalc 요구). 메인·서브가 함께 지원하는 앰프로 통일.
            # (서브에 메인 앰프를 강제해도 서브가 미지원이면 amp_fix가 되돌려 혼재 → 빨간 에러. 공통 앰프로 방지)
            _mainamp=m.get('amp','D90')
            _sub_amps=AMP_OK.get(SUB[_sm2][1],[]); _main_amps=AMP_OK.get(LINE[m['mdl']][1],[])
            if _mainamp in _sub_amps:
                _mgrp_amp=_mainamp
            else:
                _common=[a for a in _main_amps if a in _sub_amps]
                if _common:
                    _mgrp_amp=_common[0]
                    warnings.append(f"ℹ 통합 행잉: 한 그룹=한 앰프 → {m['mdl']}+{_s0.get('mdl')} 공통 앰프 {_mgrp_amp}로 통일 ({_s0.get('mdl')}는 {_mainamp} 미지원, {m['mdl']} 시스템 표준 앰프)")
                else:
                    _integrated=False   # 공통 앰프 없음 → 통합 불가, 별도 G.SUB 그룹으로
                    warnings.append(f"⚠ 통합 행잉 해제: {m['mdl']}({_mainamp})와 {_s0.get('mdl')}가 공통 앰프 없음 → 서브를 별도 G.SUB 그룹으로 생성(메인 앰프 유지)")
            if _integrated:
                _subtop={'spk':_integ_spk,'n':_per,'amp':_mgrp_amp,
                         'part':'G.SUB','h':sub_h(SUB[_sm2][0]),'link':_s0.get('link',1)}
        b.line_array('MAIN L',m['mdl'],_mgrp_amp,-yMn,z_main_top,m.get('tilt',0),bx,sp,mnt,xM,horiz=mh,gname='MAIN',nxt=_nl+1,link=m.get('link',1),subtop=_subtop,rigpts=m.get('rigPts','2'))
        b.line_array('MAIN R',m['mdl'],_mgrp_amp, yMn,z_main_top,m.get('tilt',0),bx,sp,mnt,xM,horiz=-mh,gname='MAIN',ordr=-1,link=m.get('link',1),subtop=(dict(_subtop) if _subtop else None),rigpts=m.get('rigPts','2'))
    elif m.get('type')=='point':
        mm=alt(m.get('mdl'),'point')
        if mm in POINT:
            _,pid,psys=POINT[mm]
            # 포인트소스 M20 폴 스택(서브 위): 높이 = 받침 서브 스택 + 폴대 길이(+ 캐비닛 반높이 근사)
            _st=spec.get('_state') or {}
            if m.get('mount')=='stack':
                _sm0=(spec.get('sub') or {}).get('mdl'); _sma=alt(_sm0,'sub') if _sm0 else None
                _subh=sub_h(SUB[_sma][0]) if (_sma in SUB) else 0.5
                import math as _math
                _psn=max(1,_math.ceil(int((spec.get('sub') or {}).get('box') or 2)/2))  # 받침 서브 = SUB 섹션 측당 통수
                _polem=float(_st.get('poleH') or 1100)/1000.0
                z_pt=R(_psn*_subh+_polem+0.2,2)
                warnings.append(f"ℹ 포인트소스 폴 스택: {m.get('mdl')}를 {_sm0 or '서브'} {_psn}통(측당) 위 M20 폴({_polem:.2f}m)에 스택 → 높이 {z_pt}m. 받침 서브는 서브우퍼 섹션에서 설정.")
            else:
                z_pt=z_main
            # ── 포인트-스택 메인 + 서브 ≤4채널 → 앰프 1대 통합. 채널 기준(서브 링크 반영: 서브ch=ceil(통수/링크)) ──
            _cs=spec.get('sub') or {}; _csm=alt(_cs.get('mdl'),'sub') if _cs.get('mdl') else None
            _sbox=int(_cs.get('box') or 0); _slink=max(1,int(_cs.get('link') or 1))
            _ys=[-yMn,yMn]; _mch=len(_ys)
            _subch=(-(-_sbox//_slink)) if _sbox else 0   # ceil(통수/링크) = 서브 채널 수
            _mbi=(pid in CH2_IDS); _sbi=(SUB[_csm][1] in CH2_IDS) if (_csm in SUB) else True
            _common=[a for a in AMP_OK.get(pid,[]) if a in AMP_OK.get(SUB[_csm][1],[])] if (_csm in SUB) else []
            _combo=(m.get('mount')=='stack' and _csm in SUB and 1<=_sbox and (_mch+_subch)<=4
                    and _common and not _mbi and not _sbi)
            if _combo:
                _camp=_common[0]   # 공통 앰프(V10P∩V-SUB=D40 우선)
                b.point_stack_combo('MAIN',psys,pid,_ys,z_pt,m.get('tilt',0),xM,'G.SUB',SUB[_csm][2],SUB[_csm][1],_sbox,_slink,xM,sub_h(SUB[_csm][0]),_camp,sym=1)
                warnings.append(f"ℹ 통합 앰프: {m.get('mdl')} {_mch}통 + {_cs.get('mdl')} {_sbox}통(링크1:{_slink}→{_subch}ch) = {_mch+_subch}채널 → {_camp} 1대(측당 탑+서브 A/B·C/D).")
            else:
                b.point_row('MAIN',psys,m.get('amp','D80'),pid,_ys,z_pt,m.get('tilt',0),xM,sym=1,link=m.get('link',1))
        else: warnings.append(f"메인 {m.get('mdl')} 미보유→건너뜀")
    elif m.get('type')=='line': warnings.append(f"메인 {m.get('mdl')} 미보유→건너뜀")
    s=spec.get('sub',{})
    _sm=alt(s.get('mdl'),'sub') if s.get('mdl') else None
    if s.get('mdl') and _sm not in SUB:
        warnings.append(f"⚠ {s.get('mdl')}: ArrayCalc SpeakerId 미확보 → 서브 생성 생략. ArrayCalc에서 {s.get('mdl')} 소스를 하나 만들어 저장한 .dbpr을 주시면 정식 추가합니다.")
    if _sm in SUB and (_integrated or _combo):
        pass   # 통합 행잉 or 포인트-스택 통합앰프: 서브가 이미 처리됨(별도 G.SUB 그룹 생성 안 함)
    elif _sm in SUB:
        smdl=_sm; _,sid,ssys=SUB[smdl]; nb=int(s.get('box',2)); half=nb//2; pos=[]
        flown=(s.get('pos')=='flown')
        zs=z_main if flown else 0.0
        cfg=s.get('cfg','stack'); C=343.0
        if flown:
            # ── 플라잉 서브 배치 모드 ──
            fm=s.get('flyMode','integrated')
            _shh=sub_h(SUB[smdl][0])
            if fm=='behind':
                # 메인 라인어레이 뒤(무대쪽)에 별도 플라잉 서브 — 센터 브로드사이드 클러스터
                xb=R(xS-2.0,1)
                if nb==1: pos.append((xb,0.0,zs))
                else:
                    for k in range(nb): pos.append((xb, R((-1+2*k/(nb-1))*(ySb*0.75),2), zs))
                warnings.append("ℹ G.SUB 플라잉(메인 뒤 별도): 무대 뒤 센터 브로드사이드 서브 어레이 — 정렬·커버리지는 ArrayCalc 확인")
            elif fm=='stacked':
                # 서브 위 · 라인어레이 아래: 좌우 각 메인 위에 서브 컬럼(트림부터 아래로), 메인은 그 아래로 낮춰 걸림
                for side in (-1,1):
                    cnt=half+(1 if (side<0 and nb%2) else 0)
                    for k in range(cnt): pos.append((xS, side*ySb, R(z_main-k*_shh,2)))
                _tk=SUB_KG.get(SUB[smdl][0],40)
                warnings.append(f"ℹ G.SUB 플라잉(서브 위·어레이 아래): 좌우 메인 위 서브 컬럼 + 라인어레이 아래로 통합 행잉. "
                                f"측당 서브 {(nb+1)//2}통(~{_tk*((nb+1)//2)}kg)+어레이 하중이 한 모터에 걸림 — ArrayCalc에서 각 그룹 Load 합산 확인")
            else:
                # integrated: 좌우 메인과 함께 플라잉 서브 컬럼(라인어레이 옆에 통합 행잉)
                for side in (-1,1):
                    cnt=half+(1 if (side<0 and nb%2) else 0)
                    for k in range(cnt): pos.append((xS, side*ySb, R(zs-k*_shh,2)))
                warnings.append("ℹ G.SUB 플라잉(메인과 함께): 좌우 메인 옆 서브 컬럼 — 라인어레이와 통합 행잉, ArrayCalc에서 카디오이드/정렬 확인")
            _skipGround=True
        else:
            _skipGround=False
        _min={'arc':3,'endfire':2,'cardioid':3}.get(cfg)
        if (not flown) and _min and nb<_min:
            warnings.append(f"⚠ {cfg} 배열은 최소 {_min}통 필요 — {nb}통이라 일반 L/R 스택으로 생성됨 (통수를 늘리면 {cfg} 적용)")
        if flown: pass
        elif cfg=='endfire' and nb>=2:
            # 엔드파이어: 간격 = c/4f(1/4 파장). 목표 주파수 spec.sub.efFreq(기본 69Hz→1.24m). 앞 캐비닛에 간격/음속 딜레이.
            f0=float(s.get('efFreq',69) or 69); gap=R(C/(4.0*f0),2)
            for side in (-1,1):
                cnt=half+(1 if (side<0 and nb%2) else 0)
                for k in range(cnt):
                    pos.append((R(xS-gap*k,2), side*(ySb), zs, 0, R(gap*k/C,6)))
            warnings.append(f"ℹ G.SUB 엔드파이어 {f0:g}Hz: 간격 {gap}m(c/4f)·전방 딜레이 — 기하 초기값, 주파수별 결과는 ArrayCalc에서 확인")
        elif (not flown) and cfg=='arc' and nb>=3:
            # 브로드사이드 아크: 무대 앞 일렬 + 가상 반경 딜레이 커브(중앙 0, 바깥쪽으로 갈수록 증가 = 커버 확장)
            Rv=max(8.0,ySb*2.0)
            for k in range(nb):
                y=(-1+2*k/(nb-1))*ySb if nb>1 else 0.0
                dly=((Rv*Rv+y*y)**0.5 - Rv)/C
                pos.append((xS, R(y,2), zs, 0, R(dly,6)))
            warnings.append("ℹ G.SUB 아크: 가상 반경 딜레이 커브 반영 — 커버리지는 ArrayCalc에서 확인")
        elif (not flown) and cfg=='cardioid' and nb>=3:
            # 카디오이드: 좌/우 클러스터에서 3통당 가운데 1통 후방 반전(180°) — CSA류 셋업은 앰프에서 선택 필요.
            idx=0
            for side in (-1,1):
                cnt=half+(1 if (side<0 and nb%2) else 0)
                for k in range(cnt):
                    rev = (k%3==1)
                    pos.append((xS, side*(ySb+0.6*k), zs, 180 if rev else 0, 0))
                    idx+=1
            warnings.append("ℹ G.SUB 카디오이드: 3통당 1통 후방 반전 배치 — 전용 CSA 셋업·딜레이는 앰프/ArrayCalc에서 설정")
        elif not flown:
            for k in range(half): pos.append((xS,-ySb-0.6*k,zs))
            for k in range(half): pos.append((xS, ySb+0.6*k,zs))
            if nb%2: pos.append((xS,0.0,zs))
        if not pos: pos=[(xS,0.0,zs)]
        # 프론트 서브(무대 앞 분산) — spec.sub.fSubOn/fSubBox 반영
        if s.get('fSubOn'):
            fn=int(s.get('fSubBox',3) or 3)
            hw=max(2.0,ySb*0.7)
            for k in range(fn):
                y=(-1+2*k/(fn-1))*hw if fn>1 else 0.0
                pos.append((R(xS+0.6,2), R(y,2), 0.0))
        b.sub_stack('G.SUB',ssys,s.get('amp','D90'),sid,pos,sym=1,link=s.get('link',1))
    elif s.get('mdl'): warnings.append(f"서브 {s.get('mdl')} 미보유→건너뜀")
    f=spec.get('front',{})
    if f.get('on'):
        fm=f.get('mdl')
        fm=alt(fm,'point')
        if f.get('type')=='point' and fm in POINT:
            _,pid,psys=POINT[fm]; nb=int(f.get('box',6))
            _stw=(spec.get('_state') or {}).get('stageW')
            hw=R(max(2.0,float(_stw)/2.0-0.5),1) if _stw else R(y_main*0.8,1)   # 립 포지션: 무대폭 기준
            ys=[R(-hw+2*hw*i/(nb-1),2) for i in range(nb)] if nb>1 else [0.0]
            _fa=float(f.get('aim') or 0); faim=-(_fa if _fa else 30.0)   # +=하향/−=상향(부호 존중), 0=기본 30↓
            b.point_row('Front fill',psys,f.get('amp','D20'),pid,[R(_y+yFf,2) for _y in ys],R(float(f.get('height') or 1.2),2),faim,(xFf if xFf is not None else x_front),sym=1,link=f.get('link',1))
        elif f.get('type')=='line' and fm in LINE:
            nb=int(f.get('box',6)); nm=LINE[fm]; bx=apply_manual_variants(variants(nb,*nm),nm,f.get('variants'))
            b.line_array('Front fill',fm,f.get('amp','D80'),yFf,R(float(f.get('height') or 2.5),2),f.get('aim',0),bx,f.get('splay') or [0]*nb,ox=(xFf if xFf is not None else 0),link=f.get('link',1),rigpts=f.get('rigPts','2'))
        else: warnings.append(f"프론트필 {fm} 미보유→건너뜀")
    d=spec.get('delay',{})
    if d.get('on'):
        dm=d.get('mdl'); ht=float(d.get('height',7))
        if d.get('type')=='line' and dm in LINE:
            dmnt=d.get('mount','flown'); nb,sp=clamp_line(dm,d.get('box',8),d.get('splay'),dmnt); nm=LINE[dm]; bx=apply_manual_variants(variants(nb,*nm),nm,d.get('variants'))
            _ndl=b.sg
            _am=d.get('alignMs')
            dms_=R(float(_am),1) if _am is not None else R((xDl-xM)/343.0*1000+0.3,1)
            b.line_array('DELAY L',dm,d.get('amp','D40'),-yDl,ht,d.get('aim',0),bx,sp,dmnt,xDl,horiz=float(d.get('horiz') or 0),gname='DELAY',nxt=_ndl+1,link=d.get('link',1),dms=dms_)
            b.line_array('DELAY R',dm,d.get('amp','D40'), yDl,ht,d.get('aim',0),bx,sp,dmnt,xDl,horiz=-float(d.get('horiz') or 0),gname='DELAY',ordr=-1,link=d.get('link',1),dms=dms_)
        elif d.get('type')=='point' and alt(dm,'point') in POINT:
            dm2=alt(dm,'point'); _,pid,psys=POINT[dm2]; b.point_row('Delay',psys,d.get('amp','D40'),pid,[-yDl,yDl],ht,d.get('aim',0),xDl,sym=1,link=d.get('link',1),horiz=float(d.get('horiz') or 0),dms=(R(float(d.get('alignMs')),1) if d.get('alignMs') is not None else R((xDl-xM)/343.0*1000+0.3,1)))
        else: warnings.append(f"딜레이 {dm} 미보유→건너뜀")
    c=spec.get('center',{})
    if c.get('on'):
        cm=c.get('mdl')
        if c.get('type')=='line' and cm in LINE:
            nb,sp=clamp_line(cm,c.get('box',6),c.get('splay'),'flown'); nm=LINE[cm]; bx=apply_manual_variants(variants(nb,*nm),nm,c.get('variants'))
            zc=R(float(c.get('height') or z_main),1)
            b.line_array('CENTER',cm,c.get('amp','D80'),yC,zc,c.get('aim',0),bx,sp,'flown',xC,horiz=float(c.get('horiz') or 0),sym=1,link=c.get('link',1),rigpts=c.get('rigPts','2'))
        elif alt(cm,'point') in POINT: cm2=alt(cm,'point'); _,pid,psys=POINT[cm2]; b.point_row('Center',psys,c.get('amp','D80'),pid,[yC],R(float(c.get('height') or z_main),1),c.get('aim',0),xC,sym=1,horiz=float(c.get('horiz') or 0),link=c.get('link',1))
        else: warnings.append(f"센터필 {cm} 미보유→건너뜀")
    o=spec.get('out',{})
    if o.get('on'):
        om=o.get('mdl')
        if o.get('type')=='line' and om in LINE:
            nb,sp=clamp_line(om,o.get('box',6),o.get('splay'),o.get('mount','flown')); nm=LINE[om]; bx=apply_manual_variants(variants(nb,*nm),nm,o.get('variants'))
            oh=float(o.get('horiz',0) or 0); _no=b.sg
            omnt=o.get('mount','flown')
            b.line_array('OUT L',om,o.get('amp','D80'),-yOt,R(z_main-0.5,1),o.get('tilt',0),bx,sp,omnt,xO,horiz=oh,gname='OUT',nxt=_no+1,link=o.get('link',1),rigpts=o.get('rigPts','2'))
            b.line_array('OUT R',om,o.get('amp','D80'), yOt,R(z_main-0.5,1),o.get('tilt',0),bx,sp,omnt,xO,horiz=-oh,gname='OUT',ordr=-1,link=o.get('link',1),rigpts=o.get('rigPts','2'))
        elif alt(om,'point') in POINT: om2=alt(om,'point'); _,pid,psys=POINT[om2]; b.point_row('Out',psys,o.get('amp','D80'),pid,[-yOt,yOt],R(z_main-0.5,1),o.get('tilt',0),xO,sym=1,link=o.get('link',1))
        else: warnings.append(f"아웃필 {om} 미보유→건너뜀")
    # ── 커스텀 스피커 그룹(spec.customs) — 탭 + 로 추가한 자유 스피커 ──
    for ci,cu in enumerate(spec.get('customs') or []):
        try:
            cnm=str(cu.get('name') or f'CUSTOM {ci+1}')[:24].replace("'","")
            ctp=cu.get('type','point'); cmdl=cu.get('mdl'); cn=max(1,int(cu.get('box',1) or 1))
            cx=R(x_front+float(cu.get('x') or 0),2); cyv=float(cu.get('y') or 0); _zv=cu.get('z'); cz=float(5 if _zv is None else _zv)
            cam=float(cu.get('aim',0) or 0); csym=1 if cu.get('sym',True) else 0
            clk=max(1,int(cu.get('link',1) or 1)); camp=cu.get('amp','D40')
            if ctp=='line' and cmdl in LINE:
                cmt=cu.get('mount','flown'); crg=str(cu.get('rigPts','2')); chz=float(cu.get('horiz') or 0)
                cn2,csp=clamp_line(cmdl,cn,cu.get('splay'),cmt)
                bxc=variants(cn2,*LINE[cmdl])
                if csym:
                    nxc=b.sg
                    b.line_array(cnm+' L',cmdl,camp,-abs(cyv),cz,cam,bxc,csp,cmt,cx,horiz=chz,gname=cnm,nxt=nxc+1,link=clk,rigpts=crg)
                    b.line_array(cnm+' R',cmdl,camp, abs(cyv),cz,cam,bxc,csp,cmt,cx,horiz=-chz,gname=cnm,ordr=-1,link=clk,rigpts=crg)
                else:
                    b.line_array(cnm,cmdl,camp,cyv,cz,cam,bxc,csp,cmt,cx,horiz=chz,link=clk,rigpts=crg)
            elif ctp=='sub' and cmdl in SUB:
                _,sid2,ssys2=SUB[cmdl]; pos2=[]; half2=cn//2; cz0=max(0.0,cz)
                if csym:
                    for k in range(half2): pos2.append((cx,-abs(cyv)-0.6*k,cz0))
                    for k in range(half2): pos2.append((cx, abs(cyv)+0.6*k,cz0))
                    if cn%2: pos2.append((cx,0.0,cz0))
                else:
                    for k in range(cn): pos2.append((cx,cyv+0.6*k,cz0))
                b.sub_stack(cnm,ssys2,camp,sid2,pos2,sym=csym,link=clk)
            else:
                cm2=cmdl if cmdl in POINT else alt(cmdl,'point')
                if cm2 in POINT:
                    _,pid2,psys2=POINT[cm2]
                    ys2=([-abs(cyv),abs(cyv)] if csym else [cyv])
                    b.point_row(cnm,psys2,camp,pid2,ys2,cz,cam,cx,sym=csym,link=clk,horiz=float(cu.get('horiz') or 0))
                else:
                    warnings.append(f"커스텀 {cnm}: 모델 {cmdl} 미보유→건너뜀")
        except Exception as e:
            warnings.append(f"커스텀 그룹 실패({cu.get('name','?')}): {e}")
    b.flushdev()
    b.sql.append("COMMIT;")
    cur.executescript("\n".join(b.sql)); con.commit()
    r1_overview(con,cur,b.parts)
    ok=cur.execute("PRAGMA integrity_check;").fetchone()[0]
    ncab=cur.execute("SELECT COUNT(*) FROM Cabinets").fetchone()[0]
    rt=round_trip(cur,spec)
    con.close()
    return ok, ncab, rt

def round_trip(cur,spec):
    """생성 .dbpr 재파싱 → spec 대조 (spec→dbpr→re-parse). 파일 생성 정확성 검증 — 음향·리깅 검증 아님."""
    checks=[]
    _w=list(warnings)   # 역검증 중 clamp_line 재호출로 경고 중복되지 않게 보호
    def ck(name,okv,detail=''): checks.append({'name':name,'ok':bool(okv),'detail':detail})
    try:
        # 1) 파트별 캐비닛 수
        cnt={}
        for nm,c in cur.execute("SELECT s.Name,COUNT(*) FROM SourceGroups s JOIN Cabinets c ON c.SourceGroupId=s.SourceGroupId GROUP BY s.SourceGroupId"):
            cnt[nm]=cnt.get(nm,0)+c
        m=spec.get('main',{}); su=spec.get('sub',{})
        exp={}
        if m.get('type')=='line' and m.get('mdl') in LINE:
            n,_=clamp_line(m['mdl'],m['box'],m.get('splay'),m.get('mount','flown')); exp['MAIN']=n*2
        elif m.get('type')=='point': exp['MAIN']=2
        _smrt=alt(su.get('mdl'),'sub') if su.get('mdl') else None
        _integ_rt=(su.get('pos')=='flown' and su.get('flyMode')=='stacked' and _smrt in SUB
                   and m.get('type')=='line' and m.get('mdl') in LINE and same_series(m.get('mdl'),su.get('mdl')))
        if _smrt in SUB:
            if _integ_rt:
                exp['MAIN']=exp.get('MAIN',0)+((int(su.get('box',2))+1)//2)*2   # 통합: 서브가 MAIN 그룹에 포함
            else:
                exp['G.SUB']=max(1,int(su.get('box',2)))+(int(su.get('fSubBox',0)) if su.get('fSubOn') else 0)
        for key,part in (('front','Front fill'),('center','CENTER'),('out','OUT'),('delay','DELAY')):
            v=spec.get(key,{})
            if not v.get('on'): continue
            typ=v.get('type'); nb=int(v.get('box',1) or 1)
            if typ=='line':
                mdl=alt(v.get('mdl'),'x')
                if mdl in LINE:
                    n,_=clamp_line(mdl,nb,v.get('splay'),v.get('mount','flown'))
                    exp[part]=n*(2 if part in ('OUT','DELAY') else 1)
            else:
                exp[part]={'Front fill':nb,'CENTER':1,'OUT':2,'DELAY':2}.get(part,nb)
                if part=='CENTER': exp['Center']=exp.pop('CENTER')
                if part=='OUT': exp['Out']=exp.pop('OUT')
                if part=='DELAY': exp['Delay']=exp.pop('DELAY')
        for part,e in exp.items():
            got=cnt.get(part,0)
            ck(f'{part} 캐비닛 수', got==e, f'{got}/{e}')
        # 2) 앰프 모델이 캐비닛 호환 목록 내인가
        bad=0
        for mdl,sid in cur.execute("SELECT DISTINCT d.Model,c.SpeakerId FROM Devices d JOIN Cabinets c ON c.DeviceId=d.DeviceId"):
            okl=AMP_OK.get(sid)
            if okl and mdl not in okl: bad+=1
        ck('앰프-스피커 호환', bad==0, f'위반 {bad}건' if bad else '전 장치 OK')
        # 3) 채널(쌍)당 캐비닛 수 ≤ 해당 스피커·운용모드 허용값 (모델별 세분)
        viol=0; mx=0
        for sid,n in cur.execute("SELECT SpeakerId,COUNT(*) FROM Cabinets GROUP BY DeviceId,AmplifierChannel,SpeakerId"):
            lim = (2 if sid in CH2_LINK2 else 1) if sid in CH2_IDS else LINK1_MAX.get(sid,1)
            if n>lim: viol+=1
            if n>mx: mx=n
        ck('채널(쌍)당 통수 한계(모델별)', viol==0, f'위반 {viol}건' if viol else f'최대 {mx}통/채널 · 전 모델 허용 내')
        # 4) L/R 대칭쌍 무결(R: OrderIndex=-1 & HasPrevious=1)
        badp=cur.execute("SELECT COUNT(*) FROM SourceGroups s JOIN SourceGroupsAdditionalData a USING(SourceGroupId) WHERE s.OrderIndex=-1 AND a.HasPrevious!=1 AND s.Type IN(1,2,3)").fetchone()[0]
        ck('L/R 대칭쌍 링크', badp==0)
        # 5) 스냅샷 입력소스: 리드채널 수 == InputEnable1=1 행 수
        leads=cur.execute("SELECT COUNT(DISTINCT DeviceId||'/'||AmplifierChannel) FROM Cabinets").fetchone()[0]
        sv=cur.execute("SELECT COUNT(*) FROM SnapshotValues WHERE TargetProperty='Config_InputEnable1' AND Value=1.0").fetchone()[0]
        ck('채널 입력소스(스냅샷)', sv>=leads if leads else True, f'{sv}/{leads}')
        # 6) 요청 서브 배열 == 실제 생성 배열 (최소 통수 미달 폴백은 ⚠로 표면화)
        cfg=su.get('cfg')
        if cfg in ('endfire','arc','cardioid'):
            nbs=int(su.get('box',0) or 0)
            _min={'arc':3,'endfire':2,'cardioid':3}[cfg]
            if cfg in ('endfire','arc'):
                got=cur.execute("SELECT COUNT(*) FROM CabinetsAdditionalData ca JOIN Cabinets c USING(CabinetId) JOIN SourceGroups s ON s.SourceGroupId=c.SourceGroupId WHERE s.Name='G.SUB' AND ca.Delay>0").fetchone()[0]
                applied=got>0; det=f'딜레이 {got}통'
            else:
                got=cur.execute("SELECT COUNT(*) FROM Cabinets c JOIN SourceGroups s ON s.SourceGroupId=c.SourceGroupId WHERE s.Name='G.SUB' AND c.HorizontalAngle=180").fetchone()[0]
                applied=got>0; det=f'반전 {got}통'
            if nbs<_min:
                ck(f'서브 배열 요청({cfg})', False, f'최소 {_min}통 필요({nbs}통) → L/R 스택 폴백 — 경고 표시됨')
            else:
                ck(f'서브 배열 요청({cfg})', applied, det if applied else '미적용!')
    except Exception as e:
        ck('역검증 실행', False, str(e)[:80])
    warnings[:]= _w
    return {'ok': all(c['ok'] for c in checks), 'checks': checks}

def generate_from_spec(spec, out_dir=None):
    del warnings[:]
    out_dir = out_dir or FOLDER
    os.makedirs(out_dir, exist_ok=True)
    name=(spec.get('projName') or 'AudioAZ').strip()
    ver=(spec.get('ver') or 'v.1').strip()
    date=spec.get('date') or datetime.date.today().strftime('%y%m%d')
    out=os.path.join(out_dir, f"{name} {ver}({date}).dbpr")
    ok,ncab,rt=build(spec,out)
    return {'ok': ok=='ok', 'file': os.path.basename(out), 'path': out, 'cabinets': ncab, 'warnings': list(warnings), 'roundtrip': rt}
