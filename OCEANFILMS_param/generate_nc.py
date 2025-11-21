import xarray as xr
import pandas as pd


def create_dataset(pol, pro, lip, y, lon, lat):
    time_date = str(y) + "-01-01"
    time = pd.date_range(time_date, periods=12, freq='M')
    ds = xr.Dataset(
        data_vars=dict(
            OMF_POL=(["time", "lat", "lon"], pol),
            OMF_PRO=(["time", "lat", "lon"], pro),
            OMF_LIP=(["time", "lat", "lon"], lip),
        ),
        coords=dict(
            lon=(["lon"], lon),
            lat=(["lat"], lat),
            time=time,
        ),
    )
    return ds


