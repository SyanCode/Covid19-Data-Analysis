############################################
#
# Plot infection, death, and recovery graphs
# Author : MS
# Date : 16/03/2020
#
############################################

import urllib.request as urllib2
import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def download_file(url, file_name):
    '''
    Download a file from url and copy it locally with file_name as name
    '''
    try:
        # Ensure data directory exists
        os.makedirs('data', exist_ok=True)
        os.makedirs('visualizations', exist_ok=True)
        
        # Construct full path in data directory
        full_path = os.path.join('data', file_name)
        
        # open url passed in argument
        file = urllib2.urlopen(url)
        # open file for writing in binary mode
        with open(full_path, 'wb') as output:
            # write in output the file read
            output.write(file.read())
        # OK : return true
        return True
    except Exception as e:
        print(f"Erreur lors du téléchargement : {e}")
        # Something is wrong : return false
        return False

def compute_daily_change(data):
    """Compute daily change in cases"""
    return data.diff().fillna(0)

# here the main code
if __name__ == '__main__':
    # File names of data
    confirmed_file = "time_series_covid19_confirmed_global.csv"
    deaths_file = "time_series_covid19_deaths_global.csv"
    recovered_file = "time_series_covid19_recovered_global.csv"
    
    # URLs for data
    confirmed_url = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv"
    deaths_url = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv"
    recovered_url = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_recovered_global.csv"

    # Download files
    download_results = [
        (confirmed_file, confirmed_url),
        (deaths_file, deaths_url),
        (recovered_file, recovered_url)
    ]

    for file_name, url in download_results:
        if download_file(url, file_name):
            print(f'Téléchargement du fichier {file_name} terminé avec succès')
        else:
            print(f'Téléchargement du fichier {file_name} impossible')

    # Read the data
    confirmed = pd.read_csv(os.path.join('data', confirmed_file))
    deaths = pd.read_csv(os.path.join('data', deaths_file))
    recovered = pd.read_csv(os.path.join('data', recovered_file))

    # Compute global totals for each time series
    confirmed_totals = confirmed.iloc[:, 4:].sum()
    deaths_totals = deaths.iloc[:, 4:].sum()
    recovered_totals = recovered.iloc[:, 4:].sum()

    # Compute daily changes
    confirmed_daily_change = compute_daily_change(confirmed_totals)
    deaths_daily_change = compute_daily_change(deaths_totals)
    recovered_daily_change = compute_daily_change(recovered_totals)

    # Plotting
    plt.figure(figsize=(20, 12))

    # Cumulative Cases Subplot
    plt.subplot(2, 2, 1)
    plt.title('Cas Cumulatifs Globaux')
    plt.plot(confirmed_totals.index[::30], confirmed_totals.values[::30], label='Confirmés', color='blue')
    plt.plot(deaths_totals.index[::30], deaths_totals.values[::30], label='Décès', color='red')
    plt.plot(recovered_totals.index[::30], recovered_totals.values[::30], label='Rétablis', color='green')
    plt.xlabel('Date')
    plt.ylabel('Nombre de Cas')
    plt.legend()
    plt.xticks(rotation=45)
    plt.grid(True, linestyle='--', alpha=0.7)

    # Daily Changes Subplot
    plt.subplot(2, 2, 2)
    plt.title('Changements Quotidiens Globaux')
    plt.plot(confirmed_daily_change.index[::30], confirmed_daily_change.values[::30], label='Nouveaux Cas', color='blue')
    plt.plot(deaths_daily_change.index[::30], deaths_daily_change.values[::30], label='Nouveaux Décès', color='red')
    plt.plot(recovered_daily_change.index[::30], recovered_daily_change.values[::30], label='Nouveaux Rétablis', color='green')
    plt.xlabel('Date')
    plt.ylabel('Changement Quotidien')
    plt.legend()
    plt.xticks(rotation=45)
    plt.grid(True, linestyle='--', alpha=0.7)

    # Mortality and Recovery Rates Subplot
    plt.subplot(2, 2, 3)
    plt.title('Taux de Mortalité et de Rétablissement')
    mortality_rate = deaths_totals / confirmed_totals * 100
    recovery_rate = recovered_totals / confirmed_totals * 100
    plt.plot(mortality_rate.index[::30], mortality_rate.values[::30], label='Taux de Mortalité (%)', color='red')
    plt.plot(recovery_rate.index[::30], recovery_rate.values[::30], label='Taux de Rétablissement (%)', color='green')
    plt.xlabel('Date')
    plt.ylabel('Pourcentage')
    plt.legend()
    plt.xticks(rotation=45)
    plt.grid(True, linestyle='--', alpha=0.7)

    # Active Cases Subplot
    plt.subplot(2, 2, 4)
    plt.title('Cas Actifs Globaux')
    active_cases = confirmed_totals - deaths_totals - recovered_totals
    plt.plot(active_cases.index[::30], active_cases.values[::30], label='Cas Actifs', color='purple')
    plt.xlabel('Date')
    plt.ylabel('Nombre de Cas Actifs')
    plt.legend()
    plt.xticks(rotation=45)
    plt.grid(True, linestyle='--', alpha=0.7)

    plt.tight_layout()
    plt.savefig(os.path.join('visualizations', '19-covid-global-analysis.png'), dpi=300)
    plt.close()
