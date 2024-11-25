# -*- coding: utf-8 -*-
"""
Created on Fri Nov 22 14:59:06 2024

@author: Alex Lascelles
"""

import pandas as pd
import matplotlib.pyplot as plt
import math
import random

#####################################################################################################
## Load data, filter in only: Payload satellites, orbiting Earth, which have not been terminated
#####################################################################################################

satcat = pd.read_csv('satcat.csv')

# earth_orbiting_satellites = satcat[
#     (satcat['OBJECT_TYPE'] == 'PAY') &
#     (satcat['ORBIT_CENTER'] == 'EA') &
#     (satcat['DECAY_DATE'].isna())
# ]

# earth_orbiting_satellites.to_csv('earth_orbiting_satellites.csv', index=False)

#####################################################################################################
## Check how many orbits are close to circular (having an apogee and perigee within a certain % of eachother)
#####################################################################################################

earth_orbiting_satellites = pd.read_csv('earth_orbiting_satellites.csv')

# Define the eccentricity threshold
eccentricity_threshold = 0.1

# Define a function to check if the eccentricity is smaller than 0.1
def low_eccentricity(row):
    apogee = row['APOGEE']
    perigee = row['PERIGEE']
    
    # Check if apogee and perigee values are not null and not zero
    if pd.notnull(apogee) and pd.notnull(perigee) and apogee > 0 and perigee > 0:
        
        # Calculate eccentricity
        eccentricity = abs(apogee - perigee) / (apogee + perigee)
        
        # Check if eccentricity exceeds the threshold
        return eccentricity < eccentricity_threshold

    # If apogee or perigee is zero, return False (cannot calculate eccentricity)
    return False

# Check for rows where apogee or perigee is zero
def has_zero_apogee_or_perigee(row):
    apogee = row['APOGEE']
    perigee = row['PERIGEE']
    
    # Return True if either apogee or perigee is zero
    return apogee == 0 or perigee == 0

# Apply the function to each row and count the True results
count_low_eccentricity = earth_orbiting_satellites.apply(low_eccentricity, axis=1).sum()

print(f"Number of rows with eccentricity less than {eccentricity_threshold}: {count_low_eccentricity}")

# Apply the function to each row and print rows with high eccentricity
high_eccentricity = earth_orbiting_satellites[~earth_orbiting_satellites.apply(low_eccentricity, axis=1)]

print(f"Rows where orbits have eccentricity higher than {eccentricity_threshold}:")
print(high_eccentricity)

# Apply the function to count rows where apogee or perigee is zero
count_zero_apogee_or_perigee = earth_orbiting_satellites.apply(has_zero_apogee_or_perigee, axis=1).sum()
print(f"Number of rows with apogee or perigee equal to 0: {count_zero_apogee_or_perigee}")

#####################################################################################################
## Calculate Statistics: Max, Min, Distribution
#####################################################################################################

# Apogee and Perigee statistics
apogee_max = earth_orbiting_satellites['APOGEE'].max()
apogee_min = earth_orbiting_satellites['APOGEE'].min()
perigee_max = earth_orbiting_satellites['PERIGEE'].max()
perigee_min = earth_orbiting_satellites['PERIGEE'].min()

print(f"Max Apogee: {apogee_max} km, Min Apogee: {apogee_min} km")
print(f"Max Perigee: {perigee_max} km, Min Perigee: {perigee_min} km")

# Get distribution of apogee and perigee
apogee_description = earth_orbiting_satellites['APOGEE'].describe()
perigee_description = earth_orbiting_satellites['PERIGEE'].describe()

print(f"\nApogee Distribution:\n{apogee_description}")
print(f"\nPerigee Distribution:\n{perigee_description}")

# Plotting the distributions using histograms
plt.figure(figsize=(12, 6))

