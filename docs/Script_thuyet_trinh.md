---
title: "MovieLOD: lời thuyết trình cho bộ 24 slide"
date: "Bản đầy đủ · 08/10/2026"
---

## Cách dùng

Bộ chính có **24 slide**, thuyết trình đầy đủ khoảng **18–22 phút**. Mỗi đoạn lời cũng nằm trong Speaker Notes. Bản ngắn 13 trang vẫn ở Slide_ngan_13.pptx/pdf và Script_thuyet_trinh_ngan_13.md/pdf. Video demo 4:50 là tài liệu riêng; không đọc toàn bộ lời slide vào video.

Tập theo 3 phần: thành viên A slide 1–10; B slide 11–18; C slide 19–24. Nếu chỉ có 2 người, chia sau slide 14. Các con số lấy từ dữ liệu và evidence hiện tại. Khung ảnh Protégé chưa có ảnh thực; không đọc ghi chú chờ bổ sung như kết quả đã chứng minh.

## Luồng rút gọn 12–15 phút

Ưu tiên slide 1–5, 9–10, 12–13, 15–17, 19–23. Các trang cây lớp, công thức cardinality và tra cứu IRI có thể dùng khi trả lời câu hỏi.

## Mục lục

| Slide | Nội dung |
|:--|:--|
| 01 | MovieLOD |
| 02 | Bài giải quyết gì? Đối chiếu đủ 5 yêu cầu |
| 03 | Kiến trúc và đường đi của dữ liệu |
| 04 | Bộ dữ liệu hiện tại: đọc đúng các con số |
| 05 | YC1 · Ontology: 42 lớp, 6 nhóm khái niệm |
| 06 | YC1 · Cây lớp tác phẩm và phim |
| 07 | YC1 · Người, tổ chức và vai trò nghề nghiệp |
| 08 | YC1 · Thể loại, giải thưởng và xuất xứ |
| 09 | YC1 · Contribution: ai làm gì trong phim nào? |
| 10 | YC1 · Quan hệ, domain/range và inverse |
| 11 | YC1 · OWL mô tả ngữ nghĩa như thế nào? |
| 12 | YC1 · 14 lớp có kiểu được bổ sung |
| 13 | YC1 · Ví dụ suy luận: Christopher Nolan |
| 14 | YC1 · Cardinality: ngưỡng 2 và ngưỡng 3 |
| 15 | YC2 · Thu thập thật và giữ xuất xứ |
| 16 | YC3 · RDF và giá trị có datatype |
| 17 | YC3–YC4 · Từ RDF đến Linked Open Data |
| 18 | YC3 · Tra cứu IRI của Inception |
| 19 | YC5 · Truy vấn Inception trên Web |
| 20 | YC5 · Một người, nhiều vai trò và nhiều câu hỏi |
| 21 | YC5 · Endpoint, terminal và kiểu được bổ sung |
| 22 | Kiểm tra dữ liệu, ứng dụng và bản công khai |
| 23 | Đối chiếu đề và giới hạn cần nói rõ |
| 24 | Kết luận và ảnh Protégé cần bổ sung |

## Slide 01 — MovieLOD

**Lời nói:**

Chào thầy cô và các bạn. Nhóm chúng em trình bày MovieLOD, ứng dụng dữ liệu mở có liên kết về điện ảnh. Bài đi từ mô hình khái niệm, dữ liệu nguồn và RDF đến liên kết ngoài và truy vấn. Phiên bản hiện tại có 30 phim, 42 lớp ontology và 1.727 liên kết ngoài. Ví dụ xuyên suốt là Inception và Christopher Nolan. Bộ slide này có 24 trang; lời nói riêng và hướng dẫn chụp minh chứng Protégé đi kèm. Một số khung ảnh Protégé được để sẵn vì lần làm tài liệu này chưa chụp được giao diện trên máy. Các khung này ghi rõ yêu cầu, không được coi là ảnh minh chứng đã có.

**Chuyển trang:** Sau đây nhóm chuyển sang bài giải quyết gì? đối chiếu đủ 5 yêu cầu.

## Slide 02 — Bài giải quyết gì? Đối chiếu đủ 5 yêu cầu

**Lời nói:**

Điện ảnh có nhiều thực thể và nhiều vai trò chồng lấp. Chúng ta muốn hỏi Nolan tham gia Inception ở những vai trò nào, phim này liên quan tới công ty nào hoặc dữ liệu lấy từ phản hồi nào. Năm yêu cầu của đề tạo thành một chuỗi công việc. Ontology định nghĩa khái niệm và quan hệ. Thu thập cung cấp dữ liệu thật. Chuyển đổi tạo RDF và IRI với giấy phép mở. Liên kết nối cá thể tới Wikidata và DBpedia. SPARQL cho phép đặt câu hỏi trên đồ thị. Đề còn yêu cầu báo cáo không quá 15 trang và video 3–5 phút; video demo hiện dài khoảng 4 phút 50 giây.

