"""This module contains a simple class to define
random or deterministic values"""

from enum import Enum

import numpy as np
from lark import Token


class ValueType(Enum):
    real = 1
    uniform = 2
    normal = 3


class Value:
    """
    This class implements a determinstic or random value using
    several random distributions.
    """

    def __init__(self, value1, value2, value_type):
        self.value1 = float(value1)
        self.value2 = float(value2)
        self.value_type = value_type

    @property
    def value(self):
        """
        This function instantiates the random or
         deterministic value into a float
        :return: the computed float value
        """
        match self.value_type:
            case ValueType.real:
                return self.value1
            case ValueType.uniform:
                return np.random.uniform(self.value1, self.value2)
            case ValueType.normal:
                return np.random.normal(self.value1, self.value2)

        return 0.0


def get_values(arguments):
    """
    Instantiates the Value objects into actual floating point values.
    :param arguments: the arguments to process
    :return: the processed arguments with Value objects
            turned into floating point numbers
    """
    realized = []
    for argument in arguments[1:]:

        if isinstance(argument, list):
            realized_argument = []
            for component in argument:
                if isinstance(component, Value):
                    # crystallize the random value
                    realized_argument.append(component.value)
                else:
                    realized_argument.append(component)
            realized.append(realized_argument)
        else:
            if isinstance(argument, Value):
                realized.append(argument.value)
            elif isinstance(argument, Token):
                realized.append(argument.value)

    return realized
