import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Load data
@st.cache
def load_data():
    day_df = pd.read_csv('day.csv')  # Adjust the file path as needed
    return day_df

day_df = load_data()

# Sidebar
st.sidebar.title("Bike Sharing Data Analysis")
options = st.sidebar.radio("Choose a Section", ["Overview", "User Behavior", "Weather Impact", "Yearly Performance", "Advanced Analysis"])

# Overview Section
if options == "Overview":
    st.title("Bike Sharing System Overview")
    st.write("Dashboard ini menyediakan insight terhadap 'Bike Sharing' system data, berfokus pada perilaku user, pengaruh cuaca, dan performa tahunan perusahaan.")
    st.write(day_df.head())

# User Behavior Section
elif options == "User Behavior":
    st.title("Analysis Perilaku User")
    
    #User rental data
    user_rentals = day_df[['dteday', 'casual', 'registered', 'cnt']].copy()
    
    # Plot
    plt.figure(figsize=(10, 6))
    plt.plot(user_rentals['dteday'], user_rentals['casual'], label='Casual Users', color='orange')
    plt.plot(user_rentals['dteday'], user_rentals['registered'], label='Registered Users', color='blue')
    plt.xlabel('Date')
    plt.ylabel('Number of Rentals')
    plt.title('Bike Rentals by User Type')
    plt.legend()
    st.pyplot(plt)

    # Insights
    st.subheader("Insight:")
    st.write("- Registered users tentunya berjumlah lebih banyak dari Casual users.")
    st.write("- Registered users memiliki pola sewa yang lebih stabil, hal ini menunjukan kemungkinan kebutuhan perjalanan reguler atau perjalanan sehari-hari.")

# Weather Impact Section
elif options == "Weather Impact":
    st.title("Pengaruh Cuaca terhadap Sewa Sepeda")
    
    # Weather rental data
    weather_rentals = day_df.groupby('weathersit').agg({'cnt': 'sum'}).reset_index()

    # Plot
    plt.figure(figsize=(8, 5))
    sns.barplot(x='weathersit', y='cnt', data=weather_rentals, palette='coolwarm')
    
    # Menambahkan judul dan keterangan
    plt.xlabel('Weather Condition')
    plt.ylabel('Total Rentals')
    plt.title('Total Bike Rentals by Weather Condition')
    plt.xticks([0, 1, 2, 3], ['Clear', 'Mist/Cloudy', 'Light Snow/Rain', 'Heavy Rain/Snow'])
    st.pyplot(plt)

    # Insights
    st.subheader("Insight:")
    st.write("- Ketika cuaca 'Clear' atau cerah, pengguna rental sepeda terbanyak dibandingkan dengan keadaan cuaca yang lain.")
    st.write("- Terilhat bahwa ketika cuaca hujan besar atau bersalju lebat tidak ada satupun user yang merental sepeda.")

# Yearly Performance Section
elif options == "Yearly Performance":
    st.title("Performa Tahunan Perusahaan")
    
    # Grouping data berdasarkan tahun
    year_rentals = day_df.groupby('yr').agg({
        'casual': 'sum',
        'registered': 'sum',
        'cnt': 'sum'
    }).reset_index()
    
    # Merubah nama indeks tahun
    year_rentals['yr'] = year_rentals['yr'].replace({0: '2011', 1: '2012'})
    
    
    year_rentals_melted = year_rentals.melt(id_vars='yr', value_vars=['casual', 'registered', 'cnt'], 
                                             var_name='User Type', value_name='Rentals')
    
    # Plot
    plt.figure(figsize=(10, 6))
    sns.barplot(x='yr', y='Rentals', hue='User Type', data=year_rentals_melted, palette='Set2')
    plt.xlabel('Year')
    plt.ylabel('Total Rentals')
    plt.title('Bike Rentals by User Type and Year')
    plt.legend(title='User Type')
    st.pyplot(plt)

    # Insights
    st.subheader("Insight:")
    st.write("- Terlihat bahwa dari tahun 2011 ke tahun 2012 terjadi kenaikan yang signifikan baik pada casual maupun registered users ataupun secara akumulasi (total rental) yaitu pada variable 'cnt'.")
    st.write("- Registered users memiliki jumlah sewa yang lebih banyak dibandingkan dengan casual users. Hal ini menunjukkan bahwa 'Bike Sharing' mungkin telah berhasil mengubah lebih banyak users menjadi registered users dari tahun 2011 hingga 2012.")
    st.write("- Terlihat bahwa ketika cuaca hujan besar atau bersalju lebat, tidak ada satupun user yang merental sepeda.")

# Advanced Analysis Section
elif options == "Advanced Analysis":
    st.title("Analisis Lanjutan: Box Plot Rental Berdasarkan Cuaca")
    
    # Plot
    plt.figure(figsize=(8, 6))
    sns.boxplot(x='weathersit', y='cnt', data=day_df, palette='coolwarm')
    
    # Menambahkan judul dan keterangan
    plt.xlabel('Weather Condition (1: Clear, 2: Mist/Cloudy, 3: Light Snow/Rain, 4: Heavy Rain/Snow)')
    plt.ylabel('Total Bike Rentals (cnt)')
    plt.title('Box Plot: Total Bike Rentals by Weather Condition')
    plt.xticks([0, 1, 2, 3], ['Clear', 'Mist/Cloudy', 'Light Snow/Rain', 'Heavy Rain/Snow'])
    st.pyplot(plt)

    # Insights
    st.subheader("Insight:")
    st.write("- Jumlah rata-rata sewa sepeda jauh lebih tinggi pada cuaca cerah atau berawan parsial/sebagian. Secara statistik, hal ini menunjukkan bahwa cuaca cerah merupakan indikator kuat dalam memprediksi peningkatan penyewaan sepeda.")
    st.write("- Interquartile range (IQR) untuk cuaca buruk menunjukkan rendahnya variability dalam sewa, hal ini menunjukkan bahwa cuaca buruk menjadi penentu apakah users akan menyewa sepeda atau tidak.")
    st.write("- Terdapat outlier pada hari-hari cuaca cerah, yang berarti terjadinya 'special event' di mana jumlah sewa jauh di atas normal.")

# Run Streamlit
if __name__ == "__main__":
    st.write("Dashboard is running.")
