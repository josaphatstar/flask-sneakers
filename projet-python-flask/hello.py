from flask import (
    Flask,
    g,
    redirect,
    render_template,
    app,
    request,
    session,
    url_for
)
import sqlite3
import os
listProduits = []
users = []

class User:
        def __init__(self, id, username, password):
            self.id = id
            self.username = username
            self.password = password

        def __repr__(self):
            return f'<User: {self.username}>'
def create_app():

    
    users = []
    users.append(User(id=1, username='josaphat', password='josaphat'))
    users.append(User(id=2, username='user', password='1234'))
    users.append(User(id=3, username='admin', password='root'))

    # Class Produit + implementation
    class Produit:
        def __init__(self, id, code, marque, modele, coloris, prix, image):
            self.id = id
            self.code = code
            self.marque = marque
            self.modele = modele
            self.coloris = coloris
            self.prix = prix
            self.image = image

        def __repr__(self):
            return f'<Produit: {self.code}>'

    listProduits.append(
        Produit(id=1, code='SNKRS-001', marque='Nike', modele='Vaporwaffle Sacai', coloris='Black White', prix=570,
                image='Nike-Sacai-Vaporwaffle-black-white.png'))
    listProduits.append(
        Produit(id=2, code='SNKRS-002', marque='Nike', modele='Vaporwaffle Sacai', coloris='Sport Fuchsia Game Royal',
                prix=590, image='Nike-Sacai-VaporWaffle-Game-Royal-Fuchsia.png'))
    listProduits.append(
        Produit(id=3, code='SNKRS-003', marque='Nike', modele='Vaporwaffle Sacai', coloris='Tour Yellow Stadium Green',
                prix=490, image='Nike-Sacai-VaporWaffle-Tour-Yellow-Stadium-Green.png'))
    listProduits.append(
        Produit(id=4, code='SNKRS-004', marque='Nike', modele='Vaporwaffle Sacai', coloris='Villain Red Neptune Green',
                prix=510, image='Nike-Sacai-Vaporwaffle-Villain-Red-Neptune-Green.png'))

    listProduits.append(Produit(id=5, code='SNKRS-005', marque='Nike', modele='Air Jordan 1 Retro High Travis Scott',
                                coloris='Cactus Jack', prix=1520, image='Air-Jordan-1-Cactus-Jack-Travis-Scott.webp'))
    listProduits.append(
        Produit(id=6, code='SNKRS-006', marque='Nike', modele='Air Jordan 1 Retro High Off-White', coloris='NRG White',
                prix=2370, image='Air-Jordan-1-Retro-High-Off-White-The-Ten-NRJ.webp'))
    listProduits.append(
        Produit(id=7, code='SNKRS-007', marque='Nike', modele='Air Jordan 1 Retro High', coloris='UNC Patent', prix=730,
                image='Air-Jordan-1-Retro-High-UNC-Patent.webp'))
    listProduits.append(
        Produit(id=8, code='SNKRS-008', marque='Nike', modele='Air Jordan 1 Retro High', coloris='Fearless OG',
                prix=460, image='Air-Jordan-1-Retro-High-OG-Fearless.webp'))

    listProduits.append(
        Produit(id=9, code='SNKRS-009', marque='Adidas', modele='Yeezy Boost 350 V2', coloris='Tail Light', prix=380,
                image='Adidas-Yeezy-Boost-350-V2-Tail-Light.png'))
    listProduits.append(
        Produit(id=10, code='SNKRS-010', marque='Adidas', modele='Yeezy Boost 350 V2', coloris='Natural', prix=310,
                image='Adidas-Yeezy-350-V2-Natural.png'))
    listProduits.append(
        Produit(id=11, code='SNKRS-010', marque='Adidas', modele='Yeezy Boost 350 V2', coloris='Cinder', prix=390,
                image='Adidas-Yeezy-350-V2-Cinder.png'))
    listProduits.append(
        Produit(id=12, code='SNKRS-010', marque='Adidas', modele='Yeezy Boost 350 V2', coloris='Zebra', prix=420,
                image='Adidas-Yeezy-Boost-350-V2-Zebra.png'))

    listPanier = []

    app = Flask(__name__)
    app.secret_key = 'somesecretkey'

    @app.before_request
    def before_request():
       
        g.user = None
        if 'user_id' in session:
          
            user = next((x for x in users if x.id == session['user_id']), None)
            if user:
                g.user = user

            g.user = user

            

   
    @app.route('/')
    def defaultPage():
        return render_template("mon_acceuil.html")
    
       
    @app.route('/Inscription', methods=['GET', 'POST'])
    def Inscription():
        return render_template("view_Inscription.html")
    
    @app.route("/traitement", methods=['GET', 'POST'])
    def traitement ():
        donnee = request.form
        username = donnee.get("username")
        password = donnee.get("password")

        existing_user = next((user for user in users if user.username == username), None)


        if existing_user:
            return render_template("view_user_exists.html")  
        else:
           
            new_user = User(id=len(users) + 1, username=username, password=password)
            users.append(new_user)
        return redirect(url_for('connexion'))
    

    @app.route("/addproduit", methods=['GET', 'POST'])
    def admin():
       return render_template("addproduit.html")

    @app.route("/traitement_admin",methods=['GET','POST'])
    def traitement_admin():
        # Récupérer les données du formulaire
        id = request.form['id']
        code = request.form['code']
        marque = request.form['marque']
        modele = request.form['modele']
        coloris = request.form['coloris']
        prix = request.form['prix']
        image = request.form['image']  # À vérifier s'il s'agit bien d'un fichier image, si oui, vous devrez utiliser request.files

        nouveau_produit = Produit(id=id, code=code, marque=marque, modele=modele, coloris=coloris, prix=prix, image=image)

        # Ajouter le nouveau produit à la liste listProduits
        listProduits.append(nouveau_produit)

        # Rediriger vers une autre page ou afficher un message de confirmation
        return "Produit ajouté avec succès !"
    
    @app.route("/admin_page")
    def admin_page():
        return render_template("admin_page.html", listProduits=listProduits)


    
    @app.route("/supprimer_produit", methods=['POST'])
    def supprimer_produit():
        produit_id = request.form['produit_id']
        # Convertir l'ID du produit en entier (si nécessaire)
        produit_id = int(produit_id)
        
        # Supprimer le produit de la liste listProduits
        for produit in listProduits:
            if produit.id == produit_id:
                listProduits.remove(produit)
                break  # Arrêtez la boucle une fois que le produit est supprimé

        # Rediriger vers la page d'administration après la suppression
        return redirect(url_for('admin_page'))

    from flask import request

    @app.route("/modifier_produit/<produit_id>", methods=['GET', 'POST'])
    def modifier_produit(produit_id):
        # Récupérer le produit à modifier en fonction de son ID
        produit = None
        for p in listProduits:
            if p.id == int(produit_id):
                produit = p
                break

        if produit is None:
            # Gérer le cas où le produit n'existe pas
            return render_template("404.html")

        if request.method == 'POST':
            # Mettre à jour les informations du produit avec les nouvelles données du formulaire
            produit.code = request.form['code']
            produit.marque = request.form['marque']
            produit.modele = request.form['modele']
            produit.coloris = request.form['coloris']
            produit.prix = float(request.form['prix'])  # Convertir en float si nécessaire

            # Rediriger vers la page de détails du produit après la modification
            return redirect(url_for('produit', produit_id=produit.id))

        # Afficher le formulaire de modification avec les informations actuelles du produit
        return render_template("modifier_produit.html", produit=produit)


    @app.route('/connexion', methods=['GET', 'POST'])
    def connexion():
        if request.method == 'POST':
            session.pop('user_id', None)

            result = request.form
            username = result['username']
            password = result['password']

            user = [x for x in users if x.username == username][0]
            
            if user and user.password == password:
                session['user_id'] = user.id
                if username == 'admin' and password == 'root':
                    return redirect(url_for('admin_page'))
                else:
                    return redirect(url_for('produit'))

            return redirect(url_for('connexion'))

        return render_template("view_connexion.html")

    @app.route('/deconnexion')
    def deconnexion():
        session.clear()
       
        listPanier.clear()
        return redirect(url_for('connexion'))

    @app.route('/produit')
    def produit():
        if not g.user:
            return redirect(url_for('connexion'))

        return render_template("view_produit.html", listProduits=listProduits, listPanier=listPanier)

    @app.route('/addPanier', methods=['GET', 'POST'])
    def addPanier():
       
        if not g.user:
            return redirect(url_for('connexion'))

        if request.method == 'POST':
            
            result = request.form
            unProduit = result['produitCode']
            leProduit = [x for x in listProduits if x.code == unProduit][0]
       
            listPanier.append(leProduit)
            return render_template("view_panier.html", listPanier=listPanier)

        return render_template("view_panier.html", listPanier=listPanier)

  
    @app.route('/delPanier', methods=['GET', 'POST'])
    def delPanier():
      
        if not g.user:
            return redirect(url_for('connexion'))

        if request.method == 'POST':
          
            result = request.form
            unProduit = result['produitCode']
            leProduit = [x for x in listProduits if x.code == unProduit][0]
           
            listPanier.remove(leProduit)
            return render_template("view_panier.html", listPanier=listPanier)

        return render_template("view_panier.html", listPanier=listPanier)

    
    @app.route('/addCommande', methods=['GET', 'POST'])
    def addCommande():
        
        if not g.user:
            return redirect(url_for('connexion'))

        if request.method == 'POST':
            
            listPanier.clear()
            return render_template("view_confirmationCommande.html")

        return render_template("view_panier.html", listPanier=listPanier)


    @app.route('/panier')
    def panier():
       
        if not g.user:
            return redirect(url_for('connexion'))
        return render_template("view_panier.html", listPanier=listPanier)


    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('404.html'), 404

    return app