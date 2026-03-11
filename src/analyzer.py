import extractor
from geopy.distance import geodesic
from geopy.geocoders import Nominatim
from datetime import datetime, timedelta

geolocator = Nominatim(user_agent="zone_cluster")

def num_of_items(images_data: list[dict]):
    return len(images_data)

def item_with_gps_num(images_data: list[dict]):
    result = 0
    for image in images_data:
        if image["has_gps"]:
            result += 1
    return result

def repeated_locations(images_data):
    locations = []
    for image in images_data:
        locations.append(image["latitude"], image["longitude"])
    pass # צריך לסיים את הפונקציה

def list_of_cameras(images_data: list[dict]):
    cameras = set()
    for image in images_data:
        if image["camera_make"] and image["camera_model"]:
            cameras.add(f"{image["camera_make"]} {image["camera_model"]}")
    return list(cameras)

def date_range_check(images_data: list[dict]):
    dates = []
    data_range = {}
    for image in images_data:
        dates.append(image["datetime"])
    
    data_range["start"] = min(dates)
    data_range["end"] = max(dates)
    
    return data_range

def time_gaps_between_pics(images_data, min_gap=12):
    dates = [datetime.strptime(image["datetime"], "%Y-%m-%d %H-%M-%S") for image in images_data]
    large_gaps = []
    
    for i in range(len(dates)-1):
        diff = dates[i+1] - dates[i]
        if diff >= timedelta(hours=min_gap):
            large_gaps.append({
                "from": images_data[i],
                "to": images_data[i+1],
                "hours_diff": diff.total_seconds() / 3600 # הפרש הזמן בשעות
            })
        
def detect_camera_switches(images_data):
    sorted_images = sorted(
        [img for img in images_data if img["datetime"]],
        key=lambda x: x["datetime"]
    )
    switches = []
    for i in range(1, len(sorted_images)):
        prev_cam = sorted_images[i-1].get("camera_model")
        curr_cam = sorted_images[i].get("camera_model")
        if prev_cam and curr_cam and prev_cam != curr_cam:
            switches.append({
                "date": sorted_images[i]["datetime"],
                "from": prev_cam,
                "to": curr_cam
            })
    return switches

def get_zone_name(lat, lon) -> str:
    try:
        location = geolocator.reverse(f"{lat}, {lon}", language="he")
        address = location.raw["address"]
        return (
            address.get("city") or
            address.get("town") or
            address.get("village") or
            address.get("county") or
            f"zone ({lat:.4f}, {lon:.4f})"
        )
    except:
        return f"zone ({lat:.4f}, {lon:.4f})"

def distance_km(coord1, coord2) -> float:
    return geodesic(coord1, coord2).kilometers

def cluster_locations(locations: list[tuple], radius_km=1.0) -> dict:
    """
    Clusters a list of GPS coordinates by proximity.

    Args:
        locations: List of tuples in one of two formats:
                   - (lat, lon)
                   - (lat, lon, id)
        radius_km: Maximum distance in kilometers between two points
                   to be considered in the same cluster. Default is 1.0.

    Returns:
        A dictionary where each key is a city name (or fallback coordinates),
        and each value is a dictionary containing:
            - device_id (str): (lat, lon) tuple for each location in the cluster
            - "location_count" (int): total number of locations in the cluster
    """
    normalized = []
    for i, loc in enumerate(locations):
        if len(loc) == 2:
            normalized.append({"id": f"location_{i+1}", "lat": loc[0], "lon": loc[1]})
        else:
            normalized.append({"id": loc[2], "lat": loc[0], "lon": loc[1]})

    visited = set()
    clusters = []

    for i, loc in enumerate(normalized):
        if i in visited:
            continue
        cluster = [loc]
        visited.add(i)

        for j, other in enumerate(normalized):
            if j in visited:
                continue
            if distance_km((loc["lat"], loc["lon"]), (other["lat"], other["lon"])) <= radius_km:
                cluster.append(other)
                visited.add(j)

        clusters.append(cluster)

    result = {}
    for cluster in clusters:
        center_lat = sum(l["lat"] for l in cluster) / len(cluster)
        center_lon = sum(l["lon"] for l in cluster) / len(cluster)
        zone_key = get_zone_name(center_lat, center_lon)  

        zone_data = {loc["id"]: (loc["lat"], loc["lon"]) for loc in cluster}
        zone_data["location_count"] = len(cluster)
        result[zone_key] = zone_data

    return result 
    
def analyze(images_data: list[dict]) -> dict:
    """
    Analyze the data and extracts insights
    
    arg:
        images_data: list from extract all func
        
    return:
        list of insights
    """
    pass
