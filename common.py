import os
import subprocess

def execute_shell_command(cmd):
    subprocess.run(["sh", "-c", cmd])

def find_folders_with_extension(root_path, target_extension):
    folders_with_extension = []

    for filename in os.listdir(root_path):
        if filename.endswith(target_extension):
            folders_with_extension.append(os.path.join(root_path, filename))

    return folders_with_extension

def find_app_bundle(working_dir):
    payload_dir = os.path.join(working_dir, "Payload")
    for filename in os.listdir(payload_dir):
        if filename.endswith(".app"):
            return os.path.join(payload_dir, filename)
    return None

def zip_payload(working_dir, dest,):
    print("Zipping to {}".format(dest))
    execute_shell_command("rm -rf {}".format(dest))
    execute_shell_command("cd {} && zip -qr {} {}".format(working_dir, "tmp.ipa", "Payload"))
    execute_shell_command("mv {}/tmp.ipa {}".format(working_dir, dest))

def unzip_ipa(ipa, dest):
    print("Unzipping {}".format(ipa))
    execute_shell_command("unzip -q {} -d {}".format(ipa, dest))

def get_original_bundle_id(bundle):
    plist_path = "{}/Info.plist".format(bundle)
    try:
        command = [
            "/usr/libexec/PlistBuddy",
            "-c", "Print :CFBundleIdentifier",
            plist_path
        ]
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        return result.stdout.strip()
    except (subprocess.CalledProcessError, FileNotFoundError) as e:
        print(f"Error: {e}")
        return None

def get_binary_name(bundle):
    plist_path = "{}/Info.plist".format(bundle)
    try:
        command = [
            "/usr/libexec/PlistBuddy",
            "-c", "Print :CFBundleExecutable",
            plist_path
        ]
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        return result.stdout.strip()
    except (subprocess.CalledProcessError, FileNotFoundError) as e:
        print(f"Error: {e}")
        return None