from typing import List
import pandas as pd
from .handle_errors import *
from .auth import gaAuth
    
class gaQuery:
    def __init__(
        self,
        auth=None,
        metrics:List=['ga:sessions'],
        dimensions:List=['ga:country'],
        startDate: str='7daysAgo',
        endDate: str='today'
    ):
        """
        You can explore the available metrics and dimensions on UA Dimensions & Metrics Explorer
        (https://ga-dev-tools.google/dimensions-metrics-explorer/)
        
        Args:
            - auth: the gaAuth object for authentication
            - metrics: List of metrics to retrieve
            - dimensions: List of dimensions to retrieve
            - startDate : The start date
            - endDate: The end date
        """
        self.auth = auth
        self.metrics = metrics
        self.dimensions = dimensions
        self.start_date = startDate
        self.end_date = endDate
        
    def pull_response(self):
        """
        Queries the Analytics Reporting API V4.
        Returns:
            - The Analytics Reporting API V4 response.
        """
        outputs = []
        analytics = self.auth.authenticate()
        query_dict = self.query()
        response = analytics.reports().batchGet(body={'reportRequests': [query_dict]}).execute()
        try:
            record_count = response['reports'][0]['data']['rowCount']
            if record_count == 0:
                raise resultException('Your search returns 0 record.')
            print('{} records are returned.'.format(record_count))
            outputs.append(response)
            # pagination
            while response['reports'][0].get('nextPageToken'):
                page_token = response['reports'][0].get('nextPageToken')
                query_dict = self.query(page_token)
                response = analytics.reports().batchGet(body={'reportRequests': [query_dict]}).execute()
                outputs.append(response)
            return outputs
        except:
            raise resultException('Failed to return any result. Plese check your query.')
    
    def retrieve_data(self):
        """
        Retrieve data with the data query
        """
        outputs = self.pull_response()
        df = pd.concat([self.sort_data(response) for response in outputs])
        return df
    
    def to_excel(self, filename:str):
        """
        Export the response directly into Excel
        Args:
            - filename: path of the file to export
        """
        df = self.retrieve_data()
        df.to_excel(filename, index=False)
        

    def query(self, page_token=None):
        return {
            'viewId': self.auth.view_id,
            'dateRanges': [{'startDate': self.start_date, 'endDate': self.end_date}],
            'metrics': [{'expression': m} for m in self.metrics],
            'dimensions': [{'name': d} for d in self.dimensions],
            'pageToken': page_token
        }
        
    @staticmethod
    def sort_data(response):
        """
        Parse the Analytics Reporting API V4 response.
        Args:
            - The Analytics Reporting API V4 response
        Returns:
            - The data in a Pandas DataFrame
        """
        records = response['reports'][0]['data']['rows']
        records = [row['dimensions'] + row['metrics'][0]['values'] for row in records]
        headers = response['reports'][0]['columnHeader']
        dims = headers['dimensions']
        vals = headers['metricHeader']['metricHeaderEntries']
        df = pd.DataFrame(records)
        df.columns = dims + [x['name'] for x in vals]
        for col in vals:
            if col['type'] == 'INTEGER':
                df[col['name']] = df[col['name']].apply(lambda x: int(float(x)))
            elif col['type'] in ['PERCENT', 'TIME']:
                df[col['name']] = df[col['name']].apply(lambda x: round(float(x), 2))
        return df
