import streamlit as st
import requests
import yt_dlp
import os
import tempfile

st.set_page_config(page_title="All-in-One Downloader", page_icon="📥")

st.title("📥 Downloader TikTok & YouTube")
st.write("Unduh video TikTok tanpa watermark atau video/audio dari YouTube.")

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
    yt_url = st.text_input("Tempel URL Video YouTube:")
    format_choice = st.radio("Pilih Format Unduhan:", ["Video HD (.mp4)", "Audio Jernih (.mp3)"])

    if st.button("Proses YouTube"):
        if yt_url:
            with st.spinner("Memproses media dari YouTube..."):
                try:
                    with tempfile.TemporaryDirectory() as tmpdirname:
                        output_template = os.path.join(tmpdirname, '%(title)s.%(ext)s')
                        
                        # Pengaturan umum yt-dlp untuk menembus proteksi HTTP 403
                        ydl_opts = {
                            'outtmpl': output_template,
                            'quiet': True,
                            'nocheckcertificate': True,
                            'geo_bypass': True,
                            'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                            'extractor_args': {
                                'youtube': {
                                    'player_client': ['android', 'ios']
                                }
                            }
                        }

                        # Menyesuaikan format berdasarkan pilihan
                        if "Audio" in format_choice:
                            ydl_opts.update({
                                'format': 'bestaudio/best',
                                'postprocessors': [{
                                    'key': 'FFmpegExtractAudio',
                                    'preferredcodec': 'mp3',
                                    'preferredquality': '192',
                                }]
                            })
                            mime_type = "audio/mp3"
                            ext = "mp3"
                        else:
                            ydl_opts.update({
                                'format': 'best[ext=mp4]/best'
                            })
                            mime_type = "video/mp4"
                            ext = "mp4"

                        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                            info = ydl.extract_info(yt_url, download=True)
                            title = info.get('title', 'youtube_media')

                        # Ambil berkas hasil unduhan
                        downloaded_files = os.listdir(tmpdirname)
                        if downloaded_files:
                            file_path = os.path.join(tmpdirname, downloaded_files[0])
                            with open(file_path, "rb") as f:
                                file_bytes = f.read()

                            st.success("Media YouTube berhasil diproses!")
                            st.download_button(
                                label=f"⬇️ Unduh Berkas {ext.upper()}",
                                data=file_bytes,
                                file_name=f"{title}.{ext}",
                                mime=mime_type
                            )
                except Exception as e:
                    st.error(f"Terjadi kesalahan saat memproses YouTube: {e}")
        else:
            st.warning("Masukkan URL YouTube terlebih dahulu.")
