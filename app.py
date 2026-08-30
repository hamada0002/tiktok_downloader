import streamlit as st
import requests

st.set_page_config(page_title="TikTok HD Downloader", page_icon="🎵")

st.title("🎵 TikTok Video Downloader")
st.write("Unduh video TikTok tanpa watermark dalam kualitas HD.")

# Input URL dari pengguna
tiktok_url = st.text_input("Tempel URL Video TikTok di sini:")

if st.button("Proses Video"):
    if tiktok_url:
        with st.spinner("Mengambil data video..."):
            try:
                # Memanggil API TikWM dengan parameter hd=1
                response = requests.post(
                    "https://www.tikwm.com/api/",
                    data={"url": tiktok_url, "hd": 1}
                ).json()

                if response.get("code") == 0:
                    video_data = response["data"]
                    # Menggunakan URL HD jika tersedia, fallback ke URL standar tanpa watermark
                    download_url = video_data.get("hdplay") or video_data.get("play")
                    
                    st.success("Video berhasil diproses!")
                    st.write(f"**Judul:** {video_data.get('title', 'Video TikTok')}")
                    st.write(f"**Pengunggah:** @{video_data.get('author', {}).get('unique_id', 'user')}")

                    # Pratinjau pemutar video
                    st.video(download_url)

                    # Ambil file video untuk tombol unduh langsung
                    video_bytes = requests.get(download_url).content
                    
                    st.download_button(
                        label="⬇️ Unduh Video HD",
                        data=video_bytes,
                        file_name=f"tiktok_{video_data.get('id')}.mp4",
                        mime="video/mp4"
                    )
                else:
                    st.error("Gagal mengambil video. Pastikan tautan TikTok valid dan akun tidak diprivat.")
            except Exception as e:
                st.error(f"Terjadi kesalahan koneksi: {e}")
    else:
        st.warning("Silakan masukkan URL TikTok terlebih dahulu.")
