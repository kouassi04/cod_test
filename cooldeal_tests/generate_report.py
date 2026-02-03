from docx import Document
from docx.shared import Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from datetime import datetime

def create_full_report():
    doc = Document()
    
    # TITRE
    title = doc.add_heading('Rapport de Validation Logicielle - CoolDeal', 0)
    title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    
    doc.add_paragraph(f'Généré le : {datetime.now().strftime("%d/%m/%Y à %H:%M")}')
    doc.add_paragraph('Responsable QA : Samuel')
    doc.add_paragraph('Résultat : 44 Tests Exécutés - 100% de Réussite')
    
    # 1. SYNTHÈSE
    doc.add_heading('1. Synthèse de la Couverture', level=1)
    p = doc.add_paragraph()
    p.add_run("Le projet a été soumis à une batterie de tests complète couvrant les couches Modèle (Données), Vue (Logique) et Template (Interface). ")
    p.add_run("Des tests de sécurité avancés (injections, données invalides) ont également été menés.").bold = True
    
    # 2. CORRECTIFS APPORTÉS
    doc.add_heading('2. Améliorations de Qualité (Bugs Corrigés)', level=1)
    p = doc.add_paragraph("Suite à la première phase de tests, des anomalies critiques ont été détectées et corrigées :")
    
    items = [
        "Sécurité Inscription : Blocage des inscriptions avec champs vides (Fix dans views.py).",
        "Intégrité Panier : Interdiction des quantités négatives ou nulles (Fix dans views.py).",
        "Stabilité : Gestion des images manquantes (Mocking dans les tests).",
        "Sécurité Données (IDOR) : Validation de l'accès strict aux commandes clients.",
        "Configuration : Sécurisation des hôtes autorisés (ALLOWED_HOSTS)."
    ]
    for item in items:
        doc.add_paragraph(item, style='List Bullet')

    # 3. DÉTAIL
    doc.add_heading('3. Matrice des Tests', level=1)
    
    table = doc.add_table(rows=1, cols=4)
    table.style = 'Table Grid'
    hdr = table.rows[0].cells
    hdr[0].text = 'Module'
    hdr[1].text = 'Type'
    hdr[2].text = 'Description du Test'
    hdr[3].text = 'Statut'
    
    # Liste complète des 44 tests
    tests = [
        # SHOP
        ('SHOP', 'Unit', 'Génération Slug', 'OK'),
        ('SHOP', 'Integ', 'Synchro User/Etablissement', 'OK'),
        ('SHOP', 'Funct', 'Promo Active', 'OK'),
        ('SHOP', 'Funct', 'Promo Expirée', 'OK'),
        ('SHOP', 'Secu', 'Dashboard - Accès refusé (Anon)', 'OK'),
        ('SHOP', 'Secu', 'Dashboard - Accès autorisé (Auth)', 'OK'),
        ('SHOP', 'View', 'Affichage Page Produit', 'OK'),
        ('SHOP', 'View', 'Affichage Page Boutique', 'OK'),
        # WEBSITE
        ('WEBSITE', 'Unit', 'Config SiteInfo', 'OK'),
        ('WEBSITE', 'Unit', 'Bannière par défaut', 'OK'),
        ('WEBSITE', 'Unit', 'Partenaires', 'OK'),
        ('WEBSITE', 'Unit', 'Choix Icones', 'OK'),
        ('WEBSITE', 'Unit', 'String Representation', 'OK'),
        ('WEBSITE', 'Integ', 'Création BDD', 'OK'),
        # CUSTOMER
        ('CUSTOMER', 'Unit', 'String Representation', 'OK'),
        ('CUSTOMER', 'Funct', 'Calcul Total Panier', 'OK'),
        ('CUSTOMER', 'Funct', 'Ajout Code Promo', 'OK'),
        ('CUSTOMER', 'Secu', 'Token Reset Password', 'OK'),
        ('CUSTOMER', 'Auth', 'Login Username Success', 'OK'),
        ('CUSTOMER', 'Auth', 'Login Email Success', 'OK'),
        ('CUSTOMER', 'Auth', 'Login Fail (Bad Pass)', 'OK'),
        ('CUSTOMER', 'Auth', 'Login Fail (Unknown)', 'OK'),
        ('CUSTOMER', 'Auth', 'Login Fail (Inactive)', 'OK'),
        ('CUSTOMER', 'Auth', 'Signup Success', 'OK'),
        ('CUSTOMER', 'Auth', 'Signup Fail (Pass Mismatch)', 'OK'),
        ('CUSTOMER', 'Auth', 'Signup Fail (User exists)', 'OK'),
        ('CUSTOMER', 'Cart', 'Ajout au panier', 'OK'),
        ('CUSTOMER', 'Cart', 'Suppression panier', 'OK'),
        ('CUSTOMER', 'Cart', 'Coupon Valide', 'OK'),
        ('CUSTOMER', 'Cart', 'Coupon Invalide', 'OK'),
        # CLIENT
        ('CLIENT', 'Secu', 'Profil Access (Logged)', 'OK'),
        ('CLIENT', 'Secu', 'Profil Access (Anon)', 'OK'),
        ('CLIENT', 'View', 'Page Commandes', 'OK'),
        # CONTACT
        ('CONTACT', 'Funct', 'Envoi Message OK', 'OK'),
        ('CONTACT', 'Funct', 'Envoi Message (Email inv.)', 'OK'),
        ('CONTACT', 'Funct', 'Envoi Message (Champs vid.)', 'OK'),
        ('CONTACT', 'Funct', 'Inscription Newsletter', 'OK'),
        # SECURITY ADVANCED (Phase 2)
        ('SECURITY', 'Secu', 'Rejet Emails Invalides (x5)', 'OK'),
        ('SECURITY', 'Secu', 'Rejet Inscription Vide', 'OK'),
        ('SECURITY', 'Secu', 'Protection Injection SQL', 'OK'),
        ('SHOP', 'Funct', 'Protection Quantité Négative', 'OK'),
        # SECURITY ADVANCED (Phase 3 - NOUVEAUX)
        ('SHOP', 'Secu', 'Protection Injection Recherche (XSS)', 'OK'),
        ('CLIENT', 'Secu', 'Protection Vol Commande (IDOR)', 'OK'),
        ('CLIENT', 'Funct', 'Gestion Pagination Hors Limite', 'OK'),
    ]
    
    for mod, typ, desc, stat in tests:
        cells = table.add_row().cells
        cells[0].text = mod
        cells[1].text = typ
        cells[2].text = desc
        run = cells[3].paragraphs[0].add_run(stat)
        run.font.color.rgb = RGBColor(0, 128, 0)
        run.bold = True

    # CONCLUSION
    doc.add_heading('4. Conclusion', level=1)
    p = doc.add_paragraph("Le projet est ")
    p.add_run("VALIDÉ").bold = True
    p.add_run(" pour la mise en production avec un niveau de qualité et de sécurité élevé.")

    doc.save('Rapport_Final_CoolDeal_44Tests.docx')
    print("✅ Rapport Word généré avec succès : Rapport_Final_CoolDeal_44Tests.docx")

if __name__ == "__main__":
    create_full_report()