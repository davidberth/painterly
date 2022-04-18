"""This module contains a simple class to define
random or deterministic values"""
from dataclasses import dataclass
from enum import Enum, auto

import numpy as np

variables = {}


class ValueType(Enum):
    real = auto()
    uniform = auto()
    normal = auto()
    variable = auto()


class Value:
    """
    This class implements a deterministic or random value using
    several random distributions.
    """

    def __init__(self, value1, value2, value_type):
        self.value1 = float(value1)
        self.value2 = float(value2)
        self.value_type = value_type
        self.label = ''

    @property
    def value(self):
        """
        This function instantiates the random or
         deterministic value into a float
        :return: the computed float value
        """
        global variables
        value = 0.0
        match self.value_type:
            case ValueType.real:
                value = self.value1
            case ValueType.uniform:
                value = np.random.uniform(self.value1, self.value2)
            case ValueType.normal:
                value = np.random.normal(self.value1, self.value2)
            case ValueType.variable:
                if self.label in variables:
                    value = variables[self.label]
                else:
                    raise ValueError(f'Variable {self.label} not found. '
                                     f'Please be sure to assign a value to '
                                     f'{self.label} before attempting '
                                     f'to use it.')

        return InstantiatedValue(self.label, value)


@dataclass
class InstantiatedValue:
    """
    This is a simple class that holds an instantiated Value object.
    This contains a label and a floating point value.
    """
    label: str = ''
    value: float = 0.0


