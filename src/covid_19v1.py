import urllib.request as urllib2
import os

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