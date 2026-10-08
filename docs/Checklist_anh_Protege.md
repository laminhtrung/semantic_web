---
title: "MovieLOD: checklist ảnh minh chứng Protégé"
date: "11 vị trí trong bộ 24 slide · 08/10/2026"
---

## Cách chèn

Có 11 khung ảnh ghi rõ mã, tên file và thao tác ngay trên slide. Lần tạo này không có ảnh Protégé thật: macOS chặn quyền điều khiển giao diện; không thay bằng ảnh dựng. Ảnh ứng dụng Web trong slide là ảnh chụp thực.

Cách 1: chèn ảnh vào PowerPoint và che/xóa khung chờ cùng phần hướng dẫn của khung đó. Cách 2: lưu đúng tên ở `evidence/protege/` (PNG/JPG/JPEG cùng stem), chạy `.venv/bin/python src/make_slides_video.py --slides-only`; khung chờ tự thay bằng ảnh. Speaker Notes giữ quy trình chụp.

Chụp đúng cửa sổ/view, chữ đủ lớn (gợi ý 1440×900 trở lên); không lấy cả desktop có ứng dụng khác. Giữ tên ontology và IRI/thông tin cần chứng minh. Ảnh cây khai báo không được ghi nhãn inferred.

## Danh sách ảnh

### P00 — Slide 05: Ontology IRI và phiên bản

**Tên file:** `P00_ontology_header.png`. **Mở:** `ontology/Movie_Ontology.owl`.

1. Mở ontology/Movie_Ontology.owl.
2. Chọn Active Ontology / Ontology Header.
3. Giữ IRI ontology và versionInfo 2.0.0 trong khung hình.

**Mục cần thấy:** IRI đúng namespace của bài; phiên bản 2.0.0. Metrics có thể tính cả lớp ngoài được tham chiếu, khác 42 lớp tự khai báo.

### P01 — Slide 06: Cây lớp phim

**Tên file:** `P01_film_hierarchy.png`. **Mở:** `ontology/Movie_Ontology.owl`.

1. Entities → Classes → mở CreativeWork và Film.
2. Hiện các lớp con FeatureFilm, AnimatedFilm và nhóm phim.
3. Chọn Film; giữ IRI DBpedia và Class Description.

**Mục cần thấy:** Film thuộc CreativeWork; IRI là http://dbpedia.org/ontology/Film. Chụp cây khai báo, không gọi là cây đã suy luận.

### P02 — Slide 07: Cây người và tổ chức

**Tên file:** `P02_agent_hierarchy.png`. **Mở:** `ontology/Movie_Ontology.owl`.

1. Entities → Classes → mở Agent.
2. Mở Person và Organization → ProductionCompany.
3. Chọn Person hoặc Filmmaker; giữ cây lớp và Description.

**Mục cần thấy:** Person và Organization cùng dưới Agent; Actor/Filmmaker/AwardWinner là lớp con Person.

### P03 — Slide 08: Cây Genre và Award

**Tên file:** `P03_genre_award_hierarchy.png`. **Mở:** `ontology/Movie_Ontology.owl`.

1. Thu gọn Film/Agent để ảnh dễ đọc.
2. Mở Genre → FictionGenre / NonFictionGenre và Award.
3. Hiện các lớp thể loại và nhóm giải; giữ Class Description.

**Mục cần thấy:** Cây Genre/Award khớp sơ đồ. Nhóm thể loại/giải được ánh xạ theo nhãn trong bước build.

### P04 — Slide 09: Ràng buộc của Contribution

**Tên file:** `P04_contribution_restrictions.png`. **Mở:** `ontology/Movie_Ontology.owl`.

1. Entities → Classes → chọn Contribution.
2. Trong Class Description, mở đủ SubClass Of.
3. Hiện contributionBy / contributionTo / hasRole: exactly 1.

**Mục cần thấy:** Ba qualified cardinality đúng 1, cùng các allValuesFrom. Đây là mô hình OWL, không phải biên bản kiểm tra thiếu trường.

### P05 — Slide 10: Domain, range, inverse, functional