# Apogee histogram
plt.subplot(1, 2, 1)
plt.hist(earth_orbiting_satellites['APOGEE'].dropna(), bins=100, range=(0, 2000), color='blue', alpha=0.7)
plt.title('Apogee Distribution')
plt.xlabel('Apogee (km)')
plt.ylabel('Frequency')

# Perigee histogram
plt.subplot(1, 2, 2)
plt.hist(earth_orbiting_satellites['PERIGEE'].dropna(), bins=100, range=(0, 2000), color='green', alpha=0.7)
plt.title('Perigee Distribution')
plt.xlabel('Perigee (km)')
plt.ylabel('Frequency')

plt.tight_layout()
plt.show()

#####################################################################################################
## Count Satellites by Country
#####################################################################################################

# List of owners to count
owner_list = [
    'AB', 'ABS', 'AC', 'ALG', 'ANG', 'ARGN', 'ARM', 'ASRA', 'AUS', 'AZER', 'BEL', 'BELA', 'BERM',
    'BGD', 'BHUT', 'BOL', 'BRAZ', 'BUL', 'CA', 'CHBZ', 'CHTU', 'CHLE', 'CIS', 'COL', 'CRI', 'CZCH',
    'DEN', 'DJI', 'ECU', 'EGYP', 'ESA', 'ESRO', 'EST', 'ETH', 'EUME', 'EUTE', 'FGER', 'FIN', 'FR',
    'FRIT', 'GER', 'GHA', 'GLOB', 'GREC', 'GRSA', 'GUAT', 'HUN', 'IM', 'IND', 'INDO', 'IRAN', 'IRAQ',
    'IRID', 'IRL', 'ISRA', 'ISRO', 'ISS', 'IT', 'ITSO', 'JPN', 'KAZ', 'KEN', 'LAOS', 'LKA', 'LTU',
    'LUXE', 'MA', 'MALA', 'MCO', 'MDA', 'MEX', 'MMR', 'MNG', 'MUS', 'NATO', 'NETH', 'NICO', 'NIG',
    'NKOR', 'NOR', 'NPL', 'NZ', 'O3B', 'ORB', 'PAKI', 'PERU', 'POL', 'POR', 'PRC', 'PRY', 'PRES',
    'QAT', 'RASC', 'ROC', 'ROM', 'RP', 'RWA', 'SAFR', 'SAUD', 'SDN', 'SEAL', 'SEN', 'SES', 'SGJP',
    'SING', 'SKOR', 'SPN', 'STCT', 'SVN', 'SWED', 'SWTZ', 'TBD', 'THAI', 'TMMC', 'TUN', 'TURK', 
    'UAE', 'UK', 'UKR', 'UNK', 'URY', 'US', 'USBZ', 'VAT', 'VENZ', 'VTNM', 'ZWE'
]

# Filter the dataset to include only rows with OWNER in owner_list
satellites_by_owner = earth_orbiting_satellites[earth_orbiting_satellites['OWNER'].isin(owner_list)]

# Count the number of satellites for each owner in the list
owner_counts = satellites_by_owner['OWNER'].value_counts().reindex(owner_list, fill_value=0)

# Calculate the total number of satellites
total_satellites = owner_counts.sum()

# Convert counts to percentages
owner_percentages = (owner_counts / total_satellites * 100).sort_values(ascending=False)

# Display the result
print("\nPercentage of satellites by owner:")
print(owner_percentages)

#####################################################################################################
## Count Satellites by Date Launched
#####################################################################################################

# Convert LAUNCH_DATE to datetime format
earth_orbiting_satellites['LAUNCH_DATE'] = pd.to_datetime(earth_orbiting_satellites['LAUNCH_DATE'], errors='coerce')

