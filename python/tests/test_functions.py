from unittest import TestCase
from functions import b, db, t, critical_index, additional_one
import numpy as np


class TestFunctions(TestCase):

    def test_b(self):
        self.assertAlmostEqual(b(0.0), 0.0)
        self.assertAlmostEqual(b(np.pi / 2), 0.0)
        self.assertAlmostEqual(b(np.pi), 2.0)
        self.assertAlmostEqual(b(2 * np.pi), 0)


    def test_db(self):
        # Checking that b'(x) is less than 4*pi
        xs = np.linspace(0, 2 * np.pi, 100)
        for x in xs:
            self.assertLessEqual(db(x), 4 * np.pi)


    def test_t(self):
        self.assertAlmostEqual(t(0.0), 0.0)
        self.assertAlmostEqual(t(1.0), 4*np.pi)
        self.assertAlmostEqual(t(1.0/4), np.pi - 4)
        self.assertAlmostEqual(t(1.0/8), np.pi/2 + 1 - 4/np.sqrt(2))


    def test_critical_index(self):
        """see Figure 6.
        """
        # p8
        Kc = 0.3404614162445069

        self.assertEqual(critical_index(8)[0] / 8, 0.375) 

        for N in range(5, 2000):
            target = critical_index(N)[0] / N

            # Eq. (A19)
            self.assertLessEqual(
                target, 
                (np.ceil(Kc * N - 1 / 2 + 2 * np.pi / (2 * N)) / N))

            # Eq. (A1)
            self.assertLessEqual(
                target, 
                Kc + 1.0 / (2 * N) + 2 * np.pi / (3 * N ** 2))

        # N=19, kc=6 (Eq (43), p6)
        self.assertLessEqual(critical_index(19)[0], 6)
