from entsoe import EntsoePandasClient
import pandas as pd
import time
import xmltodict
import pprint
import json

client = EntsoePandasClient(api_key='37c416e5-19fb-47a6-8852-d7721dc930db')


hoy=time.strftime('%Y%m%d')
mañana=str(int(hoy)+1)
print('Fecha incio extracción = ' + hoy)
print('Fecha fin extracción = ' + mañana)

start = pd.Timestamp(hoy, tz='Europe/Brussels')
end = pd.Timestamp(mañana, tz='Europe/Brussels')

PSRTYPE_MAPPINGS = {'A03': 'Mixed',
    'A04': 'Generation',
    'A05': 'Load',
    'B01': 'Biomass',
    'B02': 'Fossil Brown coal/Lignite',
    'B03': 'Fossil Coal-derived gas',
    'B04': 'Fossil Gas',
    'B05': 'Fossil Hard coal',
    'B06': 'Fossil Oil',
    'B07': 'Fossil Oil shale',
    'B08': 'Fossil Peat',
    'B09': 'Geothermal',
    'B10': 'Hydro Pumped Storage',
    'B11': 'Hydro Run-of-river and poundage',
    'B12': 'Hydro Water Reservoir',
    'B13': 'Marine',
    'B14': 'Nuclear',
    'B15': 'Other renewable',
    'B16': 'Solar',
    'B17': 'Waste',
    'B18': 'Wind Offshore',
    'B19': 'Wind Onshore',
    'B20': 'Other',
    'B21': 'AC Link',
    'B22': 'DC Link',
    'B23': 'Substation',
    'B24': 'Transformer'}

BSNTYPE = {'A29': 'Already allocated capacity (AAC)',
           'A43': 'Requested capacity (without price)',
           'A46': 'System Operator redispatching',
           'A53': 'Planned maintenance',
           'A54': 'Unplanned outage',
           'A85': 'Internal redispatch',
           'A95': 'Frequency containment reserve',
           'A96': 'Automatic frequency restoration reserve',
           'A97': 'Manual frequency restoration reserve',
           'A98': 'Replacement reserve',
           'B01': 'Interconnector network evolution',
           'B02': 'Interconnector network dismantling',
           'B03': 'Counter trade',
           'B04': 'Congestion costs',
           'B05': 'Capacity allocated (including price)',
           'B07': 'Auction revenue',
           'B08': 'Total nominated capacity',
           'B09': 'Net position',
           'B10': 'Congestion income',
           'B11': 'Production unit'}

DOCUMENTTYPE = {
    #'A09': 'Finalised schedule',
    #            'A11': 'Aggregated energy data report',
    #            'A25': 'Allocation result document',
    #            'A26': 'Capacity document',
    #            'A31': 'Agreed capacity',
                'A44': 'Price Document'
                #,
                #'A61': 'Estimated Net Transfer Capacity',
                #'A63': 'Redispatch notice',
                #'A65': 'System total load',
                #'A68': 'Installed generation per type',
                #'A69': 'Wind and solar forecast',
                #'A70': 'Load forecast margin',
                #'A71': 'Generation forecast',
                #'A72': 'Reservoir filling information',
                #'A73': 'Actual generation',
                #'A74': 'Wind and solar generation',
                #'A75': 'Actual generation per type',
                #'A76': 'Load unavailability',
                #'A77': 'Production unavailability',
                #'A78': 'Transmission unavailability',
                #'A79': 'Offshore grid infrastructure unavailability',
                #'A80': 'Generation unavailability',
                #'A81': 'Contracted reserves',
                #'A82': 'Accepted offers',
                #'A83': 'Activated balancing quantities',
                #'A84': 'Activated balancing prices',
                #'A85': 'Imbalance prices',
                #'A86': 'Imbalance volume',
                #'A87': 'Financial situation',
                #'A88': 'Cross border balancing',
                #'A89': 'Contracted reserve prices',
                #'A90': 'Interconnection network expansion',
                #'A91': 'Counter trade notice',
                #'A92': 'Congestion costs',
                #'A93': 'DC link capacity',
                #'A94': 'Non EU allocations',
                #'A95': 'Configuration document',
                #'B11': 'Flow-based allocations'
                }

DOMAIN_MAPPINGS = {'AL': '10YAL-KESH-----5',
    'AT': '10YAT-APG------L',
    'BA': '10YBA-JPCC-----D',
    'BE': '10YBE----------2',
    'BG': '10YCA-BULGARIA-R',
    'BY': '10Y1001A1001A51S',
    'CH': '10YCH-SWISSGRIDZ',
    'CZ': '10YCZ-CEPS-----N',
    'DE': '10Y1001A1001A83F',
    'DK': '10Y1001A1001A65H',
    'EE': '10Y1001A1001A39I',
    'ES': '10YES-REE------0',
    'FI': '10YFI-1--------U',
    'FR': '10YFR-RTE------C',
    'GB': '10YGB----------A',
    'GB-NIR': '10Y1001A1001A016',
    'GR': '10YGR-HTSO-----Y',
    'HR': '10YHR-HEP------M',
    'HU': '10YHU-MAVIR----U',
    'IE': '10YIE-1001A00010',
    'IT': '10YIT-GRTN-----B',
    'LT': '10YLT-1001A0008Q',
    'LU': '10YLU-CEGEDEL-NQ',
    'LV': '10YLV-1001A00074',
    # 'MD': 'MD',
    'ME': '10YCS-CG-TSO---S',
    'MK': '10YMK-MEPSO----8',
    'MT': '10Y1001A1001A93C',
    'NL': '10YNL----------L',
    'NO': '10YNO-0--------C',
    'PL': '10YPL-AREA-----S',
    'PT': '10YPT-REN------W',
    'RO': '10YRO-TEL------P',
    'RS': '10YCS-SERBIATSOV',
    'RU': '10Y1001A1001A49F',
    'RU-KGD': '10Y1001A1001A50U',
    'SE': '10YSE-1--------K',
    'SI': '10YSI-ELES-----O',
    'SK': '10YSK-SEPS-----K',
    'TR': '10YTR-TEIAS----W',
    'UA': '10YUA-WEPS-----0',
    'DE-AT-LU': '10Y1001A1001A63L'}



