#!/usr/bin/env python3

#
# NOSA HEADER START
#
# The contents of this file are subject to the terms of the NASA Open
# Source Agreement (NOSA), Version 1.3 only (the "Agreement").  You may
# not use this file except in compliance with the Agreement.
#
# You can obtain a copy of the agreement at
#   docs/NASA_Open_Source_Agreement_1.3.txt
# or
#   https://cdaweb.gsfc.nasa.gov/WebServices/NASA_Open_Source_Agreement_1.3.txt.
#
# See the Agreement for the specific language governing permissions
# and limitations under the Agreement.
#
# When distributing Covered Code, include this NOSA HEADER in each
# file and include the Agreement file at
# docs/NASA_Open_Source_Agreement_1.3.txt.  If applicable, add the
# following below this NOSA HEADER, with the fields enclosed by
# brackets "[]" replaced with your own identifying information:
# Portions Copyright [yyyy] [name of copyright owner]
#
# NOSA HEADER END
#
# Copyright (c) 2019 United States Government as represented by
# the National Aeronautics and Space Administration. No copyright is
# claimed in the United States under Title 17, U.S.Code. All Other
# Rights Reserved.
#

"""
Module for unittest of the CdasWs class.<br>

Copyright &copy; 2018-2019 United States Government as represented by the
National Aeronautics and Space Administration. No copyright is claimed in
the United States under Title 17, U.S.Code. All Other Rights Reserved.
"""

#import json
import unittest
import os
import sys
from datetime import datetime, timezone

# pylint: disable=import-error,wrong-import-position
sys.path.append(os.path.abspath('../cdasws'))
from cdasws import CdasWs, TimeInterval
# pylint: enable=import-error,wrong-import-position


# pylint: disable=line-too-long

BARREL_OBSERV_GROUP = [
        {
            "Name": "BARREL",
            "ObservatoryId": [
                "bar_1A",
                "bar_1B",
                "bar_1C",
                "bar_1D",
                "bar_1G",
                "bar_1H",
                "bar_1I",
                "bar_1J",
                "bar_1K",
                "bar_1L",
                "bar_1M",
                "bar_1O",
                "bar_1Q",
                "bar_1R",
                "bar_1S",
                "bar_1T",
                "bar_1U",
                "bar_1V",
                "bar_2A",
                "bar_2B",
                "bar_2C",
                "bar_2D",
                "bar_2E",
                "bar_2F",
                "bar_2I",
                "bar_2K",
                "bar_2L",
                "bar_2M",
                "bar_2N",
                "bar_2O",
                "bar_2P",
                "bar_2Q",
                "bar_2T",
                "bar_2W",
                "bar_2X",
                "bar_2Y"
            ]
        }
    ]

APOLLO12_DATASETS = [
        {
            "Id": "APOLLO12_SWS_1HR",
            "Observatory": [
                "ALSEP"
            ],
            "Instrument": [
                "SWS"
            ],
            "ObservatoryGroup": [
                "Apollo"
            ],
            "InstrumentType": [
                "Particles (space)",
                "Plasma and Solar Wind"
            ],
            "Label": "Apollo 12 Solar Wind measurements at the lunar surface - Conway W. Snyder (Jet Propulsion Laboratory )",
            "TimeInterval": {
                "Start": "1969-11-19T19:30:00.000Z",
                "End": "1976-03-25T08:30:00.000Z"
            },
            "PiName": "Conway W. Snyder",
            "PiAffiliation": "Jet Propulsion Laboratory ",
            "Notes": "https://cdaweb.gsfc.nasa.gov/misc/NotesA.html#APOLLO12_SWS_1HR",
            "DatasetLink": [
                {
                    "Text": "Dataset ",
                    "Title": "Documentation",
                    "Url": "https://nssdc.gsfc.nasa.gov/nmc/publicationDisplay.do?id=B55381-000A"
                },
                {
                    "Text": "Additional Data Services via",
                    "Title": " the Lunar Surface Origins Exploration service (LUNASOX)",
                    "Url": "https://lunasox.gsfc.nasa.gov"
                }
            ]
        },
        {
            "Id": "APOLLO12_SWS_28S",
            "Observatory": [
                "ALSEP"
            ],
            "Instrument": [
                "SWS"
            ],
            "ObservatoryGroup": [
                "Apollo"
            ],
            "InstrumentType": [
                "Particles (space)",
                "Plasma and Solar Wind"
            ],
            "Label": "Apollo 12 Solar Wind measurements at the lunar surface - Conway W. Snyder (Jet Propulsion Laboratory )",
            "TimeInterval": {
                "Start": "1969-11-19T18:42:13.000Z",
                "End": "1976-03-25T08:35:57.000Z"
            },
            "PiName": "Conway W. Snyder",
            "PiAffiliation": "Jet Propulsion Laboratory ",
            "Notes": "https://cdaweb.gsfc.nasa.gov/misc/NotesA.html#APOLLO12_SWS_28S",
            "DatasetLink": [
                {
                    "Text": "Dataset ",
                    "Title": "Documentation",
                    "Url": "https://nssdc.gsfc.nasa.gov/nmc/publicationDisplay.do?id=B55381-000A"
                },
                {
                    "Text": "Additional Data Services via",
                    "Title": " the Lunar Surface Origins Exploration service (LUNASOX)",
                    "Url": "https://lunasox.gsfc.nasa.gov"
                }
            ]
        }
    ]


