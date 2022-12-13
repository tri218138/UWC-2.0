**Project UWC 2.0**  
Subject Công nghệ phần mềm
Description:  
Hệ thống quản trị cơ quan vệ sinh đô thị  


Để chạy được: trước tiên mn tải về môi trường này https://drive.google.com/file/d/1cACufcV_FWg6dOD017omQLEadkF_lf3v/view?usp=share_link -> giải nén -> để cùng cấp với file app.py  
Sau đó trên vscode, mn run file app.py như bình thường nha  

Mô tả:  
+File controller.py: xử lý điều hướng, post, get. Mỗi hàm sẽ có 1 cơ chế chung như sau: xác thực người dùng, gọi data, gửi data này cho view return.  
+File dbms.py: query theo yêu cầu của controller.  
+File view.py: render_template theo yêu cầu của controller.  

Ghi chú:  
-Những gì được post hay get thì do user nhấn button trong file html, button này sẽ submit (tức là gửi post request)   
-Flask nhận tín hiệu post request qua hàm: request.form. Nhưng để sử dụng thì ta chuyển về dictionary trong python: request.form.to_dict():  
+key là attribute 'name' trong html  
+value là attribute 'value' trong html  

**TODO** - bạn nào làm phần nào thì viết tên vô nhé, để tránh trùng  
Trang lịch công việc:  
[bạn 1] BO: xem tất cả  
[bạn 2] Janitor: xem bản thân mình (có thể trỏ đến MCP)  
[bạn 3] Collector: xem bản thân mình (có thể xem lộ trình)  
[bạn 4] Kênh chat. Do là thời gian có hạn nên mình dùng chung 1 kênh chat cho tất cả mn  
[ban 5] Kênh thông báo của MCP  
[Bạn 6] Trang thông tin cá nhân  
[bạn 7] Thêm MCP  

Tool:  
excel to json: https://codebeautify.org/excel-to-json  
collect mcp: https://www.google.com/maps/d/u/1/edit?mid=11aL88Ezni6YK0BCSb-0COg1vMA3ssK4&ll=10.881486763825414%2C106.80721780054947&z=15  