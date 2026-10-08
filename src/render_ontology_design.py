"""Render the independently validated ontology design into readable offline artifacts."""
import hashlib, json, subprocess, zipfile
from pathlib import Path
from common import ROOT, write_json

def main():
    from audit_ontology_design import main as audit
    audit()
    md=ROOT/'docs/DBpedia_OWL_Design.md';out=md.with_suffix('.html')
    css='''body{font-family:"Times New Roman",serif;font-size:18px;line-height:1.5;color:#172b3a;max-width:1400px;margin:32px auto;padding:24px}h1,h2,h3{color:#075a66;line-height:1.25}h2{border-bottom:2px solid #b9d9dd;padding-bottom:8px;margin-top:42px}a{color:#006a83}table{display:block;overflow-x:auto;border-collapse:collapse;width:100%;font-size:16px;margin:20px 0}th,td{border:1px solid #c4d2d6;padding:10px;vertical-align:top;min-width:105px}th{background:#e8f4f4;text-align:left}tr:nth-child(even){background:#f8fbfc}pre{white-space:pre-wrap;overflow-wrap:anywhere;background:#edf3f5;padding:18px;border-radius:6px;font-size:14px;line-height:1.45}code{font-family:Menlo,monospace;font-size:.82em;overflow-wrap:anywhere}nav{background:#eff7f8;padding:20px}p{overflow-wrap:anywhere}@media print{body{font-size:13pt;max-width:none;margin:0;padding:0}table{font-size:10pt;display:table;table-layout:fixed}td,th{min-width:0;overflow-wrap:anywhere;padding:4px}pre{font-size:9pt}h2{break-before:page}h3{break-after:avoid}}'''
    header=ROOT/'evidence/ontology_design/html_header.html';header.write_text('<style>'+css+'</style>')
    subprocess.run(['pandoc',str(md),'--standalone','--toc','--toc-depth=2','--metadata','title=DBpedia Movie Ontology — Verified Design','--include-in-header',str(header),'-o',str(out)],check=True)
    # Editable Word reference: preserve familiar Times New Roman / 13 / 1.5 body formatting.
    from docx import Document
    from docx.shared import Pt,Cm
    d=Document();normal=d.styles['Normal'];normal.font.name='Times New Roman';normal.font.size=Pt(13);normal.paragraph_format.line_spacing=1.5
    for sec in d.sections:sec.page_width=Cm(21);sec.page_height=Cm(29.7);sec.left_margin=Cm(3);sec.right_margin=Cm(2);sec.top_margin=Cm(2);sec.bottom_margin=Cm(2)
    for n in ['Heading 1','Heading 2','Heading 3']:d.styles[n].font.name='Times New Roman';d.styles[n].font.size=Pt(13)
    reference=ROOT/'evidence/ontology_design/reference.docx';d.save(reference)
    subprocess.run(['pandoc',str(md),'--reference-doc='+str(reference),'-o',str(md.with_suffix('.docx'))],check=True)
    readme=ROOT/'evidence/ontology_design/README.md'
    readme.write_text('''# Cách sử dụng bản thiết kế đã kiểm chứng

Đây là bản đề xuất độc lập từ dữ liệu hiện có, chưa thay ontology/app đang dùng.

- Đọc docs/DBpedia_OWL_Design.html để xem đủ 7 bảng, định nghĩa OWL, 5 demo và kết quả truy vấn. Bảng rộng có thể cuộn ngang.
- schema.ttl chứa các tiên đề; asserted.ttl chỉ chứa dữ liệu đầu vào; inferred.ttl chứa kết quả suy luận.
- Trong Protégé: mở complete.ttl rồi chọn HermiT → Start reasoner. Đây là đồ thị đầy đủ chứa schema + facts, chưa gán thủ công các lớp suy luận.
- Có thể tạo tạm một OWL đầy đủ từ `Graph().parse("schema.ttl") + Graph().parse("asserted.ttl")` bằng RDFLib. Tắt normalization của xsd:dateTime hoặc chuyển lexical timestamp về 3 chữ số thập phân trước khi serialize để tương thích HermiT cũ.
- Query 01–08 chạy với asserted.ttl. Query 09–26 chạy với tổng schema + asserted + inferred. Query 27 chạy trên before_after.trig (hai named graph).
- reasoning.json ghi số lượng local URI; query_results.json ghi số dòng truy vấn, có thể bao gồm sameAs alias ở một số câu hierarchy.
- hermit.log là log thật; cardinality_negative.log xác nhận MultiGenreFilm không có member suy luận. Không thêm AllDifferent cho genre/film/award để ép điểm.
- exactly 1 không thay cho kiểm tra dữ liệu thiếu trong mô hình thế giới mở.
- Không sửa Video_demo.mp4; không tạo bản OWL thứ hai làm file chính.
''')
    bundle=ROOT/'docs/DBpedia_OWL_Design.zip'
    with zipfile.ZipFile(bundle,'w',zipfile.ZIP_DEFLATED) as z:
        for p in [md,md.with_suffix('.html'),md.with_suffix('.docx')]:z.write(p,'docs/'+p.name)
        for p in sorted((ROOT/'queries/design').glob('*.rq')):z.write(p,'queries/design/'+p.name)
        for name in ['complete.ttl','schema.ttl','asserted.ttl','inferred.ttl','before_after.trig','reasoning.json','query_results.json','source_mapping.json','hermit.log','cardinality_negative.log','classification_input.json','checks.json','README.md']:
            p=ROOT/'evidence/ontology_design'/name;z.write(p,'evidence/'+name)
    write_json(ROOT/'evidence/ontology_design/deliverables.json',{'artifacts':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in [md,md.with_suffix('.html'),md.with_suffix('.docx'),bundle]},'authoritative_owl_unmodified':True,'app_unmodified':True,'video_sha256':hashlib.sha256((ROOT/'docs/Video_demo.mp4').read_bytes()).hexdigest()})
    print(bundle)
if __name__=='__main__':main()
