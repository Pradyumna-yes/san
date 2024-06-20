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
# Copyright (c) 2018-2019 United States Government as represented by
# the National Aeronautics and Space Administration. No copyright is
# claimed in the United States under Title 17, U.S.Code. All Other
# Rights Reserved.
#

"""
Package for accessing the Coordinate Data Analysis System (CDAS)
web services <https://cdaweb.gsfc.nasa.gov/WebServices/REST/>.<br>

Copyright &copy; 2018-2019 United States Government as represented by the
National Aeronautics and Space Administration. No copyright is claimed in
the United States under Title 17, U.S.Code. All Other Rights Reserved.
"""

import os
import platform
import logging
import urllib.parse
import json
from operator import itemgetter
from datetime import datetime, timezone
from tempfile import mkstemp
from typing import Dict, List, Tuple, Union
import requests
import dateutil.parser
import spacepy.datamodel as spdm       # type: ignore



class TimeInterval:
    """
    A time interval constisting of a start and end datetime.

    Attributes
    ----------
    start
        Start time of interval.
    end
        End time of interval.
    """
    def __init__(self, start: Union[datetime, str],
                 end: Union[datetime, str]):
        """
        Constructs a TimeInterval object.

        Parameters
        ----------
        start
            Start time of interval.
        end
            End time of interval.
        Raises
        ------
        ValueError
            If the given start/end datetime values are invalid.
        """

        if isinstance(start, datetime):
            self.start = start
        elif isinstance(start, str):
            self.start = dateutil.parser.parse(start)
        else:
            raise ValueError('unrecognized datetime value')

        self.start.astimezone(timezone.utc)

        if isinstance(end, datetime):
            self.end = end
        elif isinstance(end, str):
            self.end = dateutil.parser.parse(end)
        else:
            raise ValueError('unrecognized datetime value')

        self.end.astimezone(timezone.utc)

    def __str__(self):
        return self.start.isoformat() + ' ' + self.end.isoformat()

    def __eq__(self, other):
        return self.start == other.start and self.end == other.end

    @staticmethod
    def basic_iso_format(value: datetime) -> str:
        """
        Produces the basic (minimal) ISO 8601 format of the given
        datetime.

        Parameters
        ----------
        value
            datetime value to convert to string.
        Returns
        -------
        str
            Basic ISO 8601 format time string.
        """
        return value.isoformat().replace('+00:00', 'Z').translate(
            {ord(i):None for i in ':-'})


