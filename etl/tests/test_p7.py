"""P7 : indice de blocage de Tibaldi et Molteni, moyenne de secteur (calculs purs)."""

import unittest

import numpy as np

from etl.sources import era5_blocking as B


def field(lat, lon, f):
    return np.array([[f(la, lo) for lo in lon] for la in lat], dtype=float)


class TestBlocking(unittest.TestCase):
    lat = np.arange(85.0, 29.9, -2.5)
    lon = np.arange(-60.0, 60.1, 2.5)

    def test_zonal_flow_not_blocked(self):
        z = field(self.lat, self.lon, lambda la, lo: 5800 - 10 * (la - 30))      # Z décroît vers le nord
        self.assertFalse(B.blocked_longitudes(z, self.lat).any())

    def test_reversed_gradient_blocked_locally(self):
        def f(la, lo):
            base = 5800 - 10 * (la - 30)
            if -10 <= lo <= 10:                                               # dorsale : maximum vers 60° N
                base = 5600 + (300 - 15 * abs(la - 60)) if la >= 40 else 5600
            return base
        z = field(self.lat, self.lon, f)
        b = B.blocked_longitudes(z, self.lat)
        self.assertTrue(b[list(self.lon).index(0.0)])
        self.assertFalse(b[list(self.lon).index(-50.0)])

    def test_sector_mean_weights(self):
        z = field(self.lat, self.lon, lambda la, lo: 5500.0)
        self.assertAlmostEqual(B.sector_mean(z, self.lat, self.lon), 5500.0)


class TestEpisodes(unittest.TestCase):
    def test_sector_contiguity(self):
        from etl.indicators import exploratoire as E
        bits = ["0"] * 49
        for i in (20, 21):                       # 2 longitudes contiguës dans le secteur : insuffisant
            bits[i] = "1"
        self.assertFalse(E.sector_blocked("".join(bits)))
        bits[22] = "1"
        self.assertTrue(E.sector_blocked("".join(bits)))
        far = ["0"] * 49
        for i in (0, 1, 2):                      # −60 à −55° : hors secteur
            far[i] = "1"
        self.assertFalse(E.sector_blocked("".join(far)))

    def test_episode_persistence(self):
        from etl.indicators import exploratoire as E
        flags = {f"2001-01-{d:02d}": d in (1, 2, 3, 4, 10, 11, 12, 13, 14) for d in range(1, 20)}
        self.assertEqual(E.episode_days(flags), {f"2001-01-{d:02d}" for d in (10, 11, 12, 13, 14)})

    def test_winter_includes_previous_december(self):
        from etl.indicators import exploratoire as E
        days = E.season_days(2001, "hiver")
        self.assertEqual((days[0], days[-1], len(days)), ("2000-12-01", "2001-02-28", 90))


if __name__ == "__main__":
    unittest.main()
