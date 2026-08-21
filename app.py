import streamlit as st
import requests
# --- CONFIGURATION DE LA PAGE ---
st.set_page_config(page_title="Flashscore Live", page_icon="⚽", layout="wide")
# --- CLE API INTEGRÉE ---
API_KEY = "2c29a09f780640819233da95eed7470d"
API_URL = "https://api.football-data.org/v4/matches"
headers = {"X-Auth-Token": API_KEY}
# --- STYLES FLASHSCORE (INTERFACE VASTE ET COMPACTE) ---
st.markdown("""
<style>
    /* Réduire les marges globales pour un rendu vaste */
    .block-container {
        padding-top: 1.5rem !important;
        padding-bottom: 1rem !important;
        max-width: 95% !important;
    }
   
    .stApp { background-color: #0d1117; color: #c9d1d9; }
   
    /* En-tête de ligue compact */
    .league-header {
        background-color: #161b22;
        padding: 5px 10px;
        border-radius: 4px;
        border-left: 3px solid #ee2435;
        font-weight: bold;
        font-size: 13px;
        margin-top: 10px;
        margin-bottom: 6px;
        color: #ffffff;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
   
    /* Réduire la taille du texte dans l'accordéon */
    .streamlit-expanderHeader {
        font-size: 13px !important;
        padding: 4px 8px !important;
    }
</style>
""", unsafe_allow_html=True)
# --- FONCTION DE NETTOYAGE / RACCOURCISSEMENT DES NOMS ---
def format_team_name(name):
    if not name:
        return ""
    # Mots et suffixes courants à nettoyer/raccourcir
    replacements = {
        " FC": "", "CF ": "", "FC ": "", " Olympique": "", " Real": "",
        "Real Sociedad de Fútbol": "R. Sociedad",
        "Real Betis Balompié": "Betis",
        "Paris Saint-Germain FC": "PSG",
        "Borussia Dortmund": "Dortmund",
        "Atletico de Madrid": "Atlético",
        "Club Atlético de Madrid": "Atlético",
        "Manchester City FC": "Man City",
        "Manchester United FC": "Man United",
        "Tottenham Hotspur FC": "Tottenham",
        "Wolverhampton Wanderers FC": "Wolves",
        "Brighton & Hove Albion FC": "Brighton",
        "Athletic Club": "Athletic Bilbao"
    }
    clean_name = name
    for key, val in replacements.items():
        clean_name = clean_name.replace(key, val)
    return clean_name.strip()
# --- FONCTION POUR CHARGER LES MATCHS ---
@st.cache_data(ttl=60)
def fetch_matches():
    try:
        response = requests.get(API_URL, headers=headers)
        if response.status_code == 200:
            return response.json().get("matches", []), None
        elif response.status_code == 429:
            return None, "Limite de requêtes atteinte. Réessaie dans une minute."
        else:
            return None, f"Erreur API ({response.status_code})."
    except Exception as e:
        return None, f"Erreur : {str(e)}"
# --- INTERFACE PRINCIPALE ---
st.title("⚽ Flashscore")
# Bouton d'actualisation rapide
col_space, col_btn = st.columns([5, 1])
with col_btn:
    if st.button("🔄 Actualiser"):
        st.cache_data.clear()
tab_matchs, tab_standings, tab_news = st.tabs(["📊 Matchs & Scores", "🏆 Classements", "📰 Actualités"])
with tab_matchs:
    matches, error = fetch_matches()
    if error:
        st.error(error)
    elif not matches:
        st.warning("Aucun match au programme aujourd'hui.")
    else:
        leagues = {}
        for m in matches:
            l_name = m.get("competition", {}).get("name", "Autres")
            leagues.setdefault(l_name, []).append(m)
        for l_name, l_matches in leagues.items():
            st.markdown(f'<div class="league-header">🏆 {l_name}</div>', unsafe_allow_html=True)
            for m in l_matches:
                # Récupération et raccourcissement des noms
                raw_h = m["homeTeam"].get("shortName") or m["homeTeam"].get("name")
                raw_a = m["awayTeam"].get("shortName") or m["awayTeam"].get("name")
                h = format_team_name(raw_h)
                a = format_team_name(raw_a)
               
                # Scores
                sh = m["score"]["fullTime"]["home"]
                sa = m["score"]["fullTime"]["away"]
                sh_str = str(sh) if sh is not None else "0"
                sa_str = str(sa) if sa is not None else "0"
               
                # Statut compact
                status = m.get("status")
                if status == "IN_PLAY":
                    label = "🔴 LIVE"
                elif status == "PAUSED":
                    label = "⏸️ MT"
                elif status == "FINISHED":
                    label = "FT"
                else:
                    label = m.get("utcDate", "")[11:16]
                # Titre de ligne compact (façon Flashscore)
                match_title = f"{label} | {h} {sh_str} - {sa_str} {a}"
               
                with st.expander(match_title):
                    st.write(f"**{h} {sh_str} - {sa_str} {a}**")
                    goals = m.get("goals", [])
                    if goals:
                        st.markdown("**⚽ Buteurs :**")
                        for g in goals:
                            scorer = g.get('scorer', {}).get('name', 'Buteur')
                            team = format_team_name(g.get('team', {}).get('name', ''))
                            minute = g.get('minute', '')
                            st.write(f"• {minute}' {scorer} ({team})")
                    else:
                        st.caption("Aucun buteur renseigné pour le moment.")
with tab_standings:
    st.info("Classements en cours de déploiement.")
with tab_news:
    st.info("Actualités en cours de déploiement.")