# pylint: disable=too-many-instance-attributes
class CdasWs:
    """
    Class representing the web service interface to NASA's
    Coordinated Data Analysis System (CDAS)
    <https://cdaweb.gsfc.nasa.gov>.

    Notes
    -----
    The logger used by this class has the class' name (CdasWs).  By default,
    it is configured with a NullHandler.  Users of this class may configure
    the logger to aid in diagnosing problems.
    """
    # pylint: disable=too-many-arguments
    def __init__(self, endpoint=None, timeout=None, proxy=None,
                 ca_certs=None, disable_ssl_certificate_validation=False):
        """
        Creates an object representing the CDAS web services.

        Parameters
        ----------
        endpoint
            URL of the CDAS web service.  If None, the default is
            'https://cdaweb.gsfc.nasa.gov/WS/cdasr/1/dataviews/sp_phys/'.
        timeout
            Number of seconds to wait for a response from the server.
        proxy
            HTTP proxy information.  For example,
            proxies = {
              'http': 'http://10.10.1.10:3128',
              'https': 'http://10.10.1.10:1080',
            }
            Proxy information can also be set with environment variables.
            For example,
            $ export HTTP_PROXY="http://10.10.1.10:3128"
            $ export HTTPS_PROXY="http://10.10.1.10:1080"
        ca_certs
            Path to certificate authority (CA) certificates that will
            override the default bundle.
        disable_ssl_certificate_validation
            Flag indicating whether to validate the SSL certificate.
        """

        self.logger = logging.getLogger(type(self).__name__)
        self.logger.addHandler(logging.NullHandler())

        if endpoint is None:
            self._endpoint = 'https://cdaweb.gsfc.nasa.gov/WS/cdasr/1/dataviews/sp_phys/'
        else:
            self._endpoint = endpoint

        self._user_agent = 'CdasWsExample.py (' + \
            platform.python_implementation() + ' ' \
            + platform.python_version() + '; ' + platform.platform() + ')'

        self._request_headers = {
            'Content-Type' : 'application/json',
            'Accept' : 'application/json',
            'User-Agent' : self._user_agent,
            #'Accept-Encoding' : 'gzip'  # only beneficial for icdfml responses
        }
        self._session = requests.Session()
        self._session.headers.update(self._request_headers)

        if ca_certs is not None:
            self._session.verify = ca_certs

        if disable_ssl_certificate_validation is True:
            self._session.verify = False

        if proxy is not None:
            self._proxy = proxy

        self._timeout = timeout

    # pylint: enable=too-many-arguments


    def __del__(self):
        """
        Destructor.  Closes all network connections.
        """

        self.close()


    def close(self) -> None:
        """
        Closes any persistent network connections.  Generally, deleting
        this object is sufficient and calling this method is unnecessary.
        """
        self._session.close()


    def get_observatory_groups(self, **keywords) -> List[Dict]:
        """
        Gets descriptions of the observatory groups from the server.

        Parameters
        ----------
        keywords
            instrumentType value.
        Returns
        -------
        List
            An array of ObservatoryGroupDescription
            dictionaries where the structure of the dictionary mirrors
            ObservatoryGroupDescription in
            <https://cdaweb.gsfc.nasa.gov/WebServices/REST/CDAS.xsd>.
        """
        if 'instrumentType' in keywords:
            url = self._endpoint + 'observatoryGroups?instrumentType=' + \
                      urllib.parse.quote(keywords['instrumentType'])
        else:
            url = self._endpoint + 'observatoryGroups'

        self.logger.debug('request url = %s', url)

        response = self._session.get(url, timeout=self._timeout)

        if response.status_code != 200:

            self.logger.info('%s failed with http code %d', url,
                             response.status_code)
            self.logger.info('response.text: %s', response.text)
            return []

        observatory_groups = response.json()

        if self.logger.level <= logging.DEBUG:
            self.logger.debug('observatory_groups: %s',
                              json.dumps(observatory_groups,
                                         indent=4, sort_keys=True))

        if not observatory_groups:
            return []

        return observatory_groups['ObservatoryGroupDescription']


    def get_instrument_types(self, **keywords) -> List[Dict]:
        """
        Gets descriptions of the instrument types from the server.

        Parameters
        ----------
        keywords
            observatory or observatoryGroup value.
        Returns
        -------
        List
            An array of InstrumentTypeDescription
            dictionaries where the structure of the dictionary mirrors
            InstrumentTypeDescription in
            <https://cdaweb.gsfc.nasa.gov/WebServices/REST/CDAS.xsd>.
        """
        if 'observatory' in keywords:
            url = self._endpoint + 'instrumentTypes?observatory=' \
                  + urllib.parse.quote(keywords['observatory'])
        elif 'observatoryGroup' in keywords:
            url = self._endpoint + 'instrumentTypes?observatoryGroup=' \
                  + urllib.parse.quote(keywords['observatoryGroup'])
        else:
            url = self._endpoint + 'instrumentTypes'

        self.logger.debug('request url = %s', url)

        response = self._session.get(url, timeout=self._timeout)

        if response.status_code != 200:

            self.logger.info('%s failed with http code %d', url,
                             response.status_code)
            self.logger.info('response.text: %s', response.text)
            return []

        instrument_types = response.json()

        if self.logger.level <= logging.DEBUG:
            self.logger.debug('instrument_types = %s',
                              json.dumps(instrument_types, indent=4,
                                         sort_keys=True))

        if not instrument_types:
            return []

        return instrument_types['InstrumentTypeDescription']


    def get_instruments(self, **keywords) -> List[Dict]:
        """
        Gets descriptions of the instruments from the server.

        Parameters
        ----------
        keywords
            observatory or instrumentType value.
        Returns
        -------
        List
            An array of InstrumentDescription
            dictionaries where the structure of the dictionary mirrors
            InstrumentDescription in
            <https://cdaweb.gsfc.nasa.gov/WebServices/REST/CDAS.xsd>.
        """
        if 'observatory' in keywords:
            url = self._endpoint + 'instruments?observatory=' \
                  + urllib.parse.quote(keywords['observatory'])
        elif 'instrumentType' in keywords:
            url = self._endpoint + 'instruments?instrumentType=' \
                  + urllib.parse.quote(keywords['instrumentType'])
        else:
            url = self._endpoint + 'instruments'

        self.logger.debug('request url = %s', url)

        response = self._session.get(url, timeout=self._timeout)

        if response.status_code != 200:

            self.logger.info('%s failed with http code %d', url,
                             response.status_code)
            self.logger.info('response.text: %s', response.text)
            return []

        instruments = response.json()

        if self.logger.level <= logging.DEBUG:
            self.logger.debug('instruments = %s',
                              json.dumps(instruments, indent=4,
                                         sort_keys=True))

        if not instruments:
            return []

        return instruments['InstrumentDescription']


    def get_observatories(self, **keywords) -> List[Dict]:
        """
        Gets descriptions of the observatories from the server.

        Parameters
        ----------
        keywords
            instrument or instrumentType value.
        Returns
        -------
        List
            An array of ObservatoryDescriptions
            dictionaries where the structure of the dictionary mirrors
            ObservatoryDescription in
            <https://cdaweb.gsfc.nasa.gov/WebServices/REST/CDAS.xsd>.
        """
        if 'instrument' in keywords:
            url = self._endpoint + 'observatories?instrument=' \
                  + urllib.parse.quote(keywords['instrument'])
        elif 'instrumentType' in keywords:
            url = self._endpoint + 'observatories?instrumentType=' \
                  + urllib.parse.quote(keywords['instrumentType'])
        else:
            url = self._endpoint + 'observatories'

        self.logger.debug('request url = %s', url)

        response = self._session.get(url, timeout=self._timeout)

        if response.status_code != 200:

            self.logger.info('%s failed with http code %d', url,
                             response.status_code)
            self.logger.info('response.text: %s', response.text)
            return []

        observatories = response.json()

        if self.logger.level <= logging.DEBUG:
            self.logger.debug('observatories = %s',
                              json.dumps(observatories, indent=4,
                                         sort_keys=True))

        if not observatories:
            return []

        return observatories['ObservatoryDescription']


    def get_observatory_groups_and_instruments(self, **keywords) -> List[Dict]:
        """
        Gets descriptions of the observatory groups (and associated
        instruments) from the server.

        Parameters
        ----------
        keywords
            instrumentType value.
        Returns
        -------
        List
            An array of ObservatoryGroupInstrumentDescription
            dictionaries where the structure of the dictionary mirrors
            ObservatoryGroupInstrumentDescription in
            <https://cdaweb.gsfc.nasa.gov/WebServices/REST/CDAS.xsd>.
        """
        if 'instrumentType' in keywords:
            url = self._endpoint \
                  + 'observatoryGroupsAndInstruments?instrumentType=' \
                  + urllib.parse.quote(keywords['instrumentType'])
        else:
            url = self._endpoint + 'observatoryGroupsAndInstruments'

        self.logger.debug('request url = %s', url)

        response = self._session.get(url, timeout=self._timeout)

        if response.status_code != 200:

            self.logger.info('%s failed with http code %d', url,
                             response.status_code)
            self.logger.info('response.text: %s', response.text)
            return []

        observatories = response.json()

        if self.logger.level <= logging.DEBUG:
            self.logger.debug('observatories = %s',
                              json.dumps(observatories, indent=4,
                                         sort_keys=True))

        if not observatories:
            return []

        return observatories['ObservatoryGroupInstrumentDescription']


    def get_datasets(self, **keywords) -> List[Dict]:
        """
        Gets descriptions of the specified datasets from the server.

        Parameters
        ----------
        keywords
            observatoryGroup, instrumentType, observatory,
            instrument, startDate, stopDate, idPattern, labelPattern,
            and/or notesPattern value(s).
        Returns
        -------
        List
            A dictionary containing descriptions of the datasets
            requested.  The dictionary structure is defined by the
            DatasetDescription element in
            <https://cdaweb.gsfc.nasa.gov/WebServices/REST/CDAS.xsd>.
        """
        url = self._endpoint + 'datasets?'

        if 'observatoryGroup' in keywords:
            url = url + 'observatoryGroup=' \
                  + urllib.parse.quote(keywords['observatoryGroup']) + '&'

        if 'instrumentType' in keywords:
            url = url + 'instrumentType=' \
                  + urllib.parse.quote(keywords['instrumentType']) + '&'

        if 'observatory' in keywords:
            url = url + 'observatory=' \
                  + urllib.parse.quote(keywords['observatory']) + '&'

        if 'instrument' in keywords:
            url = url + 'instrument=' \
                  + urllib.parse.quote(keywords['instrument']) + '&'

        if 'startDate' in keywords:
            url = url + 'startDate=' \
                  + urllib.parse.quote(keywords['startDate']) + '&'

        if 'stopDate' in keywords:
            url = url + 'stopDate=' \
                  + urllib.parse.quote(keywords['stopDate']) + '&'

        if 'idPattern' in keywords:
            url = url + 'idPattern=' \
                  + urllib.parse.quote(keywords['idPattern']) + '&'

        if 'labelPattern' in keywords:
            url = url + 'labelPattern=' \
                  + urllib.parse.quote(keywords['labelPattern']) + '&'

        if 'notesPattern' in keywords:
            url = url + 'notesPattern=' \
                  + urllib.parse.quote(keywords['notesPattern']) + '&'

        self.logger.debug('request url = %s', url[:-1])

        response = self._session.get(url[:-1], timeout=self._timeout)

        if response.status_code != 200:

            self.logger.info('%s failed with http code %d', url,
                             response.status_code)
            self.logger.info('response.text: %s', response.text)
            return []

        datasets = response.json()

        if self.logger.level <= logging.DEBUG:
            self.logger.debug('datasets = %s',
                              json.dumps(datasets, indent=4, sort_keys=True))

        if not datasets:
            return []

        return sorted(datasets['DatasetDescription'], key=itemgetter('Id'))



    def get_inventory(self, identifier: str, **keywords
                     ) -> List[TimeInterval]:
        """
        Gets a description of the specified dataset's data inventory.

        Parameters
        ----------
        identifier
            dataset identifier of data inventory to get.
        keywords
            time interval value.
        Returns
        -------
        List
            An array of TimeIntervals when data is available.
        """

        url = self._endpoint + 'datasets/' + identifier + '/inventory'

        if 'timeInterval' in keywords:
            time_interval_keyword = keywords['timeInterval']
            url = url + '/' + \
                  TimeInterval.basic_iso_format(time_interval_keyword.start) + \
                  ',' + \
                  TimeInterval.basic_iso_format(time_interval_keyword.end)

        self.logger.debug('request url = %s', url)

        response = self._session.get(url, timeout=self._timeout)

        if response.status_code != 200:

            self.logger.info('%s failed with http code %d', url,
                             response.status_code)
            self.logger.info('response.text: %s', response.text)
            return []

        inventory = response.json()

        if self.logger.level <= logging.DEBUG:
            self.logger.debug('inventory = %s',
                              json.dumps(inventory, indent=4, sort_keys=True))

        intervals = []

        data_intervals = inventory['InventoryDescription'][0]

        if 'TimeInterval' in data_intervals:

            for time_interval in data_intervals['TimeInterval']:

                intervals.append(
                    TimeInterval(
                        time_interval['Start'],
                        time_interval['End']
                    )
                )

        return intervals


    def get_variables(self, identifier: str) -> List[Dict]:
        """
        Gets a description of the variables in the specified dataset.

        Parameters
        ----------
        identifier
            dataset identifier of data to get.
        Returns
        -------
        List
            A dictionary containing descriptions of the variables in
            the specified dataset.  The dictionary structure is defined by
            the VariableDescription element in
            <https://cdaweb.gsfc.nasa.gov/WebServices/REST/CDAS.xsd>.
        """

        url = self._endpoint + 'datasets/' + identifier + '/variables'

        response = self._session.get(url, timeout=self._timeout)

        if response.status_code != 200:

            self.logger.info('%s failed with http code %d', url,
                             response.status_code)
            self.logger.info('response.text: %s', response.text)
            return []

        variables = response.json()

        if not variables:
            return []

        return variables['VariableDescription']


    # pylint: disable=too-many-locals
    # pylint: disable=too-many-return-statements
    # pylint: disable=too-many-statements
    # pylint: disable=too-many-branches
    def get_data(self, dataset: str, variables: List[str],
                 start: Union[datetime, str], end: Union[datetime, str],
                 **keywords
                ) -> Tuple[int, spdm.SpaceData]:
        """
        Gets the specified data from the server.

        Parameters
        ----------
        dataset
            dataset identifier of data to get.
        variables
            array containing names of variables to get.
        start
            start time of data to get.
        end
            end time of data to get.
        keywords
            optional keyword parameters as follows<br>
            binData - indicates that uniformly spaced values should be
            computed for scaler/vector/spectrogram data according to
            the given binning parameter values.  binData may contain
            the following keys: interval, interpolateMissingValues,
            and/or sigmaMultiplier with values that override the
            defaults.<br>
            progressCallback - is a
            typing.Callable[[float, str, typing.Any], int]
            function that is called repeatedly to report the progress
            of getting the data.  The function should return 0 if it
            wants to continue getting data.  If it returns non-0 value,
            getting the data will be aborted and the get_data() function
            will immediately return (204, None).  The float parameter
            is a value between 0.0 and 1.0 to indicate progress and
            the str parameter will contain a text message indicating
            the progress of this call.<br>
            progressUserValue - is a typing.Any value that is passsed
            to the progressCallback function.<br>
        Returns
        -------
        Tuple
            [0] contains a dictionary of HTTP and CDAS status information.
            When successful, ['http']['status_code'] will be 200.<br>
            [1] contains the requested data (SpaceData object) or None.
        Raises
        ------
        ValueError
            If the given start/end datetime values are invalid.
        """

        if isinstance(start, datetime):
            start_datetime = start
        elif isinstance(start, str):
            start_datetime = dateutil.parser.parse(start)
        else:
            raise ValueError('unrecognized start datetime value')

        if isinstance(end, datetime):
            end_datetime = end
        elif isinstance(end, str):
            end_datetime = dateutil.parser.parse(end)
        else:
            raise ValueError('unrecognized end datetime value')

        data_request = {
            'CdfRequest': {
                'CdfFormat': 'Cdf',
                'TimeInterval': {
                    'Start': start_datetime.isoformat(),
                    'End': end_datetime.isoformat()
                },
                'DatasetRequest': {
                    'DatasetId': dataset,
                    'VariableName': variables
                }
            }
        }
        if 'binData' in keywords:
            bin_data_kw = keywords['binData']
            data_request['CdfRequest']['BinData'] = {}
            if 'interval' in bin_data_kw:
                data_request['CdfRequest']['BinData']['Interval'] = \
                    bin_data_kw['interval']
            if 'interpolateMissingValues' in bin_data_kw:
                data_request['CdfRequest']['BinData']['InterpolateMissingValues'] = \
                    bin_data_kw['interpolateMissingValues']
            if 'sigmaMultiplier' in bin_data_kw:
                data_request['CdfRequest']['BinData']['SigmaMultiplier'] = \
                    bin_data_kw['sigmaMultiplier']

        progress_callback = keywords.get('progressCallback', None)
        progress_user_value = keywords.get('progressUserValue', None)

        self.logger.debug('data_request = %s', data_request)

        status = {
            'http': {
                'status_code': 204
            },
            'cdas': {
                'status': [],
                'message': [],
                'warning': [],
                'error': []
            }
        }
        if progress_callback is not None:
            if progress_callback(0.1, 'Making initial server request.',
                                 progress_user_value) != 0:
                return (status, None)

        url = self._endpoint + 'datasets'

        response = self._session.post(url, data=json.dumps(data_request),
                                      timeout=self._timeout)

        status['http']['status_code'] = response.status_code

        if progress_callback is not None:
            if progress_callback(0.2, 'Initial server request complete.',
                                 progress_user_value) != 0:
                return (status, None)

        try:
            data_result = response.json()
            if 'Status' in data_result:
                status['cdas']['status'] = data_result['Status']
            if 'Message' in data_result:
                status['cdas']['message'] = data_result['Message']
            if 'Warning' in data_result:
                status['cdas']['warning'] = data_result['Warning']
            if 'Error' in data_result:
                status['cdas']['error'] = data_result['Error']
        except ValueError:
            # for example, a 503 from apache will not be json
            self.logger.debug('Non-JSON response: %s', response.text)
            status['http']['error_body'] = response.text

        if response.status_code != 200:

            self.logger.info('%s failed with http code %d', url,
                             response.status_code)
            self.logger.info('data_request = %s', data_request)
            self.logger.info('response.text: %s', response.text)
            return (status, None)

        if not data_result:
            return (status, None)

        if self.logger.level <= logging.DEBUG:
            self.logger.debug('data_result = %s',
                              json.dumps(data_result, indent=4,
                                         sort_keys=True))

        if progress_callback is not None:
            if progress_callback(0.3, 'Beginning download of data.',
                                 progress_user_value) != 0:
                return (status, None)

        file_descriptions = data_result['FileDescription']

        data_url = file_descriptions[0]['Name']
        data_length = file_descriptions[0]['Length']

        self.logger.debug('data_url = %s, data_length = %d',
                          data_url, data_length)

        file_descriptor, tmp_filename = mkstemp(suffix='.cdf')

        download_bytes = 0
        next_progress_report = 0.1
        with self._session.get(data_url, stream=True,
                               timeout=self._timeout) as response:

            file = open(tmp_filename, 'wb')
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:  # filter out keep-alive new chunks
                    file.write(chunk)
                    # file.flush()
                    if progress_callback is not None:
                        download_bytes += len(chunk)
                        download_progress = float(download_bytes) / data_length
                        if download_progress > next_progress_report:
                            next_progress_report += download_progress
                            if progress_callback(0.3 + 0.1 * download_progress,
                                                 'Continuing download of data.',
                                                 progress_user_value) != 0:
                                file.close()
                                os.close(file_descriptor)
                                return (status, None)
            file.close()
            os.close(file_descriptor)

        if progress_callback is not None:
            if progress_callback(0.4, 'Data download complete. Reading data.',
                                 progress_user_value) != 0:
                return (status, None)

        data = spdm.fromCDF(tmp_filename)
        if progress_callback is not None:
            if progress_callback(1.0, 'Finished reading data.',
                                 progress_user_value) != 0:
                return (status, None)
        os.remove(tmp_filename)
        return (status, data)
    # pylint: enable=too-many-locals
    # pylint: enable=too-many-return-statements
    # pylint: enable=too-many-statements
    # pylint: enable=too-many-branches

# pylint: enable=too-many-instance-attributes
