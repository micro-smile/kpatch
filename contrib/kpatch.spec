Name: kpatch
Summary: Dynamic kernel patching
Version: 0.7.1
License: GPLv2
Group: System Environment/Kernel
URL: http://github.com/dynup/kpatch
Release: 1%{?dist}
Source0: %{name}-%{version}.tar.gz

Requires: kmod bash
BuildRequires: gcc kernel-devel elfutils elfutils-devel
BuildRoot: %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)

# needed for the kernel specific module
%define KVER %(uname -r)

%description
kpatch is a Linux dynamic kernel patching tool which allows you to patch a
running kernel without rebooting or restarting any processes.  It enables
sysadmins to apply critical security patches to the kernel immediately, without
having to wait for long-running tasks to complete, users to log off, or
for scheduled reboot windows.  It gives more control over up-time without
sacrificing security or stability.


%package runtime
Summary: Dynamic kernel patching
Buildarch: noarch
Provides: %{name} = %{version}
%description runtime
kpatch is a Linux dynamic kernel patching tool which allows you to patch a
running kernel without rebooting or restarting any processes.  It enables
sysadmins to apply critical security patches to the kernel immediately, without
having to wait for long-running tasks to complete, users to log off, or
for scheduled reboot windows.  It gives more control over up-time without
sacrificing security or stability.


%package build
Requires: %{name}
Summary: Dynamic kernel patching
%description build
kpatch is a Linux dynamic kernel patching tool which allows you to patch a
running kernel without rebooting or restarting any processes.  It enables
sysadmins to apply critical security patches to the kernel immediately, without
having to wait for long-running tasks to complete, users to log off, or
for scheduled reboot windows.  It gives more control over up-time without
sacrificing security or stability.

%package %{KVER}
Requires: %{name}
Summary: Dynamic kernel patching
%description %{KVER}
kpatch is a Linux dynamic kernel patching tool which allows you to patch a
running kernel without rebooting or restarting any processes.  It enables
sysadmins to apply critical security patches to the kernel immediately, without
having to wait for long-running tasks to complete, users to log off, or
for scheduled reboot windows.  It gives more control over up-time without
sacrificing security or stability.


%prep
%setup -q

%build
make %{_smp_mflags}

%install
rm -rf %{buildroot}

make install PREFIX=/%{_usr} DESTDIR=%{buildroot}

%clean
rm -rf %{buildroot}

