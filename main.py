#!/usr/bin/env python3
import asyncio
import aiohttp
import base64
import json
import os
import re
import socket
import statistics
import time
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Optional, Dict, List, Tuple
from urllib.parse import unquote

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SOURCES_FILE = os.path.join(BASE_DIR, "sources.json")
CHANNELS_FILE = os.path.join(BASE_DIR, "channels.json")
OUTPUT_DIR = os.path.join(BASE_DIR, "output/subscriptions")
LOGGER_FILE = os.path.join(BASE_DIR, "output/PRX11-LOGGER.json")
AUTO_UPDATE_FILE = os.path.join(BASE_DIR, "output/AUTO_UPDATE.txt")

ENABLE_GEOIP = True
ENABLE_LATENCY = True
MAX_ENRICH_GEOIP = 6000
MAX_ENRICH_LATENCY = 3000
GEOIP_CONCURRENCY = 12
LATENCY_CONCURRENCY = 60
FETCH_CONCURRENCY = 10
FETCH_RETRIES = 3
LATENCY_TIMEOUT = 4.0
DNS_TIMEOUT = 3.0

GEOIP_PROVIDERS = [
    ("https://ipinfo.io/{ip}/json", ("country",)),
    ("https://api.ip2location.io/?ip={ip}", ("country_code",)),
    ("https://api.country.is/{ip}", ("country",)),
]

USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/125.0 Safari/537.36"
)

CHANNEL_NAME = "PRX11 | @proxystore11"
NAME_TEMPLATE = "{channel} {flag} {protocol} {latency}"
SHOW_LATENCY_IN_NAME = True

COUNTRY_FLAGS: Dict[str, str] = {
    "DE": "🇩🇪", "FI": "🇫🇮", "NL": "🇳🇱", "SE": "🇸🇪", "CH": "🇨🇭",
    "AT": "🇦🇹", "US": "🇺🇸", "CA": "🇨🇦", "FR": "🇫🇷", "GB": "🇬🇧",
    "SG": "🇸🇬", "AU": "🇦🇺", "PL": "🇵🇱", "RO": "🇷🇴", "TR": "🇹🇷",
    "IR": "🇮🇷", "RU": "🇷🇺", "AE": "🇦🇪", "JP": "🇯🇵", "HK": "🇭🇰",
    "IN": "🇮🇳", "IT": "🇮🇹", "ES": "🇪🇸", "EE": "🇪🇪", "BG": "🇧🇬",
    "LT": "🇱🇹", "LV": "🇱🇻", "CZ": "🇨🇿", "SK": "🇸🇰", "HU": "🇭🇺",
    "NO": "🇳🇴", "DK": "🇩🇰", "IE": "🇮🇪", "BE": "🇧🇪", "LU": "🇱🇺",
    "PT": "🇵🇹", "GR": "🇬🇷", "UA": "🇺🇦", "KZ": "🇰🇿", "MD": "🇲🇩",
    "RS": "🇷🇸", "HR": "🇭🇷", "SI": "🇸🇮", "IL": "🇮🇱", "KR": "🇰🇷",
    "TW": "🇹🇼", "VN": "🇻🇳", "TH": "🇹🇭", "MY": "🇲🇾", "ID": "🇮🇩",
    "BR": "🇧🇷", "AR": "🇦🇷", "MX": "🇲🇽", "ZA": "🇿🇦", "NZ": "🇳🇿",
}
DEFAULT_FLAG = "🏳️"

COUNTRY_PRIORITY: Dict[str, int] = {
    "DE": 9, "FI": 9, "NL": 9, "SE": 8, "CH": 8,
    "AT": 7, "US": 7, "CA": 7, "FR": 6, "GB": 6,
    "SG": 6, "AU": 6, "PL": 5, "RO": 5, "TR": 4, "IR": 4,
}

MAX_PER_FILE = 1000
HIDDIFY_LIMIT = 200

POPULAR_COUNTRIES: List[str] = [
    "DE", "NL", "FR", "TR", "AE", "US", "GB", "FI", "SE", "CH",
    "AT", "CA", "PL", "SG", "AU", "RO", "IR", "JP", "HK", "IT",
]

