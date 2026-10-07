# Mô tả ontology MovieLOD và cách giải thích khi bảo vệ

Ontology phiên bản 1.1.0 có **15 lớp có tên**: 9 lớp nền và 6 lớp được định nghĩa để suy luận. Các node vô danh biểu diễn giao/hợp là biểu thức lớp, không tính thành lớp nghiệp vụ mới. Nguồn sinh ontology là `src/build.py`; không sửa riêng file OWL vì build sẽ ghi lại.

## Đánh giá các góp ý

1. **Disjointness:** bản trước đã có `owl:AllDisjointClasses` cho 9 lớp nền, bao gồm Film và Country. Khai báo này đã nói mọi cặp trong danh sách rời nhau. Bản mới bổ sung 36 cặp `owl:disjointWith` tương đương để dễ xem bằng công cụ. Chỉ áp dụng cho lớp nền; Director, Actor và Screenwriter có thể chồng lấp.
2. **Defined class:** hợp lý, đã bổ sung `equivalentClass` với `intersectionOf` và `someValuesFrom`, tận dụng trực tiếp `dbo:Person`, `dbo:Film` cùng dữ liệu hiện có.
3. **Alias phẳng:** không có `ex:Film ≡ dbo:Film`; mô hình dùng trực tiếp `dbo:Film`, `dbo:Person`, `dbo:Country`. Giữ alignment Genre, Language và Dataset để tương thích dữ liệu hiện tại, nhưng phần phân loại nghiệp vụ được định nghĩa bằng điều kiện, không chỉ bằng alias.
4. **Union/intersection:** đã thêm cả hai. Union không yêu cầu các lớp thành viên rời nhau.
5. **Description:** mỗi lớp có `rdfs:comment` tiếng Anh trong RDF; tài liệu này giải thích tiếng Việt, công thức, ví dụ và giới hạn.

## Chín lớp nền

| Lớp | Ý nghĩa và quan hệ chính |
|:--|:--|
| `dbo:Film` | Tác phẩm phim; có người tham gia, thể loại, quốc gia, ngôn ngữ, thời lượng và nguồn. |
| `dbo:Person` | Con người; một người có thể đồng thời đạo diễn, diễn xuất và viết kịch bản. |
| `ex:Genre` | Thể loại của phim, nối qua `ex:hasGenre`; tương đương `dbo:Genre`. |
| `dbo:Country` | Quốc gia sản xuất, nối từ phim qua `ex:country`. |
| `ex:Language` | Ngôn ngữ của phim, nối qua `ex:language`; tương đương `dbo:Language`. |
| `ex:Credit` | Bản ghi đóng góp, nối đúng một phim (`inFilm`), một người (`participant`) và một vai trò (`role`). |
| `ex:ContributionRole` | Loại công việc; DirectorRole, ActorRole, WriterRole là ba cá thể khác nhau, không phải ba người. |
| `ex:SourceSnapshot` | Phản hồi nguồn được lưu với URL, thời điểm thu thập và SHA-256. |
| `ex:Dataset` | Bộ dữ liệu công bố; tương đương `void:Dataset`. |

Các lớp nền rời nhau theo lựa chọn mô hình của bài. Đây là ràng buộc cục bộ sử dụng các IRI DBpedia, không phải tuyên bố đã nhập toàn bộ ontology DBpedia. Không có `owl:imports`; các kiểm tra ở đây không bao gồm dữ liệu bên ngoài được tải qua `sameAs`.

## Sáu lớp được định nghĩa

`≡` là tương đương (điều kiện cần và đủ); `⊓` là giao (đồng thời thỏa); `⊔` là hợp (ít nhất một); `∃p.C` hay `p some C` là tồn tại ít nhất một đối tượng thuộc C được nối qua p.

| Lớp | Công thức | Giải thích bằng lời |
|:--|:--|:--|
| `ex:Director` | `dbo:Person ⊓ ∃ex:directed.dbo:Film` | Người đã đạo diễn ít nhất một phim trong mô hình. |
| `ex:Actor` | `dbo:Person ⊓ ∃ex:actedIn.dbo:Film` | Người đã diễn xuất trong ít nhất một phim trong mô hình. |
| `ex:Screenwriter` | `dbo:Person ⊓ ∃ex:wrote.dbo:Film` | Người có đóng góp viết kịch bản trong ít nhất một phim; bám theo quan hệ writer đã thu thập. |
| `ex:FilmContributor` | `ex:Director ⊔ ex:Actor ⊔ ex:Screenwriter` | Người có ít nhất một trong ba vai trò đang xét, có thể có nhiều vai trò. |
| `ex:DirectorWriter` | `ex:Director ⊓ ex:Screenwriter` | Người vừa từng đạo diễn vừa từng viết kịch bản; hai phim có thể khác nhau. |
| `ex:CreditedFilm` | `dbo:Film ⊓ ∃ex:hasCredit.ex:Credit` | Phim có ít nhất một bản ghi đóng góp; không có nghĩa danh sách credit đã đầy đủ. |

FilmContributor chỉ bao quát ba vai trò trong bài. Nó không đại diện cho tất cả nghề điện ảnh ngoài thực tế.

Ví dụ dạng Turtle cho Director:

```turtle
ex:Director a owl:Class ;
    rdfs:subClassOf dbo:Person ;
    owl:equivalentClass [ a owl:Class ;
        owl:intersectionOf (
            dbo:Person
            [ a owl:Restriction ;
              owl:onProperty ex:directed ;
              owl:someValuesFrom dbo:Film ]
        ) ] .
```

