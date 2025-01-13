import tkinter as tk
from tkinter import messagebox
import os

class TextInputWindow:
    """Fenêtre pour taper ou coller le texte initial."""

    def __init__(self, root):
        self.root = root
        self.root.title("Étape 1 : Saisissez le texte")
        self.root.geometry("900x600")

        # Texte d'aide
        help_text = (
            "Instructions :\n\n"
            "1. Entrez ou collez votre texte dans la zone ci-dessous.\n"
            "2. Cliquez sur 'Suivant >>>' pour passer à l'étape suivante.\n"
            "3. À l'étape suivante, vous pourrez sélectionner et configurer des mots ou expressions.\n"
        )
        tk.Label(self.root, text=help_text, font=("Arial", 10), justify="left", wraplength=880).pack(pady=10)

        # Bouton pour passer à l'étape suivante
        next_button = tk.Button(self.root, text="Suivant >>>", command=self.next_step, font=("Arial", 12))
        next_button.pack(pady=10)

        # Zone de texte pour saisir le prompt
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
        self.root.geometry("900x600")

        self.prompt_content = prompt_content
        self.selected_blends = []  # Liste des sélections avec leurs configurations
        self.iterations = tk.IntVar(value=5)  # Nombre d'itérations par défaut

        # Texte d'aide
        help_text = (
            "Instructions :\n\n"
            "1. Sélectionnez un mot ou une expression avec la souris.\n"
            "2. Configurez le remplacement dans la fenêtre qui s'ouvre.\n"
            "3. Vous pouvez répéter pour plusieurs mots avant de cliquer sur 'Terminé'.\n"
        )
        tk.Label(self.root, text=help_text, font=("Arial", 10), justify="left", wraplength=880).pack(pady=10)

        # Zone de texte pour afficher et sélectionner les mots
        self.prompt_text = tk.Text(self.root, wrap="word", font=("Arial", 12))
        self.prompt_text.insert("1.0", self.prompt_content)
        self.prompt_text.pack(expand=True, fill="both", padx=10, pady=10)

        # Boutons en bas
        bottom_frame = tk.Frame(self.root)
        bottom_frame.pack(fill="x", padx=10, pady=5)
        tk.Label(bottom_frame, text="Nombre d'itérations :", font=("Arial", 10)).pack(side="left")
        tk.Entry(bottom_frame, textvariable=self.iterations, width=5).pack(side="left", padx=5)
        tk.Button(bottom_frame, text="Terminé", command=self.finish).pack(side="right")

        # Mise à jour des surbrillances
        self.update_highlights()

        # Gestion de la sélection de texte
        self.prompt_text.bind("<ButtonRelease-1>", self.select_text)

    def select_text(self, event):
        """Sélectionne un mot ou une phrase et ouvre une fenêtre de configuration."""
        try:
            start_idx = self.prompt_text.index("sel.first")
            end_idx = self.prompt_text.index("sel.last")
            selected_text = self.prompt_text.get(start_idx, end_idx).strip()

            if not selected_text:
                return

            # Vérifie si le mot est déjà sélectionné
            for entry in self.selected_blends:
                if entry['selection'] == selected_text:
                    messagebox.showinfo("Info", f"'{selected_text}' est déjà configuré.")
                    return

            self.configure_replacement(selected_text)

        except tk.TclError:
            pass  # Aucun texte sélectionné

    def configure_replacement(self, selected_text):
        """Fenêtre de configuration pour définir le blending."""
        config_window = tk.Toplevel(self.root)
        config_window.title("Configuration du remplacement")
        config_window.geometry("500x400")

        # Instructions
        tk.Label(config_window, text=f"Configuration pour '{selected_text}'", font=("Arial", 12)).pack(pady=10)
        tk.Label(config_window, text="Texte de remplacement :", font=("Arial", 10)).pack()
        replacement_entry = tk.Entry(config_window, width=30)
        replacement_entry.pack(pady=5)

        tk.Label(config_window, text="Valeur de début (%):", font=("Arial", 10)).pack()
        start_value = tk.IntVar(value=0)
        tk.Entry(config_window, textvariable=start_value, width=10).pack(pady=5)

        tk.Label(config_window, text="Valeur de fin (%):", font=("Arial", 10)).pack()
        end_value = tk.IntVar(value=100)
        tk.Entry(config_window, textvariable=end_value, width=10).pack(pady=5)

        direction = tk.StringVar(value="croissant")
        tk.Label(config_window, text="Sens du blending :", font=("Arial", 10)).pack()
        tk.Radiobutton(config_window, text="Croissant", variable=direction, value="croissant").pack()
        tk.Radiobutton(config_window, text="Décroissant", variable=direction, value="décroissant").pack()

        def save_configuration():
            replacement_text = replacement_entry.get().strip()
            if not replacement_text:
                messagebox.showerror("Erreur", "Le texte de remplacement ne peut pas être vide.")
                return

            self.selected_blends.append({
                "selection": selected_text,
                "replacement": replacement_text,
                "start": start_value.get() / 100,
                "end": end_value.get() / 100,
                "direction": direction.get(),
            })
            self.update_highlights()
            config_window.destroy()
            messagebox.showinfo("Succès", f"Blending ajouté : '{selected_text}' -> '{replacement_text}'")

        tk.Button(config_window, text="Valider", command=save_configuration).pack(pady=20)

    def update_highlights(self):
        """Surligne les mots sélectionnés en rouge."""
        self.prompt_text.tag_remove("highlight", "1.0", "end")
        for entry in self.selected_blends:
            selection = entry['selection']
            start_idx = "1.0"
            while True:
                start_idx = self.prompt_text.search(selection, start_idx, stopindex="end")
                if not start_idx:
                    break
                end_idx = f"{start_idx}+{len(selection)}c"
                self.prompt_text.tag_add("highlight", start_idx, end_idx)
                start_idx = end_idx
        self.prompt_text.tag_config("highlight", foreground="red")

    def get_unique_filename(self, base_name="generated_prompts", extension=".txt"):
        """Génère un nom de fichier unique avec un numéro croissant."""
        counter = 0
        while True:
            file_name = f"{base_name}{'_' + str(counter) if counter > 0 else ''}{extension}"
            if not os.path.exists(file_name):
                return file_name
            counter += 1

    def finish(self):
        """Génère un fichier texte avec les prompts modifiés."""
        if not self.selected_blends:
            messagebox.showwarning("Attention", "Aucune sélection n'a été configurée.")
            return

        # Obtenir un nom de fichier unique
        file_name = self.get_unique_filename()

        # Générer les prompts avec les modifications appliquées
        with open(file_name, "w") as file:
            file.write("Prompt initial :\n")
            file.write(self.prompt_content + "\n\nPrompts générés :\n")

            # Appliquer chaque sélection au texte initial
            for i in range(self.iterations.get()):
                factor_step = i / (self.iterations.get() - 1)  # Calcul du facteur progressif
                modified_prompt = self.prompt_content

                # Remplacer chaque mot ou expression avec blending
                for entry in self.selected_blends:
                    selection = entry['selection']
                    replacement = entry['replacement']
                    start = entry['start']
                    end = entry['end']
                    direction = entry['direction']

                    # Calculer le facteur de blending
                    factor = start + (end - start) * factor_step
                    if direction == "décroissant":
                        factor = end - (factor - start)

                    # Appliquer le remplacement dans le texte
                    blended_text = f"[{selection} : {replacement} : {round(factor, 2)}]"
                    modified_prompt = modified_prompt.replace(selection, blended_text)

                # Écrire le prompt modifié dans le fichier
                file.write(modified_prompt + "\n")

        messagebox.showinfo("Succès", f"Fichier généré : {file_name}")
        self.root.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = TextInputWindow(root)
    root.mainloop()
