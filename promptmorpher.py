import tkinter as tk
from tkinter import messagebox


class TextInputWindow:
    """Fenêtre pour taper ou coller le texte initial."""

    def __init__(self, root):
        self.root = root
        self.root.title("Étape 1 : Saisissez le texte")
        self.root.geometry("900x600")  # Taille ajustée pour plus de confort

        # Texte d'aide
        help_text = (
            "Instructions :\n\n"
            "1. Entrez ou collez votre texte dans la zone ci-dessous.\n"
            "2. Une fois prêt, cliquez sur le bouton 'Suivant >>>' pour passer à l'étape suivante.\n"
            "3. À l'étape suivante, vous pourrez sélectionner des mots ou des expressions pour les configurer.\n"
        )
        tk.Label(self.root, text=help_text, font=("Arial", 10), justify="left", wraplength=880).pack(pady=10)

        # Bouton pour passer à l'étape suivante (placé en haut)
        next_button = tk.Button(self.root, text="Suivant >>>", command=self.next_step, font=("Arial", 12))
        next_button.pack(pady=10)

        # Champ de texte pour entrer le prompt
        self.prompt_text = tk.Text(self.root, wrap="word", font=("Arial", 12))
        self.prompt_text.pack(expand=True, fill="both", padx=10, pady=10)
        self.prompt_text.insert("1.0", "Entrez ou collez votre texte ici.")

    def next_step(self):
        """Passe à l'étape suivante pour sélectionner les mots."""
        prompt_content = self.prompt_text.get("1.0", "end").strip()
        if not prompt_content:
            messagebox.showerror("Erreur", "Le texte ne peut pas être vide.")
            return

        # Ouvrir la fenêtre suivante
        self.root.destroy()
        root = tk.Tk()
        WordSelectionWindow(root, prompt_content)


