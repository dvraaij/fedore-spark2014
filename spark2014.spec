# OPEN-ISSUE: Testsuite does not work due to the absolute paths in configuration.

# The test suite isn't normally run. It can be enabled with "--without=check".
%bcond_with check

# Constrain make to 1 CPU to see the log output.
%{constrain_build -c 1}

# Upstream source information.
%global upstream_owner             AdaCore
%global upstream_name              spark2014
%global upstream_commit_date       20240111
%global upstream_commit            ce5fad038790d5dc18f9b5345dc604f1ccf45b06
%global upstream_shortcommit       %(c=%{upstream_commit}; echo ${c:0:7})

%global upstream_name_why3         why3
%global upstream_commit_why3       fb4ca6cd8c7d888d3e8d281e6de87c66ec20f084
%global upstream_shortcommit_why3  %(c=%{upstream_commit_why3}; echo ${c:0:7})

# Major version must match the targeted version SPARK's FSF branch
# (i.e., "fsf-xy"). The minor version is of limited interest as the
# GNAT front-end is rarely updated on a GCC release branch.
%global gcc_version  14.2.1-20241025
%global gcc_sha512   1729619d7c0ebdb6801f692f213ccdd2f393d28d2c2acc3cedc897992c0996d45d760e9f4bd4d6f3ef16c7343a1e24c21c45989fa6c08ba1556fa8c9a5662d5f

Name:           spark2014
Version:        14.0
Release:        2%{?dist}
Summary:        Software development technology for engineering high-reliability applications

License:        GPL-3.0-or-later AND LGPL-2.1-only AND LGPL-2.0-only WITH OCaml-LGPL-linking-exception
# The license of the SPARK 2014 tooling is GPLv3+.
# The license of the bundled GNAT compiler code is GPLv3+.
# The license of the bundled Why3 software is LGPLv2.1, except for
# - why3/src/util/extmap.mli : LGPLv2.0 with OCaml LGPL linking exception
# - why3/src/util/extmap.ml  : LGPLv2.0 with OCaml LGPL linking exception
#
# The Why3 IDE depends on the "FatCow" icon set, which is included in the Why3
# source package and licensed separately. However, as the Why3 IDE is not in the
# spark2014 package, the license of the "FatCow" icon set is not mentioned.

URL:            https://www.adacore.com/about-spark
Source0:        https://github.com/%{upstream_owner}/%{upstream_name}/archive/%{upstream_commit}.tar.gz#/%{name}-%{upstream_shortcommit}.tar.gz
Source1:        https://github.com/%{upstream_owner}/%{upstream_name_why3}/archive/%{upstream_commit_why3}.tar.gz#/%{upstream_name_why3}-%{upstream_shortcommit_why3}.tar.gz

# The gnat2why application is partly built with source code from the GNAT front-end.
Source2:        https://src.fedoraproject.org/repo/pkgs/gcc/gcc-%{gcc_version}.tar.xz/sha512/%{gcc_sha512}/gcc-%{gcc_version}.tar.xz

# Build-time configurable version of the SPARK_Install package.
Source3:        spark_install.ads.in

# --- Patches for SPARK and GNATprove.

# [Fedora-specific] Make (search) paths configurable (GNATprove).
Patch0:         %{name}-prep-fix-paths-gnatprove.patch
# [Fedora-specific] Allow additional build options for gnatprove.
Patch1:         %{name}-add-build-options-for-gnatprove.patch
# [Fedora-specific] Colibri solver not available on Fedora.
Patch2:         %{name}-colibri-not-available-for-testing.patch
# [Fedora-specific] Add ppc64le and s390x targets.
Patch3:         %{name}-add-ppc64le-and-s390x-targets.patch
# [Fedora-specific] Switches for Alt-Ergo use a single dash prior to v2.4.0.
#   See also: https://ocamlpro.github.io/alt-ergo/About/changes.html#version-2-4-0-january-22-2021
Patch4:         %{name}-fix-gnatprove-alt-ergo-version-inquiry.patch
# [Fedora-specific] Adapt `install` target in makefile: SPARKlib is separate.
Patch5:         %{name}-sparklib-is-separate.patch
# Use 'gnatcoll_core.gpr' instead of 'gnatcoll.gpr'.
Patch6:         %{name}-refine-dependencies-to-gnatcoll.patch

