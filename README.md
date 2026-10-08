# MovieLOD — dữ liệu phim liên kết, bản 2.0 đã hoàn tất

**5/5 yêu cầu đạt theo phạm vi kiểm tra; tự đề xuất 10/10** trên thang chia đều 2 điểm/yêu cầu. Đây không phải điểm chính thức của giảng viên. Bản cục bộ và [website công khai](https://movie-lod-semantic-web.laminhtrung2001.chatgpt.site) đã đồng bộ ontology 2.0: **42 lớp, 30 phim, 851 người, 1.010 đóng góp, 19.339 triple dữ liệu và 1.727 liên kết ngoài**.

## Bộ nộp và tài liệu thuyết trình

| File | Nội dung |
|:--|:--|
| [Slide.pptx](docs/Slide.pptx) / [PDF](docs/Slide.pdf) | 24 trang, font Be Vietnam Pro, ảnh app thật, sơ đồ; 11 khung ảnh Protégé có hướng dẫn ngay trên slide; chữ/sơ đồ và Speaker Notes chỉnh sửa được |
| [Script thuyết trình](docs/Script_thuyet_trinh.pdf) / [Markdown](docs/Script_thuyet_trinh.md) | Lời nói riêng cho 24 slide, khoảng 18–22 phút; chia người nói và câu hỏi bảo vệ |
| [Video demo](docs/Video_demo.mp4) | Bản 2.0 mới, 4 phút 50 giây; ghi tương tác app và kết quả lệnh thật, có giọng tổng hợp tiếng Việt Linh |
| [Kịch bản demo](docs/Kich_ban_video.pdf) / [Markdown](docs/Kich_ban_video.md) | Timeline, lời đọc khớp video, lệnh và kết quả cần thấy; cách tự quay/ghi lại |
| [Checklist ảnh Protégé](docs/Checklist_anh_Protege.pdf) | 11 ảnh, tên file, slide tương ứng, thao tác và nội dung cần thấy |
| [Bảng chấm](CHAM_DIEM.pdf) / [Markdown](CHAM_DIEM.md) | 10/10 tự đề xuất sau sửa; đủ 5 YC, tiêu chí con, minh chứng và giới hạn |
| [Báo cáo](docs/Bao_cao.pdf) / [Markdown](docs/Bao_cao.md) | Đúng 5 yêu cầu, cập nhật 2.0, không quá 15 trang |
| [A–Z](docs/Huong_dan_A_Z.pdf) / [hướng dẫn chi tiết](docs/Huong_dan_thao_tac_chi_tiet.pdf) | Chạy, đọc từ khóa, lệnh, Protégé, Web/endpoint/terminal và xử lý lỗi |
| [Mô tả ontology](docs/Mo_ta_ontology.pdf) / [bảng đầy đủ](docs/Ontology_Redesign.pdf) | Giải thích tiếng Việt: 42 lớp/23 quan hệ/6 datatype property/14 lớp phân loại/24 truy vấn |
| [ZIP tài liệu](docs/Bo_tai_lieu_thuyet_trinh.zip) | Slide, video, báo cáo, scripts và hướng dẫn trong một gói |

**Bản ngắn:** [13 slide](docs/Slide_ngan_13.pptx) và [lời nói riêng](docs/Script_thuyet_trinh_ngan_13.pdf) vẫn được giữ. Video demo 4:50 minh họa app và nhắc bộ ngắn 13 trang; bộ 24 trang phục vụ thuyết trình đầy đủ.

**Ảnh Protégé:** chưa chụp được do macOS chặn điều khiển giao diện. Các khung P00–P10 ghi rõ hướng dẫn; nhóm bổ sung ảnh thật vào PPTX hoặc lưu đúng tên trong evidence/protege rồi tạo lại slide. Khung chờ không được gọi là ảnh minh chứng đã có.

**Chạy HermiT trong Protégé:** mở `ontology/Movie_Knowledge_Graph.owl`. File chính đã sửa timestamp đến mili giây và đồng bộ Turtle/JSON-LD/Web; không còn bản OWL tương thích riêng. HermiT và Pellet đã kiểm tra. Xem `docs/Ket_qua_reasoner.pdf` và `evidence/hermit_run.json`. Video giữ nguyên; minh chứng chỉ thay đổi timestamp ở `evidence/video_dataset_compatibility.json`.

Bộ dự án đầy đủ được đóng thành `../movie_lod_complete.zip`, gồm mã, nguồn gốc, RDF/OWL, sản phẩm và evidence. **Điền tên nhóm/thành viên/lớp trên bìa**, xem lại video và tập nói trước khi nộp. Font trên máy khác cần Be Vietnam Pro hoặc dùng PDF. Video dùng giọng tổng hợp, không phải lời ghi của sinh viên; nhóm có thể đọc lại bằng giọng thành viên.

## Các lỗi đã sửa và minh chứng

- **Nguồn:** bổ sung 43 phản hồi thiếu; hiện **76/76 file có và hash khớp**. Một phản hồi tải lại đổi nội dung được lưu hash/time mới; giữ danh mục trước sửa. Đã chạy collect từ cache, build, reason, validate và test.
- **Public:** triển khai lại site hiện có và giữ audience public. Kiểm tra 8 URL không đăng nhập trả 200; 4 graph RDF kiểm tra (Turtle, JSON-LD, ontology, Inception) đều đẳng cấu local, có giấy phép và mô tả máy đọc được.
- **Video/tài liệu:** thay video cũ bằng demo tương tác bản 2.0 dài 290,05 giây, đồng bộ slide/scripts/báo cáo/hướng dẫn và chấm lại theo minh chứng.
- **Tái lập:** bỏ gitignore loại phản hồi nguồn; thu thập giãn lượt tải và tôn trọng 429 Retry-After; validate báo file thiếu rõ ràng và chạy nhóm truy vấn ở chế độ dữ liệu phù hợp; đóng gói kiểm tra nguồn/video/public trước khi tạo ZIP.

**14 test pass, 9/9 browser checks, 24 file truy vấn đã chạy.** Minh chứng mới: [validation](evidence/validation.json), [tests](evidence/tests.txt), [browser](evidence/browser_checks.json), [public HTTP/graph](evidence/publication_checks.json), [source recovery](evidence/source_recovery.json), [video](evidence/video.json), [bộ nộp](evidence/deliverables.json). `review_before_fix.json`, `self_assessment_before_fix.md` và `review_publication_2026-10-08.json` là lịch sử trước sửa.

## Chạy ứng dụng

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python src/server.py
```

Mở **http://127.0.0.1:8000**, dừng Ctrl+C; macOS có thể dùng start.command. Nếu cổng bận thêm `--port 8001`, đổi URL/curl tương ứng. **Sau build cần khởi động lại server** để endpoint nạp graph mới.

```bash
.venv/bin/python src/query.py queries/02_inception.rq
.venv/bin/python src/query.py queries/18_inferred_filmmakers.rq --reasoned
curl -X POST http://127.0.0.1:8000/sparql \
  -H 'Content-Type: application/sparql-query' \
  --data-binary @queries/02_inception.rq
curl -L -H 'Accept: text/turtle' \
  http://127.0.0.1:8000/resource/film-Q25188
```

Inception: 2010/148 phút/Christopher Nolan; phim Nolan: 8 dòng; đóng góp Inception: 25 dòng với 4 vai trò. Web có 14 mẫu trực tiếp, queries có 24 file. Endpoint chỉ graph khai báo; --reasoned nạp schema và file phân loại đã lưu, không tự tính suy luận lúc truy vấn. Hosted dùng Comunica trong trình duyệt, không phải endpoint Flask public.

## Quy trình và giới hạn

```bash
.venv/bin/python src/collect.py
.venv/bin/python src/build.py
.venv/bin/python src/prepare_web.py
.venv/bin/python src/reason.py
.venv/bin/python src/validate.py
.venv/bin/python -m pytest -q
```

`collect.py --refresh` chủ động tải nguồn mới và có thể đổi dữ liệu; cache đủ/khớp hash không tải lại. Khi thay dữ liệu, cập nhật tài liệu/video, xuất bản lại và chạy check_publication.py. `make all` chạy quy trình từ cache nguồn hiện đã đủ.

Contribution ghi một người, một phim, một vai trò: Director/Actor/Writer/Producer. Dùng dbo:Film/Person/Country là tái sử dụng lớp; owl:sameAs nối cá thể; sourceSnapshot ghi xuất xứ. 12 lớp dùng OWL RL; MultiGenreFilm/FilmStudio dùng SPARQL đếm IRI bổ sung. HermiT/Pellet xác nhận tính nhất quán; hai lớp cardinality vẫn dùng COUNT DISTINCT trong ứng dụng; mẫu 30 phim có chủ đích và một số nhóm genre/award ánh xạ bằng nhãn. Hash kiểm tra toàn vẹn, không bảo đảm mọi phát biểu ngoài đời đúng.

## Tạo lại tài liệu, ảnh và video

Sửa Markdown trong docs/CHAM_DIEM; lời slide ở src/presentation_content.py. PDF cần Pandoc/Tectonic/font Be Vietnam Pro; slide dùng python-pptx/Pillow.

```bash
.venv/bin/python src/make_slides_video.py --slides-only
.venv/bin/python src/make_docs.py
.venv/bin/python src/prepare_web.py
```

make_docs render Markdown hiện có, không ghi đè nội dung. Slide có editable text/diagram; PDF slide hiện là bản vector có chữ tìm kiếm được, xuất từ bố cục PPTX. Kiểm tra browser cần Playwright và Chrome/Chromium; `browser_check.py --port 8000` khi server đang chạy.

Ghi lại demo trên macOS cần Playwright, FFmpeg hệ thống và voice Linh. Terminal A chạy `src/demo_server.py --port 8002`; terminal B:

```bash
.venv/bin/python -m pip install playwright
.venv/bin/python -m playwright install ffmpeg
.venv/bin/python src/record_demo.py --port 8002
```

Các trang xem minh chứng chỉ phục vụ ghi demo cục bộ, không được xuất bản lên sản phẩm. Cảnh kết luận chỉ ghi khi public graph check đã đạt. Kịch bản có hướng dẫn dùng giọng thành viên nếu muốn.

**Đóng gói:** `.venv/bin/python src/package.py` kiểm tra graph, nguồn, video, sản phẩm và public evidence rồi tạo ZIP đầy đủ ở thư mục cha; loại .venv/Git/cache/file dựng video/hosting archive. Dữ liệu CC BY-SA 4.0, mã MIT; giữ giấy phép thư viện.

Tham khảo [Linked Data](https://www.w3.org/DesignIssues/LinkedData.html), [SPARQL](https://www.w3.org/TR/sparql11-query/), [OWL 2 Profiles](https://www.w3.org/TR/owl2-profiles/).