# Define date ranges and count satellites launched within each range
counts_by_range = {
    "Launched in 2024": earth_orbiting_satellites[(earth_orbiting_satellites['LAUNCH_DATE'].dt.year == 2024)].shape[0],
    "Launched in 2023": earth_orbiting_satellites[(earth_orbiting_satellites['LAUNCH_DATE'].dt.year == 2023)].shape[0],
    "Launched in 2022": earth_orbiting_satellites[(earth_orbiting_satellites['LAUNCH_DATE'].dt.year == 2022)].shape[0],
    "Launched in 2021": earth_orbiting_satellites[(earth_orbiting_satellites['LAUNCH_DATE'].dt.year == 2021)].shape[0],
    "Launched in 2020": earth_orbiting_satellites[(earth_orbiting_satellites['LAUNCH_DATE'].dt.year == 2020)].shape[0],
    "Launched in 2010-2020": earth_orbiting_satellites[(earth_orbiting_satellites['LAUNCH_DATE'].dt.year >= 2010) & (earth_orbiting_satellites['LAUNCH_DATE'].dt.year < 2020)].shape[0],
    "Launched in 2000-2010": earth_orbiting_satellites[(earth_orbiting_satellites['LAUNCH_DATE'].dt.year >= 2000) & (earth_orbiting_satellites['LAUNCH_DATE'].dt.year < 2010)].shape[0],
    "Launched in 1990-2000": earth_orbiting_satellites[(earth_orbiting_satellites['LAUNCH_DATE'].dt.year >= 1990) & (earth_orbiting_satellites['LAUNCH_DATE'].dt.year < 2000)].shape[0],
    "Launched in 1980-1990": earth_orbiting_satellites[(earth_orbiting_satellites['LAUNCH_DATE'].dt.year >= 1980) & (earth_orbiting_satellites['LAUNCH_DATE'].dt.year < 1990)].shape[0],
    "Launched in 1970-1980": earth_orbiting_satellites[(earth_orbiting_satellites['LAUNCH_DATE'].dt.year >= 1970) & (earth_orbiting_satellites['LAUNCH_DATE'].dt.year < 1980)].shape[0],
    "Launched in 1958-1970": earth_orbiting_satellites[(earth_orbiting_satellites['LAUNCH_DATE'].dt.year >= 1958) & (earth_orbiting_satellites['LAUNCH_DATE'].dt.year < 1970)].shape[0]
}

# Print results
for range_label, count in counts_by_range.items():
    print(f"{range_label} = {count}")
    
    
#####################################################################################################
## Deal with data for plotting
#####################################################################################################

earth_radius_km = 6371

# Calculate average orbit radius as the mean of APOGEE and PERIGEE
earth_orbiting_satellites['AVERAGE_RADIUS'] = (earth_orbiting_satellites['APOGEE'] + earth_orbiting_satellites['PERIGEE']) / 2

# Identify rows with AVERAGE_RADIUS greater than 50000
filtered_out_satellites = earth_orbiting_satellites[earth_orbiting_satellites['AVERAGE_RADIUS'] > 50000]

# Print the rows that are being filtered out
if not filtered_out_satellites.empty:
    print("Rows with AVERAGE_RADIUS greater than 50000 (filtered out):")
    print(filtered_out_satellites)

# Filter out rows with AVERAGE_RADIUS > 50000
filtered_satellites = earth_orbiting_satellites[earth_orbiting_satellites['AVERAGE_RADIUS'] <= 50000]

# Generate a random angle for each row
filtered_satellites['RANDOM_THETA'] = filtered_satellites.apply(lambda _: math.radians(random.uniform(0, 360)), axis=1)

# Calculate X and Y coordinates based on the generated angle
filtered_satellites['X_COORD'] = (filtered_satellites['AVERAGE_RADIUS'] + earth_radius_km) * filtered_satellites['RANDOM_THETA'].apply(math.cos)
filtered_satellites['Y_COORD'] = (filtered_satellites['AVERAGE_RADIUS'] + earth_radius_km) * filtered_satellites['RANDOM_THETA'].apply(math.sin)

# Save the filtered data to a new CSV file
filtered_satellites.to_csv('earth_orbiting_satellites_50k.csv', index=False)

print("Filtered data saved to 'earth_orbiting_satellites_50k.csv'.")

