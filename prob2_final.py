import math
import numpy as np
import pandas as pd
import statsmodels.api as sm

vt = pd.read_csv('VT-clean.csv')
mt = pd.read_csv('MT-clean.csv')

print('male driver proportion in Montana: {}'.format(np.sum(mt.driver_gender == 'M') / mt.shape[0]))

mt_outState = mt[mt.out_of_state == True]
mt_inState = mt[mt.out_of_state == False]
mt_outState_total = len(mt_outState)
mt_inState_total = len(mt_inState)
mt_outState_arrested = len(mt_outState[mt_outState.stop_outcome == 'Arrest'])
mt_inState_arrested = len(mt_inState[mt_inState.stop_outcome == 'Arrest'])
outState_arrestP = mt_outState_arrested / mt_outState_total
inState_arrestP = mt_inState_arrested / mt_inState_total
print('Arrest ratio for out/in of state plates:{}'.format(outState_arrestP / inState_arrestP))

arrestP = (mt_inState_arrested + mt_outState_arrested) / (mt_inState_total + mt_outState_total)
mt_outState_arrested_expected = arrestP * mt_outState_total
mt_inState_arrested_expected = arrestP * mt_inState_total
chi_sqaure = math.pow(mt_outState_arrested - mt_outState_arrested_expected, 2) / mt_outState_arrested_expected
chi_sqaure += math.pow((mt_outState_total - mt_outState_arrested) - (mt_outState_total - mt_outState_arrested_expected), 2) / (mt_outState_total - mt_outState_arrested_expected)
chi_sqaure += math.pow(mt_inState_arrested - mt_inState_arrested_expected, 2) / mt_inState_arrested_expected
chi_sqaure += math.pow((mt_inState_total - mt_inState_arrested) - (mt_inState_total - mt_inState_arrested_expected), 2) / (mt_inState_total - mt_inState_arrested_expected)
print('chi_sqaure value:{}'.format(chi_sqaure))

speeding_count = np.sum(mt.violation.str.contains("Speeding", case=False))
print('Montana speeding violation proportion: {}'.format(speeding_count / mt.shape[0]))

vt_dui_count = np.sum(vt.violation.str.contains("dui", case=False))
mt_dui_count = np.sum(mt.violation.str.contains("dui", case=False))
print('Montana vs Vermont DUI violation proportions: {}'.format((mt_dui_count / mt.shape[0]) / (vt_dui_count / vt.shape[0])))

mt_lr = mt[['stop_date', 'vehicle_year']].dropna()
mt_lr.stop_date = pd.to_datetime(mt_lr.stop_date, infer_datetime_format=True)
mt_lr.vehicle_year = pd.to_numeric(mt_lr.vehicle_year, errors='coerce')
vehicle_year = mt_lr.groupby(mt_lr.stop_date.dt.year).vehicle_year.mean().reset_index()
vehicle_year = vehicle_year.values

y = vehicle_year[:,1]
X = sm.add_constant(vehicle_year[:,0])
model = sm.OLS(y, X).fit()
print("2020 predicted average vehicle_year in Montana:{}".format(model.predict(np.array([1, 2020]))[0]))
print("p-value:{}".format(model.pvalues[1]))

ct = pd.concat([vt, mt])
ct = ct['stop_time'].dropna()
ct = ct.replace({r'(\d+):(\d+)': r'\1'}, regex=True)
ct = pd.to_numeric(ct, errors='coerce')
ct = ct.value_counts()
print("Difference in max/min hours:{}".format(ct.max() - ct.min()))

mta = mt[(mt.lon >= -118) & (mt.lon <= -100) & (mt.lat >= 43) & (mt.lat <= 52)]
mtg = mta.groupby(mta.county_name)
mt_lon = mtg.lon.std().reset_index()
mt_lat = mtg.lat.std().reset_index()
mt_lat_avg = mtg.lat.mean().reset_index()
mt_lat_avg.columns = ['county_name', 'lat_avg']
mtc = pd.concat([mt_lon, mt_lat, mt_lat_avg], axis=1)
mtc['area'] = mtc.apply(lambda row: math.pi * (111.32 * math.cos(row.lat_avg * math.pi / 180.0) * row.lon) * (110.574 * row.lat), axis=1)
print("Montana Largest country area(km^2):{}".format(mtc.area.max()))

