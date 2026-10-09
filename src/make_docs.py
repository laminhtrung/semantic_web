"""Render the maintained Vietnamese Markdown documents without overwriting their content."""
import argparse
import subprocess
from pathlib import Path
from pypdf import PdfReader
from common import ROOT,write_json

DOCUMENTS=['Bao_cao','Huong_dan_A_Z','Huong_dan_thao_tac_chi_tiet','Mo_ta_ontology','Ontology_Redesign','Kich_ban_video','Script_thuyet_trinh','Checklist_anh_Protege','Script_thuyet_trinh_ngan_13','Ket_qua_reasoner','Huong_dan_doc_hieu_project']

def render(source):
    source=Path(source);docs=ROOT/'docs'
    if source.name=='Huong_dan_doc_hieu_project.md':
        from make_reading_guide import main as make_guide
        make_guide()
        return len(PdfReader(source.with_suffix('.pdf')).pages)
    if source.name=='Bao_cao.md':
        from make_report import main as make_report
        return make_report()
    header=docs/'latex_header.tex'
    subprocess.run(['pandoc',str(source),'--standalone','--from=markdown','--to=latex','--resource-path='+str(ROOT)+':'+str(docs),'--lua-filter='+str(docs/'code-wrap.lua'),'--include-in-header='+str(header),'-V','documentclass=article','-V','fontsize=11pt','-V','geometry:a4paper,margin=19mm','-V','mainfont=Be Vietnam Pro','-V','monofont=Menlo','-V','colorlinks=true','-V','linkcolor=teal','-V','urlcolor=teal','--syntax-highlighting=none','-o',str(source.with_suffix('.tex'))],check=True,cwd=docs)
    log=ROOT/'evidence'/('build_'+source.stem+'.log')
    with log.open('w') as f:subprocess.run(['tectonic',str(source.with_suffix('.tex'))],check=True,cwd=source.parent,stdout=f,stderr=f)
    return len(PdfReader(source.with_suffix('.pdf')).pages)

def main():
    p=argparse.ArgumentParser();p.add_argument('files',nargs='*');args=p.parse_args()
    files=[ROOT/f for f in args.files] if args.files else [ROOT/'docs'/f'{n}.md' for n in DOCUMENTS]+[ROOT/'CHAM_DIEM.md']
    result={str(f.relative_to(ROOT)):render(f) for f in files}
    if 'docs/Bao_cao.md' in result:assert result['docs/Bao_cao.md']<=15,result
    record=ROOT/'evidence/document_pages.json'
    import json
    existing=json.loads(record.read_text()) if record.exists() else {}
    existing.update(result);write_json(record,existing);print(result)

if __name__=='__main__':main()
