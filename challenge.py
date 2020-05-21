import requests
import datetime
import json

UTC_TIME_NOW = datetime.datetime.now(datetime.timezone.utc)
FORMATTED_TIME = UTC_TIME_NOW.strftime("%d/%m/%Y %H:%M:%S")


class ApiInterface():
    '''Provides an interface for the JSONPlaceholder API
    
    The class takes an input of the URL for the API as
    http://jsonplaceholder.typicode.com
    Several methods are then available to:
        - Get a post title by post id
        - Update a given post by adding a timestamp
        - Create a new post
        - Delete a given post
    '''
    
    def __init__(self, api_url):
        self.api_url = api_url

    def get_post_title(self, post_id):
        '''Gets a post title
        
        Gets a post title of given ID and prints the title
        '''
        response = requests.get(f'{self.api_url}/posts/{post_id}')

        print(response.json()['title'])

    def update_post(self, post_id):
        '''Updates a post
        
        Updates a post of given ID with UTC timestamp and prints the
        full JSON response of the POST request.
        '''
        payload = json.dumps({'time': FORMATTED_TIME})
        
        try:
            response = requests.patch(
                url=f'{self.api_url}/posts/{post_id}',
                data=payload,
                headers= {'Content-Type': 'application/json'}
            )
            print(response.json())
        except:
            print(f'PATCH failed with status {response.status_code}')

    def create_post(self):
        '''Creates a new post
        
        Creates a new post, checks for success of the create. If successful,
        get the new post ID, status code and X-Powered-By header and
        prints a tuple of (post_id, status_code, x_header)

        Returns:
            A tuple with the post_id, status_code and X-Powered-By header,
            for example:

            (1, 201, Express)
        '''
        payload = {
            'Title': 'Security Interview Post',
            'UserId': 500,
            'Body': 'This is an insertion test with a known API'
        }

        response = requests.post(
            url=f'{self.api_url}/posts',
            data=json.dumps(payload),
            headers={'Content-Type': 'application/json'}
        )

        if response.status_code == 201:
            post_id = response.json()['id']
            status_code = response.status_code
            x_header = response.headers['X-Powered-By']

            response_tuple = (post_id, status_code, x_header)

        print(response_tuple)

        return response_tuple

    def delete_post(self, post_id):
        '''Deletes given post
        
        Deletes the given post, then prints the status code for the
        delete requests and the X-Content-Type-Options header
        '''
        response = requests.delete(f'{self.api_url}/posts/{post_id}')

        print(response.status_code)
        print(response.headers['X-Content-Type-Options'])


def main():
    interface = ApiInterface('http://jsonplaceholder.typicode.com')
    interface.get_post_title(99)
    interface.update_post(100)
    create_response = interface.create_post()
    interface.delete_post(create_response[0])


if __name__ == "__main__":
    main()