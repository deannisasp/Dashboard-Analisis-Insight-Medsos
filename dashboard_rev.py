import streamlit as st
import pandas as pd
import plotly.express as px

def load_data_from_url(url):
    try:
        # Ekstrak file ID dari URL Google Drive
        file_id = url.split('/')[-2]
        download_url = f'https://drive.google.com/uc?id={file_id}'
        
        # Membaca file Excel
        df = pd.read_excel(download_url)
        return df
    except Exception as e:
        st.error(f"Kesalahan memuat data: {e}")
        return None

def main():
    st.header("📊 Dashboard Analisis Media Sosial", divider='rainbow')
    
    # Tab untuk berbagai platform
tab1, tab2 = st.tabs(["Analisis dari Google Drive", "Unggah File Sendiri"])

with tab1:
    st.header("Analisis Data dari Google Drive")
    
    # Input URL untuk Instagram
    url_instagram = st.text_input("Masukkan URL Google Drive untuk Data Instagram:")
    
    # Input URL untuk TikTok
    url_tiktok = st.text_input("Masukkan URL Google Drive untuk Data TikTok:")
    
    # Tombol untuk memuat data
    if st.button("Muat Data"):
        # Memuat data Instagram
        if url_instagram:
            df_ig = load_data_from_url(url_instagram)
            if df_ig is not None:
                # Proses data Instagram
                df_ig['Tanggal Upload'] = pd.to_datetime(df_ig['Tanggal Upload'], errors='coerce')
                df_ig['Engagement Rate (%)'] = (df_ig['Engagement'] / df_ig['Reach']) * 100
                df_ig['Reach Rate (%)'] = (df_ig['Reach'] / 3086) * 100
                st.success("Data Instagram berhasil dimuat!")
                
                # Simpan data Instagram di session state
                st.session_state.df_ig = df_ig
        
        # Memuat data TikTok
        if url_tiktok:
            df_tiktok = load_data_from_url(url_tiktok)
            if df_tiktok is not None:
                # Proses data TikTok
                df_tiktok['Tanggal Upload'] = pd.to_datetime(df_tiktok['Tanggal Upload'], errors='coerce')
                df_tiktok['Engagement'] = df_tiktok[['Like', 'Share', 'Comment', 'Save']].sum(axis=1)
                df_tiktok['Engagement Rate (%)'] = (df_tiktok['Engagement'] / df_tiktok['Reach']) * 100
                df_tiktok['Reach Rate (%)'] = (df_ig['Reach'] / 2341) * 100
                
                # Menjumlahkan nilai berdasarkan kategori
                upload_tiktok = df_tiktok.groupby('Type')['Jumlah Konten'].sum().reindex(['Photo Slide', 'Video'], fill_value=0).reset_index()
                upload_tiktok.columns = ['Jenis Konten', 'Jumlah Konten']

                # Mengelompokkan data berdasarkan nama bulan dan jenis konten
                upload_bulanan_tiktok = (
                    df_tiktok.groupby([df_tiktok['Tanggal Upload'].dt.month_name(), 'Type'])['Jumlah Konten']
                    .sum()
                    .unstack(fill_value=0)
                    .reindex(columns=['Photo Slide', 'Video'], fill_value=0)
                    .reset_index()
                )

                # Urutkan berdasarkan bulan dalam urutan kalender
                bulan_mapping = {bulan: i for i, bulan in enumerate(
                    ['January', 'February', 'March', 'April', 'May', 'June',
                    'July', 'August', 'September', 'October', 'November', 'December'], 1)}

                upload_bulanan_tiktok['Index'] = upload_bulanan_tiktok['Tanggal Upload'].map(bulan_mapping)
                upload_bulanan_tiktok = upload_bulanan_tiktok.sort_values('Index').drop(columns=['Index']).reset_index(drop=True)

                # Mengubah nama kolom
                upload_bulanan_tiktok = upload_bulanan_tiktok.rename(columns={'Tanggal Upload': 'Bulan'})
                
                st.success("Data TikTok berhasil dimuat!")
                
                # Simpan data TikTok di session state
                st.session_state.df_tiktok = df_tiktok
                st.session_state.upload_bulanan_tiktok = upload_bulanan_tiktok