**Chuyển trang:** Sau đây nhóm chuyển sang kiến trúc và đường đi của dữ liệu.

## Slide 03 — Kiến trúc và đường đi của dữ liệu

**Lời nói:**

Luồng xử lý bắt đầu từ danh sách phim trong config. collect lấy phản hồi nguồn và lưu metadata. build tạo ontology cùng graph RDF từ dữ liệu đã chuẩn hóa. validate kiểm tra trường ứng dụng, hash và truy vấn. reason bổ sung các kiểu phân loại ở file riêng. Web cục bộ gọi endpoint Flask dùng RDFLib; hosted dùng Comunica trong trình duyệt. Endpoint mặc định đọc movies.ttl, còn terminal với reasoned nạp thêm schema và inferred_classes.ttl. Tùy chọn này nạp kết quả phân loại đã lưu, không tự chạy reasoner mỗi lần truy vấn. Việc tách ba phần giúp phân biệt dữ kiện gốc với kiểu được bổ sung.

**Chuyển trang:** Sau đây nhóm chuyển sang bộ dữ liệu hiện tại: đọc đúng các con số.

## Slide 04 — Bộ dữ liệu hiện tại: đọc đúng các con số

**Lời nói:**

Mẫu hiện có 30 phim, 851 người và 1.010 bản ghi đóng góp. Ngoài ra có 45 công ty, 672 thực thể giải thưởng, 75 thể loại, 11 quốc gia và 15 ngôn ngữ. 76 phản hồi gốc được giữ và kiểm tra hash. Dữ liệu gồm 19.339 triple, tách khỏi 518 triple lược đồ. Cần đọc đúng đơn vị: 672 là số thực thể giải khác nhau, không phải số lần trao giải; 1.010 là bản ghi một người giữ một vai trò trong một phim, không phải số người. Mọi phim trong mẫu có năm, thời lượng và đạo diễn, nhưng mẫu này không đại diện toàn bộ điện ảnh.

**Chuyển trang:** Sau đây nhóm chuyển sang yc1 · ontology: 42 lớp, 6 nhóm khái niệm.

## Slide 05 — YC1 · Ontology: 42 lớp, 6 nhóm khái niệm

**Lời nói:**

Ontology có 42 IRI lớp được khai báo owl Class, trong đó ba lớp dùng trực tiếp từ DBpedia, còn lại thuộc namespace của bài. Chúng ta có nhánh tác phẩm và phim; chủ thể người hoặc tổ chức; đóng góp và vai trò; thể loại; giải thưởng; và các lớp bổ trợ cho quốc gia, ngôn ngữ, nguồn, dataset. Trong số này, 14 lớp có kiểu được bổ sung từ định nghĩa hoặc quy tắc phân loại. Các lớp ngoài được tham chiếu qua equivalentClass có thể được Protégé tính thêm trong Metrics; vì vậy con số 42 dùng quy ước đếm lớp tự khai báo. Ảnh cần bổ sung ở bên phải là IRI ontology và versionInfo 2.0.0.

**Ảnh cần bổ sung — P00:** `P00_ontology_header.png`; mở `ontology/Movie_Ontology.owl`.

1. Mở ontology/Movie_Ontology.owl.
2. Chọn Active Ontology / Ontology Header.
3. Giữ IRI ontology và versionInfo 2.0.0 trong khung hình.

**Cần thấy:** IRI đúng namespace của bài; phiên bản 2.0.0. Metrics có thể tính cả lớp ngoài được tham chiếu, khác 42 lớp tự khai báo.

**Chuyển trang:** Sau đây nhóm chuyển sang yc1 · cây lớp tác phẩm và phim.

## Slide 06 — YC1 · Cây lớp tác phẩm và phim

**Lời nói:**

CreativeWork là nhánh tác phẩm. Film dùng IRI DBpedia và có các lớp con như FeatureFilm, AnimatedFilm, DocumentaryFilm. FeatureFilm và AnimatedFilm được ánh xạ theo quy tắc P31 của bài; đây là cách giản lược, không phải khẳng định đã kiểm tra mọi tiêu chí phát hành rạp. Các lớp ActionFilm, ComedyFilm, DramaFilm, ScienceFictionFilm, MultiGenreFilm và AwardWinningFilm được phân loại bổ sung. DocumentaryFilm hiện không có cá thể trong mẫu. Việc có một lớp trong mô hình không yêu cầu mẫu dữ liệu phải có sẵn mọi loại phim. Khung ảnh yêu cầu mở cây CreativeWork/Film và chọn Film để thấy IRI DBpedia.

**Ảnh cần bổ sung — P01:** `P01_film_hierarchy.png`; mở `ontology/Movie_Ontology.owl`.

1. Entities → Classes → mở CreativeWork và Film.
2. Hiện các lớp con FeatureFilm, AnimatedFilm và nhóm phim.
3. Chọn Film; giữ IRI DBpedia và Class Description.

