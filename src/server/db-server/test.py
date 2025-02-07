import unittest
import helpers
import db


class TestStringMethods(unittest.TestCase):

    def test_upper(self):     

        # Thursday, February 6, 2025 11:00:00 AM GMT-05:00
        thursdayMorning = 1738857600
        data = db.Event(None,"test",thursdayMorning,60,False,False,False,False,False,False,False)
        eventList = [db.Event(None,"test",thursdayMorning,60,False,False,False,False,False,False,False)]
        self.assertFalse(helpers.timeIsUnique(data,eventList))

        # Wednesday, February 5, 2025 11:00:00 AM GMT-05:00
        wednesdayMorning = 1738771200
        data = db.Event(None,"Wednesday Morning Repeating",wednesdayMorning,60,False,False,False,False,True,False,False)
        eventList = [db.Event(None,"test",thursdayMorning,60,False,False,False,False,False,False,False)]
        self.assertFalse(helpers.timeIsUnique(data,eventList))

        # Wednesday, February 5, 2025 11:00:00 AM GMT-05:00
        wednesdayMorning = 1738771200
        data = db.Event(None,"Wednesday Morning Repeating",wednesdayMorning,60,False,False,False,False,False,False,True)
        eventList = [db.Event(None,"test",thursdayMorning,60,False,False,False,False,False,False,True)]
        self.assertFalse(helpers.timeIsUnique(data,eventList))

        # Wednesday, February 5, 2025 11:30:00 PM GMT-05:00
        wednesdayNight = 1738816200
        data = db.Event(None,"Wednesday night full day",wednesdayNight,24*60,False,False,False,False,False,False,False)
        eventList = [db.Event(None,"test",thursdayMorning,60,False,False,False,False,False,False,False)]
        self.assertFalse(helpers.timeIsUnique(data,eventList))

        data = db.Event(None,"Wednesday night full day",wednesdayNight,24*60,False,False,False,False,False,False,False)
        eventList = [db.Event(None,"test",wednesdayMorning,60,False,False,False,False,False,False,False)]
        self.assertTrue(helpers.timeIsUnique(data,eventList))





if __name__ == '__main__':
    unittest.main()