# --- Patches for Why3.

# [Fedora-specific] Make (search) paths configurable (gnatwhy3).
Patch20:        %{name}-why3-prep-fix-paths-gnatwhy3.patch
# [Fedora-specific] Suppress "warning 70 [missing-mli]".
#   Build fails as the warning-is-error option is enabled on Fedora.
Patch21:        %{name}-why3-fix-missing-mli-error.patch
# Add missing functions in ptree.ml (added in Inria-Why3 commit c8a5858).
#   Functions are needed in `plugins/gnat_json/gnat_ast_to_ptree.ml`.
Patch22:        %{name}-why3-add-missing-functions-in-ptree.patch
# Replace `Pervasives` with `Stdlib` (fixed in upstream commit 92e01ef).
Patch23:        %{name}-why3-replace-pervasives-with-stdlib.patch
# Adapt to Coq 8.18 (fixed in upstream commit 25b9f61).
Patch24:        %{name}-why3-adapt-to-coq-8.18.patch

BuildRequires:  gcc-gnat gprbuild autoconf make sed
# A fedora-gnat-project-common that contains GPRbuild_flags is needed.
BuildRequires:  fedora-gnat-project-common >= 3.17
# SPARK/GNATprove depends on a special version of libgpr2, called "next".
BuildRequires:  libgpr2_next-devel
# A gnatcoll-core that contains gnatcoll_core.gpr is needed.
BuildRequires:  gnatcoll-core-devel >= 25.0.0
BuildRequires:  zlib-devel
BuildRequires:  coq
# OCaml dependencies as mentioned in `Why3/fsf_build.sh`.
# -- Note: Package `ocaml-seq` not available in Fedora (yet).
BuildRequires:  ocaml-menhir
BuildRequires:  ocaml-ocamlgraph-devel
BuildRequires:  ocaml-num-devel
BuildRequires:  ocaml-re-devel
BuildRequires:  ocaml-yojson-devel
BuildRequires:  ocaml-zarith-devel
BuildRequires:  ocaml-sexplib-devel
BuildRequires:  ocaml-ppx-sexp-conv-devel
BuildRequires:  ocaml-ppx-deriving-devel
BuildRequires:  python3-sphinx
BuildRequires:  python3-sphinx-latex
BuildRequires:  python3-sphinx_rtd_theme
BuildRequires:  latexmk
%if %{with check}
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python3-e3-testsuite
# Install solvers.
BuildRequires:  cvc5, z3, alt-ergo
%endif

Requires:       gcc-gnat >= 14
Requires:       gprbuild

# gnat2why depends on a forked version of Why3. This version is installed in a
# package specific directory in the libexec dir. It is roughly based on Why3
# 1.6.0. Common commit has author date 2023-05-15 11:52:04:
#
# - Inria        : 006edd7ea285bfd32eb2404e8695b1273505ce04
# - AdaCore fork : 006edd7ea285bfd32eb2404e8695b1273505ce04
#
Provides:       bundled(why3)

# gnat2why is build with portions of the GNAT source code. GNAT itself is not
# included (as a binary) and can be installed alongside.
Provides:       bundled(gcc-gnat)

# Alternative names.
Provides:       spark-ada = %{version}
Provides:       gnatprove = %{version}

# Recommend SPARKlib and all supported solvers available in Fedora.
Recommends:     sparklib
Recommends:     cvc5, z3, alt-ergo

