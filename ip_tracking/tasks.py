from celery import shared_task
from datetime import datetime, timedelta
from .models import RequestLog, SuspiciousIP

@shared_task
def detect_suspicious_ips():
    one_hour_ago = datetime.now() - timedelta(hours=1)
    logs = RequestLog.objects.filter(timestamp__gte=one_hour_ago)

    ip_counts = {}
    sensitive_paths = ['/admin', '/login']

    for log in logs:
        ip_counts[log.ip_address] = ip_counts.get(log.ip_address, 0) + 1
        if log.path in sensitive_paths:
            SuspiciousIP.objects.get_or_create(ip_address=log.ip_address, reason=f"Accessed sensitive path {log.path}")

    for ip, count in ip_counts.items():
        if count > 100:
            SuspiciousIP.objects.get_or_create(ip_address=ip, reason=f"High request rate: {count} requests/hour")