**Cần thấy:** Film thuộc CreativeWork; IRI là http://dbpedia.org/ontology/Film. Chụp cây khai báo, không gọi là cây đã suy luận.

**Chuyển trang:** Sau đây nhóm chuyển sang yc1 · người, tổ chức và vai trò nghề nghiệp.

## Slide 07 — YC1 · Người, tổ chức và vai trò nghề nghiệp

**Lời nói:**

Agent gồm Person và Organization. Person dùng lớp DBpedia và có các nhóm Actor, Filmmaker, AwardWinner. Organization có ProductionCompany; FilmStudio là nhóm công ty được ứng dụng phân loại theo ngưỡng số phim trong mẫu. Actor và Filmmaker không rời nhau, vì một người có thể vừa diễn xuất vừa đạo diễn hoặc biên kịch. Chúng ta cũng không dùng một lớp tổ hợp DirectorWriter để giữ hai nghề; từng công việc được ghi qua Contribution và SPARQL có thể JOIN các đóng góp. Số người hoặc công ty không được suy từ số dòng của một truy vấn có LIMIT. Ảnh cần chụp là cây Agent mở cả nhánh Person và Organization.

**Ảnh cần bổ sung — P02:** `P02_agent_hierarchy.png`; mở `ontology/Movie_Ontology.owl`.

1. Entities → Classes → mở Agent.
2. Mở Person và Organization → ProductionCompany.
3. Chọn Person hoặc Filmmaker; giữ cây lớp và Description.

**Cần thấy:** Person và Organization cùng dưới Agent; Actor/Filmmaker/AwardWinner là lớp con Person.

**Chuyển trang:** Sau đây nhóm chuyển sang yc1 · thể loại, giải thưởng và xuất xứ.

## Slide 08 — YC1 · Thể loại, giải thưởng và xuất xứ

**Lời nói:**

Genre có FictionGenre và NonFictionGenre; các lớp thể loại hành động, hài, chính kịch, khoa học viễn tưởng thuộc FictionGenre, còn DocumentaryGenre dưới NonFictionGenre. Award có các nhóm FilmAward, ActingAward, DirectingAward, WritingAward. Việc chia nhóm thể loại và giải hiện dùng từ khóa nhãn trong bước build, không phải suy luận tự khám phá nghĩa tiếng Anh. FilmAward là nhóm mặc định khi nhãn chưa khớp một nhóm nghề nghiệp. Các lớp Country, Language, SourceSnapshot và Dataset bổ sung bối cảnh và xuất xứ. Giải của người được giữ riêng với giải của phim. Khung ảnh cần mở hai nhánh Genre và Award, thu gọn nhánh khác để đọc rõ.

**Ảnh cần bổ sung — P03:** `P03_genre_award_hierarchy.png`; mở `ontology/Movie_Ontology.owl`.

1. Thu gọn Film/Agent để ảnh dễ đọc.
2. Mở Genre → FictionGenre / NonFictionGenre và Award.
3. Hiện các lớp thể loại và nhóm giải; giữ Class Description.

**Cần thấy:** Cây Genre/Award khớp sơ đồ. Nhóm thể loại/giải được ánh xạ theo nhãn trong bước build.

**Chuyển trang:** Sau đây nhóm chuyển sang yc1 · contribution: ai làm gì trong phim nào?.

## Slide 09 — YC1 · Contribution: ai làm gì trong phim nào?

**Lời nói:**

Nếu chỉ gắn một nhãn nghề nghiệp cho Nolan, chúng ta không biết vai trò đó thuộc phim nào. Contribution giải quyết bằng một bản ghi nối một người, một phim và một vai trò. contributionBy trỏ Person, contributionTo trỏ Film, hasRole trỏ ContributionRole. Mỗi quan hệ có ràng buộc đúng một giá trị phù hợp. Bốn cá thể vai trò là DirectorRole, ActorRole, WriterRole, ProducerRole. Nolan giữ ba vai trò trong Inception, vì vậy có ba Contribution riêng. Các nhóm Acting, Directing, Writing, ProducingContribution được phân loại từ hasRole. Ảnh cần chụp Class Description của Contribution, hiện cả exactly 1 và các restriction về loại giá trị.

**Ảnh cần bổ sung — P04:** `P04_contribution_restrictions.png`; mở `ontology/Movie_Ontology.owl`.

1. Entities → Classes → chọn Contribution.
2. Trong Class Description, mở đủ SubClass Of.
3. Hiện contributionBy / contributionTo / hasRole: exactly 1.

**Cần thấy:** Ba qualified cardinality đúng 1, cùng các allValuesFrom. Đây là mô hình OWL, không phải biên bản kiểm tra thiếu trường.

**Chuyển trang:** Sau đây nhóm chuyển sang yc1 · quan hệ, domain/range và inverse.