class WordSelectionWindow:
    """Fenêtre pour sélectionner les mots ou groupes de mots et définir le blending."""

    def __init__(self, root, prompt_content):
        self.root = root
        self.root.title("Étape 2 : Sélectionnez les mots ou groupes de mots")
        self.root.geometry("900x600")  # Taille ajustée pour plus de confort

        self.prompt_content = prompt_content
        self.selected_blends = []  # Liste des sélections avec leurs configurations
        self.iterations = tk.IntVar(value=5)  # Nombre d'itérations par défaut

        # Texte d'aide
        help_text = (
            "Instructions :\n\n"
            "1. Sélectionnez un mot ou une expression en maintenant le clic gauche de la souris "
            "et en surlignant le mot ou l'expression souhaité(e).\n"
            "2. Relâchez la souris pour afficher une fenêtre où vous pourrez configurer le remplacement.\n"
            "3. Vous pouvez configurer plusieurs remplacements avant de cliquer sur 'Terminé' pour générer le fichier.\n"
        )
        tk.Label(self.root, text=help_text, font=("Arial", 10), justify="left", wraplength=880).pack(pady=10)

        # Champ de texte modifiable pour afficher et sélectionner le prompt
        self.prompt_text = tk.Text(self.root, wrap="word", font=("Arial", 12))
        self.prompt_text.insert("1.0", self.prompt_content)
        self.prompt_text.pack(expand=True, fill="both", padx=10, pady=10)

        # Formulaire pour itérations et bouton "Terminé"
        bottom_frame = tk.Frame(self.root)
        bottom_frame.pack(fill="x", padx=10, pady=5)

        tk.Label(bottom_frame, text="Nombre d'itérations (par défaut : 5) :", font=("Arial", 10)).pack(side="left")
        tk.Entry(bottom_frame, textvariable=self.iterations, width=5).pack(side="left", padx=5)

        tk.Button(bottom_frame, text="Terminé", command=self.finish).pack(side="right")

        # Marquer les sélections déjà faites
        self.update_highlights()

        # Associer un événement pour la sélection de texte
        self.prompt_text.bind("<ButtonRelease-1>", self.select_text)

    def select_text(self, event):
        """Permet de sélectionner un groupe de mots et de configurer un blending."""
        try:
            # Obtenir la sélection actuelle
            start_idx = self.prompt_text.index("sel.first")
            end_idx = self.prompt_text.index("sel.last")
            selected_text = self.prompt_text.get(start_idx, end_idx).strip()

            # Vérifier si une sélection valide est faite
            if not selected_text:
                return

            # Si la sélection a déjà été modifiée
            for entry in self.selected_blends:
                if entry['selection'] == selected_text:
                    messagebox.showinfo("Information", f"'{selected_text}' a déjà été modifié.")
                    return

            # Ouvrir la fenêtre de configuration
            self.configure_replacement(selected_text)

        except tk.TclError:
            # Aucune sélection n'a été faite
            pass

    def configure_replacement(self, selected_text):
        """Fenêtre pour configurer le remplacement et les paramètres de blending."""
        config_window = tk.Toplevel(self.root)
        config_window.title("Configuration du remplacement")
        config_window.geometry("500x500")  # Taille ajustée pour la configuration

        # Texte d'aide
        help_text = (
            f"Configuration pour : '{selected_text}'\n\n"
            "1. Entrez le texte de remplacement.\n"
            "2. Configurez les valeurs de début et de fin en pourcentage (par défaut : 0% à 100%).\n"
            "3. Sélectionnez le sens du blending : croissant ou décroissant.\n"
            "4. Cliquez sur 'Valider' pour sauvegarder la configuration."
        )
        tk.Label(config_window, text=help_text, font=("Arial", 10), justify="left", wraplength=480).pack(pady=10)

        # Champ pour le remplacement
        tk.Label(config_window, text="Texte de remplacement :", font=("Arial", 10)).pack()
        replacement_entry = tk.Entry(config_window, width=30)
        replacement_entry.pack(pady=5)

        # Valeur de début
        tk.Label(config_window, text="Valeur de début en pourcent :", font=("Arial", 10)).pack()
        start_value = tk.IntVar(value=0)
        start_entry = tk.Entry(config_window, textvariable=start_value, width=10)
        start_entry.pack(pady=5)

        # Valeur de fin
        tk.Label(config_window, text="Valeur de fin en pourcent :", font=("Arial", 10)).pack()
        end_value = tk.IntVar(value=100)
        end_entry = tk.Entry(config_window, textvariable=end_value, width=10)
        end_entry.pack(pady=5)

        # Sens du blending
        blending_direction = tk.StringVar(value="croissant")
        tk.Label(config_window, text="Sens du blending :", font=("Arial", 10)).pack()
        tk.Radiobutton(config_window, text="Croissant", variable=blending_direction, value="croissant").pack()
        tk.Radiobutton(config_window, text="Décroissant", variable=blending_direction, value="décroissant").pack()

        # Bouton pour valider
        def save_configuration():
            replacement_text = replacement_entry.get().strip()
            if not replacement_text:
                messagebox.showerror("Erreur", "Le texte de remplacement ne peut pas être vide.")
                return

            # Ajouter la configuration sans modifier le texte
            self.selected_blends.append({
                "selection": selected_text,
                "replacement": replacement_text,
                "start": start_value.get() / 100,  # Convertir en valeur décimale
                "end": end_value.get() / 100,    # Convertir en valeur décimale
                "direction": blending_direction.get()
            })

            # Mettre à jour les surbrillances après validation
            self.update_highlights()

            config_window.destroy()
            messagebox.showinfo("Succès", f"Blending ajouté : {selected_text} -> {replacement_text}")

        tk.Button(config_window, text="Valider", command=save_configuration).pack(pady=20)

    def update_highlights(self):
        """Mettre à jour les sélections en rouge dans le texte."""
        self.prompt_text.tag_remove("highlight", "1.0", "end")  # Supprimer les anciennes surbrillances
        for entry in self.selected_blends:
            selection = entry['selection']
            start_idx = "1.0"
            while True:
                start_idx = self.prompt_text.search(selection, start_idx, stopindex="end", nocase=False)
                if not start_idx:
                    break
                end_idx = f"{start_idx}+{len(selection)}c"
                self.prompt_text.tag_add("highlight", start_idx, end_idx)
                start_idx = end_idx
        self.prompt_text.tag_config("highlight", foreground="red")

    def finish(self):
        """Génère un fichier texte avec les prompts modifiés."""
        if not self.selected_blends:
            messagebox.showwarning("Avertissement", "Aucun mot ou groupe de mots n'a été sélectionné.")
            return

        num_iterations = self.iterations.get()
        if num_iterations < 1:
            messagebox.showerror("Erreur", "Le nombre d'itérations doit être supérieur à 0.")
            return

        # Générer le fichier de résultats
        with open("stable_diffusion_blending_prompts.txt", "w") as file:
            file.write("Prompt initial:\n")
            file.write(self.prompt_content + "\n\n")
            file.write("Prompts générés avec keyword blending:\n")

            # Appliquer les transitions cumulatives pour toutes les sélections
            for i in range(num_iterations):
                factor_step = i / (num_iterations - 1)
                blended_prompt = self.prompt_content

                for entry in self.selected_blends:
                    start = entry['start']
                    end = entry['end']
                    direction = entry['direction']
                    selection = entry['selection']
                    replacement = entry['replacement']

                    # Calculer le facteur en fonction du sens
                    factor = start + (end - start) * factor_step
                    if direction == "décroissant":
                        factor = end - (factor - start)

                    blended_prompt = blended_prompt.replace(
                        selection, f"[{selection} : {replacement} : {round(factor, 2)}]"
                    )

                file.write(f"{blended_prompt}\n")

        messagebox.showinfo("Succès", "Le fichier de blending a été généré : stable_diffusion_blending_prompts.txt")
        self.root.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = TextInputWindow(root)
    root.mainloop()
