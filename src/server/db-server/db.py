import sqlite3

DATABASE_NAME = "ScheduledEvent.db"


class Event:
    def __init__(
        self,
        id,
        name,
        start_time,
        duration,
        repeats_su,
        repeats_m,
        repeats_t,
        repeats_w,
        repeats_th,
        repeats_f,
        repeats_s,
    ):
        self.id = id
        self.name = name
        self.start_time = start_time
        self.duration = duration
        self.repeats_su = repeats_su
        self.repeats_m = repeats_m
        self.repeats_t = repeats_t
        self.repeats_w = repeats_w
        self.repeats_th = repeats_th
        self.repeats_f = repeats_f
        self.repeats_s = repeats_s


def query(queryString):
    con = sqlite3.connect(DATABASE_NAME)
    cursor = con.cursor()
    response = cursor.execute("SELECT * FROM ScheduledEvents")
    result = response.fetchall()
    out = []
    print(result)
    for r in result:
        out.append(
            Event(r[0], r[1], r[2], r[3], r[4], r[5], r[6], r[7], r[8], r[9], r[10])
        )
    con.close()
    return out


def insert(insertString):
    con = sqlite3.connect(DATABASE_NAME)
    cursor = con.cursor()
    response = cursor.execute(insertString)
    con.commit()
    result = response.fetchall()
    con.close()
    return result
