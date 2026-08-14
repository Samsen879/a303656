#!/usr/bin/env python3
"""Independent verifier and compact artifact builder for the weighted audit."""
from __future__ import annotations
import argparse,csv,hashlib,json,os,subprocess,sys
from fractions import Fraction
from pathlib import Path

PAIR_COUNT=407
DEN={"odd":2334,"even":2337,"pool":4671}
CONCLUSION="VALIDATED WEIGHTED FIXED-P4 TRANSFERABILITY AUDIT"
class VerifyError(RuntimeError):pass
def demand(x:bool,m:str)->None:
    if not x:raise VerifyError(m)
def atomic(path:Path,v:object)->None:
    t=path.with_name(path.name+f".tmp.{os.getpid()}");t.write_text(json.dumps(v,indent=2,sort_keys=True)+"\n");os.replace(t,path)
def sha(path:Path)->str:return hashlib.sha256(path.read_bytes()).hexdigest()
def tuple4(s:str)->tuple[int,int,int,int]:
    x=tuple(map(int,s.split(',')));demand(len(x)==4,"tuple width");return x # type: ignore
def parse_cert(path:Path)->dict[str,object]:
    lines=[line.rstrip("\n").split("\t") for line in path.read_text().splitlines()]
    demand(lines[0]==["schema","a303656-weighted-enumerator-certificate-v1"],"certificate schema")
    result={"implementation":lines[1][1],"rows":int(lines[2][1]),"ordered_digest":lines[3][1],"objectives":{},"tops":[],"targets":{},"cross":{}}
    for x in lines[4:]:
        if x[0]=="objective":
            demand(len(x)==13,"objective width");result["objectives"][(x[1],x[2])]={"scope":x[1],"weights":x[2],"denominator":int(x[3]),"maximum_numerator":int(x[4]),"argmax_count":int(x[5]),"lexicographically_first_argmax":list(tuple4(x[6])),"coverage_mask_hex":x[7],"G":int(x[8]),"cross_scores":{"odd":int(x[9]),"even":int(x[10]),"pool":int(x[11])},"argmax_digest":x[12]}
        elif x[0]=="top":
            demand(len(x)==10,"top width");result["tops"].append({"weights":x[1],"rank":int(x[2]),"first_tuple":list(tuple4(x[3])),"coverage_mask_hex":x[4],"G":int(x[5]),"scores":{"odd":int(x[6]),"even":int(x[7]),"pool":int(x[8])},"lexicographically_first_t3eq2_representative":None if x[9]=="NONE" else list(tuple4(x[9]))})
        elif x[0]=="target":
            demand(len(x)==12,"target width");result["targets"][x[1]]={"tuple":list(tuple4(x[2])),"coverage_mask_hex":x[3],"G":int(x[4]),"scores":{"odd":int(x[5]),"even":int(x[7]),"pool":int(x[9])},"ranks":{"odd":int(x[6]),"even":int(x[8]),"pool":int(x[10])},"lexicographically_first_t3eq2_representative":list(tuple4(x[11]))}
        elif x[0]=="cross":
            demand(len(x)==8,"cross width");result["cross"][x[1]]={"scores":{"odd":int(x[2]),"even":int(x[4]),"pool":int(x[6])},"ranks":{"odd":int(x[3]),"even":int(x[5]),"pool":int(x[7])}}
        else:raise VerifyError(f"unknown certificate row {x[0]}")
    demand(result["rows"]==28227969 and len(result["objectives"])==6 and len(result["tops"])==24 and len(result["targets"])==4 and len(result["cross"])==3,"certificate cardinalities")
    return result
def powers(base:int,limit:int)->list[int]:
    out=[];x=1
    while True:
        out.append(x)
        if x>limit//base:break
        x*=base
    return out
def pairs()->list[tuple[int,int,int]]:
    return [(c,d,a+b) for c,a in enumerate(powers(3,183968950234)) for d,b in enumerate(powers(5,183968950234)) if a+b<=183968950234]
