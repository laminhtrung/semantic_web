---
title: "MovieLOD: hướng dẫn đọc và chạy từ A đến Z"
date: "MovieLOD 2.0 · Đối chiếu ngày 08/10/2026"
---

## Đọc theo thứ tự nào?

1. Đọc tài liệu này để biết chạy ứng dụng và hiểu từ khóa.
2. Mở `Slide.pptx` cùng `Script_thuyet_trinh.pdf` để tập nói.
3. Đọc `Kich_ban_video.pdf` để quay demo 3–5 phút.
4. Đọc `Bao_cao.pdf` và `CHAM_DIEM.pdf` để đối chiếu yêu cầu.
5. Tra `Huong_dan_thao_tac_chi_tiet.pdf` khi cần lệnh và xử lý lỗi; `Ontology_Redesign.pdf` khi cần đầy đủ lớp/thuộc tính.

## Chạy ứng dụng từ dữ liệu đã có

Trong terminal ở thư mục dự án:

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python src/server.py
```

Mở `http://127.0.0.1:8000`. Nếu cổng đang bị dùng, chạy server với `--port 8001`, mở URL cổng 8001 và thay cổng trong curl. Sau khi build dữ liệu mới, dừng và chạy lại server để endpoint nạp graph mới. Không dừng tiến trình của người khác chỉ để lấy lại cổng.

Chọn Sample queries: Inception; kết quả **2010, 148, Christopher Nolan**. Chọn Films directed by Christopher Nolan: **8 dòng**. Chọn Who contributed to Inception: **25 dòng** gồm các vai trò Director, Actor, Writer, Producer. Tìm Inception ở Find a film, mở trang phim để xem nguồn và RDF.

## Từ khóa cần hiểu

| Từ | Nghĩa dễ nhớ |
|:--|:--|
| Ontology | Bản mô tả các khái niệm, quan hệ và quy tắc |
| Class / individual | Loại đối tượng / một đối tượng cụ thể; Film / Inception |
| RDF triple | Một câu dữ liệu: chủ thể, quan hệ, đối tượng hoặc giá trị |
| IRI / URI | Định danh để phân biệt thực thể; HTTP IRI còn có thể tra cứu |
| SPARQL | Ngôn ngữ đặt câu hỏi trên đồ thị RDF |
| SELECT / ASK / CONSTRUCT | Lấy bảng / hỏi đúng-sai / tạo đồ thị |
| owl:sameAs | Hai định danh cùng chỉ một thực thể |
| SourceSnapshot | Bản ghi URL, thời điểm, hash của phản hồi nguồn |
| OWL RL | Bộ luật suy luận mà thư viện owlrl đang dùng |
| --reasoned | Nạp thêm schema và kết quả phân loại đã lưu |

## Phân biệt ba việc dễ nhầm

Dùng `dbo:Film` là tái sử dụng lớp DBpedia. Nối Inception với Wikidata bằng sameAs là nối **cá thể**. Ghi nguồn bằng sourceSnapshot là giữ **xuất xứ**. Ba việc này giải quyết ba câu hỏi khác nhau.

Một người có thể giữ nhiều vai trò. Contribution là bản ghi **một người + một phim + một vai trò**. Các vai trò khác nhau có bản ghi riêng. Không dùng mô hình Credit/participant/hasCredit của bản cũ.

Endpoint truy vấn dữ liệu khai báo. Muốn hỏi các lớp Actor/Filmmaker được suy ra, dùng terminal với --reasoned. File inferred_classes.ttl đã có; chạy reason.py khi cần tính lại sau sửa dữ liệu. Một SELECT trực tiếp trả 0 không có nghĩa ontology không có định nghĩa.

## Số liệu và kết quả hoàn tất

Bản local: **42 lớp, 30 phim, 851 người, 1.010 đóng góp, 19.339 triple, 1.727 liên kết ngoài**. Bản 2.0 đã được xuất bản công khai và kiểm tra không đăng nhập: dữ liệu Turtle/JSON-LD, ontology và mô tả RDF của Inception đều đẳng cấu với graph cục bộ. Có 19.339 triple dữ liệu và 42 lớp ontology.

Đã bổ sung 43 phản hồi còn thiếu và chạy lại quy trình: đủ 76/76 file nguồn, 76/76 SHA-256 khớp, không có file thiếu. Một phản hồi tải lại có nội dung thay đổi được ghi thời điểm/hash mới; danh mục lịch sử được giữ ở `evidence/source_manifest_before_recovery.json`.

Theo thang chia đều 2 điểm/yêu cầu, hiện **10/10**: cả 5 yêu cầu đạt trong phạm vi đề và kiểm tra hiện tại. Đây là tự đánh giá, không phải điểm chính thức. `Video_demo.mp4` đã được thay bằng demo thao tác bản 2.0, có lời tiếng Việt tổng hợp; nhóm có thể tự đọc lại theo kịch bản. Đọc `CHAM_DIEM.md` để biết minh chứng và cách hoàn tất.

## Slide đầy đủ và ảnh Protégé

Slide.pptx/pdf hiện có **24 trang**, Script_thuyet_trinh.md/pdf khớp từng trang. Bản ngắn 13 trang vẫn ở Slide_ngan_13.pptx/pdf cùng lời nói riêng. Có **11 khung ảnh Protégé** ghi ngay trên slide; xem Checklist_anh_Protege.pdf để bổ sung. Lần này chưa có ảnh Protégé thật, không dùng khung chờ làm minh chứng đã chụp.

**Cập nhật timestamp/reasoner:** dùng duy nhất Movie_Knowledge_Graph.owl cho graph đầy đủ. HermiT/Pellet đã chạy; xem Ket_qua_reasoner.pdf. Video_demo.mp4 giữ nguyên theo yêu cầu nhóm; timestamp trong dữ liệu mới giảm đến mili giây, nội dung phim/quan hệ giữ nguyên, đã kiểm tra ở video_dataset_compatibility.json. Video chưa thể hiện kết quả reasoner mới và vẫn nhắc bộ slide ngắn 13 trang.