`rdfs:subClassOf` làm rõ cây lớp; `owl:equivalentClass` mới cho phép từ điều kiện đầy đủ suy ra membership. Chỉ gắn restriction bằng `subClassOf` lên Director thì chưa đủ để phân loại người thành Director từ quan hệ directed.

## Ví dụ suy luận với dữ liệu thật

Dữ liệu khai báo Inception (`film-Q25188`) là `dbo:Film`, có `dbo:director` và `dbo:writer` trỏ tới Christopher Nolan (`person-Q25191`). Nolan được khai báo `dbo:Person`; không gán sẵn sáu kiểu mới.

1. `dbo:director inverseOf ex:directed` suy ra Nolan `directed` Inception.
2. Nolan là Person và đã directed một Film ⇒ Nolan thuộc Director.
3. `dbo:writer inverseOf ex:wrote` cùng dữ liệu phim ⇒ Nolan thuộc Screenwriter.
4. Nolan thuộc Director và Screenwriter ⇒ thuộc DirectorWriter.
5. Nolan thuộc ít nhất một lớp thành viên ⇒ thuộc FilmContributor.
6. Inception có `hasCredit` nối tới một Credit ⇒ thuộc CreditedFilm.

Kết quả thực tế (chỉ đếm IRI nội bộ, loại alias qua `sameAs`):

| Lớp suy ra | Số cá thể |
|:--|--:|
| Director | 16 |
| Actor | 769 |
| Screenwriter | 34 |
| FilmContributor | 805 |
| DirectorWriter | 10 |
| CreditedFilm | 30 |

Cả sáu lớp có 0 cá thể được gán kiểu sẵn trong dataset; số trên là kết quả suy luận.

## Các câu hỏi dễ gặp

**Vì sao không khai báo Director và Screenwriter disjoint?** Vì một người có thể làm cả hai. Khai báo rời nhau sẽ làm ví dụ Nolan mâu thuẫn.

**Director khác DirectorRole thế nào?** Director là lớp của người. DirectorRole là một cá thể mô tả loại công việc trong bản ghi Credit.

**DirectorWriter có nghĩa đạo diễn và biên kịch cùng một phim không?** Không. Công thức giao hiện tại chỉ yêu cầu người đó có hai vai trò, có thể ở hai phim khác nhau. Nếu muốn cùng phim, truy vấn cùng biến phim qua director và writer, hoặc bổ sung cơ chế suy luận phù hợp.

**Vì sao chưa thêm Cinematographer?** Đây là ví dụ hợp lý nhưng dữ liệu chưa thu thập đóng góp quay phim. Nếu thêm, phải dùng quan hệ người → phim, chẳng hạn `ex:shotFilm inverseOf dbo:cinematography`, rồi định nghĩa `Cinematographer ≡ dbo:Person ⊓ ∃ex:shotFilm.dbo:Film`. Không dùng trực tiếp một thuộc tính phim → người làm điều kiện trên người.

**Không thấy Actor có nghĩa người đó không phải diễn viên?** Không. OWL dùng giả định thế giới mở: chưa đủ thông tin để suy ra Actor không đồng nghĩa phủ định Actor. Tương tự, không có credit đã lưu không chứng minh phim không có credit.

**Cardinality có buộc dữ liệu lưu đủ trường không?** OWL phát biểu ngữ nghĩa, không kiểm tra biểu mẫu như cơ sở dữ liệu. Thiếu triple có thể chỉ là thiếu thông tin; functional/cardinality có thể dẫn đến đồng nhất giá trị. `src/validate.py` kiểm tra riêng các trường phải có trong dữ liệu ứng dụng.

## Tái lập và kiểm tra

```bash
.venv/bin/python src/build.py
.venv/bin/python src/validate.py
.venv/bin/python src/reason.py
.venv/bin/python -m pytest -q
```

`evidence/ontology_reasoning.json` lưu số cá thể khai báo/suy ra của sáu lớp, các lớp suy ra cho Nolan và lỗi mà owlrl phát hiện. `data/processed/inferred_classes.ttl` là kết quả phân loại riêng, có thể truy vấn bằng RDFLib. Dataset ứng dụng, endpoint và Comunica vẫn truy vấn dữ liệu khai báo; chúng không tự chạy suy luận. Muốn dùng các lớp mới trong truy vấn, nạp thêm kết quả phân loại hoặc chạy reasoner.

Mở `ontology/Movie_Knowledge_Graph.owl` bằng Protégé, chọn HermiT và Start reasoner để xem phân loại với dữ liệu. `Movie_Ontology.owl` chỉ có schema và các cá thể vai trò, nên không có Nolan để phân loại. HermiT chưa được chạy trong kiểm tra tự động của repo; owlrl là phép đóng theo luật OWL RL/RDF, không phải bằng chứng nhất quán đầy đủ OWL DL.

Các test kiểm tra phân loại đúng tập người/phim, cho phép chồng lấp vai trò, hai phim khác nhau trong DirectorWriter, thiếu dữ kiện không tạo membership và phát hiện ca cố ý gán cùng một cá thể là Film và Country. Không đưa dữ liệu mâu thuẫn vào bản nộp.

Nguồn ngữ nghĩa: [W3C OWL 2 Primer, mục 4.3, 5.1 và 5.2](https://www.w3.org/TR/owl2-primer/).
