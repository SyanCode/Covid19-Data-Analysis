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

    # Plotting
    plt.figure(figsize=(18, 6))

    # Confirmed Cases Plot
    plt.subplot(131)
    plt.title('Cas Confirmés Globaux')
    plt.plot(confirmed_totals.index[::30], confirmed_totals.values[::30], label='Confirmés')
    plt.xlabel('Date')
    plt.ylabel('Nombre de Cas')
    plt.xticks(rotation=45)
    plt.grid(True, linestyle='--', alpha=0.7)

    # Deaths Plot
    plt.subplot(132)
    plt.title('Décès Globaux')
    plt.plot(deaths_totals.index[::30], deaths_totals.values[::30], color='red', label='Décès')
    plt.xlabel('Date')
    plt.ylabel('Nombre de Décès')
    plt.xticks(rotation=45)
    plt.grid(True, linestyle='--', alpha=0.7)

    # Recovered Plot
    plt.subplot(133)
    plt.title('Cas Rétablis Globaux')
    plt.plot(recovered_totals.index[::30], recovered_totals.values[::30], color='green', label='Rétablis')
    plt.xlabel('Date')
    plt.ylabel('Nombre de Rétablis')
    plt.xticks(rotation=45)
    plt.grid(True, linestyle='--', alpha=0.7)

    plt.tight_layout()
    plt.savefig(os.path.join('visualizations', '19-covid-global.png'), dpi=300)
    plt.close()