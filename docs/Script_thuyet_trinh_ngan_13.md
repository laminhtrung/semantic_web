---
title: "MovieLOD: lời thuyết trình riêng cho 13 slide"
date: "MovieLOD 2.0 · Đối chiếu ngày 08/10/2026"
---

## Cách dùng

Lời nói riêng cho đúng **13 slide** trong `Slide_ngan_13.pptx`; toàn bộ lời cũng nằm trong Speaker Notes. Thời lượng gợi ý **12–14 phút**, khác video demo 4 phút 50 giây. Nói khoảng 150–175 từ/phút và điều chỉnh theo buổi bảo vệ. Điền tên thành viên/lớp trên slide 1; phân công người nói trước khi tập. Các đoạn là mẫu lời đọc hoàn chỉnh, có thể rút gọn bằng cách bỏ ví dụ phụ nhưng giữ kết luận và giới hạn.

| Slide | Người nói gợi ý | Thời lượng |
|:--|:--|:--|
| 01 — MovieLOD | Thành viên A | 45–70 giây |
| 02 — Từ câu hỏi điện ảnh đến 5 yêu cầu | Thành viên A | 45–70 giây |
| 03 — Kiến trúc: nguồn → đồ thị → ứng dụng | Thành viên A | 45–70 giây |
| 04 — YC1 · Mô hình điện ảnh với 42 lớp | Thành viên A | 45–70 giây |
| 05 — YC1 · Ai làm gì trong phim nào? | Thành viên A | 45–70 giây |
| 06 — YC2 · Thu thập thật, truy lại được nguồn | Thành viên B | 45–70 giây |
| 07 — YC3 · Từ dữ liệu nguồn thành RDF | Thành viên B | 45–70 giây |
| 08 — YC4 · Nối đúng danh tính ra Web dữ liệu | Thành viên B | 45–70 giây |
| 09 — YC5 · Truy vấn Inception trên ứng dụng | Thành viên B | 45–70 giây |
| 10 — YC5 · Endpoint, terminal và tra cứu IRI | Thành viên C | 45–70 giây |
| 11 — Điểm Semantic Web: dữ kiện → kiến thức mới | Thành viên C | 45–70 giây |
| 12 — Đối chiếu đề: 10/10 theo thang tự đánh giá | Thành viên C | 45–70 giây |
| 13 — Hoàn thiện bản nộp và kết luận | Thành viên C | 45–70 giây |

## Slide 01 — MovieLOD

**Chỉ trên màn hình:** các thông tin chính theo thứ tự từ trái sang phải / trên xuống dưới.

**Lời nói:**

Chào thầy cô và các bạn. Nhóm chúng em trình bày MovieLOD, ứng dụng dữ liệu mở có liên kết về điện ảnh. Bài đi qua năm yêu cầu: xây dựng ontology, thu thập dữ liệu, chuyển thành RDF, liên kết với dữ liệu bên ngoài và cung cấp giao diện SPARQL. Phiên bản cục bộ hiện có ba mươi phim, bốn mươi hai lớp và một nghìn bảy trăm hai mươi bảy liên kết ngoài. Ví dụ xuyên suốt là Inception và Christopher Nolan. Các số liệu trên slide được đối chiếu với dữ liệu hiện tại ngày tám tháng mười năm hai nghìn không trăm hai mươi sáu. Tên thành viên và lớp học có thể điền ở trang bìa trước khi nộp.

**Chuyển trang:** Sau đây nhóm chuyển sang từ câu hỏi điện ảnh đến 5 yêu cầu.

## Slide 02 — Từ câu hỏi điện ảnh đến 5 yêu cầu

**Chỉ trên màn hình:** các thông tin chính theo thứ tự từ trái sang phải / trên xuống dưới.

**Lời nói:**

Nhóm chọn điện ảnh vì một phim liên quan đến nhiều người, thể loại, giải thưởng và công ty sản xuất. Người dùng muốn hỏi Inception do ai đạo diễn, Nolan tham gia phim nào hoặc dữ liệu này được lấy từ đâu. Năm yêu cầu của đề tương ứng với năm lớp công việc trên màn hình. Ontology quy định ý nghĩa của dữ liệu; chương trình thu thập lấy thông tin thật; bước chuyển đổi tạo RDF và định danh; bước liên kết nối với Wikidata và DBpedia; SPARQL cho phép đặt câu hỏi trên đồ thị. Đề còn yêu cầu báo cáo không quá mười lăm trang và video dài ba đến năm phút. Bộ slide và lời nói này dành cho phần thuyết trình, còn kịch bản quay demo được tách riêng để giữ đúng thời lượng.

