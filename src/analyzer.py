import extractor


def num_of_items(images_data: list[dict]):
    return len(images_data)

def item_with_gps_num(images_data: list[dict]):
    result = 0
    for image in images_data:
        if image["has_gps"]:
            result += 1
    return result

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
    
    
def analyze(images_data: list[dict]) -> dict:
    """
    Analyze the data and extracts insights
    
    arg:
        images_data: list from extract all func
        
    return:
        list of insights
    """
    pass
