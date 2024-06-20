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
# Copyright (c) 2019-2023 United States Government as represented by
# the National Aeronautics and Space Administration. No copyright is
# claimed in the United States under Title 17, U.S.Code. All Other
# Rights Reserved.
#


"""
Package defining classes to represent the DataRequestEntity and its
sub-classes from
<https://cdaweb.gsfc.nasa.gov/WebServices/REST/CDAS.xsd>.<br>

Copyright &copy; 2019-2023 United States Government as represented by the
National Aeronautics and Space Administration. No copyright is claimed in
the United States under Title 17, U.S.Code. All Other Rights Reserved.
"""


import enum
import json
from typing import List, Union # when python 3.8 , TypedDict
from abc import ABCMeta, abstractmethod
from cdasws.timeinterval import TimeInterval


class RequestType(enum.Enum):
    """
    Enumerations representing the concrete sub-classes of a
    DataRequestEntity from
    <https://cdaweb.gsfc.nasa.gov/WebServices/REST/CDAS.xsd>.
    """
    TEXT = "Text"
    CDF = "Cdf"
    GRAPH = "Graph"
    THUMBNAIL = "Thumbnail"
    AUDIO = "Audio"

# Finish the following when python 3.8
#class DataRequestDict(TypedDict):
#    pass
#
#class TimeIntervalDict(TypeDict):
#    Start: str   # ISO 8601
#    End: str
#
#...
#
#class TextRequestDict(DataRequestDict):
#    TimeInterval: TimeIntervalDict
#    DataRequest: ...
#    Compression: ...
#    Format: ...
#    BinData: ...
#class CdfRequestDict(DataRequestDict):
#    ...
#class GraphRequestDict(DataRequestDict):
#    ...
#class ThumbnailRequestDict(DataRequestDict):
#    ...
#class AudioRequestDict(DataRequestDict):
#    ...


class DataRequest(metaclass=ABCMeta): # pylint: disable=too-few-public-methods
    """
    Class representing a DataRequestEntity from
    <https://cdaweb.gsfc.nasa.gov/WebServices/REST/CDAS.xsd>.

    Attributes
    ----------
    _data_request
        a dictionary representation of a DataRequestEntity.

    Notes
    -----
    Although this class is essentially a dictionary, it was defined as a
    class to make certain that it matched the structure and key names
    of a DataRequestEntity from
    <https://cdaweb.gsfc.nasa.gov/WebServices/REST/CDAS.xsd>.
    It also needs to function as a base class for the concrete
    sub-classes of a DataRequestEntity.
    """
    @abstractmethod
    def __init__(self,
                 request_type: RequestType,
                 dataset: str,
                 variables: List[str],
                 intervals: Union[TimeInterval, List[TimeInterval]],
                 **keywords):
        """
        Creates an object representing a DataRequestEntity from
        <https://cdaweb.gsfc.nasa.gov/WebServices/REST/CDAS.xsd>.

        Parameters
        ----------
        request_type
            concrete type of this data request.
        dataset
            dataset identifier of data to get.
        variables
            array containing names of variables to get.
        intervals
            time interval(s) of data to get.
        keywords
            optional binning parameters as follows<br>
            <b>binData</b> - indicates that uniformly spaced values should
            be computed for scaler/vector/spectrogram data according to
            the given binning parameter values.  See
            <https://cdaweb.gsfc.nasa.gov/CDAWeb_Binning_readme.html>
            for more details.  binData is a Dict that
            may contain the following keys: interval,
            interpolateMissingValues, sigmaMultiplier, and/or
            overrideDefaultBinning with values that override the defaults.<br>
        """

        request_name = request_type.value + 'Request'

        self._data_request = {
            request_name: {
                'DatasetRequest': {
                    'DatasetId': dataset,
                    'VariableName': variables
                }
            }
        }
        if isinstance(intervals, list):

            self._data_request[request_name]['TimeInterval'] = []
            for interval in intervals:
                self._data_request[request_name]['TimeInterval'].append({
                    'Start': interval.start.isoformat(),
                    'End': interval.end.isoformat()
                })
        else:
            self._data_request[request_name]['TimeInterval'] = {
                'Start': intervals.start.isoformat(),
                'End': intervals.end.isoformat()
            }

        bin_data = keywords.get('binData', {})
        if bin_data:
            self._data_request[request_name]['BinData'] = {}
            if 'interval' in bin_data:
                self._data_request[request_name]['BinData']['Interval'] = \
                    bin_data['interval']
            if 'interpolateMissingValues' in bin_data:
                self._data_request[request_name]['BinData']['InterpolateMissingValues'] = \
                    bin_data['interpolateMissingValues']
            if 'sigmaMultiplier' in bin_data:
                self._data_request[request_name]['BinData']['SigmaMultiplier'] = \
                    bin_data['sigmaMultiplier']
            if 'overrideDefaultBinning' in bin_data:
                self._data_request[request_name]['BinData']['OverrideDefaultBinning'] = \
                    bin_data['overrideDefaultBinning']


    def json(self, **keywords) -> str:
        """
        Produces a JSON representation of this object matching the
        JSON representation of a DataRequestEntity from
        <https://cdaweb.gsfc.nasa.gov/WebServices/REST/CDAS.xsd>.

        Parameters
        ----------
        keywords
            json.dumps keyword paramters.

        Returns
        -------
        str
            string JSON representation of this object.
        """

        return json.dumps(self._data_request, **keywords)


