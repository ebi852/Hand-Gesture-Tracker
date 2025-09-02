# Hand-Gesture-Tracker
A simple Python suite demonstrating real-time hand gesture detection and control
Note: This suite is tested on Linux only. It is not guaranteed to work on Windows or macOS.



یک مجموعه ساده و کاربردی از پروژه‌های Python برای **تشخیص و ردیابی حرکات دست** با استفاده از OpenCV و Mediapipe.

## پروژه‌ها
##Projects

- **تشخیص انگشت شست (Thumb Tracker):**  
  تشخیص دقیق موقعیت انگشت شست در تصویر زنده و نمایش آن به صورت گرافیکی.
  Thumb Tracker:Accurately detects the thumb tip position in a live webcam feed and visually highlights it.

- **کنترل اسکرول با انگشت وسط (Scroll with Middle Finger):**  
  کنترل حرکت اسکرول صفحه با حرکت عمودی انگشت وسط نسبت به انگشت اشاره، جایگزین روش‌های معمول.
  Scroll with Middle Finger:Scrolls the screen up and down based on the vertical movement of the middle finger relative to the index finger.

- **تشخیص حرکت انگشت اشاره نسبت به شست (Index vs Thumb Movement):**  
  بررسی موقعیت نسبی عمودی انگشت اشاره نسبت به انگشت شست و نمایش جهت حرکت.
  Index vs Thumb Movement:Compares the relative vertical position of the index finger to the thumb and displays the movement direction.

-**تغییر موس و قابلیت کلیک کردن (Mouse Control & Clicking):**

این نسخه امکان کنترل مکان‌نما (Mouse Cursor) و انجام کلیک را فراهم می‌کند.  

Mouse Control & Clicking**: Allows controlling the cursor position and performing mouse clicks.


## ابزارها
##Tools

- Python  
- OpenCV  
- Mediapipe  
-OS (built-in)
-RE (built-in)
-Subprocess (built-in)
-Collections (deque, built-in)

## نصب
##Installation

ابتدا مطمئن شوید که پایتون و pip نصب شده است. سپس وابستگی‌ها را نصب کنید:
Make sure Python and pip are installed, then install dependencies:

```bash
pip install mediapipe opencv-python

