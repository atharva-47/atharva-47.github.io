import streamlit as st
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import time  # For throttling requests (optional)


def count_ads(url, max_requests=10, delay_between_requests=1):
    """Counts potential ads on a website using a combination of heuristics."""
    potential_ads = 0

    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise exception for non-2xx status codes

        soup = BeautifulSoup(response.content, 'html.parser')

        # Heuristics for potential ad detection (can be further customized):
        potential_ads += len(soup.find_all('iframe'))
        potential_ads += len(soup.find_all('img', attrs={'alt': 'Advertisement'}))
        potential_ads += len(soup.find_all(class_=lambda class_: class_ and 'ad' in class_.lower()))
        potential_ads += len(soup.find_all(id=lambda id_: id_ and 'ad' in id_.lower()))

    except requests.exceptions.RequestException as e:
        raise ValueError(f"Error fetching URL: {e}")

    return potential_ads


def estimate_time_wasted(ad_count, average_ad_duration=5):
    """Estimates the time potentially wasted on ads based on estimated ad count and average ad duration."""
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
average_cpm = st.number_input('Estimated Cost-Per-Thousand Impressions (Optional):', min_value=0.0)

if st.button('Count Ads and Estimate Time Wasted'):
    if url:
        try:
            ad_count = count_ads(url)
            estimated_time_wasted = estimate_time_wasted(ad_count)

            st.write(f"Number of potential ads: {ad_count}")
            st.write(f"Estimated time potentially wasted: {estimated_time_wasted}")

            st.info("**Disclaimer:** Estimating a website's ad revenue is not possible from the user's side. "
                    "Ad revenue depends on various factors like user location, demographics, and browsing history. "
                    "This application can only estimate the time potentially wasted on ads based on the number of potential ads and an assumed average ad duration.")

            if average_cpm > 0:
                estimated_impressions = ad_count * 1000  # Assuming 1000 impressions per page view
                estimated_revenue = estimated_impressions * average_cpm / 1000000  # Convert to millions

                st.write("**Informative Estimation (not accurate):**")
                st.write(f"Estimated ad impressions (assuming 1000 per page view): {estimated_impressions:,}")
                st.write(f"Estimated potential ad revenue based on your CPM input: ${estimated_revenue:.2f} (highly dependent on actual ad rates)")

        except ValueError as ve:
            st.error(f"Error: {ve}")
            st.write("An error occurred while fetching the website. Please try again.")
        except requests.exceptions.RequestException as re:
            st.error(f"Error: {re}")
            st.write("An error occurred while fetching the website. Please try again.")
