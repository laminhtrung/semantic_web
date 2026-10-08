---
title: "MovieLOD: mô tả ontology và câu hỏi bảo vệ"
date: "MovieLOD 2.0 · Đối chiếu 08/10/2026"
---

## Những ý cần nhớ

Ontology 2.0 có **42 lớp**: 3 lớp DBpedia dùng trực tiếp (Film/Person/Country), 39 lớp namespace ex:, trong đó 14 lớp có kiểu được bổ sung từ định nghĩa/quy tắc. Có 23 object property và 6 datatype property. Bảng toàn bộ nằm ở [Ontology_Redesign.md](Ontology_Redesign.md).

Contribution nối đúng một **người, phim và vai trò**. Các quan hệ là contributionBy, contributionTo và hasRole. Bốn vai trò: Director, Actor, Writer, Producer. Đường đi ngược: hasContribution từ người và contributionOf từ phim. Dữ liệu hiện có 1.010 Contribution. Mỗi vai trò trong từng phim có bản ghi riêng; một người không bị ép chỉ một nghề.

## Ví dụ nói trong buổi bảo vệ

Dữ liệu Inception ghi Nolan là Person, có đóng góp với DirectorRole. Từ hasValue suy ra DirectingContribution; Person có loại đóng góp này được phân loại Filmmaker. Nolan còn có giải riêng nên được phân loại AwardWinner. Các kiểu bổ sung lưu tách ở inferred_classes.ttl.

```bash
.venv/bin/python src/query.py queries/24_nolan_asserted_types_only.rq
.venv/bin/python src/query.py queries/24_nolan_asserted_types_only.rq --reasoned
```

Không --reasoned: 1 kiểu Person. Có --reasoned: 3 kiểu Person, Filmmaker, AwardWinner. Lệnh chỉ nạp file phân loại đã lưu; cần `src/reason.py` để tính lại sau khi sửa dữ liệu.

## 14 lớp được xử lý như thế nào?

| Nhóm | Lớp | Cách xử lý |
|:--|:--|:--|
| Đóng góp | Acting/Directing/Writing/ProducingContribution | OWL RL, hasValue |
| Người | Actor, Filmmaker, AwardWinner | OWL RL, tồn tại/giao/hợp |
| Phim | Action/Comedy/Drama/ScienceFiction/AwardWinningFilm | OWL RL, thể loại hoặc giải |
| Đếm theo ngưỡng | MultiGenreFilm, FilmStudio | SPARQL COUNT DISTINCT bổ sung |

Có 769 Actor, 89 Filmmaker, 12 ActionFilm, 26 AwardWinningFilm, 30 MultiGenreFilm, 6 FilmStudio trong kết quả phân loại hiện tại. Phạm vi đếm là IRI tài nguyên nội bộ; hai truy vấn người chỉ hiển thị 20 dòng do LIMIT.

## Các câu hỏi dễ nhầm

**Cardinality có bắt buộc file phải điền đủ không?** Không như kiểm tra form/CSDL. OWL dùng thế giới mở; Python kiểm tra trường bắt buộc riêng.

**Hai IRI khác nhau có chắc là hai cá thể khác nhau không?** Không trong OWL. COUNT DISTINCT là đếm tên trong ứng dụng; cần căn cứ phân biệt cá thể khi chứng minh cardinality DL.

**owlrl đã chứng minh ontology nhất quán chưa?** Chỉ chạy bộ luật và kiểm tra lỗi được phát hiện trong phạm vi đó; chưa phải chứng minh OWL DL đầy đủ. HermiT và Pellet đã chạy riêng trên file OWL chính và xác nhận nhất quán; xem Ket_qua_reasoner.pdf.

**Actor/Filmmaker có rời nhau không?** Không. Một người có thể diễn xuất và đạo diễn; vai trò chồng lấp được mô hình hóa bằng các Contribution riêng.

**sameAs có phải nguồn không?** sameAs là cùng danh tính; sourceSnapshot là xuất xứ. dbo:Film là tái dùng từ vựng lớp.

**Vì sao endpoint không có Filmmaker?** Endpoint mặc định chỉ nạp movies.ttl; dùng --reasoned ở terminal để nạp schema và file phân loại.

**DocumentaryFilm bằng 0 có phải lỗi?** Không nhất thiết: danh sách 30 phim hiện không có phim tài liệu. ASK false không nói rằng thế giới không có phim tài liệu.

**Mẫu có đủ nguồn để tái lập chưa?** Có đủ 76/76 file và hash khớp. Đã chạy lại thu thập từ cache nguồn, build, validate, reason và 14 test. Giữ cả biên bản nguồn lịch sử và nguồn tải lại.

**Website đã có 42 lớp chưa?** Có. Bản public đã được triển khai lại, ontology 42 lớp và dữ liệu 19.339 triple đều đẳng cấu với local; kiểm tra không đăng nhập ở publication_checks.json.

## Xem trong Protégé

Mở Movie_Ontology.owl để xem mô hình; mở Movie_Knowledge_Graph.owl để xem cả dữ liệu. Xem lớp, IRI, restriction; xem inverse và functional ở Object properties. HermiT và Pellet đã xác nhận nhất quán, không có lớp không khả thỏa. File OWL chính và các bản RDF đều xuất timestamp đến mili giây để tránh lỗi HermiT. Có 769 Actor, 89 Filmmaker và 290 AwardWinner; MultiGenreFilm/FilmStudio không có cá thể suy luận DL, khác số đếm ứng dụng 30/6.
