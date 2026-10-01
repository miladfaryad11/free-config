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
- **نام‌گذاری قابل‌تنظیم**: نام نمایشی هر کانفیگ از قالب قابل‌ویرایش ساخته می‌شود و شامل **نام کانال + پرچم کشور + پروتکل + تأخیر** است؛ مثلاً `PRX11 | @proxystore11 🇩🇪 VLESS 120ms`. جزئیات تنظیم در بخش [⚙️ تنظیم نام کانفیگ‌ها](#️-تنظیم-نام-کانفیگها) آمده است.
- **مرتب‌سازی**: همه‌ی پروتکل‌ها بر اساس امتیاز کیفیت (اولویت کشور + کمترین تأخیر) مرتب می‌شوند، نه فقط VLESS.
- **اعتبارسنجی**: کانفیگ‌های با میزبان/پورت/شناسه‌ی نامعتبر و کانفیگ‌های دارای کلیدواژه‌های مشکوک (free, fake, test, ...) حذف می‌شوند.
- **تست تأخیر واقعی**: تأخیر با اتصال TCP + TLS handshake واقعی اندازه‌گیری می‌شود، نه درخواست HTTP ساده.
- **تشخیص کشور**: میزبان ابتدا به‌صورت محلی resolve شده و سپس کشور آن با چند سرویس GeoIP (با fallback) تعیین می‌شود.
- **تعداد**: هر فایل پروتکل حداکثر **۱۰۰۰ کانفیگ** دارد؛ فایل «همه» (`prx11-all.txt`) بدون محدودیت است.
- **تنوع کشوری در Hiddify**: فایل Hiddify شامل **۲۰۰ کانفیگ** است که به‌طور متوازن بین کشورهای محبوب (آلمان، هلند، فرانسه، ترکیه، امارات، آمریکا و…) تقسیم می‌شود تا همه‌ی کانفیگ‌ها از یک کشور نباشند.

> ⚠️ **توجه درباره‌ی `prx11-insta-youto.txt`**: این فایل حاوی تنظیمات **Fragment** (برای دور زدن اختلال اینستاگرام/یوتیوب) است و **کانفیگ پروکسی نیست**؛ آن را به‌عنوان subscription معمولی اضافه نکنید.

---

## ⚙️ تنظیم نام کانفیگ‌ها

نام نمایشی هر کانفیگ از متغیرهای داخل `main.py` ساخته می‌شود. برای تغییر آن، فقط بخش تنظیمات بالای فایل را ویرایش کنید:

```python
# نام کانال/برند شما
CHANNEL_NAME = "PRX11 | @proxystore11"

# قالب نام نمایشی
NAME_TEMPLATE = "{channel} {flag} {protocol} {latency}"

# نمایش تأخیر در نام (True/False)
SHOW_LATENCY_IN_NAME = True
```

### متغیرهای قابل استفاده در `NAME_TEMPLATE`

| متغیر | توضیح | نمونه |
|-------|-------|-------|
| `{channel}` | نام کانال (`CHANNEL_NAME`) | `PRX11 \| @proxystore11` |
| `{flag}` | پرچم ایموجی کشور | `🇩🇪` |
| `{country}` | کد دو حرفی کشور | `DE` |
| `{protocol}` | نام پروتکل | `VLESS` |
| `{latency}` | تأخیر (در صورت نامشخص بودن حذف می‌شود) | `120ms` |
| `{host}` | میزبان سرور | `example.com` |
| `{port}` | پورت سرور | `443` |
| `{index}` | شماره‌ی ترتیب | `1` |

### نمونه قالب‌ها

```python
# پیش‌فرض: کانال + پرچم + پروتکل + تأخیر
NAME_TEMPLATE = "{channel} {flag} {protocol} {latency}"
# → PRX11 | @proxystore11 🇩🇪 VLESS 120ms

# با نام کانال در ابتدا و جزئیات کامل
NAME_TEMPLATE = "{channel} | {flag} {country} {protocol} | {latency} | {host}:{port}"
# → PRX11 | @proxystore11 | 🇩🇪 DE VLESS | 120ms | example.com:443

# فقط پرچم و پروتکل
NAME_TEMPLATE = "{flag} {protocol}"
# → 🇩🇪 VLESS
```

> اگر کشوری شناسایی نشود، پرچم سفید (`🏳️`) و کد `XX` نمایش داده می‌شود. برای افزودن پرچم دستی یک کشور، آن را در دیکشنری `COUNTRY_FLAGS` اضافه کنید (برای سایر کدها به‌صورت خودکار ساخته می‌شود).

---

## 📦 تنظیم تعداد و تنوع کانفیگ‌ها

تعداد کانفیگ‌های هر فایل و تنوع کشوری فایل Hiddify از بالای `main.py` قابل تنظیم است:

```python
# حداکثر کانفیگ در هر فایل پروتکل (فایل «همه» محدودیتی ندارد)
MAX_PER_FILE = 1000

# تعداد کانفیگ فایل Hiddify
HIDDIFY_LIMIT = 200

# کشورهای محبوب برای تقسیم متوازن در Hiddify
POPULAR_COUNTRIES = ["DE", "NL", "FR", "TR", "AE", "US", "GB", ...]

# سهمیه‌ی هر کشور در Hiddify (۰ = بی‌نهایت)
HIDDIFY_PER_COUNTRY = 0
```

- **`MAX_PER_FILE`**: هر فایل پروتکل (VLESS/VMESS/Trojan/SS) به این تعداد محدود می‌شود. فایل تلفیقی `prx11-all.txt` بدون محدودیت می‌ماند.
- **`HIDDIFY_LIMIT`**: تعداد کل کانفیگ‌های فایل Hiddify.
- **`POPULAR_COUNTRIES`**: کانفیگ‌های Hiddify به‌نوبت (round-robin) از این کشورها انتخاب می‌شوند تا خروجی متنوع بماند.
- **`HIDDIFY_PER_COUNTRY`**: اگر بزرگ‌تر از صفر باشد، حداکثر این تعداد کانفیگ از هر کشور برداشته می‌شود.

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