class CdfFormat(enum.Enum):
    """
    Enumerations representing the enumCdfFormat from
    <https://cdaweb.gsfc.nasa.gov/WebServices/REST/CDAS.xsd>.
    """
    BINARY = "Binary"
    CDFML = "CDFML"
    GZIP_CDFML = "GzipCDFML"
    ZIP_CDFML = "ZipCDFML"
    ICDFML = "ICDFML"
    NETCDF = "NetCdf"


class CdfRequest(DataRequest): # pylint: disable=too-few-public-methods
    """
    Class representing a CdfRequest from
    <https://cdaweb.gsfc.nasa.gov/WebServices/REST/CDAS.xsd>.

    Parameters
    ----------
    dataset
        dataset identifier of data to get.
    variables
        array containing names of variables to get.
    intervals
        time interval(s) of data to get.
    cdf_version
        CDF version.
    cdf_format
        CDF format.
    keywords
        optional binning parameters as follows<br>
        <b>binData</b> - indicates that uniformly spaced values should
        be computed for scaler/vector/spectrogram data according to
        the given binning parameter values.  binData is a Dict that
        may contain the following keys: interval,
        interpolateMissingValues, sigmaMultiplier, and/or
        overrideDefaultBinning with values that override the defaults.<br>
    """
    def __init__(self,
                 dataset: str,
                 variables: List[str],
                 intervals: Union[TimeInterval, List[TimeInterval]],
                 cdf_version: int = 3,
                 cdf_format: CdfFormat = CdfFormat.BINARY,
                 **keywords): # pylint: disable=too-many-arguments

        DataRequest.__init__(self, RequestType.CDF, dataset, variables,
                             intervals, **keywords)
        self._data_request['CdfRequest']['CdfVersion'] = cdf_version
        self._data_request['CdfRequest']['CdfFormat'] = cdf_format.value


class Compression(enum.Enum):
    """
    Enumerations representing the enumCompression from
    <https://cdaweb.gsfc.nasa.gov/WebServices/REST/CDAS.xsd>.
    """
    UNCOMPRESSED = "Uncompressed"
    GZIP = "Gzip"
    BZIP2 = "Bzip2"
    ZIP = "Zip"


class TextFormat(enum.Enum):
    """
    Enumerations representing the enumTextFormat from
    <https://cdaweb.gsfc.nasa.gov/WebServices/REST/CDAS.xsd>.
    """
    PLAIN = "Plain"
    CSV = "CSV"
    CSV1 = "CSV1"
    CSV2 = "CSV2"


class TextRequest(DataRequest): # pylint: disable=too-few-public-methods
    """
    Class representing a TextRequest from
    <https://cdaweb.gsfc.nasa.gov/WebServices/REST/CDAS.xsd>.

    Parameters
    ----------
    dataset
        dataset identifier of data to get.
    variables
        array containing names of variables to get.
    interval
        time interval of data to get.
    compression
        file compression.
    format
        text format.
    keywords
        optional binning parameters as follows<br>
        <b>binData</b> - indicates that uniformly spaced values should
        be computed for scaler/vector/spectrogram data according to
        the given binning parameter values.  binData is a Dict that
        may contain the following keys: interval,
        interpolateMissingValues, sigmaMultiplier, and/or
        overrideDefaultBinning with values that override the defaults.<br>
    """
    def __init__(self,
                 dataset: str,
                 variables: List[str],
                 interval: TimeInterval,
                 compression: Compression = Compression.UNCOMPRESSED,
                 text_format: TextFormat = TextFormat.PLAIN,
                 **keywords): # pylint: disable=too-many-arguments

        DataRequest.__init__(self, RequestType.TEXT, dataset, variables,
                             interval, **keywords)
        self._data_request['TextRequest']['Compression'] = compression.value
        self._data_request['TextRequest']['Format'] = text_format.value


class ImageFormat(enum.Enum):
    """
    Enumerations representing the enumImageFormat from
    <https://cdaweb.gsfc.nasa.gov/WebServices/REST/CDAS.xsd>.
    """
    GIF = "GIF"
    PNG = "PNG"
    PS = "PS"
    PDF = "PDF"