AC_INSTRUMENT_TYPES = [
        {
            "Name": "Ephemeris/Attitude/Ancillary"
        },
        {
            "Name": "Magnetic Fields (space)"
        },
        {
            "Name": "Particles (space)"
        },
        {
            "Name": "Plasma and Solar Wind"
        }
    ]

ALSEP_INSTRUMENTS = [
        {
            "LongDescription": "Solar Wind Spectrometer",
            "Name": "SWS",
            "ShortDescription": "Solar Wind Spectrometer"
        }
    ]

ALSEP_OBSERVATORY = [
        {
            "LongDescription": "Apollo Lunar Surface Experiment Package",
            "Name": "ALSEP",
            "ShortDescription": "Apollo Lunar Surface Experiment Package"
        }
    ]

BARREL_INSTRUMENTS = [
        {
            "Name": "BARREL",
            "ObservatoryInstruments": [
                {
                    "InstrumentDescription": [
                        {
                            "LongDescription": "MAGNetometer",
                            "Name": "MAGN",
                            "ShortDescription": "MAGNetometer"
                        }
                    ],
                    "Name": "bar_1A"
                },
                {
                    "InstrumentDescription": [
                        {
                            "LongDescription": "MAGNetometer",
                            "Name": "MAGN",
                            "ShortDescription": "MAGNetometer"
                        }
                    ],
                    "Name": "bar_1B"
                },
                {
                    "InstrumentDescription": [
                        {
                            "LongDescription": "MAGNetometer",
                            "Name": "MAGN",
                            "ShortDescription": "MAGNetometer"
                        }
                    ],
                    "Name": "bar_1C"
                },
                {
                    "InstrumentDescription": [
                        {
                            "LongDescription": "MAGNetometer",
                            "Name": "MAGN",
                            "ShortDescription": "MAGNetometer"
                        }
                    ],
                    "Name": "bar_1D"
                },
                {
                    "InstrumentDescription": [
                        {
                            "LongDescription": "MAGNetometer",
                            "Name": "MAGN",
                            "ShortDescription": "MAGNetometer"
                        }
                    ],
                    "Name": "bar_1G"
                },
                {
                    "InstrumentDescription": [
                        {
                            "LongDescription": "MAGNetometer",
                            "Name": "MAGN",
                            "ShortDescription": "MAGNetometer"
                        }
                    ],
                    "Name": "bar_1H"
                },
                {
                    "InstrumentDescription": [
                        {
                            "LongDescription": "MAGNetometer",
                            "Name": "MAGN",
                            "ShortDescription": "MAGNetometer"
                        }
                    ],
                    "Name": "bar_1I"
                },
                {
                    "InstrumentDescription": [
                        {
                            "LongDescription": "MAGNetometer",
                            "Name": "MAGN",
                            "ShortDescription": "MAGNetometer"
                        }
                    ],
                    "Name": "bar_1J"
                },
                {
                    "InstrumentDescription": [
                        {
                            "LongDescription": "MAGNetometer",
                            "Name": "MAGN",
                            "ShortDescription": "MAGNetometer"
                        }
                    ],
                    "Name": "bar_1K"
                },
                {
                    "InstrumentDescription": [
                        {
                            "LongDescription": "MAGNetometer",
                            "Name": "MAGN",
                            "ShortDescription": "MAGNetometer"
                        }
                    ],
                    "Name": "bar_1L"
                },
                {
                    "InstrumentDescription": [
                        {
                            "LongDescription": "MAGNetometer",
                            "Name": "MAGN",
                            "ShortDescription": "MAGNetometer"
                        }
                    ],
                    "Name": "bar_1M"
                },
                {
                    "InstrumentDescription": [
                        {
                            "LongDescription": "MAGNetometer",
                            "Name": "MAGN",
                            "ShortDescription": "MAGNetometer"
                        }
                    ],
                    "Name": "bar_1O"
                },
                {
                    "InstrumentDescription": [
                        {
                            "LongDescription": "MAGNetometer",
                            "Name": "MAGN",
                            "ShortDescription": "MAGNetometer"
                        }
                    ],
                    "Name": "bar_1Q"
                },
                {
                    "InstrumentDescription": [
                        {
                            "LongDescription": "MAGNetometer",
                            "Name": "MAGN",
                            "ShortDescription": "MAGNetometer"
                        }
                    ],
                    "Name": "bar_1R"
                },
                {
                    "InstrumentDescription": [
                        {
                            "LongDescription": "MAGNetometer",
                            "Name": "MAGN",
                            "ShortDescription": "MAGNetometer"
                        }
                    ],
                    "Name": "bar_1S"
                },
                {
                    "InstrumentDescription": [
                        {
                            "LongDescription": "MAGNetometer",
                            "Name": "MAGN",
                            "ShortDescription": "MAGNetometer"
                        }
                    ],
                    "Name": "bar_1T"
                },
                {
                    "InstrumentDescription": [
                        {
                            "LongDescription": "MAGNetometer",
                            "Name": "MAGN",
                            "ShortDescription": "MAGNetometer"
                        }
                    ],
                    "Name": "bar_1U"
                },
                {
                    "InstrumentDescription": [
                        {
                            "LongDescription": "MAGNetometer",
                            "Name": "MAGN",
                            "ShortDescription": "MAGNetometer"
                        }
                    ],
                    "Name": "bar_1V"
                },
                {
                    "InstrumentDescription": [
                        {
                            "LongDescription": "MAGNetometer",
                            "Name": "MAGN",
                            "ShortDescription": "MAGNetometer"
                        }
                    ],
                    "Name": "bar_2A"
                },
                {
                    "InstrumentDescription": [
                        {
                            "LongDescription": "MAGNetometer",
                            "Name": "MAGN",
                            "ShortDescription": "MAGNetometer"
                        }
                    ],
                    "Name": "bar_2B"
                },
                {
                    "InstrumentDescription": [
                        {
                            "LongDescription": "MAGNetometer",
                            "Name": "MAGN",
                            "ShortDescription": "MAGNetometer"
                        }
                    ],
                    "Name": "bar_2C"
                },
                {
                    "InstrumentDescription": [
                        {
                            "LongDescription": "MAGNetometer",
                            "Name": "MAGN",
                            "ShortDescription": "MAGNetometer"
                        }
                    ],
                    "Name": "bar_2D"
                },
                {
                    "InstrumentDescription": [
                        {
                            "LongDescription": "MAGNetometer",
                            "Name": "MAGN",
                            "ShortDescription": "MAGNetometer"
                        }
                    ],
                    "Name": "bar_2E"
                },
                {
                    "InstrumentDescription": [
                        {
                            "LongDescription": "MAGNetometer",
                            "Name": "MAGN",
                            "ShortDescription": "MAGNetometer"
                        }
                    ],
                    "Name": "bar_2F"
                },
                {
                    "InstrumentDescription": [
                        {
                            "LongDescription": "MAGNetometer",
                            "Name": "MAGN",
                            "ShortDescription": "MAGNetometer"
                        }
                    ],
                    "Name": "bar_2I"
                },
                {
                    "InstrumentDescription": [
                        {
                            "LongDescription": "MAGNetometer",
                            "Name": "MAGN",
                            "ShortDescription": "MAGNetometer"
                        }
                    ],
                    "Name": "bar_2K"
                },
                {
                    "InstrumentDescription": [
                        {
                            "LongDescription": "MAGNetometer",
                            "Name": "MAGN",
                            "ShortDescription": "MAGNetometer"
                        }
                    ],
                    "Name": "bar_2L"
                },
                {
                    "InstrumentDescription": [
                        {
                            "LongDescription": "MAGNetometer",
                            "Name": "MAGN",
                            "ShortDescription": "MAGNetometer"
                        }
                    ],
                    "Name": "bar_2M"
                },
                {
                    "InstrumentDescription": [
                        {
                            "LongDescription": "MAGNetometer",
                            "Name": "MAGN",
                            "ShortDescription": "MAGNetometer"
                        }
                    ],
                    "Name": "bar_2N"
                },
                {
                    "InstrumentDescription": [
                        {
                            "LongDescription": "MAGNetometer",
                            "Name": "MAGN",
                            "ShortDescription": "MAGNetometer"
                        }
                    ],
                    "Name": "bar_2O"
                },
                {
                    "InstrumentDescription": [
                        {
                            "LongDescription": "MAGNetometer",
                            "Name": "MAGN",
                            "ShortDescription": "MAGNetometer"
                        }
                    ],
                    "Name": "bar_2P"
                },
                {
                    "InstrumentDescription": [
                        {
                            "LongDescription": "MAGNetometer",
                            "Name": "MAGN",
                            "ShortDescription": "MAGNetometer"
                        }
                    ],
                    "Name": "bar_2Q"
                },
                {
                    "InstrumentDescription": [
                        {
                            "LongDescription": "MAGNetometer",
                            "Name": "MAGN",
                            "ShortDescription": "MAGNetometer"
                        }
                    ],
                    "Name": "bar_2T"
                },
                {
                    "InstrumentDescription": [
                        {
                            "LongDescription": "MAGNetometer",
                            "Name": "MAGN",
                            "ShortDescription": "MAGNetometer"
                        }
                    ],
                    "Name": "bar_2W"
                },
                {
                    "InstrumentDescription": [
                        {
                            "LongDescription": "MAGNetometer",
                            "Name": "MAGN",
                            "ShortDescription": "MAGNetometer"
                        }
                    ],
                    "Name": "bar_2X"
                },
                {
                    "InstrumentDescription": [
                        {
                            "LongDescription": "MAGNetometer",
                            "Name": "MAGN",
                            "ShortDescription": "MAGNetometer"
                        }
                    ],
                    "Name": "bar_2Y"
                }
            ]
        }
    ]