for pais in DOMAIN_MAPPINGS:
    print(DOMAIN_MAPPINGS[pais])
    for documento in DOCUMENTTYPE:
        try:

            params={
            'documentType': documento,
            'in_Domain': DOMAIN_MAPPINGS[pais],
            'out_Domain': DOMAIN_MAPPINGS[pais]
            }    
            ts=client.base_request(params=params,start=start,end=end)
            pp = pprint.PrettyPrinter(indent=4)
            ts_json=pp.pprint(json.dumps(xmltodict.parse(ts.content)))
            #with open('data.txt','w') as outfile:
            #    json.dump(ts,outfile)
            #mydata=json.loads(ts)
            #DataFile=open("Precio.json","w")
            #DataFile.write(simplejson.dumps(simplejson.loads(ts_json),indent=4,sort_keys=True))
            #DataFile.close()

            #print(ts.text)
            #print(ts.content)

            ##################################
        
            #doc=xmltodict.parse(ts.content)
            #pp = pprint.PrettyPrinter(indent=4)
            #pp.pprint(json.dumps(doc))
        
            ##################################
        
            #mydict=xmltodict.parse(ts.content)
            #print(mydict['postion'])
            #print(mydict(['position']['price.amount']))
            #print(type(ts))
            #df=ts.content
        except:
            print("El documento "+documento + " del país "+ pais + " no se ha podido obtener")
            pass


params = {
    'documentType': 'A44',
    'in_Domain': '10YBE----------2',
    'out_Domain': '10YBE----------2'
}

country_code = 'BE'  # Belgium
path='C:\\Users\\jarpa\\OneDrive - Fundacion CIRCE\\RREE-ENTSOE\\ENTSOE-API\\Prueba API GIT\\Descargas\\'
# methods that returns Pandas Series
        
for country_code in DOMAIN_MAPPINGS:
    
    try:    
        ts=client.query_day_ahead_prices(country_code, start=start,end=end)
        ts.to_csv(path+country_code+'-precio_d-1.csv')
        ts=client.query_load(country_code, start=start,end=end)
        ts.to_csv(path+country_code+'-carga_d')
        ts=client.query_load_forecast(country_code, start=start,end=end)
        ts.to_csv(path+country_code+'-carga_d-1.csv')
        ts=client.query_generation_forecast(country_code, start=start,end=end)
        ts.to_csv(path+country_code+'-generacion_d-1.csv')
    except:
        print("El pais " + country_code+" no está disponible en la API (magnitudes diarias)")
        pass
#methods that returns Pandas DataFrames

for country_code in DOMAIN_MAPPINGS:
    try:
        ts=client.query_wind_and_solar_forecast(country_code, start=start,end=end, psr_type=None)
        ts.to_csv(path+country_code+'-solar+PV_d-1.csv')
        client.query_generation(country_code, start=start,end=end, psr_type=None)
        ts.to_csv(path+country_code+'-generacion_d.csv')
        ts=client.query_installed_generation_capacity(country_code, start=start,end=end, psr_type=None)
        ts.to_csv(path+country_code+'-capacidad_instalada.csv')
        ts=client.query_crossborder_flows(antiguo_country_code,country_code, start=start,end=end)
        ts.to_csv(path+country_code+'-flujo_fronterizo.csv')
        ts=client.query_imbalance_prices(country_code, start=start,end=end, psr_type=None)
        ts.to_csv(path+country_code+'-desequilibrio_precios.csv')
        ts=client.query_unavailability_of_generation_units(country_code, start=start,end=end, docstatus=None)
        ts.to_csv(path+country_code+'-incapacidad_unidades_generacion.csv')
        ts=client.query_withdrawn_unavailability_of_generation_units(country_code, start=start,end=end)
        ts.to_csv(path+country_code+'-incapacidad_unidades_generacion_retirada.csv')
        antiguo_country_code=country_code
    except:
        print("El pais "+country_code+" no está disponible en la API (magnitudes intradiarias)")
        pass

#Para realizar el estudio por Bidding Zone, utilizando la variable "params"

ts=client.base_request(params=params,start=start,end=end)
#print(ts.text)
#print(type(ts))
##print(ts[0].json())
##print(ts[0].json.loads())

##XML to dict
#my_dict = xmltodict.parse(ts)
#print(my_dict['resolution']['Point'])
#print(my_dict['resolution']['Point']['@position'])
#print(my_dict['resolution']['Point']['@price.amount'])