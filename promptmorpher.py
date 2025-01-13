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
