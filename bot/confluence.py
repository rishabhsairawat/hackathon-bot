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
    limit = 100 # This is just for starting with the project
    pages = []
    count = 0
    while count < 100 and keep_going:
        results = confluence.get_all_pages_from_space(space, start=start, limit=100, status=None, expand='body.storage', content_type='page')
        pages.extend(results)
        count += len(results)
        if len(results) < limit:
            keep_going = False
        else:
            start = start + limit
    return pages

def save_confluence_docs():
    confluence = connect_to_Confluence()
    pages = get_all_pages(confluence, 'EN')
    for page in pages:
      page_id = page['id']
      # page_title = page['title']
      pdf_file_name = f'{page_id}.pdf'
      page_html = confluence.get_page_by_id(page_id, expand='body.storage')['body']['storage']['value']
      pdfkit.from_string(page_html, os.path.join(os.getenv('SOURCE_DIRECTORY'), pdf_file_name))

if __name__ == '__main__':
    save_confluence_docs()