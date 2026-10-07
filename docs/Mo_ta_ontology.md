# Mô tả ontology MovieLOD và cách giải thích khi bảo vệ

Ontology phiên bản **2.0.0** có **42 lớp có tên**: phần lớn là lớp tường minh (gán trực tiếp từ dữ liệu Wikidata), 14 lớp được **suy luận** (chỉ tồn tại nhờ `owl:equivalentClass`, không bao giờ gán sẵn). Bảng chi tiết đầy đủ (class hierarchy, property, inferred class, inference chain, 24 câu SPARQL, so sánh Semantic Web vs truyền thống) nằm ở [`docs/Ontology_Redesign.md`](Ontology_Redesign.md) — tài liệu này chỉ tóm tắt phần cần nhớ khi bảo vệ. Nguồn sinh ontology là `src/build.py`; không sửa riêng file OWL vì build sẽ ghi lại.

## Vì sao đổi từ v1.1.0 sang v2.0.0

Bản trước có 3 lớp "tổ hợp" không đẹp về mặt mô hình: `CreditedFilm` ("phim có credit"), `DirectorWriter` ("vừa đạo diễn vừa biên kịch"), `FilmContributor`. Bản mới thay bằng một cây phân cấp đúng nghĩa (`CreativeWork`, `Agent`, `Contribution`, `Genre`, `Award`, `Organization`) và **mô hình Contribution**: `Person --hasContribution--> Contribution --contributionTo--> Film`, `Contribution --hasRole--> ContributionRole`. Nhờ vậy một người có thể giữ bao nhiêu vai trò tùy ý mà không cần lớp tổ hợp nào cả — câu hỏi "ai vừa đạo diễn vừa biên kịch" giờ chỉ là 1 câu SPARQL join 2 dòng (`queries/23_people_with_directing_and_writing_contribution.rq`), không phải một lớp hard-code.

Để `Award` và `ProductionCompany` có dữ liệu thật thay vì để trống, `src/collect.py` được bổ sung lấy thêm `wdt:P166` (award received, trên cả phim lẫn người), `wdt:P272` (production company) và `wdt:P162` (producer). Không có cá thể nào trong tài liệu này là dữ liệu bịa — mọi thứ đều truy được về một claim Wikidata lưu trong `data/raw/`.

## Các nhánh lớp chính (xem Bảng 1 trong Ontology_Redesign.md để có đủ 42 lớp)

| Nhánh | Lớp tiêu biểu | Ý nghĩa |
|:--|:--|:--|
| `ex:CreativeWork` | `dbo:Film`, `ex:FeatureFilm`, `ex:AnimatedFilm`, `ex:ActionFilm`(*)... | Tác phẩm điện ảnh và các lớp con theo thể loại |
| `ex:Agent` | `dbo:Person`, `ex:Organization`, `ex:ProductionCompany`, `ex:Actor`(*), `ex:Filmmaker`(*) | Người hoặc tổ chức có thể đóng góp vào phim |
| `ex:Contribution` | `ex:ActingContribution`(*), `ex:DirectingContribution`(*)... | Bản ghi nối đúng 1 người — 1 phim — 1 vai trò |
| `ex:Genre` | `ex:FictionGenre`, `ex:ActionGenre`, `ex:NonFictionGenre`... | Thể loại phim, phân theo nhãn Wikidata thật |
| `ex:Award` | `ex:FilmAward`, `ex:ActingAward`, `ex:DirectingAward`, `ex:WritingAward` | Giải thưởng (`wdt:P166`), phân loại theo nhãn thật |

(*) = lớp **suy luận**, không gán trực tiếp.

## 14 lớp suy luận và công thức (xem Bảng 4 trong Ontology_Redesign.md để có số liệu đầy đủ)

`≡` là tương đương; `⊓` là giao; `⊔` là hợp; `∃p.C` là tồn tại ít nhất một đối tượng thuộc C qua thuộc tính p; `≥n p.C` là có ít nhất n đối tượng thuộc C qua p.

| Lớp | Công thức | Số cá thể thật |
|:--|:--|--:|
| `ex:Actor` | `dbo:Person ⊓ ∃ex:hasContribution.ex:ActingContribution` | 769 |
| `ex:Filmmaker` | `dbo:Person ⊓ (∃hasContribution.DirectingContribution ⊔ WritingContribution ⊔ ProducingContribution)` | 89 |
| `ex:AwardWinner` | `dbo:Person ⊓ ∃ex:hasAward.ex:Award` | 290 |
| `ex:ActionFilm` | `dbo:Film ⊓ ∃ex:hasGenre.ex:ActionGenre` | 12 |
| `ex:MultiGenreFilm` | `dbo:Film ⊓ ≥2 ex:hasGenre.ex:Genre` | 30 (xem giới hạn bên dưới) |
| `ex:AwardWinningFilm` | `dbo:Film ⊓ ∃ex:hasAward.ex:Award` | 26 |
| `ex:FilmStudio` | `ex:ProductionCompany ⊓ ≥3 ex:productionOf.dbo:Film` | 6 |
| (+ 4 lớp `*Contribution`, `ComedyFilm`, `DramaFilm`, `ScienceFictionFilm`) | — | xem Ontology_Redesign.md |

