# TODO: Unbundle JS from server/includes
#  - jquery 3.6.0 (Done for Fedora)
#  - bootstrap 4.6.0

%global unbundle_jquery 0%{?fedora}%{?el8}%{?el9}%{?el10}

Name:    nrdp
Version: 2.0.6
Release: 2%{?dist}
Summary: Nagios Remote Data Processor

# Bundled jquery and boostrap are MIT
# Everything else is GPLv3
License: GPL-3.0-only and MIT
URL:     https://github.com/NagiosEnterprises/nrdp
Source0: https://github.com/NagiosEnterprises/%{name}/archive/%{version}/%{name}-%{version}.tar.gz
Source1: %{name}-httpd.conf
Source2: %{name}-config.inc.php

BuildArch: noarch

Requires: nagios
# For clarity since Nagios should pull them
Requires: httpd
Requires: php(httpd)

%if %{unbundle_jquery}
BuildRequires: js-jquery3 >= 3.6.0
Requires:      js-jquery3 >= 3.6.0
%else
Provides: bundled(js-jquery) = 3.6.0
%endif
Provides: bundled(js-bootstrap) = 4.6.0


%description
Nagios Remote Data Processor (NDRP) is a flexible data transport
mechanism and processor for Nagios. It is designed with a simple
and powerful architecture that allows for it to be easily extended
and customized to fit individual users needs. It uses standard ports
protocols (HTTP(S) and XML) and can be implemented as a replacement for NSCA.


%package client-shell
Summary: Send NRDP shell script for Nagios
%description client-shell
A shell script to send NRDP data to a Nagios server.

%package client-php
Summary: Send NRDP php script for Nagios
%description client-php
A php script to send NRDP data to a Nagios server.

%package client-python
Summary: Send NRDP python script for Nagios
%description client-python
A python script to send NRDP data to a Nagios server.


%prep
%setup -q
# Fix perms
chmod a-x server/includes/bootstrap-4.6.0.bundle.min.js
chmod a-x server/includes/bootstrap-4.6.0.min.css
chmod a-x server/includes/jquery-3.6.0.min.js
# Fix shebang
sed -i -e '1d;2i#!/usr/bin/python3' clients/send_nrdp.py
sed -i -e '1d;2i#!/usr/bin/python2' clients/send_nrdp_py2.py
# Fix EOL
sed -i "s|\r||g" clients/send_nrdp.php


%build
# Nothing here


%install
# Server
mkdir -p %{buildroot}%{_datadir}/%{name}/
rm -f  server/config.inc.php
cp -pr server/*  %{buildroot}%{_datadir}/%{name}/
ln -s %{_sysconfdir}/%{name}/config.inc.php \
    %{buildroot}%{_datadir}/%{name}/config.inc.php
# Server conf file
mkdir -p %{buildroot}%{_sysconfdir}/%{name}/
install -m 0644 -D -p %{SOURCE2} %{buildroot}%{_sysconfdir}/%{name}/config.inc.php
# httpd conf
mkdir -p %{buildroot}%{_sysconfdir}/httpd/conf.d/
install -m 0644 -D -p %{SOURCE1} \
    %{buildroot}%{_sysconfdir}/httpd/conf.d/nrdp.conf
# Unbundle jquery
%if %{unbundle_jquery}
rm -f %{buildroot}%{_datadir}/%{name}/includes/jquery-3.6.0.min.js
ln -s %{_datadir}/javascript/jquery/3/jquery.min.js \
    %{buildroot}%{_datadir}/%{name}/includes/jquery-3.6.0.min.js
%endif
# Client scripts
mkdir -p %{buildroot}%{_bindir}/
install -m 0755 -D -p clients/* %{buildroot}%{_bindir}/
%if 0%{?fedora} >= 41 || 0%{?rhel} >= 10
rm %{buildroot}%{_bindir}/send_nrdp_py2.py
%endif


%files
%license LICENSE.md
%doc CHANGES.md README.md
%{_datadir}/%{name}/
%dir %{_sysconfdir}/%{name}/
%config(noreplace) %{_sysconfdir}/%{name}/config.inc.php
%config(noreplace) %{_sysconfdir}/httpd/conf.d/nrdp.conf

%files client-shell
%license LICENSE.md
%{_bindir}/send_nrdp.sh

%files client-php
%license LICENSE.md
%{_bindir}/send_nrdp.php

%files client-python
%license LICENSE.md
%{_bindir}/send_nrdp.py
%if ( 0%{?fedora} && 0%{?fedora} < 41 ) || ( 0%{?rhel} && 0%{?rhel} < 10 )
%{_bindir}/send_nrdp_py2.py
%endif


%changelog
* Wed Jan 29 2025 RPM Fusion Release Engineering <sergiomb@rpmfusion.org> - 2.0.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Sun Sep 22 2024 Xavier Bachelot <xavier@bachelot.org> 2.0.2-1
- Update to 2.0.6 (Re-licensed to GPLv3)
- Unbundle jquery
- Drop EL6 support

* Sat Aug 03 2024 RPM Fusion Release Engineering <sergiomb@rpmfusion.org> - 1.5.2-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Sun Feb 04 2024 RPM Fusion Release Engineering <sergiomb@rpmfusion.org> - 1.5.2-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Aug 03 2023 RPM Fusion Release Engineering <sergiomb@rpmfusion.org> - 1.5.2-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Mon Aug 08 2022 RPM Fusion Release Engineering <sergiomb@rpmfusion.org> - 1.5.2-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild and ffmpeg
  5.1

* Thu Feb 10 2022 RPM Fusion Release Engineering <sergiomb@rpmfusion.org> - 1.5.2-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Wed Aug 04 2021 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 1.5.2-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Thu Feb 04 2021 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 1.5.2-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Thu Aug 20 2020 Xavier Bachelot <xavier@bachelot.org> 1.5.2-7
- Replace dependency on mod_php with php(httpd) for all but EL6

* Wed Aug 19 2020 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 1.5.2-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed Feb 05 2020 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 1.5.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Sat Aug 10 2019 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 1.5.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Tue Mar 05 2019 Xavier Bachelot <xavier@bachelot.org> 1.5.2-3
- Mark python client as python2.

* Tue Mar 05 2019 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 1.5.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Wed Sep 12 2018 Xavier Bachelot <xavier@bachelot.org> 1.5.2-1
- Update to 1.5.2.
- Fix License: tag for php client sub-package.

* Sun Aug 19 2018 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 1.5.1-6
- Rebuilt for Fedora 29 Mass Rebuild binutils issue

* Fri Jul 27 2018 RPM Fusion Release Engineering <sergio@serjux.com> - 1.5.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Mon Feb 26 2018 Xavier Bachelot <xavier@bachelot.org> 1.5.1-4
- Clarify license.
- Own %%{_sysconfdir}/%%{name}.
- Requires mod_php rather than php.

* Fri Feb 23 2018 Athmane Madjoudj <athmane@fedoraproject.org> - 1.5.1-3
- Revamp requirements

* Fri Feb 23 2018 Xavier Bachelot <xavier@bachelot.org> 1.5.1-2
- More clean up.

* Fri Feb 23 2018 Xavier Bachelot <xavier@bachelot.org> 1.5.1-1
- Update to 1.5.1.
- Clean up spec.

* Sat Nov 21 2015 Athmane Madjoudj <athmane@fedoraproject.org> 0.20150122gitbd1b5d0-2
- Use better version (pre-release)
- Include license file in the clients sub-pkg
- Add a license workaround

* Fri Nov 20 2015 Athmane Madjoudj <athmane@fedoraproject.org> 0.bd1b5d0git-1
- Initial spec file.
