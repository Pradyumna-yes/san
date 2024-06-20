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
# Copyright (c) 2018-2023 United States Government as represented by
# the National Aeronautics and Space Administration. No copyright is
# claimed in the United States under Title 17, U.S.Code. All Other
# Rights Reserved.
#

"""
Example Coordinate Data Analysis System (CDAS) web service client.
Includes example calls to most of the web services.

Copyright &copy; 2018-2023 United States Government as represented by the
National Aeronautics and Space Administration. No copyright is claimed in
the United States under Title 17, U.S.Code. All Other Rights Reserved.
"""

import sys
import getopt
import json
import logging
import logging.config
from typing import List
import urllib3
#import matplotlib.pyplot as plt
from cdasws import CdasWs
from cdasws.timeinterval import TimeInterval
from cdasws.datarequest import GraphOptions, ImageFormat, Overplot, TextFormat
from cdasws.datarepresentation import DataRepresentation


logging.basicConfig()
LOGGING_CONFIG_FILE = 'logging_config.json'
try:
    with open(LOGGING_CONFIG_FILE, 'r') as fd:
        logging.config.dictConfig(json.load(fd))
except BaseException as exc:    # pylint: disable=broad-except
    if not isinstance(exc, FileNotFoundError):
        print('Logging configuration failed')
        print('Exception: ', exc)
        print('Ignoring failure')
        print()


ENDPOINT = 'https://cdaweb.gsfc.nasa.gov/WS/cdasr/1/dataviews/sp_phys/'
#CA_CERTS = '/etc/pki/ca-trust/extracted/openssl/ca-bundle.trust.crt'


def print_usage(
        name: str
    ) -> None:
    """
    Prints program usage information to stdout.

    Parameters
    ----------
    name
        name of this program

    Returns
    -------
    None
    """
    print('USAGE: {name} [-e url][-d][-c cacerts][-h]'.format(name=name))
    print('WHERE: url = CDAS web service endpoint URL')
    print('       -d disables TLS server certificate validation')
    print('       cacerts = CA certificate filename')


def example(
        argv: List[str]
    ) -> None: # pylint: disable=too-many-locals,too-many-branches,too-many-statements
    """
    Example Coordinate Data Analysis System (CDAS) web service client.
    Includes example calls to most of the web services.

    Parameters
    ----------
    argv
        Command-line arguments.<br>
        -e url or --endpoint=url where url is the cdas web service endpoint
            URL to use.<br>
        -c url or --cacerts=filename where filename is the name of the file
            containing the CA certificates to use.<br>
        -d or --disable-cert-check to disable verification of the server's
            certificate
        -h or --help prints help information.
    """

    try:
        opts = getopt.getopt(argv[1:], 'he:c:d',
                             ['help', 'endpoint=', 'cacerts=',
                              'disable-cert-check'])[0]
    except getopt.GetoptError:
        print('ERROR: invalid option')
        print_usage(argv[0])
        sys.exit(2)

#    logger = logging.getLogger(__name__)

    endpoint = ENDPOINT
    ca_certs = None
    disable_ssl_certificate_validation = False

    for opt, arg in opts:
        if opt in ('-e', '--endpoint'):
            endpoint = arg
        elif opt in ('-c', '--cacerts'):
            ca_certs = arg
        elif opt in ('-d', '--disable-cert-check'):
            disable_ssl_certificate_validation = True
            urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        elif opt in ('-h', '--help'):
            print_usage(argv[0])
            sys.exit()

    cdas = CdasWs(endpoint=endpoint, ca_certs=ca_certs,
                  disable_ssl_certificate_validation=
                  disable_ssl_certificate_validation, user_agent='Example')

    print(cdas.get_observatory_groups(
        instrumentType='Magnetic Fields (Balloon)'))
    print(cdas.get_instrument_types(observatory='AC'))
    print(cdas.get_instruments(observatory='AC'))
    print(cdas.get_observatories(
        instrumentType='Magnetic Fields (space)'))
    #print(cdas.get_observatory_groups_and_instruments(\
    #               instrumentType='Magnetic Fields (space)'))
    datasets = cdas.get_datasets(observatoryGroup=['ACE'],
                                 instrumentType='Magnetic Fields (space)')
    print('Datasets:')
    for dataset in datasets:
        print('  ', dataset['Id'], dataset['Label'])
        #print('  ', json.dumps(dataset, indent=4))

    print('DOI landing page:',
          cdas.get_doi_landing_page_url('10.48322/e0dc-0h53'))

    mms_brst_inventory = cdas.get_inventory('MMS1_FPI_BRST_L2_DES-MOMS',
                                            timeInterval=TimeInterval(
                                                '2018-08-30T08:09:53Z',
                                                '2018-08-30T08:52:00Z'))
    print('MMS1_FPI_BRST_L2_DES-MOMS inventory:')
    for interval in mms_brst_inventory:
        print('    ' + str(interval))

    doi_inventory = cdas.get_inventory('10.21978/P8T923')
    print('10.21978/P8T923 inventory:')
    for interval in doi_inventory:
        print('    ' + str(interval))

    print('AC_H0_MFI example time interval:')
    print('    ', cdas.get_example_time_interval('AC_H0_MFI'))
    print('MMS1_FPI_BRST_L2_DES-MOMS example time interval:')
    print('    ', cdas.get_example_time_interval('MMS1_FPI_BRST_L2_DES-MOMS'))

    test_ds = 'AC_H1_MFI'
    variables = cdas.get_variables(test_ds)
    if variables is not None:
        print(test_ds, ' Variable Names:')
        for variable in variables:
            print('    ' + variable['Name'])

    try:
        time_intervals = [
            TimeInterval('2009-06-01T00:00:00Z', '2009-06-01T00:10:00Z'),
            TimeInterval('2009-06-02T00:00:00Z', '2009-06-02T00:10:00Z')
        ]
        status, data = \
            cdas.get_data('AC_H1_MFI', ['Magnitude', 'BGSEc'],
                          time_intervals,
                          #'2009-06-01T00:00:00Z', '2009-06-01T01:00:00Z'
                          #binData={
                          #    'interval': 60.0,
                          #    'interpolateMissingValues': True,
                          #    'sigmaMultiplier': 4,
                          #    'overrideDefaultBinning': True
                          #}
                          )
