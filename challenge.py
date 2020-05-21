import requests
import datetime
import json

UTC_TIME_NOW = datetime.datetime.now(datetime.timezone.utc)
FORMATTED_TIME = UTC_TIME_NOW.strftime("%d/%m/%Y %H:%M:%S")

class ApiInterface():

    def __init__(self, api_url):
        self.api_url = api_url


    def get_post_title(self, post_id):
        response = requests.get(f'{self.api_url}/posts/{post_id}')
        print(response.json()['title'])


    def update_post(self, post_id):
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
            rec_id = response.json()['id']
            status_code = response.status_code
            x_header = response.headers['X-Powered-By']

            response_tuple = (rec_id, status_code, x_header)

        print(response_tuple)

        return response_tuple

    def delete_post(self, post_id):
        response = requests.delete(f'{self.api_url}/posts/{post_id}')

        status_header = {
            'status': response.status_code,
            'X-Content-Type-Options': response.headers['X-Content-Type-Options']
        }

        print(status_header)


def main():

    interface = ApiInterface('http://jsonplaceholder.typicode.com')
    # interface.get_post_title(99)
    # interface.update_post(100)
    create_response = interface.create_post()
    interface.delete_post(create_response[0])

    # get_post(99)
    # update_post(100)

    # new_post = create_post()
    # if new_post.status_code == 201:
    #     rec_id = new_post.json()['id']
    #     status_code = new_post.status_code
    #     x_header = new_post.headers['X-Powered-By']
    #     response_tuple = (rec_id, status_code, x_header)
    #     print(response_tuple)
    # else:
    #     print('Create post failed')

    # delete_post(response_tuple[0])


if __name__ == "__main__":
    main()