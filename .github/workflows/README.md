# GHA for Psi4

## [docs.yml](./docs.yml)

* Since: April 2021
* Runs on: push to master
* Goals:
  * get CI warning if doxygen docs compile broken
  * get CI warning if sphinx docs compile broken, or compile with warnings, or compile with unreachable links, or can't compile nit-picky"
  * publish nightly-build docs promptly and automatically
  * get CI warning if psi4 compile broken with conda-forge environment (as opposed to the usual defaults-based environment)
* Results:
  * automated commit of built HTML docs to psi4/psi4docs:master, which in turn is served up by netlify to https://psi4manual.netlify.app/, which in turn is [redirected by psicode](https://github.com/psi4/psicode-hugo-website/blob/master/netlify.toml) into https://psicode.org/psi4manual/master/index.html

----

## [ecosystem.yml](./ecosystem.yml)

* Since: March 2022
* Runs on: PR, push to master
* Goals:
  * get CI warning if PR breaks addons hosted by psi4 channel or by conda-forge chanel
  * show CI model of how to build Psi4 on Linux, macOS, and Windows platforms, including tweaks to the build environment, and emphasizing the minor differences between platforms
  * show how to run with the maximal ecosystem (less proprietary addons, gpu addons, and addons I haven't packaged), as the environment can be tricky
  * show what addon packages to get from what channel, especially during shift from defaults-based to conda-forge-based
* Results:
  * None

----

## [docs-pr.yml](./docs-pr.yml)

* Since: June 2022
* Runs on: PR
* Goals
  * provide CI warning to author if PR changes break sphinx docs compile, or compile with warnings, or compile with unreachable links, or can't compile nit-picky"
* Results
  * archived tarball of HTML docs (download from Actions, Archives, then unpack and view in browser)

----

## [upstream-release-sync.yml](./upstream-release-sync.yml)

* Since: May 2026
* Runs on: schedule, manual dispatch
* Goals:
  * detect the latest upstream `psi4/psi4` final release tag
  * sync that raw tag into this fork without baking wheel patches into the tag itself
  * dispatch the wheel build workflow against `upstream tag + fork overlay`

----

## [wheel-build.yml](./wheel-build.yml)

* Since: May 2026
* Runs on: manual dispatch, repository dispatch, tag push when workflow file exists on the pushed ref
* Goals:
  * build four wheel lanes: Linux `x86_64`, macOS Intel `x86_64`, macOS Apple Silicon `arm64`, Windows `x86_64`
  * repair each wheel for redistribution
  * smoke-test each repaired wheel once
  * upload reusable artifacts for later publishing

----

## [publish-release.yml](./publish-release.yml)

* Since: May 2026
* Runs on: manual dispatch
* Goals:
  * download an already-tested wheel set from a successful `build-wheel` run
  * pin verification logic to the same fork overlay commit used by that build
  * verify wheel metadata and lane completeness
  * create or update the fork GitHub Release and upload the wheels without rebuilding

----

## [publish-pypi.yml](./publish-pypi.yml)

* Since: May 2026
* Runs on: manual dispatch
* Goals:
  * download an already-tested wheel set from a successful `build-wheel` run
  * pin verification logic to the same fork overlay commit used by that build
  * verify wheel metadata and lane completeness
  * publish the verified artifacts to TestPyPI or PyPI without rebuilding
