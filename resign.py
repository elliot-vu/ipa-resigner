#!/usr/bin/python3

import argparse
import os
import subprocess
import common

def dump_entitlements(profile, working_dir):
    common.execute_shell_command("security cms -D -i {} > {}/provision.plist".format(profile, working_dir))
    common.execute_shell_command("/usr/libexec/PlistBuddy -x -c 'Print :Entitlements' {}/provision.plist > {}/entitlements.plist".format(working_dir, working_dir))

def copy_embedded_profile(profile, bundle):
    common.execute_shell_command("cp {} {}/embedded.mobileprovision".format(profile, bundle))

def rename_bundle_id(bundle, new_bundle_id):
    print("[INFO] Renaming app bundle_id {} to {}".format(bundle, new_bundle_id))
    common.execute_shell_command("/usr/libexec/PlistBuddy -c \"Set :CFBundleIdentifier {}\" {}/Info.plist".format(new_bundle_id, bundle))

def rename_bundle_id_for_plug_in(bundle, new_bundle_id, app_original_bundle_id):
    pluginFolderPath = bundle + "/PlugIns"
    if not os.path.exists(pluginFolderPath):
        return
    plug_ins = common.find_folders_with_extension(pluginFolderPath, "appex")
    for plug_in in plug_ins:
        original_bundle_id = common.get_original_bundle_id(plug_in)
        new_plug_in_bundle_id = original_bundle_id.replace(app_original_bundle_id, new_bundle_id)
        print("[INFO] Renaming bundle_id {} to {}".format(original_bundle_id, new_plug_in_bundle_id))
        common.execute_shell_command("/usr/libexec/PlistBuddy -c \"Set :CFBundleIdentifier {}\" {}/Info.plist".format(new_plug_in_bundle_id, plug_in))

def resign(bundle, certificate, entitlement):
    frameworks = common.find_folders_with_extension(os.path.join(bundle, "frameworks"), ".framework")
    print("Found {} frameworks in {}".format(len(frameworks), os.path.join(bundle, "frameworks")))

    sign_frameworks(bundle, certificate, entitlement)
    sign_plugIns(bundle, certificate, entitlement)
    code_sign([bundle], certificate, entitlement)

def sign_frameworks(bundle, certificate, entitlement):
    cmd = "/usr/bin/codesign -fs \"{}\" {} --entitlements={}".format(certificate, os.path.join(bundle, "frameworks/*"), entitlement)
    common.execute_shell_command(cmd)

def sign_plugIns(bundle, certificate, entitlement):
    cmd = "/usr/bin/codesign -fs \"{}\" {} --entitlements={}".format(certificate, os.path.join(bundle, "PlugIns/*"), entitlement)
    common.execute_shell_command(cmd)

def code_sign(paths, certificate, entitlement):
    for path in paths:
        cmd = "/usr/bin/codesign -vvv -fs \"{}\" {} --entitlements={}".format(certificate, path, entitlement)
        print("Execute: {}".format(cmd))
        common.execute_shell_command(cmd)

def process_resign(working_dir, profile, certificate, bundle_id):
    bundle = common.find_app_bundle(working_dir)
    print("[INFO] Found bundle: {}".format(bundle))

    dump_entitlements(profile, working_dir)
    copy_embedded_profile(profile, bundle)

    if bundle_id != None:
        origin_bundle_id = common.get_original_bundle_id(bundle)
        print("[INFO] origin bundle_id: {}".format(origin_bundle_id))
        rename_bundle_id(bundle, bundle_id)
        rename_bundle_id_for_plug_in(bundle, bundle_id, origin_bundle_id)
    resign(bundle, certificate, "{}/entitlements.plist".format(working_dir))

    output_bundle_id = bundle_id
    if output_bundle_id == None:
        output_bundle_id = common.get_original_bundle_id(bundle)
    output_name = "{}-resigned.ipa".format(output_bundle_id)
    common.zip_payload(working_dir, output_name)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Code sign an iOS IPA")
    parser.add_argument("--ipa", required=True, help="Path to the IPA payload directory")
    parser.add_argument("--profile", required=True, help="Provisioning profile name")
    parser.add_argument("--certificate", required=True, help="Certificate name")
    parser.add_argument("--bundle_id", required=False, help="New bundle ID")

    args = parser.parse_args()

    working_dir = "tmp"
    common.execute_shell_command("rm -rf {}".format(working_dir))
    common.unzip_ipa(args.ipa, working_dir)
    process_resign(working_dir, args.profile, args.certificate, args.bundle_id)