## Slide 10 — YC1 · Quan hệ, domain/range và inverse

**Lời nói:**

Object property nối hai thực thể. contributionBy có domain Contribution và range Person; quan hệ ngược là hasContribution. contributionTo nối tới Film, hasRole nối tới ContributionRole. Ba quan hệ này có tính functional. Các quan hệ trực tiếp director, starring, writer, producer dùng từ DBpedia để hỏi thuận tiện. Những cặp như hasGenre/genreOf, hasProductionCompany/productionOf, hasAward/awardOf cho phép đi hai chiều. inverse là đảo hướng, không đồng nghĩa quan hệ đối xứng. Domain và range có thể giúp suy ra kiểu khi quan hệ được biết; chúng không tự đóng vai trò từ chối nhập liệu như một biểu mẫu. Ảnh yêu cầu chọn contributionBy để thấy domain/range/inverse/functional.

**Ảnh cần bổ sung — P05:** `P05_object_property.png`; mở `ontology/Movie_Ontology.owl`.

1. Entities → Object properties → chọn contributionBy.
2. Hiện Domain=Contribution, Range=Person.
3. Giữ inverse hasContribution và ô Functional được chọn.

**Cần thấy:** Đúng domain/range/inverse/functional của contributionBy. Nếu cần, chụp bổ sung hasRole hoặc director.

**Tra cứu khi bảo vệ (không đọc toàn bộ):**

Bảng tra đủ 23 object property (không cần đọc hết khi thuyết trình):
| Quan hệ | Domain | Range | Inverse / đặc tính |
|:--|:--|:--|:--|
| dbo:director | dbo:Film | dbo:Person | ex:directed |
| dbo:producer | dbo:Film | dbo:Person | ex:produced |
| dbo:starring | dbo:Film | dbo:Person | ex:actedIn |
| dbo:writer | dbo:Film | dbo:Person | ex:wrote |
| ex:actedIn | dbo:Person | dbo:Film | dbo:starring |
| ex:awardOf | ex:Award | dbo:Film hoặc dbo:Person | ex:hasAward |
| ex:contributionBy | ex:Contribution | dbo:Person | ex:hasContribution · functional |
| ex:contributionOf | dbo:Film | ex:Contribution | ex:contributionTo |
| ex:contributionTo | ex:Contribution | dbo:Film | ex:contributionOf · functional |
| ex:country | dbo:Film | dbo:Country | — |
| ex:directed | dbo:Person | dbo:Film | dbo:director |
| ex:genreOf | ex:Genre | dbo:Film | ex:hasGenre |
| ex:hasAward | dbo:Film hoặc dbo:Person | ex:Award | ex:awardOf |
| ex:hasContribution | dbo:Person | ex:Contribution | ex:contributionBy |
| ex:hasGenre | dbo:Film | ex:Genre | ex:genreOf |
| ex:hasProductionCompany | dbo:Film | ex:ProductionCompany | ex:productionOf |
| ex:hasRole | ex:Contribution | ex:ContributionRole | ex:roleOf · functional |
| ex:language | dbo:Film | ex:Language | — |
| ex:produced | dbo:Person | dbo:Film | dbo:producer |
| ex:productionOf | ex:ProductionCompany | dbo:Film | ex:hasProductionCompany |
| ex:roleOf | ex:ContributionRole | ex:Contribution | ex:hasRole |
| ex:sourceSnapshot | — | ex:SourceSnapshot | — |
| ex:wrote | dbo:Person | dbo:Film | dbo:writer |

**Chuyển trang:** Sau đây nhóm chuyển sang yc1 · owl mô tả ngữ nghĩa như thế nào?.

## Slide 11 — YC1 · OWL mô tả ngữ nghĩa như thế nào?

**Lời nói:**

OWL cho phép định nghĩa tương đương lớp, giao, hợp, tồn tại, giá trị cố định và cardinality. Ví dụ Contribution có exactly một Person, một Film và một Role; DirectingContribution được nhận diện khi hasRole có giá trị DirectorRole. Quan hệ inverse suy ra đường đi ngược. Disjointness chỉ dùng cho các lớp không thể chồng lấp theo mô hình, không dùng cho Actor với Filmmaker. Cần nhớ giả định thế giới mở: thiếu một triple không tự chứng minh sự việc không có. Các IRI khác nhau cũng không tự bảo đảm là cá thể khác nhau. Vì vậy ứng dụng dùng kiểm tra Python riêng để phát hiện thiếu hoặc thừa trường, còn OWL phát biểu ý nghĩa và hỗ trợ phân loại.

**Chuyển trang:** Sau đây nhóm chuyển sang yc1 · 14 lớp có kiểu được bổ sung.

## Slide 12 — YC1 · 14 lớp có kiểu được bổ sung

**Lời nói:**

