import tkinter as tk
from tkinter import ttk, simpledialog
import mysql.connector

class StoreManager:

    def __init__(self, root):
        self.root = root
        self.root.title("Gestion de Stock")
        
        # Établir la connexion à la base de données
        self.conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="002003",
            database="store"
        )
        self.cursor = self.conn.cursor()

        # Création de l'interface graphique
        self.create_widgets()

    def create_widgets(self):
        # Treeview pour afficher la liste des produits
        self.tree = ttk.Treeview(self.root, columns=("ID", "Nom", "Description", "Prix", "Quantité", "Catégorie"))
        self.tree.heading("#0", text="ID")
        self.tree.heading("#1", text="Nom")
        self.tree.heading("#2", text="Description")
        self.tree.heading("#3", text="Prix")
        self.tree.heading("#4", text="Quantité")
        self.tree.heading("#5", text="Catégorie")

        # Ajuster la largeur des colonnes
        self.tree.column("#0", width=50)  # ID
        self.tree.column("#1", width=100)  # Nom
        self.tree.column("#2", width=200)  # Description
        self.tree.column("#3", width=80)  # Prix
        self.tree.column("#4", width=80)  # Quantité
        self.tree.column("#5", width=100)  # Catégorie

        self.tree.pack(pady=10)

        # Boutons pour les actions
        btn_frame = tk.Frame(self.root)
        btn_frame.pack(pady=10)

        add_btn = tk.Button(btn_frame, text="Ajouter Produit", command=self.add_product)
        add_btn.grid(row=0, column=0, padx=5)

        remove_btn = tk.Button(btn_frame, text="Supprimer Produit", command=self.remove_product)
        remove_btn.grid(row=0, column=1, padx=5)

        update_btn = tk.Button(btn_frame, text="Modifier Produit", command=self.update_product)
        update_btn.grid(row=0, column=2, padx=5)

        # Charger la liste des produits
        self.load_products()

    def load_products(self):
        # Effacer les éléments existants dans le Treeview
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Récupérer la liste des produits depuis la base de données
        query = "SELECT product.id, product.name, product.description, product.price, product.quantity, category.name " \
                "FROM product JOIN category ON product.id_category = category.id"
        self.cursor.execute(query)
        products = self.cursor.fetchall()

        # Ajouter les produits au Treeview
        for product in products:
            self.tree.insert("", "end", values=(product[0], product[1], product[2], product[3], product[4], product[5]))

    def add_product(self):
        # Initialiser selected_category à None
        selected_category = None

        # Boîte de dialogue pour saisir les informations du produit
        product_name = simpledialog.askstring("Ajouter Produit", "Nom du produit:")
        
        if not product_name:
            # Si le nom du produit est vide, annuler l'ajout
            return

        # Saisir d'autres informations du produit
        description = simpledialog.askstring("Ajouter Produit", "Description du produit:")
        price = simpledialog.askinteger("Ajouter Produit", "Prix du produit:")
        quantity = simpledialog.askinteger("Ajouter Produit", "Quantité du produit:")

        # Récupérer la liste des catégories
        category_query = "SELECT id, name FROM category"
        self.cursor.execute(category_query)
        categories = self.cursor.fetchall()

        # Boîte de dialogue pour choisir la catégorie
        category_names = [category[1] for category in categories]
        category_names.append("Nouvelle catégorie")

        # Utiliser une boîte de dialogue Toplevel personnalisée pour afficher la liste des catégories
        category_dialog = tk.Toplevel(self.root)
        category_dialog.title("Choisir la catégorie")

        listbox = tk.Listbox(category_dialog, selectmode=tk.SINGLE)
        for category in category_names:
            listbox.insert(tk.END, category)
        listbox.pack(padx=10, pady=10)

        def on_ok():
            nonlocal selected_category
            selected_category = listbox.get(listbox.curselection())
            category_dialog.destroy()

            if selected_category == "Nouvelle catégorie":
                # Si l'utilisateur choisit "Nouvelle catégorie", demandez-lui de saisir le nom
                new_category_name = simpledialog.askstring("Ajouter Produit", "Nom de la nouvelle catégorie:")
                
                if not new_category_name:
                    # Si le nom de la nouvelle catégorie est vide, annuler l'ajout
                    return

                # Insérer la nouvelle catégorie dans la base de données
                insert_category_query = "INSERT INTO category (name) VALUES (%s)"
                self.cursor.execute(insert_category_query, (new_category_name,))
                self.conn.commit()

        ok_button = tk.Button(category_dialog, text="OK", command=on_ok)
        ok_button.pack(pady=10)

        category_dialog.wait_window()

        if not selected_category:
            # Si aucune catégorie n'a été sélectionnée, annuler l'ajout
            return

        # Récupérer l'ID de la catégorie sélectionnée
        category_id = next(category[0] for category in categories if category[1] == selected_category)

        # Insérer le produit dans la base de données
        insert_query = "INSERT INTO product (name, description, price, quantity, id_category) " \
                    "VALUES (%s, %s, %s, %s, %s)"
        values = (product_name, description, price, quantity, category_id)
        self.cursor.execute(insert_query, values)
        self.conn.commit()

        # Recharger la liste des produits
        self.load_products()    
                                                
    def remove_product(self):
        # Boîte de dialogue pour saisir l'ID du produit à supprimer
        product_id = simpledialog.askinteger("Supprimer Produit", "ID du produit à supprimer:")

        if product_id:
            # Supprimer le produit de la base de données
            delete_query = "DELETE FROM product WHERE id = %s"
            values = (product_id,)
            self.cursor.execute(delete_query, values)
            self.conn.commit()

            # Recharger la liste des produits
            self.load_products()

    def update_product(self):
        # Boîte de dialogue pour saisir l'ID du produit à mettre à jour
        product_id = simpledialog.askinteger("Modifier Produit", "ID du produit à modifier:")

        if product_id:
            # Saisir les nouvelles informations du produit
            description = simpledialog.askstring("Modifier Produit", "Nouvelle description du produit:")
            price = simpledialog.askinteger("Modifier Produit", "Nouveau prix du produit:")
            quantity = simpledialog.askinteger("Modifier Produit", "Nouvelle quantité du produit:")
            
            # Boîte de dialogue pour choisir la nouvelle catégorie
            category_query = "SELECT id, name FROM category"
            self.cursor.execute(category_query)
            categories = self.cursor.fetchall()
            category_names = [category[1] for category in categories]
            selected_category = simpledialog.askstring("Modifier Produit", "Choisir la nouvelle catégorie:", 
                                                    initialvalue=category_names[0], 
                                                    listvalues=category_names)

            if selected_category:
                # Récupérer l'ID de la nouvelle catégorie sélectionnée
                category_id = next(category[0] for category in categories if category[1] == selected_category)

                # Mettre à jour le produit dans la base de données
                update_query = "UPDATE product SET description = %s, price = %s, quantity = %s, id_category = %s " \
                            "WHERE id = %s"
                values = (description, price, quantity, category_id, product_id)
                self.cursor.execute(update_query, values)
                self.conn.commit()

                # Recharger la liste des produits
                self.load_products()


if __name__ == "__main__":
    root = tk.Tk()
    app = StoreManager(root)
    root.mainloop()
