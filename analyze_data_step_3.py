import matplotlib.pyplot as plt

def analysis(df_liste):
    plt.rcParams['font.sans-serif'] = ["DejaVu Sans"] #gives turkish character support

    plt.figure(figsize=(12, 6))
    df_liste["Company"].value_counts().head(10).plot(kind='bar')
    plt.title("Top 10 Companies with the Most Internship Posts")
    plt.ylabel("Post Count")
    plt.xticks(rotation=45, ha='right')
    plt.show()

    plt.figure(figsize=(10, 6))
    df_temp = df_liste[df_liste["Department"] != "NotFound"]  #not putting the not found ones to chart
    df_temp["Department"].value_counts().plot(kind='pie', autopct='%1.1f%%', startangle=90, cmap='Set2')
    plt.title("Post Percentages Regarding Departments of Internship Posts")
    plt.ylabel('')
    plt.show()

    all_locations = df_liste["Location"].str.split(',').explode().str.strip()
    excluded_locations = ['Hibrit', 'Ofisten']
    all_locations = all_locations[~all_locations.isin(excluded_locations)] #take the locations other than the excluded ones
    plt.figure(figsize=(10, 6))
    all_locations.value_counts().head(10).plot(kind='bar', color='skyblue')
    plt.title("Top 10 Locations Of Internship Posts")
    plt.ylabel("Post Count")
    plt.xticks(rotation=45, ha='right')
    plt.show()