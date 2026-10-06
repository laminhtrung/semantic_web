"""Create editable PPTX, slide PDF, and a 4:16 Vietnamese narrated demonstration."""
import json
import math
import subprocess
import textwrap
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
from pptx import Presentation
from pptx.util import Inches,Pt
from pptx.dml.color import RGBColor
from common import ROOT,BASE,write_json

W,H=1920,1080
BG='#102632';WHITE='#f5fbff';ACCENT='#ffd361';MUTED='#a9c0cc'
FONT_DIR=Path.home()/'Library/Fonts'
def font(size,bold=False):
    path=FONT_DIR/('BeVietnamPro-Bold.ttf' if bold else 'BeVietnamPro-Regular.ttf')
    if not path.exists():path=Path('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf')
    return ImageFont.truetype(str(path),size)

def wrap(draw,text,f,max_width):
    lines=[];line=''
    for word in text.split():
        candidate=(line+' '+word).strip()
        if draw.textlength(candidate,font=f)>max_width and line:
            lines.append(line);line=word
        else:line=candidate
    if line:lines.append(line)
    return lines

def text(draw,xy,words,f,fill,max_width,line_height):
    x,y=xy
    for line in wrap(draw,words,f,max_width):
        draw.text((x,y),line,font=f,fill=fill);y+=line_height
    return y