class Overplot(enum.Enum):
    """
    Enumerations representing the enumOverplot from
    <https://cdaweb.gsfc.nasa.gov/WebServices/REST/CDAS.xsd>.
    """
    NONE = "None"
    VECTOR_COMPONENTS = "VectorComponents"
    IDENTICAL_MISSION_VARIABLES = "IdenticalMissionVariables"


class GraphOptions:
    """
    Class representing a GraphOptions from
    <https://cdaweb.gsfc.nasa.gov/WebServices/REST/CDAS.xsd>.

    Parameters
    ----------
    coarse_noise_filter
        Use coarse noise filtering to remove values outside 3 deviations
        from mean of all values in the plotted time interval.
    x_axis_width_factor
        Multiply the X-axis width for time-series and spectrogram by
        the given value.  For example, if the standard width is 320
        pixels and factor is 3, then the width of the X-axis will be 960.
    y_axis_height_factor
        Multiply the Y-axis height for time-series and spectrogram by
        the given value.  For example, if the standard height is 100
        pixels and factor is 2, then the height of the Y-axis will be 200.
    combine
        Combine all time-series and spectrogram plots, for all requested
        datasets, into one plot file.
    overplot
        Overplot option.  This option requests that vector quantities
        and/or corresponding variables from related datasets be plotted
        on the same graph.  For example, include this option to have all
        components of the tha_fgm_gsm vector variable (from the
        THA_L2_FGM dataset) plotted on the same graph.  Another example
        involving related variables in multiple datasets is the B_Ion
        variables from the RBSPA_REL03_ECT-HOPE-SCI-L2SA and
        RBSPB_REL03_ECT-HOPE-SCI-L2SA datasets plotted on the same
        graph.<br>
        NOTE: These web services do not currently return sufficient
        metadata for a client to reliably request this option.  For
        example, the returned VariableDescription does not contain
        dimension information or information describing a relationship
        between a variable in another dataset.  But some clients may
        have this information from another source (for example, from
        a Space Physics Archive Search and Extract [SPASE] description).
        Requesting this option when there are no vector variables or
        related variables from different datasets will result in the
        same graphs being produced as when the option is not included.
    """
    def __init__(self,
                 coarse_noise_filter: bool = False,
                 x_axis_width_factor: int = 3,
                 y_axis_height_factor: int = 2,
                 combine: bool = False,
                 overplot: Overplot = Overplot.NONE,
                 ):

        self._coarse_noise_filter = coarse_noise_filter
        self._x_axis_width_factor = x_axis_width_factor
        self._y_axis_height_factor = y_axis_height_factor
        self._combine = combine
        self._overplot = overplot


    @property
    def coarse_noise_filter(self) -> bool:
        """
        Gets the coarse_noise_filter value.

        Returns
        -------
        bool
            coarse_noise_filter value.
        """
        return self._coarse_noise_filter


    @coarse_noise_filter.setter
    def coarse_noise_filter(self, value: bool):
        """
        Sets the coarse_noise_filter value.

        Parameters
        ----------
        value
            new coarse_noise_filter value.
        """
        self._coarse_noise_filter = value


    @property
    def x_axis_width_factor(self) -> int:
        """
        Gets the x_axis_width_factor value.

        Returns
        -------
        bool
            x_axis_width_factor value.
        """
        return self._x_axis_width_factor


    @x_axis_width_factor.setter
    def x_axis_width_factor(self, value: int):
        """
        Sets the x_axis_width_factor value.

        Parameters
        ----------
        value
            new x_axis_width_factor value.
        """
        self._x_axis_width_factor = value


    @property
    def y_axis_height_factor(self) -> int:
        """
        Gets the y_axis_height_factor value.

        Returns
        -------
        bool
            y_axis_height_factor value.
        """
        return self._y_axis_height_factor


    @y_axis_height_factor.setter
    def y_axis_height_factor(self, value: int):
        """
        Sets the y_axis_height_factor value.

        Parameters
        ----------
        value
            new y_axis_height_factor value.
        """
        self._y_axis_height_factor = value


    @property
    def combine(self) -> bool:
        """
        Gets the combine value.

        Returns
        -------
        bool
            combine value.
        """
        return self._combine


    @combine.setter
    def combine(self, value: bool):
        """
        Sets the combine value.

        Parameters
        ----------
        value
            new combine value.
        """
        self._combine = value


    @property
    def overplot(self) -> Overplot:
        """
        Gets the overplot value.

        Returns
        -------
        Overplot
            overplot value.
        """
        return self._overplot


    @overplot.setter
    def overplot(self, value: Overplot):
        """
        Sets the overplot value.

        Parameters
        ----------
        value
            new overplot value.
        """
        self._overplot = value


