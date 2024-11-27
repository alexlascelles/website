# -*- coding: utf-8 -*-
"""
Created on Mon Nov 25 16:00:20 2024

@author: Alex Lascelles
"""

import pandas as pd
import matplotlib.pyplot as plt


## CHOOSE PLAYLIST
a = "data/liked.csv"
b = "data/alex-liked_songs.csv"
c = "data/alex-current_favourites.csv"



#####################################################################
## Artist Counts
#####################################################################

# Strip any leading/trailing whitespace in column names
songs.columns = songs.columns.str.strip()

# Split and expand the 'Artist Name(s)' column if there are multiple artists per track
songs['Artist Name(s)'] = songs['Artist Name(s)'].str.split(',')

# Explode the list of artists so each artist has their own row
songs_artists = songs.explode('Artist Name(s)')

# Remove any extra whitespace around artist names
songs_artists['Artist Name(s)'] = songs_artists['Artist Name(s)'].str.strip()

# Count the occurrences of each artist
artist_counts = songs_artists['Artist Name(s)'].value_counts()

# Convert to a DataFrame
artist_counts_songs = artist_counts.reset_index()
artist_counts_songs.columns = ['Artist Name', 'Song Count']

print("\nArtist Statistics:\n", artist_counts_songs)


# Save to a new CSV file:
artist_counts_songs.to_csv(f'output/{folder}/artist_song_counts_{folder}.csv', index=False)

# Get the top 30 artists
top_artists = artist_counts.head(30)

# Create a DataFrame for the top artists
artist_counts_top30_songs = top_artists.reset_index()
artist_counts_top30_songs.columns = ['Artist Name', 'Song Count']

# Plot the top 30 artists
plt.figure(figsize=(12, 8))
plt.barh(artist_counts_top30_songs['Artist Name'], artist_counts_top30_songs['Song Count'], color='mediumseagreen')
plt.title('Top 30 Artists')
plt.xlabel('Song Count')
plt.ylabel('Artist Name')
plt.gca().invert_yaxis()  # Invert the y-axis to display the highest counts at the top

# Display the song counts above the bars
for index, value in enumerate(artist_counts_top30_songs['Song Count']):
    plt.text(value, index, str(value), va='center', ha='left', fontsize=10)

# Save the plot as a high-resolution PNG file
plt.tight_layout()
plt.savefig(f'output/{folder}/top_30_artists_{folder}.png', dpi=600, bbox_inches='tight')  # High-resolution PNG
plt.show()


#####################################################################
## Genre Counts
#####################################################################

songs['Genres'] = songs['Genres'].str.split(',')

songs_genres = songs.explode('Genres')

songs_genres['Genres'] = songs_genres['Genres'].str.strip()

genre_counts = songs_genres['Genres'].value_counts()

genre_counts_songs = genre_counts.reset_index()
genre_counts_songs.columns = ['Genre', 'Song Count']

print("\nGenre Statistics:\n", genre_counts_songs)

# Save to a new CSV file:
genre_counts_songs.to_csv(f'output/{folder}/genre_song_counts_{folder}.csv', index=False)


# Get the top 30 genres
top_genres = genre_counts.head(30)

# Create a DataFrame for the top genres
genre_counts_top30_songs = top_genres.reset_index()
genre_counts_top30_songs.columns = ['Genre', 'Song Count']

# Plot the top 30 genres
plt.figure(figsize=(12, 8))
plt.barh(genre_counts_top30_songs['Genre'], genre_counts_top30_songs['Song Count'], color='mediumseagreen')
plt.title('Top 30 Genres')
plt.xlabel('Song Count')
plt.ylabel('Genre')
plt.gca().invert_yaxis()  # Invert the y-axis to display the highest counts at the top

# Display the song counts above the bars
for index, value in enumerate(genre_counts_top30_songs['Song Count']):
    plt.text(value, index, str(value), va='center', ha='left', fontsize=10)

# Save the plot as a high-resolution PNG file
plt.tight_layout()
plt.savefig(f'output/{folder}/top_30_genres_{folder}.png', dpi=600, bbox_inches='tight')  # High-resolution PNG
plt.show()


#####################################################################
## Song Length Statistics
#####################################################################

