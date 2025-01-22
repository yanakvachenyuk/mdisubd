from django.shortcuts import render
from django.db import connection

def audit_logs_view(request):
    logs = []
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT al.id, u.name AS user_name, al.action, al.timestamp
            FROM audit_logs al
            JOIN users u ON al.user_id = u.id
            ORDER BY al.timestamp DESC
        """)
        logs = cursor.fetchall()

    return render(request, 'admin_audit_logs.html', {'logs': logs})
