
# Traffic Index in Saudi Arabia and Middle East – Interactive Streamlit Dashboard

An interactive Streamlit dashboard for exploring hourly traffic congestion patterns across major cities in Saudi Arabia and the wider Middle East, built on top of the “Traffic Index in Saudi Arabia and Middle East” dataset from Kaggle.  
The project combines exploratory data analysis (EDA) in a Jupyter notebook with a deployed web dashboard for intuitive, visual exploration.

## Live Demo

The dashboard is deployed on Streamlit Cloud and accessible via this link:  
https://data-exploration-interactive-dashboard-project-aygyqvmpzzataea.streamlit.app/github

## Dataset

**Title:** Traffic Index in Saudi Arabia and Middle East  
**Source:** Kaggle dataset by Majed Alhulayel  
**Link:** https://www.kaggle.com/datasets/majedalhulayel/traffic-index-in-saudi-arabia-and-middle-east  

**Main columns:**

- `City`: City name (e.g., Riyadh, Jeddah, Abudhabi, Dubai, Cairo).  
- `Datetime`: Timestamp at roughly hourly resolution.  
- `TrafficIndexLive`: Live traffic index at that time.  
- `TrafficIndexWeekAgo`: Traffic index at the same time one week earlier.  
- `JamsCount`: Number of traffic jams observed.  
- `JamsDelay`: Total delay (e.g., in minutes) caused by jams.  
- `JamsLength`: Total jam length.  
- `TravelTimeHistoric`: Typical historical travel time.  
- `TravelTimeLive`: Observed live travel time.  

The data is suitable for studying temporal traffic patterns, city-level differences, and relationships between live and historic traffic indicators.

## Project Goals

This project aims to:

- Explore which cities experience the highest average congestion using traffic index and jam metrics.  
- Identify peak congestion hours during the day.  
- Detect extreme congestion events and outliers in jam counts, lengths, and delays.  
- Examine how last week’s traffic index relates to current traffic levels.  
- Provide an interactive dashboard that enables non-technical users to explore the data.  

## Key Insights

Traffic is generally moderate but can spike sharply during peak daytime hours, with the median traffic index around 10, an average of about 14, and rare events reaching values as high as 138.  
Jam-related metrics show a similar pattern: the median jam count is around 29 with an average of about 74, but extreme observations exceed 1,300 jams; the median jam length is roughly 12.2 with an average of about 49, while outliers go beyond 1,170 units; and the median delay is about 95.7 with an average near 288, yet the maximum delay approaches 9,989 minutes.  
All congestion measures—traffic index, jam count, jam length, and delays—rise together, so monitoring any one of them provides a good indication of overall traffic stress, and cities exhibit meaningful differences in their typical congestion levels, with rare but very intense outliers highlighting the importance of explicitly accounting for extreme events in traffic management and prediction.

## Features

- City-level exploration: Filter and focus on specific cities to compare congestion profiles.  
- Time-based analysis: Inspect patterns by date and time of day to see when congestion peaks.  
- Summary metrics: View key statistics for traffic index, jams, delays, and lengths.  

## Technology Stack

- Python  
- Pandas, NumPy for data manipulation  
- Matplotlib, Seaborn for visualization  
- Streamlit to build and deploy the interactive dashboard  
- Jupyter Notebook for exploratory data analysis and experimentation  

## Project Structure

dashboard.py                 -->  Streamlit dashboard entry point

project_notebook.ipynb       -->  EDA and analysis notebook

traffic_index.csv            -->  Original dataset downloaded from Kaggle

traffic_index_cleaned.csv    -->  Traffic dataset after cleaning 

requirements.txt             -->  Python dependencies

README.md                    --> Project documentation


## Getting Started (Local)

### 1. Clone the repository

git clone https://github.com/BayaderJ/Data-Exploration-Interactive-Dashboard-Project.git
cd Data-Exploration-Interactive-Dashboard-Project

### 2. (Optional) Create and activate a virtual environment

python -m venv venv
source venv/bin/activate      # On Windows: venv\Scripts\activate

### 3. Install dependencies

pip install -r requirements.txt

### 4. Add the dataset

- Place `traffic_index.csv` in the project directory (or in the path expected inside `dashboard.py` and the notebook).  
- The dataset can be downloaded from Kaggle:  
  https://www.kaggle.com/datasets/majedalhulayel/traffic-index-in-saudi-arabia-and-middle-east  

### 5. Run the dashboard

streamlit run dashboard.py

Then open the URL displayed in your terminal (usually `http://localhost:8501`).

## Using the Notebook

1. Open `project_notebook.ipynb` in Jupyter Notebook, JupyterLab, or VS Code.  
2. Run cells in order to:  
   - Load and inspect the dataset.  
   - View descriptive statistics and distributions.  
   - Explore temporal patterns and city comparisons.  
   - Investigate relationships such as `TrafficIndexWeekAgo` vs. `TrafficIndexLive`.  

## Possible Extensions

- Add forecasting models to predict future traffic index or jams.  
- Integrate real-time APIs for live updating dashboards.  
- Build additional comparison views.  
- Add alerting rules for when congestion metrics exceed specific thresholds.  


