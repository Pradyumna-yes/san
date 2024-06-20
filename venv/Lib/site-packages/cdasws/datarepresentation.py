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
# Copyright (c) 2022 United States Government as represented by
# the National Aeronautics and Space Administration. No copyright is
# claimed in the United States under Title 17, U.S.Code. All Other
# Rights Reserved.
#


"""
Module defining data representations for the data returned from the
cdasws.get_data function.<br>

Copyright &copy; 2022 United States Government as represented by the
National Aeronautics and Space Administration. No copyright is claimed in
the United States under Title 17, U.S.Code. All Other Rights Reserved.
"""


from enum import Enum, unique


@unique
class DataRepresentation(Enum):
    """
    Enumerations for the representations of data returned by the
    cdasws.get_data function.  The following representations are
    currently supported:<br>
    SPASEPY: SpacePy data model
        <https://spacepy.github.io/datamodel.html><br>
    XARRAY: cdflib xarray.Dataset <https://pypi.org/project/cdflib/> with
        datetime time values and FILLVAL values as NaN.
    """
    SPACEPY = 'SpacePyDm'
    XARRAY = 'CdfLibXArray'

#DataRepresentationValue = typing.Literal['SpacePyDm', 'CdfLibXArray']

#assert set(typing.get_args(DataRespresentationValue)) ==
#   {member.value for member in DataRepresentation}
