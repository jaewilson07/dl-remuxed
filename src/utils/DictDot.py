__all__ = ["DictDot", "split_str_to_obj"]

from types import SimpleNamespace


class DictDot(SimpleNamespace):
    """a utility class that converts json into an object that supports data retrieval with dot notation"""

    def __init__(self, dictionary: dict, **kwargs):  # dictionary to convert
        super().__init__(**kwargs)

        for key, value in dictionary.items():
            if isinstance(value, dict):
                self.__setattr__(key, DictDot(value))
            elif isinstance(value, list):
                new_list = []
                for item in value:
                    if isinstance(item, dict):
                        new_list.append(DictDot(item))
                    else:
                        new_list.append(item)
                self.__setattr__(key, new_list)
            else:
                self.__setattr__(key, value)

    def __getattr__(self, item):
        return None


def split_str_to_obj(piped_str: str, key_ls: list[str]):
    """
    split a pipe separated list into an object with keys defined by the list of keys
    ex. "test_instance|myemail|sample_password", ["domo_instance", "domo_username", "domo_password"] = {"domo_instance" : "test_intance" , "domo_username" : "myemail", "domo_password":"sample_password"}
    """
    str_ls = piped_str.split("|")
    obj = dict([new_obj_key, str_ls[index]] for index, new_obj_key in enumerate(key_ls))

    return DictDot(obj)
