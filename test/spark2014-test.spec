# Upstream source information.
%global upstream_owner        AdaCore
%global upstream_name         spark2014
%global upstream_commit_date  20250125
%global upstream_commit       1d27d7cf1e19633390beb92a9ea9f11ba601f773
%global upstream_shortcommit  %(c=%{upstream_commit}; echo ${c:0:7})

Name:           spark2014-test
Version:        0^%{upstream_commit_date}git%{upstream_shortcommit}
Release:        1%{?dist}
Summary:        Dummy package for running the SPARK 2014 testsuite

License:        GPL-3.0-or-later

URL:            https://github.com/%{upstream_owner}/%{upstream_name}
Source0:        https://github.com/%{upstream_owner}/%{upstream_name}/archive/%{upstream_commit}.tar.gz

# [Fedora-specific] Colibri solver not available on Fedora.
Patch:          spark2014-colibri-not-available-for-testing.patch

BuildRequires:  spark2014
BuildRequires:  sparklib
BuildRequires:  cvc5, z3, alt-ergo

BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python3-e3-testsuite

ExclusiveArch:  %{ocaml_native_compiler}

%description
This is a dummy package used to run the SPARK 2014 testsuite. The package acts
as workaround until the check-section of the spark2014 spec-file can be used.


#############
## Prepare ##
#############

%prep
%autosetup -n %{upstream_name}-%{upstream_commit} -p1


###########
## Build ##
###########

%build
%nil


#############
## Install ##
#############

%install
%nil


###########
## Check ##
###########

%check

export PYTHONPATH=%{python3}

# Use a file-based cache for sharing proof results between tests.
%global cachedir '%{_builddir}/%{upstream_name}-%{upstream_commit}/testsuite/result_cache'

mkdir --parents %{cachedir}
export GNATPROVE_CACHE='file:%{cachedir}'

# Run the tests.
%python3 testsuite/gnatprove/run-tests \
         --show-error-output \
         --max-consecutive-failures=8 \
         --cache


###########
## Files ##
###########

%files
%license LICENSE
%doc README*


###############
## Changelog ##
###############

%changelog
* Sun Jan 19 2025 Dennis van Raaij <dvraaij@fedoraproject.org> - 15.0-1
- Updated to FSF 15.0.

* Sun Feb 25 2024 Dennis van Raaij <dvraaij@fedoraproject.org> - 14.0-1
- Updated to FSF 14.0.

* Sat Aug 05 2023 Dennis van Raaij <dvraaij@fedoraproject.org> - 0^20230107git12db22e-1
- New package, snapshot: Git commit 12db22e (fsf-13), 2023-01-07.
