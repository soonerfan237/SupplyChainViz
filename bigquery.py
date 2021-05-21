from google.cloud import bigquery
from google.oauth2 import service_account

def get_turtles():
    credentials = service_account.Credentials.from_service_account_file('pythontest-313801-16e3ed7e71f6.json')

    project_id = 'pythontest-313801'
    client = bigquery.Client(credentials= credentials,project=project_id)

    query_job = client.query("""SELECT * FROM new_table.new_table LIMIT 1000 """)

    results = query_job.result()

    return results
