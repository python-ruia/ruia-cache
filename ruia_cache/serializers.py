#!/usr/bin/env python
"""
 Created by howie.hu at 2021/1/1.
"""
import abc

try:
    import cPickle as pickle
except ImportError:
    import pickle


class BaseSerializer(metaclass=abc.ABCMeta):
    """
    The class defines some functions that is necessary provided by JsonSerializer(might need) PickleSerializer
    """

    @abc.abstractmethod
    def dumps(self, value, **kwargs):
        pass

    @abc.abstractmethod
    def loads(self, value, **kwargs):
        pass


class PickleSerializer(BaseSerializer):
    def dumps(self, value, **kwargs):
        """
        Serialize the value
        :param value: object
        :return: bytes
        """
        return pickle.dumps(value)

    def loads(self, value, **kwargs):
        """
        Deserialize the value
        :param value: bytes
        :return: object
        """
        return pickle.loads(value) if value is not None else value
