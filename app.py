import streamlit as st
import requests

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
                    cobalt_url = "https://api.cobalt.tools/"
                    headers = {
                        "Accept": "application/json",
                        "Content-Type": "application/json"
                    }
                    
                    is_audio = "Audio" in format_choice
                    payload = {
                        "url": yt_url,
                        "downloadMode": "audio" if is_audio else "auto",
                        "audioFormat": "mp3" if is_audio else "best",
                        "videoQuality": "720"
                    }

                    res = requests.post(cobalt_url, json=payload, headers=headers)
                    res_data = res.json()

                    status = res_data.get("status")

                    if status in ["tunnel", "redirect"]:
                        download_url = res_data.get("url")
                        st.success("Media YouTube berhasil diproses!")
                        # Mengarahkan unduhan langsung ke browser pengguna
                        st.link_button("⬇️ Unduh Media Sekarang", download_url)

                    elif status == "picker":
                        st.success("Pilihan media ditemukan:")
                        for item in res_data.get("picker", []):
                            st.link_button(f"⬇️ Unduh Media ({item.get('type', 'file')})", item.get("url"))

                    else:
                        error_msg = res_data.get("text", "Server API sedang dibatasi oleh YouTube.")
                        st.error(f"Gagal memproses: {error_msg}")
                        st.info("💡 Server publik YouTube sering mengalami batasan kuota. Jika terus gagal, coba kembali beberapa saat lagi atau gunakan URL video lain.")

                except Exception as e:
                    st.error(f"Terjadi kesalahan koneksi: {e}")
        else:
            st.warning("Masukkan URL YouTube terlebih dahulu.")
