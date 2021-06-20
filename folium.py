import folium

base_lat = 26.9124
base_long = 75.7873
default_tooltip = "Redeem EarthCoin here"

m = folium.Map(location = [base_lat, base_long], zoom_start = 12)

list_coords = [[26.91241,75.7873],[26.9124,75.7873],[26.91243,75.7873]]

for coord in list_coords:
        # print(coord)
        folium.Marker(coord, popup = "<b>Shop</b>", tooltip = default_tooltip).add_to(m)

m.save("index.html")
