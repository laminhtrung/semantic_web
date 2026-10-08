"""Render the maintained Vietnamese Markdown documents without overwriting their content."""
import argparse
import subprocess
from pathlib import Path
from pypdf import PdfReader
from common import ROOT,write_json

DOCUMENTS=['Bao_cao','Huong_dan_A_Z','Huong_dan_thao_tac_chi_tiet','Mo_ta_ontology','Ontology_Redesign','Kich_ban_video','Script_thuyet_trinh','Checklist_anh_Protege','Script_thuyet_trinh_ngan_13']

def render(source):
    source=Path(source);docs=ROOT/'docs'
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
    write_json(ROOT/'evidence/document_pages.json',result);print(result)

if __name__=='__main__':main()