Bảng này cho thấy toàn bộ 14 lớp có kiểu được bổ sung. Bốn nhóm Contribution dùng role, ba nhóm người dùng đóng góp hoặc giải, năm nhóm phim dùng thể loại hoặc giải. Mười hai lớp thuộc phần xử lý bằng luật OWL RL. Hai lớp còn lại, MultiGenreFilm và FilmStudio, dùng truy vấn COUNT DISTINCT sau bước luật. Các số đếm chỉ tính tài nguyên nội bộ để tránh alias sameAs làm tăng số. Bảng là kết quả trong ontology_reasoning.json, không phải 14 kiểu gán sẵn trong movies.ttl. Hai truy vấn người có LIMIT 20; số hiển thị không phải tổng 769 Actor hoặc 89 Filmmaker. Phần cardinality được giải thích riêng ở slide sau.

**Chuyển trang:** Sau đây nhóm chuyển sang yc1 · ví dụ suy luận: christopher nolan.

## Slide 13 — YC1 · Ví dụ suy luận: Christopher Nolan

**Lời nói:**

Dữ liệu gốc chỉ khai báo Nolan là Person, cùng các quan hệ đóng góp và giải. Một Contribution của Nolan trong Inception có DirectorRole. Định nghĩa hasValue phân loại bản ghi này là DirectingContribution. Từ Person có loại đóng góp đạo diễn, biên kịch hoặc sản xuất, định nghĩa dùng giao, hợp và tồn tại phân loại Nolan là Filmmaker. Nolan còn có giải riêng nên được bổ sung AwardWinner. Đây là khác biệt giữa kiểu gán ban đầu và kiểu suy ra trong ứng dụng. Khung ảnh yêu cầu Class Description và Equivalent To của Filmmaker. Ảnh này chứng minh công thức đã khai báo; kết quả thực thi được kiểm chứng riêng bằng terminal và tests.

**Ảnh cần bổ sung — P06:** `P06_filmmaker_equivalent_class.png`; mở `ontology/Movie_Ontology.owl`.

1. Entities → Classes → chọn Filmmaker.
2. Mở Class Description → Equivalent To.
3. Hiện Person AND các nhánh SOME Directing/Writing/ProducingContribution.

**Cần thấy:** Định nghĩa giao/hợp/tồn tại. Ảnh định nghĩa không tự chứng minh HermiT đã phân loại dữ liệu.

**Chuyển trang:** Sau đây nhóm chuyển sang yc1 · cardinality: ngưỡng 2 và ngưỡng 3.

## Slide 14 — YC1 · Cardinality: ngưỡng 2 và ngưỡng 3

**Lời nói:**

MultiGenreFilm được định nghĩa là Film có ít nhất hai Genre; FilmStudio là ProductionCompany có ít nhất ba Film qua productionOf. Trong mẫu, toàn bộ 30 phim có ít nhất hai thể loại và có sáu công ty đạt ngưỡng ba phim. Warner Bros. liên quan tới 11 phim trong mẫu. owlrl không xử lý các ngưỡng này theo nhu cầu của bài, nên reason.py dùng COUNT DISTINCT bổ sung sau khi suy ra inverse. Đếm IRI khác nhau là quy tắc ứng dụng; trong OWL, hai tên khác nhau có thể chỉ cùng một cá thể. HermiT/Pellet đã chạy: hai lớp này có không cá thể được suy luận, còn 30 và sáu là số đếm trong ứng dụng. Ảnh cần chụp công thức min 3 của FilmStudio, không yêu cầu giả lập kết quả reasoner.

**Ảnh cần bổ sung — P07:** `P07_filmstudio_cardinality.png`; mở `ontology/Movie_Ontology.owl`.

1. Entities → Classes → chọn FilmStudio.
2. Mở Equivalent To; hiện min 3 productionOf Film.
3. Có thể chụp thêm MultiGenreFilm: min 2 hasGenre Genre.

**Cần thấy:** Ảnh công thức cardinality. Kết quả 6 studio/30 phim nhiều thể loại của app dùng COUNT DISTINCT, không tự coi là chứng minh OWL DL.

**Chuyển trang:** Sau đây nhóm chuyển sang yc2 · thu thập thật và giữ xuất xứ.

## Slide 15 — YC2 · Thu thập thật và giữ xuất xứ

**Lời nói:**

Danh tính phim được xác định qua sitelink Wikipedia tiếng Anh chính xác, thay vì so tên gần giống. Wikidata cung cấp đạo diễn P57, diễn viên P161, biên kịch P58, nhà sản xuất P162, giải P166 và công ty P272. DBpedia chỉ nối khi chủ thể khớp tiêu đề và có kiểu Film; vì vậy có 28 liên kết DBpedia thay vì tự đoán đủ 30. Mỗi phản hồi có URL, provider, thời điểm, HTTP status, SHA-256 và đường dẫn. Hiện đủ 76 phản hồi và hash khớp. Một phản hồi tải lại đổi nội dung được ghi hash/time mới, đồng thời giữ danh mục lịch sử. Hash kiểm tra toàn vẹn byte, không chứng minh mọi phát biểu ngoài đời đúng.