# Build only on architectures where GPRbuild and the OCaml compiler is
# available. Only pick the most narrow one. If you have two ExclusiveArch
# lines in a spec file, RPM ignores the first one and uses the second one!
# ExclusiveArch:  %{GPRbuild_arches}
ExclusiveArch:  %{ocaml_native_compiler}

%global common_description_en \
SPARK is a software development technology specifically designed for \
engineering high-reliability applications. It consists of a programming \
language, a verification toolset and a design method which, taken \
together, ensure that ultra-low defect software can be deployed in \
application domains where high-reliability must be assured and where \
safety and security are key requirements.

%description %{common_description_en}


#################
## Subpackages ##
#################

%package doc
Summary:        Documentation for SPARK 2014
BuildArch:      noarch
License:        GFDL-1.1-no-invariants-or-later AND MIT AND BSD-2-Clause AND GPL-3.0-or-later
# The license of the documentation itself is GFDL 1.1. Some Javascript and CSS
# files that Sphinx includes with the documentation are BSD 2-Clause and
# MIT-licensed. The examples are licensed under GPL 3.0 or later.

%description doc %{common_description_en}

This package contains the SPARK user's guide and SPARK 2014 language reference
manual in HTML and PDF format, and some examples.


#############
## Prepare ##
#############

%prep
%setup -q -n %{upstream_name}-%{upstream_commit}

# Replace the Why3 git submodule placeholder with the downloaded sources.
rmdir why3
tar --extract --gzip --file %{SOURCE1}
mv %{upstream_name_why3}-%{upstream_commit_why3} why3

# Extract the GNAT sources from the GCC source tarball. Create a symbolic link
# that points to these GNAT sources.
tar --extract --xz --file %{SOURCE2} gcc-%{gcc_version}/gcc/ada
ln --symbolic ../gcc-%{gcc_version}/gcc/ada gnat2why/gnat_src

# All sources have been setup, we can now start patching.

# Apply patches to SPARK and GNATprove.
%patch 0 -p1
%patch 1 -p1
%patch 2 -p1
%patch 3 -p1
%patch 4 -p1
%patch 5 -p1
%patch 6 -p1

# Apply patches to Why3.
%patch 20 -p1
%patch 21 -p1
%patch 22 -p1
%patch 23 -p1
%patch 24 -p1

# Patch gnatprove's hard-coded assumptions on (relative) paths.
# -- Note: Depends on the application of patch 0.
sed --expression='s,@PREFIX@,%{_prefix},'               \
    --expression='s,@LIBDIR@,%{_libdir},'               \
    --expression='s,@LIBEXECDIR@,%{_libexecdir},'       \
    --expression='s,@DATADIR@,%{_datadir},'             \
    --expression='s,@GNATPRJDIR@,%{_GNAT_project_dir},' \
    --expression='s,@NAME@,%{name},'                    \
    %{SOURCE3} > ./src/gnatprove/spark_install.ads

# Patch gnatwhy3's hard-coded assumptions on (relative) paths.
# -- Note: Depends on the application of patch 20.
sed --in-place \
    --expression='s,@LIBEXECDIR@,%{_libexecdir},' \
    --expression='s,@DATADIR@,%{_datadir},'       \
    --expression='s,@NAME@,%{name},'              \
    ./why3/src/gnat/gnat_util.ml

# Update some release specific information.
sed --in-place \
    --expression='25 { s/0.0w/FSF 14.0/; t; q1 }' \
    ./spark2014vsn.ads


###########
## Build ##
###########

%build

make setup
%{make_build} VERSION=%{version} PROCS=0 \
              GPRBUILD='gprbuild %{GPRbuild_flags} -cargs -fPIE -gargs'

# Don't forget the docs.
make doc VERSION=%{version}


#############
## Install ##
#############

%install

# Make will install all files under a subdirectory "install" located in
# builddir. Patching all files (including some GPRbuild files) seems too
# cumbersone so we'll move everything into the correct place afterwards.
make install-all
make install-examples

