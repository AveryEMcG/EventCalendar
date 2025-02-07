import unittest
import helpers


class TestStringMethods(unittest.TestCase):

    def test_upper(self):
        
        data = {"name":"n/a","id":0,"duration":60,"start_time":1738857600,"repeats_su":False,"repeats_m":False,"repeats_t":False,"repeats_w":False,"repeats_th":False,"repeats_f":True,"repeats_s":False}
        print(helpers.timeIsUnique(data))
     

if __name__ == '__main__':
    unittest.main()