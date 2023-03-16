import subprocess


def bump_version():
    # Get the current version
    current_version = subprocess.check_output(["git", "describe", "--tags"]).strip().decode("utf-8")

    # Split version string into major, minor, and patch versions
    major, minor, patch = [int(x) for x in current_version.strip("v").split(".")]

    # Bump the version number
    patch += 1

    new_version = f"v{major}.{minor}.{patch}"
    return new_version


if __name__ == "__main__":
    print(bump_version())
