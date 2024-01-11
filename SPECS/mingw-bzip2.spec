%?mingw_package_header

Name:           mingw-bzip2
Version:        1.0.6
Release:        14%{?dist}
Summary:        MinGW port of bzip2 file compression utility

License:        BSD
Group:          Development/Libraries
URL:            http://www.bzip.org/
Source0:        http://www.bzip.org/%{version}/bzip2-%{version}.tar.gz

BuildArch:      noarch
ExclusiveArch: %{ix86} x86_64

Patch6:         bzip2-1.0.4-bzip2recover.patch

Patch10:        mingw32-bzip2-1.0.5-slash.patch

Patch12:        bzip2-1.0.5-autoconfiscated.patch

# Export all symbols using the cdecl calling convention instead of
# stdcall as it is also done by various other downstream distributors
# (like mingw.org and gnuwin32) and it resolves various autoconf and
# cmake detection issues (RHBZ #811909, RHBZ #812573)
# Patch is taken from the gnuwin32 project
Patch13:        bzip2-use-cdecl-calling-convention.patch

BuildRequires:  mingw32-filesystem >= 95
BuildRequires:  mingw64-filesystem >= 95
BuildRequires:  mingw32-gcc
BuildRequires:  mingw64-gcc
BuildRequires:  mingw32-binutils
BuildRequires:  mingw64-binutils
BuildRequires:  autoconf, automake, libtool


%description
Bzip2 is a freely available, patent-free, high quality data compressor.
Bzip2 compresses files to within 10 to 15 percent of the capabilities
of the best techniques available.  However, bzip2 has the added benefit
of being approximately two times faster at compression and six times
faster at decompression than those techniques.  Bzip2 is not the
fastest compression utility, but it does strike a balance between speed
and compression capability.

This package contains development tools and libraries for use when
cross-compiling Windows software.

# Win32
%package -n mingw32-bzip2
Summary:        32 Bit version of bzip2 for Windows

%description -n mingw32-bzip2
Bzip2 is a freely available, patent-free, high quality data compressor.
Bzip2 compresses files to within 10 to 15 percent of the capabilities
of the best techniques available.  However, bzip2 has the added benefit
of being approximately two times faster at compression and six times
faster at decompression than those techniques.  Bzip2 is not the
fastest compression utility, but it does strike a balance between speed
and compression capability.

This package contains development tools and libraries for use when
cross-compiling Windows software.

%package -n mingw32-bzip2-static
Summary:        Static library for mingw32-bzip2 development
Requires:       mingw32-bzip2 = %{version}-%{release}

%description -n mingw32-bzip2-static
Static library for mingw32-bzip2 development.

# Win64
%package -n mingw64-bzip2
Summary:        64 Bit version of bzip2 for Windows

%description -n mingw64-bzip2
Bzip2 is a freely available, patent-free, high quality data compressor.
Bzip2 compresses files to within 10 to 15 percent of the capabilities
of the best techniques available.  However, bzip2 has the added benefit
of being approximately two times faster at compression and six times
faster at decompression than those techniques.  Bzip2 is not the
fastest compression utility, but it does strike a balance between speed
and compression capability.

This package contains development tools and libraries for use when
cross-compiling Windows software.

%package -n mingw64-bzip2-static
Summary:        Static library for mingw64-bzip2 development
Requires:       mingw64-bzip2 = %{version}-%{release}

%description -n mingw64-bzip2-static
Static library for mingw64-bzip2 development.


%?mingw_debug_package


%prep
%setup -q -n bzip2-%{version}

%patch6 -p1 -b .bz2recover

%patch10 -p1 -b .slash

%patch12 -p1 -b .autoconfiscated

%patch13 -p1 -b .cdecl

sh ./autogen.sh


%build
%mingw_configure
%mingw_make %{?_smp_mflags}


%install
%mingw_make install DESTDIR=$RPM_BUILD_ROOT

# The binaries which are symlinks contain the full buildroot
# name in the symlink, so replace those.
for dir in $RPM_BUILD_ROOT%{mingw32_bindir} $RPM_BUILD_ROOT%{mingw64_bindir} ; do
pushd $dir
rm bzcmp.exe bzegrep.exe bzfgrep.exe bzless.exe
ln -s bzdiff bzcmp
ln -s bzgrep bzegrep
ln -s bzgrep bzfgrep
ln -s bzmore bzless
popd
done


# Remove the manpages, they're duplicates of the native package,
# and located in the wrong place anyway.
rm -r $RPM_BUILD_ROOT%{mingw32_mandir}/man1
rm -r $RPM_BUILD_ROOT%{mingw64_mandir}/man1

# Remove libtool .la files.
rm $RPM_BUILD_ROOT%{mingw32_libdir}/libbz2.la
rm $RPM_BUILD_ROOT%{mingw64_libdir}/libbz2.la

