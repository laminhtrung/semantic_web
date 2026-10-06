# Kịch bản video 4 phút 16 giây

Video dùng giọng tiếng Việt tổng hợp Linh, slide và ảnh ứng dụng thật. Có thể dùng lời này để tự thuyết trình lại.

## 0:00–0:32 — MovieLOD

Bài làm này xây dựng Movie L O D, một ứng dụng dữ liệu phim liên kết. Mục tiêu là hoàn thành cả năm yêu cầu của đề, từ mô hình hóa, thu thập và chuyển đổi dữ liệu, đến liên kết ngoài và truy vấn. Thay vì mở rộng quá nhiều khái niệm, mô hình chỉ dùng chín lớp cần thiết. Chúng ta sẽ theo dõi một ví dụ quen thuộc: phim Inception và đạo diễn Christopher Nolan.

## 0:32–1:04 — YC1 · Ontology

Yêu cầu thứ nhất là định nghĩa mô hình cho lĩnh vực điện ảnh. Bài tái sử dụng trực tiếp ba lớp của DBpedia: Film cho phim, Person cho người và Country cho quốc gia. Sáu lớp của bài mô tả thể loại, ngôn ngữ, đóng góp, vai trò, nguồn và bộ dữ liệu. Mỗi bản ghi đóng góp nối đúng một phim, một người và một vai trò. Vì vậy, Nolan có thể làm đạo diễn và biên kịch trong cùng phim mà hai công việc vẫn được phân biệt rõ.

## 1:04–1:36 — YC2 · Dữ liệu thật, có nguồn

Yêu cầu thứ hai là thu thập dữ liệu thật. Danh sách chọn gồm ba mươi phim. Chương trình tải thông tin từ Wikidata và DBpedia. Danh tính được xác định bằng liên kết Wikipedia chính xác, thay vì đoán từ tên gần giống. Các phản hồi gốc được giữ nguyên, kèm địa chỉ nguồn, thời điểm lấy và mã băm. Mã băm giúp kiểm tra nội dung có bị thay đổi hay không. Bộ dữ liệu này là một mẫu phục vụ học tập, không phải toàn bộ điện ảnh.

## 1:36–2:08 — YC3 · Chuyển thành RDF

Yêu cầu thứ ba là chuyển thông tin thành dữ liệu liên kết. Mỗi câu có ba thành phần: chủ thể, quan hệ và đối tượng hoặc giá trị. Ví dụ, Inception có đạo diễn là Christopher Nolan. Mã nguồn tạo định danh ổn định từ mã thực thể, chuyển thời lượng về phút và thêm nguồn cho từng bản ghi. Dữ liệu được xuất theo các định dạng mở. Điều kiện bốn sao còn yêu cầu giấy phép mở và dữ liệu được công bố trên Web.

## 2:08–2:40 — YC4 · Liên kết ngoài

Yêu cầu thứ tư là nối dữ liệu với những bộ dữ liệu khác. Phim Inception trong ứng dụng được nối với mã thực thể tương ứng của Wikidata và DBpedia. Quan hệ same as khẳng định hai định danh chỉ cùng một thực thể, còn quan hệ nguồn nói thông tin được lấy từ đâu. Bài lưu biên bản cho từng liên kết để có thể kiểm tra phương pháp nối. Điều kiện năm sao được xây dựng trên điều kiện bốn sao đã đáp ứng.

## 2:40–3:12 — YC5 · Chạy truy vấn Inception

Đây là giao diện thật của ứng dụng. Bên trái là câu hỏi mẫu và ô nhập truy vấn. Bên phải là kết quả. Câu hỏi về Inception trả về tên phim, năm hai nghìn mười, thời lượng một trăm bốn mươi tám phút và Christopher Nolan. Người dùng có thể sửa câu truy vấn, chạy lại và tải kết quả. Khi chạy cục bộ, giao diện gọi dịch vụ truy vấn của ứng dụng. Bản hosted truy vấn bộ dữ liệu ngay trong trình duyệt.

## 3:12–3:44 — Demo · Phim của Nolan và tra cứu IRI

Thay câu hỏi mẫu sang các phim do Nolan đạo diễn, chúng ta nhận được bảng các phim trong bộ dữ liệu. Đây là kết quả truy vấn đồ thị của bài, không phải danh sách nhập cứng trong giao diện. Ngoài giao diện Web, bài có dịch vụ truy vấn và cách chạy ở terminal. Người dùng còn mở được định danh của một phim để xem thuộc tính, liên kết ngoài và nguồn. Mỗi trang có bản mô tả dữ liệu máy có thể đọc.

## 3:44–4:16 — Kiểm tra và sản phẩm nộp

Cuối cùng, bài có kiểm tra cấu trúc dữ liệu, kiểm tra toàn vẹn nguồn, tám truy vấn mẫu và tám bài kiểm tra tự động. Giao diện cũng được thử trên màn hình máy tính và điện thoại. Bộ nộp gồm mã, dữ liệu, báo cáo, slide và video này. Mọi kết quả kiểm tra được lưu để xem lại. Phần Open Data trên Web chỉ được xác nhận khi chủ sở hữu cho phép bản hosted truy cập công khai; trạng thái thực tế luôn được ghi trong biên bản xuất bản.
