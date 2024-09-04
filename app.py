from flask import Flask, request, render_template, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///budget.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Budget(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return f"Budget : {self.name}"

class Depense(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titre = db.Column(db.String(100), nullable=False)
    montant = db.Column(db.Float, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow) 

    def __init__(self, titre, montant):
        self.titre = titre
        self.montant = montant


@app.route("/ajoutDepense", methods=["GET", "POST"])
def ajout_depense():
    if request.method == "POST":
        titre = request.form['titre']
        montant = request.form['montant']
        
        new_depense = Depense(titre=titre, montant=float(montant))
        try:
            db.session.add(new_depense)
            db.session.commit()
            return redirect('/')
        except Exception as e:
            print(e)
            return "Error"

    return render_template("ajout_depense.html")

class Revenu(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titre = db.Column(db.String(100), nullable=False)
    montant = db.Column(db.Float, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow) 

    def __init__(self, titre, montant):
        self.titre = titre
        self.montant = montant


@app.route("/ajoutRevenus", methods=["GET", "POST"])
def ajout_revenus():
    if request.method == "POST":
        titre = request.form['titre']
        montant = request.form['montant']
        
        new_revenu = Revenu(titre=titre, montant=float(montant))
        try:
            db.session.add(new_revenu)
            db.session.commit()
            return redirect('/')
        except Exception as e:
            print(e)
            return "Error"
    return render_template("ajout_revenu.html")


@app.route("/", methods=["GET", "POST"])
def index():
    budgets = Budget.query.order_by(Budget.created_at).all()
    if request.method == "POST":
        name = request.form.get('budget')
        if name:
            new_budget = Budget(name=name)
            try:
                db.session.add(new_budget)
                db.session.commit()
                return redirect('/')
            except Exception as e:
                print(e)
                return "Error"
    else:
        depenses = Depense.query.all()  
        revenus = Revenu.query.all()
        return render_template("index.html", budgets=budgets, depenses=depenses, revenus=revenus) 
        
@app.route("/delete_depense/<int:id>/")
def delete_depense(id):
    depense = Depense.query.get_or_404(id)
    try:
        db.session.delete(depense)
        db.session.commit()
        return redirect('/')
    except Exception:
        return "Error "

@app.route("/delete_revenu/<int:id>/")
def delete_revenu(id):
    revenu = Revenu.query.get_or_404(id)
    try:
        db.session.delete(revenu)
        db.session.commit()
        return redirect('/')
    except Exception:
        return "Error"



@app.route("/update/<int:id>/", methods=["GET", "POST"])
def update(id):
    depense = Depense.query.get_or_404(id)
    if request.method == "POST":
        depense.titre = request.form.get('name')  # Récupère la valeur du champ du formulaire
        try:
            db.session.commit()
            return redirect('/')
        except Exception as e:
            return "Error: " + str(e)  # Affiche l'erreur si une exception se produit
    else:
        title = "Mise à jour de la Dépense"
        return render_template("update_depense.html", title=title, depense=depense)

            

    

    

@app.route("/about/")
def about():
    return render_template("about.html")


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=8000)