def slides_spec(s):
    return [
      {'title':'MovieLOD', 'subtitle':'Ứng dụng dữ liệu phim liên kết',
       'bullets':['9 lớp: mô hình vừa đủ cho lĩnh vực phim',f"{s['films']} phim thật • {s['same_as']} liên kết ngoài",'Nguồn → RDF → liên kết → truy vấn → công bố'],
       'speech':'Bài làm này xây dựng Movie L O D, một ứng dụng dữ liệu phim liên kết. Mục tiêu là hoàn thành cả năm yêu cầu của đề, từ mô hình hóa, thu thập và chuyển đổi dữ liệu, đến liên kết ngoài và truy vấn. Thay vì mở rộng quá nhiều khái niệm, mô hình chỉ dùng chín lớp cần thiết. Chúng ta sẽ theo dõi một ví dụ quen thuộc: phim Inception và đạo diễn Christopher Nolan.'},
      {'title':'YC1 · Ontology', 'subtitle':'Ontology = mô hình khái niệm và quan hệ',
       'bullets':['Tái sử dụng: dbo:Film, dbo:Person, dbo:Country','6 lớp ex: cho thể loại, ngôn ngữ, đóng góp và nguồn','Một credit = 1 phim + 1 người + 1 vai trò','Ba vai trò: đạo diễn, diễn viên, biên kịch'],
       'speech':'Yêu cầu thứ nhất là định nghĩa mô hình cho lĩnh vực điện ảnh. Bài tái sử dụng trực tiếp ba lớp của DBpedia: Film cho phim, Person cho người và Country cho quốc gia. Sáu lớp của bài mô tả thể loại, ngôn ngữ, đóng góp, vai trò, nguồn và bộ dữ liệu. Mỗi bản ghi đóng góp nối đúng một phim, một người và một vai trò. Vì vậy, Nolan có thể làm đạo diễn và biên kịch trong cùng phim mà hai công việc vẫn được phân biệt rõ.'},
      {'title':'YC2 · Dữ liệu thật, có nguồn', 'subtitle':'Thu thập và lưu phản hồi gốc',
       'bullets':[f"{s['films']} phim • {s['persons']} người • {s['credits']} credit",'Wikidata: đối chiếu đúng sitelink Wikipedia','DBpedia: kiểm tra chủ thể đúng kiểu Film',f"{s['snapshots']} phản hồi: URL + thời điểm + SHA-256"],
       'speech':'Yêu cầu thứ hai là thu thập dữ liệu thật. Danh sách chọn gồm ba mươi phim. Chương trình tải thông tin từ Wikidata và DBpedia. Danh tính được xác định bằng liên kết Wikipedia chính xác, thay vì đoán từ tên gần giống. Các phản hồi gốc được giữ nguyên, kèm địa chỉ nguồn, thời điểm lấy và mã băm. Mã băm giúp kiểm tra nội dung có bị thay đổi hay không. Bộ dữ liệu này là một mẫu phục vụ học tập, không phải toàn bộ điện ảnh.'},
      {'title':'YC3 · Chuyển thành RDF', 'subtitle':'RDF = câu dữ liệu có ba thành phần',
       'bullets':['Inception → đạo diễn → Christopher Nolan','QID tạo định danh ổn định; thời lượng đổi về phút',f"{s['data_triples']:,} triple • Turtle • JSON-LD • OWL",'Giấy phép mở + IRI tra cứu + dữ liệu trên Web'],
       'speech':'Yêu cầu thứ ba là chuyển thông tin thành dữ liệu liên kết. Mỗi câu có ba thành phần: chủ thể, quan hệ và đối tượng hoặc giá trị. Ví dụ, Inception có đạo diễn là Christopher Nolan. Mã nguồn tạo định danh ổn định từ mã thực thể, chuyển thời lượng về phút và thêm nguồn cho từng bản ghi. Dữ liệu được xuất theo các định dạng mở. Điều kiện bốn sao còn yêu cầu giấy phép mở và dữ liệu được công bố trên Web.'},
      {'title':'YC4 · Liên kết ngoài', 'subtitle':'sameAs = hai định danh chỉ cùng một thực thể',
       'bullets':['Inception nội bộ ↔ Wikidata Q25188 ↔ DBpedia',f"{s['wikidata_links']} liên kết Wikidata + {s['dbpedia_links']} DBpedia",'Mỗi liên kết có phương pháp đối chiếu trong biên bản','5 sao = điều kiện 4 sao + liên kết tới dữ liệu khác'],
       'speech':'Yêu cầu thứ tư là nối dữ liệu với những bộ dữ liệu khác. Phim Inception trong ứng dụng được nối với mã thực thể tương ứng của Wikidata và DBpedia. Quan hệ same as khẳng định hai định danh chỉ cùng một thực thể, còn quan hệ nguồn nói thông tin được lấy từ đâu. Bài lưu biên bản cho từng liên kết để có thể kiểm tra phương pháp nối. Điều kiện năm sao được xây dựng trên điều kiện bốn sao đã đáp ứng.'},
      {'title':'YC5 · Chạy truy vấn Inception', 'subtitle':'Ảnh giao diện thật: truy vấn → bảng kết quả',
       'image':'01_app.png',
       'speech':'Đây là giao diện thật của ứng dụng. Bên trái là câu hỏi mẫu và ô nhập truy vấn. Bên phải là kết quả. Câu hỏi về Inception trả về tên phim, năm hai nghìn mười, thời lượng một trăm bốn mươi tám phút và Christopher Nolan. Người dùng có thể sửa câu truy vấn, chạy lại và tải kết quả. Khi chạy cục bộ, giao diện gọi dịch vụ truy vấn của ứng dụng. Bản hosted truy vấn bộ dữ liệu ngay trong trình duyệt.'},
      {'title':'Demo · Phim của Nolan và tra cứu IRI', 'subtitle':'Thay câu hỏi; mở thực thể để xem thông tin và nguồn',
       'image':'02_nolan.png',
       'speech':'Thay câu hỏi mẫu sang các phim do Nolan đạo diễn, chúng ta nhận được bảng các phim trong bộ dữ liệu. Đây là kết quả truy vấn đồ thị của bài, không phải danh sách nhập cứng trong giao diện. Ngoài giao diện Web, bài có dịch vụ truy vấn và cách chạy ở terminal. Người dùng còn mở được định danh của một phim để xem thuộc tính, liên kết ngoài và nguồn. Mỗi trang có bản mô tả dữ liệu máy có thể đọc.'},
      {'title':'Kiểm tra và sản phẩm nộp', 'subtitle':'Mỗi yêu cầu đi kèm mã và minh chứng',
       'bullets':['Python: kiểm tra dữ liệu; SHA-256: kiểm tra nguồn','8 truy vấn mẫu • 8 test tự động • kiểm tra trình duyệt','Báo cáo ≤15 trang • slide • video 3–5 phút','Công khai bản hosted để hoàn tất Open Data trên Web'],
       'speech':'Cuối cùng, bài có kiểm tra cấu trúc dữ liệu, kiểm tra toàn vẹn nguồn, tám truy vấn mẫu và tám bài kiểm tra tự động. Giao diện cũng được thử trên màn hình máy tính và điện thoại. Bộ nộp gồm mã, dữ liệu, báo cáo, slide và video này. Mọi kết quả kiểm tra được lưu để xem lại. Phần Open Data trên Web chỉ được xác nhận khi chủ sở hữu cho phép bản hosted truy cập công khai; trạng thái thực tế luôn được ghi trong biên bản xuất bản.'}
    ]

