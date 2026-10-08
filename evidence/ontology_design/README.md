# Cách sử dụng bản thiết kế đã kiểm chứng

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