with tab2:
    st.header("Unggah File untuk Analisis")
    
    # Upload file Instagram
    uploaded_instagram = st.file_uploader("Unggah File Excel Instagram", type=['xlsx', 'xls'])
    
    # Upload file TikTok
    uploaded_tiktok = st.file_uploader("Unggah File Excel TikTok", type=['xlsx', 'xls'])
    
    # Tombol untuk memproses file yang diunggah
    if st.button("Proses File"):
        # Memproses data Instagram
        if uploaded_instagram is not None:
            try:
                df_ig = pd.read_excel(uploaded_instagram)
                df_ig['Tanggal Upload'] = pd.to_datetime(df_ig['Tanggal Upload'], errors='coerce')
                df_ig['Engagement Rate (%)'] = (df_ig['Engagement'] / df_ig['Reach']) * 100
                df_ig['Reach Rate (%)'] = (df_ig['Reach'] / 3086) * 100
                st.success("Data Instagram berhasil diproses!")
                
                # Simpan data Instagram di session state
                st.session_state.df_ig = df_ig
            except Exception as e:
                st.error(f"Kesalahan memproses file Instagram: {e}")
        
        # Memproses data TikTok
        if uploaded_tiktok is not None:
            try:
                df_tiktok = pd.read_excel(uploaded_tiktok)
                df_tiktok['Tanggal Upload'] = pd.to_datetime(df_tiktok['Tanggal Upload'], errors='coerce')
                df_tiktok['Engagement'] = df_tiktok[['Like', 'Share', 'Comment', 'Save']].sum(axis=1)
                df_tiktok['Engagement Rate (%)'] = (df_tiktok['Engagement'] / df_tiktok['Reach']) * 100
                df_tiktok['Reach Rate (%)'] = (df_ig['Reach'] / 2341) * 100
                # Menjumlahkan nilai berdasarkan kategori
                upload_tiktok = df_tiktok.groupby('Type')['Jumlah Konten'].sum().reindex(['Photo Slide', 'Video'], fill_value=0).reset_index()
                upload_tiktok.columns = ['Jenis Konten', 'Jumlah Konten']

                # Mengelompokkan data berdasarkan nama bulan dan jenis konten
                upload_bulanan_tiktok = (
                    df_tiktok.groupby([df_tiktok['Tanggal Upload'].dt.month_name(), 'Type'])['Jumlah Konten']
                    .sum()
                    .unstack(fill_value=0)
                    .reindex(columns=['Photo Slide', 'Video'], fill_value=0)
                    .reset_index()
                )

                # Urutkan berdasarkan bulan dalam urutan kalender
                bulan_mapping = {bulan: i for i, bulan in enumerate(
                    ['January', 'February', 'March', 'April', 'May', 'June',
                    'July', 'August', 'September', 'October', 'November', 'December'], 1)}

                upload_bulanan_tiktok['Index'] = upload_bulanan_tiktok['Tanggal Upload'].map(bulan_mapping)
                upload_bulanan_tiktok = upload_bulanan_tiktok.sort_values('Index').drop(columns=['Index']).reset_index(drop=True)

                # Mengubah nama kolom
                upload_bulanan_tiktok = upload_bulanan_tiktok.rename(columns={'Tanggal Upload': 'Bulan'})
                st.success("Data TikTok berhasil diproses!")
                
                # Simpan data TikTok di session state
                st.session_state.df_tiktok = df_tiktok
                st.session_state.upload_bulanan_tiktok = upload_bulanan_tiktok
            except Exception as e:
                st.error(f"Kesalahan memproses file TikTok: {e}")

