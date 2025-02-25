import threading
import time
from mod_editor import ModEditorApp, FileManager, VersionManager, TemplateManager
# Ensure that mod_editor.py (which contains ModEditorApp, FileManager, VersionManager, TemplateManager)
# is in your PYTHONPATH.
import sys

class EditorAPI:
    """
    Expanded EditorAPI provides a full programmatic interface to control the Enhanced Mod Editor.

    Features:
      • Launch the editor in a separate thread.
      • Create new mod workspaces.
      • Open and save mod projects.
      • Retrieve and update code in the UI Code, Mod Logic, and Config tabs.
      • Preview the mod UI.
      • Check for version updates.
      • Get or set the mod name.
      • Insert toolbox snippets into a target code tab.
      • Retrieve available snippet keys.
      • Get and clear the console output.
      • Switch tabs and close the editor.
    """

    def __init__(self):
        self.app = None
        self.thread = None

    def launch_editor(self):
        """
        Launches the Enhanced Mod Editor in a separate daemon thread.
        """
        if self.app is None:
            self.thread = threading.Thread(target=self._run_editor, daemon=True)
            self.thread.start()
            # Allow time for the GUI to initialize
            time.sleep(1)
        else:
            raise Exception("Editor is already running.")

    def _run_editor(self):
        self.app = ModEditorApp()
        self.app.mainloop()

    def new_mod(self):
        """
        Resets the workspace to the default templates.
        """
        if self.app:
            self.app.after(0, lambda: FileManager.new_mod(self.app))
        else:
            raise Exception("Editor is not running.")

    def open_mod(self):
        """
        Opens an existing mod project (prompts the user with a directory dialog).
        """
        if self.app:
            self.app.after(0, lambda: FileManager.open_mod(self.app))
        else:
            raise Exception("Editor is not running.")

    def save_mod(self):
        """
        Saves the current mod project to its designated location.
        """
        if self.app:
            self.app.after(0, lambda: FileManager.save_mod(self.app))
        else:
            raise Exception("Editor is not running.")

    def save_mod_as(self):
        """
        Saves the current mod project to a new location (user prompted).
        """
        if self.app:
            self.app.after(0, lambda: FileManager.save_mod_as(self.app))
        else:
            raise Exception("Editor is not running.")

    def get_ui_code(self):
        """
        Retrieves the contents of the UI Code tab.
        
        Returns:
            str: The current UI code.
        """
        if self.app:
            return self.app.ui_code_text.get("0.0", "end-1c")
        raise Exception("Editor is not running.")

    def set_ui_code(self, code):
        """
        Replaces the UI Code tab's content with the provided code.
        
        Args:
            code (str): The new UI code.
        """
        if self.app:
            self.app.ui_code_text.delete("0.0", "end")
            self.app.ui_code_text.insert("0.0", code)
        else:
            raise Exception("Editor is not running.")

    def get_mod_logic_code(self):
        """
        Retrieves the contents of the Mod Logic tab.
        
        Returns:
            str: The current mod logic code.
        """
        if self.app:
            return self.app.mod_code_text.get("0.0", "end-1c")
        raise Exception("Editor is not running.")

    def set_mod_logic_code(self, code):
        """
        Replaces the Mod Logic tab's content with the provided code.
        
        Args:
            code (str): The new mod logic code.
        """
        if self.app:
            self.app.mod_code_text.delete("0.0", "end")
            self.app.mod_code_text.insert("0.0", code)
        else:
            raise Exception("Editor is not running.")

    def get_config(self):
        """
        Retrieves the JSON configuration from the Config tab.
        
        Returns:
            str: The configuration as a JSON string.
        """
        if self.app:
            return self.app.config_text.get("0.0", "end-1c")
        raise Exception("Editor is not running.")

    def set_config(self, config):
        """
        Replaces the contents of the Config tab with the provided configuration.
        
        Args:
            config (str): The new configuration as a JSON string.
        """
        if self.app:
            self.app.config_text.delete("0.0", "end")
            self.app.config_text.insert("0.0", config)
        else:
            raise Exception("Editor is not running.")

    def preview_ui(self):
        """
        Executes the UI Code tab to launch a preview window.
        """
        if self.app:
            self.app.after(0, self.app.preview_mod_ui)
        else:
            raise Exception("Editor is not running.")

    def check_version(self):
        """
        Checks for version updates by comparing the server version with the local version.
        """
        if self.app:
            self.app.after(0, lambda: VersionManager.check_version(self.app.console_print))
        else:
            raise Exception("Editor is not running.")

    # Expanded API Methods

    def get_mod_name(self):
        """
        Retrieves the current mod name.
        
        Returns:
            str: The mod name.
        """
        if self.app:
            return self.app.mod_name_var.get()
        raise Exception("Editor is not running.")

    def set_mod_name(self, name):
        """
        Sets the mod name.
        
        Args:
            name (str): The new mod name.
        """
        if self.app:
            self.app.mod_name_var.set(name)
        else:
            raise Exception("Editor is not running.")

    def insert_snippet(self, snippet_key, target="UI Code"):
        """
        Inserts a snippet (from the toolbox) into the specified target tab.
        
        Args:
            snippet_key (str): The key of the snippet (must exist in TemplateManager.SNIPPETS).
            target (str): The target tab ("UI Code", "Mod Logic", or "Config").
        """
        if self.app:
            snippet = TemplateManager.SNIPPETS.get(snippet_key, None)
            if snippet is None:
                raise Exception(f"Snippet '{snippet_key}' not found.")
            if target == "UI Code":
                widget = self.app.ui_code_text
            elif target == "Mod Logic":
                widget = self.app.mod_code_text
            elif target == "Config":
                widget = self.app.config_text
            else:
                raise Exception(f"Invalid target '{target}'. Valid targets: UI Code, Mod Logic, Config.")
            self.app.after(0, lambda: widget.insert("insert", "\n" + snippet + "\n"))
        else:
            raise Exception("Editor is not running.")

    def get_snippet_list(self):
        """
        Returns the list of available snippet keys.
        
        Returns:
            list: Snippet keys from TemplateManager.SNIPPETS.
        """
        return list(TemplateManager.SNIPPETS.keys())

    def get_console_output(self):
        """
        Retrieves the current contents of the Console tab.
        
        Returns:
            str: The console output.
        """
        if self.app:
            return self.app.console_text.get("0.0", "end-1c")
        raise Exception("Editor is not running.")

    def clear_console(self):
        """
        Clears the Console tab.
        """
        if self.app:
            self.app.after(0, self.app.clear_console)
        else:
            raise Exception("Editor is not running.")

    def switch_tab(self, tab_name):
        """
        Switches to the specified tab in the editor.
        
        Args:
            tab_name (str): The name of the tab (e.g., "UI Code", "Mod Logic", "Config", "GUI Layout", "Console", "3D Editor").
        """
        if self.app:
            self.app.after(0, lambda: self.app.notebook.set(tab_name))
        else:
            raise Exception("Editor is not running.")

    def close_editor(self):
        """
        Closes the editor gracefully.
        """
        if self.app:
            self.app.after(0, self.app.exit_app)
        else:
            raise Exception("Editor is not running.")


