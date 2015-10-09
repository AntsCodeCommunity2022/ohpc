#----------------------------------------------------------------------------bh-
# This RPM .spec file is part of the OpenHPC project.
#
# It may have been modified from the default version supplied by the underlying
# release package (if available) in order to apply patches, perform customized
# build/install configurations, and supply additional files to support
# desired integration conventions.
#
#----------------------------------------------------------------------------eh-

%include %{_sourcedir}/OHPC_macros

Name:           docs%{PROJ_DELIM}
Version:        1.0
Release:        1
Summary:        OpenHPC documentation
License:        BSD-3-Clause
Group:          ohpc/admin
Source0:        docs-ohpc.tar
BuildRequires:  texlive-latex
BuildRequires:  texlive-caption
BuildRequires:  texlive-colortbl
BuildRequires:  texlive-fancyhdr
BuildRequires:  texlive-mdwtools
BuildRequires:  texlive-multirow
BuildRequires:  texlive-draftwatermark
BuildRequires:  latexmk
BuildRequires:  git
Requires:       make

%define debug_package %{nil}

BuildRoot:     %{_tmppath}/%{name}-%{version}-build
DocDir:        %{OHPC_PUB}/doc/contrib

%description 

This guide presents a simple cluster installation procedure using components
from the OpenHPC software stack.

%prep
%setup -n docs-ohpc

%build
%if 0%{?suse_version}
%define source_path recipes/install/sles12/vanilla
%else
%if 0%{?rhel_version} || 0%{?centos_version}
%define source_path recipes/install/centos7.1/vanilla
%endif
%endif

cd %{source_path}
make

# Include convenience recipe script(s)

../../parse_doc.pl steps.tex > fsp_vanilla_recipe.sh


%install

%{__mkdir_p} %{buildroot}%{OHPC_PUB}/doc
%{__mkdir_p} %{buildroot}%{OHPC_PUB}/doc/recipes/vanilla
install -m 0644 -p docs/recipes/install/ChangeLog %{buildroot}/%{OHPC_PUB}/doc/ChangeLog
install -m 0644 -p docs/recipes/install/Release_Notes.txt %{buildroot}/%{OHPC_PUB}/doc/Release_Notes.txt
install -m 0644 -p %{source_path}/steps.pdf %{buildroot}/%{OHPC_PUB}/doc/Install_guide.pdf 
install -m 0755 -p %{source_path}/fsp_vanilla_recipe.sh %{buildroot}/%{OHPC_PUB}/doc/recipes/vanilla/recipe.sh

install -m 0644 -p %{source_path}/../input.local.template %{buildroot}/%{OHPC_PUB}/doc/recipes/vanilla/input.local

%{__mkdir_p} ${RPM_BUILD_ROOT}/%{_docdir}

%files
%defattr(-,root,root)
%dir %{OHPC_HOME}
%{OHPC_PUB}
%doc docs/LICENSE

%changelog