class GraphRequest(DataRequest): # pylint: disable=too-few-public-methods
    """
    Class representing a GraphRequest from
    <https://cdaweb.gsfc.nasa.gov/WebServices/REST/CDAS.xsd>.

    Parameters
    ----------
    dataset
        dataset identifier of data to get.
    variables
        array containing names of variables to get.
    interval
        time interval of data to get.
    options
        graph options.
    image_format
        image format.  If None, then [ImageFormat.PNG].
    keywords
        optional binning parameters as follows<br>
        <b>binData</b> - indicates that uniformly spaced values should
        be computed for scaler/vector/spectrogram data according to
        the given binning parameter values.  binData is a Dict that
        may contain the following keys: interval,
        interpolateMissingValues, sigmaMultiplier, and/or
        overrideDefaultBinning with values that override the defaults.<br>
    """
    def __init__(self,
                 dataset: str,
                 variables: List[str],
                 interval: TimeInterval,
                 options: GraphOptions = None,
                 image_format: List[ImageFormat] = None,
                 **keywords): # pylint: disable=too-many-arguments

        DataRequest.__init__(self, RequestType.GRAPH, dataset, variables,
                             interval, **keywords)
        if options is not None:
            self._data_request['GraphRequest']['GraphOptions'] = {}
            if options.combine:
                self._data_request['GraphRequest']['GraphOptions']['Combine'] = {}
            self._data_request['GraphRequest']['GraphOptions']['XAxisWidthFactor'] = \
                options.x_axis_width_factor
            self._data_request['GraphRequest']['GraphOptions']['YAxisHeightFactor'] = \
                options.y_axis_height_factor
            if options.coarse_noise_filter:
                self._data_request['GraphRequest']['GraphOptions']['CoarseNoiseFilter'] = {}
            self._data_request['GraphRequest']['GraphOptions']['Overplot'] = \
                options.overplot.value


        if image_format is None:
            self._data_request['GraphRequest']['ImageFormat'] = \
                [ImageFormat.PNG.value]
        else:
            self._data_request['GraphRequest']['ImageFormat'] = []
            for i_format in image_format:
                self._data_request['GraphRequest']['ImageFormat'].append(
                    i_format.value)


class ThumbnailRequest(DataRequest): # pylint: disable=too-few-public-methods
    """
    Class representing a ThumbnailRequest from
    <https://cdaweb.gsfc.nasa.gov/WebServices/REST/CDAS.xsd>.

    Parameters
    ----------
    dataset
        dataset identifier of data to get.
    variables
        array containing names of variables to get.
    interval
        time interval of data to get.
    identifier
        thumbnail identifier.
    thumbnail
        number of thumbnail whose full size image is being requested.
        Thumbnail images are counted beginning at one (not zero).
    image_format
        image format.  If None, the [ImageFormat.PNG].
    """
    def __init__(self,
                 dataset: str,
                 variables: List[str],
                 interval: TimeInterval,
                 identifier: str,
                 thumbnail: int = 1,
                 image_format: List[ImageFormat] = None
                ): # pylint: disable=too-many-arguments

        DataRequest.__init__(self, RequestType.THUMBNAIL, dataset,
                             variables, interval)

        self._data_request['ThumbnailRequest']['ThumbnailId'] = identifier
        self._data_request['ThumbnailRequest']['Thumbnail'] = thumbnail

        if image_format is None:
            self._data_request['ThumbnailRequest']['ImageFormat'] = \
                [ImageFormat.PNG.value]
        else:
            self._data_request['ThumbnailRequest']['ImageFormat'] = []
            for i_format in image_format:
                self._data_request['ThumbnailRequest']['ImageFormat'].append(
                    i_format.value)


class AudioRequest(DataRequest): # pylint: disable=too-few-public-methods
    """
    Class representing an AudioRequest from
    <https://cdaweb.gsfc.nasa.gov/WebServices/REST/CDAS.xsd>.

    Parameters
    ----------
    dataset
        dataset identifier of data to get.
    variables
        array containing names of variables to get.
    interval
        time interval of data to get.
    keywords
        optional binning parameters as follows<br>
        <b>binData</b> - indicates that uniformly spaced values should
        be computed for scaler/vector/spectrogram data according to
        the given binning parameter values.  binData is a Dict that
        may contain the following keys: interval,
        interpolateMissingValues, sigmaMultiplier, and/or
        overrideDefaultBinning with values that override the defaults.<br>
    """
    def __init__(self,
                 dataset: str,
                 variables: List[str],
                 interval: TimeInterval,
                 **keywords): # pylint: disable=too-many-arguments

        DataRequest.__init__(self, RequestType.AUDIO, dataset, variables,
                             interval, **keywords)
