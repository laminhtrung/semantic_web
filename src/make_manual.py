"""Render the detailed operation guide without overwriting its Markdown source."""
import os
import json
import subprocess
import tempfile
from pathlib import Path

from common import ROOT


def main():
    docs = ROOT / 'docs'
    source = docs / 'Huong_dan_thao_tac_chi_tiet.md'
    with tempfile.TemporaryDirectory(prefix='movie-lod-manual-') as temporary:
        work = Path(temporary)
        header = (docs / 'latex_header.tex').read_text(encoding='utf-8')
        header = header.replace('MovieLOD · Bài làm hoàn chỉnh',
                                'MovieLOD · Hướng dẫn thao tác')
        header = header.replace(r'\setlength{\parskip}{4pt}',
                                r'\setlength{\parskip}{3pt}')
        header += r'''
\usepackage{needspace}
\usepackage{xurl}
\usepackage{float}
\floatplacement{figure}{H}
\setlength{\tabcolsep}{4pt}
\setlength{\emergencystretch}{5em}
'''
        header_path = work / 'header.tex'
        header_path.write_text(header, encoding='utf-8')
        layout = work / 'layout.lua'
        layout.write_text('local docs_directory = ' + json.dumps(str(docs), ensure_ascii=False) + '\n' + r'''
function Image(el)
  if not el.src:match('^%a+:') and el.src:sub(1,1) ~= '/' then
    el.src = pandoc.path.normalize(pandoc.path.join({docs_directory, el.src}))
  end
  return el
end
function Table(el)
  local widths
  if #el.colspecs == 2 then widths = {0.42, 0.58}
  elseif #el.colspecs == 3 then widths = {0.20, 0.42, 0.38} end
  if widths then
    local columns = {}
    for i=1,#widths do columns[i] = {el.colspecs[i][1], widths[i]} end
    el.colspecs = columns
  end
  return el
end
function Header(el)
  if el.level <= 3 then
    return {pandoc.RawBlock('latex', '\\Needspace{5\\baselineskip}'), el}
  end
end
''', encoding='utf-8')
        code_filter = work / 'code-wrap.lua'
        code = (docs / 'code-wrap.lua').read_text(encoding='utf-8')
        code = code.replace("char == ':' then", "char == ':' or char == '.' then")
        code_filter.write_text(code, encoding='utf-8')
        tex = work / 'Huong_dan_thao_tac_chi_tiet.tex'
        subprocess.run([
            'pandoc', str(source), '--standalone', '--from=markdown', '--to=latex',
            '--toc', '--toc-depth=2',
            '--resource-path=' + os.pathsep.join([str(docs), str(ROOT)]),
            '--lua-filter=' + str(code_filter), '--lua-filter=' + str(layout),
            '--include-in-header=' + str(header_path),
            '-V', 'documentclass=article', '-V', 'fontsize=11pt',
            '-V', 'geometry:a4paper,margin=19mm',
            '-V', 'mainfont=Be Vietnam Pro', '-V', 'monofont=Menlo',
            '-V', 'colorlinks=true', '-V', 'linkcolor=teal', '-V', 'urlcolor=teal',
            '--syntax-highlighting=none', '-o', str(tex),
        ], check=True, cwd=ROOT)
        log_path = ROOT / 'evidence/build_Huong_dan_thao_tac_chi_tiet.log'
        with log_path.open('w', encoding='utf-8') as log:
            subprocess.run(['tectonic', str(tex), '--outdir', str(docs)],
                           check=True, cwd=docs, stdout=log, stderr=log)
    print('Manual created:', docs / 'Huong_dan_thao_tac_chi_tiet.pdf')


if __name__ == '__main__':
    main()
