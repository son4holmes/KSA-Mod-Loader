import os
import zipfile
import shutil

CONFIG_FILE = "paths.txt"
MOD_SETUP_FOLDER = "ModSetup"


def save_paths(manifest_path, game_path):
    with open(CONFIG_FILE, "w") as f:
        f.write("##manifestPath##\n")
        f.write(manifest_path + "\n\n")
        f.write("##gamePath##\n")
        f.write(game_path + "\n")
    print("Paths saved!")


def load_paths():
    if not os.path.exists(CONFIG_FILE):
        print("No paths saved yet.")
        return None, None

    with open(CONFIG_FILE, "r") as f:
        lines = f.read().strip().splitlines()

    try:
        # Finds the sections and goes one line down for the provided path. This should allow for easier updates as when I need another user provided path I can just add a similar finder.
        manifest_index = lines.index("##manifestPath##") + 1 #Ill probably add more checks to make sure that its the actual path... For now it just makes sure the folder is called "Kitten Space Agency"
        game_index = lines.index("##gamePath##") + 1
        manifest_path = lines[manifest_index].strip()
        game_path = lines[game_index].strip()
        return manifest_path, game_path
    except ValueError:
        print("Error reading paths file.")
        return None, None


def require_kitten_path(path_name):
    # Forces the user to enter a path ending in 'Kitten Space Agency'
    while True:
        p = input(f"Enter the {path_name} path: ").strip()
        if os.path.basename(p) == "Kitten Space Agency":
            return p
        print("ERROR: The final folder must be 'Kitten Space Agency'.")


def read_mod_name(mod_toml_path):
    """Extract the name from a mod.toml file"""
    if not os.path.exists(mod_toml_path):
        return None

    with open(mod_toml_path, "r", encoding="utf-8") as f:
        for line in f:
            if line.strip().startswith("name"):
                # This is looking for the mod name.
                try:
                    return line.split("=", 1)[1].strip().strip('"')
                except:
                    return None
    return None


def rebuild_manifest(manifest_path, game_path):
    # Rebuild manifest.toml, makes sure to keep Core.
    content_path = os.path.join(game_path, "Content")
    manifest_file = os.path.join(manifest_path, "manifest.toml")

    entries = []
    core_entry = None

    if not os.path.isdir(content_path):
        print("No Content folder found.")
        return

    for folder in os.listdir(content_path):
        mod_dir = os.path.join(content_path, folder)
        mod_toml = os.path.join(mod_dir, "mod.toml")

        if not os.path.exists(mod_toml):
            continue

        mod_name = read_mod_name(mod_toml)
        if not mod_name:
            continue

        entry = f'[[mods]]\nid = "{mod_name}"\nenabled = true\n'

        if folder.lower() == "core":
            core_entry = entry  # store but don't append yet
        else:
            entries.append(entry)

    # Write Core first
    final_entries = []
    if core_entry:
        final_entries.append(core_entry)
    else:
        print("WARNING: Core mod missing from Content!")

    # Write all normal mods after Core
    final_entries.extend(entries)

    with open(manifest_file, "w", encoding="utf-8") as f:
        f.write("\n".join(final_entries))

    print("manifest.toml rebuilt.")



def install_mods(manifest_path, game_path):
    content_path = os.path.join(game_path, "Content")
    os.makedirs(content_path, exist_ok=True)

    if not os.path.exists(MOD_SETUP_FOLDER):
        print("No ModSetup folder found.")
        return

    zips = [z for z in os.listdir(MOD_SETUP_FOLDER) if z.endswith(".zip")]

    if not zips:
        print("No .zip mods found in ModSetup/")
        return

    for zip_file in zips:
        zip_path = os.path.join(MOD_SETUP_FOLDER, zip_file)

        with zipfile.ZipFile(zip_path, "r") as z:
            z.extractall(content_path)
            print(f"Installed {zip_file}")

        # remove zip after success
        os.remove(zip_path)

    print("All mods installed. Rebuilding manifest...")
    rebuild_manifest(manifest_path, game_path)


def manage_mods(manifest_path, game_path):
    content_path = os.path.join(game_path, "Content")

    while True:
        mods = []
        for folder in os.listdir(content_path):
            if folder.lower() == "core":
                continue

            mod_toml = os.path.join(content_path, folder, "mod.toml")
            if os.path.exists(mod_toml):
                mod_name = read_mod_name(mod_toml)
                if mod_name:
                    mods.append((folder, mod_name))

        if not mods:
            print("No installed mods found.")
            return

        print("\nInstalled Mods:")
        for idx, (folder, mod_name) in enumerate(mods, start=1):
            print(f"{idx}. {mod_name} ({folder})")

        choice = input("Enter number to delete, or 'q' to quit: ")

        if choice.lower() == "q":
            return

        if not choice.isdigit() or not (1 <= int(choice) <= len(mods)):
            print("Invalid choice.")
            continue

        idx = int(choice) - 1
        folder, mod_name = mods[idx]
        mod_path = os.path.join(content_path, folder)

        # delete folder
        shutil.rmtree(mod_path)
        print(f"Deleted {mod_name}.")

        # update manifest
        print("Updating manifest...")
        rebuild_manifest(manifest_path, game_path)

# Info
print("ModManager created by Awsomgamr999.\nProtected by CC-BY-NC-SA\nYou are free to modify and release a version of this tool, so long as you credit me and don't use it for commercial purposes.")

def main():
    while True:
        print("\n=== Mod Installer ===")
        print("1. Set paths")
        print("2. Install mods")
        print("3. Manage installed mods")
        print("q. Quit")

        choice = input("Choose an option: ")

        if choice == "1":
            manifest = require_kitten_path("manifest")
            game = require_kitten_path("game")
            save_paths(manifest, game)

        elif choice == "2":
            manifest, game = load_paths()
            if manifest and game:
                install_mods(manifest, game)

        elif choice == "3":
            manifest, game = load_paths()
            if manifest and game:
                manage_mods(manifest, game)

        elif choice.lower() == "q":
            break

        else:
            print("Invalid choice.")


if __name__ == "__main__":
    main()