# Move SPARK tools + Why3.
mkdir --parents \
      %{buildroot}%{_datadir}/%{name}        \
      %{buildroot}%{_libexecdir}/%{name}     \
      %{buildroot}%{_bindir}                 \
      %{buildroot}%{_libexecdir}/%{name}/bin \

mv ./install/share/spark/*   %{buildroot}%{_datadir}/%{name}
mv ./install/libexec/spark/* %{buildroot}%{_libexecdir}/%{name}
mv ./install/bin/gnatprove   %{buildroot}%{_bindir}
mv ./install/bin/*           %{buildroot}%{_libexecdir}/%{name}/bin

# Move docs and examples
mkdir --parents \
      %{buildroot}%{_pkgdocdir} \
      %{buildroot}%{_pkgdocdir}/examples

mv ./install/share/doc/spark/*      %{buildroot}%{_pkgdocdir}
mv ./install/share/examples/spark/* %{buildroot}%{_pkgdocdir}/examples

# Remove files that should and are already in `libexec/spark2014/bin`.
rm %{buildroot}%{_libexecdir}/%{name}/lib/why3/why3server
rm %{buildroot}%{_libexecdir}/%{name}/lib/why3/why3cpulimit

# PVS is not supported in SPARK.
rm %{buildroot}%{_libexecdir}/%{name}/lib/why3/why3-call-pvs

# Show installed files (to ease debugging based on build server logs).
find ./install    -exec stat --format "%A %n" {} \;
find %{buildroot} -exec stat --format "%A %n" {} \;


###########
## Check ##
###########

%if %{with check}
%check

# Make the files installed in the buildroot visible to the testsuite.
export PATH=%{buildroot}%{_bindir}:$PATH
export LD_LIBRARY_PATH=%{buildroot}%{_libdir}:$LD_LIBRARY_PATH
export PYTHONPATH=%{buildroot}%{python3_sitearch}:%{buildroot}%{python3_sitelib}:$PYTHONPATH

# Use a file-based cache for sharing proof results between tests.
%global cachedir '%{_builddir}/%{upstream_name}-%{upstream_commit}/testsuite/result_cache'

mkdir --parents %{cachedir}
export GNATPROVE_CACHE='file:%{cachedir}'

# Run the tests.
%python3 testsuite/gnatprove/run-tests \
         --show-error-output \
         --max-consecutive-failures=8 \
         --cache

%endif


###########
## Files ##
###########

%files
%license LICENSE
%doc README*

%{_bindir}/gnatprove
%{_libexecdir}/%{name}
%{_datadir}/%{name}
# Remove the fake prover scripts that are only used for benchmarking.
%exclude %{_libexecdir}/%{name}/bin/fake*
# Remove images and translations for why3ide: Why3ide is not included.
%exclude %{_libexecdir}/%{name}/share/why3/images
%exclude %{_libexecdir}/%{name}/share/why3/lang


%files doc
%dir %{_pkgdocdir}
%{_pkgdocdir}/html
%{_pkgdocdir}/pdf
%{_pkgdocdir}/examples
# Remove Sphinx-generated files that aren't needed in the package.
%exclude %{_pkgdocdir}/html/ug/objects.inv
%exclude %{_pkgdocdir}/html/lrm/objects.inv


###############
## Changelog ##
###############

%changelog
* Sun Nov 03 2024 Dennis van Raaij <dvraaij@fedoraproject.org> - 14.0-2
- Rebuilt for GCC 14.2.1-20241025 and the v25.0.0 dependency updates.

* Sun Feb 25 2024 Dennis van Raaij <dvraaij@fedoraproject.org> - 14.0-1
- Updated to FSF 14.0.

* Sat Aug 05 2023 Dennis van Raaij <dvraaij@fedoraproject.org> - 13.0-1
- New package, initial version FSF 13.0.
