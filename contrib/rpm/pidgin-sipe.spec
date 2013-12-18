#
# Example SPEC file to generate a RPM for pidgin-sipe.
# It should work out-of-the-box on Fedora 10+ or RHEL5+.
#
%if 0%{?_with_git:1}
#------------------------------- BUILD FROM GIT -------------------------------
# Add "--with git" to the rpmbuild command line to build from git
#
# Instructions how to access the repository: http://sipe.sourceforge.net/git/
#
# Run "./git-snapshot.sh ." in your local repository.
# Then update the following line from the generated archive name
%define git       20120905gitcc6065b
# Increment when you generate several RPMs on the same day...
%define gitcount  0
#------------------------------- BUILD FROM GIT -------------------------------
%endif

%define purple_plugin    purple-sipe
%define telepathy_plugin telepathy-sipe
%define common_files     sipe-common
%define empathy_files    empathy-sipe
%define ktp_files        ktp-accounts-kcm-sipe
%define pkg_group        Applications/Internet

Name:           pidgin-sipe
Summary:        Pidgin protocol plugin to connect to MS Office Communicator
Version:        1.17.3
%if 0%{?_with_git:1}
Release:        %{gitcount}.%{git}%{?dist}
Source:         %{name}-%{git}.tar.bz2
# git package overrides official released package
Epoch:          1
%else
Release:        1%{?dist}
Source:         http://downloads.sourceforge.net/sipe/%{name}-%{version}.tar.bz2
%endif
Group:          %{pkg_group}
License:        GPL-2.0+
URL:            http://sipe.sourceforge.net/

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  libpurple-devel >= 2.4.0
BuildRequires:  glib2-devel >= 2.12.0
BuildRequires:  gmime-devel
BuildRequires:  libxml2-devel
BuildRequires:  nss-devel
BuildRequires:  libtool
BuildRequires:  intltool
BuildRequires:  gettext-devel
# Use "--with vv" to enable Voice & Video features
%if 0%{?_with_vv:1}
BuildRequires:  libpurple-devel >= 2.8.0
BuildRequires:  libnice-devel >= 0.1.0
BuildRequires:  gstreamer-devel
%endif
# Use "--without telepathy" to disable telepathy
%if !0%{?_without_telepathy:1}
BuildRequires:  telepathy-glib-devel >= 0.18.0
BuildRequires:  glib2-devel >= 2.28.0
%endif

# Configurable components
# Use "--without kerberos" to disable krb5
%if !0%{?_without_kerberos:1}
BuildRequires:  krb5-devel
%endif

Requires:       %{purple_plugin} = %{?epoch:%{epoch}:}%{version}-%{release}


%description
A third-party plugin for the Pidgin multi-protocol instant messenger.
It implements the extended version of SIP/SIMPLE used by various products:

    * Microsoft Office 365
    * Microsoft Business Productivity Online Suite (BPOS)
    * Microsoft Lync Server
    * Microsoft Office Communications Server (OCS 2007/2007 R2)
    * Microsoft Live Communications Server (LCS 2003/2005)
    * Reuters Messaging

With this plugin you should be able to replace your Microsoft Office
Communicator client with Pidgin.

This package provides the icon set for Pidgin.


%package -n %{purple_plugin}
Summary:        Libpurple protocol plugin to connect to MS Office Communicator
Group:          %{pkg_group}
License:        GPL-2.0+
Requires:       %{common_files} = %{?epoch:%{epoch}:}%{version}-%{release}

%description -n %{purple_plugin}
A third-party plugin for the Pidgin multi-protocol instant messenger.
It implements the extended version of SIP/SIMPLE used by various products:

    * Microsoft Office 365
    * Microsoft Business Productivity Online Suite (BPOS)
    * Microsoft Lync Server
    * Microsoft Office Communications Server (OCS 2007/2007 R2)
    * Microsoft Live Communications Server (LCS 2003/2005)
    * Reuters Messaging

This package provides the protocol plugin for libpurple clients.


%if !0%{?_without_telepathy:1}
%package -n %{empathy_files}
Summary:        Telepathy connection manager to connect to MS Office Communicator
Group:          %{pkg_group}
License:        GPL-2.0+
Requires:       %{telepathy_plugin} = %{?epoch:%{epoch}:}%{version}-%{release}

%description -n %{empathy_files}
A Telepathy connection manager that implements the extended version of
SIP/SIMPLE used by various products:

    * Microsoft Office 365
    * Microsoft Business Productivity Online Suite (BPOS)
    * Microsoft Lync Server
    * Microsoft Office Communications Server (OCS 2007/2007 R2)
    * Microsoft Live Communications Server (LCS 2003/2005)
    * Reuters Messaging