# Convert 'Duration (ms)' to seconds for easier interpretation
songs['Duration (s)'] = songs['Duration (ms)'] / 1000

# Filter out songs with 0 seconds duration
songs = songs[songs['Duration (s)'] > 0]

# Helper function to format seconds as mm:ss
def format_mm_ss(seconds):
    minutes, seconds = divmod(int(seconds), 60)
    return f"{minutes}:{seconds:02}"

# Compute basic statistics
mean_length = songs['Duration (s)'].mean()
median_length = songs['Duration (s)'].median()
min_length = songs['Duration (s)'].min()
max_length = songs['Duration (s)'].max()
std_dev = songs['Duration (s)'].std()

# Find details of shortest and longest songs
shortest_song = songs[songs['Duration (s)'] == min_length].iloc[0]
longest_song = songs[songs['Duration (s)'] == max_length].iloc[0]

# Print the statistics with additional details in mm:ss
print("\nSong Length Statistics:\n")
print(f"Mean song length: {format_mm_ss(mean_length)} (mm:ss)")
print(f"Median song length: {format_mm_ss(median_length)} (mm:ss)")
print(f"Shortest song: '{shortest_song['Track Name']}' by {shortest_song['Artist Name(s)']} ({format_mm_ss(min_length)})")
print(f"Longest song: '{longest_song['Track Name']}' by {longest_song['Artist Name(s)']} ({format_mm_ss(max_length)})")
print(f"Standard deviation of song lengths: {std_dev:.2f} seconds")

# Visualize the distribution of song lengths
plt.figure(figsize=(10, 6))
plt.hist(songs['Duration (s)'], bins=144, color='skyblue', edgecolor='black', range=(0,720))
plt.title('How Long Are The Songs I Listen To?')
plt.xlabel('Song Duration (mm:ss)')
plt.ylabel('Frequency')
tick_positions = range(0, 721, 30)  # Set the positions of the ticks (every 30 seconds)
plt.xticks(tick_positions)  # Apply the new tick positions
# Format x-axis labels as mm:ss
plt.gca().set_xticklabels([format_mm_ss(tick) for tick in tick_positions])
# Adjust x-axis labels
plt.xticks(
    fontsize=7,                 # Smaller font size for readability
    rotation=0,                # Rotate slightly for better alignment
    ha='center'                 # Center-align labels with bars
)
# Add a red vertical line at the average song length (thinner line)
plt.axvline(mean_length, color='red', linestyle='--', linewidth=1, label=f'Mean: {format_mm_ss(mean_length)} (mm:ss)')
# Add an orange vertical line at the median song length
plt.axvline(median_length, color='orange', linestyle='--', linewidth=1, label=f'Median: {format_mm_ss(median_length)} (mm:ss)')
plt.legend()
plt.grid(axis='y')
plt.savefig(f'output/{folder}/song_length_distribution_{folder}.png', dpi=600, bbox_inches='tight')  # High-resolution PNG
plt.show()


#####################################################################
## Song Release Date
#####################################################################

# Convert 'Release Date' to datetime
songs['Release Date'] = pd.to_datetime(songs['Release Date'], errors='coerce')

# Extract the release year
songs['Release Year'] = songs['Release Date'].dt.year

# Drop rows where 'Release Year' is NaN (invalid or missing release dates)
songs = songs.dropna(subset=['Release Year'])

# Count songs by year
release_year_counts = songs['Release Year'].value_counts().sort_index()

print("\nSong Release Year Distribution:")
print(release_year_counts)

# Visualize the release year distribution with smaller x-axis labels
plt.figure(figsize=(12, 6))
bars = plt.bar(release_year_counts.index, release_year_counts.values, color='coral', edgecolor='black')
plt.title('My Spotify Library Song Release Year Distribution')
plt.xlabel('Year')
plt.ylabel('Number of Songs')

# Adjust x-axis labels
plt.xticks(
    release_year_counts.index,  # Align labels with the bars
    fontsize=7,                 # Smaller font size for readability
    rotation=-90,                # Rotate slightly for better alignment
    ha='center'                 # Center-align labels with bars
)

