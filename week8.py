# question 2a how to handle missing values
# 1. Decide how to handle missing values
# Example: Fill missing 'journal' values with 'Unknown'
df['journal'] = df['journal'].fillna('Unknown')

# Example: Drop rows where 'publish_time' is missing, as it's crucial for time analysis
df = df.dropna(subset=['publish_time'])

# Example: Fill missing 'abstract' with an empty string or 'No Abstract' 
# if you plan to use it for a word count feature.
df['abstract'] = df['abstract'].fillna('')

# question 2b prepare data for analysis
import pandas as pd

# Convert to datetime format
df['publish_time'] = pd.to_datetime(df['publish_time'], errors='coerce')

# Drop any rows that failed to convert ('NaT')
df = df.dropna(subset=['publish_time'])

# Extract the year for time-based analysis
df['year'] = df['publish_time'].dt.year

# Create a new column: Abstract Word Count
df['abstract_word_count'] = df['abstract'].apply(lambda x: len(str(x).split()))

#question 3 basic analysis 
# 1. Count papers by publication year
year_counts = df['year'].value_counts().sort_index()

# 2. Identify top journals
top_journals = df['journal'].value_counts().head(10)

# 3. Find most frequent words in titles
# You would need to write a function for this, but the core data is:
# df['title'].str.lower().str.split(expand=True).stack().value_counts().head(20)

#3b  how to create visualization
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud # You may need to pip install wordcloud

# 1. Plot number of publications over time (Bar Chart)
plt.figure(figsize=(10, 6))
sns.barplot(x=year_counts.index, y=year_counts.values)
plt.title('Publications by Year')
plt.xlabel('Publication Year')
plt.ylabel('Number of Papers')
plt.show()

# 2. Bar chart of top publishing journals
plt.figure(figsize=(12, 6))
sns.barplot(x=top_journals.values, y=top_journals.index)
plt.title('Top 10 Publishing Journals')
plt.xlabel('Number of Papers')
plt.ylabel('Journal')
plt.show()

# 3. Generate a word cloud of paper titles (Requires text cleaning and word frequency)
# Combine all titles into one string
titles_text = " ".join(df['title'].astype(str).tolist())
wordcloud = WordCloud(width=800, height=400, background_color='white').generate(titles_text)
plt.figure(figsize=(10, 5))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis('off')
plt.show()

# 4. streamlit application
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
# (Import all your other necessary libraries: wordcloud, numpy, etc.)

# --- Configuration and Data Loading ---
st.set_page_config(layout="wide")

# Use st.cache_data to load the data only once!
@st.cache_data
def load_and_clean_data(file_path):
    df = pd.read_csv(file_path)
    # Perform all your cleaning and preparation from Part 2 here
    df = df.dropna(subset=['publish_time'])
    df['publish_time'] = pd.to_datetime(df['publish_time'], errors='coerce')
    df['year'] = df['publish_time'].dt.year
    # ... more cleaning ...
    return df

df = load_and_clean_data('metadata.csv')

# --- App Layout and Title ---
st.title("CORD-19 Data Explorer")
st.write("Simple analysis and visualization of COVID-19 research papers.")

# --- Interactive Widgets (Sidebar) ---
st.sidebar.header("Filter Options")

# 1. Slider for year range
min_year = int(df['year'].min())
max_year = int(df['year'].max())
year_range = st.sidebar.slider(
    'Select Publication Year Range',
    min_value=min_year, max_value=max_year, value=(min_year, max_year)
)

# 2. Filter the data based on the slider
filtered_df = df[
    (df['year'] >= year_range[0]) & 
    (df['year'] <= year_range[1])
]

st.subheader(f"Data for Years {year_range[0]} - {year_range[1]}")

# --- Display Visualizations ---
# Example: Publications by Year Plot
st.subheader("1. Publications Over Time")
# Re-calculate counts on filtered data
year_counts = filtered_df['year'].value_counts().sort_index()

# Use st.pyplot() to display matplotlib figures
fig, ax = plt.subplots(figsize=(10, 5))
sns.barplot(x=year_counts.index, y=year_counts.values, ax=ax)
ax.set_title('Publications by Year')
st.pyplot(fig) # This displays the plot in Streamlit

# --- Show a sample of the data ---
st.subheader("Sample Data")
st.dataframe(filtered_df[['title', 'journal', 'year', 'abstract_word_count']].head(10))