This package provides the icon set for Empathy.


%package -n %{ktp_files}
Summary:        Telepathy connection manager to connect to MS Office Communicator
Group:          %{pkg_group}
License:        GPL-2.0+
Requires:       %{telepathy_plugin} = %{?epoch:%{epoch}:}%{version}-%{release}

%description -n %{ktp_files}
A Telepathy connection manager that implements the extended version of
SIP/SIMPLE used by various products:

    * Microsoft Office 365
    * Microsoft Business Productivity Online Suite (BPOS)
    * Microsoft Lync Server
    * Microsoft Office Communications Server (OCS 2007/2007 R2)
    * Microsoft Live Communications Server (LCS 2003/2005)
    * Reuters Messaging

This package provides the profile for KTP account manager.


%package -n %{telepathy_plugin}
Summary:        Telepathy connection manager to connect to MS Office Communicator
Group:          %{pkg_group}
License:        GPL-2.0+
Requires:       %{common_files} = %{?epoch:%{epoch}:}%{version}-%{release}

%description -n %{telepathy_plugin}
A Telepathy connection manager that implements the extended version of
SIP/SIMPLE used by various products:

    * Microsoft Office 365
    * Microsoft Business Productivity Online Suite (BPOS)
    * Microsoft Lync Server
    * Microsoft Office Communications Server (OCS 2007/2007 R2)
    * Microsoft Live Communications Server (LCS 2003/2005)
    * Reuters Messaging

This package provides the protocol support for Telepathy clients.
%endif


%package -n %{common_files}
Summary:        Common files for SIPE protocol plugins
Group:          %{pkg_group}
License:        GPL-2.0+
BuildArch:      noarch

%description -n %{common_files}
This package provides common files for the SIPE protocol plugins:

    * Localisation


%prep
%if 0%{?_with_git:1}
%setup -q -n %{name}-%{git}
%else
%setup -q
%endif


%build
%if 0%{?_with_git:1}
./autogen.sh
%endif
%configure \
	--enable-purple \
%if !0%{?_without_telepathy:1}
	--enable-telepathy
%else
	--disable-telepathy
%endif
make %{_smp_mflags}
make %{_smp_mflags} check


%install
%makeinstall
find %{buildroot} -type f -name "*.la" -delete -print
# Pidgin doesn't have 24 or 32 pixel icons
rm -f \
   %{buildroot}%{_datadir}/pixmaps/pidgin/protocols/24/sipe.png \
   %{buildroot}%{_datadir}/pixmaps/pidgin/protocols/32/sipe.png
%find_lang %{name}


%clean
rm -rf %{buildroot}


%files -n %{purple_plugin}
%defattr(-,root,root,-)
%doc AUTHORS ChangeLog COPYING NEWS README TODO
%{_libdir}/purple-2/libsipe.so


%if !0%{?_without_telepathy:1}
%files -n %{empathy_files}
%defattr(-,root,root,-)
%doc AUTHORS COPYING
%{_datadir}/empathy/icons/hicolor/*/apps/im-sipe.png
%{_datadir}/empathy/icons/hicolor/*/apps/im-sipe.svg


%files -n %{ktp_files}
%defattr(-,root,root,-)
%doc AUTHORS COPYING
%{_datadir}/telepathy/profiles/sipe.profile