**Chuyển trang:** Sau đây nhóm chuyển sang kiến trúc: nguồn → đồ thị → ứng dụng.

## Slide 03 — Kiến trúc: nguồn → đồ thị → ứng dụng

**Chỉ trên màn hình:** các thông tin chính theo thứ tự từ trái sang phải / trên xuống dưới.

**Lời nói:**

Luồng xử lý bắt đầu bằng danh sách phim trong config. Chương trình thu thập lấy phản hồi từ Wikidata và DBpedia, ghi URL, thời điểm và SHA hai trăm năm mươi sáu. Chương trình build tạo ontology và dữ liệu RDF từ bản chuẩn hóa đã có. Bộ kiểm tra xem tên phim, nguồn và các thành phần đóng góp có hợp lệ trong phạm vi ứng dụng hay không. Bước reason tạo các kiểu phân loại bổ sung ở một file riêng. Web cục bộ gọi endpoint Flask dùng RDFLib; chế độ trình duyệt dùng Comunica để đọc RDF. Terminal có tùy chọn reasoned để nạp thêm lược đồ và kết quả phân loại. Vì vậy câu truy vấn cần suy luận không nên chạy trực tiếp trên endpoint mặc định rồi kết luận dữ liệu bị mất.

**Chuyển trang:** Sau đây nhóm chuyển sang yc1 · mô hình điện ảnh với 42 lớp.

## Slide 04 — YC1 · Mô hình điện ảnh với 42 lớp

**Chỉ trên màn hình:** các thông tin chính theo thứ tự từ trái sang phải / trên xuống dưới.

**Lời nói:**

Ontology có bốn mươi hai lớp có tên được khai báo bằng owl Class. Ba lớp Film, Person và Country dùng trực tiếp IRI của DBpedia; việc này khác với liên kết sameAs giữa các cá thể. CreativeWork là nhánh tác phẩm, Agent là nhánh người và tổ chức. Contribution biểu diễn công việc một người làm cho một phim. Các nhánh Genre và Award hỗ trợ câu hỏi về thể loại và giải thưởng. Trong bốn mươi hai lớp có mười bốn lớp được phân loại từ định nghĩa, chẳng hạn Actor, Filmmaker hoặc ActionFilm. Sơ đồ trên slide chỉ hiển thị các nhánh chính để dễ đọc; bảng đủ bốn mươi hai lớp nằm trong tài liệu ontology. Số lớp là số trong lược đồ, không phải số cá thể và cũng không phải số nút mà Protégé hiển thị.

**Chuyển trang:** Sau đây nhóm chuyển sang yc1 · ai làm gì trong phim nào?.

## Slide 05 — YC1 · Ai làm gì trong phim nào?

**Chỉ trên màn hình:** sơ đồ Contribution và bốn vai trò.

**Lời nói:**

Nếu chỉ gắn một nhãn nghề nghiệp cho một người, chúng ta không biết người đó giữ vai trò nào trong từng phim. Mô hình Contribution giải quyết bằng một bản ghi nối một người, một phim và một vai trò. Nolan có thể vừa đạo diễn vừa biên kịch; hai vai trò được ghi thành hai đóng góp riêng. Bốn vai trò hiện có là đạo diễn, diễn viên, biên kịch và nhà sản xuất. Các quan hệ contributionBy, contributionTo và hasRole có domain, range, tính functional và ràng buộc số lượng. Quan hệ ngược cho phép đi từ người đến đóng góp và từ phim đến đóng góp. Cardinality của OWL là phát biểu ngữ nghĩa trong giả định thế giới mở; nó không tự thay thế kiểm tra biểu mẫu. Vì vậy ứng dụng có thêm kiểm tra Python để phát hiện một đóng góp thiếu người hoặc có nhiều vai trò.

**Chuyển trang:** Sau đây nhóm chuyển sang yc2 · thu thập thật, truy lại được nguồn.

## Slide 06 — YC2 · Thu thập thật, truy lại được nguồn

**Chỉ trên màn hình:** các thông tin chính theo thứ tự từ trái sang phải / trên xuống dưới.

**Lời nói:**

