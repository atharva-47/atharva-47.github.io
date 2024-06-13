import streamlit as st
import requests
from bs4 import BeautifulSoup
import time  # For throttling requests (optional)
from urllib.parse import urljoin  # For handling relative URLs

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

    Raises:
        ValueError: If the provided URL is invalid.
    """

    potential_ads = 0
    request_count = 0

    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise exception for non-2xx status codes

    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return 0  # Indicate error by returning 0 ads

    soup = BeautifulSoup(response.content, 'html.parser')

    # Heuristics for potential ad detection (can be further customized):
    potential_ads += len(soup.find_all('iframe'))
    potential_ads += len(soup.find_all('img', attrs={'alt': 'Advertisement'}))
    potential_ads += len(soup.find_all(class_=lambda class_: class_ and 'ad' in class_.lower()))
    potential_ads += len(soup.find_all(id=lambda id_: id_ and 'ad' in id_.lower()))

    # Explore deeper links (optional):
    if st.checkbox('Explore deeper links'):
        for link in soup.find_all('a', href=True):
            if request_count < max_requests:
                sub_url = urljoin(url, link['href'])  # Handle relative URLs
                request_count += 1
                potential_ads += count_ads(sub_url, max_requests - request_count)
                if request_count < max_requests:
                    time.sleep(delay_between_requests)  # Throttling

    return potential_ads

def estimate_time_wasted(ad_count, average_ad_duration=5):  # Assuming an average ad duration of 5 seconds
    """Estimates the time potentially wasted on ads based on estimated ad count and average ad duration.

    Args:
        ad_count (int): The estimated number of potential ads.
        average_ad_duration (float, optional): The assumed average duration of an ad in seconds. Defaults to 5.

    Returns:
        str: A user-friendly formatted string representing the estimated time wasted.
    """

    estimated_time = ad_count * average_ad_duration
    minutes, seconds = divmod(estimated_time, 60)
    hours, minutes = divmod(minutes, 60)

    time_wasted_str = ""
    if hours > 0:
        time_wasted_str += f"{hours} hour{'s' if hours > 1 else ''}"
    if minutes > 0:
        time_wasted_str += (f" {minutes} minute{'s' if minutes > 1 else ''}"
                             if time_wasted_str else f"{minutes} minutes")
    if seconds > 0:
        time_wasted_str += (f" {seconds:.2f} seconds"
                             if time_wasted_str else f"{seconds} seconds")

    return time_wasted_str

st.title('Website Ad Counter and Time Waster Estimator')
url = st.text_input('Enter a website URL:')

if st.button('Count Ads and Estimate Time Wasted'):
    if url:
        try:
            ad_count = count_ads(url)
            estimated_time_wasted = estimate_time_wasted(ad_count)

            st.write(f"Number of potential ads: {ad_count}")
            st.write(f"Estimated time potentially wasted: {estimated_time_wasted}")
        except
