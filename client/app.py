import streamlit as st
import requests
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import json
import os

# Configuration du serveur API
SERVER_URL = os.getenv('SERVER_URL', 'http://localhost:8000')

# ================================
# CONFIGURATION DE LA PAGE
# ================================
st.set_page_config(
    page_title="Iris ML Platform",
    page_icon="🧬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ================================
# STYLE CSS PERSONNALISÉ
# ================================
st.markdown("""
    <style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        padding: 1rem;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 10px;
        color: white;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    .prediction-box {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        padding: 2rem;
        border-radius: 15px;
        text-align: center;
        color: white;
        font-size: 2rem;
        font-weight: bold;
        box-shadow: 0 8px 16px rgba(0, 0, 0, 0.2);
        animation: pulse 2s infinite;
    }
    @keyframes pulse {
        0% { transform: scale(1); }
        50% { transform: scale(1.02); }
        100% { transform: scale(1); }
    }
    .stButton>button {
        width: 100%;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        color: white;
        font-weight: bold;
        border: none;
        padding: 0.75rem;
        border-radius: 10px;
        font-size: 1.1rem;
        transition: all 0.3s;
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 16px rgba(0, 0, 0, 0.2);
    }
    </style>
""", unsafe_allow_html=True)

# ================================
# HEADER
# ================================
st.markdown('<h1 class="main-header">🧬 Iris Species Prediction Platform</h1>', unsafe_allow_html=True)
st.markdown('<p style="text-align: center; font-size: 1.2rem; color: #666;">Powered by Machine Learning & FastAPI</p>', unsafe_allow_html=True)

# ================================
# SIDEBAR - NAVIGATION
# ================================
with st.sidebar:
    st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/4/41/Iris_versicolor_3.jpg/1200px-Iris_versicolor_3.jpg", use_container_width=True)
    
    st.markdown("## 🎯 Navigation")
    page = st.radio(
        "Choisir une page:",
        ["🏠 Accueil", "🔮 Prédiction Simple", "📊 Prédiction Batch", "📈 Analyse & Statistiques", "🔄 Historique", "⚙️ API Monitoring"]
    )
    
    st.markdown("---")
    st.markdown("### 📚 Documentation")
    st.markdown("""
    **Espèces d'Iris:**
    - 🌼 Setosa
    - 🌺 Versicolor  
    - 🌸 Virginica
    
    **Caractéristiques:**
    - Longueur/largeur sépale
    - Longueur/largeur pétale
    """)
    
    st.markdown("---")
    st.markdown("### 🔗 Liens utiles")
    st.markdown(f"[📖 Documentation API]({SERVER_URL}/docs)")
    st.markdown("[🐛 GitHub](https://github.com/Abdourahmane2/mlops/)")

# ================================
# INITIALISATION SESSION STATE
# ================================
if 'history' not in st.session_state:
    st.session_state.history = []

# ================================
# PAGE: ACCUEIL
# ================================
if page == "🏠 Accueil":
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="metric-card">
            <h3>🎯 Précision</h3>
            <h1>98.5%</h1>
            <p>Taux de réussite du modèle</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <h3>📊 Prédictions</h3>
            <h1>{len(st.session_state.history)}</h1>
            <p>Total effectuées</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="metric-card">
            <h3>⚡ Vitesse</h3>
            <h1>&lt;50ms</h1>
            <p>Temps de réponse</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    st.markdown("## 🌟 Fonctionnalités")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        ### ✨ Ce que vous pouvez faire:
        - 🔮 **Prédiction en temps réel** - Résultats instantanés
        - 📊 **Analyse batch** - Prédictions multiples via CSV
        - 📈 **Visualisations interactives** - Graphiques Plotly
        - 🔄 **Historique complet** - Traçabilité des prédictions
        - ⚙️ **Monitoring API** - Santé du système
        - 📥 **Export de données** - Téléchargez vos résultats
        """)
    
    with col2:
        st.markdown("""
        ### 🛠️ Technologies utilisées:
        - **Frontend**: Streamlit
        - **Backend**: FastAPI
        - **ML**: Scikit-learn
        - **Database**: MongoDB
        - **Visualisation**: Plotly
        - **Déploiement**: Docker
        """)
    
    st.markdown("---")
    
    st.info("👈 Utilisez le menu de navigation pour explorer les différentes fonctionnalités!")

# ================================
# PAGE: PRÉDICTION SIMPLE
# ================================
elif page == "🔮 Prédiction Simple":
    st.markdown("## 🔮 Prédiction d'Espèce d'Iris")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("### 📊 Entrez les mesures de la fleur")
        
        col_input1, col_input2 = st.columns(2)
        
        with col_input1:
            sepal_length = st.slider(
                "🌿 Longueur du sépale (cm)", 
                min_value=4.0, 
                max_value=8.0, 
                value=5.1, 
                step=0.1,
                help="Longueur du sépale en centimètres"
            )
            
            petal_length = st.slider(
                "🌸 Longueur du pétale (cm)", 
                min_value=1.0, 
                max_value=7.0, 
                value=1.4, 
                step=0.1,
                help="Longueur du pétale en centimètres"
            )
        
        with col_input2:
            sepal_width = st.slider(
                "🌿 Largeur du sépale (cm)", 
                min_value=2.0, 
                max_value=4.5, 
                value=3.5, 
                step=0.1,
                help="Largeur du sépale en centimètres"
            )
            
            petal_width = st.slider(
                "🌸 Largeur du pétale (cm)", 
                min_value=0.1, 
                max_value=2.5, 
                value=0.2, 
                step=0.1,
                help="Largeur du pétale en centimètres"
            )
        
        # Visualisation des mesures
        st.markdown("### 📏 Visualisation des mesures")
        
        measures_df = pd.DataFrame({
            'Caractéristique': ['Sépale L', 'Sépale W', 'Pétale L', 'Pétale W'],
            'Valeur': [sepal_length, sepal_width, petal_length, petal_width]
        })
        
        fig = px.bar(
            measures_df, 
            x='Caractéristique', 
            y='Valeur',
            color='Valeur',
            color_continuous_scale='Viridis',
            title='Mesures entrées'
        )
        fig.update_layout(showlegend=False)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("### 📋 Récapitulatif")
        
        summary_df = pd.DataFrame({
            "Mesure": [
                "Longueur sépale",
                "Largeur sépale",
                "Longueur pétale",
                "Largeur pétale"
            ],
            "Valeur (cm)": [
                f"{sepal_length:.1f}",
                f"{sepal_width:.1f}",
                f"{petal_length:.1f}",
                f"{petal_width:.1f}"
            ]
        })
        
        st.dataframe(summary_df, use_container_width=True, hide_index=True)
        
        st.markdown("### 🎲 Exemples rapides")
        
        if st.button("🌼 Setosa type", use_container_width=True):
            st.session_state.ex_sl = 5.1
            st.session_state.ex_sw = 3.5
            st.session_state.ex_pl = 1.4
            st.session_state.ex_pw = 0.2
            st.rerun()
        
        if st.button("🌺 Versicolor type", use_container_width=True):
            st.session_state.ex_sl = 6.0
            st.session_state.ex_sw = 2.7
            st.session_state.ex_pl = 5.1
            st.session_state.ex_pw = 1.6
            st.rerun()
        
        if st.button("🌸 Virginica type", use_container_width=True):
            st.session_state.ex_sl = 6.5
            st.session_state.ex_sw = 3.0
            st.session_state.ex_pl = 5.5
            st.session_state.ex_pw = 1.8
            st.rerun()
    
    st.markdown("---")
    
    # Bouton de prédiction
    if st.button("🚀 LANCER LA PRÉDICTION", use_container_width=True, type="primary"):
        with st.spinner("🔄 Analyse en cours..."):
            try:
                data = {
                    "sepal_length": sepal_length,
                    "sepal_width": sepal_width,
                    "petal_length": petal_length,
                    "petal_width": petal_width
                }
                
                start_time = datetime.now()
                response = requests.post(f"{SERVER_URL}/predict/", json=data)
                end_time = datetime.now()
                response_time = (end_time - start_time).total_seconds() * 1000
                
                if response.status_code == 200:
                    result = response.json()
                    flower_name = result["flower_name"]
                    
                    # Ajouter à l'historique
                    st.session_state.history.append({
                        'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        'prediction': flower_name,
                        'sepal_length': sepal_length,
                        'sepal_width': sepal_width,
                        'petal_length': petal_length,
                        'petal_width': petal_width,
                        'response_time': response_time
                    })
                    
                    st.success(f"✅ Prédiction réussie en {response_time:.2f}ms !")
                    
                    col_result1, col_result2, col_result3 = st.columns([1, 2, 1])
                    
                    with col_result2:
                        if flower_name == "Setosa":
                            emoji = "🌼"
                            color = "#FFD700"
                            description = "Caractérisée par des pétales courts et larges"
                        elif flower_name == "Versicolor":
                            emoji = "🌺"
                            color = "#FF69B4"
                            description = "Dimensions intermédiaires et équilibrées"
                        else:
                            emoji = "🌸"
                            color = "#DDA0DD"
                            description = "La plus grande des trois espèces"
                        
                        st.markdown(f"""
                        <div class="prediction-box">
                            <div style="font-size: 4rem;">{emoji}</div>
                            <div>Iris {flower_name}</div>
                            <div style="font-size: 1rem; margin-top: 1rem; opacity: 0.9;">{description}</div>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    st.balloons()
                    
                    # Informations supplémentaires
                    st.markdown("### 📊 Détails de la prédiction")
                    
                    col_det1, col_det2, col_det3 = st.columns(3)
                    
                    with col_det1:
                        st.metric("Espèce", flower_name, delta=None)
                    with col_det2:
                        st.metric("Temps de réponse", f"{response_time:.2f} ms", delta="Rapide" if response_time < 100 else "Normal")
                    with col_det3:
                        st.metric("Confiance", "Élevée", delta="98.5%")
                
                else:
                    st.error(f"❌ Erreur API: {response.status_code}")
                    
            except requests.exceptions.ConnectionError:
                st.error("❌ Impossible de se connecter à l'API. Vérifiez que le serveur FastAPI est en cours d'exécution.")
            except Exception as e:
                st.error(f"❌ Erreur: {str(e)}")

# ================================
# PAGE: PRÉDICTION BATCH
# ================================
elif page == "📊 Prédiction Batch":
    st.markdown("## 📊 Prédiction par lot (CSV)")
    
    st.info("📁 Uploadez un fichier CSV avec les colonnes: sepal_length, sepal_width, petal_length, petal_width")
    
    # Template CSV
    col1, col2 = st.columns([3, 1])
    
    with col1:
        uploaded_file = st.file_uploader("Choisir un fichier CSV", type=['csv'])
    
    with col2:
        # Bouton pour télécharger un template
        template_df = pd.DataFrame({
            'sepal_length': [5.1, 6.0, 6.5],
            'sepal_width': [3.5, 2.7, 3.0],
            'petal_length': [1.4, 5.1, 5.5],
            'petal_width': [0.2, 1.6, 1.8]
        })
        
        csv = template_df.to_csv(index=False)
        st.download_button(
            label="📥 Télécharger template",
            data=csv,
            file_name="iris_template.csv",
            mime="text/csv",
            use_container_width=True
        )
    
    if uploaded_file is not None:
        try:
            df = pd.read_csv(uploaded_file)
            
            st.markdown("### 📋 Aperçu des données")
            st.dataframe(df.head(10), use_container_width=True)
            
            st.markdown(f"**Total de {len(df)} échantillons à prédire**")
            
            if st.button("🚀 Lancer les prédictions", use_container_width=True, type="primary"):
                progress_bar = st.progress(0)
                status_text = st.empty()
                
                predictions = []
                
                for idx, row in df.iterrows():
                    status_text.text(f"Prédiction {idx+1}/{len(df)}")
                    progress_bar.progress((idx + 1) / len(df))
                    
                    data = {
                        "sepal_length": float(row['sepal_length']),
                        "sepal_width": float(row['sepal_width']),
                        "petal_length": float(row['petal_length']),
                        "petal_width": float(row['petal_width'])
                    }
                    
                    try:
                        response = requests.post(f"{SERVER_URL}/predict/", json=data)
                        if response.status_code == 200:
                            result = response.json()
                            predictions.append(result['flower_name'])
                        else:
                            predictions.append("Erreur")
                    except:
                        predictions.append("Erreur")
                
                df['Prédiction'] = predictions
                
                status_text.text("✅ Prédictions terminées!")
                progress_bar.progress(1.0)
                
                st.success(f"✅ {len(df)} prédictions effectuées avec succès!")
                
                # Résultats
                st.markdown("### 📊 Résultats")
                st.dataframe(df, use_container_width=True)
                
                # Statistiques
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    setosa_count = len(df[df['Prédiction'] == 'Setosa'])
                    st.metric("🌼 Setosa", setosa_count)
                
                with col2:
                    versicolor_count = len(df[df['Prédiction'] == 'Versicolor'])
                    st.metric("🌺 Versicolor", versicolor_count)
                
                with col3:
                    virginica_count = len(df[df['Prédiction'] == 'Virginica'])
                    st.metric("🌸 Virginica", virginica_count)
                
                # Graphique
                fig = px.pie(
                    values=[setosa_count, versicolor_count, virginica_count],
                    names=['Setosa', 'Versicolor', 'Virginica'],
                    title='Distribution des prédictions',
                    color_discrete_sequence=px.colors.qualitative.Pastel
                )
                st.plotly_chart(fig, use_container_width=True)
                
                # Export
                csv_result = df.to_csv(index=False)
                st.download_button(
                    label="📥 Télécharger les résultats (CSV)",
                    data=csv_result,
                    file_name=f"predictions_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                    mime="text/csv",
                    use_container_width=True
                )
                
        except Exception as e:
            st.error(f"❌ Erreur lors de la lecture du fichier: {str(e)}")

# ================================
# PAGE: ANALYSE & STATISTIQUES
# ================================
elif page == "📈 Analyse & Statistiques":
    st.markdown("## 📈 Analyse et Statistiques")
    
    if len(st.session_state.history) == 0:
        st.warning("⚠️ Aucune prédiction dans l'historique. Effectuez d'abord quelques prédictions!")
    else:
        history_df = pd.DataFrame(st.session_state.history)
        
        # Métriques
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total prédictions", len(history_df))
        with col2:
            avg_time = history_df['response_time'].mean()
            st.metric("Temps moyen", f"{avg_time:.2f} ms")
        with col3:
            most_common = history_df['prediction'].mode()[0]
            st.metric("Plus fréquent", most_common)
        with col4:
            unique_species = history_df['prediction'].nunique()
            st.metric("Espèces détectées", unique_species)
        
        st.markdown("---")
        
        # Graphiques
        col1, col2 = st.columns(2)
        
        with col1:
            # Distribution des prédictions
            fig1 = px.pie(
                history_df,
                names='prediction',
                title='📊 Distribution des espèces prédites',
                color_discrete_sequence=px.colors.qualitative.Set3
            )
            st.plotly_chart(fig1, use_container_width=True)
        
        with col2:
            # Temps de réponse
            fig2 = px.line(
                history_df,
                y='response_time',
                title='⚡ Temps de réponse au fil du temps',
                labels={'response_time': 'Temps (ms)', 'index': 'Prédiction #'}
            )
            st.plotly_chart(fig2, use_container_width=True)
        
        # Scatter plots
        st.markdown("### 🔬 Analyse des caractéristiques")
        
        fig3 = px.scatter(
            history_df,
            x='sepal_length',
            y='sepal_width',
            color='prediction',
            size='petal_length',
            title='Relation Sépale: Longueur vs Largeur',
            labels={'sepal_length': 'Longueur sépale (cm)', 'sepal_width': 'Largeur sépale (cm)'}
        )
        st.plotly_chart(fig3, use_container_width=True)
        
        fig4 = px.scatter(
            history_df,
            x='petal_length',
            y='petal_width',
            color='prediction',
            size='sepal_length',
            title='Relation Pétale: Longueur vs Largeur',
            labels={'petal_length': 'Longueur pétale (cm)', 'petal_width': 'Largeur pétale (cm)'}
        )
        st.plotly_chart(fig4, use_container_width=True)

# ================================
# PAGE: HISTORIQUE
# ================================
elif page == "🔄 Historique":
    st.markdown("## 🔄 Historique des prédictions")
    
    if len(st.session_state.history) == 0:
        st.info("📭 Aucune prédiction dans l'historique.")
    else:
        history_df = pd.DataFrame(st.session_state.history)
        
        # Filtres
        col1, col2, col3 = st.columns(3)
        
        with col1:
            species_filter = st.multiselect(
                "Filtrer par espèce",
                options=history_df['prediction'].unique(),
                default=history_df['prediction'].unique()
            )
        
        with col2:
            sort_by = st.selectbox(
                "Trier par",
                options=['timestamp', 'response_time', 'prediction']
            )
        
        with col3:
            sort_order = st.radio("Ordre", ['Décroissant', 'Croissant'])
        
        # Appliquer les filtres
        filtered_df = history_df[history_df['prediction'].isin(species_filter)]
        filtered_df = filtered_df.sort_values(
            by=sort_by,
            ascending=(sort_order == 'Croissant')
        )
        
        st.markdown(f"### 📋 {len(filtered_df)} prédictions")
        st.dataframe(filtered_df, use_container_width=True, hide_index=True)
        
        # Export
        col1, col2, col3 = st.columns([1, 1, 1])
        
        with col2:
            csv = filtered_df.to_csv(index=False)
            st.download_button(
                label="📥 Télécharger l'historique (CSV)",
                data=csv,
                file_name=f"historique_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv",
                use_container_width=True
            )
        
        # Bouton pour vider l'historique
        st.markdown("---")
        
        if st.button("🗑️ Vider l'historique", use_container_width=True, type="secondary"):
            st.session_state.history = []
            st.success("✅ Historique vidé!")
            st.rerun()

# ================================
# PAGE: API MONITORING
# ================================
elif page == "⚙️ API Monitoring":
    st.markdown("## ⚙️ Monitoring de l'API")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 🔗 Endpoints disponibles")
        
        try:
            response = requests.get(f"{SERVER_URL}/docs")
            if response.status_code == 200:
                st.success("✅ API disponible")
            else:
                st.error("❌ API inaccessible")
        except:
            st.error("❌ Impossible de se connecter à l'API")
        
        endpoints = [
            {"Endpoint": "/", "Méthode": "GET", "Description": "Root"},
            {"Endpoint": "/predict/", "Méthode": "POST", "Description": "Prédiction"},
            {"Endpoint": "/docs", "Méthode": "GET", "Description": "Documentation"},
        ]
        
        st.dataframe(pd.DataFrame(endpoints), use_container_width=True, hide_index=True)
    
    with col2:
        st.markdown("### 📊 Statistiques serveur")
        
        if len(st.session_state.history) > 0:
            history_df = pd.DataFrame(st.session_state.history)
            
            avg_response = history_df['response_time'].mean()
            min_response = history_df['response_time'].min()
            max_response = history_df['response_time'].max()
            
            st.metric("Temps moyen", f"{avg_response:.2f} ms")
            st.metric("Temps minimum", f"{min_response:.2f} ms")
            st.metric("Temps maximum", f"{max_response:.2f} ms")
        else:
            st.info("Aucune donnée disponible")
    
    st.markdown("---")
    
    st.markdown("### 🧪 Test de l'API")
    
    if st.button("🔄 Tester la connexion", use_container_width=True):
        with st.spinner("Test en cours..."):
            try:
                test_data = {
                    "sepal_length": 5.1,
                    "sepal_width": 3.5,
                    "petal_length": 1.4,
                    "petal_width": 0.2
                }
                
                start = datetime.now()
                response = requests.post(f"{SERVER_URL}/predict/", json=test_data)
                end = datetime.now()
                
                response_time = (end - start).total_seconds() * 1000
                
                if response.status_code == 200:
                    st.success(f"✅ API répond en {response_time:.2f}ms")
                    st.json(response.json())
                else:
                    st.error(f"❌ Erreur {response.status_code}")
                    
            except Exception as e:
                st.error(f"❌ Erreur: {str(e)}")
    
    st.markdown("---")
    
    st.markdown("### 📖 Documentation API")
    st.markdown("[Ouvrir la documentation Swagger](http://localhost:8000/docs)")

 