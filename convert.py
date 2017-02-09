import numpy as np
import pandas as pd
filepath = '/2015-raporti-vjetor-per-kontratat-e-nenshkruara-publike.xlsx'
df = pd.read_excel(filepath, skiprows=26, skip_footer=58, index_col=False)
# add in meta data required by OCDS
meta = pd.read_excel(filepath, skiprows=0, skip_footer=173, index_col=False, encoding='iso8859_2')
publishedDate = pd.Series(pd.to_datetime(meta.iat[5,6]))
publisher =  = pd.Series({
    'name':'Open Data Kosovo Foundation', 
    'address': 'Bajram Kelmendi Street, Object KIG, Entry 1, Floor 4, Apt 16.',
    'email': 'opencontracting@opendatakosovo.org'})
releases = np.array(1.0) 
uri = pd.Series(str(meta.iloc[17,8]))

meta_info = pd.concat([publishedDate, publisher,releases, uri], ignore_index=True, axis=1)
meta_info.rename(columns={0:"publishedDate",1:'publisher',2:'releases', 3:'uri' }, inplace=True)

df = pd.concat([df,meta_info],axis=1)

#rename columns to comply with OCDS
df.rename(index=str, columns={
    1:'planning/budget/source', 2:'id', 3:'tender/description', 
    4:'tender/value/description', 
    5:'tender/procurementMethod', 6:'FPP', 7:'tender/title', 
    8:'planning/period/endDate', 9:'tender/tenderPeriod/startDate',
    10:'tender/tenderPeriod/endDate', 11: 'contract/DateSigned',
    12: 'contract/contractPeriod/timeframe', 13:'contract/contractPeriod/endDate', 
    14: 'contract/contractValue/amount/estimate', 15:'contract price', 
    16:'Annex/AnnexValue/amount',
    17:'Contract/contractValue/amount/deductions', 18:'contract/contractValue/amount', 
    19: 'Award/AwardSuppliers/name', 20: 'Award/AwardSuppliers/local',
    21:'Tender/numberOfEnquires', 21:'Tender/numberOfRequests', 'Unnamed: 21': 'Tender/numberOfTenderers',
    22: 'Tender/numberOfTendersRejected', 23:'Tender/details/expedited', 
    24:'Tender/awardCriteria'}, inplace=True)

#add in currency information
df['Value.currency'] = 'EUR'
#add in language code
df['langauge'] = 'en'
#add OCID prefix
df['ocid'] = 'ocds-3n5h6d-'
df['id'] = df['id'].astype(str)
df['ocid'] = df[['ocid','id']].apply(lambda x: ''.join(x), axis=1)



###############################


#transform datetime formats

def to_date(series):
    ts = pd.to_datetime(series, yearfirst = True)
    return ts
    
startTime = str('00:00:00UTC+1h')
endTime= str('23:23:59UTC+1h')

df['planning/period/endDate'] = to_date(df['planning/period/endDate'])
df['tender/tenderPeriod/startDate' ] = to_date(df['tender/tenderPeriod/startDate' ])
df['tender/tenderPeriod/endDate'] = to_date(df['tender/tenderPeriod/endDate'])
df['contract/DateSigned'] = to_date(df['contract/DateSigned'])
df['contract/contractPeriod/endDate'] = to_date(df['contract/contractPeriod/endDate'])
    
#convert numerical variables back into string text

df['planning/budget/source'] = df['planning/budget/source'].replace([1,2,3],['local municipal funds', 'Kosovo Consolidated Budget', 'Donation' ])
df['tender/description'] = df['tender/description'].replace([1,2,3,4,5,6,7], ['supply', 'services', 'counseling services','design contest', 'jobs', 'concession jobs', 'immovable property'])
df['tender/value/description'] = df['tender/value/description'].replace([1,2,3,4], ['great','medium','small', 'minimal'])
df['tender/procurementMethod'] = df['tender/procurementMethod'].replace([1,2,3,4,5,6,7],['open procedure', 'restricted procedure', 'design contest', 'negotiated procedure after publication of a contract notice','negotiated procedure without publication of a contract notice', 'price quotation procedure', 'cheapest offer' ])
df['Award/AwardSuppliers/local'] = df['Award/AwardSuppliers/local'].replace([1,2],['domestic', 'international'])

# convert to machine readable - Award.contractPeriod
#split the column on white space into a new df
x = df['contract/contractPeriod/timeframe'].str.split(expand=True)

#translate Albanian time expressions into an integer amount of days
x[0] = x[0].replace(['një', 'tri', 'tre', 'dy', '12-', '90ditë', 'dhjetë'], [1,3,3,2,12,90,10])
x[1] = x[1].replace(['ditë', 'vite', 'muaj', 'dite', 'vit', 'muj', '-muaj'], [1,365, 30,1, 365, 30,30 ])

#******issue: strings containing ë are not being replaced

# multiply x[0] and x[1] to create series showing contract length in days

#x[3] = x[0] * x[1]

# use contract length to fill in missing values in contractPeriod.endDate


df.to_json('/Desktop/2016 Gjilan public works report.json')