MMS1_FPI_BRST_INVENTORY = [
    TimeInterval("2018-08-30T08:09:53.000Z", "2018-08-30T08:13:12.000Z"),
    TimeInterval("2018-08-30T08:39:23.000Z", "2018-08-30T08:44:02.000Z"),
    TimeInterval("2018-08-30T08:50:43.000Z", "2018-08-30T08:55:02.000Z")
]


AC_H2_MFI_VARIABLES = [
        {
            "LongDescription": "B-field magnitude",
            "Name": "Magnitude",
            "ShortDescription": "magnetic_field>magnitude"
        },
        {
            "LongDescription": "Magnetic Field Vector in GSE Cartesian coordinates (1 hr)",
            "Name": "BGSEc",
            "ShortDescription": "magnetic_field"
        },
        {
            "LongDescription": "Magnetic field vector in GSM coordinates (1 hr)",
            "Name": "BGSM",
            "ShortDescription": ""
        },
        {
            "LongDescription": "ACE s/c position, 3 comp. in GSE coord.",
            "Name": "SC_pos_GSE",
            "ShortDescription": "position>gse_cartesian"
        },
        {
            "LongDescription": "ACE s/c position, 3 comp. in GSM coord.",
            "Name": "SC_pos_GSM",
            "ShortDescription": "position>gsm_cartesian"
        }
    ]


