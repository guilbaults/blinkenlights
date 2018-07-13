Name:	  blinkenlights	
Version:  0.0.1
Release:  1%{?dist}
Summary:  Script to manage LED and power in Xyratex 5U84 slots JBOD	

License:  Apache License 2.0
URL:      https://github.com/guilbaults/blinkenlights
Source0:  https://github.com/guilbaults/%{name}/archive/v%{gittag}/%{name}-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  python%{python3_pkgversion}-devel
Requires:       sasutils
Requires:       sg3_utils

%description
This tool is used to control the LEDs and slot power in a Xyratex 84 slots JBODs, also know as:
* Seagate/Xyratex SP-2584
* Dell MD1280
* Lenovo D3284
This script can be adapted for other types of JBODs, as long as its possible
to control the LED/power with a sg_ses command.

%prep
%autosetup -n %{name}-%{gittag}
%setup -q

%build
%py3_build

%install
%py3_install

%files
%{_bindir}/blinkenlights
%doc
%license LICENSE

%changelog
* Fri Jul 13 2018 Simon Guilbault <simon.guilbault@calculquebec.ca> 0.0.1-1
- Initial release, supporting Xyratex 84 slots JBOD

