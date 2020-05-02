import attr

from pandas import read_json as df_from_json


@attr.s(str=True, repr=True)
class Dataset:
    datapoints = attr.ib(init=True)
    name = attr.ib(init=True, default=None)
    size = attr.ib(init=False, default=attr.Factory(lambda self: len(self.datapoints), takes_self=True))



@attr.s(str=True, repr=True)
class StrainDataset(Dataset):
    pass