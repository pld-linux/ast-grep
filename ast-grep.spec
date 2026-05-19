%define		crates_ver	%{version}

Summary:	Tool for code structural search, lint and rewriting
Name:		ast-grep
Version:	0.42.3
Release:	1
License:	MIT
Group:		Applications
Source0:	https://github.com/ast-grep/ast-grep/archive/%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	b562e6d9dd1e3ea361baebcb527b8c5c
Source1:	%{name}-crates-%{crates_ver}.tar.xz
# Source1-md5:	db5e2bbd8f5409be4be4ba994772332e
URL:		https://ast-grep.github.io/
BuildRequires:	cargo
BuildRequires:	rpmbuild(macros) >= 2.050
BuildRequires:	rust >= 1.79
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
%{?rust_req}
ExclusiveArch:	%{rust_arches}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
ast-grep is an abstract syntax tree based tool to search code by
pattern code. Think of it as your old-friend grep, but matching AST
nodes instead of text. You can write patterns as if you are writing
ordinary code. It will match all code that has the same syntactical
structure.

%prep
%setup -q -a1

%{__mv} ast-grep-%{crates_ver}/* .

# use our offline registry
export CARGO_HOME="$(pwd)/.cargo"

mkdir -p "$CARGO_HOME"
cat >.cargo/config <<EOF
[source.crates-io]
registry = 'https://github.com/rust-lang/crates.io-index'
replace-with = 'vendored-sources'

[source.vendored-sources]
directory = '$PWD/vendor'
EOF

%build
export CARGO_HOME="$(pwd)/.cargo"

%cargo_build --frozen --package ast-grep

%install
rm -rf $RPM_BUILD_ROOT
export CARGO_HOME="$(pwd)/.cargo"

%cargo_install --frozen --root $RPM_BUILD_ROOT%{_prefix} --path "$(pwd)/crates/cli"

%{__rm} $RPM_BUILD_ROOT%{_prefix}/bin/sg

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc CHANGELOG.md LICENSE README.md
%attr(755,root,root) %{_bindir}/ast-grep