Danh sách ba mươi phim được chọn có chủ đích cho bài học. Từ các phim này, dữ liệu hiện có tám trăm năm mươi mốt người, một nghìn không trăm mười đóng góp, bốn mươi lăm công ty sản xuất và sáu trăm bảy mươi hai thực thể giải thưởng. Wikidata cung cấp phát biểu về đạo diễn, diễn viên, biên kịch, nhà sản xuất, giải thưởng và công ty. Danh tính phim được xác định qua sitelink Wikipedia tiếng Anh chính xác. DBpedia chỉ được nối khi đúng chủ thể và có kiểu Film. Hiện đủ bảy mươi sáu phản hồi gốc và cả bảy mươi sáu đều khớp mã băm. Bốn mươi ba file từng thiếu đã được bổ sung. Một phản hồi tải lại có nội dung thay đổi được ghi thời điểm và hash mới; danh mục cũ được giữ để đối chiếu. Nhóm đã chạy lại thu thập từ cache nguồn đầy đủ, tạo RDF và kiểm tra. SHA chứng minh nội dung khớp với mốc lưu, không chứng minh mọi phát biểu ngoài đời đều đúng.

**Chuyển trang:** Sau đây nhóm chuyển sang yc3 · từ dữ liệu nguồn thành rdf.

## Slide 07 — YC3 · Từ dữ liệu nguồn thành RDF

**Chỉ trên màn hình:** các thông tin chính theo thứ tự từ trái sang phải / trên xuống dưới.

**Lời nói:**

RDF biểu diễn dữ liệu bằng các bộ ba. Chủ thể là Inception, quan hệ là director và đối tượng là Christopher Nolan. Một bộ ba khác có thể nối phim với giá trị năm hai nghìn mười hoặc thời lượng một trăm bốn mươi tám phút. Định danh nội bộ dùng QID để giảm nhầm lẫn giữa các tên giống nhau. Dữ liệu được xuất thành Turtle và JSON LD; ontology có bản OWL để mở bằng Protégé. Bộ dữ liệu hiện có mười chín nghìn ba trăm ba mươi chín triple, tách khỏi năm trăm mười tám triple lược đồ. Dữ liệu có giấy phép CC BY SA bốn chấm không và định danh HTTP. Điều kiện bốn sao cần dữ liệu công khai trên Web, có giấy phép mở và IRI cung cấp thông tin hữu ích. Nhóm đã triển khai lại bản hai chấm không và kiểm tra các URL không đăng nhập. Graph Turtle, JSON LD, ontology và mô tả Inception đều đẳng cấu với bản cục bộ. Đây là bằng chứng công bố của bản hiện tại, khác việc chỉ có file RDF trong máy.

**Chuyển trang:** Sau đây nhóm chuyển sang yc4 · nối đúng danh tính ra web dữ liệu.

## Slide 08 — YC4 · Nối đúng danh tính ra Web dữ liệu

**Chỉ trên màn hình:** các thông tin chính theo thứ tự từ trái sang phải / trên xuống dưới.

**Lời nói:**

Một thực thể có thể mang nhiều định danh trong các bộ dữ liệu khác nhau. Với Inception, đồ thị nội bộ nối tới Wikidata Q hai năm một tám tám và tài nguyên Inception của DBpedia bằng owl sameAs. Bài có một nghìn sáu trăm chín mươi chín liên kết Wikidata và hai mươi tám liên kết DBpedia. Không phải cả ba mươi phim đều được nối DBpedia, vì kiểm tra danh tính không chấp nhận mọi phản hồi. sameAs là khẳng định hai IRI cùng chỉ một thực thể, mạnh hơn một liên kết xem thêm. sourceSnapshot là quan hệ về xuất xứ, nói dữ liệu được lấy ở phản hồi nào. Truy vấn liên kết theo từng phim trả năm mươi tám dòng, còn một nghìn bảy trăm hai mươi bảy là tổng trên tất cả loại thực thể. Mức năm sao cần cả điều kiện bốn sao và liên kết ngoài; số lượng liên kết tự nó không chứng minh công bố. Trong bản hiện tại, các kiểm tra HTTP và graph đã xác nhận dữ liệu công khai khớp local.

**Chuyển trang:** Sau đây nhóm chuyển sang yc5 · truy vấn inception trên ứng dụng.

## Slide 09 — YC5 · Truy vấn Inception trên ứng dụng

**Chỉ trên màn hình:** ảnh Inception và bảng kết quả.

**Lời nói:**

Đây là ảnh giao diện ứng dụng thật được kiểm tra lại. Người dùng chọn câu hỏi mẫu hoặc sửa SPARQL trong ô nhập, rồi chạy để xem bảng kết quả. Truy vấn Inception trả tên phim, năm hai nghìn mười, một trăm bốn mươi tám phút và Christopher Nolan. Câu hỏi các phim Nolan đạo diễn trả tám dòng trong bộ dữ liệu này. Câu hỏi đóng góp trả hai mươi lăm dòng và có bốn loại vai trò. Giao diện có câu hỏi trực tiếp về diễn viên, công ty, giải thưởng và nguồn. Ngoài SELECT trả bảng, ASK trả đúng hoặc sai, còn CONSTRUCT tạo một đồ thị RDF. Kết quả được tính từ dữ liệu; danh sách phim Nolan không được nhập cứng vào bảng. Khi quay demo, nhóm sẽ chuyển qua nhiều câu hỏi và mở trang Inception để chỉ rõ liên kết ngoài và thông tin nguồn.

