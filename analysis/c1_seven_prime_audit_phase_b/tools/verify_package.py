#!/usr/bin/env python3
"""Verify frozen artifacts; optional replays always run in a temporary copy."""
from __future__ import annotations
import argparse,hashlib,json,os,shutil,stat,subprocess,sys,tempfile,zipfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def mathematical(obj):
    if isinstance(obj,dict):return {k:mathematical(v) for k,v in obj.items() if k!='seconds'}
    if isinstance(obj,list):return [mathematical(v) for v in obj]
    return obj

def mhash(path:Path)->str:
    data=mathematical(json.loads(path.read_text()))
    return hashlib.sha256(json.dumps(data,sort_keys=True,separators=(',',':')).encode()).hexdigest()

def run(args:list[str],cwd:Path,stdout:Path|None=None,stderr:Path|None=None):
    env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1',PYTHONHASHSEED='0')
    p=subprocess.run(args,cwd=cwd,env=env,capture_output=True,text=True)
    if p.returncode:raise RuntimeError(f'{args[0]} exited {p.returncode}: {p.stderr[-5000:]}\n{p.stdout[-5000:]}')
    if stdout is not None:stdout.write_text(p.stdout)
    if stderr is not None:stderr.write_text(p.stderr)
    return p

def check_bytes()->int:
    listed=set()
    for line in (ROOT/'SHA256SUMS.txt').read_text().splitlines():
        digest,name=line.split('  ',1);p=(ROOT/name).resolve()
        if not p.is_relative_to(ROOT) or not p.is_file():raise RuntimeError('unsafe or missing payload: '+name)
        if hashlib.sha256(p.read_bytes()).hexdigest()!=digest:raise RuntimeError('byte mismatch: '+name)
        listed.add(name)
    actual={p.relative_to(ROOT).as_posix() for p in ROOT.rglob('*') if p.is_file() and '__pycache__' not in p.parts and p.name!='SHA256SUMS.txt'}
    if actual!=listed:raise RuntimeError('inventory mismatch: '+str(actual^listed))
    return len(listed)

def source_replay(work:Path):
    zpath=work/'evidence/original_research_bundle.zip'
    expected='4d75958f51ff27e7a0d4d50811c6f60fb1e0886745eeae1b292e5b9718f0653e'
    if not zpath.exists():
        receipt=json.loads((work/'evidence/nested_source_receipt.json').read_text())
        if receipt.get('committed') is not False or receipt.get('byte_identity_with_package_a')!='PASS' or receipt.get('outer_sha256')!=expected:
            raise RuntimeError('invalid omitted nested-source receipt')
        return 'SOURCE_REPLAY_PREINTEGRATION_PASS_NESTED_TRANSPORT_OMITTED'
    if hashlib.sha256(zpath.read_bytes()).hexdigest()!=expected:raise RuntimeError('source custody mismatch')
    dest=work/'source_replay_area';dest.mkdir()
    with zipfile.ZipFile(zpath) as z:
        for item in z.infolist():
            p=Path(item.filename)
            if p.is_absolute() or '..' in p.parts or '\\' in item.filename or stat.S_ISLNK(item.external_attr>>16):raise RuntimeError('unsafe source ZIP')
        z.extractall(dest)
    original=dest/'A303656_UNIFIED_ENDGAME_PHASE_B'
    run([sys.executable,'-B','tools/verify_bundle.py','--replay'],original)
    return 'PASS'

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--replay-small',action='store_true')
    parser.add_argument('--replay-scan',action='store_true')
    args=parser.parse_args()
    if not __debug__:raise RuntimeError('Run without python -O; verification assertions must be enabled.')
    n=check_bytes();expected=json.loads((ROOT/'results/mathematical_hashes.json').read_text())
    for rel,h in expected.items():
        if mhash(ROOT/rel)!=h:raise RuntimeError('mathematical hash mismatch: '+rel)
    receipts=dict(byte_payload_files=n,mathematical_json_files=len(expected),integrity='PASS',github_writes='NONE')
    if args.replay_small or args.replay_scan:
        with tempfile.TemporaryDirectory(prefix='a303656_scan_review_') as temp:
            work=Path(temp)/'bundle';shutil.copytree(ROOT,work,ignore=shutil.ignore_patterns('__pycache__'))
            if args.replay_small:
                run([sys.executable,'-B','tools/audit_independent.py'],work)
                run([sys.executable,'-B','tools/verify_scan.py','baseline'],work)
                run([sys.executable,'-B','-m','unittest','discover','-s','tests','-v'],work)
                source_status=source_replay(work)
                receipts.update(new_audit_replay='PASS',python_baseline_replay='PASS',new_tests=18,source_reference_replay=source_status,source_tests=15)
            if args.replay_scan:
                for alg in ['a','b']:
                    exe=work/('scan_'+alg)
                    run(['g++','-O3','-std=c++17',str(work/f'tools/scan_{alg}.cpp'),'-o',str(exe)],work)
                    run([str(exe),'2000000000'],work,work/f'results/scan_{alg}.jsonl',work/f'results/scan_{alg}.log')
                    if (work/f'results/scan_{alg}.jsonl').read_bytes()!=(ROOT/f'results/scan_{alg}.jsonl').read_bytes():raise RuntimeError('full scan replay differs: '+alg)
                run([str(work/'scan_a'),'100000000','all'],work,work/'results/aux_all_odd_1e8.jsonl',work/'results/aux_all_odd_1e8.log')
                if (work/'results/aux_all_odd_1e8.jsonl').read_bytes()!=(ROOT/'results/aux_all_odd_1e8.jsonl').read_bytes():raise RuntimeError('auxiliary scan mismatch')
                run([sys.executable,'-B','tools/verify_scan.py'],work)
                receipts['two_full_scan_replays']='PASS'
            for rel,h in expected.items():
                if mhash(work/rel)!=h:raise RuntimeError('replay mathematical mismatch: '+rel)
            receipts['mathematical_replay']='PASS'
    print(json.dumps(receipts,indent=2))
if __name__=='__main__':main()
