#
# Conditional build:
%bcond_without	apidocs		# API documentation
#
Summary:	Concurrent Data Structers library
Summary(pl.UTF-8):	Biblioteka współbieżnych struktur danych (Concurrent Data Structures)
Name:		libcds
Version:	2.3.3
Release:	1
License:	Boost v1.0
Group:		Libraries
#Source0Download: https://github.com/khizmax/libcds/releases
Source0:	https://github.com/khizmax/libcds/archive/v%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	e2622b1334f271022140253e3557f0ae
URL:		https://github.com/khizmax/libcds
BuildRequires:	boost >= 1.50
BuildRequires:	cmake >= 3.0.2
%{?with_apidocs:BuildRequires:	doxygen}
BuildRequires:	libstdc++-devel >= 6:4.7
BuildRequires:	rpmbuild(macros) >= 1.605
BuildRequires:	rpm-build >= 4.6
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
The Concurrent Data Structures (CDS) library is a collection of
concurrent containers that don't require external (manual)
synchronization for shared access, and safe memory reclamation (SMR)
algorithms like Hazard Pointer and user-space RCU that is used as an
epoch-based SMR.

%description -l pl.UTF-8
Biblioteka CDS (Concurrent Data Structures - współbieżnych struktur
danych) to zbiór współbieżnych kontenerów, nie wymagających
zewnętrznej (ręcznej) synchronizacji dostępu współdzielonego oraz
algorytmy bezpiecznego zwalniania pamięci (SMR - Safe Memory
Reclamation), takie jak Hazard Pointer czy RCU w przestrzeni
użytkownika, używane jako SMR oparte na epokach.

%package devel
Summary:	Header files for CDS library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki CDS
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Header files for CDS library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki CDS.

%package static
Summary:	Static CDS library
Summary(pl.UTF-8):	Statyczna biblioteka CDS
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static CDS library.

%description static -l pl.UTF-8
Statyczna biblioteka CDS.

%package apidocs
Summary:	API documentation for CDS library
Summary(pl.UTF-8):	Dokumentacja API biblioteki CDS
Group:		Documentation
BuildArch:	noarch

%description apidocs
API documentation for CDS library.

%description apidocs -l pl.UTF-8
Dokumentacja API biblioteki CDS.

%prep
%setup -q

%build
install -d build
cd build
%cmake ..

%{__make}

%if %{with apidocs}
cd ..
DOXYPRJ_ROOT=$(pwd) \
doxygen doxygen/cds.doxy
%endif

%install
rm -rf $RPM_BUILD_ROOT

%{__make} -C build install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc LICENSE change.log readme.md thanks
%{_libdir}/libcds.so.*.*.*

%files devel
%defattr(644,root,root,755)
%{_libdir}/libcds.so
%{_includedir}/cds
%{_libdir}/cmake/LibCDS

%files static
%defattr(644,root,root,755)
%{_libdir}/libcds-s.a

%if %{with apidocs}
%files apidocs
%defattr(644,root,root,755)
%doc doc/cds-api/*.{css,html,js,png}
%endif
