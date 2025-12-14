from models import init_db, Session, Device, UsageEntry
import random
import datetime

init_db()
s = Session()

# Clear old data
s.query(UsageEntry).delete()
s.query(Device).delete()

# Devices
devices = ['Phone', 'Laptop']
for name in devices:
    d = Device(name=name)
    s.add(d)
    s.commit()

    # Apps
    apps = ['Social Media', 'Gaming', 'Video'] if name=='Phone' else ['Study','Browsing']
    for app in apps:
        u = UsageEntry(
            device_id=d.id,
            app_name=app,
            seconds=random.randint(1800, 7200),
            pickups=random.randint(5, 30),
            timestamp=datetime.datetime.utcnow()
        )
        s.add(u)

s.commit()
print("Sample data created")
