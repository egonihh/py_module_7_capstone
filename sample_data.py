from models import init_db, Session, Device, UsageEntry
import random, datetime

init_db()
s = Session()

device_names = ["Phone", "Laptop", "Tablet"]
apps = ["Browser","Chat","Video","Game","Social"]

for name in device_names:
    d = s.query(Device).filter_by(name=name).first()
    if not d:
        d = Device(name=name)
        s.add(d)
        s.commit()
    for _ in range(random.randint(5,15)):
        ue = UsageEntry(
            device_id=d.id,
            app_name=random.choice(apps),
            seconds=random.randint(60, 7200),
            timestamp=datetime.datetime.utcnow(),
            background=random.choice([True, False])
        )
        s.add(ue)
s.commit()
s.close()
print("Sample data created")