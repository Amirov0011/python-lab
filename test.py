import re

import re

LogFile = """
192.168.1.100 - - [08/Dec/2024:10:35:22 +0000] "POST /login HTTP/1.1" 200 678
10.0.0.2 - - [08/Dec/2024:10:36:10 +0000] "GET /nonexistent-page.html HTTP/1.1" 404 123
172.16.5.10 - - [08/Dec/2024:10:37:45 +0000] "GET /admin-panel HTTP/1.1" 401 0
203.0.113.45 - - [08/Dec/2024:10:40:15 +0000] "GET /video.mp4 HTTP/1.1" 200 4590234
"""

LogPattern = re.compile(
    r'(?P<ip>\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}) - - .*?"(?P<mthod>GET|POST|PUT|DELETE) (?P<url>.*?) HTTP/1\.1" (?P<status>\d{3})'
)

matches = LogPattern.finditer(LogFile)

log_entries = []

for match in matches:
    entry = {
        "IP": match.group("ip"),
        "Method": match.group("mthod"),
        "URL": match.group("url"),
        "Status": match.group("status"),
    }
    log_entries.append(entry)
    print(entry)

print("All log entries:", log_entries)
