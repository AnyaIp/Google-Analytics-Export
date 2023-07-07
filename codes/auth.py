from apiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials

class gaAuth:
    def __init__(self, key_file_location:str, view_id:str):
        """
        Args:
            - key_file_location: path to the key file (.json) downloaded
            - view_id: view id of GA4 project
        
        """
        self.key_file_location = key_file_location
        self.view_id = view_id
        
    def authenticate(self):
        """
        Initializes an Analytics Reporting API V4 service object.
        Returns:
            - An authorized Analytics Reporting API V4 service object.
        """
        scopes = ['https://www.googleapis.com/auth/analytics.readonly']
        key_file_location = self.key_file_location
        credentials = ServiceAccountCredentials.from_json_keyfile_name(key_file_location, scopes)
        
        # Build the service object.
        analytics = build('analyticsreporting', 'v4', credentials=credentials)
        return analytics

if __name__== '__main__':
    key_file_location = 'xxxxxx'
    view_id = 'xxxxx'
    auth = gaAuth(key_file_location, view_id)
    # the authenticated object
    analytics = auth.authenticate()

