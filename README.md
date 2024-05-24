# earthengine-dask

<!-- WARNING: THIS FILE WAS AUTOGENERATED! DO NOT EDIT! -->

This file will become your README and also the index of your
documentation.

# Prerequisites

- A [Google Earth Engine](https://earthengine.google.com/) account.
- Access to a Google Cloud Platform (GCP) [project with the Earth Engine
  API
  enabled](https://developers.google.com/earth-engine/cloud/earthengine_cloud_project_setup).
- A [Coiled](https://www.coiled.io/) account that is [setup to use the
  GCP project](https://docs.coiled.io/user_guide/setup/gcp/cli.html).

# Installation

``` sh
TODO...
```

# How to use

## Import Python packages

``` python
import altair as alt
import ee
from earthengine_dask.core import ClusterGEE
import google.auth
import pandas as pd
```

## Authenticate & Initialize Earth Engine

Get credentials and the GCP project ID, authenticating if necessary.

``` python
try:
    credentials, project_id = google.auth.default()
except google.auth.exceptions.DefaultCredentialsError:
    !gcloud auth application-default login
    credentials, project_id = google.auth.default()

ee.Initialize(credentials=credentials, project=project_id)
```

## Start Dask Cluster

Start up a Earth Engine enabled cluster. This may take a few minutes to
complete.

``` python
cluster = ClusterGEE(
    name='test-class-cluster',
    n_workers=2,
    worker_cpu=8,
    region='us-central1',
)
```

Retrieve a client for the cluster, and display it.

``` python
client = cluster.get_client()
client
```

## Submit Jobs

Test it out by: - Defining a function that can be distributed, -
Submitting jobs running the function to workers, - Gathering the results
locally, and - Displaying the results

``` python
# Get a list of countries to analyze.
country_fc = ee.FeatureCollection('USDOS/LSIB_SIMPLE/2017')
country_list = country_fc.aggregate_array('country_na').distinct().sort().getInfo()

# Write a function that can be run by the cluster workers. 
def get_country_stats(country_name):
    country = country_fc.filter(ee.Filter.eq('country_na', country_name))
    elev = ee.ImageCollection("COPERNICUS/DEM/GLO30").select('DEM').mosaic()
    return {
        'country': country_name, 
        'area_km2': country.geometry().area().multiply(1e-6).round().getInfo(), 
        'mean_elev': elev.reduceRegion(reducer=ee.Reducer.mean(),
                                       geometry=country.geometry(),
                                       scale=10000,
                                       ).get('DEM').getInfo(),
    }

# Create and submit jobs to among the workers.
submitted_jobs = [
    client.submit(get_country_stats, country)
    for country in country_list
]

# Gather up the results and display them.
results = client.gather(submitted_jobs)
df = pd.DataFrame(results)
df
```

## Shut down the cluster

``` python
cluster.shutdown()
```
