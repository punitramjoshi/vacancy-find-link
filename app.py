import streamlit as st
from main import JobFinder
import json

# Create an instance of JobFinder
job_finder = JobFinder()
st.title('LinkedIn Job Finder')
st.write('Enter the URL of the LinkedIn company:')
company_url = st.text_input('Company URL')

def download_data(jobs_data):
    json_data = json.dumps(jobs_data, indent=4)
    st.download_button(label='Download JSON', data=json_data, file_name='job_data.json', mime='application/json')


if company_url:
    # Fetch the search_id using the provided URL
    search_id = job_finder.fetch_search_id(company_url)

    # Create dropdowns for each parameter
    job_type = st.selectbox('Job Type', ['anything', 'full-time', 'part-time', 'contract', 'internship', 'temporary', 'volunteer'])
    experience_level = st.selectbox('Experience Level', ['anything', 'internship', 'entry_level', 'associate', 'mid_senior_level', 'director'])
    when = st.selectbox('When', ['anytime', 'yesterday', 'past-week', 'past-month'])
    flexibility = st.selectbox('Flexibility', ['anything', 'remote', 'on-site', 'hybrid'])
    geo_id = st.text_input('Geo ID', value='92000000')
    keyword = st.text_input('Keyword', value=None)

    if st.button('Fetch Jobs'):
        # Call the job_scrape method with selected parameters
        jobs_data = job_finder.job_scrape(
            search_id=str(search_id),
            job_type=job_type,
            experience_level=experience_level,
            when=when,
            flexibility=flexibility,
            geo_id=geo_id,
            keyword=keyword
        )

        # Display the fetched job data
        st.write(jobs_data)

        if st.button('Download Job Data'):
            download_data(jobs_data)
