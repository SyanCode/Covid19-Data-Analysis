import urllib.request as urllib2
import os
import pandas as pd
import matplotlib.pyplot as plt
import csv

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

def read_CSV(file):
    '''
    Read a csv file and return :
    - fields name as string in a list
    - datas dictionary by countries in a list
    '''
    # datas is an empty list
    datas = []
    # open the file passed in argument as csvfile
    with open(file, newline='', encoding='utf-8') as csvfile:
        # Create a dictionary with all datas
        reader = csv.DictReader(csvfile)
        # each row in reader is a dictionary by country
        for row in reader:
            # add row in datas list
            datas.append(row)
        # return the list of dictionaries by countries
        return datas

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
    if download_file(confirmed_url, confirmed_file):
        print(f'Téléchargement du fichier {confirmed_file} terminé avec succès')
    else:
        print(f'Téléchargement du fichier {confirmed_file} impossible')

    if download_file(deaths_url, deaths_file):
        print(f'Téléchargement du fichier {deaths_file} terminé avec succès')
    else:
        print(f'Téléchargement du fichier {deaths_file} impossible')

    if download_file(recovered_url, recovered_file):
        print(f'Téléchargement du fichier {recovered_file} terminé avec succès')
    else:
        print(f'Téléchargement du fichier {recovered_file} impossible')

    # Read the data
    confirmed = pd.read_csv(os.path.join('data', confirmed_file))
    deaths = pd.read_csv(os.path.join('data', deaths_file))
    recovered = pd.read_csv(os.path.join('data', recovered_file))

    # Plotting
    plt.figure(figsize=(15, 5))
    plt.subplot(131)
    plt.title('Cas Confirmés')
    plt.plot(confirmed.iloc[:, 4:].sum())
    plt.subplot(132)
    plt.title('Décès')
    plt.plot(deaths.iloc[:, 4:].sum())
    plt.subplot(133)
    plt.title('Rétablis')
    plt.plot(recovered.iloc[:, 4:].sum())
    plt.tight_layout()
    plt.savefig(os.path.join('visualizations', '19-covid-global.png'))
    plt.close()

    # Read CSV
    countries = read_CSV(os.path.join('data', confirmed_file))
    print("Liste des pays et régions recensés")
    print("----------------------------------")
    for row in countries:
        print(row.get('Province/State', 'N/A'), row.get('Country/Region', 'N/A'))