class EditorLauncher:
    """
    EditorLauncher provides a command-line interface (CLI) to launch and control the Enhanced Mod Editor.
    
    The launcher uses the EditorAPI to perform operations such as creating a new mod, opening/saving projects,
    previewing the UI, inserting snippets, checking for updates, and more.
    """
    def __init__(self):
        self.api = EditorAPI()

    def run(self):
        print("Launching the Enhanced Mod Editor...")
        self.api.launch_editor()
        print("Editor launched successfully.")

        # Interactive command-line menu loop
        while True:
            print("\nLauncher Menu:")
            print("1. New Mod")
            print("2. Open Mod")
            print("3. Save Mod")
            print("4. Save Mod As")
            print("5. Preview UI")
            print("6. Check Version")
            print("7. Insert Snippet")
            print("8. Get Console Output")
            print("9. Clear Console")
            print("10. Get Mod Name")
            print("11. Set Mod Name")
            print("12. Switch Tab")
            print("13. Close Editor and Exit Launcher")
            choice = input("Enter your choice (1-13): ").strip()
            try:
                if choice == "1":
                    self.api.new_mod()
                    print("New mod workspace initialized.")
                elif choice == "2":
                    self.api.open_mod()
                elif choice == "3":
                    self.api.save_mod()
                elif choice == "4":
                    self.api.save_mod_as()
                elif choice == "5":
                    self.api.preview_ui()
                elif choice == "6":
                    self.api.check_version()
                elif choice == "7":
                    snippet_list = self.api.get_snippet_list()
                    print("Available snippets:", snippet_list)
                    key = input("Enter snippet key to insert: ").strip()
                    target = input("Enter target tab (UI Code/Mod Logic/Config): ").strip()
                    self.api.insert_snippet(key, target)
                    print(f"Snippet '{key}' inserted into {target}.")
                elif choice == "8":
                    output = self.api.get_console_output()
                    print("Console Output:\n", output)
                elif choice == "9":
                    self.api.clear_console()
                    print("Console cleared.")
                elif choice == "10":
                    name = self.api.get_mod_name()
                    print("Current mod name:", name)
                elif choice == "11":
                    new_name = input("Enter new mod name: ").strip()
                    self.api.set_mod_name(new_name)
                    print("Mod name updated.")
                elif choice == "12":
                    tab = input("Enter tab name (UI Code, Mod Logic, Config, GUI Layout, Console, 3D Editor): ").strip()
                    self.api.switch_tab(tab)
                    print("Switched to tab:", tab)
                elif choice == "13":
                    self.api.close_editor()
                    print("Editor closed. Exiting launcher.")
                    break
                else:
                    print("Invalid choice. Please enter a number between 1 and 13.")
            except Exception as e:
                print("Error:", e)
            time.sleep(0.5)


if __name__ == "__main__":
    launcher = EditorLauncher()
    launcher.run()
