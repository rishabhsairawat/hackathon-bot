from atlassian import Confluence # See https://atlassian-python-api.readthedocs.io/index.html
import os
import pdfkit

def connect_to_Confluence():
    '''
    Connect to Confluence
    
    Return
    ------
    A connector to Confluence
    '''
    print(os.getenv('CONFLUENCE_URL'))
    confluence = Confluence(
        url=os.getenv('CONFLUENCE_URL'),
        username=os.getenv('CONFLUENCE_USERNAME'),
        password=os.getenv('CONFLUENCE_API_TOKEN'),
        cloud=True)
    
    return confluence

def get_all_pages(confluence, space='EN'):
    '''
    Get all the pages within the MY-SPACE space.
    
    Parameters
    ----------
    confluence: a connector to Confluence
    space: Space of the Confluence (i.e. 'EN')
    
    Return
    ------
    List of page objects. Each page object has all the information concerning
    a Confluence page (title, body, etc)
    '''
    
    # There is a limit of how many pages we can retrieve one at a time
    # so we retrieve 100 at a time and loop until we know we retrieved all of
    # them.
    keep_going = True
    start = 0
    limit = 100
    pages = []
    print("Fetching confluence docs....")
    while keep_going:
        results = confluence.get_all_pages_from_space(space, start=start, limit=100, status=None, expand='body.storage', content_type='page')
        pages.extend(results)
        if len(results) < limit:
            keep_going = False
        else:
            start = start + limit
    print("Confluence docs fetched.")
    return pages

def save_confluence_docs():
    confluence = connect_to_Confluence()
    pages = get_all_pages(confluence, 'EN')
    excluded_conflunce_docs_id = ['3083005', '3094737']
    print("Downloading confluence docs....")
    for page in pages:
      page_id = page['id']
      if page_id in excluded_conflunce_docs_id:
        continue
      # page_title = page['title']
      pdf_file_name = f'{page_id}.pdf'
      page_html = confluence.get_page_by_id(page_id, expand='body.storage')['body']['storage']['value']
      pdfkit.from_string(page_html, os.path.join(os.getenv('SOURCE_DIRECTORY'), pdf_file_name))
    print("Confluence docs dowloaded.")

if __name__ == '__main__':
    save_confluence_docs()