**Chuyển trang:** Sau đây nhóm chuyển sang yc5 · endpoint, terminal và tra cứu iri.

## Slide 10 — YC5 · Endpoint, terminal và tra cứu IRI

**Chỉ trên màn hình:** các thông tin chính theo thứ tự từ trái sang phải / trên xuống dưới.

**Lời nói:**

Đề yêu cầu một giao diện qua endpoint hoặc terminal; bài có cả hai và thêm Web. Endpoint cục bộ hỗ trợ GET và POST. SELECT và ASK trả JSON theo SPARQL Results, CONSTRUCT và DESCRIBE trả Turtle. Terminal đọc câu truy vấn từ file và in kết quả, thuận tiện để tái lập. Khi mở IRI Inception bằng trình duyệt, người dùng nhận mô tả HTML. Khi gửi Accept text turtle tới máy chủ cục bộ, phản hồi chuyển hướng ba trăm linh ba đến bản RDF của thực thể. Hai mươi bốn file truy vấn chia thành nhóm trực tiếp, theo cây lớp và cần kết quả suy luận. Giao diện mẫu có mười bốn câu chạy trên dữ liệu khai báo. Endpoint mặc định không nạp các lớp suy luận; phần đó được trình diễn riêng qua terminal với tùy chọn reasoned. Bản hosted dùng Comunica trong trình duyệt, nên không gọi nó là endpoint Python công khai.

**Chuyển trang:** Sau đây nhóm chuyển sang điểm semantic web: dữ kiện → kiến thức mới.

## Slide 11 — Điểm Semantic Web: dữ kiện → kiến thức mới

**Chỉ trên màn hình:** các thông tin chính theo thứ tự từ trái sang phải / trên xuống dưới.

**Lời nói:**

Điểm đáng chú ý của Semantic Web là định nghĩa lớp cho phép phân loại từ các quan hệ đã có. Dữ liệu gốc chỉ khai báo Nolan thuộc Person. Đóng góp có DirectorRole được phân loại DirectingContribution; người có loại đóng góp đó được phân loại Filmmaker. Tương tự, người có đóng góp diễn xuất được phân loại Actor. Mười hai lớp được xử lý bằng luật OWL RL trong thư viện owlrl. Hai lớp MultiGenreFilm và FilmStudio được tính bổ sung bằng COUNT DISTINCT vì các ngưỡng hai và ba không được bộ luật này xử lý theo cách cần dùng. Đây là quy tắc đếm IRI của ứng dụng, chưa phải bằng chứng phân loại OWL DL đầy đủ; IRI khác nhau không tự đảm bảo cá thể khác nhau trong OWL. Lệnh reasoned nạp lược đồ và file phân loại đã lưu. Kết quả có bảy trăm sáu mươi chín Actor, tám mươi chín Filmmaker và mười hai ActionFilm; truy vấn mẫu Actor và Filmmaker chỉ hiện hai mươi dòng do LIMIT.

**Chuyển trang:** Sau đây nhóm chuyển sang đối chiếu đề: 10/10 theo thang tự đánh giá.

## Slide 12 — Đối chiếu đề: 10/10 theo thang tự đánh giá

**Chỉ trên màn hình:** các thông tin chính theo thứ tự từ trái sang phải / trên xuống dưới.

**Lời nói:**

Ảnh đề gốc không quy định trọng số. Nhóm dùng thang tự đánh giá chia đều hai điểm cho mỗi yêu cầu và dẫn minh chứng cho từng mục. Sau lần sửa, bảy mươi sáu phản hồi gốc đều có và khớp hash; quy trình thu thập từ cache, build, validate và suy luận đã chạy lại. Website được xuất bản với mô hình hai chấm không; các graph RDF công khai đẳng cấu với bản cục bộ. Các liên kết ngoài được kiểm kê và truy vấn. Mười ba test và chín kiểm tra trình duyệt đều đạt. Vì vậy cả năm yêu cầu được đề xuất hai điểm, tổng mười trên mười theo thang này. Đây là tự đánh giá kỹ thuật trong phạm vi đã kiểm tra, không phải điểm chính thức hoặc cam kết của giảng viên. Các giới hạn mô hình và phương pháp suy luận vẫn được trình bày trung thực.

