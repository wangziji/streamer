"""Read-only Task 1 evidence checks. Run with Python plus pypdf; writes no files."""
from pathlib import Path
import csv
import hashlib
import json
import re
import subprocess
from urllib.parse import urlparse, unquote
import xml.etree.ElementTree as ET
from pypdf import PdfReader

ROOT = Path(__file__).resolve().parents[3]
EVIDENCE = ROOT / 'docs/evidence'
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
baseline = json.loads((EVIDENCE / 'task1-2026-10-25/baseline-verification.json').read_text())
for name, digest in baseline['cad_hashes'].items():
    assert sha(ROOT / name) == digest, f'CAD drift: {name}'
p = json.loads((EVIDENCE / 'netlist-provenance.json').read_text())
assert sha(ROOT / 'AK4499.kicad_sch') == p['source_sha256']
assert sha(EVIDENCE / p['export']) == p['export_sha256']
assert sha(EVIDENCE / 'netlist-provenance.json') == baseline['original_provenance_sha256']
assert sha(EVIDENCE / 'components.json') == baseline['components_sha256']
components = json.loads((EVIDENCE / 'components.json').read_text())
net = ET.parse(EVIDENCE / p['export']).getroot()
exported = {c.attrib['ref']: (c.findtext('value'), c.findtext('footprint', ''))
            for c in net.findall('./components/comp')}
# Both evidence formats encode an unassigned footprint: JSON null, XML absent.
assert {c['ref']: (c['value'], (c.get('footprint') or '')) for c in components} == exported
assert len(components) == 33

allowed = {'analog.com', 'akm.com', 'crystek.com', 'raspberrypi.com',
           'xmos.com', 'ti.com', 'st.com', 'rrc-ps.com', 'raw.githubusercontent.com'}
files = set()
for manifest in sorted((ROOT / 'docs/specs').glob('*/manifest.json')):
    data = json.loads(manifest.read_text())
    for doc in data.get('documents', [data]):
        name = doc.get('file') or doc.get('local_file') or doc.get('filename')
        if not doc.get('sha256'):
            continue
        assert name, manifest
        f = manifest.parent / name
        assert sha(f) == doc['sha256'], f'Hash mismatch: {f}'
        for field in ['source_url', 'url', 'download_url', 'final_url', 'finalURL']:
            if not doc.get(field):
                continue
            u = urlparse(doc[field]); host = u.hostname or ''
            assert u.scheme == 'https' and any(host == a or host.endswith('.'+a) for a in allowed), doc[field]
        if f.suffix == '.pdf':
            reader = PdfReader(f)
            assert len(reader.pages) == doc.get('page_count', doc.get('pages')), f
            assert all(isinstance(page.extract_text(), str) for page in reader.pages), f
        files.add(f.resolve())
actual = {p.resolve() for p in (ROOT / 'docs/specs').rglob('*') if p.suffix in ['.pdf', '.adoc']}
assert files == actual, f'Manifest inventory gap: {files ^ actual}'
assert len(files) == 25 and sum(f.suffix == '.pdf' for f in files) == 24

with (ROOT / 'docs/engineering/traceability.csv').open(newline='') as f:
    rows = list(csv.DictReader(f))
assert len(rows) == 59
ids = [r['requirement_id'] for r in rows]
assert len(ids) == len(set(ids))
assert {'R-POWER-01','R-RUNTIME-01','R-AUDIO-01','R-PC-01','R-SOURCE-01','R-MECH-01'} <= set(ids)
assert len([r for r in rows if r['requirement_id'].startswith('R-SOURCE-01-')]) == 32
inputs = (ROOT / 'docs/engineering/design-inputs.md').read_text()
for row in rows:
    assert None not in row and all(row[k] for k in ['requirement','owner_package','artifact','verification','current_status','current_evidence'])
    assert 'passed' not in row['current_status']
    for name in row['current_evidence'].split('; '):
        assert (ROOT / name).is_file(), name
    for dep in row['dependencies'].split('; '):
        if dep:
            assert f'| {dep} |' in inputs, dep
volume = next(r for r in rows if r['requirement_id'] == 'R-VOLUME-01')
assert all(t in volume['requirement'] for t in ['−20/−40/−60dB', '残余噪声', '声道匹配'])
assert all(t in volume['verification'] for t in ['先冻结低音量限值', '完整链路', '布局前', '模拟/混合衰减'])
assert 'docs/validation/analog-protocol.md' in volume['artifact']
safety = next(r for r in rows if r['requirement_id'] == 'R-SAFETY-01')
assert all(t in safety['requirement'] for t in ['固件升级', '失败恢复', '始终禁止模拟输出']), 'Missing update/recovery output protection'
assert all(t in safety['verification'] for t in ['升级', '中断', '失败恢复', '全过程', '禁止模拟输出']), 'Missing update/recovery verification scenarios'
assert all(t in safety['owner_package'] for t in ['Task 6', 'Task 9'])
assert 'docs/engineering/control-state-machine.csv' in safety['artifact']
assert 'docs/superpowers/plans/2026-10-25-streamer-implementation.md' in safety['current_evidence']
for id in ['R-SCOPE-01', 'R-SCOPE-02', 'R-SCOPE-03']:
    assert next(r for r in rows if r['requirement_id'] == id)['current_status'] == 'scope_pending'
for rel in ['docs/engineering/design-inputs.md','docs/specs/README.md','docs/design-clarifications.md','docs/progress-2026-10-25.md']:
    f = ROOT / rel
    for target in re.findall(r'\]\(([^)]+)\)', f.read_text()):
        if '://' in target or target.startswith('#'):
            continue
        assert (f.parent / unquote(target.split('#')[0])).exists(), (rel, target)
cli = subprocess.check_output(['kicad-cli','version'], text=True).strip()
assert cli == baseline['cli_version']
print(json.dumps({'result':'PASS','cad_and_library_hashes':len(baseline['cad_hashes']),
                  'netlist_components':33,'archived_files':len(files),'pdf_files':24,
                  'requirements':len(rows),'individual_source_targets':32,
                  'cli_version':cli,'checks':'hashes, manifest inventory/official URLs, all PDF page extraction, component identity, requirement ownership/dependencies/status, current evidence and Markdown links',
                  'limits':'Saved files only; no CAD mutation, electrical correctness, ERC/DRC or bench/system verdict'},ensure_ascii=False,indent=2))
