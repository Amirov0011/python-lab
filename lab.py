import re
import csv
from collections import defaultdict

LogFile = """
192.168.1.100 - - [08/Dec/2024:10:35:22 +0000] "POST /login HTTP/1.1" 200 678
10.0.0.2 - - [08/Dec/2024:10:36:10 +0000] "GET /nonexistent-page.html HTTP/1.1" 404 123
172.16.5.10 - - [08/Dec/2024:10:37:45 +0000] "GET /admin-panel HTTP/1.1" 401 0
192.168.1.100 - - [08/Dec/2024:10:38:00 +0000] "POST /login HTTP/1.1" 401 0
172.16.5.10 - - [08/Dec/2024:10:39:00 +0000] "GET /admin-panel HTTP/1.1" 401 0
203.0.113.45 - - [08/Dec/2024:10:40:15 +0000] "GET /video.mp4 HTTP/1.1" 200 4590234
172.16.5.10 - - [08/Dec/2024:10:41:10 +0000] "GET /admin-panel HTTP/1.1" 401 0
172.16.5.10 - - [08/Dec/2024:10:42:20 +0000] "GET /admin-panel HTTP/1.1" 401 0
172.16.5.10 - - [08/Dec/2024:10:43:30 +0000] "GET /admin-panel HTTP/1.1" 401 0
"""

# Define the pattern
LogPattern = re.compile(
    r'(?P<ip>\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}) - - .*?"(?P<mthod>GET|POST|PUT|DELETE) (?P<url>.*?) HTTP/1\.1" (?P<status>\d{3})'
)

matches = LogPattern.finditer(LogFile)

failed_attempts = defaultdict(int)

for match in matches:
    status = int(match.group("status"))
    if status == 401:  # Unsuccessful login
        ip = match.group("ip")
        failed_attempts[ip] += 1

filtered_attempts = {ip: count for ip, count in failed_attempts.items() if count >= 5}

print("IPs with 5 or more unsuccessful login attempts:")
for ip, count in filtered_attempts.items():
    print(f"{ip} - {count} attempts")

csv_filename = ".venv/Scripts/failed_logins.csv"
with open(csv_filename, mode="w", newline="") as csvfile:
    csv_writer = csv.writer(csvfile)
    csv_writer.writerow(["IP Address", "Failed Attempts"])  # Header
    for ip, count in filtered_attempts.items():
        csv_writer.writerow([ip, count])

print(f"Results written to {csv_filename}")
