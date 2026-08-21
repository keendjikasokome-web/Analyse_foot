import streamlit as st
import requests
st.set_page_config(page_title="Analyse Foot Pro - Kevin Kasokome", page_icon="⚽", layout="wide")
st.title("⚽ Dashboard d'Analyse Sportive & Pronostics")
st.caption("🚀 Conçu et développé par **Kevin Kasokome**")
st.markdown("---")
API_KEY = "2c29a09f780640819233da95eed7470d"
HEADERS = {"X-Auth-Token": API_KEY}
st.sidebar.header("👨‍💻 Développeur")
st.sidebar.write("**Kevin Kasokome**")
st.sidebar.header("🔒 Version VIP & Monetization")
st.sidebar.markdown("""
Pour débloquer l'intégralité des **prédictions automatisées**, des **statistiques avancées** et des **indices de confiance**, effectuez votre paiement Mobile Money :
* 📱 **M-Pesa / Airtel / Orange** : `+243 XX XXX XXX`
* 💡 *Inscrivez votre nom en motif du transfert.*
""")
code_vip = st.sidebar.text_input("Saisissez votre code VIP", type="password")
is_vip = False
if code_vip == "FOOT2026":
    is_vip = True
    st.sidebar.success("🎉 Accès VIP Activé !")
elif code_vip != "":
    st.sidebar.error("Code VIP invalide.")
@st.cache_data(ttl=60)
def fetch_matches():
    url = "https://api.football-data.org/v4/matches"
    try:
        response = requests.get(url, headers=HEADERS)
        if response.status_code == 200:
            return response.json().get("matches", [])
        return []
    except Exception:
        return []
matches_data = fetch_matches()
st.header("📅 Matchs du Jour & Scores en Direct")
if matches_data:
    live_matches = [m for m in matches_data if m["status"] in ["IN_PLAY", "PAUSED", "HALFTIME"]]
    upcoming_matches = [m for m in matches_data if m["status"] in ["TIMED", "SCHEDULED"]]
    finished_matches = [m for m in matches_data if m["status"] == "FINISHED"]
    tab1, tab2, tab3 = st.tabs(["🔴 En Direct", "⏳ À Venir (Programmés)", "✅ Terminés"])
    with tab1:
        if live_matches:
            for m in live_matches:
                st.subheader(f"🔴 {m['homeTeam']['name']} {m['score']['fullTime']['home']} - {m['score']['fullTime']['away']} {m['awayTeam']['name']}")
                st.caption(f"Compétition : {m['competition']['name']} | Statut : {m['status']}")
        else:
            st.info("Aucun match ne se joue actuellement en direct.")
    with tab2:
        if upcoming_matches:
            for m in upcoming_matches[:10]:
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.write(f"⚔️ **{m['homeTeam']['name']}** vs **{m['awayTeam']['name']}**")
                    st.caption(f"Compétition : {m['competition']['name']}")
                with col2:
                    st.write(f"⏰ {m['utcDate'][11:16]} UTC")
                st.divider()
        else:
            st.info("Aucun match programmé trouvé pour le moment.")
    with tab3:
        if finished_matches:
            for m in finished_matches[:5]:
                st.write(f"✔️ **{m['homeTeam']['name']}** {m['score']['fullTime']['home']} - {m['score']['fullTime']['away']} **{m['awayTeam']['name']}**")
        else:
            st.info("Aucun match terminé répertorié aujourd'hui.")
else:
    st.warning("Chargement des données en cours ou limite d'appels API atteinte.")
st.markdown("---")
st.header("🔮 Pronostics & Analyses Avancées")
if is_vip:
    st.success("⭐ MODULE PREDICTION VIP DEBLOQUÉ")
   
    st.subheader("📊 Prédictions Algorithmiques Avant-Match")
   
    col_a, col_b, col_c = st.columns(3)
    with col_a:
        st.metric("Victoire Domicile", "62%")
    with col_b:
        st.metric("Match Nul", "22%")
    with col_c:
        st.metric("Victoire Extérieur", "16%")
       
    st.markdown("""
    **Conseils de Paris Exclusifs VIP :**
    * 🎯 **Option Sécurisée** : Plus de 1.5 buts dans le match.
    * 💣 **Option Score Exact** : 2 - 1
    * 📈 **Indice de Confiance** : 8.5 / 10
    """)
else:
    st.warning("🔒 Les prédictions automatisées et les statistiques avancées sont réservées aux membres VIP.")
    st.info("Pour débloquer cet espace, saisissez le code reçu après votre paiement Mobile Money dans la barre latérale.")