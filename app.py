import streamlit as st
import pandas as pd
import plotly.express as px

# Load data
uploaded_file = st.file_uploader("Upload Client Purchases Data", type="xlsx")
if uploaded_file:
    # Read the uploaded file
    df = pd.read_excel(uploaded_file)

    # Filter clients who purchased only one category
    single_category_clients = df[df['Product_Categories_Purchased_Count'] == 1].copy()

    # Identify which single category each client bought
    categories = [
        'Product Category_Boissons', 'Product Category_Boucherie', 'Product Category_Charcuterie',
        'Product Category_Consommables', 'Product Category_Crémerie', 'Product Category_Emballages',
        'Product Category_Epicerie salée', 'Product Category_Epicerie sucrée',
        'Product Category_Fruits et Légumes', 'Product Category_Marée',
        'Product Category_Produits Préparés'
    ]
    
    # Add a column to label the purchased category for each client
    def get_single_category(row):
        for category in categories:
            if row[category] == 1:
                return category.replace('Product Category_', '')

    single_category_clients['Single_Category'] = single_category_clients.apply(get_single_category, axis=1)

    # Group data by Postal code, Pays, and Region for heatmap
    category_counts = single_category_clients.groupby(['Postal code', 'Pays', 'region', 'Single_Category']).size().reset_index(name='Count')

    # Select a region and category for specific analysis
    selected_pays = st.selectbox("Select Country (Pays):", category_counts['Pays'].unique())
    selected_category = st.selectbox("Select Product Category:", category_counts['Single_Category'].unique())
    
    filtered_data = category_counts[(category_counts['Pays'] == selected_pays) & 
                                    (category_counts['Single_Category'] == selected_category)]

    # Plot heatmap using Postal codes and client count
    st.subheader(f"Heatmap of Clients Buying Only '{selected_category}' in {selected_pays}")
    fig = px.density_mapbox(
        filtered_data,
        lat="Postal code",  # Placeholder, assumes postal code or needs geo-coordinates
        lon="Postal code",
        z="Count",
        radius=10,
        center=dict(lat=50, lon=2),  # Center adjusted based on country, adjust for real lat/lon
        mapbox_style="carto-positron",
        title=f"Client Density by Postal Code for {selected_category} in {selected_pays}"
    )

    st.plotly_chart(fig)
