import sys
import os
import unittest
from pathlib import Path
import django
from datetime import datetime

# ==========================================
# CONFIGURATION DU SYSTÈME (LE "PONT")
# ==========================================
def setup_django_environment():
    """Connecte le script de test au projet Django (cod_test)"""
    
    base_dir = Path(__file__).resolve().parent
    
    # On remonte d'un cran pour trouver 'cod_test'
    project_path = base_dir.parent
    
    sys.path.insert(0, str(project_path))
    
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cooldeal.settings')
    try:
        django.setup()
        print(f"✅ Environnement Django chargé depuis : {project_path}")
    except Exception as e:
        print(f"❌ Erreur critique lors du chargement de Django : {e}")
        sys.exit(1)

# ==========================================
# MOTEUR DE TEST
# ==========================================
def run_tests_in_folder(folder_name, title):
    """Cherche et exécute les tests dans un dossier spécifique"""
    print(f"\n" + "-"*60)
    print(f"📦 MODULE : {title}")
    print("-"*60)

    loader = unittest.TestLoader()
    # On cherche le dossier (ex: t_shop)
    start_dir = Path(__file__).parent / folder_name

    # Vérification que le dossier existe
    if not start_dir.exists():
        print(f"⚠️  Dossier de test introuvable : {folder_name}")
        return None

    # Découverte automatique : Il va trouver TOUS les fichiers commençant par 'test_'
    suite = loader.discover(start_dir, pattern='test_*.py')
    
    # Lancement des tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    return result

# ==========================================
# FONCTION PRINCIPALE
# ==========================================
if __name__ == "__main__":
    print("==================================================")
    print("   RAPPORT DE TEST AUTOMATISÉ - COOLDEAL")
    print("   Date : " + datetime.now().strftime("%d/%m/%Y à %H:%M"))
    print("==================================================")

    # 1. D'abord, on charge Django
    setup_django_environment()

    # 2. Ensuite, on lance les modules UN PAR UN
    
    # --- MODULE SHOP (Modèles + Vues + URLs) ---
    run_tests_in_folder("t_shop", "SHOP (Produits, Vues & URLs)")

    # --- MODULE WEBSITE (Configuration) ---
    run_tests_in_folder("t_website", "WEBSITE (Contenu & Pages)")

    # --- MODULE CUSTOMER (Auth, Panier, Coupons) ---
    run_tests_in_folder("t_customer", "CUSTOMER (Clients, Panier & Sécurité)")

    # --- MODULE CLIENT (Espace personnel) ---
    run_tests_in_folder("t_client", "CLIENT (Profil, Commandes)")

    # --- MODULE CONTACT (Formulaires) ---
    run_tests_in_folder("t_contact", "CONTACT (Messagerie, Newsletter)")

    # --- MODULE VALIDATION (Nouveau : Boundary Testing) ---
    run_tests_in_folder("t_validation", "VALIDATION & LIMITES (Tests Techniques)")

    print("\n" + "="*50)
    print("✅ FIN DE L'EXÉCUTION DE TOUS LES TESTS")
    print("="*50)