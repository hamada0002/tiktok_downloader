import streamlit as st
import requests
import streamlit.components.v1 as components

st.set_page_config(page_title="All-in-One Downloader", page_icon="📥")

st.title("📥 Downloader TikTok & YouTube")
st.write("Unduh video TikTok tanpa watermark atau media dari YouTube.")

tab1, tab2 = st.tabs(["🎵 TikTok", "▶️ YouTube"])

# --- TAB 1: TIKTOK ---
with tab1:
    st.header("TikTok Downloader")
    tiktok_url = st.text_input("Tempel URL Video TikTok:")

    if st.button("Proses TikTok"):
        if tiktok_url:
            with st.spinner("Mengambil data video TikTok..."):
                try:
                    response = requests.post(
                        "https://www.tikwm.com/api/",
                        data={"url": tiktok_url, "hd": 1}
                    ).json()

                    if response.get("code") == 0:
                        video_data = response["data"]
                        download_url = video_data.get("hdplay") or video_data.get("play")
                        
                        st.success("Video berhasil diproses!")
                        st.write(f"**Judul:** {video_data.get('title', 'Video TikTok')}")
                        st.video(download_url)

                        video_bytes = requests.get(download_url).content
                        st.download_button(
                            label="⬇️ Unduh Video HD (.mp4)",
                            data=video_bytes,
                            file_name=f"tiktok_{video_data.get('id')}.mp4",
                            mime="video/mp4"
                        )
                    else:
                        st.error("Gagal mengambil video. Pastikan tautan valid.")
                except Exception as e:
                    st.error(f"Terjadi kesalahan: {e}")
        else:
            st.warning("Masukkan URL TikTok terlebih dahulu.")

# --- TAB 2: YOUTUBE ---
with tab2:
    st.header("YouTube Downloader")
    yt_url = st.text_input("Tempel URL Video YouTube di sini:", placeholder="https://www.youtube.com/watch?v=...")

    if yt_url:
        # Bersihkan URL untuk mengambil ID Video
        clean_url = yt_url.strip()
        
        st.success("Pilih metode unduhan di bawah ini:")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("1. Pintasan Instan (Rekomendasi)")
            # Mengubah URL menjadi pintasan bebas blokir IP
            ss_url = clean_url.replace("youtube.com", "ssyoutube.com").replace("youtu.be/", "ssyoutube.com/watch?v=")
            pp_url = clean_url.replace("youtube.com", "youtubepp.com").replace("youtu.be/", "youtubepp.com/watch?v=")
            
            st.link_button("🚀 Unduh via SaveFrom (MP4/MP3)", ss_url, use_container_width=True)
            st.link_button("🚀 Unduh via Y2Mate (MP4/MP3)", pp_url, use_container_width=True)

        with col2:
            st.subheader("2. Pemproses Langsung")
            st.write("Jalankan konverter langsung di browser Anda:")
            # Widget konverter client-side bebas dari pemblokiran server
            embed_code = f"""
            <iframe src="https://loader.to/api/card/?url={clean_url}" 
                    width="100%" 
                    height="300px" 
                    scrolling="no" 
                    style="border:none; border-radius:10px;">
            </iframe>
            """
            components.html(embed_code, height=320)
    else:
        st.info("💡 Tempelkan tautan YouTube di atas untuk memunculkan opsi unduhan MP3/MP4.")
