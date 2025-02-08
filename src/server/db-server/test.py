import unittest
import helpers
import db

# The only testing so far is for the timeIsUnique function (because it's the most complicated)

wednesdayMorning = 1738771200  # Wednesday, February 5, 2025 11:00:00 AM GMT-05:00
wednesdayNight = 1738816200  # Wednesday, February 5, 2025 11:30:00 PM GMT-05:00
thursdayMorning = 1738857600  # Thursday, February 6, 2025 11:00:00 AM GMT-05:00


class TestTimeIsUnique(unittest.TestCase):
    def test_overlapping_events(self):
        data = db.Event(
            id=None,
            name="Thursday Morning Event1",
            start_time=thursdayMorning,
            duration=60,
            repeats_su=False,
            repeats_m=False,
            repeats_t=False,
            repeats_w=False,
            repeats_th=False,
            repeats_f=False,
            repeats_s=False,
        )
        eventList = [
            db.Event(
                id=None,
                name="Thursday Morning Event2",
                start_time=thursdayMorning,
                duration=60,
                repeats_su=False,
                repeats_m=False,
                repeats_t=False,
                repeats_w=False,
                repeats_th=False,
                repeats_f=False,
                repeats_s=False,
            )
        ]

        # events scheduled at same time should fail
        self.assertFalse(helpers.timeIsUnique(data, eventList))

    def test_event_overlaps_repeats(self):
        data = db.Event(
            id=None,
            name="Thursday Morning Repeating",
            start_time=thursdayMorning,
            duration=60,
            repeats_su=False,
            repeats_m=False,
            repeats_t=False,
            repeats_w=False,
            repeats_th=True,
            repeats_f=False,
            repeats_s=False,
        )
        eventList = [
            db.Event(
                id=None,
                name="Wednesday but Repeating on Thursday Mornings",
                start_time=wednesdayMorning,
                duration=60,
                repeats_su=False,
                repeats_m=False,
                repeats_t=False,
                repeats_w=False,
                repeats_th=True,
                repeats_f=False,
                repeats_s=False,
            )
        ]
        # an event scheduled to repeat onto another event should fail
        self.assertFalse(helpers.timeIsUnique(data, eventList))

    def test_repeats_overlap(self):
        data = db.Event(
            id=None,
            name="Wednesday Morning Repeating Saturday",
            start_time=wednesdayMorning,
            duration=60,
            repeats_su=False,
            repeats_m=False,
            repeats_t=False,
            repeats_w=False,
            repeats_th=False,
            repeats_f=False,
            repeats_s=True,
        )
        eventList = [
            db.Event(
                id=None,
                name="Thursday Morning repeating Saturday",
                start_time=thursdayMorning,
                duration=60,
                repeats_su=False,
                repeats_m=False,
                repeats_t=False,
                repeats_w=False,
                repeats_th=True,
                repeats_f=False,
                repeats_s=True,
            )
        ]
        # events scheduled to repeat over another repeat should fail
        self.assertFalse(helpers.timeIsUnique(data, eventList))

    def test_repeats_overlap(self):
        data = db.Event(
            id=None,
            name="Wednesday night",
            start_time=wednesdayNight,
            duration=60,
            repeats_su=False,
            repeats_m=True,
            repeats_t=False,
            repeats_w=False,
            repeats_th=False,
            repeats_f=False,
            repeats_s=False,
        )
        eventList = [
            db.Event(
                id=None,
                name="Wednesday Morning",
                start_time=wednesdayMorning,
                duration=60,
                repeats_su=False,
                repeats_m=False,
                repeats_t=False,
                repeats_w=False,
                repeats_th=False,
                repeats_f=False,
                repeats_s=False,
            ),
            db.Event(
                id=None,
                name="Thursday Morning",
                start_time=thursdayMorning,
                duration=60,
                repeats_su=False,
                repeats_m=False,
                repeats_t=False,
                repeats_w=False,
                repeats_th=False,
                repeats_f=False,
                repeats_s=True,
            ),
        ]
        # This should work even with many events already exisiting
        self.assertTrue(helpers.timeIsUnique(data, eventList))

    def test_overnight(self):
        data = db.Event(
            id=None,
            name="Wednesday night full day",
            start_time=wednesdayNight,
            duration=24 * 60,
            repeats_su=False,
            repeats_m=False,
            repeats_t=False,
            repeats_w=False,
            repeats_th=True,
            repeats_f=False,
            repeats_s=True,
        )
        eventList = [
            db.Event(
                id=None,
                name="Thursday Morning",
                start_time=thursdayMorning,
                duration=60,
                repeats_su=False,
                repeats_m=False,
                repeats_t=False,
                repeats_w=False,
                repeats_th=False,
                repeats_f=False,
                repeats_s=False,
            )
        ]
        # we should find clashes across day boundaries
        self.assertFalse(helpers.timeIsUnique(data, eventList))

    def test_before_repeats(self):
        data = db.Event(
            id=None,
            name="Wednesday Morning",
            start_time=wednesdayMorning,
            duration=60,
            repeats_su=False,
            repeats_m=False,
            repeats_t=False,
            repeats_w=False,
            repeats_th=False,
            repeats_f=False,
            repeats_s=False,
        )
        eventList = [
            db.Event(
                id=None,
                name="Thursday Morning",
                start_time=thursdayMorning,
                duration=60,
                repeats_su=False,
                repeats_m=False,
                repeats_t=False,
                repeats_w=True,
                repeats_th=False,
                repeats_f=False,
                repeats_s=False,
            )
        ]
        # If you schedule an event which IF it repeated, would clash,
        # but it's happening BEFORE that repeating event and does not repeat on that day, it should pass
        self.assertTrue(helpers.timeIsUnique(data, eventList))


if __name__ == "__main__":
    unittest.main()