**Chuyển trang:** Sau đây nhóm chuyển sang hoàn thiện bản nộp và kết luận.

## Slide 13 — Hoàn thiện bản nộp và kết luận

**Chỉ trên màn hình:** các thông tin chính theo thứ tự từ trái sang phải / trên xuống dưới.

**Lời nói:**

MovieLOD đã có quy trình từ nguồn thật đến ontology, RDF, liên kết ngoài và ba cách truy vấn. Các lỗi làm mất điểm đã được sửa: phản hồi nguồn đầy đủ, hash được kiểm tra và bản công khai đồng bộ với dữ liệu nộp. Video mới ghi thao tác ứng dụng và các kết quả lệnh thật trên mô hình hai chấm không, có lời tiếng Việt tổng hợp; nhóm có thể tự đọc lại theo kịch bản. Bộ nộp gồm báo cáo trong giới hạn mười lăm trang, mười ba slide, lời thuyết trình riêng, video ba đến năm phút và mã/dữ liệu/biên bản. Hạn chế còn lại là mẫu ba mươi phim có chủ đích, một số nhóm được ánh xạ theo nhãn và chưa chứng minh tính nhất quán bằng reasoner OWL DL đầy đủ. Nhóm xin kết thúc và sẵn sàng nhận câu hỏi.

**Chuyển trang:** Nhóm xin mời thầy cô đặt câu hỏi.

## Câu hỏi bảo vệ và lời đáp ngắn

**Vì sao 42 lớp nhưng slide chỉ có vài nhánh?** Số 42 đếm các IRI khai báo owl:Class; slide tóm tắt nhánh chính. Bảng đủ ở Ontology_Redesign.md.

**Tái dùng lớp khác gì sameAs?** dbo:Film dùng từ vựng chung; sameAs nối cá thể có cùng danh tính.

**Nolan vừa đạo diễn vừa biên kịch có mâu thuẫn không?** Không. Hai vai trò có các Contribution riêng; Actor và Filmmaker không được khai báo disjoint.

**OWL exact cardinality có bảo đảm dữ liệu đủ trường?** Không theo cơ chế kiểm tra biểu mẫu. Python kiểm tra trường bắt buộc; OWL dùng ngữ nghĩa thế giới mở.

**COUNT DISTINCT có bằng reasoner DL không?** Không. Đếm IRI là quy tắc ứng dụng; OWL không mặc định hai IRI khác nhau là hai cá thể khác nhau. Chưa chạy chứng minh DL đầy đủ.

**Căn cứ đề xuất 10/10 là gì?** Đủ 76 nguồn và hash khớp; graph public đẳng cấu local; ontology, liên kết và truy vấn có minh chứng. Dùng thang tự chia đều, không phải điểm giảng viên.

**Rỗng khi hỏi Filmmaker trên endpoint có phải lỗi?** Endpoint chỉ nạp graph khai báo; dùng terminal --reasoned để nạp schema và file phân loại.

**CSDL quan hệ có trả các câu hỏi này được không?** Có thể dùng JOIN, view hoặc quy tắc ứng dụng. Điểm của RDF/OWL là IRI chung, từ vựng tái dùng, liên kết giữa dataset và định nghĩa lớp máy có thể xử lý; không nói SQL không làm được.

**13 test pass có nghĩa toàn bộ nguồn đúng không?** Không. Test kiểm tra hành vi cụ thể; hash nguồn kiểm tra toàn vẹn. Cả hai không chứng minh mọi phát biểu ngoài đời đúng.

**Video hiện có có thể nộp không?** Video đã cập nhật bản 2.0, ghi thao tác thật và kết quả lệnh, có giọng tổng hợp Linh. Nhóm cần xem lại trước khi nộp và có thể đọc lại bằng giọng thành viên.

## Cập nhật sau lần ghi video và tạo slide ngắn

Bản chính hiện có 24 slide và 14 test pass. Movie_Knowledge_Graph.owl đã đồng bộ timestamp đến mili giây với Turtle/JSON-LD/Web và chạy được HermiT/Pellet. Hai reasoner xác nhận nhất quán; 12 lớp khớp OWL RL; MultiGenreFilm/FilmStudio có 0 cá thể suy luận DL, khác số đếm ứng dụng 30/6. Các lời mô tả chưa chạy reasoner trong bản ngắn là lịch sử; khi trình bày hiện tại dùng Script_thuyet_trinh.pdf và Ket_qua_reasoner.pdf. Video và slide ngắn giữ nguyên.