%files -n %{telepathy_plugin}
%defattr(-,root,root,-)
%doc AUTHORS ChangeLog COPYING NEWS README TODO
%{_datadir}/dbus-1/services/*.sipe.service
%{_libexecdir}/telepathy-sipe
%endif


%files -n %{common_files} -f %{name}.lang
%defattr(-,root,root,-)


%files
%defattr(-,root,root,-)
%doc AUTHORS COPYING
%{_datadir}/pixmaps/pidgin/protocols/*/sipe.png
%{_datadir}/pixmaps/pidgin/protocols/*/sipe.svg


%changelog
* Wed Dec 11 2013 J. D. User <jduser@noreply.com> 1.17.3
- update to 1.17.3

* Sat Nov 30 2013 J. D. User <jduser@noreply.com> 1.17.2
- update to 1.17.2

* Sat Nov 16 2013 J. D. User <jduser@noreply.com> 1.17.1
- update to 1.17.1

* Sat Sep 21 2013 J. D. User <jduser@noreply.com> 1.17.0
- update to 1.17.0

* Sat Jul 13 2013 J. D. User <jduser@noreply.com> 1.16.1
- update to 1.16.1

* Fri Jun 14 2013 J. D. User <jduser@noreply.com> 1.16.0
- update to 1.16.0

* Thu May 16 2013 J. D. User <jduser@noreply.com> 1.15.1-*git*
- BR glib-2.0 >= 2.28.0 no longer required for Voice & Video features

* Sun Apr 07 2013 J. D. User <jduser@noreply.com> 1.15.1
- update to 1.15.1

* Fri Mar 29 2013 J. D. User <jduser@noreply.com> 1.15.0-*git*
- update package description texts

* Sat Mar 09 2013 J. D. User <jduser@noreply.com> 1.15.0
- update to 1.15.0

* Wed Dec 26 2012 J. D. User <jduser@noreply.com> 1.14.1
- update to 1.14.1

* Sun Dec 16 2012 J. D. User <jduser@noreply.com> 1.14.0
- update to 1.14.0

* Sun Sep 09 2012 J. D. User <jduser@noreply.com> 1.13.3-*git*
- BR telepathy-glib-devel >= 0.18.0

* Wed Sep 05 2012 J. D. User <jduser@noreply.com> 1.13.3-*git*
- BR telepathy-glib-devel >= 0.14.0

* Mon Aug 27 2012 J. D. User <jduser@noreply.com> 1.13.3-*git*
- add ktp-accounts-kcm-sipe package

* Sun Aug 26 2012 J. D. User <jduser@noreply.com> 1.13.3-*git*
- telepathy now requires glib-2.0 >= 2.22.0
- use "--without telepathy" to disable telepathy packages

* Fri Aug 24 2012 J. D. User <jduser@noreply.com> 1.13.3-*git*
- add empathy-sipe package

* Wed Aug 22 2012 J. D. User <jduser@noreply.com> 1.13.3-*git*
- add telepathy-sipe & sipe-common packages

* Sun Aug 19 2012 J. D. User <jduser@noreply.com> 1.13.3
- update to 1.13.3

* Sun Jun 10 2012 J. D. User <jduser@noreply.com> 1.13.2
- update to 1.13.2

* Mon Apr 09 2012 J. D. User <jduser@noreply.com> 1.13.1
- update to 1.13.1

* Wed Mar 14 2012 J. D. User <jduser@noreply.com> 1.13.0
- update to 1.13.0

* Mon Dec 12 2011 J. D. User <jduser@noreply.com> 1.12.0-*git*
- we do support Microsoft Lync Server 2010 now.

* Tue Dec 06 2011 J. D. User <jduser@noreply.com> 1.12.0-*git*
- update GPL2 license name

* Sat Nov 12 2011 J. D. User <jduser@noreply.com> 1.12.0-*git*
- add BR gmime-devel

* Mon Oct 31 2011 J. D. User <jduser@noreply.com> 1.12.0-*git*
- add BR nss-devel

* Mon Aug 29 2011 J. D. User <jduser@noreply.com> 1.12.0
- update to 1.12.0

* Wed Jun 22 2011 J. D. User <jduser@noreply.com> 1.11.2-*git*
- add "--with vv" option to enable Voice & Video features

* Tue Nov 02 2010 J. D. User <jduser@noreply.com> 1.11.2
- update to 1.11.2

* Sun Oct 24 2010 J. D. User <jduser@noreply.com> 1.11.1
- update to 1.11.1

* Sun Oct 04 2010 J. D. User <jduser@noreply.com> 1.11.0
- update to 1.11.0

* Fri Sep 02 2010 J. D. User <jduser@noreply.com> 1.10.1-*git*
- add (commented out) BR libnice-devel

* Sun Jun 27 2010 J. D. User <jduser@noreply.com> 1.10.1
- update to 1.10.1

* Mon Apr 12 2010 J. D. User <jduser@noreply.com> 1.10.0-*git*
- add (commented out) BR nss-devel

* Sun Apr 04 2010 J. D. User <jduser@noreply.com> 1.10.0
- update to 1.10.0

* Sun Mar 28 2010 J. D. User <jduser@noreply.com> 1.9.1-*git*
- changed --with/--without options to --enable/--disable

* Sun Mar 28 2010 J. D. User <jduser@noreply.com> 1.9.1-*git*
- removed --with-krb5 configure option as it is autodetected now

* Tue Mar 23 2010 J. D. User <jduser@noreply.com> 1.9.1-*git*
- add SVG icon

* Sat Mar 20 2010 J. D. User <jduser@noreply.com> 1.9.1-*git*
- add BR glib2-devel >= 2.12.0

* Wed Mar 17 2010 J. D. User <jduser@noreply.com> 1.9.1-*git*
- add tests to build

* Tue Mar 16 2010 J. D. User <jduser@noreply.com> 1.9.1
- update to 1.9.1

* Thu Mar 11 2010 J. D. User <jduser@noreply.com> 1.9.0-*git*
- add BR libxml2-devel

* Wed Mar 10 2010 J. D. User <jduser@noreply.com> 1.9.0
- update to 1.9.0

* Mon Mar 08 2010 J. D. User <jduser@noreply.com> 1.8.1-*git*
- increased libpurple build requisite to >= 2.4.0

* Sun Mar 07 2010 J. D. User <jduser@noreply.com> 1.8.1-*git*
- sync with RPM SPEC from contrib/OBS

* Sat Mar 06 2010 J. D. User <jduser@noreply.com> 1.8.1-*git*
- update package summary & description

* Tue Feb 16 2010 J. D. User <jduser@noreply.com> 1.8.1
- update to 1.8.1

* Sun Feb 07 2010 J. D. User <jduser@noreply.com> 1.8.0
- update to 1.8.0

* Thu Jan 14 2010 J. D. User <jduser@noreply.com> 1.7.1-*git*
- autogen.sh no longer runs configure

* Tue Dec 29 2009 J. D. User <jduser@noreply.com> 1.7.1-*git*
- add configure parameters for purple and telepathy

* Sat Dec 12 2009 J. D. User <jduser@noreply.com> 1.7.1-*git*
- add Epoch: for git packages to avoid update clash with official packages

* Mon Nov 19 2009 J. D. User <jduser@noreply.com> 1.7.1
- update to 1.7.1

* Mon Oct 28 2009 J. D. User <jduser@noreply.com> 1.7.0-*git*
- add missing Group: to purple-sipe

* Mon Oct 19 2009 J. D. User <jduser@noreply.com> 1.7.0
- update to 1.7.0

* Sun Oct 11 2009 J. D. User <jduser@noreply.com> 1.6.3-*git*
- move non-Pidgin files to new sub-package purple-sipe

* Sun Oct 11 2009 J. D. User <jduser@noreply.com> 1.6.3-*git*
- remove directory for emoticon theme icons

* Sun Oct 11 2009 J. D. User <jduser@noreply.com> 1.6.3-*git*
- libpurple protocol plugins are located under %{_libdir}/purple-2

* Mon Sep 28 2009 J. D. User <jduser@noreply.com> 1.6.3-*git*
- added directory for emoticon theme icons

* Wed Sep 09 2009 J. D. User <jduser@noreply.com> 1.6.3
- update to 1.6.3

* Fri Aug 28 2009 J. D. User <jduser@noreply.com> 1.6.2-*git*
- reduce libpurple-devel requirement to >= 2.3.1

* Mon Aug 24 2009 J. D. User <jduser@noreply.com> 1.6.2
- update to 1.6.2

* Fri Aug 21 2009 J. D. User <jduser@noreply.com> 1.6.1-*git*
- reduce libpurple-devel requirement to >= 2.4.1

* Mon Aug 17 2009 J. D. User <jduser@noreply.com> 1.6.1-*git*
- com_err.h only required for kerberos

* Tue Aug 11 2009 J. D. User <jduser@noreply.com> 1.6.0-*git*
- require libpurple-devel >= 2.5.0

* Sun Aug 09 2009 J. D. User <jduser@noreply.com> 1.6.0-*git*
- refactor configure parameters
- make kerberos configurable
- don't hard code prefix for git builds

* Sun Aug 09 2009 J. D. User <jduser@noreply.com> 1.6.0-*git*
- removed unnecessary zlib-devel

* Sat Aug 08 2009 J. D. User <jduser@noreply.com> 1.6.0-*git*
- fix prefix for git builds

* Sat Aug 01 2009 J. D. User <jduser@noreply.com> 1.6.0-*git*
- append -Wno-unused-parameter for GCC <4.4 compilation errors

* Thu Jul 30 2009 J. D. User <jduser@noreply.com> 1.6.0-*git*
- remove duplicate GPL2

* Thu Jul 30 2009 J. D. User <jduser@noreply.com> 1.6.0-*git*
- use "--with git" to build from git
- corrected download URL for release archive
- add missing BR gettext-devel

* Wed Jul 29 2009 J. D. User <jduser@noreply.com> 1.6.0-*git*
- use default rpmbuild CFLAGS also for git builds
- merge with SPEC files created by mricon & jberanek

* Tue Jul 28 2009 J. D. User <jduser@noreply.com> 1.6.0-*git*
- initial RPM SPEC example generated
