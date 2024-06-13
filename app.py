import streamlit as st
import requests
from bs4 import BeautifulSoup
import time  # For throttling requests (optional)

def count_ads(url, max_requests=10, delay_between_requests=1):
  """Counts potential ads on a website using a combination of heuristics.

  Args:
      url (str): The URL of the website to analyze.
      max_requests (int, optional): The maximum number of requests to make
          within a short timeframe to avoid overloading the server. Defaults to 10.
      delay_between_requests (float, optional): The delay (in seconds) between
          requests for throttling. Defaults to 1.

  Returns:
      int: The estimated number of potential ads.
  """

  potential_ads = 0
  request_count = 0

  while request_count < max_requests:
    try:
      response = requests.get(url)
      response.raise_for_status()  # Raise exception for non-2xx status codes
      soup = BeautifulSoup(response.content, 'html.parser')

      # Heuristics for potential ad detection (can be further customized):
      potential_ads += len(soup.find_all('iframe'))
      potential_ads += len(soup.find_all('img', attrs={'alt': 'Advertisement'}))
      potential_ads += len(soup.find_all(class_=lambda class_: class_ and 'ad' in class_.lower()))
      potential_ads += len(soup.find_all(id=lambda id_: id_ and 'ad' in id_.lower()))

      request_count += 1
      if request_count < max_requests:
        time.sleep(delay_between_requests)  # Throttling to avoid overloading servers

    except requests.exceptions.RequestException as e:
      print(f"Error: {e}")
      break  # Stop further requests on error

  return potential_ads

st.title('Website Ad Counter')
url = st.text_input('Enter a website URL:')

if st.button('Count Ads'):
  if url:
    try:
      ad_count = count_ads(url)
      st.write(f"Number of potential ads: {ad_count}")
    except requests.exceptions.RequestException as e:
      st.error(f"Error: {e}")
  else:
    st.warning('Please enter a URL.')