# pylint: enable=line-too-long


class TestCdasWs(unittest.TestCase):
    """
    Class for unittest of CdasWs class.
    """

    def __init__(self, *args, **kwargs):
        super(TestCdasWs, self).__init__(*args, **kwargs)
        self._cdas = CdasWs()


    def test_time_interval_init_exceptions(self):

        with self.assertRaises(ValueError):
            TimeInterval(123, 'bad_datetime')
        

    def test_time_interval_eq(self):

        t1 = TimeInterval('20190101T000000Z', '2019-01-02T00:00:00Z')
        t2 = TimeInterval(datetime(2019, 1, 1, 0, 0, 0, 0, timezone.utc),
                          datetime(2019, 1, 2, 0, 0, 0, 0, timezone.utc))

        self.assertEqual(t1, t2)


    def test_time_interval_basic_iso_format(self):

        self.assertEqual(
            TimeInterval.basic_iso_format(
                datetime(2019, 1, 1, 0, 0, 0, 0, timezone.utc)),
            '20190101T000000Z')


    def test_time_interval_str(self):

        t1 = TimeInterval(datetime(2019, 1, 1, 0, 0, 0, 0, timezone.utc),
                          datetime(2019, 1, 2, 0, 0, 0, 0, timezone.utc))

        self.assertEqual(str(t1), 
            '2019-01-01T00:00:00+00:00 2019-01-02T00:00:00+00:00')


    def test_get_observatory_groups(self):
        """
        Test of get_observatory_group method.
        """

        self.assertListEqual(
            self._cdas.get_observatory_groups(
                instrumentType='Magnetic Fields (Balloon)'),
            BARREL_OBSERV_GROUP)


    def test_get_instrument_types(self):
        """
        Test of get_instrument_types method.
        """

        self.assertListEqual(
            self._cdas.get_instrument_types(observatory='AC'),
            AC_INSTRUMENT_TYPES)


    def test_get_instruments(self):
        """
        Test of get_instruments method.
        """

        self.assertListEqual(
            self._cdas.get_instruments(observatory='ALSEP'),
            ALSEP_INSTRUMENTS)


    def test_get_observatories(self):
        """
        Test of get_observatories method.
        """

        self.assertListEqual(
            self._cdas.get_observatories(instrument='SWS'),
            ALSEP_OBSERVATORY)


    def test_get_observatory_groups_and_instruments(self):
        """
        Test of get_observatory_groups_and_instruments method.
        """

        self.assertListEqual(
            self._cdas.get_observatory_groups_and_instruments(
                instrumentType='Magnetic Fields (Balloon)'),
            BARREL_INSTRUMENTS)


    def test_get_datasets(self):
        """
        Test of get_datasets method.
        """

        self.assertListEqual(
            self._cdas.get_datasets(idPattern='APOLLO12.*'),
            APOLLO12_DATASETS)


    def test_get_inventory(self):
        """
        Test of get_inventory method.
        """

        self.assertListEqual(
            self._cdas.get_inventory(
                'MMS1_FPI_BRST_L2_DES-MOMS',
                timeInterval=TimeInterval('2018-08-30T08:09:53Z',
                                          '2018-08-30T08:52:00Z')),
            MMS1_FPI_BRST_INVENTORY)


    def test_get_variables(self):
        """
        Test of get_variables method.
        """

        self.assertListEqual(
            self._cdas.get_variables('AC_H2_MFI'),
            AC_H2_MFI_VARIABLES)


    def test_get_data_exception(self):
        """
        Test of get_data method exception.
        """

        with self.assertRaises(ValueError):
            self._cdas.get_data('dummy_ds', ['dummy_var'],
                                123, 'bad_datetime')

if __name__ == '__main__':
    unittest.main()
