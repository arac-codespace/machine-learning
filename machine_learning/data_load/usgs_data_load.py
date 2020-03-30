import requests
import io
from collections import namedtuple
import pandas as pd
import pdb


class UTIL:       
    def _get(self, url, end_point, header):
        response = None
        try:
            uri = f'{url}/{end_point}'
            print(uri)
            response = requests.get(
                uri,
                headers=header
            )
        except Exception as err:
            print('Caught exception: {}'.format(str(err)))
            InstanceProperties = namedtuple(
                'ResponseProperties', ['status_code'])
            response = InstanceProperties(status_code=500)
        return response

    def make_get_request(self, url, header=None, end_point=None):

        print('Calling: {}'.format(url))
        if not end_point:
            raise Exception('Error: end_point is None.')


        res = self._get(url, end_point, header)

        return res

class USGS(UTIL):
    DEFAULT_URL = "https://waterservices.usgs.gov/nwis"

    """
        For more info about params for site endpoint:
        https://waterservices.usgs.gov/rest/Site-Service.html#format
    """
    def get_sites(self, stateCd, **params):
            query_params = []
            if stateCd:
                param = f"stateCd={stateCd}"
                query_params.append(param)

            if params:
                for param in params:
                    key = param
                    value = params[param]
                    query_params.append(f"{key}={value}")

            end_point = "&".join(query_params)
            end_point = f"site/?{end_point}"
            response = self.make_get_request(self.DEFAULT_URL, end_point = end_point)        
            data = response.content
            # Eliminate comments and the second line after the headers...
            df = pd.read_csv(io.StringIO(data.decode('utf-8')), sep='\t', comment='#')
            df = df.iloc[1:].reset_index(drop=True)            
            return df

    def get_site_observations(self, site,**params):
        # Takes the requests json response
        def parse_observations_response(site, response):
            # Get that data from json response
            data = []
            for timeseries in response["value"]["timeSeries"]:
                for row in timeseries["values"]:
                    for value_row in row["value"]:
                        # Create a new row dictionary...
                        new_row = {}
                        # Qualifiers are in a list. Convert to str...
                        new_row["site_no"] = site
                        new_row["date_time"] = value_row.get("dateTime")
                        new_row["value"] = value_row.get("value")
                        new_row["qualifiers"] = ",".join(value_row.get("qualifiers"))

                        data.append(new_row)
            return data  
      
        query_params = []
        if site:
            param = f"site={site}"
            query_params.append(param)

        if params:
            for param in params:
                key = param
                value = params[param]
                query_params.append(f"{key}={value}")

        end_point = "&".join(query_params)
        end_point = f"iv/?{end_point}"
        response = self.make_get_request(self.DEFAULT_URL, end_point = end_point)        
        response = response.json()

        data = parse_observations_response(site, response)
        df = pd.DataFrame.from_dict(data)
        return df