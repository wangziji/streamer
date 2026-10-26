"""Task 2 reproducible arithmetic and provenance checks; no CAD writes."""
from pathlib import Path
from decimal import Decimal as D
import csv, hashlib, json, re
from urllib.parse import unquote

ROOT=Path(__file__).resolve().parents[3]
HERE=Path(__file__).resolve().parent
sha=lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
baseline=json.loads((HERE/'input-baseline.json').read_text())
for rel,digest in baseline['cad_hashes'].items():
    assert sha(ROOT/rel)==digest, f'CAD/library drift: {rel}'
assert sha(ROOT/'docs/evidence/task1-2026-10-25/verification-result.json')==baseline['task1_verification_sha256']
rows=list(csv.DictReader((ROOT/'docs/engineering/power-budget.csv').open()))
assert len(rows)==24 and len({r['rail'] for r in rows})==24
required={'rail','voltage_V','idle_A','playback_A','peak_A','evidence_kind','source_page','efficiency_basis','power_W'}
assert required <= set(rows[0])
assert {r['domain'] for r in rows} >= {'mainboard','display','usb_bridge','clock','akm','iv','output','control'}
assert sum(r['evidence_kind']=='manufacturer_bound' for r in rows)==4
assert sum(r['evidence_kind']=='assumed' for r in rows)==20
assert all(r['evidence_kind'] in {'measured','manufacturer_bound','assumed'} for r in rows)
assert not any(r['evidence_kind']=='measured' for r in rows)
used=set()
for r in rows:
    assert D('0')<D(r['eta_path'])<=D('1')
    assert 'assumed' in r['efficiency_basis']
    for current,power in [('idle_A','idle_power_W'),('playback_A','power_W'),('peak_A','peak_power_W')]:
        assert D(r[current])>=0
        assert abs(D(r['voltage_V']))*D(r[current])==D(r[power]), r['rail']
    assert D(r['peak_A'])>=max(D(r['idle_A']),D(r['playback_A']))
    if not r['source_page'].startswith('none:'):
        source=r['source_page'].split(':')[0]
        assert (ROOT/source).is_file(),source
        used.add(source)
assert {r['rail'] for r in rows if D(r['voltage_V'])<0}=={'IV_NEG_12V','OUT_NEG_12V'}
# Independent expected loads catch omitted domains and negative-rail cancellation.
expected={'idle':D('9.61980'),'playback':D('22.48490'),'peak':D('36.93854')}
summary={}
for mode,col in [('idle','idle_power_W'),('playback','power_W'),('peak','peak_power_W')]:
    load=sum(D(r[col]) for r in rows)
    assert load==expected[mode],(mode,load)
    battery=sum(D(r[col])/D(r['eta_path']) for r in rows)
    summary[mode]={'load_W':float(load),'battery_W':float(battery),'effective_eta':float(load/battery),'loss_W':float(battery-load)}
# Plan examples explicitly exclude additional aging derating.
assert round(D(30)/(D('.85')*D('.8')),2)==D('44.12')
assert round(D(40)/(D('.85')*D('.8')),2)==D('58.82')
play=D(str(summary['playback']['battery_W']))
nom=play/(D('.8')*D('.75'))
peak=expected['peak']; ip=peak/(D(12)*D('.75'))
scenarios=[('csv_baseline',float(nom)),('eta_75',float(expected['playback']/(D('.75')*D('.8')*D('.75')))),('window_70',float(expected['playback']/(D('.75')*D('.7')*D('.75')))),('load_30',float(D(30)/(D('.75')*D('.7')*D('.75')))),('load_40',float(D(40)/(D('.75')*D('.7')*D('.75'))))]
runtimes={str(e):float(D(str(e))*D('.8')*D('.75')/play*60) for e in [48,60,80,97.92]}
shutdown=peak/D('.75')*60
assert round(nom,5)==D('42.65731')
assert ip<D('4.25')<ip*D('1.25')
assert peak/(D(11)*D('.75'))>D('4.25')
assert D(48)*D('.8')*D('.75')/(expected['playback']/D('.75'))<1
assert round(shutdown/D(3600),5)==D('.82086')
# Manufacturer source archive hashes must match manifests, including supporting files.
used.update(['docs/specs/rrc/RRC2054-technical.pdf','docs/specs/rrc/RRC2054-2-datasheet.pdf','docs/specs/adi/LT3045.pdf'])
source_hashes={}
for rel in sorted(used):
    path=ROOT/rel
    manifest=json.loads((path.parent/'manifest.json').read_text())
    docs=manifest.get('documents',[manifest])
    entry=next(d for d in docs if (d.get('file') or d.get('local_file') or d.get('filename'))==path.name)
    assert sha(path)==entry['sha256'],rel
    source_hashes[rel]=sha(path)
for rel in ['docs/engineering/battery-energy.md','docs/validation/runtime-protocol.md']:
    path=ROOT/rel; content=path.read_text()
    for link in re.findall(r'\]\(([^)]+)\)',content):
        if '://' not in link and not link.startswith('#'):
            assert (path.parent/unquote(link.split('#')[0])).exists(),(rel,link)
    assert 'Task 3' in content and 'Task 9' in content
energy=(ROOT/'docs/engineering/battery-energy.md').read_text()
protocol=(ROOT/'docs/validation/runtime-protocol.md').read_text()
assert all(s in energy for s in ['design_accepted=false','bench_passed=false','system_passed=false','不含老化','4.35A','I/V先于EX','R-POWER-02'])
assert all(s in protocol for s in ['not_run','不确定度下界≥3600s','各3次','external-inputs.csv','monotonic_s','BMS硬切断','掉音','200cd/m','0.82086Wh'])
# P2 regression: permitted VBUS detection must remain distinct from system supply.
assert '若能检出正向外供，判fail' not in protocol, 'Blanket VBUS criterion rejects permitted sensing current'
assert all(s in protocol for s in ['必要连接检测', '检测支路电流上界', '系统轨或电池', '隔离证据', 'measurement_scope', '不得仅从总端口电流减去']), 'Missing VBUS sensing boundary or measurement evidence'
result={'result':'PASS','scope':'Arithmetic/document/source/saved-CAD consistency only; no hardware acceptance',
        'budget_rows':len(rows),'assumed_rows':20,'manufacturer_current_rows':4,'measured_rows':0,
        'summary':summary,'energy_required_Wh':float(nom),'energy_scenarios_Wh':dict(scenarios),
        'runtime_estimates_minutes':runtimes,'peak_current_A':float(ip),'screening_current_with_margin_A':float(ip*D('1.25')),
        'shutdown_battery_J':float(shutdown),'shutdown_battery_Wh':float(shutdown/D(3600)),
        'source_hashes':source_hashes,'cad_and_library_hashes_checked':len(baseline['cad_hashes']),
        'hardware_tests':'not_run','design_accepted':False,'bench_passed':False,'system_passed':False}
print(json.dumps(result,ensure_ascii=False,indent=2))
