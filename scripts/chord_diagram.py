import geopandas as gpd
import matplotlib.pyplot as plt

# Shapefile for Bolivia's departments (you'll need to have a suitable shapefile)
bolivia = gpd.read_file('path_to_shapefile/bolivia_departments.shp')

# Data for the pie charts (replace with your own data)
departments = ['La Paz', 'Cochabamba', 'Santa Cruz', 'Potosi', 'Oruro', 'Tarija', 'Chuquisaca', 'Beni', 'Pando']
populations = [2204248, 1750430, 2767509, 816874, 734231, 583548, 631062, 521488, 463474]

# Calculate the percentage of each department's population
total_population = sum(populations)
percentages = [pop / total_population * 100 for pop in populations]

# Plot the pie charts on the map
fig, ax = plt.subplots(1, 1, figsize=(10, 10))
bolivia.plot(ax=ax, color='lightgray', edgecolor='black')

for i, dept in enumerate(departments):
    dept_data = gpd.overlay(bolivia, bolivia[bolivia['NOM_DPTO'] == dept], how='intersection')
    ax.text(dept_data.centroid.x, dept_data.centroid.y, f"{dept}\n{populations[i]}", ha='center', va='center')

    # Create a pie chart
    sizes = [percentages[i], 100 - percentages[i]]
    labels = [f'{populations[i]}', '']
    ax.pie(sizes, labels=labels, startangle=90, counterclock=False, wedgeprops=dict(width=0.3), center=(dept_data.centroid.x, dept_data.centroid.y))

ax.set_aspect('equal')
ax.set_axis_off()
plt.title('Population Distribution by Department in Bolivia')
plt.show()