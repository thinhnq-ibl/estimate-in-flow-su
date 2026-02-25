import geopandas as gpd

def get_seoul_geometry2():

    # 1. Load the original Vietnam district-level file
    vnm_city = gpd.read_file("../map/gadm36_KOR_1.shp")

    # 2. Get HCM shape
    db_seoul = vnm_city[vnm_city['GID_1'].str.contains("KOR.16", case=False, na=False)]

    print(db_seoul[["GID_1","NAME_1"]])

    # fig, ax = plt.subplots(figsize=(7, 7))
    # db_seoul.plot(ax=ax, facecolor='none', edgecolor='red', linewidth=2)
    # ax.set_title(f"Seoul Boundary")
    # plt.show()

    return db_seoul

def get_seoul_geometry():

    # 1. Load the original Vietnam district-level file
    vnm_city = gpd.read_file("../map/data_seoul_subzone.shp")

    # 2. Get HCM shape
    # db_seoul = vnm_city[vnm_city['GID_1'].str.contains("KOR.16", case=False, na=False)]

    # print(db_seoul[["GID_1","NAME_1"]])

    # fig, ax = plt.subplots(figsize=(7, 7))
    # db_seoul.plot(ax=ax, facecolor='none', edgecolor='red', linewidth=2)
    # ax.set_title(f"Seoul Boundary")
    # plt.show()

    return vnm_city