# Cek apakah data sudah dimuat
if 'df_ig' in st.session_state and 'df_tiktok' in st.session_state:
    # Sidebar untuk memilih platform
    platform = st.sidebar.selectbox(
        "Pilih platform untuk dianalisis:", 
        ["Instagram", "TikTok"],
        key='platform_select'  # Tambahkan key untuk menjaga state
    )
    
    # Simpan platform di session state
    st.session_state.platform = platform
    
    # Pilih menu sesuai platform
    menu = st.sidebar.radio("Pilih Menu", ["Data Awal", "Analisis Performa", "Analisis Bulanan", "Informasi Dataset"])

    # Gunakan kondisi dengan st.session_state.platform
    if st.session_state.platform == "Instagram":
        df_ig = st.session_state.df_ig

        st.title("📊Dashboard Analisis Performa Instagram")
        
        if menu == "Data Awal":
            st.header("Tampilan Data Awal")
            st.write("Dataset Instagram:")
            st.write(df_ig)

        elif menu == "Analisis Performa":
            st.header("Analisis Performa Instagram")
            # Halaman Analisis Performa
            # Analisis Berdasarkan Jenis Konten
            st.write("Analisis Berdasarkan Jenis Konten:")
            jenis_konten_analysis = df_ig.groupby('Jenis Konten').agg({
                'Reach': 'mean',
                'Engagement': 'mean',
                'Engagement Rate (%)': 'mean',
                'Reach Rate (%)' : 'mean'
            }).reset_index()

            jenis_konten_analysis.columns = [
                'Jenis Konten',
                'Average Reach',
                'Average Engagement',
                'Average Engagement Rate',
                'Average Reach Rate (%)
            ]

            jenis_konten_analysis = jenis_konten_analysis.sort_values(by='Average Engagement Rate', ascending=False)

            # Tampilkan data dalam tabel
            st.write(jenis_konten_analysis)

            # Visualisasi menggunakan Plotly
            st.write("Visualisasi Rata-rata Engagement Rate Berdasarkan Jenis Konten:")
            fig = px.bar(
                jenis_konten_analysis,
                x='Average Engagement Rate',
                y='Jenis Konten',
                orientation='h',
                color='Average Engagement Rate',
                color_continuous_scale='Blues',
                labels={'Average Engagement Rate': 'Average Engagement Rate (%)'},
                title="Rata-rata Engagement Rate Berdasarkan Jenis Konten"
            )
            fig.update_layout(
                xaxis_title='Average Engagement Rate (%)',
                yaxis_title='Jenis Konten',
                coloraxis_showscale=True
            )
            st.plotly_chart(fig)

            # Analisis Berdasarkan Topik
            st.write("Analisis Berdasarkan Topik:")
            topik_performance = df_ig.groupby('Topik').agg({
                'Reach': 'mean',
                'Engagement Rate (%)': 'mean',
                'Judul Konten': 'count'  # Jumlah konten per topik
            }).rename(columns={'Judul Konten': 'Jumlah Konten'}).reset_index()

            topik_performance = topik_performance.sort_values(by='Reach', ascending=False)

            # Tampilkan data dalam tabel
            st.write(topik_performance)

            # Visualisasi scatter plot menggunakan Plotly
            st.write("Visualisasi Rata-rata Reach dan Engagement Rate Berdasarkan Topik:")
            fig_topik = px.scatter(
                topik_performance,
                x='Reach',
                y='Engagement Rate (%)',
                size='Jumlah Konten',
                color='Topik',
                hover_name='Topik',
                size_max=60,
                labels={'Reach': 'Rata-rata Reach', 'Engagement Rate (%)': 'Rata-rata Engagement Rate (%)'},
                title="Rata-rata Reach dan Engagement Rate Berdasarkan Topik"
            )
            fig_topik.update_layout(
                xaxis_title='Rata-rata Reach',
                yaxis_title='Rata-rata Engagement Rate (%)'
            )
            st.plotly_chart(fig_topik)

            # Menghitung distribusi demografi berdasarkan lokasi
            demografi_lokasi = df_ig[['East Java', 'West Java', 'Central Java', 'Bali Nusra', 'Others']].sum()
            demografi_lokasi = demografi_lokasi.sort_values(ascending=False).reset_index()
            demografi_lokasi.columns = ['Lokasi', 'Jumlah (%)']

            # Menampilkan tabel distribusi
            st.write(demografi_lokasi)

            # Diagram Lingkaran
            st.write("### Distribusi Demografi Berdasarkan Lokasi")
            fig = px.pie(
                demografi_lokasi,
                names='Lokasi',
                values='Jumlah (%)',
                title='Distribusi Demografi Berdasarkan Lokasi',
                #hole=0.4,  # Membuat pie chart menjadi donut chart
                color_discrete_sequence=px.colors.sequential.RdBu
            )

            # Menampilkan diagram lingkaran
            st.plotly_chart(fig)

            # Target Market berdasarkan Usia
            st.write("Target Market Berdasarkan Usia:")
            # Menghitung total jumlah berdasarkan usia
            demografi_usia = df_ig[['18-24', '25-34', '35-44', 'Others Age']].sum().reset_index()
            demografi_usia.columns = ['Usia', 'Jumlah (%)']
            st.write(demografi_usia)

            # Distribusi Demografi Berdasarkan Usia
            st.write("Distribusi Demografi Berdasarkan Usia:")
            demografi_usia = df_ig[['18-24', '25-34', '35-44', 'Others Age']].sum()
            demografi_usia = demografi_usia.sort_values(ascending=False).reset_index()
            demografi_usia.columns = ['Usia', 'Jumlah']

            # Visualisasi bar chart
            fig_usia = px.bar(
                demografi_usia,
                x='Jumlah',
                y='Usia',
                orientation='h',
                color='Usia',
                title="Distribusi Demografi Berdasarkan Usia"
            )
            st.plotly_chart(fig_usia)

            # Target Market berdasarkan Gender
            st.write("Target Market Berdasarkan Gender:")
            demografi_gender = df_ig[['Woman', 'Men', 'Others Gender']].sum().reset_index()
            demografi_gender.columns = ['Gender', 'Jumlah (%)']
            st.write(demografi_gender)

            # Distribusi Demografi Berdasarkan Gender
            st.write("Distribusi Demografi Berdasarkan Gender:")
            demografi_gender = df_ig[['Woman', 'Men', 'Others Gender']].sum()
            demografi_gender = demografi_gender.sort_values(ascending=False).reset_index()
            demografi_gender.columns = ['Gender', 'Jumlah']

            # Visualisasi donut chart
            fig_gender = px.pie(
                demografi_gender,
                names='Gender',
                values='Jumlah',
                hole=0.4,  # Membuat chart berbentuk donut
                title="Distribusi Demografi Berdasarkan Gender"
            )
            st.plotly_chart(fig_gender)

            # Memisahkan data berdasarkan 'Note'
            routine_data = df_ig[df_ig['Note'] == 'Routine']
            ad_data = df_ig[df_ig['Note'] == 'Ad']

            # Menghitung rata-rata metrik kinerja untuk masing-masing kategori
            routine_metrics = routine_data[['Reach', 'Engagement', 'Engagement Rate (%)', 'Plays', 'Like', 'Share', 'Comment', 'Save', 'Follows']].mean()
            ad_metrics = ad_data[['Reach', 'Engagement', 'Engagement Rate (%)', 'Plays', 'Like', 'Share', 'Comment', 'Save', 'Follows']].mean()

            # Menggabungkan hasil ke dalam satu DataFrame untuk perbandingan
            comparison = pd.DataFrame({
                'Routine': routine_metrics,
                'Ad': ad_metrics
            })

            # Tambahkan kolom selisih untuk mempermudah analisis
            comparison['Difference'] = comparison['Ad'] - comparison['Routine']
            comparison['Difference (%)'] = (comparison['Difference'] / comparison['Routine']) * 100

            # Menampilkan tabel perbandingan
            st.write("Perbandingan Performan Konten Routine dan Ad:")
            st.write(comparison)

            # Visualisasi perbandingan metrik kinerja antara Routine dan Ad menggunakan bar chart
            st.write("Visualisasi Perbandingan Metrik Kinerja antara Routine dan Ad:")

            fig_comparison = px.bar(
                comparison,
                x=comparison.index,
                y=['Routine', 'Ad'],
                labels={'value': 'Nilai Metrik', 'variable': 'Kategori'},
                title="Perbandingan Metrik Kinerja antara Routine dan Ad"
            )

            fig_comparison.update_layout(
                barmode='group',
                xaxis_title='Metrik',
                yaxis_title='Nilai Metrik'
            )

            # Tampilkan grafik
            st.plotly_chart(fig_comparison)

            # Membuat heatmap dari perbedaan (selisih) antara Routine dan Ad
            st.write("Heatmap Perbandingan Selisih Metrik Kinerja antara Routine dan Ad:")

            # Menyusun data selisih menjadi format yang sesuai untuk heatmap
            heatmap_data = comparison[['Difference', 'Difference (%)']].transpose()

            # Membuat heatmap
            fig_heatmap = px.imshow(
                heatmap_data,
                labels={'x': 'Metrik', 'y': 'Perbandingan', 'color': 'Selisih'},
                title="Heatmap Perbandingan Selisih Metrik Kinerja antara Routine dan Ad",
                color_continuous_scale='RdBu',  # Skema warna yang cocok untuk selisih
                aspect="auto"
            )

            # Menampilkan heatmap
            st.plotly_chart(fig_heatmap)

            # Filter konten dengan kata 'giveaway' di kolom Judul Konten
            giveaway_data = df_ig[df_ig['Judul Konten'].str.contains('giveaway', case=False, na=False)]

            # Rata-rata performa konten giveaway
            giveaway_metrics = giveaway_data[['Reach', 'Engagement', 'Engagement Rate (%)', 'Follows', 'External Link Taps', 'Profile Visits']].mean()

            # Rata-rata performa konten non-giveaway
            non_giveaway_data = df_ig[~df_ig['Judul Konten'].str.contains('giveaway', case=False, na=False)]
            non_giveaway_metrics = non_giveaway_data[['Reach', 'Engagement', 'Engagement Rate (%)', 'Follows', 'External Link Taps', 'Profile Visits']].mean()

            # Membandingkan performa konten giveaway vs non-giveaway
            comparison_giveaway = pd.DataFrame({
                'Giveaway': giveaway_metrics,
                'Non-Giveaway': non_giveaway_metrics
            })

            # Tambahkan kolom selisih
            comparison_giveaway['Difference'] = (comparison_giveaway['Giveaway'] - comparison_giveaway['Non-Giveaway'])

            # Tambahkan kolom selisih dalam persen
            comparison_giveaway['Difference (%)'] = (comparison_giveaway['Difference'] / comparison_giveaway['Non-Giveaway']) * 100

            # Menampilkan perbandingan performa konten Giveaway vs Non-Giveaway
            st.write("Perbandingan Performan Konten Giveaway vs Non-Giveaway:")
            st.write(comparison_giveaway)

            # Visualisasi perbandingan metrik kinerja antara Giveaway dan Non-Giveaway menggunakan bar chart
            st.write("Visualisasi Perbandingan Metrik Kinerja antara Giveaway dan Non-Giveaway:")

            fig_comparison_giveaway = px.bar(
                comparison_giveaway,
                x=comparison_giveaway.index,
                y=['Giveaway', 'Non-Giveaway'],
                labels={'value': 'Nilai Metrik', 'variable': 'Kategori'},
                title="Perbandingan Metrik Kinerja antara Giveaway dan Non-Giveaway"
            )

            fig_comparison_giveaway.update_layout(
                barmode='group',
                xaxis_title='Metrik',
                yaxis_title='Nilai Metrik'
            )

            # Tampilkan grafik
            st.plotly_chart(fig_comparison_giveaway)

            # Membuat heatmap dari selisih antara Giveaway dan Non-Giveaway
            st.write("Heatmap Perbandingan Selisih Metrik Kinerja antara Giveaway dan Non-Giveaway:")

            # Menyusun data selisih menjadi format yang sesuai untuk heatmap
            heatmap_data_giveaway = comparison_giveaway[['Difference', 'Difference (%)']].transpose()

            # Membuat heatmap
            fig_heatmap_giveaway = px.imshow(
                heatmap_data_giveaway,
                labels={'x': 'Metrik', 'y': 'Perbandingan', 'color': 'Selisih'},
                title="Heatmap Perbandingan Selisih Metrik Kinerja antara Giveaway dan Non-Giveaway",
                color_continuous_scale='RdBu',  # Skema warna yang cocok untuk selisih
                aspect="auto"
            )

            # Menampilkan heatmap
            st.plotly_chart(fig_heatmap_giveaway)

            # Filter data dengan kata 'giveaway' di kolom Judul Konten
            giveaway_data = df_ig[df_ig['Judul Konten'].str.contains('giveaway', case=False, na=False)]

            # Menghitung total interaksi untuk konten giveaway
            total_interaksi = (giveaway_data['Like'].sum() +
                            giveaway_data['Share'].sum() +
                            giveaway_data['Comment'].sum() +
                            giveaway_data['Save'].sum())

            # Menghitung total reach konten giveaway
            total_reach_giveaway = giveaway_data['Reach'].sum()

            # Misalkan jumlah followers diketahui
            jumlah_followers = 3050  # Total pengikut dari semua data
            persentase_tahu = (total_reach_giveaway / jumlah_followers) * 100

            # Menampilkan hasil perhitungan
            st.write("Hasil Perhitungan Giveaway:")
            st.write(f"Total Interaksi pada Giveaway: {total_interaksi}")
            st.write(f"Total Reach Konten Giveaway: {total_reach_giveaway}")
            st.write(f"Persentase orang yang tahu tentang giveaway: {persentase_tahu:.2f}%")

            # Visualisasi Total Interaksi
            st.write("Visualisasi Total Interaksi Konten Giveaway:")
            fig_interaksi = px.bar(
                x=['Like', 'Share', 'Comment', 'Save'],
                y=[giveaway_data['Like'].sum(), giveaway_data['Share'].sum(), giveaway_data['Comment'].sum(), giveaway_data['Save'].sum()],
                labels={'x': 'Tipe Interaksi', 'y': 'Jumlah Interaksi'},
                title="Distribusi Interaksi pada Konten Giveaway"
            )
            st.plotly_chart(fig_interaksi)

            # Visualisasi Total Reach
            st.write("Visualisasi Total Reach Konten Giveaway:")
            fig_reach = px.bar(
                x=['Total Reach Konten Giveaway'],
                y=[total_reach_giveaway],
                labels={'x': 'Jenis Data', 'y': 'Total Reach'},
                title="Total Reach pada Konten Giveaway"
            )
            st.plotly_chart(fig_reach)

        elif menu == "Analisis Bulanan":
            st.header("Analisis Bulanan Instagram")
            if "Tanggal Upload" in df_ig.columns and "Jenis Konten" in df_ig.columns:
                # Mengelompokkan data berdasarkan nama bulan dan jenis konten
                upload_bulanan = (
                    df_ig.groupby([df_ig['Tanggal Upload'].dt.month_name(), 'Jenis Konten'])['Jumlah Konten']
                    .sum()
                    .unstack(fill_value=0)
                    .reindex(columns=['Feed IG', 'Reels IG', 'Story IG'], fill_value=0)
                    .reset_index()
                )

                # Urutkan berdasarkan bulan dimulai dari Juni
                bulan_mapping = ['June', 'July', 'August', 'September', 'October', 'November', 'December', 
                                'January', 'February', 'March', 'April', 'May']
                
                # Konversi kolom bulan ke kategori dengan urutan khusus
                upload_bulanan['Tanggal Upload'] = pd.Categorical(
                    upload_bulanan['Tanggal Upload'], 
                    categories=bulan_mapping, 
                    ordered=True
                )

                # Sort data berdasarkan urutan bulan
                upload_bulanan = upload_bulanan.sort_values('Tanggal Upload').reset_index(drop=True)
                upload_bulanan = upload_bulanan.rename(columns={'Tanggal Upload': 'Bulan'})

                # Tampilkan data dalam tabel
                st.write("Jumlah Konten yang Diupload per Bulan:")
                st.write(upload_bulanan)

                # Visualisasi menggunakan Plotly
                st.write("Visualisasi Jumlah Konten Berdasarkan Jenis Konten:")
                fig_bulan = px.bar(
                    upload_bulanan,
                    x='Bulan',
                    y=['Feed IG', 'Reels IG', 'Story IG'],
                    labels={'value': 'Jumlah Konten', 'variable': 'Jenis Konten'},
                    title="Jumlah Konten per Bulan Berdasarkan Jenis Konten"
                )
                st.plotly_chart(fig_bulan)
            else:
                st.error("Kolom 'Tanggal Upload' atau 'Jenis Konten' tidak ditemukan dalam dataset.")

        elif menu == "Informasi Dataset":
            st.header("Informasi Dataset Instagram")
            st.write(f"Jumlah baris: {len(df_ig)}")
            st.write(f"Jumlah kolom: {df_ig.shape[1]}")
            st.write(f"Nama kolom: {', '.join(df_ig.columns)}")

    elif st.session_state.platform == "TikTok":
        # Mengambil data TikTok dan upload bulanan TikTok dari session state
        df_tiktok = st.session_state.df_tiktok
        upload_bulanan_tiktok = st.session_state.upload_bulanan_tiktok

        # Judul dashboard
        st.title("📊 Dashboard Analisis Performa TikTok")

        if menu == "Data Awal":
            st.header("Tampilan Data Awal")
            st.write("Dataset TikTok:")
            st.write(df_tiktok)

        elif menu == "Analisis Performa":
            st.header("Analisis Performa TikTok")
            st.write("Tabel dan visualisasi performa berdasarkan jenis konten:")

            # Mengelompokkan data berdasarkan jenis konten untuk TikTok
            jenis_konten_analysis_tiktok = df_tiktok.groupby('Type').agg({
                'Reach': 'mean',
                'Engagement': 'mean',
                'Engagement Rate (%)': 'mean',
                'Reach Rate (%)' : 'mean'
            }).reset_index()

            # Merapikan kolom hasil
            jenis_konten_analysis_tiktok.columns = [
                'Jenis Konten',
                'Average Reach',
                'Average Engagement',
                'Average Engagement Rate (%)',
                'Reach Rate (%)
            ]

            # Urutkan data berdasarkan Average Engagement Rate
            jenis_konten_analysis_tiktok = jenis_konten_analysis_tiktok.sort_values(by='Average Engagement Rate (%)', ascending=False)

            # Tampilkan tabel hasil analisis
            st.write("Tabel Performa berdasarkan Jenis Konten:")
            st.write(jenis_konten_analysis_tiktok)

            # Visualisasi rata-rata Engagement Rate per jenis konten
            fig_performance = px.bar(
                jenis_konten_analysis_tiktok,
                x='Jenis Konten',
                y='Average Engagement Rate (%)',
                title="Rata-Rata Engagement Rate per Jenis Konten",
                labels={'Jenis Konten': 'Jenis Konten', 'Average Engagement Rate (%)': 'Rata-Rata Engagement Rate (%)'},
                color='Jenis Konten',  # Warna berdasarkan jenis konten
                color_discrete_sequence=px.colors.qualitative.Set2  # Skema warna yang beragam
            )
            st.plotly_chart(fig_performance)

            # Analisis Berdasarkan Lokasi
            st.write("Distribusi Demografi Berdasarkan Lokasi:")
            df_tiktok['Indonesia'] = pd.to_numeric(df_tiktok['Indonesia'], errors='coerce')
            df_tiktok['Others Negara'] = pd.to_numeric(df_tiktok['Others Negara'], errors='coerce')

            demografi_lokasi_tiktok = (
                df_tiktok[['Indonesia', 'Others Negara']]
                .sum()
                .reset_index(name='Jumlah')
                .rename(columns={'index': 'Lokasi'})
            )
            demografi_lokasi_tiktok = demografi_lokasi_tiktok.sort_values(by='Jumlah', ascending=False)

            # Tampilkan tabel
            st.write(demografi_lokasi_tiktok)

            # Visualisasi Distribusi Lokasi
            fig_lokasi = px.pie(
                demografi_lokasi_tiktok,
                names='Lokasi',
                values='Jumlah',
                title="Distribusi Demografi Berdasarkan Lokasi",
                color='Lokasi',
                color_discrete_sequence=px.colors.qualitative.Set2
            )
            st.plotly_chart(fig_lokasi)

            # Distribusi Demografi Berdasarkan Usia
            st.write("Distribusi Demografi Berdasarkan Usia:")
            usia_kolom = ['18-24', '25-34', '35-44', 'Others']
            df_tiktok[usia_kolom] = df_tiktok[usia_kolom].apply(pd.to_numeric, errors='coerce')

            demografi_usia_tiktok = (
                df_tiktok[usia_kolom]
                .sum()
                .reset_index(name='Jumlah')
                .rename(columns={'index': 'Usia'})
            )
            demografi_usia_tiktok = demografi_usia_tiktok.sort_values(by='Jumlah', ascending=False)

            # Tampilkan tabel
            st.write(demografi_usia_tiktok)

            # Visualisasi Distribusi Usia
            fig_usia = px.bar(
                demografi_usia_tiktok,
                x='Jumlah',
                y='Usia',
                orientation='h',
                title="Distribusi Demografi Berdasarkan Usia",
                labels={'Usia': 'Kelompok Usia', 'Jumlah': 'Jumlah Pengguna'},
                color='Usia',
                color_discrete_sequence=px.colors.qualitative.Pastel
            )
            st.plotly_chart(fig_usia)

            # Distribusi Demografi Berdasarkan Gender
            st.write("Distribusi Demografi Berdasarkan Gender:")
            gender_kolom = ['Male', 'Female', 'Others Gender']
            df_tiktok[gender_kolom] = df_tiktok[gender_kolom].apply(pd.to_numeric, errors='coerce')

            demografi_gender_tiktok = (
                df_tiktok[gender_kolom]
                .sum()
                .reset_index(name='Jumlah')
                .rename(columns={'index': 'Gender'})
            )
            demografi_gender_tiktok = demografi_gender_tiktok.sort_values(by='Jumlah', ascending=False)

            # Tampilkan tabel
            st.write(demografi_gender_tiktok)

            # Visualisasi Distribusi Gender
            fig_gender = px.pie(
                demografi_gender_tiktok,
                names='Gender',
                values='Jumlah',
                title="Distribusi Demografi Berdasarkan Gender",
                hole=0.3,  # Membuatnya menjadi diagram donat
                color='Gender',
                color_discrete_sequence=px.colors.qualitative.G10
            )
            st.plotly_chart(fig_gender)

            # Menambahkan Analisis Perbandingan Routine dan Ad
            st.write("Perbandingan Performa Konten Routine dan Ad:")

            # Memisahkan data berdasarkan 'Note'
            routine_data_tiktok = df_tiktok[df_tiktok['Note'] == 'Routine']
            ad_data_tiktok = df_tiktok[df_tiktok['Note'] == 'Ad']

            # Menghitung rata-rata metrik kinerja untuk masing-masing kategori
            routine_metrics_tiktok = routine_data_tiktok[['Reach', 'Engagement', 'Engagement Rate (%)', 'Views', 'Like', 'Share', 'Comment', 'Save']].mean()
            ad_metrics_tiktok = ad_data_tiktok[['Reach', 'Engagement', 'Engagement Rate (%)', 'Views', 'Like', 'Share', 'Comment', 'Save']].mean()

            # Menggabungkan hasil ke dalam satu DataFrame untuk perbandingan
            comparison_tiktok = pd.DataFrame({
                'Routine': routine_metrics_tiktok,
                'Ad': ad_metrics_tiktok
            })

            # Tambahkan kolom selisih untuk mempermudah analisis
            comparison_tiktok['Difference'] = comparison_tiktok['Ad'] - comparison_tiktok['Routine']

            # Tambahkan kolom selisih dalam persen
            comparison_tiktok['Difference (%)'] = (comparison_tiktok['Difference'] / comparison_tiktok['Routine']) * 100

            # Tampilkan tabel perbandingan
            st.write("Tabel Perbandingan Performa Konten Routine dan Ad:")
            st.write(comparison_tiktok)

            # Visualisasi Perbandingan Rata-Rata
            fig_comparison = px.bar(
                comparison_tiktok,
                x=comparison_tiktok.index,
                y=['Routine', 'Ad'],
                title="Perbandingan Rata-Rata Metrik Performa Konten Routine dan Ad",
                labels={'index': 'Metrik', 'value': 'Rata-Rata', 'variable': 'Jenis Konten'},
                barmode='group',  # Menampilkan bar secara berkelompok
                color='variable',
                color_discrete_sequence=px.colors.qualitative.Set1  # Skema warna yang kontras
            )
            st.plotly_chart(fig_comparison)

            # Menambahkan Heatmap untuk Selisih
            st.write("Heatmap Perbandingan Selisih Metrik Performa antara Routine dan Ad:")

            # Menyusun data selisih menjadi format yang sesuai untuk heatmap
            heatmap_data = comparison_tiktok[['Difference', 'Difference (%)']].transpose()

            # Membuat heatmap
            fig_heatmap = px.imshow(
                heatmap_data,
                labels={'x': 'Metrik', 'y': 'Perbandingan', 'color': 'Selisih'},
                title="Heatmap Perbandingan Selisih Metrik Performa antara Routine dan Ad",
                color_continuous_scale='RdBu',  # Skema warna yang cocok untuk selisih
                aspect="auto"
            )

            # Menampilkan heatmap
            st.plotly_chart(fig_heatmap)

            # Menambahkan Analisis Perbandingan Giveaway vs Non-Giveaway
            st.write("Perbandingan Performa Konten Giveaway vs Non-Giveaway:")

            # Filter konten dengan kata 'giveaway' di kolom Judul Konten
            giveaway_data_tiktok = df_tiktok[df_tiktok['Judul Konten'].str.contains('Giveaway', case=False, na=False)]

            # Rata-rata performa konten giveaway
            giveaway_metrics_tiktok = giveaway_data_tiktok[['Reach', 'Engagement', 'Engagement Rate (%)', 'Views']].mean()

            # Rata-rata performa konten non-giveaway
            non_giveaway_data_tiktok = df_tiktok[~df_tiktok['Judul Konten'].str.contains('Giveaway', case=False, na=False)]
            non_giveaway_metrics_tiktok = non_giveaway_data_tiktok[['Reach', 'Engagement', 'Engagement Rate (%)', 'Views']].mean()

            # Membandingkan performa konten giveaway vs non-giveaway
            comparison_giveaway_tiktok = pd.DataFrame({
                'Giveaway': giveaway_metrics_tiktok,
                'Non-Giveaway': non_giveaway_metrics_tiktok
            })

            # Tambahkan kolom selisih
            comparison_giveaway_tiktok['Difference'] = (comparison_giveaway_tiktok['Giveaway'] - comparison_giveaway_tiktok['Non-Giveaway'])

            # Tambahkan kolom selisih dalam persen
            comparison_giveaway_tiktok['Difference (%)'] = (comparison_giveaway_tiktok['Difference'] / comparison_giveaway_tiktok['Non-Giveaway']) * 100

            # Tampilkan tabel perbandingan
            st.write("Tabel Perbandingan Performa Konten Giveaway vs Non-Giveaway:")
            st.write(comparison_giveaway_tiktok)

            # Visualisasi Perbandingan Rata-Rata
            fig_comparison_giveaway = px.bar(
                comparison_giveaway_tiktok,
                x=comparison_giveaway_tiktok.index,
                y=['Giveaway', 'Non-Giveaway'],
                title="Perbandingan Rata-Rata Metrik Performa Konten Giveaway vs Non-Giveaway",
                labels={'index': 'Metrik', 'value': 'Rata-Rata', 'variable': 'Jenis Konten'},
                barmode='group',  # Menampilkan bar secara berkelompok
                color='variable',
                color_discrete_sequence=px.colors.qualitative.Set1  # Skema warna yang kontras
            )
            st.plotly_chart(fig_comparison_giveaway)

            # Menambahkan Heatmap untuk Selisih Giveaway vs Non-Giveaway
            st.write("Heatmap Perbandingan Selisih Metrik Performa Konten Giveaway vs Non-Giveaway:")

            # Menyusun data selisih menjadi format yang sesuai untuk heatmap
            heatmap_data_giveaway = comparison_giveaway_tiktok[['Difference', 'Difference (%)']].transpose()

            # Membuat heatmap
            fig_heatmap_giveaway = px.imshow(
                heatmap_data_giveaway,
                labels={'x': 'Metrik', 'y': 'Perbandingan', 'color': 'Selisih'},
                title="Heatmap Perbandingan Selisih Metrik Performa Konten Giveaway vs Non-Giveaway",
                color_continuous_scale='RdBu',  # Skema warna yang cocok untuk selisih
                aspect="auto"
            )

            # Menampilkan heatmap
            st.plotly_chart(fig_heatmap_giveaway)

            st.write("Analisis performa konten Giveaway TikTok:")

            # Filter data dengan kata 'giveaway' di kolom Judul Konten
            giveaway_data_tiktok = df_tiktok[df_tiktok['Judul Konten'].str.contains('giveaway', case=False, na=False)]

            # Menghitung total interaksi untuk konten giveaway
            total_interaksi = (giveaway_data_tiktok['Like'].sum() +
                            giveaway_data_tiktok['Share'].sum() +
                            giveaway_data_tiktok['Comment'].sum() +
                            giveaway_data_tiktok['Save'].sum())
            
            st.write(f"**Total Interaksi pada Konten Giveaway**: {total_interaksi}")

            # Menghitung total reach dari konten giveaway
            total_reach_giveaway_tiktok = giveaway_data_tiktok['Reach'].sum()
            st.write(f"**Total Reach Konten Giveaway**: {total_reach_giveaway_tiktok}")

            # Menghitung persentase orang yang tahu tentang giveaway
            jumlah_followers_tiktok = 2266  # Total pengikut dari semua data
            persentase_tahu_tiktok = (total_reach_giveaway_tiktok / jumlah_followers_tiktok) * 100
            st.write(f"**Persentase Orang yang Tahu tentang Giveaway**: {persentase_tahu_tiktok:.2f}%")

            # Visualisasi Total Interaksi
            st.subheader("Visualisasi Total Interaksi Giveaway")
            fig_interaksi = px.bar(
                x=['Like', 'Share', 'Comment', 'Save'],
                y=[giveaway_data_tiktok['Like'].sum(),
                    giveaway_data_tiktok['Share'].sum(),
                    giveaway_data_tiktok['Comment'].sum(),
                    giveaway_data_tiktok['Save'].sum()],
                title="Total Interaksi Giveaway",
                labels={'x': 'Tipe Interaksi', 'y': 'Jumlah Interaksi'},
                color=['Like', 'Share', 'Comment', 'Save'],
                color_discrete_sequence=px.colors.qualitative.Set2
            )
            st.plotly_chart(fig_interaksi)

            # Visualisasi Total Reach dan Persentase Tahu
            st.subheader("Visualisasi Reach dan Persentase Tahu tentang Giveaway")
            fig_reach = px.pie(
                names=["Reach Giveaway", "Total Followers"],
                values=[total_reach_giveaway_tiktok, jumlah_followers_tiktok - total_reach_giveaway_tiktok],
                title="Distribusi Reach Giveaway terhadap Total Followers",
                color=["Reach Giveaway", "Non-Reach"],
                color_discrete_sequence=px.colors.qualitative.Set3
            )
            st.plotly_chart(fig_reach)

            # Visualisasi Persentase Orang yang Tahu tentang Giveaway
            fig_persentase = px.bar(
                x=["Persentase Tahu Giveaway"],
                y=[persentase_tahu_tiktok],
                title="Persentase Orang yang Tahu Tentang Giveaway",
                labels={'x': 'Metrik', 'y': 'Persentase (%)'},
                color=["Persentase Tahu Giveaway"],
                color_discrete_sequence=px.colors.qualitative.Pastel
            )
            st.plotly_chart(fig_persentase)

        elif menu == "Analisis Bulanan":
            st.header("Analisis Bulanan TikTok")
            st.write("Jumlah konten per bulan berdasarkan jenis konten:")

            # Tampilkan tabel hasil analisis bulanan
            st.write("Tabel Jumlah Konten per Bulan Berdasarkan Jenis Konten:")
            st.write(upload_bulanan_tiktok)

            # Visualisasi Analisis Bulanan
            fig_monthly_performance = px.bar(
                upload_bulanan_tiktok,
                x='Bulan',
                y=['Photo Slide', 'Video'],
                title="Performa Konten TikTok Berdasarkan Bulan",
                labels={'Bulan': 'Bulan', 'value': 'Jumlah Konten', 'variable': 'Jenis Konten'}
            )
            st.plotly_chart(fig_monthly_performance)

        elif menu == "Informasi Dataset":
            st.header("Informasi Dataset TikTok")
            st.write(f"Jumlah baris: {len(df_tiktok)}")
            st.write(f"Jumlah kolom: {df_tiktok.shape[1]}")
            st.write(f"Nama kolom: {', '.join(df_tiktok.columns)}")

else:
    st.warning("Silakan muat atau unggah data terlebih dahulu.")

if __name__ == "__main__":
    main()