**Chuyển trang:** Sau đây nhóm chuyển sang yc3 · rdf và giá trị có datatype.

## Slide 16 — YC3 · RDF và giá trị có datatype

**Lời nói:**

Một triple gồm chủ thể, quan hệ và đối tượng hoặc giá trị. Inception có đạo diễn Nolan, năm 2010 và thời lượng 148 phút. Quan hệ đạo diễn nối hai thực thể; năm và thời lượng là literal có datatype. Dùng QID để tạo IRI ổn định; chuẩn hóa các đơn vị giờ, phút, giây về phút và ghi các trường hợp nguồn có nhiều giá trị. Sáu datatype property khai báo là title, releaseYear, runtimeMinutes, sourceUrl, retrievedAt, sha256. Turtle và JSON-LD biểu diễn cùng graph; file OWL riêng có schema, file Knowledge Graph có schema và dữ liệu. Ảnh cần chọn runtimeMinutes trong Data properties để thấy domain Film và range decimal.

**Ảnh cần bổ sung — P08:** `P08_runtime_datatype.png`; mở `ontology/Movie_Ontology.owl`.

1. Entities → Data properties → chọn runtimeMinutes.
2. Hiện Domain=Film và Range=xsd:decimal.
3. Có thể chụp thêm releaseYear có range xsd:integer.

**Cần thấy:** Thuộc tính dữ liệu nối thực thể với literal, khác quan hệ nối hai thực thể.

**Chuyển trang:** Sau đây nhóm chuyển sang yc3–yc4 · từ rdf đến linked open data.

## Slide 17 — YC3–YC4 · Từ RDF đến Linked Open Data

**Lời nói:**

Mức một sao bắt đầu với dữ liệu trên Web có giấy phép mở; hai sao là có cấu trúc; ba sao dùng định dạng mở; bốn sao dùng HTTP URI và chuẩn RDF để tra cứu; năm sao thêm liên kết tới dữ liệu khác. Bài có giấy phép CC BY-SA 4.0, RDF/Turtle/JSON-LD và các IRI có trang mô tả. Bản công khai đã được kiểm tra không đăng nhập, cả bốn graph RDF đối chiếu đều đẳng cấu với local. Có 1.699 liên kết Wikidata và 28 DBpedia. sameAs khẳng định cùng danh tính, còn sourceSnapshot ghi xuất xứ. Tái dùng dbo:Film là dùng từ vựng lớp ở YC1, khác liên kết cá thể ở YC4.

**Chuyển trang:** Sau đây nhóm chuyển sang yc3 · tra cứu iri của inception.

## Slide 18 — YC3 · Tra cứu IRI của Inception

**Lời nói:**

Trang Inception hiển thị tên, kiểu, năm, thời lượng, đạo diễn, đóng góp, liên kết ngoài và nguồn. Người đọc có thể tải mô tả Turtle; HTML cũng nhúng JSON-LD. Ở Flask local, Accept text turtle trả 303 đến mô tả RDF và curl trừ L theo chuyển hướng. Hosted tĩnh cung cấp HTML/JSON-LD và link RDF; không tự khẳng định nó có cùng hành vi 303 như Flask. Bên trái là ảnh ứng dụng thật. Bên phải là khung cần ảnh Individuals trong Protégé khi mở Knowledge Graph: chọn film-Q25188 và hiện kiểu cùng các thuộc tính. Không mở file chỉ schema để chụp cá thể.

**Ảnh cần bổ sung — P09:** `P09_inception_individual.png`; mở `ontology/Movie_Knowledge_Graph.owl`.

1. Mở ontology/Movie_Knowledge_Graph.owl.
2. Individuals → chọn film-Q25188 (Inception).
3. Hiện Film, title, releaseYear=2010, runtimeMinutes=148 và director.

**Cần thấy:** Cá thể thật và thuộc tính khớp truy vấn. Giữ tên ontology để không chụp nhầm file chỉ có schema.

**Chuyển trang:** Sau đây nhóm chuyển sang yc5 · truy vấn inception trên web.

## Slide 19 — YC5 · Truy vấn Inception trên Web

**Lời nói:**

Truy vấn đầu tiên tìm phim tên Inception, đi theo director tới người và lấy nhãn người đó. Kết quả là Inception, 2010, 148 phút, Christopher Nolan. SELECT chọn cột, WHERE đưa mẫu đồ thị, dấu hỏi đánh dấu biến. OPTIONAL giữ dòng khi thuộc tính năm hoặc thời lượng có thể thiếu. Người dùng có thể sửa truy vấn, bấm Run query và tải kết quả. Giao diện có 14 mẫu trực tiếp. Ngoài SELECT trả bảng, ASK trả True hoặc False, CONSTRUCT tạo graph RDF. Kết quả được tính từ graph; danh sách phim hoặc tên đạo diễn không được nhập cứng trong bảng.

