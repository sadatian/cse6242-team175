# K MEANS CLUSTERING
#
# Precedes GMM in pipeline
#
# INPUT: a ZIP code or neighborhood, a distance threshold
# OUTPUT: crime cluster centers (the number and locations of which will be inputs/parameters for GMM), the number of clusters

from typing import Union
import numpy as np
from shapely.geometry import shape
from sklearn.cluster import KMeans
from sklearn.mixture import GaussianMixture
from sklearn.metrics.pairwise import euclidean_distances
import pandas as pd
from scipy.spatial import cKDTree
import geopy
from geopy.geocoders import Nominatim
from geopy import Point, distance
from collections import Counter

class CrimeCluster:
    def __init__(self, df_crime: pd.DataFrame, neighborhoods: dict, zip_codes: dict):
        self._df_crime = df_crime
        self._neighborhoods = df_crime.Neighborhood.unique()
        self._zip_codes = df_crime['Zip Code'].unique()
        self._neighborhood_to_center = self.__property_to_center(neighborhoods, 'pri_neigh')
        self._zip_to_center = self.__property_to_center(zip_codes, 'zip')
        self._tree = cKDTree(df_crime[['Latitude', 'Longitude']])
        
    def __property_to_center(self, geo: dict, property: str) -> dict:
        
        property_to_center = {}
        for location in geo['features']:
            
            name = location['properties'][property]
            if property == 'zip':
                name = int(name)
                
            center = shape(location['geometry']).centroid
            center = center.x, center.y
            property_to_center[name] = center
            
        return property_to_center
        
        # TO-DO: will want to later allow different data inputs to be specified, since we'll want to filter by crime type
    def GMM(self, location: Union[str, int], crime_type: str, thresh_dist: float=0.025) -> (pd.DataFrame, int):
        '''
        Given a neighborhood or ZIP code, finds the best k-means cluster centers for crimes within the threshold
            distance of the center of the neighborhood or ZIP code, then returns the GMM means and covariance matrices.
        Returns the tuple (number of cluster centers, array of the cluster centers , covariance matrices)
        '''
        # convert to upper-case
        if isinstance(location, str):
            location = location.title()

        # return None if the location isn't valid
        if location not in self._neighborhoods and location not in self._zip_codes:
            return None

        if isinstance(location, str):
            center_y, center_x = self._neighborhood_to_center[location]
        else:
            center_y, center_x = self._zip_to_center[location]

        center = np.array([center_x, center_y])
        
        if crime_type != 'ALL':
            df_crime = self._df_crime[self._df_crime['Crime Type'] == crime_type]
        else:
            df_crime = self._df_crime
        
        crime_locations = df_crime[['Latitude', 'Longitude']]
        
        distances = np.linalg.norm((crime_locations - center), axis=1, ord=1)
        crime_thresholded = df_crime[distances < thresh_dist][['Latitude', 'Longitude']]

        # the actual k-means
        old_inertia = np.inf
        best_k = 8
        for k in range(2, 8):
            model = KMeans(n_clusters=k).fit(crime_thresholded)
            new_inertia = model.inertia_
            n_per_cluster = Counter(model.labels_)
            if new_inertia * 1.05 > old_inertia or min(n_per_cluster.values()) < 0.1 * sum(n_per_cluster.values()):
                best_k = k - 1
                break
            else:
                old_inertia = new_inertia
        k_means = KMeans(n_clusters=best_k).fit(crime_thresholded)
        centers = k_means.cluster_centers_
        df_centers = pd.DataFrame(data=centers, columns=['lat', 'lon'])

        model = GaussianMixture(n_components=best_k, means_init=df_centers).fit(crime_thresholded)
        n_per_cluster = Counter(k_means.labels_)
        n_weights = np.zeros(best_k)
        for i in n_per_cluster.keys():
            n_weights[i] = n_per_cluster[i]
        return best_k, model.means_, model.covariances_, n_weights
    
    def GMM_Address(self, address: str, radius: int, crime_type: str, thresh_dist: float=0.025):
        
        geolocator = Nominatim(user_agent='team175')
        location = geolocator.geocode(address)
        print(location)
        
        start = Point(location.latitude, location.longitude)
        dist = distance.geodesic(miles=radius)
        end = dist.destination(start, bearing=0)
        degrees = end.latitude - start.latitude
        
        center = (location.latitude, location.longitude)
        points = self._tree.query_ball_point(center, degrees)
        
        if crime_type != 'ALL':
            df_crime = self._df_crime.iloc[points]
            df_crime = df_crime[df_crime['Crime Type'] == crime_type]
        else:
            df_crime = self._df_crime.iloc[points]
        
        crime_thresholded = df_crime[['Latitude', 'Longitude']]

        old_inertia = np.inf
        best_k = 8
        for k in range(2, 8):
            model = KMeans(n_clusters=k).fit(crime_thresholded)
            new_inertia = model.inertia_
            n_per_cluster = Counter(model.labels_)
            if new_inertia * 1.05 > old_inertia or min(n_per_cluster.values()) < 0.1 * sum(n_per_cluster.values()):
                best_k = k - 1
                break
            else:
                old_inertia = new_inertia
        k_means = KMeans(n_clusters=best_k).fit(crime_thresholded)
        centers = k_means.cluster_centers_
        df_centers = pd.DataFrame(data=centers, columns=['lat', 'lon'])

        model = GaussianMixture(n_components=best_k, means_init=df_centers).fit(crime_thresholded)
        n_per_cluster = Counter(k_means.labels_)
        n_weights = np.zeros(best_k)
        for i in n_per_cluster.keys():
            n_weights[i] = n_per_cluster[i]
        return best_k, model.means_, model.covariances_, df_crime, n_weights, start
    
    def GMM_Chicago(self, crime_type):
        
        if crime_type != 'ALL':
            df_crime = self._df_crime[self._df_crime['Crime Type'] == crime_type]
        else:
            df_crime = self._df_crime
        
        crime_thresholded = df_crime[['Latitude', 'Longitude']]

        old_inertia = np.inf
        best_k = 8
        for k in range(2, 8):
            model = KMeans(n_clusters=k).fit(crime_thresholded)
            new_inertia = model.inertia_
            n_per_cluster = Counter(model.labels_)
            if new_inertia * 1.05 > old_inertia or min(n_per_cluster.values()) < 0.1 * sum(n_per_cluster.values()):
                best_k = k - 1
                break
            else:
                old_inertia = new_inertia
        k_means = KMeans(n_clusters=best_k).fit(crime_thresholded)
        centers = k_means.cluster_centers_
        df_centers = pd.DataFrame(data=centers, columns=['lat', 'lon'])
        
        model = GaussianMixture(n_components=best_k, means_init=df_centers).fit(crime_thresholded)
        n_per_cluster = Counter(k_means.labels_)
        n_weights = np.zeros(best_k)
        for i in n_per_cluster.keys():
            n_weights[i] = n_per_cluster[i]
        return best_k, model.means_, model.covariances_, n_weights
        