%files runtime
%defattr(-,root,root,-)
%doc COPYING README.md
%{_sbindir}/kpatch
%{_mandir}/man1/kpatch.1*
%{_usr}/lib/systemd/system/*
%{_sysconfdir}/init/kpatch.conf

%files %{KVER}
%defattr(-,root,root,-)
%{_usr}/lib/kpatch/%{KVER}

%files build
%defattr(-,root,root,-)
%{_bindir}/*
%{_libexecdir}/*
%{_datadir}/%{name}
%{_mandir}/man1/kpatch-build.1*

%changelog
* Wed Jul 24 2019 Josh Poimboeuf <jpoimboe@redhat.com> - 0.7.1
- Fix several powerpc-specific bugs, including two which can result in kernel
  panics
- Use rpmbuild --nodeps for installing srpm on Fedora/RHEL
- Fix inconsistent unit test failures for FAIL tests

* Thu Jul 18 2019 Artem Savkov <asavkov@redhat.com> - 0.7.0
- Multiple memory leak fixes in kpatch-build
- livepatch-patch-hook compatability fixes for kernels 5.1+
- Making kpatch-build compatible with custom gcc names
- Added rhel-rebased integration tests
- kpatch.service will no longer unload modules on stop
- kpatch load will no longer fail if a module is already loaded and enabled
- kpatch-build will now check for *_fixup section changes on ppc64le and will
  fail on such changes
- Add support for R_X86_64_PLT32
- don't allow jump labels
- ppc64le-specific kpatch-build fixes

* Fri Apr 12 2019 Joe Lawrence <joe.lawrence@redhat.com> - 0.6.3
- Lots of integration test work
- Better support for building out-of-tree modules
- Updated manpage options, drop deprecated distro specific mentions
- README.md updates for shadow variables, out-of-tree modules
- Fix core module compilation with CONFIG_HAVE_ARCH_PREL32_RELOCATIONS
- kpatch-build detects and abort on unsupported options
  GCC_PLUGIN_LATENT_ENTROPY, GCC_PLUGIN_RANDSTRUCT
- Fix patch linking with 4.20+
- Other minor shellcheck and kpatch-build fixups

* Tue Oct 2 2018 Joe Lawrence <joe.lawrence@redhat.com> - 0.6.2
- ppc64le: relax .text section addralign value check
- gcc8: unit-tests
- gcc8: support parent/child symbol relations
- gcc8: handle functions changing subsection
- gcc8: consider ".text.hot" sections bundleable
- kpatch-build: bugfix for less aggressive clean build-cache
- ubuntu: remove "-signed" substring from the kernel source package name
- ubuntu: explicitly note elfutils dependency
- upstream 4.18: unit-tests
- upstream 4.18: KCFLAGS -mcount-record support support
- RHEL-8: don't care who provides yumdownloader
- RHEL-8: account for quirky SRPM / release name conventions

* Tue May 29 2018 Joe Lawrence <joe.lawrence@redhat.com> - 0.6.1
- Increase the transition timeout, helpful for large CPU count systems
- Miscellaneous unit testing, ppc64, etc. fixes

* Mon Apr 22 2018 Josh Poimboeuf <jpoimboe@redhat.com> - 0.6.0
- Support and converted to livepatch-style hooks.
- Lots of misc bugfixes and cleanups
- Manpage, README.md fixups
- More PPC64 work
- "Undefined reference" build failure rework
- Livepatch disable retries
- New unit testing framework

* Thu Dec 21 2017 Josh Poimboeuf <jpoimboe@redhat.com> - 0.5.0
- Basic ppc64le support
- kpatch: load automatically signals stalled processes after a timeout
- kpatch: list shows stalled processes
- kpatch: signal signals stalled processes
- kpatch-build: multiple source patches can be combined into a single binary patch module
- kpatch-build: -n|--name option for giving a custom name to the patch module
- kpatch-build: additional -d options for more verbose debug modes
- The module prefix is now either livepatch- or kpatch- depending on the underlying patching technology

* Mon Mar 13 2017 Josh Poimboeuf <jpoimboe@redhat.com> - 0.4.0
- The tools underlying kpatch-build have been made more modular, in preparation for making create-diff-object more generally useful to other use cases (kernel livepatch, Xen live patching, user space patching).
- Support for all new upstream kernels up to 4.10.
- KASLR support.
- Many other bug fixes and improvements.

* Thu Oct 11 2016 Jessica Yu - 0.3.4
- bump version to 0.3.4

* Fri Aug 19 2016 Josh Poimboeuf <jpoimboe@redhat.com> - 0.3.3
- bump version to 0.3.3

* Thu Feb 18 2016 Josh Poimboeuf <jpoimboe@redhat.com> - 0.3.2
- bump version to 0.3.2

* Thu Nov 19 2015 Josh Poimboeuf <jpoimboe@redhat.com> - 0.3.1
- Get kernel version from vmlinux if the kernel source tree is used

* Wed Nov 18 2015 Josh Poimboeuf <jpoimboe@redhat.com> - 0.3.0
- kpatch-build: fix gcc_version_check: both "GNU" and "GCC" are possible

* Wed Dec 3 2014 Josh Poimboeuf <jpoimboe@redhat.com> - 0.2.2-1
- rebased to current version

* Tue Sep 2 2014 Josh Poimboeuf <jpoimboe@redhat.com> - 0.2.1-1
- rebased to current version

* Mon Jul 28 2014 Josh Poimboeuf <jpoimboe@redhat.com> - 0.1.9-1
- moved core module to /usr/lib/kpatch
- rebased to current version

* Mon Jul 07 2014 Udo Seidel <udoseidel@gmx.de> - 0.1.7-1
- rebased to current version

* Sat May 24 2014 Udo Seidel <udoseidel@gmx.de> - 0.1.1-1
- rebased to current version

* Thu Apr 10 2014 Udo Seidel <udoseidel@gmx.de> - 0.0.1-3
- added dracut module

* Tue Mar 25 2014 Udo Seidel <udoseidel@gmx.de> - 0.0.1-2
- added man pages

* Sat Mar 22 2014 Udo Seidel <udoseidel@gmx.de> - 0.0.1-1
- initial release