**Chuyển trang:** Sau đây nhóm chuyển sang yc5 · một người, nhiều vai trò và nhiều câu hỏi.

## Slide 20 — YC5 · Một người, nhiều vai trò và nhiều câu hỏi

**Lời nói:**

Câu hỏi toàn bộ đóng góp Inception trả 25 bản ghi, gồm 21 diễn viên, một đạo diễn, một biên kịch và hai nhà sản xuất. Ảnh trên slide lọc riêng Christopher Nolan nên chỉ còn ba dòng: Director, Writer, Producer. Chúng ta không lấy ba dòng này làm tổng đóng góp. Các truy vấn khác cho biết tám phim do Nolan đạo diễn trong mẫu, bốn công ty liên quan Inception và bảy giải của The Godfather. Việc thêm câu hỏi không cần nhập một bảng kết quả riêng; chúng dùng cùng đồ thị và mô hình. Download results xuất kết quả đang hiển thị. Các file truy vấn và biên bản cho phép kiểm tra lại những số này.

**Chuyển trang:** Sau đây nhóm chuyển sang yc5 · endpoint, terminal và kiểu được bổ sung.

## Slide 21 — YC5 · Endpoint, terminal và kiểu được bổ sung

**Lời nói:**

Bài có endpoint GET/POST và terminal, ngoài giao diện Web. SELECT và ASK trả JSON; CONSTRUCT và DESCRIBE trả Turtle. Endpoint mặc định chỉ nạp graph khai báo. Lệnh query.py với reasoned nạp thêm schema và inferred_classes.ttl. Cùng câu 24 trên Nolan trả một kiểu Person khi chạy gốc; chạy reasoned trả Person, Filmmaker, AwardWinner. File kiểu được tạo trước bởi reason.py, không tính suy luận mỗi lần gọi query.py. Truy vấn hierarchy như câu 13 cần schema; Actor/Filmmaker có LIMIT 20 nên tổng thực ở biên bản là 769 và 89. Khung ảnh Protégé yêu cầu Types của Nolan ở chế độ asserted; nếu ảnh sau reasoner phải ghi rõ trạng thái.

**Ảnh cần bổ sung — P10:** `P10_nolan_asserted_types.png`; mở `ontology/Movie_Knowledge_Graph.owl`.

1. Mở Movie_Knowledge_Graph.owl, chọn person-Q25191 (Nolan).
2. Hiện Types trong chế độ asserted / trước suy luận.
3. Giữ dbo:Person và các quan hệ đóng góp/giải trong ảnh.

**Cần thấy:** Kiểu gán gốc là Person; Filmmaker/AwardWinner trong app được bổ sung qua file phân loại. Nếu chụp sau reasoner, phải ghi rõ tên và trạng thái thực thi.

**Tra cứu khi bảo vệ (không đọc toàn bộ):**

Bảng tra 24 truy vấn; số là số dòng trả về, hoặc boolean đối với ASK:
| File | Gốc | Có schema / phân loại |
|:--|:--|:--|
| 01_films.rq | 30 | 30 |
| 02_inception.rq | 1 | 1 |
| 03_nolan.rq | 8 | 8 |
| 04_credits.rq | 25 | 25 |
| 05_external_links.rq | 58 | 58 |
| 06_genres.rq | 75 | 75 |
| 07_source.rq | 2 | 2 |
| 08_ask.rq | true | true |
| 09_actors_of_inception.rq | 21 | 21 |
| 10_production_companies_of_a_film.rq | 4 | 4 |
| 11_awards_received_by_a_film.rq | 7 | 7 |
| 12_countries_and_languages_of_a_film.rq | 1 | 1 |
| 13_fiction_genre_films_via_hierarchy.rq | 0 | 29 |
| 14_all_agents_people_and_organizations.rq | 1 | 1 |
| 15_feature_vs_animated_film_counts.rq | 1 | 1 |
| 16_documentary_film_count_ask.rq | false | false |
| 17_inferred_actors.rq | 0 | 20 |
| 18_inferred_filmmakers.rq | 0 | 20 |
| 19_inferred_action_films.rq | 0 | 12 |
| 20_inferred_multi_genre_films.rq | 0 | 30 |
| 21_inferred_award_winning_films.rq | 0 | 26 |
| 22_inferred_film_studios.rq | 0 | 6 |
| 23_people_with_directing_and_writing_contribution.rq | 0 | 10 |
| 24_nolan_asserted_types_only.rq | 1 | 3 |
Câu 14/15 trả một dòng thống kê. Câu 17/18 có LIMIT 20; tổng Actor/Filmmaker là 769/89. Câu 24 có 1 kiểu gốc hoặc 3 kiểu khi nạp phân loại.

**Chuyển trang:** Sau đây nhóm chuyển sang kiểm tra dữ liệu, ứng dụng và bản công khai.

