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
            with st.spinner("Mencari server yang tersedia..."):
                is_audio = "Audio" in format_choice
                success = False
                
                # Daftar server API publik alternatif untuk mengantisipasi blokir IP
                api_instances = [
                    "https://api.cobalt.tools/",
                    "https://cobalt-api.kwiatek.xyz/",
                    "https://api.co.wuk.sh/"
                ]
                
                payload = {
                    "url": yt_url,
                    "downloadMode": "audio" if is_audio else "auto",
                    "audioFormat": "mp3" if is_audio else "best",
                    "videoQuality": "720"
                }
                headers = {
                    "Accept": "application/json",
                    "Content-Type": "application/json"
                }

                # Mencoba setiap server satu per satu
                for api_url in api_instances:
                    try:
                        res = requests.post(api_url, json=payload, headers=headers, timeout=8)
                        if res.status_code == 200:
                            res_data = res.json()
                            status = res_data.get("status")
                            
                            if status in ["tunnel", "redirect"]:
                                download_url = res_data.get("url")
                                st.success("Media YouTube berhasil diproses!")
                                st.link_button("⬇️ Unduh Media Sekarang", download_url)
                                success = True
                                break
                            elif status == "picker":
                                st.success("Pilihan media ditemukan:")
                                for item in res_data.get("picker", []):
                                    st.link_button(f"⬇️ Unduh Media ({item.get('type', 'file')})", item.get("url"))
                                success = True
                                break
                    except Exception:
                        continue  # Lanjut ke server berikutnya jika terjadi timeout/error

                # Solusi cadangan jika seluruh API publik sedang dibatasi oleh YouTube
                if not success:
                    st.warning("⚠️ Semua server API gratisan sedang dibatasi oleh YouTube saat ini.")
                    st.info("Gunakan tombol alternatif di bawah ini untuk membuka halaman unduhan langsung:")
                    
                    video_id = yt_url.replace("https://www.youtube.com/watch?v=", "").replace("https://youtu.be/", "").split("&")[0]
                    st.link_button("🌐 Buka via Y2Mate", f"https://www.y2mate.com/youtube/{video_id}")
                    st.link_button("🌐 Buka via Cobalt Web", "https://cobalt.tools/")
        else:
            st.warning("Masukkan URL YouTube terlebih dahulu.")