# Win32
%files -n mingw32-bzip2
%doc COPYING
%{mingw32_bindir}/libbz2-1.dll
%{mingw32_bindir}/bunzip2.exe
%{mingw32_bindir}/bzcat.exe
%{mingw32_bindir}/bzcmp
%{mingw32_bindir}/bzdiff
%{mingw32_bindir}/bzegrep
%{mingw32_bindir}/bzfgrep
%{mingw32_bindir}/bzgrep
%{mingw32_bindir}/bzip2.exe
%{mingw32_bindir}/bzip2recover.exe
%{mingw32_bindir}/bzless
%{mingw32_bindir}/bzmore
%{mingw32_includedir}/bzlib.h
%{mingw32_libdir}/libbz2.dll.a
%{mingw32_libdir}/pkgconfig/bzip2.pc

%files -n mingw32-bzip2-static
%{mingw32_libdir}/libbz2.a

# Win64
%files -n mingw64-bzip2
%doc COPYING
%{mingw64_bindir}/libbz2-1.dll
%{mingw64_bindir}/bunzip2.exe
%{mingw64_bindir}/bzcat.exe
%{mingw64_bindir}/bzcmp
%{mingw64_bindir}/bzdiff
%{mingw64_bindir}/bzegrep
%{mingw64_bindir}/bzfgrep
%{mingw64_bindir}/bzgrep
%{mingw64_bindir}/bzip2.exe
%{mingw64_bindir}/bzip2recover.exe
%{mingw64_bindir}/bzless
%{mingw64_bindir}/bzmore
%{mingw64_includedir}/bzlib.h
%{mingw64_libdir}/libbz2.dll.a
%{mingw64_libdir}/pkgconfig/bzip2.pc

%files -n mingw64-bzip2-static
%{mingw64_libdir}/libbz2.a


%changelog
* Tue Dec  1 2020 Uri Lublin <uril@redhat.com> - 1.0.6-14
- rebuilt

* Tue Jun  9 2020 Uri Lublin <uril@redhat.com> - 1.0.6-13
- Rebuild
  Related: rhbz#1841952

* Tue Aug 13 2019 Victor Toso <victortoso@redhat.com> - 1.0.6-12
- Metadata: Don't refer to Fedora on Red Hat package
- Resolves: rhbz#1704074

* Tue Aug 14 2018 Victor Toso <victortoso@redhat.com> - 1.0.6-11
- ExclusiveArch: i686, x86_64
- Related: rhbz#1615874

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.6-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.6-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.6-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.6-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.6-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.6-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.6-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.6-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Apr 25 2012 Erik van Pienbroek <epienbro@fedoraproject.org> - 1.0.6-1
- Update to 1.0.6
- Export all symbols using the cdecl calling convention instead of
  stdcall as it is also done by various other downstream distributors
  (like mingw.org and gnuwin32) and it resolves various autoconf and
  cmake detection issues (RHBZ #811909, RHBZ #812573)
- Added -static subpackages (RHBZ #665539)

* Fri Mar 16 2012 Erik van Pienbroek <epienbro@fedoraproject.org> - 1.0.5-13
- Added win64 support (contributed by Jay Higley)
- Added the autoconf patch from http://ftp.suse.com/pub/people/sbrabec/bzip2/
- Dropped some unneeded patches
- Dropped the non-implementated testsuite pieces
- Bundle the pkgconfig files

* Wed Mar 07 2012 Erik van Pienbroek <epienbro@fedoraproject.org> - 1.0.5-12
- Renamed the source package to mingw-bzip2 (RHBZ #800847)
- Use mingw macros without leading underscore
- Dropped unneeded RPM tags

* Mon Feb 27 2012 Erik van Pienbroek <epienbro@fedoraproject.org> - 1.0.5-11
- Rebuild against the mingw-w64 toolchain

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.5-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.5-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.5-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.5-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Fri Feb 20 2009 Richard W.M. Jones <rjones@redhat.com> - 1.0.5-6
- Rebuild for mingw32-gcc 4.4

* Thu Dec 18 2008 Richard Jones <rjones@redhat.com> - 1.0.5-5
- Include the LICENSE file in doc section.

* Sat Nov 22 2008 Richard Jones <rjones@redhat.com> - 1.0.5-4
- Rename the implib as libbz2.dll.a so that libtool can find it.

* Wed Oct 29 2008 Richard Jones <rjones@redhat.com> - 1.0.5-3
- Fix mixed spaces/tabs in specfile.

* Fri Oct 10 2008 Richard Jones <rjones@redhat.com> - 1.0.5-2
- Allow the tests to be disabled selectively.

* Thu Sep 25 2008 Richard Jones <rjones@redhat.com> - 1.0.5-1
- Initial RPM release.
