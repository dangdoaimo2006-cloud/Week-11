# Lab 11 - Campus Safety Hub

**Sinh viên:** Nguyễn Hải Đăng  
**MSSV:** 202418863

Chương trình console mô phỏng giám sát khói trong phòng máy. Hệ thống chuyển đổi cảm biến cũ sang giao diện cảm biến chung, phát cảnh báo cho nhiều observer và điều phối thiết bị khẩn cấp khi có mức khói nghiêm trọng.

## Chức năng

- `SmokeSensorAdapter` đọc `LegacySmokeDetector` theo giao diện `ISensor` và đổi mức 0-1000 sang phần trăm.
- `SensorMonitor` đọc cảm biến, phân loại mức khói và thông báo cho các observer đã đăng ký.
- `DashboardObserver`, `EmailAlertObserver` và `AuditLogObserver` hiển thị hoặc ghi nhận cảnh báo giả lập.
- `EmergencyBridgeObserver` chuyển cảnh báo CRITICAL đến `EmergencyMediator`.
- `EmergencyMediator` điều phối còi báo động, cửa thoát hiểm và thông gió.

## Cấu trúc

```text
Week 11/
├── main.py
├── src/
│   ├── sensor.py
│   ├── legacy_smoke_detector.py
│   ├── smoke_sensor_adapter.py
│   ├── alert_event.py
│   ├── observers.py
│   ├── sensor_monitor.py
│   ├── emergency_bridge_observer.py
│   ├── emergency_mediator.py
│   └── emergency_devices.py
└── tests/
    ├── test_adapter.py
    ├── test_observer.py
    ├── test_emergency_mediator.py
    └── test_campus_safety.py
```

## Chạy chương trình

Yêu cầu Python 3.10 trở lên, không cần cài package ngoài.

```bash
python main.py
```

Chạy kiểm thử:

```bash
python -m unittest discover -s tests -v
```

## Ngưỡng và luồng xử lý

| Mức khói | Kết quả |
|---|---|
| Dưới 50% | Bình thường, không phát cảnh báo |
| Từ 50% đến dưới 70% | `WARNING`, gửi đến các observer |
| Từ 70% trở lên | `CRITICAL`, gửi cảnh báo và kích hoạt còi, mở cửa thoát hiểm, bật thông gió |

`AlertEvent` là đối tượng bất biến. `SensorMonitor` không đăng ký trùng một observer, cho phép hủy đăng ký, thông báo trên bản sao danh sách và ghi log nếu một observer bị lỗi để các observer còn lại vẫn nhận cảnh báo.

## Câu hỏi thiết kế

1. **Adapter nên kế thừa hay chứa `LegacySmokeDetector`?**  
   Adapter nên **chứa** đối tượng cũ (composition). Adapter chỉ chuyển đổi API và đơn vị đo; kế thừa sẽ gắn chặt vào chi tiết triển khai của cảm biến cũ và không cần thiết để chuyển đổi giao diện. Cách chứa cũng giúp giữ nguyên lớp cũ và đọc trạng thái hiện tại của nó.

2. **`SensorMonitor` có nên biết `EmailAlertObserver` cụ thể không?**  
   Không. Monitor chỉ nên phụ thuộc vào hợp đồng `IAlertObserver`. Nhờ vậy có thể thêm, gỡ hoặc thay observer mà không sửa logic giám sát; email trong bài chỉ là một cách nhận cảnh báo.

3. **Alarm có cần tham chiếu trực tiếp đến `DoorController` không?**  
   Không. Các thiết bị không nên điều khiển hoặc giữ tham chiếu trực tiếp lẫn nhau. `EmergencyMediator` nhận cảnh báo rồi gọi alarm, cửa và thông gió theo một luồng thống nhất, giảm phụ thuộc giữa các thiết bị.

4. **Ai quyết định giá trị nào vượt ngưỡng?**  
   Trong phiên bản này, `SensorMonitor` chịu trách nhiệm so sánh giá trị cảm biến với ngưỡng 50% và 70%, vì đây là nơi đọc cảm biến và quyết định có phát sự kiện hay không. Adapter chỉ đổi giao diện/đơn vị; observer chỉ nhận và xử lý sự kiện. Nếu quy tắc ngưỡng thay đổi thường xuyên, có thể tách phần so ngưỡng thành một policy riêng.

Mã nguồn: [GitHub - Week-11](https://github.com/dangdoaimo2006-cloud/Week-11).
