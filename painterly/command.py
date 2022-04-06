"""
This module contains functions to process each of the painterly commands.
"""


def brush(arguments, context):
    """
    Changes the characteristics of the current brush
    :param arguments: the arguments from the painterly command
    :param context: the current contex
    """
    print('brush', arguments)


def stroke(arguments, context):
    """
    Performs a brush stroke at the provided coordinates and with
    the given curve and wavy values.
    :param arguments: the arguments from the painterly command
    :param context: the current contex
    """
    print('stroke', arguments)


def sample(arguments, context):
    """
    Sets the current sampler object to the provided sampler type.
    :param arguments: the arguments from the painterly command
    :param context: the current context
    """
    print('sample', arguments)
