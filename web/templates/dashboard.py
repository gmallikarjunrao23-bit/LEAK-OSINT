<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>LeakOSINT Pro — Admin</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap" rel="stylesheet">
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'Inter', sans-serif;
            background: #0a0a0f;
            color: #fff;
            min-height: 100vh;
            background-image: radial-gradient(ellipse at 20% 50%, rgba(88,28,135,0.15) 0%, transparent 60%);
        }
        .container { max-width: 1280px; margin: 0 auto; padding: 24px; }
        .header { display: flex; justify-content: space-between; align-items: center; padding: 16px 0; border-bottom: 1px solid rgba(255,255,255,0.06); margin-bottom: 32px; }
        .header h1 { font-size: 28px; font-weight: 800; background: linear-gradient(135deg, #fff, #a78bfa); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
        .admin-badge { display: flex; align-items: center; gap: 12px; background: rgba(255,255,255,0.04); padding: 8px 20px; border-radius: 100px; border: 1px solid rgba(255,255,255,0.06); }
        .stat-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap: 20px; margin-bottom: 32px; }
        .stat-card { background: rgba(255,255,255,0.04); border: 1px solid rgba(255,255,255,0.06); border-radius: 20px; padding: 24px; }
        .stat-card .value { font-size: 32px; font-weight: 800; background: linear-gradient(135deg, #fff 60%, rgba(255,255,255,0.6)); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
        .stat-card .label { font-size: 14px; color: rgba(255,255,255,0.5); margin-top: 4px; }
        .glass-card { background: rgba(255,255,255,0.04); border: 1px solid rgba(255,255,255,0.06); border-radius: 24px; padding: 24px; overflow: hidden; }
        .table-container { overflow-x: auto; }
        table { width: 100%; border-collapse: collapse; font-size: 14px; }
        thead { background: rgba(255,255,255,0.03); border-bottom: 1px solid rgba(255,255,255,0.06); }
        th { text-align: left; padding: 14px 16px; font-weight: 600; font-size: 12px; text-transform: uppercase; color: rgba(255,255,255,0.4); }
        td { padding: 14px 16px; border-bottom: 1px solid rgba(255,255,255,0.04); }
        .badge { display: inline-block; padding: 4px 14px; border-radius: 100px; font-size: 12px; font-weight: 600; }
        .badge-pending { background: rgba(251,191,36,0.15); color: #fbbf24; }
        .badge-approved { background: rgba(52,211,153,0.15); color: #34d399; }
        .badge-rejected { background: rgba(239,68,68,0.15); color: #ef4444; }
        .btn { padding: 8px 16px; border: none; border-radius: 10px; font-weight: 600; font-size: 13px; cursor: pointer; font-family: inherit; }
        .btn-approve { background: linear-gradient(135deg, #10b981, #059669); color: #fff; }
        .btn-reject { background: linear-gradient(135deg, #ef4444, #dc2626); color: #fff; }
        .btn-approve:hover, .btn-reject:hover { transform: scale(1.04); }
        .section-title { font-size: 18px; font-weight: 700; margin-bottom: 16px; }
        .empty-state { text-align: center; padding: 48px; color: rgba(255,255,255,0.3); }
        @media (max-width: 768px) { .stat-grid { grid-template-columns: repeat(2,1fr); } .header { flex-direction: column; align-items: flex-start; gap: 16px; } }
    </style>
</head>
<body>
    <div class="container">
        <header class="header">
            <h1>✦ LeakOSINT Pro</h1>
            <div class="admin-badge">👑 Admin | <a href="/" style="color:rgba(255,255,255,0.3);text-decoration:none;">Logout</a></div>
        </header>
        
        <div class="stat-grid">
            <div class="stat-card"><div class="value">{{ stats.total_users }}</div><div class="label">Total Users</div></div>
            <div class="stat-card"><div class="value">{{ stats.premium_users }}</div><div class="label">Premium Users</div></div>
            <div class="stat-card"><div class="value">{{ stats.total_searches }}</div><div class="label">Total Searches</div></div>
            <div class="stat-card"><div class="value">{{ stats.pending_payments }}</div><div class="label">Pending Payments</div></div>
        </div>
        
        <div class="section-title">📋 Pending Payments ({{ pending_payments|length }})</div>
        <div class="glass-card">
            {% if pending_payments %}
            <div class="table-container">
                <table>
                    <thead><tr><th>User</th><th>Plan</th><th>Amount</th><th>Txn ID</th><th>Submitted</th><th>Actions</th></tr></thead>
                    <tbody>
                        {% for p in pending_payments %}
                        <tr>
                            <td>@{{ p.username or 'N/A' }}<br><span style="color:rgba(255,255,255,0.3);font-size:12px;">ID: {{ p.user_id }}</span></td>
                            <td><span class="badge badge-pending">{{ p.plan.upper() }}</span></td>
                            <td>₹{{ p.amount }}</td>
                            <td><code style="background:rgba(255,255,255,0.04);padding:2px 8px;border-radius:6px;">{{ p.transaction_id }}</code></td>
                            <td>{{ p.created_at.strftime('%Y-%m-%d %H:%M') }}</td>
                            <td>
                                <form method="POST" action="/admin/approve/{{ p.id }}" style="display:inline;"><button class="btn btn-approve">✅</button></form>
                                <form method="POST" action="/admin/reject/{{ p.id }}" style="display:inline;margin-left:4px;">
                                    <input type="hidden" name="reason" value="Verification failed">
                                    <button class="btn btn-reject">❌</button>
                                </form>
                            </td>
                        </tr>
                        {% endfor %}
                    </tbody>
                </table>
            </div>
            {% else %}
            <div class="empty-state">🎉 No pending payments</div>
            {% endif %}
        </div>
    </div>
    <script>setInterval(()=>location.reload(), 30000);</script>
</body>
</html>
