#!/usr/bin/python

import unittest
import sys
from interment import Interment


class TestInterment(unittest.TestCase):

    def test_name_with_plus_sign(self):

        # plus before name
        i = Interment()
        i.set_name_raw("+ Samuel Nicholl")
        self.assertEqual(i.get_name_first(), "Samuel")
        self.assertEqual(i.get_name_last(), "Nicholl")
        self.assertTrue(i.is_plot_owner())
        self.assertEqual(i.get_name_gender_guess(), "M")
        self.assertEqual(i.get_name_full(), "Samuel Nicholl")

        # plus after name
        j = Interment()
        j.set_name_raw("Charles Reichart +")
        self.assertEqual(j.get_name_first(), "Charles")
        self.assertEqual(j.get_name_last(), "Reichart")
        self.assertTrue(j.is_plot_owner())
        self.assertEqual(j.get_name_gender_guess(), "M")
        self.assertEqual(j.get_name_full(), "Charles Reichart")

    def test_name(self):

        # test salutation
        i = Interment()
        i.set_name_raw("Rev Robert Travis")
        self.assertEqual(i.get_name_salutation(), "Rev")
        self.assertEqual(i.get_name_first(), "Robert")
        self.assertEqual(i.get_name_last(), "Travis")
        self.assertEqual(i.get_name_gender_guess(), "M")
        self.assertEqual(i.get_name_full(), "Rev Robert Travis")

        # can't guess gender based on first name
        j = Interment()
        j.set_name_raw("asdfadsf Smith")
        self.assertEqual(j.get_name_gender_guess(), "Unknown")

        # test archaic suffix abbreviations
        k = Interment()
        k.set_name_raw("James Monroe Jur")
        self.assertEqual(k.get_name_suffix(), "Jr")
        self.assertEqual(k.get_name_first(), "James")
        self.assertEqual(k.get_name_last(), "Monroe")
        self.assertEqual(k.get_name_gender_guess(), "M")
        self.assertEqual(k.get_name_full(), "James Monroe Jr")

        # test abbreviations in first and middle names
        l = Interment()
        l.set_name_raw("Wm Monroe")
        self.assertEqual(l.get_name_first(), "William")
        self.assertEqual(l.get_name_gender_guess(), "M")
        self.assertEqual(l.get_name_full(), "William Monroe")
        m = Interment()
        m.set_name_raw("James Geo Monroe")
        self.assertEqual(m.get_name_first(), "James")
        self.assertEqual(m.get_name_middle(), "George")
        self.assertEqual(m.get_name_full(), "James George Monroe")

        # test child of...
        n = Interment()
        n.set_name_raw("A Male Child Of R Sturgis")
        self.assertEqual(n.get_name_last(), "Sturgis")
        self.assertEqual(n.get_name_gender_guess(), "M")
        o = Interment()
        o.set_name_raw("A Female Child Of Wm L Lowden")
        self.assertEqual(o.get_name_last(), "Lowden")
        self.assertEqual(o.get_name_gender_guess(), "F")
        p = Interment()
        p.set_name_raw("A Child No Name")
        self.assertEqual(p.get_name_last(), None)
        self.assertEqual(p.get_name_full(), "A Child No Name")
        self.assertEqual(p.get_name_gender_guess(), "Unknown")

        # test simple ditto
        q = Interment()
        q.set_name_raw("A Male Child Of J D Warren")
        self.assertEqual(q.get_name_last(), "Warren")
        r = Interment()
        r.set_previous(q)
        r.set_name_raw("Do")
        self.assertEqual(r.get_name_last(), "Warren")

    def test_registry_image_filename(self):
        i = Interment()
        i.set_registry_image_filename_raw("volume 16_009")
        self.assertEqual(i.get_registry_image_filename_raw(), "volume 16_009")
        self.assertEqual(i.get_registry_image_filename(), "Volume 16_009")
        self.assertEqual(i.get_registry_volume(), "16")
        self.assertEqual(i.get_registry_page(), "009")

        j = Interment()
        j.set_registry_image_filename_raw("asdfa 0_00a")
        self.assertEqual(j.get_registry_volume(), None)
        self.assertEqual(j.get_registry_page(), None)
        self.assertEqual(j.get_registry_image_filename(), None)

    def test_interment_year_lookup(self):
        i = Interment()
        i.set_id(121920)
        i.set_registry_image_filename_raw("Volume 16_002")
        self.assertEqual(i.get_interment_date_year(), 1866)
        # id not found
        j = Interment()
        j.set_id(999999)
        j.set_registry_image_filename_raw("Volume 16_002")
        self.assertEqual(j.get_interment_date_year(), None)
        self.assertTrue(j.get_needs_review())
        # volume not found
        k = Interment()
        k.set_id(999999)
        k.set_registry_image_filename_raw("Volume 999_002")
        self.assertEqual(k.get_interment_date_year(), None)
        self.assertTrue(k.get_needs_review())

    def test_interment_date(self):
        i = Interment()
        i.set_id(121920)
        i.set_registry_image_filename_raw("Volume 16_002")
        i.set_interment_date("December", 4)
        self.assertEqual(i.get_interment_date_year(), 1866)
        self.assertEqual(i.get_interment_date_display(), "December 4, 1866")
        self.assertEqual(i.get_interment_date_iso(), "1866-12-04")
        # misspelled month
        j = Interment()
        j.set_id(121920)
        j.set_registry_image_filename_raw("Volume 16_002")
        j.set_interment_date("dicember", 12)
        self.assertEqual(j.get_interment_date_iso(), None)
        self.assertTrue(j.get_needs_review())
        # impossible day of month
        k = Interment()
        k.set_id(121920)
        k.set_registry_image_filename_raw("Volume 16_002")
        k.set_interment_date("February", 31)
        self.assertEqual(k.get_interment_date_year(), 1866)
        self.assertEqual(k.get_interment_date_display(), "February 31, 1866")
        self.assertEqual(k.get_interment_date_iso(), None)
        self.assertTrue(k.get_needs_review())
        # infer date from previous entry
        l = Interment()
        l.set_id(121920)
        l.set_registry_image_filename_raw("Volume 16_002")
        l.set_interment_date("February", 28)
        self.assertEqual(l.get_interment_date_year(), 1866)
        self.assertEqual(l.get_interment_date_display(), "February 28, 1866")
        self.assertEqual(l.get_interment_date_iso(), "1866-02-28")
        m = Interment()
        m.set_id(121921)
        m.set_registry_image_filename_raw("Volume 16_002")
        m.set_previous(l)
        m.set_interment_date(None, None)
        self.assertEqual(m.get_interment_date_year(), 1866)
        self.assertEqual(m.get_interment_date_display(), "February 28, 1866")
        self.assertEqual(m.get_interment_date_iso(), "1866-02-28")

    def test_death_date(self):
        i = Interment()
        i.set_id(121920)
        i.set_registry_image_filename_raw("Volume 16_002")
        i.set_death_date("December", 4)
        self.assertEqual(i.get_death_date_year(), 1866)
        self.assertEqual(i.get_death_date_display(), "December 4, 1866")
        self.assertEqual(i.get_death_date_iso(), "1866-12-04")
        # misspelled month
        j = Interment()
        j.set_id(121920)
        j.set_registry_image_filename_raw("Volume 16_002")
        j.set_death_date("dicember", 12)
        self.assertEqual(j.get_death_date_iso(), None)
        self.assertTrue(j.get_needs_review())
        # impossible day of month
        k = Interment()
        k.set_id(121920)
        k.set_registry_image_filename_raw("Volume 16_002")
        k.set_death_date("February", 31)
        self.assertEqual(k.get_death_date_year(), 1866)
        self.assertEqual(k.get_death_date_display(), "February 31, 1866")
        self.assertEqual(k.get_death_date_iso(), None)
        self.assertTrue(k.get_needs_review())
        # infer date from previous entry
        l = Interment()
        l.set_id(121920)
        l.set_registry_image_filename_raw("Volume 16_002")
        l.set_death_date("February", 28)
        self.assertEqual(l.get_death_date_year(), 1866)
        self.assertEqual(l.get_death_date_display(), "February 28, 1866")
        self.assertEqual(l.get_death_date_iso(), "1866-02-28")
        m = Interment()
        m.set_id(121921)
        m.set_registry_image_filename_raw("Volume 16_002")
        m.set_previous(l)
        m.set_death_date('', None)
        self.assertEqual(m.get_death_date_year(), 1866)
        self.assertEqual(m.get_death_date_display(), "February 28, 1866")
        self.assertEqual(m.get_death_date_iso(), "1866-02-28")

    def test_birth_place(self):
        # test country only
        i = Interment()
        i.set_id(121920)
        i.set_registry_image_filename_raw("Volume 16_002")
        i.set_birth_place_raw('France')
        self.assertEqual(i.get_birth_geo_country_short(), 'FR')
        # test nonsense place name
        j = Interment()
        j.set_id(121920)
        j.set_registry_image_filename_raw("Volume 16_002")
        j.set_birth_place_raw('zzzzzzzzzzzzzzzz')
        self.assertTrue(j.get_needs_review())
        self.assertEqual(j.get_birth_place_comments(), "Can't find transcribed place in geocoded place.")
        # test ditto place
        k = Interment()
        k.set_id(121920)
        k.set_registry_image_filename_raw("Volume 16_002")
        k.set_birth_place_raw('Brooklyn')
        l = Interment()
        l.set_id(121941)
        l.set_previous(k)
        l.set_birth_place_raw('"')
        self.assertEqual(l.get_birth_geo_city(), "Brooklyn")
        # test complicated ditto
        m = Interment()
        m.set_id(121920)
        m.set_registry_image_filename_raw("Volume 16_002")
        m.set_birth_place_raw('" State')
        self.assertEqual(m.get_birth_geo_city(), '')
        # test empty birth place
        n = Interment()
        n.set_id(121920)
        n.set_registry_image_filename_raw("Volume 16_002")
        n.set_birth_place_raw('')
        self.assertEqual(m.get_birth_geo_city(), '')
        # test abbrevs
        o = Interment()
        o.set_id(121920)
        o.set_registry_image_filename_raw("Volume 16_002")
        o.set_birth_place_raw('Bn E.D.')
        self.assertEqual(o.get_birth_place_raw_expand_abbreviations(), 'Brooklyn Eastern District')
        # print(n.to_csv())

    def test_death_place(self):
        # test country only
        i = Interment()
        i.set_id(121920)
        i.set_registry_image_filename_raw("Volume 16_002")
        i.set_death_place_raw('Us')
        self.assertEqual(i.get_death_geo_country_short(), 'US')
        # test nonsense place name
        j = Interment()
        j.set_id(121920)
        j.set_registry_image_filename_raw("Volume 16_002")
        j.set_death_place_raw('zzzzzzzzzzzzzzzz')
        self.assertTrue(j.get_needs_review())
        self.assertEqual(j.get_death_place_comments(), "Can't find transcribed place in geocoded place.")
        # test ditto place
        k = Interment()
        k.set_id(121920)
        k.set_registry_image_filename_raw("Volume 16_002")
        k.set_death_place_raw('Brooklyn')
        l = Interment()
        l.set_id(121941)
        l.set_previous(k)
        l.set_death_place_raw('"')
        self.assertEqual(l.get_death_geo_city(), "Brooklyn")
        # test complicated ditto
        m = Interment()
        m.set_id(121920)
        m.set_registry_image_filename_raw("Volume 16_002")
        m.set_death_place_raw('" Ed')
        self.assertEqual(m.get_death_geo_city(), '')
        self.assertTrue(m.get_needs_review())
        # test empty death place
        n = Interment()
        n.set_id(121920)
        n.set_registry_image_filename_raw("Volume 16_002")
        n.set_death_place_raw('')
        self.assertEqual(m.get_death_geo_city(), '')
        # test abbrevs
        o = Interment()
        o.set_id(121920)
        o.set_registry_image_filename_raw("Volume 16_002")
        o.set_death_place_raw('Bn E.D.')
        self.assertEqual(o.get_death_place_raw_expand_abbreviations(), 'Brooklyn Eastern District')
        # print(n.to_csv())

    def test_residence_place(self):
        i = Interment()
        i.set_id(1234567)
        i.set_residence_place_street_raw('199 West 20Th')
        i.set_residence_place_city_raw('New York')
        i.set_residence_place_geocode()
        self.assertEqual(i.get_residence_place_city_raw(), 'New York')
        self.assertEqual(i.get_residence_place_city_full(), 'New York')
        self.assertEqual(i.get_residence_place_street_raw(), '199 West 20Th')
        self.assertEqual(i.get_residence_place_full(), '199 W 20th St, New York, NY 10011, USA')
        # test ditto
        j = Interment()
        j.set_previous(i)
        j.set_residence_place_city_raw('"')
        j.set_residence_place_street_raw("9 Varick Place")
        j.set_residence_place_geocode()
        self.assertEqual(j.get_residence_place_city_full(), 'New York')
        self.assertEqual(j.get_residence_place_city_raw(), '"')
        self.assertEqual(j.get_residence_place_street_raw(), '9 Varick Place')
        self.assertEqual(j.get_residence_place_full(), '9 Warwick Pl, Port Washington, NY 11050, USA')
        # test empty street
        k = Interment()
        k.set_residence_place_street_raw('-')
        k.set_residence_place_city_raw('New Jersey')
        k.set_residence_place_geocode()
        self.assertEqual(k.get_residence_place_street_full(), '')
        self.assertEqual(k.get_residence_place_full(), 'New Jersey, USA')
        # test abbreviation
        l = Interment()
        l.set_residence_place_city_raw('Hancock Mich')
        l.set_residence_place_street_raw('')
        l.set_residence_place_geocode()
        self.assertEqual(l.get_residence_city_raw_expand_abbreviations(), 'Hancock Michigan')
        self.assertEqual(l.get_residence_place_full(), 'Hancock, MI 49930, USA')

    def test_burial_location_lot(self):
        i = Interment()
        i.set_id(121920)
        i.set_burial_location_lot_raw("21524 [15588]")
        self.assertEqual(i.get_burial_location_lot_raw(), "21524 [15588]")
        self.assertEqual(i.get_burial_location_lot(), "21524")
        self.assertEqual(i.get_burial_location_lot_strike(), "15588")
        # strike through only
        j = Interment()
        j.set_id(121920)
        j.set_burial_location_lot_raw("[15588]")
        self.assertEqual(j.get_burial_location_lot_raw(), "[15588]")
        self.assertEqual(j.get_burial_location_lot(), "")
        self.assertEqual(j.get_burial_location_lot_strike(), "15588")
        # no strike through
        k = Interment()
        k.set_id(121920)
        k.set_burial_location_lot_raw("21524")
        self.assertEqual(k.get_burial_location_lot_raw(), "21524")
        self.assertEqual(k.get_burial_location_lot(), "21524")
        self.assertEqual(k.get_burial_location_lot_strike(), None)
        # multiple strike through
        l = Interment()
        l.set_id(121920)
        l.set_burial_location_lot_raw("21524 [15588] [15589]")
        self.assertEqual(l.get_burial_location_lot_raw(), "21524 [15588] [15589]")
        self.assertEqual(l.get_burial_location_lot(), "21524")
        self.assertEqual(l.get_burial_location_lot_strike(), "15588 15589")
        # todo: account for mistyped end bracket? e.g. 18150 [11193[
        # m = Interment()
        # m.set_id(121920)
        # m.set_burial_location_lot_raw("18150 [11193[")
        # self.assertEqual(m.get_burial_location_lot_raw(), "18150 [11193[")
        # self.assertEqual(m.get_burial_location_lot(), "18150")
        # self.assertEqual(m.get_burial_location_lot_strike(), "18150")
        # strike through contains no numbers
        n = Interment()
        n.set_id(121920)
        n.set_burial_location_lot_raw("24246 [\"]")
        self.assertEqual(n.get_burial_location_lot_raw(), "24246 [\"]")
        self.assertEqual(n.get_burial_location_lot(), "24246")
        self.assertEqual(n.get_burial_location_lot_strike(), "\"")
        self.assertEqual(n.get_burial_location_lot_strike_comments(), "Contains no numbers.")
        # ditto test
        p = Interment()
        p.set_id(121920)
        p.set_burial_location_lot_raw("21524")
        self.assertEqual(p.get_burial_location_lot(), "21524")
        q = Interment()
        q.set_id(121921)
        q.set_previous(p)
        q.set_burial_location_lot_raw("\"")
        self.assertEqual(q.get_burial_location_lot(), "21524")

    def test_burial_location_grave(self):
        i = Interment()
        i.set_id(121920)
        i.set_burial_location_grave_raw("13 & 733")
        self.assertEqual(i.get_burial_location_grave_raw(), "13 & 733")
        self.assertEqual(i.get_burial_location_grave(), "13 & 733")
        self.assertEqual(i.get_burial_location_grave_strike(), None)
        # strike through only
        j = Interment()
        j.set_id(121920)
        j.set_burial_location_grave_raw("[161]")
        self.assertEqual(j.get_burial_location_grave_raw(), "[161]")
        self.assertEqual(j.get_burial_location_grave(), "")
        self.assertEqual(j.get_burial_location_grave_strike(), "161")
        # no strike through
        k = Interment()
        k.set_id(121920)
        k.set_burial_location_grave_raw("551")
        self.assertEqual(k.get_burial_location_grave_raw(), "551")
        self.assertEqual(k.get_burial_location_grave(), "551")
        self.assertEqual(k.get_burial_location_grave_strike(), None)
        # mixed
        l = Interment()
        l.set_id(121920)
        l.set_burial_location_grave_raw("2 & 3 - [439]")
        self.assertEqual(l.get_burial_location_grave_raw(), "2 & 3 - [439]")
        self.assertEqual(l.get_burial_location_grave(), "2 & 3 -")
        self.assertEqual(l.get_burial_location_grave_strike(), "439")
        # multiple strike through, no space between
        m = Interment()
        m.set_id(121920)
        m.set_burial_location_grave_raw("[398][700]")
        self.assertEqual(m.get_burial_location_grave_raw(), "[398][700]")
        self.assertEqual(m.get_burial_location_grave(), "")
        self.assertEqual(m.get_burial_location_grave_strike(), "398 700")
        # multiple strike through, no space between
        n = Interment()
        n.set_id(121920)
        n.set_burial_location_grave_raw("FROM THE CEMETERY")
        self.assertEqual(n.get_burial_location_grave_raw(), "FROM THE CEMETERY")
        self.assertEqual(n.get_burial_location_grave(), "FROM THE CEMETERY")
        self.assertEqual(n.get_burial_location_grave_comments(), "Contains no numbers.")
        # empty grave number
        o = Interment()
        o.set_id(121920)
        o.set_burial_location_grave_raw("")
        self.assertEqual(o.get_burial_location_grave_raw(), "")
        self.assertEqual(o.get_burial_location_grave(), "")
        self.assertEqual(o.get_burial_location_grave_comments(), None)
        # ditto test
        p = Interment()
        p.set_id(121920)
        p.set_burial_location_grave_raw("551")
        self.assertEqual(p.get_burial_location_grave(), "551")
        q = Interment()
        q.set_id(121921)
        q.set_previous(p)
        q.set_burial_location_grave_raw("\"")
        self.assertEqual(q.get_burial_location_grave(), "551")

    def test_age(self):
        i = Interment()
        i.set_id(121920)
        i.set_age_years_raw('1')
        i.set_age_months_raw('10')
        i.set_age_days_raw('13')
        self.assertEqual(i.get_age_display(), "1 year 10 months 13 days")
        j = Interment()
        j.set_id(121921)
        j.set_age_years_raw('49')
        j.set_age_months_raw('-')
        j.set_age_days_raw('-')
        self.assertEqual(j.get_age_months(), 0)
        self.assertEqual(j.get_age_days(), 0)
        self.assertEqual(j.get_age_display(), "49 years")
        k = Interment()
        k.set_id(121921)
        k.set_age_years_raw('49')
        k.set_age_months_raw('')
        k.set_age_days_raw('')
        self.assertEqual(k.get_age_months(), 0)
        self.assertEqual(k.get_age_days(), 0)
        self.assertEqual(k.get_age_display(), "49 years")
        l = Interment()
        l.set_id(121921)
        l.set_age_years_raw('')
        l.set_age_months_raw('')
        l.set_age_days_raw('')
        self.assertEqual(l.get_age_months(), 0)
        self.assertEqual(l.get_age_days(), 0)
        self.assertEqual(l.get_age_years(), 0)
        self.assertEqual(l.get_age_display(), "Unknown")
        m = Interment()
        m.set_id(121921)
        m.set_age_years_raw('-')
        m.set_age_months_raw('-')
        m.set_age_days_raw('2 1/2')
        self.assertEqual(m.get_age_months(), 0)
        self.assertEqual(m.get_age_years(), 0)
        self.assertEqual(m.get_age_days(), 2)
        self.assertEqual(m.get_age_hours(), 12)
        self.assertEqual(m.get_age_display(), "2 days 12 hours")
        n = Interment()
        n.set_id(121921)
        n.set_age_years_raw('')
        n.set_age_months_raw('')
        n.set_age_days_raw('2 1/4')
        self.assertEqual(n.get_age_months(), 0)
        self.assertEqual(n.get_age_years(), 0)
        self.assertEqual(n.get_age_days(), 2)
        self.assertEqual(n.get_age_hours(), 6)
        self.assertEqual(n.get_age_display(), "2 days 6 hours")
        o = Interment()
        o.set_id(121921)
        o.set_age_years_raw('')
        o.set_age_months_raw('')
        o.set_age_days_raw('2 3/4')
        self.assertEqual(o.get_age_months(), 0)
        self.assertEqual(o.get_age_years(), 0)
        self.assertEqual(o.get_age_days(), 2)
        self.assertEqual(o.get_age_hours(), 18)
        self.assertEqual(o.get_age_display(), "2 days 18 hours")
        p = Interment()
        p.set_id(121921)
        p.set_age_years_raw('')
        p.set_age_months_raw('')
        p.set_age_days_raw('17 Hours')
        self.assertEqual(p.get_age_months(), 0)
        self.assertEqual(p.get_age_years(), 0)
        self.assertEqual(p.get_age_days(), 0)
        self.assertEqual(p.get_age_hours(), 17)
        self.assertEqual(p.get_age_display(), "17 hours")
        q = Interment()
        q.set_id(121921)
        q.set_age_years_raw('')
        q.set_age_months_raw('')
        q.set_age_days_raw('1 Hr')
        self.assertEqual(q.get_age_months(), 0)
        self.assertEqual(q.get_age_years(), 0)
        self.assertEqual(q.get_age_days(), 0)
        self.assertEqual(q.get_age_hours(), 1)
        self.assertEqual(q.get_age_display(), "1 hour")
        r = Interment()
        r.set_id(121921)
        r.set_age_years_raw('')
        r.set_age_months_raw('')
        r.set_age_days_raw('FROM CEMETERY')
        self.assertEqual(r.get_age_months(), 0)
        self.assertEqual(r.get_age_years(), 0)
        self.assertEqual(r.get_age_days(), 0)
        self.assertTrue(r.get_needs_review())
        self.assertEqual(r.get_age_days_comments(), "Age in days isn't a number or dash")

    def test_marital_status(self):
        i = Interment()
        i.set_id(121920)
        i.set_marital_status_raw('M')
        self.assertEqual(i.get_marital_status(), "Married")
        j = Interment()
        j.set_id(121921)
        j.set_marital_status_raw('S')
        self.assertEqual(j.get_marital_status(), "Single")
        k = Interment()
        k.set_id(121921)
        k.set_marital_status_raw('W')
        self.assertEqual(k.get_marital_status(), "Widow")
        l = Interment()
        l.set_id(121921)
        l.set_marital_status_raw('')
        self.assertEqual(l.get_marital_status(), "Not recorded")
        m = Interment()
        m.set_id(121923)
        m.set_previous(i)
        m.set_marital_status_raw('"')
        self.assertEqual(m.get_marital_status(), "Married")
        n = Interment()
        n.set_id(121923)
        n.set_previous(l)
        n.set_marital_status_raw('"')
        self.assertEqual(n.get_marital_status(), "Not recorded")
        self.assertTrue(n.get_needs_review())
        o = Interment()
        o.set_id(121921)
        o.set_marital_status_raw('FROM CEMETERY')
        self.assertEqual(o.get_marital_status(), "Not recorded")
        self.assertEqual(o.get_marital_status_comments(), 'Marital status not found in list')
        self.assertTrue(o.get_needs_review())

    def test_cause_of_death(self):
        i = Interment()
        i.set_id(121920)
        i.set_cause_of_death_raw('Apoplexia')
        self.assertEqual(i.get_cause_of_death_display(), "Apoplexia")
        # ditto
        j = Interment()
        j.set_id(12121)
        j.set_previous(i)
        j.set_cause_of_death_raw('"')
        self.assertEqual(j.get_cause_of_death_display(), "Apoplexia")
        k = Interment()
        k.set_previous(i)
        k.set_cause_of_death_raw('Do')
        self.assertEqual(k.get_cause_of_death_display(), "Apoplexia")
        # empty
        l = Interment()
        l.set_cause_of_death_raw('-')
        self.assertEqual(l.get_cause_of_death_display(), "")
        m = Interment()
        m.set_cause_of_death_raw('')
        self.assertEqual(m.get_cause_of_death_display(), "")

    def test_undertaker(self):
        i = Interment()
        i.set_id(121920)
        i.set_undertaker_raw('Jonas Stolts')
        self.assertEqual(i.get_undertaker_display(), "Jonas Stolts")
        # ditto
        j = Interment()
        j.set_id(12121)
        j.set_previous(i)
        j.set_undertaker_raw('"')
        self.assertEqual(j.get_undertaker_display(), "Jonas Stolts")
        k = Interment()
        k.set_previous(i)
        k.set_undertaker_raw('Do')
        self.assertEqual(k.get_undertaker_display(), "Jonas Stolts")
        # empty
        l = Interment()
        l.set_undertaker_raw('-')
        self.assertEqual(l.get_undertaker_display(), "")
        m = Interment()
        m.set_undertaker_raw('')
        self.assertEqual(m.get_undertaker_display(), "")

    def test_remarks(self):
        i = Interment()
        i.set_id(121920)
        i.set_remarks_raw('May 3 1867')
        self.assertEqual(i.get_remarks_display(), "May 3 1867")
        # ditto
        j = Interment()
        j.set_id(12121)
        j.set_previous(i)
        j.set_remarks_raw('"')
        self.assertEqual(j.get_remarks_display(), "May 3 1867")
        k = Interment()
        k.set_previous(i)
        k.set_remarks_raw('Do')
        self.assertEqual(k.get_remarks_display(), "May 3 1867")
        # empty
        l = Interment()
        l.set_remarks_raw('-')
        self.assertEqual(l.get_remarks_display(), "")
        m = Interment()
        m.set_remarks_raw('')
        self.assertEqual(m.get_remarks_display(), "")


if __name__ == '__main__':
    unittest.main()