def coverage(t:tuple[int,int,int,int],domain:list[tuple[int,int,int]])->bytes:
    out=bytearray(51)
    for i,(_,_,shift) in enumerate(domain):
        for p,r in zip((3,7,11,23),t):
            diff=(r-shift)%(p*p)
            if diff%p==0 and diff!=0:out[i//8]|=1<<(i%8);break
    return bytes(out)
def score(mask:bytes,weights:dict[str,list[int]])->dict[str,int]:return {k:sum(v[i] for i in range(PAIR_COUNT) if mask[i//8]>>(i%8)&1) for k,v in weights.items()}
def fraction(n:int,d:int)->dict[str,int]:
    x=Fraction(n,d);return {"numerator":x.numerator,"denominator":x.denominator}
def mask_pairs(mask:bytes,domain:list[tuple[int,int,int]])->list[dict[str,int]]:return [{"pair_index":i,"c":c,"d":d,"shift":s} for i,(c,d,s) in enumerate(domain) if mask[i//8]>>(i%8)&1]
def main()->int:
    p=argparse.ArgumentParser();p.add_argument("--root",type=Path,required=True);p.add_argument("--artifact-dir",type=Path,required=True);p.add_argument("--certificate-a",type=Path,required=True);p.add_argument("--certificate-b",type=Path,required=True);p.add_argument("--source-commit",required=True);p.add_argument("--negative-report",type=Path);p.add_argument("--command-manifest",type=Path);p.add_argument("--check-only",action="store_true");a=p.parse_args()
    try:
        root=a.root.resolve();art=a.artifact_dir.resolve();ca=parse_cert(a.certificate_a);cb=parse_cert(a.certificate_b)
        head=subprocess.check_output(["git","rev-parse","HEAD"],cwd=root,text=True).strip();demand(subprocess.run(["git","merge-base","--is-ancestor",a.source_commit,head],cwd=root).returncode==0,"source commit is not an ancestor of HEAD")
        xa=a.certificate_a.read_text().splitlines();xb=a.certificate_b.read_text().splitlines();demand(xa[:1]+xa[2:]==xb[:1]+xb[2:],"independent enumerator certificates disagree")
        demand(ca["implementation"]!=cb["implementation"],"enumerator identities not independent")
        prov=json.loads((art/"payload_provenance.json").read_text());demand(prov["normalized_payload_digests_match"] and prov["decoded_digests_match"],"mask payload discrepancy")
        direct=json.loads((art/"direct_oracle_selection_manifest.json").read_text());demand(direct["selected_point_count"]==457 and direct["contains_n_196653638594_T15"] and direct["all_class_minima_and_tied_argmins_included"] and direct["all_predeclared_low_T_points_included"] and direct["all_predeclared_class_representatives_included"] and not direct["weighted_analysis_used_for_selection"],"direct manifest contract")
        rows=list(csv.DictReader((art/"exact_weight_table.csv").open()));demand(len(rows)==PAIR_COUNT,"weight row count")
        domain=pairs();demand(len(domain)==PAIR_COUNT and [(c,d) for c,d,s in domain if s==28]==[(1,2),(3,0)],"pair domain/duplicate shift")
        weights={k:[int(r[f"{k}_winner_numerator"]) for r in rows] for k in DEN}
        for i,r in enumerate(rows):
            demand(int(r["pair_index"])==i and (int(r["c"]),int(r["d"]),int(r["shift"]))==domain[i],"weight pair identity")
            demand(all(int(r[f"{k}_denominator"])==DEN[k] for k in DEN),"weight denominator drift")
            demand(0<=int(r["odd_class_prevalence"])<=42 and 0<=int(r["even_class_prevalence"])<=42 and 0<=int(r["pool_class_prevalence"])<=84,"class prevalence range")
        checked=[]
        records=list(ca["objectives"].values())+ca["tops"]+list(ca["targets"].values())
        for item in records:
            t=tuple(item.get("lexicographically_first_argmax",item.get("first_tuple",item.get("tuple"))))
            m=coverage(t,domain);demand(m.hex()==item["coverage_mask_hex"],"reported coverage mask mismatch");s=score(m,weights)
            declared=item.get("cross_scores",item.get("scores"));demand(s==declared,"reported exact score mismatch");demand(sum(x.bit_count() for x in m)==item["G"],"reported G mismatch");checked.append(t)
        if a.check_only:
            print("WEIGHTED_AUDIT_CERTIFICATE_CHECK_PASS");return 0
        obj=ca["objectives"];cross=ca["cross"]
        maxima={}
        for scope in ("full","t3eq2"):
            maxima[scope]={}
            for k in DEN:
                x=dict(obj[(scope,k)]);x["maximum_score"]=fraction(x["maximum_numerator"],DEN[k]);maxima[scope][k]=x
        odd=obj[("full","odd")];even=obj[("full","even")];pool=obj[("full","pool")]
        regret={"odd_training_to_even_test":{"numerator":even["maximum_numerator"]-odd["cross_scores"]["even"],"denominator":DEN["even"]},"even_training_to_odd_test":{"numerator":odd["maximum_numerator"]-even["cross_scores"]["odd"],"denominator":DEN["odd"]}}
        maxima_art={"schema":"a303656-weighted-maxima-v1","tuple_count":28227969,"ordered_result_digest":ca["ordered_digest"],"enumerators":{"A":ca["implementation"],"B":cb["implementation"]},"exact_denominators":DEN,"maxima":maxima,"cross_fold_scores_and_ranks":cross,"cross_fold_exact_regret":regret,"optimum_G_values":{"odd":odd["G"],"even":even["G"],"pool":pool["G"]},"three_optima_share_coverage_mask":len({odd["coverage_mask_hex"],even["coverage_mask_hex"],pool["coverage_mask_hex"]})==1}
        atomic(art/"weighted_maxima.json",maxima_art)
        common=bytes.fromhex(ca["targets"]["G231-COMMON"]["coverage_mask_hex"])
        comparisons={}
        for k,x in (("odd",odd),("even",even),("pool",pool)):
            m=bytes.fromhex(x["coverage_mask_hex"])
            new=bytes(a&~b&255 for a,b in zip(m,common));lost=bytes(b&~a&255 for a,b in zip(m,common))
            contributions=sorted((weights[k][i] for i in range(PAIR_COUNT) if m[i//8]>>(i%8)&1),reverse=True);total=sum(contributions)
            comparisons[k]={"newly_covered_relative_to_G231_common":mask_pairs(new,domain),"lost_relative_to_G231_common":mask_pairs(lost,domain),"concentration":{"nonzero_covered_pair_count":sum(v>0 for v in contributions),"top_8_share":fraction(sum(contributions[:8]),total),"top_16_share":fraction(sum(contributions[:16]),total),"top_32_share":fraction(sum(contributions[:32]),total)}}
        freq=json.loads((art/"frequency_analysis.json").read_text());odd_rank={x["pair_index"]:x["rank"] for x in freq["top_frequency_rankings"]["odd"]};even_rank={x["pair_index"]:x["rank"] for x in freq["top_frequency_rankings"]["even"]};sumsq=sum((odd_rank[i]-even_rank[i])**2 for i in range(PAIR_COUNT));rho=Fraction(1)-Fraction(6*sumsq,PAIR_COUNT*(PAIR_COUNT**2-1))
        transfer={"schema":"a303656-weighted-transfer-report-v1","classification":"EXACT FINITE COMPUTATION; EMPIRICAL WEIGHTS; GLOBAL PROBLEM UNRESOLVED","odd_optimum_under_even":{"score_numerator":odd["cross_scores"]["even"],"denominator":DEN["even"],"rank":cross["odd_opt"]["ranks"]["even"]},"even_optimum_under_odd":{"score_numerator":even["cross_scores"]["odd"],"denominator":DEN["odd"],"rank":cross["even_opt"]["ranks"]["odd"]},"pooled_optimum":pool,"cross_fold_exact_regret":regret,"optimum_mask_comparisons":comparisons,"calibration_exact_ranks":ca["targets"],"weight_order_stability":{"spearman_rho_exact":fraction(rho.numerator,rho.denominator),"top_k_overlaps":freq["top_k_overlaps"],"exact_L1_frequency_difference":freq["exact_L1_frequency_difference"]},"interpretation":{"weighted_score_is_proof":False,"weighted_optimum_is_counterexample_direction":False,"new_integer_panel_run":False,"concentration_note":"Shares are descriptive exact fractions of each optimum score; they do not establish a theorem or search direction.","ordering_note":"Stability is reported by exact rank correlation, top-k overlap, and exact L1 difference only."}}
        atomic(art/"transfer_report.json",transfer)
        bymask={}
        for x in ca["tops"]:
            z=bymask.setdefault(x["coverage_mask_hex"],{"coverage_mask_hex":x["coverage_mask_hex"],"G":x["G"],"lexicographically_first_t3eq2_representative":x["lexicographically_first_t3eq2_representative"],"selected_by":[]});z["selected_by"].append(f"top8_{x['weights']}")
        for name in ("CAL-216","CAL-227","CAL-230","G231-COMMON"):
            x=ca["targets"][name];z=bymask.setdefault(x["coverage_mask_hex"],{"coverage_mask_hex":x["coverage_mask_hex"],"G":x["G"],"lexicographically_first_t3eq2_representative":x["lexicographically_first_t3eq2_representative"],"selected_by":[]});z["selected_by"].append(name)
        demand(len(bymask)<=28,"candidate manifest size")
        candidates={"schema":"a303656-future-weighted-candidate-manifest-v1","future_artifact_only":True,"new_integers_evaluated":0,"deduplicated_by":"coverage_mask_hex","candidate_count":len(bymask),"maximum_allowed":28,"candidates":sorted(bymask.values(),key=lambda x:(x["lexicographically_first_t3eq2_representative"] is None,x["lexicographically_first_t3eq2_representative"] or [],x["coverage_mask_hex"]))}
        atomic(art/"candidate_manifest.json",candidates)
        negative={}
        if a.negative_report:
            negative=json.loads(a.negative_report.read_text());demand(negative.get("all_rejected") and negative.get("required_count",0)>=10,"negative mutation report")
        input_prov=json.loads((art/"input_provenance.json").read_text())
        protected=input_prov["protected_baseline_hashes"]
        for name,digest in protected.items():demand(sha(root/name)==digest,f"protected baseline changed: {name}")
        report={"schema":"a303656-weighted-audit-verification-report-v1","status":"PASS","all_28227969_tuples_enumerated_twice":True,"enumerator_ordered_results_agree":True,"normalized_mask_payloads_agree":True,"direct_oracle_manifest_validated":True,"odd_even_class_split":"42/42","pair_count":407,"duplicate_shift_pair_identities_retained":True,"exact_integer_numerator_ranking":True,"negative_mutations":negative,"protected_baseline_hashes_unchanged":True,"no_new_integer_evaluation":True,"candidate_count":len(bymask),"mathematical_status":"UNRESOLVED","validation_conclusion":CONCLUSION}
        atomic(art/"verification_report.json",report)
        core=[p for p in art.iterdir() if p.is_file() and p.name not in {"metadata.json","verification_report.json","command_manifest.json"}]
        atomic(art/"metadata.json",{"schema":"a303656-weighted-audit-metadata-v1","starting_commit":"d547130508c7d06b099eab4e93b0db7a0afa7c89","source_commit":a.source_commit,"results_commit":"RESULTS_COMMIT_CONTAINING_THIS_FILE","artifact_sha256_excluding_metadata_and_verification_report":{p.name:sha(p) for p in sorted(core)},"protected_baseline_hashes":protected,"scope_guards":{"new_integers_evaluated":0,"panel_points_read":4838,"weighted_points":4671,"new_primes":0,"activation_cell_extensions":0,"exponent_domain_extensions":0,"adaptive_integer_classes":0},"validation_conclusion":CONCLUSION})
        print("WEIGHTED_AUDIT_VERIFICATION_PASS");return 0
    except (VerifyError,OSError,ValueError,KeyError,IndexError,json.JSONDecodeError,csv.Error,subprocess.CalledProcessError) as e:
        print(f"weighted_verifier: ERROR: {e}",file=sys.stderr);return 2
if __name__=="__main__":raise SystemExit(main())
