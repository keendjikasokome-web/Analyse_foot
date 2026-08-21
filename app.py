import streamlit as st
import requests
import datetime
# --- CONFIGURATION PAGE & STYLES FLASHSCORE ---
st.set_page_config(page_title="Analyse Foot Pro", page_icon="⚽", layout="wide")
st.markdown("""
<style>
    /* Style Sombre style FlashScore */
    .stApp {
        background-color: #0d1117;
        color: #e6edf3;
    }
   
    /* En-tête Championnat */
    .league-header {
        background-color: #161b22;
        padding: 8px 12px;
        border-radius: 6px;
        border-left: 4px solid #e50914;
        font-weight: bold;
        font-size: 15px;
        margin-top: 15px;
        margin-bottom: 10px;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
   
    /* Carte Match */
    .match-card {
        background-color: #1c2128;
        padding: 10px 15px;
        border-radius: 6px;
        margin-bottom: 8px;
        border: 1px solid #30363d;
    }
   
    /* Ligne Équipe */
    .team-row {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 2px 0;
        font-size: 14px;
    }
   
    /* Minute en Direct */
    .live-time {
        color: #ff4b4b;
        font-weight: bold;
        font-size: 13px;
    }
   
    /* Score */
    .score-num {
        font-weight: bold;
        font-size: 16px;
        color: #ffffff;
    }
   
    .score-live {
        color: #ff4b4b;
        font-weight: bold;
        font-size: 16px;
    }
    /* Séparateur */
    hr {
        border-color: #30363d;
    }
</style>
""", unsafe_allow_html=True)
# --- FONCTION NETTOYAGE NOMS D'ÉQUIPES ---
def clean_team_name(name):
    replacements = {
        " FC": "", "CF ": "", " Olympique": "", " Real": " Real",
        "Olympique de Marseille": "Marseille", "Real Betis Balompié": "Betis",
        "Real Sociedad de Fútbol": "Real Sociedad", "Coventry City": "Coventry",
        "Arsenal FC": "Arsenal", " Paris Saint-Germain FC": "PSG"
    }
    cleaned = name
    for key, val in replacements.items():
        cleaned = cleaned.replace(key, val)
    return cleaned.strip()
# --- BARRE LATÉRALE : VIP & DÉVELOPPEUR ---
st.sidebar.title("⚽ Analyse Foot Pro")
st.sidebar.caption("🚀 Développé par **Kevin Kasokome**")
st.sidebar.markdown("---")
st.sidebar.subheader("🔒 Espace Membre VIP")
vip_code = st.sidebar.text_input("Saisissez votre code VIP :", type="password")
is_vip = False
if vip_code == "FOOT2026":
    is_vip = True
    st.sidebar.success("✅ Accès VIP Débloqué !")
elif vip_code:
    st.sidebar.error("❌ Code incorrect")
st.sidebar.markdown("---")
st.sidebar.subheader("💳 Obtenir un accès VIP")
st.sidebar.write("Pour recevoir votre code VIP, effectuez un paiement Mobile Money au :")
st.sidebar.info("📱 **+243 XX XXX XXXX**\n*(M-Pesa / Airtel / Orange)*")
# --- EN-TÊTE PRINCIPAL ---
st.title("⚽ Matchs & Directs")
# SÉLECTEUR DE DATE/ONGLETS
col1, col2, col3 = st.columns(3)
with col1:
    tab_choice = st.radio("Affichage :", ["Tous les matchs", "🔴 EN DIRECT"], horizontal=True)
st.markdown("---")
# --- DONNÉES SIMULÉES / DÉMO FLASHSCORE ---
# (Remplaçable par vos appels API)
matches_data = [
    {
        "league": "ANGLETERRE : Premier League",
        "home": "Arsenal FC", "away": "Coventry City",
        "score_home": 2, "score_away": 0,
        "status": "PAUSED", "minute": "Mi-temps"
    },
    {
        "league": "ESPAGNE : LaLiga",
        "home": "Real Betis Balompié", "away": "Real Sociedad de Fútbol",
        "score_home": 1, "score_away": 0,
        "status": "IN_PLAY", "minute": "65'"
    },
    {
        "league": "FRANCE : Ligue 1",
        "home": "Olympique de Marseille", "away": "RC Strasbourg Alsace",
        "score_home": 1, "score_away": 0,
        "status": "IN_PLAY", "minute": "42'"
    }
]
# Rendre unique la liste des ligues
leagues = list(set(m["league"] for m in matches_data))
for league in leagues:
    # Filtrer les matchs selon la compétition
    league_matches = [m for m in matches_data if m["league"] == league]
   
    # Appliquer filtre DIRECT si sélectionné
    if tab_choice == "🔴 EN DIRECT":
        league_matches = [m for m in league_matches if m["status"] in ["IN_PLAY", "PAUSED"]]
   
    if not league_matches:
        continue
    # Affichage de l'en-tête de ligue
    st.markdown(f'<div class="league-header">🏆 {league} <span>{len(league_matches)}</span></div>', unsafe_allow_html=True)
   
    for match in league_matches:
        home = clean_team_name(match["home"])
        away = clean_team_name(match["away"])
        is_live = match["status"] == "IN_PLAY"
        time_display = match["minute"] if is_live else ("MT" if match["status"] == "PAUSED" else "FT")
       
        score_class = "score-live" if is_live else "score-num"
        time_class = "live-time" if is_live else ""
        # Carte de chaque match style FlashScore
        st.markdown(f"""
        <div class="match-card">
            <div style="display: flex; justify-content: space-between; margin-bottom: 5px;">
                <span class="{time_class}">{time_display}</span>
            </div>
            <div class="team-row">
                <span>⚪ <b>{home}</b></span>
                <span class="{score_class}">{match["score_home"]}</span>
            </div>
            <div class="team-row">
                <span>⚪ <b>{away}</b></span>
                <span class="{score_class}">{match["score_away"]}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
# --- MODULE VIP ---
if is_vip:
    st.markdown("---")
    st.subheader("⭐ Pronostics VIP & Algorithme")
    col_a, col_b = st.columns(2)
    with col_a:
        st.metric("Victoire Marseille", "68%", "+5% ce mois")
    with col_b:
        st.metric("Plus de 1.5 buts (Betis vs Real Sociedad)", "85%", "+2%")