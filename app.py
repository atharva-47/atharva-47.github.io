import streamlit as st
import requests
from bs4 import BeautifulSoup

# Function to count ads on a webpage
def count_ads(url):
    try:
        # Fetch the webpage content
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Example: Count div elements with class names commonly used for ads
        ad_divs = soup.find_all('div', class_='ad-class-name')  # Replace with actual ad class name
        
        # Count the ad divs
        ad_count = len(ad_divs)
        
        return ad_count
    
    except Exception as e:
        st.error(f"Error fetching or parsing the webpage: {e}")
        return None

# Streamlit web interface
def main():
    st.title("Webpage Ad Counter")
    
    # Input URL
    url = st.text_input("Enter the URL of the webpage:")
    
    if st.button("Count Ads"):
        if url:
            st.info(f"Counting ads on {url}...")
            ad_count = count_ads(url)
            
            if ad_count is not None:
                st.success(f"Number of ads on {url}: {ad_count}")
            else:
                st.error("Failed to retrieve ad count.")
        else:
            st.warning("Please enter a valid URL.")

if __name__ == "__main__":
    main()
