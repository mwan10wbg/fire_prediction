<h3> Fire Prediciton </h3>

<strong> about </strong>
We were inspired by recent forest fires in the west coast to experiment with the feasibility of predicting forest fires so authorities may take the necessary preventative measures.

Plots around 195,000 historical data points in the last five years of forest fires in the states of Washington, California and Oregon to reveal trends. Used clustering model to detect spots that have high risk to forest fire

We utilized open data of past fires in Washington, Oregon, and California and aimed to show trends with Plotly in Python. The data is from the following sources:
  
<a href="https://fsapps.nwcg.gov/gisdata.php"> USDA Forest Service: Cumulative MODIS fire detections </a>

<a href="https://catalog.data.gov/dataset/tiger-line-shapefile-2016-state-california-current-county-subdivision-state-based"> Data.gov:California </a>

<a href="https://catalog.data.gov/dataset/tiger-line-shapefile-2016-state-washington-current-county-subdivision-state-based"> Data.gov:Washington </a>

<a href="https://catalog.data.gov/dataset/tiger-line-shapefile-2016-state-oregon-current-county-subdivision-state-based"> Data.gov:Oregon </a>


<strong> Running the App </strong>

Clone and cd into the repo, then run `pip install requirements.txt`

Once requirements are satisfied, run `python app.py`

If the app does not open in your browser, navigate to `http://127.0.0.1:8050/`

![alt text](https://github.com/mwan10wbg/fire_prediction/blob/master/result/app%20demo.PNG)
