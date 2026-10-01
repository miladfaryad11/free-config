# 🔥 PRX11 - Free Config Collector

این مخزن به‌طور خودکار و در بازه‌های زمانی منظم (هر ۶ ساعت)، کانفیگ‌های پروکسی رایگان از پروتکل‌های **VLESS**، **VMESS**، **Trojan**، **Shadowsocks** و **Fragment** را از منابع معتبر جمع‌آوری، پالایش و در قالب فایل‌های متنی آماده‌ی استفاده منتشر می‌کند.

---

## 📥 لینک‌های دانلود مستقیم (RAW)

| نوع پروتکل | فایل خروجی | لینک دانلود |
|------------|------------|-------------|
| **VLESS** | `prx11-vless.txt` | [🔗 دانلود](https://raw.githubusercontent.com/miladfaryad11/free-config/main/output/subscriptions/prx11-vless.txt) |
| **VMESS** | `prx11-vmess.txt` | [🔗 دانلود](https://raw.githubusercontent.com/miladfaryad11/free-config/main/output/subscriptions/prx11-vmess.txt) |
| **Trojan** | `prx11-trojan.txt` | [🔗 دانلود](https://raw.githubusercontent.com/miladfaryad11/free-config/main/output/subscriptions/prx11-trojan.txt) |
| **Shadowsocks** | `prx11-ss.txt` | [🔗 دانلود](https://raw.githubusercontent.com/miladfaryad11/free-config/main/output/subscriptions/prx11-ss.txt) |
| **Hiddify (بهینه‌شده)** | `prx11-hiddify.txt` | [🔗 دانلود](https://raw.githubusercontent.com/miladfaryad11/free-config/main/output/subscriptions/prx11-hiddify.txt) |
| **Fragment (اینستاگرام/یوتیوب)** | `prx11-insta-youto.txt` | [🔗 دانلود](https://raw.githubusercontent.com/miladfaryad11/free-config/main/output/subscriptions/prx11-insta-youto.txt) |
| **همه‌ی پروتکل‌ها (تلفیقی)** | `prx11-all.txt` | [🔗 دانلود](https://raw.githubusercontent.com/miladfaryad11/free-config/main/output/subscriptions/prx11-all.txt) |

---

## 📊 فایل‌های گزارش و اطلاعات

- **گزارش آماری** (`PRX11-LOGGER.json`):  
  شامل تعداد کانفیگ‌ها، توزیع کشورها، میانگین تأخیر و ۱۰ کشور سریع‌تر.  
  [📈 مشاهده](https://raw.githubusercontent.com/miladfaryad11/free-config/main/output/PRX11-LOGGER.json)

- **زمان آخرین به‌روزرسانی** (`AUTO_UPDATE.txt`):  
  تاریخ و ساعت آخرین اجرای موفق به‌وقت ایران.  
  [🕒 مشاهده](https://raw.githubusercontent.com/miladfaryad11/free-config/main/output/AUTO_UPDATE.txt)

---

## 🚀 نحوه‌ی استفاده در نرم‌افزارها

### ۱. اپلیکیشن‌های موبایل (Android / iOS)
- **V2RayNG / Nekobox / Hiddify / Streisand**:  
  لینک مربوط به پروتکل موردنظر را در قسمت **“اشتراک” (Subscription)** وارد کنید.  
  برنامه به‌صورت خودکار کانفیگ‌ها را دریافت و مرتباً به‌روز می‌کند.

- **Shadowsocks / Outline**:  
  از لینک `prx11-ss.txt` استفاده کنید (فرمت `ss://`).

### ۲. نرم‌افزارهای دسکتاپ (Windows / macOS / Linux)
- **V2RayN / Qv2ray / Clash Verge**:  
  لینک فایل موردنظر را به‌عنوان **“Remote Subscription”** اضافه کنید.

- **Clash / Sing-box**:  
  می‌توانید محتوای فایل `prx11-all.txt` را به‌عنوان لیست proxy-group استفاده کنید.

### ۳. مرورگرها (با افزونه‌های پروکسی)
- لینک `prx11-all.txt` را در ابزارهایی مانند **SwitchyOmega** یا **FoxyProxy** به‌صورت **PAC** یا **Proxy List** تنظیم کنید.

---

## 📌 نکات مهم

- **به‌روزرسانی خودکار**: این فایل‌ها هر **۶ ساعت** یکبار بازتولید می‌شوند. بنابراین همیشه جدیدترین کانفیگ‌ها در دسترس هستند.
- **نام‌گذاری استاندارد**: نام هر کانفیگ به‌صورت خودکار به قالب `PROTOCOL-کشور-تأخیر | host:port` تغییر می‌کند (مثلاً `VLESS-DE-120ms | example.com:443`) تا در کلاینت‌ها قابل‌تشخیص و مرتب باشد.
- **مرتب‌سازی**: همه‌ی پروتکل‌ها بر اساس امتیاز کیفیت (اولویت کشور + کمترین تأخیر) مرتب می‌شوند، نه فقط VLESS.
- **اعتبارسنجی**: کانفیگ‌های با میزبان/پورت/شناسه‌ی نامعتبر و کانفیگ‌های دارای کلیدواژه‌های مشکوک (free, fake, test, ...) حذف می‌شوند.
- **تست تأخیر واقعی**: تأخیر با اتصال TCP + TLS handshake واقعی اندازه‌گیری می‌شود، نه درخواست HTTP ساده.
- **تشخیص کشور**: میزبان ابتدا به‌صورت محلی resolve شده و سپس کشور آن با چند سرویس GeoIP (با fallback) تعیین می‌شود.
- **تعداد**: فایل Hiddify شامل **۱۰۰ کانفیگ برتر** است؛ سایر فایل‌ها همه‌ی کانفیگ‌های معتبر را دارند.

> ⚠️ **توجه درباره‌ی `prx11-insta-youto.txt`**: این فایل حاوی تنظیمات **Fragment** (برای دور زدن اختلال اینستاگرام/یوتیوب) است و **کانفیگ پروکسی نیست**؛ آن را به‌عنوان subscription معمولی اضافه نکنید.

---

## 📢 پشتیبانی و ارتباط

- **کانال تلگرام**: [@proxystore11](https://t.me/proxystore11)  
- **وب‌سایت**: [proxystore11.news](https://proxystore11.news)  
- **گزارش مشکل**: در بخش [Issues](https://github.com/miladfaryad11/free-config/issues) مخزن ثبت کنید.

---

## ⚠️ سلب مسئولیت

این کانفیگ‌ها صرفاً برای **آزمایش و توسعه** جمع‌آوری شده‌اند. استفاده از آن‌ها برای دور زدن تحریم‌ها یا نقض قوانین کشور محل سکونت، بر عهده‌ی خود کاربر است.  
ما هیچ‌گونه مسئولیتی در قبال عملکرد یا امنیت این کانفیگ‌ها نداریم.

---

**🔄 آخرین به‌روزرسانی:** (به‌طور خودکار در فایل `AUTO_UPDATE.txt` درج می‌شود)