def create_slides(spec):
    out=ROOT/'docs/slides';out.mkdir(parents=True,exist_ok=True)
    prs=Presentation();prs.slide_width=Inches(16);prs.slide_height=Inches(9)
    pngs=[]
    for i,slide in enumerate(spec,1):
        image=Image.new('RGB',(W,H),BG);d=ImageDraw.Draw(image)
        d.rectangle((0,0,15,H),fill=ACCENT)
        d.text((100,70),'MOVIELOD / SEMANTIC WEB',font=font(25,True),fill=ACCENT)
        text(d,(100,130),slide['title'],font(62,True),WHITE,W-200,77)
        text(d,(102,230),slide['subtitle'],font(33),MUTED,W-204,43)
        if slide.get('image'):
            shot=Image.open(ROOT/'evidence/screenshots'/slide['image']).convert('RGB')
            shot.thumbnail((1720,700))
            image.paste(shot,((W-shot.width)//2,318))
        else:
            y=365
            for bullet in slide['bullets']:
                d.ellipse((110,y+18,126,y+34),fill=ACCENT)
                y=text(d,(155,y),bullet,font(39),WHITE,W-260,54)+42
        d.text((100,H-75),'Định nghĩa → Thu thập → RDF → Liên kết → Truy vấn',font=font(22),fill=MUTED)
        d.text((W-150,H-75),f'{i:02d} / 08',font=font(22),fill=ACCENT)
        path=out/f'{i:02d}.png';image.save(path);pngs.append(path)
        # The slide has editable title/body text; screenshots remain normal image elements.
        ps=prs.slides.add_slide(prs.slide_layouts[6])
        ps.background.fill.solid();ps.background.fill.fore_color.rgb=RGBColor.from_string('102632')
        def box(x,y,w,h,txt,size,color,bold=False):
            tb=ps.shapes.add_textbox(Inches(x),Inches(y),Inches(w),Inches(h));tf=tb.text_frame;tf.word_wrap=True
            p=tf.paragraphs[0];p.text=txt;p.font.name='Be Vietnam Pro';p.font.size=Pt(size);p.font.bold=bold;p.font.color.rgb=RGBColor.from_string(color)
        box(.8,.45,14,.4,'MOVIELOD / SEMANTIC WEB',14,'FFD361',True)
        box(.8,1.05,14,1.1,slide['title'],36,'F5FBFF',True)
        box(.8,1.95,14,.65,slide['subtitle'],20,'A9C0CC')
        if slide.get('image'):
            ps.shapes.add_picture(str(ROOT/'evidence/screenshots'/slide['image']),Inches(2.3),Inches(2.75),height=Inches(5.8))
        else:
            for j,b in enumerate(slide['bullets']):box(.95,3.05+j*1.12,14,1.0,'• '+b,25,'F5FBFF')
        box(.8,8.4,13,.4,'Định nghĩa → Thu thập → RDF → Liên kết → Truy vấn',13,'A9C0CC')
        box(14.8,8.4,1,.4,str(i)+'/8',13,'FFD361')
        ps.notes_slide.notes_text_frame.text=slide['speech']
    prs.save(ROOT/'docs/Slide.pptx')
    pages=[Image.open(p).convert('RGB') for p in pngs]
    pages[0].save(ROOT/'docs/Slide.pdf',save_all=True,append_images=pages[1:],resolution=120)
    script=['# Kịch bản video 4 phút 16 giây','', 'Video dùng giọng tiếng Việt tổng hợp Linh, slide và ảnh ứng dụng thật. Có thể dùng lời này để tự thuyết trình lại.','']
    for i,s in enumerate(spec):
        start=i*32;end=start+32
        script.extend([f"## {start//60}:{start%60:02d}–{end//60}:{end%60:02d} — {s['title']}",'',s['speech'],''])
    (ROOT/'docs/Kich_ban_video.md').write_text('\n'.join(script),encoding='utf-8')
    return pngs

def create_video(spec,pngs):
    out=ROOT/'docs/video_parts';out.mkdir(parents=True,exist_ok=True)
    segments=[]
    for i,(slide,png) in enumerate(zip(spec,pngs),1):
        txt=out/f'{i:02d}.txt';txt.write_text(slide['speech'],encoding='utf-8')
        aiff=out/f'{i:02d}.aiff'
        subprocess.run(['say','-v','Linh','-r','200','-f',str(txt),'-o',str(aiff)],check=True)
        duration=float(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration','-of','default=noprint_wrappers=1:nokey=1',str(aiff)]))
        tempo=max(1,duration/29)
        filters=[]
        while tempo>2:filters.append('atempo=2');tempo/=2
        filters.extend([f'atempo={tempo:.6f}','apad'])
        segment=out/f'{i:02d}.mp4'
        subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y','-loop','1','-framerate','12','-i',str(png),'-i',str(aiff),'-t','32','-vf','scale=1280:720,format=yuv420p','-af',','.join(filters),'-c:v','libx264','-preset','veryfast','-crf','22','-r','12','-c:a','aac','-b:a','128k',str(segment)],check=True)
        segments.append(segment)
        print('Video segment',i,'/ 8',flush=True)
    concat=out/'concat.txt';concat.write_text(''.join("file '"+str(p)+"'\n" for p in segments))
    final=ROOT/'docs/Video_demo.mp4'
    subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y','-f','concat','-safe','0','-i',str(concat),'-c','copy','-movflags','+faststart',str(final)],check=True)
    info=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_format','-show_streams','-of','json',str(final)]))
    seconds=float(info['format']['duration'])
    assert 180<=seconds<=300,seconds
    write_json(ROOT/'evidence/video.json',{'file':'docs/Video_demo.mp4','duration_seconds':seconds,'width':1280,'height':720,'narration':'Vietnamese synthetic voice Linh; not a recording of the student','slides':8,'contains_real_application_screenshots':True})
    print('Video created:',seconds,'seconds')

if __name__=='__main__':
    import argparse
    p=argparse.ArgumentParser();p.add_argument('--slides-only',action='store_true');args=p.parse_args()
    s=json.loads((ROOT/'evidence/statistics.json').read_text());spec=slides_spec(s)
    pngs=create_slides(spec)
    if not args.slides_only:create_video(spec,pngs)