HIDDIFY_PER_COUNTRY = 0

VALID_PORTS = {80, 443, 2052, 2053, 2082, 2083, 2086, 2087,
               2095, 2096, 8080, 8443, 8880}

TELEGRAM_WEB = "https://t.me/s/{channel}"


def load_sources() -> Dict[str, List[str]]:
    default = {
        "vless": ["https://raw.githubusercontent.com/SoliSpirit/v2ray-configs/refs/heads/main/Protocols/vless.txt"],
        "vmess": ["https://raw.githubusercontent.com/SoliSpirit/v2ray-configs/refs/heads/main/Protocols/vmess.txt"],
        "trojan": ["https://raw.githubusercontent.com/SoliSpirit/v2ray-configs/refs/heads/main/Protocols/trojan.txt"],
        "ss": ["https://raw.githubusercontent.com/SoliSpirit/v2ray-configs/refs/heads/main/Protocols/ss.txt"],
        "frag": ["https://raw.githubusercontent.com/hiddify/hiddify-app/refs/heads/main/test.configs/fragment"],
    }
    if not os.path.exists(SOURCES_FILE):
        with open(SOURCES_FILE, "w", encoding="utf-8") as f:
            json.dump(default, f, indent=2)
        return default
    try:
        with open(SOURCES_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        return {k: v for k, v in data.items() if k in default}
    except Exception as e:
        print(f"خطا در خواندن {SOURCES_FILE}: {e} — از مقدار پیش‌فرض استفاده می‌شود.")
        return default


def load_channels() -> List[str]:
    default = [
        "v2ray_configs",
        "v2ray_ng",
        "FreeV2rayConfig",
        "vpnowl",
        "v2rayng_fars",
        "v2ryNG01",
        "v2rayngpro",
        "v2rayfree",
    ]
    if not os.path.exists(CHANNELS_FILE):
        with open(CHANNELS_FILE, "w", encoding="utf-8") as f:
            json.dump(default, f, indent=2, ensure_ascii=False)
        return default
    try:
        with open(CHANNELS_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        if isinstance(data, dict):
            data = data.get("channels", [])
        return [str(c).strip().lstrip("@") for c in data if str(c).strip()]
    except Exception as e:
        print(f"خطا در خواندن {CHANNELS_FILE}: {e} — از مقدار پیش‌فرض استفاده می‌شود.")
        return default


def ensure_dirs() -> None:
    try:
        if os.path.isfile(OUTPUT_DIR):
            os.remove(OUTPUT_DIR)
        os.makedirs(OUTPUT_DIR, exist_ok=True)
    except Exception as e:
        print(f"⚠️ خطا در ایجاد پوشه‌ها: {e}")
        raise


def now_iran() -> str:
    iran_ts = datetime.now(timezone.utc).timestamp() + 3.5 * 3600
    return datetime.fromtimestamp(iran_ts).strftime("%Y-%m-%d %H:%M:%S")


def country_flag(country_code: Optional[str]) -> str:
    cc = (country_code or "").strip().upper()
    if not cc:
        return DEFAULT_FLAG
    if cc in COUNTRY_FLAGS:
        return COUNTRY_FLAGS[cc]
    if len(cc) == 2 and cc.isalpha():
        return chr(0x1F1E6 + ord(cc[0]) - 65) + chr(0x1F1E6 + ord(cc[1]) - 65)
    return DEFAULT_FLAG


def build_display_name(entry: "ConfigEntry", index: int = 0) -> str:
    latency = ""
    if SHOW_LATENCY_IN_NAME and entry.latency_ms is not None:
        latency = f"{int(entry.latency_ms)}ms"

    fields = {
        "channel": CHANNEL_NAME,
        "flag": country_flag(entry.country_code),
        "country": (entry.country_code or "XX").upper(),
        "protocol": entry.proto.upper(),
        "latency": latency,
        "host": entry.host or "",
        "port": str(entry.port or ""),
        "index": str(index),
    }

    try:
        name = NAME_TEMPLATE.format(**fields)
    except KeyError as e:
        print(f"⚠️ متغیر ناشناخته در NAME_TEMPLATE: {e} — از قالب پیش‌فرض استفاده می‌شود.")
        name = f"{CHANNEL_NAME} {fields['flag']} {fields['protocol']} {latency}"

    parts = [p.strip() for p in name.split("|")]
    parts = [p for p in parts if p]
    cleaned = " | ".join(parts) if len(parts) > 1 else (parts[0] if parts else name)
    return re.sub(r"\s{2,}", " ", cleaned).strip()


@dataclass
class ConfigEntry:
    proto: str
    raw: str
    identity: str
    host: Optional[str] = None
    port: Optional[int] = None
    country: Optional[str] = None
    country_code: Optional[str] = None
    latency_ms: Optional[float] = None
    quality_score: Optional[float] = None
    source: Optional[str] = None

    @property
    def uid(self) -> str:
        host = (self.host or "").lower().strip()
        port = self.port or 0
        return f"{self.proto}|{host}|{port}|{self.identity}"

    @property
    def display_name(self) -> str:
        return build_display_name(self)


def split_host_port(value: str) -> Tuple[Optional[str], Optional[int]]:
    if not value:
        return None, None
    value = value.strip()
    if value.startswith("["):
        end = value.find("]")
        if end != -1:
            host = value[1:end]
            rest = value[end + 1:]
            if rest.startswith(":") and rest[1:].isdigit():
                return host, int(rest[1:])
            return host, None
    if ":" in value:
        host, p = value.rsplit(":", 1)
        return host.strip(), int(p) if p.isdigit() else None
    return value, None


def parse_vless(line: str) -> Optional[ConfigEntry]:
    try:
        no_scheme = line.split("://", 1)[1]
        userinfo, rest = no_scheme.split("@", 1)
        identity = unquote(userinfo.split(":", 1)[0]).strip()
        host, port = split_host_port(rest.split("?", 1)[0].split("#", 1)[0])
        if not identity or not host:
            return None
        return ConfigEntry("vless", line, identity, host, port)
    except Exception:
        return None


def parse_vmess(line: str) -> Optional[ConfigEntry]:
    try:
        raw = line.split("://", 1)[1].strip()
        pad = len(raw) % 4
        if pad:
            raw += "=" * (4 - pad)
        decoded = base64.b64decode(raw, validate=False).decode("utf-8", errors="ignore")
        obj = json.loads(decoded)
        identity = str(obj.get("id") or obj.get("uuid") or "").strip()
        host = str(obj.get("add") or obj.get("host") or "").strip() or None
        p = obj.get("port")
        port = int(p) if str(p).isdigit() else None
        if not identity or not host:
            return None
        return ConfigEntry("vmess", line, identity, host, port)
    except Exception:
        return None


def parse_trojan(line: str) -> Optional[ConfigEntry]:
    try:
        no_scheme = line.split("://", 1)[1]
        userinfo, rest = no_scheme.split("@", 1)
        identity = unquote(userinfo.split(":", 1)[0]).strip()
        host, port = split_host_port(rest.split("?", 1)[0].split("#", 1)[0])
        if not identity or not host:
            return None
        return ConfigEntry("trojan", line, identity, host, port)
    except Exception:
        return None


def parse_ss(line: str) -> Optional[ConfigEntry]:
    try:
        body = line.split("://", 1)[1]
        tmp = body.split("#", 1)[0].split("?", 1)[0]

        if "@" in tmp:
            userinfo, hp = tmp.split("@", 1)
            identity = unquote(userinfo)
        else:
            pad = len(tmp) % 4
            tmp_padded = tmp + "=" * (4 - pad) if pad else tmp
            try:
                decoded = base64.b64decode(tmp_padded, validate=False).decode("utf-8", errors="ignore")
            except Exception:
                return None
            if "@" not in decoded:
                return None
            userinfo, hp = decoded.split("@", 1)
            identity = userinfo

        host, port = split_host_port(hp)
        if not host or not identity:
            return None
        return ConfigEntry("ss", line, identity, host, port)
    except Exception:
        return None


def parse_config(proto: str, line: str) -> Optional[ConfigEntry]:
    l = line.strip().lower()
    if not l:
        return None
    if proto == "vless" or l.startswith("vless://"):
        return parse_vless(line.strip())
    if proto == "vmess" or l.startswith("vmess://"):
        return parse_vmess(line.strip())
    if proto == "trojan" or l.startswith("trojan://"):
        return parse_trojan(line.strip())
    if proto == "ss" or l.startswith("ss://"):
        return parse_ss(line.strip())
    if proto == "frag":
        return ConfigEntry("frag", line.strip(), line.strip())
    return None


FAKE_PATTERNS = [
    r"\bfree\b.*\bvpn\b", r"\bfake\b", r"\btest\b", r"\bexample\b",
    r"\btemp\b", r"\bspeedtest\b", r"x{4,}", r"\bnull\b", r"\bunknown\b",
]


def is_fake(entry: ConfigEntry) -> bool:
    txt = entry.raw.lower()
    return any(re.search(p, txt) for p in FAKE_PATTERNS)


def is_valid_entry(e: ConfigEntry) -> bool:
    if not e.host or not e.port:
        return False
    if not (1 <= e.port <= 65535):
        return False
    if not e.identity:
        return False
    host = e.host.strip()
    if len(host) < 4 or " " in host or host.startswith(".") or host.endswith("."):
        return False
    if not re.match(r"^[A-Za-z0-9._\-:\[\]]+$", host):
        return False
    if host.replace(".", "").isdigit():
        parts = host.split(".")
        if len(parts) != 4 or any(not (0 <= int(p) <= 255) for p in parts):
            return False
    return True


def dedupe_entries(entries: List[ConfigEntry]) -> List[ConfigEntry]:
    seen = set()
    out: List[ConfigEntry] = []
    for e in entries:
        key = e.uid
        if key not in seen:
            seen.add(key)
            out.append(e)
    return out


async def resolve_host(host: str) -> Optional[str]:
    if not host:
        return None
    if re.match(r"^\d{1,3}(\.\d{1,3}){3}$", host):
        return host
    loop = asyncio.get_running_loop()
    try:
        infos = await asyncio.wait_for(
            loop.getaddrinfo(host, None, family=socket.AF_INET),
            timeout=DNS_TIMEOUT,
        )
        if infos:
            return infos[0][4][0]
    except Exception:
        return None
    return None


async def geoip_lookup(ip: str, session: aiohttp.ClientSession,
                       sem: asyncio.Semaphore) -> Optional[str]:
    if not ip:
        return None
    async with sem:
        for template, keys in GEOIP_PROVIDERS:
            try:
                async with session.get(template.format(ip=ip),
                                       timeout=aiohttp.ClientTimeout(total=6)) as r:
                    if r.status != 200:
                        continue
                    data = await r.json(content_type=None)
                    cc = ""
                    for k in keys:
                        cc = str(data.get(k) or "").strip().upper()
                        if cc:
                            break
                    if len(cc) == 2 and cc.isalpha():
                        return cc
            except Exception:
                continue
    return None


async def measure_latency(entry: ConfigEntry, sem: asyncio.Semaphore) -> Optional[float]:
    if not entry.host or not entry.port:
        return None
    async with sem:
        start = time.monotonic()
        try:
            reader, writer = await asyncio.wait_for(
                asyncio.open_connection(
                    entry.host, entry.port,
                    ssl=True, server_hostname=entry.host,
                ),
                timeout=LATENCY_TIMEOUT,
            )
            writer.close()
            try:
                await writer.wait_closed()
            except Exception:
                pass
            return round((time.monotonic() - start) * 1000, 1)
        except Exception:
            return None


async def resolve_many(entries: List[ConfigEntry], limit: int) -> Dict[str, Optional[str]]:
    cache: Dict[str, Optional[str]] = {}
    sem = asyncio.Semaphore(80)

    async def one(e: ConfigEntry) -> None:
        h = (e.host or "").lower()
        if not h or h in cache:
            return
        async with sem:
            cache[h] = await resolve_host(h)

    await asyncio.gather(*[one(e) for e in entries[:limit]])
    return cache


async def enrich_entries(entries: List[ConfigEntry], session: aiohttp.ClientSession) -> None:
    geo_sem = asyncio.Semaphore(GEOIP_CONCURRENCY)
    lat_sem = asyncio.Semaphore(LATENCY_CONCURRENCY)
    geo_cache: Dict[str, Optional[str]] = {}

    dns_cache: Dict[str, Optional[str]] = {}
    if ENABLE_GEOIP:
        dns_cache = await resolve_many(entries, MAX_ENRICH_GEOIP)

    async def lookup_cached(ip: Optional[str]) -> Optional[str]:
        if not ip:
            return None
        if ip not in geo_cache:
            geo_cache[ip] = await geoip_lookup(ip, session, geo_sem)
        return geo_cache[ip]

    async def do_geo(e: ConfigEntry) -> None:
        ip = dns_cache.get((e.host or "").lower())
        cc = await lookup_cached(ip)
        if cc:
            e.country_code = cc
            e.country = cc

    async def do_lat(e: ConfigEntry) -> None:
        ms = await measure_latency(e, lat_sem)
        if ms is not None:
            e.latency_ms = ms

    tasks: List[asyncio.Task] = []
    if ENABLE_GEOIP:
        for e in entries[:MAX_ENRICH_GEOIP]:
            tasks.append(asyncio.create_task(do_geo(e)))
    if ENABLE_LATENCY:
        for e in entries[:MAX_ENRICH_LATENCY]:
            tasks.append(asyncio.create_task(do_lat(e)))

    if tasks:
        await asyncio.gather(*tasks)


async def fetch_url(url: str, session: aiohttp.ClientSession,
                    sem: asyncio.Semaphore) -> List[str]:
    async with sem:
        for attempt in range(FETCH_RETRIES):
            try:
                async with session.get(
                    url,
                    timeout=aiohttp.ClientTimeout(total=25),
                    headers={"User-Agent": USER_AGENT},
                ) as r:
                    if r.status != 200:
                        raise RuntimeError(f"HTTP {r.status}")
                    text = await r.text()
                    return [line.strip() for line in text.splitlines() if line.strip()]
            except Exception as e:
                if attempt == FETCH_RETRIES - 1:
                    print(f"⚠️ خطا در دریافت {url}: {e}")
                else:
                    await asyncio.sleep(2 ** attempt)
    return []


CONFIG_RE = re.compile(
    r"(vless://|vmess://|trojan://|ss://)[^\s<>\"']+"
)


def extract_configs(text: str) -> List[str]:
    out: List[str] = []
    for m in CONFIG_RE.finditer(text):
        raw = m.group(0)
        raw = raw.replace("&amp;", "&").strip().rstrip(".,;)")
        out.append(raw)
    return out


async def fetch_telegram_channel(channel: str, session: aiohttp.ClientSession,
                                 sem: asyncio.Semaphore) -> Tuple[List[str], str]:
    async with sem:
        for attempt in range(FETCH_RETRIES):
            try:
                async with session.get(
                    TELEGRAM_WEB.format(channel=channel),
                    timeout=aiohttp.ClientTimeout(total=25),
                    headers={"User-Agent": USER_AGENT},
                ) as r:
                    if r.status != 200:
                        raise RuntimeError(f"HTTP {r.status}")
                    html = await r.text()
                    configs = extract_configs(html)
                    return configs, channel
            except Exception as e:
                if attempt == FETCH_RETRIES - 1:
                    print(f"⚠️ خطا در کانال @{channel}: {e}")
                else:
                    await asyncio.sleep(2 ** attempt)
    return [], channel


async def fetch_all(sources: Dict[str, List[str]], channels: List[str]) -> Tuple[Dict[str, List[ConfigEntry]], Dict[str, int]]:
    stats = {"initial": 0, "invalid": 0, "fake": 0, "after_dedup": 0, "telegram": 0}

    async with aiohttp.ClientSession() as session:
        sem = asyncio.Semaphore(FETCH_CONCURRENCY)

        tasks: List[Tuple[str, asyncio.Task]] = []
        for proto, urls in sources.items():
            for u in urls:
                tasks.append((proto, asyncio.create_task(fetch_url(u, session, sem))))

        raw_lines: Dict[str, List[str]] = {k: [] for k in sources.keys()}
        for proto, task in tasks:
            try:
                raw_lines[proto].extend(await task)
            except Exception:
                pass

        if "frag" in raw_lines:
            raw_lines["frag"] = [l for l in raw_lines["frag"] if not l.strip().startswith("#")]

        entries: List[ConfigEntry] = []
        for proto, lines in raw_lines.items():
            for line in lines:
                if not line or line.startswith("#"):
                    continue
                stats["initial"] += 1
                e = parse_config(proto, line)
                if not e:
                    stats["invalid"] += 1
                    continue
                if proto != "frag" and not is_valid_entry(e):
                    stats["invalid"] += 1
                    continue
                if proto != "frag" and is_fake(e):
                    stats["fake"] += 1
                    continue
                e.source = proto
                entries.append(e)

        if channels:
            print(f"📡 دریافت از {len(channels)} کانال تلگرام ...")
            ch_tasks = [asyncio.create_task(fetch_telegram_channel(c, session, sem)) for c in channels]
            for ch_task in asyncio.as_completed(ch_tasks):
                try:
                    configs, channel = await ch_task
                except Exception:
                    continue
                for line in configs:
                    stats["initial"] += 1
                    e = parse_config("", line)
                    if not e or e.proto == "frag":
                        stats["invalid"] += 1
                        continue
                    if not is_valid_entry(e) or is_fake(e):
                        stats["fake"] += 1
                        continue
                    e.source = f"@{channel}"
                    entries.append(e)
                    stats["telegram"] += 1

        entries = dedupe_entries(entries)
        stats["after_dedup"] = len(entries)

        await enrich_entries(entries, session)

        grouped: Dict[str, List[ConfigEntry]] = {k: [] for k in sources.keys()}
        for e in entries:
            grouped.setdefault(e.proto, []).append(e)

        return grouped, stats


def compute_quality(e: ConfigEntry) -> None:
    country_weight = COUNTRY_PRIORITY.get(e.country_code or "", 0)
    lat = e.latency_ms if e.latency_ms is not None else 500.0
    e.quality_score = country_weight * 10 - lat * 0.3


def sort_by_quality(entries: List[ConfigEntry]) -> List[ConfigEntry]:
    for e in entries:
        compute_quality(e)
    return sorted(entries, key=lambda x: -(x.quality_score if x.quality_score is not None else -9999))


def cap_entries(entries: List[ConfigEntry], limit: int = MAX_PER_FILE) -> List[ConfigEntry]:
    return entries[:limit] if limit and limit > 0 else entries


def diversify_by_country(entries: List[ConfigEntry], limit: int,
                         countries: Optional[List[str]] = None,
                         per_country: int = 0) -> List[ConfigEntry]:
    countries = countries or POPULAR_COUNTRIES

    buckets: Dict[str, List[ConfigEntry]] = {}
    for e in entries:
        cc = (e.country_code or "").upper() or "??"
        buckets.setdefault(cc, []).append(e)

    ordered = [cc for cc in countries if cc in buckets]
    rest = [cc for cc in buckets if cc not in countries and cc != "??"]
    rest.sort(key=lambda cc: -(buckets[cc][0].quality_score or -9999))
    ordered += rest
    if "??" in buckets:
        ordered.append("??")

    result: List[ConfigEntry] = []
    idx: Dict[str, int] = {cc: 0 for cc in ordered}
    counts: Dict[str, int] = {cc: 0 for cc in ordered}

    progress = True
    while len(result) < limit and progress:
        progress = False
        for cc in ordered:
            if len(result) >= limit:
                break
            if per_country and counts[cc] >= per_country:
                continue
            i = idx[cc]
            if i < len(buckets[cc]):
                result.append(buckets[cc][i])
                idx[cc] = i + 1
                counts[cc] += 1
                progress = True

    return result


def rename_config(entry: ConfigEntry, index: int) -> str:
    name = build_display_name(entry, index)
    raw = entry.raw

    if entry.proto in ("vless", "trojan", "ss"):
        base = raw.split("#", 1)[0]
        return f"{base}#{name}"

    if entry.proto == "vmess":
        try:
            body = raw.split("://", 1)[1].strip()
            pad = len(body) % 4
            padded = body + "=" * (4 - pad) if pad else body
            decoded = base64.b64decode(padded, validate=False).decode("utf-8", errors="ignore")
            obj = json.loads(decoded)
            obj["ps"] = name
            new_json = json.dumps(obj, ensure_ascii=False, separators=(",", ":"))
            encoded = base64.b64encode(new_json.encode("utf-8")).decode("ascii")
            return f"vmess://{encoded}"
        except Exception:
            return raw

    return raw


def b64_header_title(title: str) -> str:
    return base64.b64encode(title.encode("utf-8")).decode("ascii")


def subscription_header(title: str, test_url: str = "https://www.gstatic.com/generate_204") -> str:
    return (
        f"#profile-title: base64:{b64_header_title(title)}\n"
        f"#profile-update-interval: 6\n"
        f"#subscription-userinfo: upload=0; download=0; total=10737418240000000; expire=2546249531\n"
        f"#support-url: https://t.me/proxystore11\n"
        f"#profile-web-page-url: https://proxystore11.news\n"
        f"#connection-test-url: {test_url}\n"
        f"#remote-dns-address: https://sky.rethinkdns.com/dns-query\n"
    )


async def run() -> None:
    print("🔄 بارگذاری منابع ...")
    sources = load_sources()
    channels = load_channels()
    print(f"✅ {sum(len(v) for v in sources.values())} منبع و {len(channels)} کانال تلگرام")

    ensure_dirs()

    grouped, stats = await fetch_all(sources, channels)

    vless = sort_by_quality(grouped.get("vless", []))
    vmess = sort_by_quality(grouped.get("vmess", []))
    trojan = sort_by_quality(grouped.get("trojan", []))
    ss = sort_by_quality(grouped.get("ss", []))
    frag = grouped.get("frag", [])

    def renamed(entries: List[ConfigEntry]) -> List[str]:
        return [rename_config(e, i) for i, e in enumerate(entries)]

    vless_out = renamed(cap_entries(vless))
    vmess_out = renamed(cap_entries(vmess))
    trojan_out = renamed(cap_entries(trojan))
    ss_out = renamed(cap_entries(ss))

    def write_file(name: str, lines: List[str], header: str = "") -> None:
        path = os.path.join(OUTPUT_DIR, name)
        body = "\n".join(lines)
        content = f"{header}\n{body}" if header else body
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"📄 نوشته شد: {path} ({len(lines)} کانفیگ)")

    hdr_all = subscription_header(f"{CHANNEL_NAME} | All Configs")
    hdr_vless = subscription_header(f"{CHANNEL_NAME} | VLESS")
    hdr_vmess = subscription_header(f"{CHANNEL_NAME} | VMESS")
    hdr_trojan = subscription_header(f"{CHANNEL_NAME} | Trojan")
    hdr_ss = subscription_header(f"{CHANNEL_NAME} | Shadowsocks")
    hdr_hiddify = subscription_header(f"{CHANNEL_NAME} | Hiddify Optimized")
    hdr_frag = subscription_header(f"{CHANNEL_NAME} | Fragment (Instagram/YouTube)", "https://www.instagram.com")

    hiddify_entries = diversify_by_country(
        vless, HIDDIFY_LIMIT, POPULAR_COUNTRIES, HIDDIFY_PER_COUNTRY
    )
    hiddify_out = renamed(hiddify_entries)

    write_file("prx11-vless.txt", vless_out, hdr_vless)
    write_file("prx11-vmess.txt", vmess_out, hdr_vmess)
    write_file("prx11-trojan.txt", trojan_out, hdr_trojan)
    write_file("prx11-ss.txt", ss_out, hdr_ss)
    write_file("prx11-hiddify.txt", hiddify_out, hdr_hiddify)

    frag_raw = [e.raw for e in frag]
    write_file("prx11-insta-youto.txt", frag_raw, hdr_frag)

    all_out = list(dict.fromkeys(
        [e.raw for e in vless] + [e.raw for e in vmess] + [e.raw for e in trojan] + [e.raw for e in ss]
    ))
    write_file("prx11-all.txt", all_out, hdr_all)

    iran_str = now_iran()
    with open(AUTO_UPDATE_FILE, "w", encoding="utf-8") as f:
        f.write(f"Auto Update: {iran_str}\n")

    country_stats: Dict[str, int] = {}
    latency_map: Dict[str, List[float]] = {}

    for lst in [vless, vmess, trojan, ss]:
        for e in lst:
            cc = e.country_code or "??"
            country_stats[cc] = country_stats.get(cc, 0) + 1
            if e.latency_ms is not None:
                latency_map.setdefault(cc, []).append(e.latency_ms)

    latency_summary: Dict[str, Dict[str, float]] = {}
    for cc, vals in latency_map.items():
        latency_summary[cc] = {
            "avg": round(statistics.mean(vals), 1),
            "min": round(min(vals), 1),
            "max": round(max(vals), 1),
            "samples": len(vals),
        }

    top_fast = sorted(
        [(cc, latency_summary[cc]["avg"]) for cc in latency_summary],
        key=lambda x: x[1],
    )[:10]

    hiddify_countries: Dict[str, int] = {}
    for e in hiddify_entries:
        cc = e.country_code or "??"
        hiddify_countries[cc] = hiddify_countries.get(cc, 0) + 1

    source_stats: Dict[str, int] = {}
    for e in vless + vmess + trojan + ss:
        s = e.source or "unknown"
        source_stats[s] = source_stats.get(s, 0) + 1

    known_country = sum(v for k, v in country_stats.items() if k != "??")
    log_data = {
        "updated_at_iran": iran_str,
        "initial_configs": stats["initial"],
        "invalid_removed": stats["invalid"],
        "fake_removed": stats["fake"],
        "telegram_configs": stats["telegram"],
        "after_dedup": stats["after_dedup"],
        "removed_duplicates": stats["initial"] - stats["invalid"] - stats["fake"] - stats["after_dedup"],
        "geoip_known": known_country,
        "geoip_unknown": country_stats.get("??", 0),
        "outputs": {
            "vless": len(vless_out),
            "vmess": len(vmess_out),
            "trojan": len(trojan_out),
            "ss": len(ss_out),
            "hiddify": len(hiddify_out),
            "all": len(all_out),
        },
        "hiddify_country_distribution": dict(sorted(hiddify_countries.items(), key=lambda x: -x[1])),
        "country_distribution": dict(sorted(country_stats.items(), key=lambda x: -x[1])),
        "source_distribution": dict(sorted(source_stats.items(), key=lambda x: -x[1])),
        "latency_summary_ms": latency_summary,
        "top10_fastest_countries": top_fast,
    }

    with open(LOGGER_FILE, "w", encoding="utf-8") as f:
        json.dump(log_data, f, indent=2, ensure_ascii=False)

    print("✅ جمع‌آوری با موفقیت انجام شد.")
    print(f"   خام: {stats['initial']} | نامعتبر: {stats['invalid']} | جعلی: {stats['fake']} | نهایی: {stats['after_dedup']}")


def main() -> None:
    try:
        asyncio.run(run())
    except KeyboardInterrupt:
        print("⏹️ اجرا توسط کاربر متوقف شد.")
    except Exception as e:
        print(f"❌ خطای غیرمنتظره: {e}")
        raise


if __name__ == "__main__":
    main()