Cả 14 lớp có **0 cá thể được gán kiểu sẵn** trong dataset (kiểm chứng bằng `tests/test_ontology.py::test_defined_classes_are_inferred_not_asserted`); mọi số trong bảng trên đều là kết quả suy luận thật, lấy từ `evidence/ontology_reasoning.json`.

## Ví dụ suy luận với dữ liệu thật — Christopher Nolan

Dữ liệu khai báo Inception (`film-Q25188`) có `dbo:director`/`dbo:writer` trỏ tới Nolan (`person-Q25191`), và một `ex:Contribution` ghi `ex:hasRole ex:DirectorRole` nối Nolan với Inception. Nolan chỉ được khai báo `dbo:Person` — **không có triple nào gán Nolan là Filmmaker**.

1. `contribution rdf:type ex:Contribution`, `ex:hasRole ex:DirectorRole` (dữ kiện gốc).
2. `owl:hasValue` ⟹ `contribution rdf:type ex:DirectingContribution` (bước suy luận 1).
3. `owl:someValuesFrom` + `owl:unionOf` ⟹ `nolan rdf:type ex:Filmmaker` (bước suy luận 2).

Kiểm tra trực tiếp: `python src/query.py queries/24_nolan_asserted_types_only.rq` (không `--reasoned`) chỉ trả về `dbo:Person`; còn `python src/query.py queries/18_inferred_filmmakers.rq --reasoned` có Nolan trong danh sách. Đây là minh chứng rõ nhất cho khác biệt Semantic Web vs truy vấn CSDL truyền thống — xem mục 11 trong Ontology_Redesign.md.

## Các câu hỏi dễ gặp

**Vì sao không khai báo Actor và Filmmaker disjoint?** Vì một người có thể làm cả hai (ví dụ: Quentin Tarantino, Peter Jackson — xem `queries/23_...rq`, 10 người trong dữ liệu vừa có DirectingContribution vừa có WritingContribution). Khai báo rời nhau sẽ gây mâu thuẫn ngay với dữ liệu thật.

**Vì sao `MultiGenreFilm` ra đúng 30/30 phim?** Vì bộ 30 phim thu thập đều là phim nổi tiếng, Wikidata luôn gắn ≥2 thể loại phụ cho mỗi phim (nhỏ nhất là 2, lớn nhất 18). Công thức vẫn đúng; mẫu dữ liệu này đơn giản không có phim chỉ 1 thể loại để tạo đối chứng. Xem mục 9 (giới hạn) trong Ontology_Redesign.md.

**Vì sao owlrl không tự suy ra được `MultiGenreFilm`/`FilmStudio`?** Vì chuẩn OWL 2 RL (mà thư viện `owlrl` cài đặt) chỉ có luật cho cardinality 0 hoặc 1, không có luật cho `minQualifiedCardinality ≥ 2`. Đây là suy luận OWL DL hợp lệ (Protégé + HermiT/Pellet suy ra được), nhưng `owlrl` bỏ qua một cách im lặng. `src/reason.py` tính bù phần này bằng một truy vấn SPARQL aggregate tương đương, có ghi chú rõ trong code.

**Cardinality có buộc dữ liệu lưu đủ trường không?** OWL phát biểu ngữ nghĩa, không kiểm tra biểu mẫu như cơ sở dữ liệu. `src/validate.py` kiểm tra riêng các trường bắt buộc trong dữ liệu ứng dụng (mỗi `ex:Contribution` phải có đúng 1 `contributionBy`/`contributionTo`/`hasRole`).

## Tái lập và kiểm tra

```bash
.venv/bin/python src/collect.py   # crawl (đã thêm P162/P166/P272)
.venv/bin/python src/build.py
.venv/bin/python src/validate.py
.venv/bin/python src/reason.py
.venv/bin/python -m pytest -q     # 13 test, ~2 phút (có chạy owlrl)
```

`evidence/ontology_reasoning.json` lưu số cá thể khai báo/suy ra của 14 lớp, các lớp suy ra cho Nolan và lỗi owlrl phát hiện (hiện tại: 0 lỗi, đồ thị nhất quán). `data/processed/inferred_classes.ttl` là kết quả phân loại riêng. Endpoint `/sparql` và giao diện web chỉ truy vấn dữ liệu khai báo (`movies.ttl`), không tự chạy suy luận — muốn dùng 14 lớp suy luận trong truy vấn, chạy `python src/query.py <file> --reasoned` (nạp thêm schema + `inferred_classes.ttl`).

Mở `ontology/Movie_Knowledge_Graph.owl` bằng Protégé, chọn HermiT và Start reasoner để thấy toàn bộ 14 lớp suy luận populate trực tiếp, **bao gồm cả `MultiGenreFilm`/`FilmStudio`** mà owlrl không suy ra được (một DL reasoner đầy đủ xử lý được cardinality ≥2).

Nguồn ngữ nghĩa: [W3C OWL 2 Primer, mục 4.3, 5.1 và 5.2](https://www.w3.org/TR/owl2-primer/); [OWL 2 RL Profile](https://www.w3.org/TR/owl2-profiles/#OWL_2_RL) cho giới hạn cardinality.
