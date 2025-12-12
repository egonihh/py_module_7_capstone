THRESHOLD_PER_APP = 3600  # 1 hour

def format_time(s):
    h = s // 3600
    m = (s % 3600) // 60
    return f"{h}h {m}m" if h else f"{m}m"

def generate_recommendations(device_data):
    out = []
    for dev in device_data:
        total = sum(e['seconds'] for e in dev['entries'])
        apps_sorted = sorted(dev['entries'], key=lambda x: x['seconds'], reverse=True)
        recs = []

        if total > 3*3600:
            recs.append({'type':'limit_suggestion',
                         'msg': f"You've spent {format_time(total)} on {dev['device']}. Try a 3-hour daily cap."})

        for a in apps_sorted[:3]:
            if a['seconds'] > THRESHOLD_PER_APP:
                recs.append({'type':'nudge',
                             'app': a['app'],
                             'msg': f"Consider setting a {format_time(THRESHOLD_PER_APP)} limit for {a['app']}"})

        recs.append({'type':'micro_goal','msg':'Start with a 10-minute less screen window before bed.'})
        recs.append({'type':'env_tweak','msg':'Turn off non-essential notifications for 2 hours after study start.'})

        out.append({'device': dev['device'], 'recommendations': recs})
    return out