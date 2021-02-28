#
# Conditional build:
%bcond_without	apidocs		# do not build and package API docs
#
Summary:	C++ Reflection Library
Name:		rttr
Version:	0.9.6
Release:	1
License:	MIT
Group:		Libraries
Source0:	https://github.com/rttrorg/rttr/archive/v%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	611c7062a9da181ee1cee012048a0640
URL:		https://www.rttr.org/
BuildRequires:	cmake
%{?with_apidocs:BuildRequires:	doxygen}
BuildRequires:	ninja
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
RTTR stands for Run Time Type Reflection. It describes the ability of
a computer program to introspect and modify an object at runtime. It
is also the name of the library itself, which is written in C++ and
released as open source library. You can find more information on:
www.rttr.org

%package devel
Summary:	Header files for %{name} library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki %{name}
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Header files for %{name} library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki %{name}.

%package apidocs
Summary:	API documentation for %{name} library
Summary(pl.UTF-8):	Dokumentacja API biblioteki %{name}
Group:		Documentation
# if not arch-dependent
BuildArch:	noarch

%description apidocs
API documentation for %{name} library.

%description apidocs -l pl.UTF-8
Dokumentacja API biblioteki %{name}.

%prep
%setup -q

%build
mkdir -p build
cd build
%cmake .. \
	-G Ninja \
	%cmake_on_off apidocs BUILD_DOCUMENTATION \
	-DBUILD_UNIT_TESTS:BOOL=OFF \
	-DBUILD_EXAMPLES:BOOL=OFF \
	-DBUILD_BENCHMARKS:BOOL=OFF

%ninja_build

%install
rm -rf $RPM_BUILD_ROOT

%ninja_install -C build

%{__rm} -r $RPM_BUILD_ROOT%{_prefix}/doc

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc README.md
%attr(755,root,root) %{_libdir}/librttr_core.so.*.*.*

%files devel
%defattr(644,root,root,755)
%doc ChangeLog.md
%attr(755,root,root) %{_libdir}/librttr_core.so
%{_includedir}/rttr
%{_datadir}/rttr

%if %{with apidocs}
%files apidocs
%defattr(644,root,root,755)
%doc build/doc/rttr-0-9-6/*
%endif