**Tên file:** `P05_object_property.png`. **Mở:** `ontology/Movie_Ontology.owl`.

1. Entities → Object properties → chọn contributionBy.
2. Hiện Domain=Contribution, Range=Person.
3. Giữ inverse hasContribution và ô Functional được chọn.

**Mục cần thấy:** Đúng domain/range/inverse/functional của contributionBy. Nếu cần, chụp bổ sung hasRole hoặc director.

### P06 — Slide 13: Định nghĩa Filmmaker

**Tên file:** `P06_filmmaker_equivalent_class.png`. **Mở:** `ontology/Movie_Ontology.owl`.

1. Entities → Classes → chọn Filmmaker.
2. Mở Class Description → Equivalent To.
3. Hiện Person AND các nhánh SOME Directing/Writing/ProducingContribution.

**Mục cần thấy:** Định nghĩa giao/hợp/tồn tại. Ảnh định nghĩa không tự chứng minh HermiT đã phân loại dữ liệu.

### P07 — Slide 14: Định nghĩa FilmStudio

**Tên file:** `P07_filmstudio_cardinality.png`. **Mở:** `ontology/Movie_Ontology.owl`.

1. Entities → Classes → chọn FilmStudio.
2. Mở Equivalent To; hiện min 3 productionOf Film.
3. Có thể chụp thêm MultiGenreFilm: min 2 hasGenre Genre.

**Mục cần thấy:** Ảnh công thức cardinality. Kết quả 6 studio/30 phim nhiều thể loại của app dùng COUNT DISTINCT, không tự coi là chứng minh OWL DL.

### P08 — Slide 16: Datatype của thời lượng

**Tên file:** `P08_runtime_datatype.png`. **Mở:** `ontology/Movie_Ontology.owl`.

1. Entities → Data properties → chọn runtimeMinutes.
2. Hiện Domain=Film và Range=xsd:decimal.
3. Có thể chụp thêm releaseYear có range xsd:integer.

**Mục cần thấy:** Thuộc tính dữ liệu nối thực thể với literal, khác quan hệ nối hai thực thể.

### P09 — Slide 18: Cá thể Inception

**Tên file:** `P09_inception_individual.png`. **Mở:** `ontology/Movie_Knowledge_Graph.owl`.

1. Mở ontology/Movie_Knowledge_Graph.owl.
2. Individuals → chọn film-Q25188 (Inception).
3. Hiện Film, title, releaseYear=2010, runtimeMinutes=148 và director.

**Mục cần thấy:** Cá thể thật và thuộc tính khớp truy vấn. Giữ tên ontology để không chụp nhầm file chỉ có schema.

### P10 — Slide 21: Kiểu khai báo của Nolan

**Tên file:** `P10_nolan_asserted_types.png`. **Mở:** `ontology/Movie_Knowledge_Graph.owl`.

1. Mở Movie_Knowledge_Graph.owl, chọn person-Q25191 (Nolan).
2. Hiện Types trong chế độ asserted / trước suy luận.
3. Giữ dbo:Person và các quan hệ đóng góp/giải trong ảnh.

**Mục cần thấy:** Kiểu gán gốc là Person; Filmmaker/AwardWinner trong app được bổ sung qua file phân loại. Nếu chụp sau reasoner, phải ghi rõ tên và trạng thái thực thi.

## Kiểm tra trước khi dùng làm minh chứng

- Đúng ontology 2.0 của bài, không phải file mở rộng cũ.
- Ảnh cá thể dùng Knowledge Graph; ảnh mô hình dùng schema OWL.
- IRI lớp DBpedia, cardinality và datatype đọc được.
- Không nói HermiT/Pellet đã chứng minh DL nếu chỉ chụp công thức hoặc chọn menu.
- Nếu chạy reasoner, giữ tên và trạng thái; ghi cả lỗi nếu có.

Nguồn hướng dẫn giao diện: [Protégé Views](https://protegeproject.github.io/protege/views/). Ngữ nghĩa cần nhớ: [OWL 2 Primer](https://www.w3.org/TR/owl2-primer/). Nội dung lớp/thuộc tính/cá thể lấy từ OWL của bài.