# Add the numbers above each bar, rotated -90 degrees
for bar in bars:
    yval = bar.get_height()
    plt.text(bar.get_x() + bar.get_width() / 2 - 0.2, yval + 1,  # Position the text above the bar
             str(int(yval)),  # Convert the height to an integer and display it as text
             ha='center',      # Horizontally center the text
             va='bottom',      # Vertically align the text at the bottom (above the bar)
             rotation=-90,     # Rotate the text by -90 degrees
             fontsize=7)       # Set font size for the labels
    
plt.grid(False)
plt.tight_layout()  # Ensure the labels fit within the figure

plt.savefig(f'output/{folder}/song_release_year_distribution_{folder}.png', dpi=600, bbox_inches='tight')  # High-resolution PNG
plt.show()


# Group by decade
songs['Decade'] = (songs['Release Year'] // 10) * 10
release_decade_counts = songs['Decade'].value_counts().sort_index()

print("\nSong Release Decade Distribution:")
print(release_decade_counts)

# Visualize the release decade distribution with x-axis labels
plt.figure(figsize=(10, 6))
bars_decade = plt.bar(release_decade_counts.index, release_decade_counts.values, color='coral', edgecolor='black', width=8)
plt.title('My Spotify Library Song Release Decade Distribution')
plt.xlabel('Decade')
plt.ylabel('Number of Songs')

# Adjust decade labels
plt.xticks(
    release_decade_counts.index,  # Align labels with the bars
    [f"{int(decade)}s" for decade in release_decade_counts.index],  # Decade labels
    fontsize=10                  # Font size for decades
)

# Add the numbers above each bar for the decade distribution
for bar in bars_decade:
    yval = bar.get_height()
    plt.text(bar.get_x() + bar.get_width() / 2, yval + 1,  # Position the text above the bar
             str(int(yval)),  # Convert the height to an integer and display it as text
             ha='center',      # Horizontally center the text
             va='bottom',      # Vertically align the text at the bottom (above the bar)
             rotation=0,     # Rotate the text by -90 degrees
             fontsize=10)      # Set font size for the labels

plt.grid(False)
plt.tight_layout()  # Ensure the labels fit within the figure

# Save the plot as a high-quality PNG file for the decade distribution
plt.savefig(f'output/{folder}/song_release_decade_distribution_{folder}.png', dpi=600, bbox_inches='tight')  # High-resolution PNG
plt.show()


#####################################################################
## Date Added
#####################################################################

# Ensure 'Date Added' is in datetime format
songs['Added At'] = pd.to_datetime(songs['Added At'])

# Filter out songs added on September 10, 2021 (when I imported all my old songs)
#songs = songs[songs['Added At'].dt.date != pd.to_datetime('2021-09-10').date()]

# Extract year and month from the 'Added At' column
songs['Year Added'] = songs['Added At'].dt.year
songs['Month Added'] = songs['Added At'].dt.month
songs['Day Added'] = songs['Added At'].dt.day

# Count the number of songs added per year, month, and day
year_counts = songs['Year Added'].value_counts().sort_index()
month_counts = songs['Month Added'].value_counts().sort_index()
day_counts = songs['Day Added'].value_counts().sort_index()

# Visualize the distribution of songs added per year
plt.figure(figsize=(12, 6))
plt.bar(year_counts.index, year_counts.values, color='mediumorchid', edgecolor='black')
plt.title('Distribution of Songs Added by Year')
plt.xlabel('Year')
plt.ylabel('Song Count')
plt.xticks(rotation=45)
for index, value in enumerate(year_counts.values):
    plt.text(year_counts.index[index], value, str(value), va='bottom', ha='center', fontsize=10)
plt.tight_layout()
plt.savefig(f'output/{folder}/songs_added_by_year_{folder}.png', dpi=600, bbox_inches='tight')  # Save high-resolution plot
plt.show()

# Visualize the distribution of songs added per month
plt.figure(figsize=(12, 6))
plt.bar(month_counts.index, month_counts.values, color='mediumorchid', edgecolor='black')
plt.title('Distribution of Songs Added by Month')
plt.xlabel('Month')
plt.ylabel('Song Count')
plt.xticks(month_counts.index, ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'])
for index, value in enumerate(month_counts.values):
    plt.text(month_counts.index[index], value, str(value), va='bottom', ha='center', fontsize=10)
plt.tight_layout()
plt.savefig(f'output/{folder}/songs_added_by_month_{folder}.png', dpi=600, bbox_inches='tight')  # Save high-resolution plot
plt.show()

#####################################################################
## Misc: Track Position
#####################################################################


#####################################################################
## Musical Properties
#####################################################################

# Define continuous and categorical musical properties
continuous_properties = [
    'Danceability', 'Energy', 'Loudness', 'Speechiness', 'Acousticness', 
    'Instrumentalness', 'Liveness', 'Valence', 'Tempo'
]
categorical_properties = ['Mode', 'Key', 'Time Signature']

# Mapping for Key and Mode
key_mapping = {
    0: 'C', 1: 'Db', 2: 'D', 3: 'Eb', 4: 'E', 5: 'F', 
    6: 'Gb', 7: 'G', 8: 'Ab', 9: 'A', 10: 'Bb', 11: 'B'
}
mode_mapping = {0: 'Minor', 1: 'Major'}

# Apply mappings
songs['Key'] = songs['Key'].map(key_mapping)
songs['Mode'] = songs['Mode'].map(mode_mapping)

### Continuous Properties Plot ###
fig_continuous, axes_continuous = plt.subplots(nrows=3, ncols=3, figsize=(15, 12))  # 3x3 grid for 9 properties
fig_continuous.suptitle('Distribution of Continuous Musical Properties', fontsize=16)
axes_continuous = axes_continuous.flatten()

# Loop over each continuous property, plot histogram and mean line
for i, property in enumerate(continuous_properties):
    ax = axes_continuous[i]
    data = songs[property].dropna()
    mean_value = data.mean()
    median_value = data.median()
    ax.hist(data, bins=30, color='#D32F2F', edgecolor='black', alpha=0.7)
    ax.axvline(mean_value, color='red', linestyle='--', linewidth=1.5, label=f'Mean: {mean_value:.2f}')
    ax.axvline(median_value, color='orange', linestyle='--', linewidth=1.5, label=f'Median: {median_value:.2f}')
    ax.set_title(f'{property}')
    ax.set_xlabel(property)
    ax.set_ylabel('Frequency')
    ax.legend(frameon=False)

# Hide any unused subplots
for j in range(i + 1, len(axes_continuous)):
    axes_continuous[j].axis('off')

plt.tight_layout(rect=[0, 0, 1, 0.96])
plt.savefig(f'output/{folder}/continuous_properties_distribution_{folder}.png', dpi=600, bbox_inches='tight')
plt.show()

### Categorical Properties Plot ###
fig_categorical, axes_categorical = plt.subplots(nrows=1, ncols=3, figsize=(18, 6))  # 1x3 grid for 3 properties
fig_categorical.suptitle('Distribution of Categorical Musical Properties', fontsize=16)

# Predefine the ordered categories for sorting
key_order = ['C', 'Db', 'D', 'Eb', 'E', 'F', 'Gb', 'G', 'Ab', 'A', 'Bb', 'B']
mode_order = ['Minor', 'Major']
time_signature_order = sorted(songs['Time Signature'].dropna().unique())  # Assuming numeric order for Time Signature

# Loop over each categorical property and plot as bar chart
for i, property in enumerate(categorical_properties):
    ax = axes_categorical[i]
    data = songs[property].dropna()
    
    # Sort data by the predefined order for each categorical property
    if property == 'Key':
        data = data.astype(pd.CategoricalDtype(categories=key_order, ordered=True))
    elif property == 'Mode':
        data = data.astype(pd.CategoricalDtype(categories=mode_order, ordered=True))
    elif property == 'Time Signature':
        data = data.astype(pd.CategoricalDtype(categories=time_signature_order, ordered=True))

    # Count and plot the values in the specified order
    counts = data.value_counts().reindex(data.cat.categories)
    counts.plot(kind='bar', ax=ax, color='#E57373', edgecolor='black', alpha=0.7)
    
    ax.set_title(f'{property}')
    ax.set_xlabel(property)
    ax.set_ylabel('Frequency')
    ax.set_xticklabels(counts.index, rotation=0, ha='center')

plt.tight_layout(rect=[0, 0, 1, 0.96])
plt.savefig(f'output/{folder}/categorical_properties_distribution_{folder}.png', dpi=600, bbox_inches='tight')
plt.show()


#####################################################################
## TODO Time Analysis - how do these things above change over time??
#####################################################################