## Slide 22 — Kiểm tra dữ liệu, ứng dụng và bản công khai

**Lời nói:**

validate đã kiểm tra tên, nguồn, liên kết của phim và các thành phần Contribution; 76 hash nguồn khớp và 24 file truy vấn đã chạy ở chế độ dữ liệu phù hợp. Có 14 test pass và chín kiểm tra trình duyệt đạt, gồm endpoint, Comunica, lỗi cú pháp, ASK, CONSTRUCT, trang IRI và màn hình mobile. Bản công khai được kiểm tra qua tám URL không có cookie hay đăng nhập; bốn graph RDF đều đẳng cấu với local, có giấy phép và link mô tả máy đọc được. HermiT/Pellet riêng đã xác nhận OWL nhất quán và không có lớp không khả thỏa. Test và hash không chứng minh mọi thông tin ngoài đời đúng. Timestamp OWL/Turtle/JSON-LD đã đồng bộ đến mili giây. Đó là lý do cần vừa nêu kết quả vừa giữ giới hạn phương pháp.

**Chuyển trang:** Sau đây nhóm chuyển sang đối chiếu đề và giới hạn cần nói rõ.

## Slide 23 — Đối chiếu đề và giới hạn cần nói rõ

**Lời nói:**

Ảnh đề gốc không đưa trọng số; nhóm dùng thang tự đánh giá chia đều hai điểm mỗi yêu cầu. Ontology, thu thập, RDF công khai, liên kết và truy vấn đều có minh chứng đạt nên đề xuất mười trên mười. Đây không phải điểm chính thức của giảng viên. Các giới hạn vẫn còn: mẫu 30 phim có chủ đích; nhóm thể loại và giải ánh xạ theo nhãn; chưa có ngân sách hoặc streaming; HermiT/Pellet đã xác nhận nhất quán, còn hai nhóm cardinality chỉ có số đếm ứng dụng 30/6; DL có không cá thể. SQL cũng có thể trả nhiều câu hỏi bằng JOIN/view/quy tắc. Giá trị Semantic Web ở đây là IRI dùng chung, từ vựng tái dùng, liên kết dataset, xuất xứ và định nghĩa ngữ nghĩa tường minh.

**Chuyển trang:** Sau đây nhóm chuyển sang kết luận và ảnh protégé cần bổ sung.

## Slide 24 — Kết luận và ảnh Protégé cần bổ sung

**Lời nói:**

MovieLOD đã nối mô hình, dữ liệu thật, nguồn, RDF, liên kết và truy vấn trong một ứng dụng. Bản này có 24 slide; nhóm có thể trình bày đầy đủ khoảng 18–22 phút hoặc chọn các trang chính để rút gọn. Trước khi nộp, điền tên thành viên và bổ sung các ảnh Protégé theo mã trên bảng. Các khung ảnh và hướng dẫn đã có ngay ở những slide liên quan. Giao diện macOS chưa cho phép chụp trong lần làm tài liệu này, nên không có ảnh Protégé giả được gắn vào. Có thể chèn ảnh trực tiếp trong PowerPoint hoặc lưu đúng tên ở evidence/protege rồi chạy lại trình tạo slide. Nhóm xin kết thúc và sẵn sàng trả lời câu hỏi.

**Chuyển trang:** Nhóm xin mời thầy cô đặt câu hỏi.

## Câu hỏi bảo vệ ngắn

**42 lớp khác gì 30 phim?** 42 là lớp trong schema; 30 là cá thể Film trong graph dữ liệu. Protégé Metrics có thể tính thêm lớp ngoài được tham chiếu.

**Vì sao cần Contribution?** Một người có nhiều vai trò trong nhiều phim; mỗi bộ người–phim–vai trò có bản ghi riêng.

**Vì sao exact cardinality chưa thay Python?** OWL dùng thế giới mở; Python kiểm tra trường bắt buộc của ứng dụng.

**COUNT DISTINCT có phải suy luận DL không?** Đếm tên IRI là quy tắc ứng dụng; OWL không mặc định tên khác nhau chỉ cá thể khác nhau.

**Endpoint không có Filmmaker có phải lỗi?** Endpoint mặc định graph gốc. Dùng --reasoned nạp schema và kết quả phân loại.

**sameAs khác nguồn thế nào?** sameAs là cùng danh tính; sourceSnapshot là xuất xứ; dbo:Film là tái dùng từ vựng.

**SQL có trả được các câu hỏi không?** Có, bằng JOIN/view/quy tắc. Giá trị của bài là IRI, từ vựng chung, liên kết, nguồn và định nghĩa ngữ nghĩa.

**Ảnh Protégé có chứng minh reasoner đã chạy không?** Ảnh cây asserted/định nghĩa chỉ chứng minh khai báo. Muốn dùng ảnh inferred, phải ghi rõ reasoner và trạng thái/kết quả thật.
