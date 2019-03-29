"""
Download golang package release binary from GitHub.
"""

import os
from logging import getLogger
from pathlib import Path

import requests
from github import Github


logger = getLogger(__name__)


def match_asset(asset_name, goos, goarch):
    """
    Compate asset name with GOOS and GOARCH.
    Return True if matched.
    """
    asset_name = asset_name.lower()
    goarch = {
        "386": ["386"],
        "amd64": ["amd64", "x86_64"]
    }[goarch]
    match_goos = goos in asset_name
    match_goarch = any([word in asset_name for word in goarch])
    return match_goos and match_goarch


def install_release_binary(go_pkg_name):
    """
    Download golang package release binary from GitHub.
    """
    gopath = os.environ.get("GOPATH")
    goos = os.environ.get("GOOS")
    goarch = os.environ.get("GOARCH")

    g = Github()
    repo_name = go_pkg_name.lstrip("github.com/")
    repo = g.get_repo(repo_name)
    release = repo.get_latest_release()
    logger.info("Release: %s", release.title)

    assets = release.get_assets()
    assets = [asset for asset in assets
              if match_asset(asset.name, goos, goarch)]
    asset = assets[0]
    logger.info("Asset: %s", asset.name)

    r = requests.get(asset.browser_download_url)
    path = Path(gopath, "bin", repo.name)
    with open(path, "wb") as f:
        f.write(r.content)
    os.chmod(path, 0o755)