#            cdas.get_data('10.21978/P8PG8V', ['BT'],
#                          '1987-09-24T00:00:00Z', '1987-09-24T01:00:00Z'

        if status['http']['status_code'] == 200:
            print("Results from cdas.get_data('AC_H1_MFI', ['Magnitude', 'BGSEc'], time_intervals)")
            print(data.attrs['TITLE'][0], '  ', data.attrs['Data_type'][0])
            print(data)
            #print(data.attrs)
            #plt.plot(data['Epoch'], data['Magnitude'])
            #plt.xlabel(data['Epoch'].attrs['LABLAXIS'])
            #plt.ylabel(data['Magnitude'].attrs['LABLAXIS'] + ' ' +
            #           data['Magnitude'].attrs['UNITS'])
            #plt.show()
        else:
            print('Request failed with status = ', status)

        print()
        print('Trying the same request again while requesting an xarray representation')
        status, data = \
            cdas.get_data('AC_H1_MFI', ['Magnitude', 'BGSEc'],
                          time_intervals,
                          dataRepresentation=DataRepresentation.XARRAY)

        if status['http']['status_code'] == 200:
            print(data)
            print()
        else:
            print('Request failed with status = ', status)
    except ModuleNotFoundError as exception:
        mod = exception.name
        print('-----------------------------------------------------------')
        print('Skipping this get_data() call because it requires', mod)
        print('To call this get_data() example, install', mod)
        print('and re-run this example.')
        print('That is, do the following:')
        print('pip install', mod)
        print('-----------------------------------------------------------')


    status, result = \
        cdas.get_graph('AC_H1_MFI', ['Magnitude', 'BGSEc'],
                       '2009-06-01T00:00:00Z', '2009-06-01T00:10:00Z',
                       GraphOptions(coarse_noise_filter=True,
                                    x_axis_width_factor=4,
                                    y_axis_height_factor=2,
                                    combine=True,
                                    overplot=Overplot.VECTOR_COMPONENTS),
                       [ImageFormat.PDF]
                       #binData={
                       #    'interval': 60.0,
                       #    'interpolateMissingValues': True,
                       #    'sigmaMultiplier': 4
                       #}
                       )

    if status == 200:
        print(result)
    else:
        print('Request failed with status = ', status)


    status, result = \
        cdas.get_graph('IM_K0_EUV', ['IMAGE'],
                       '2005-01-01T00:00:00Z', '2005-01-02T00:00:00Z')

    if status == 200:
        print(result)

        thumbnail_id = result['FileDescription'][0].get('ThumbnailId', None)
        if thumbnail_id is not None:
            thumbnail = result['FileDescription'][0]['ThumbnailDescription']['NumFrames'] // 2
            status, result = \
                cdas.get_thumbnail('IM_K0_EUV', ['IMAGE'],
                                   '2005-01-01T00:00:00Z',
                                   '2005-01-02T00:00:00Z',
                                   thumbnail_id, thumbnail)
        if status == 200:
            print(result)
        else:
            print('Request failed with status = ', status)
    else:
        print('Request failed with status = ', status)


    status, result = \
        cdas.get_text('AC_H1_MFI', ['Magnitude', 'BGSEc'],
                      '2009-06-01T00:00:00Z', '2009-06-01T00:10:00Z',
                      text_format=TextFormat.CSV2
                      #binData={
                      #    'interval': 60.0,
                      #    'interpolateMissingValues': True,
                      #    'sigmaMultiplier': 4
                      #}
                      )

    if status == 200:
        print(result)
    else:
        print('Request failed with status = ', status)

    status, result = \
        cdas.get_audio('AC_H1_MFI', ['Magnitude', 'BGSEc'],
                       '2009-06-01T00:00:00Z', '2009-06-01T00:10:00Z',
                       #binData={
                       #    'interval': 60.0,
                       #    'interpolateMissingValues': True,
                       #    'sigmaMultiplier': 4
                       #}
                       )

    if status == 200:
        print(result)
    else:
        print('Request failed with status = ', status)

    print('TWINS_M2_ENA ssc_ids: ', cdas.get_ssc_id('TWINS_M2_ENA'))
    print('MMS1_FPI_BRST_L2_DES-MOMS ssc_ids: ',
          cdas.get_ssc_id('MMS1_FPI_BRST_L2_DES-MOMS'))
    #ds_wo_ssc_id = []
    #found_ssc_id = 0
    #all_ds = cdas.get_datasets()
    #for ds in all_ds:
    #    status, ssc_id = cdas.get_ssc_id(ds['Id'])
    #    if ssc_id is None:
    #        ds_wo_ssc_id.append(ds['Id'])
    #    else:
    #        found_ssc_id +=1
    #print('number of ssc_ids found = {:d}/{:d} ({:7.2f}%)'.format(\
    #      found_ssc_id, len(all_ds), float(found_ssc_id) / len(all_ds) * 100.0))
    #print('datasets without ssc id: ', ds_wo_ssc_id)
    #return

if __name__ == '__main__':
    example(sys.argv)
