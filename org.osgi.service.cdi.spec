Name:		org.osgi.service.cdi
Version:	1.0.1
Release:	1
Summary:	OSGi CDI Integration API
Group:		Development/Java
License:	ASL 2.0
URL:		https://docs.osgi.org/
Source0:	https://repo1.maven.org/maven2/org/osgi/org.osgi.service.cdi/%{version}/org.osgi.service.cdi-%{version}-sources.jar
Source1:	https://raw.githubusercontent.com/osgi/osgi/r8-cmpn-final/LICENSE#/org.osgi.service.cdi-%{version}-LICENSE

BuildArch:	noarch
BuildRequires:	python
# Literal, so the first rpmbuild -bs records them before sysjar is installed.
BuildRequires:	maven
BuildRequires:	java-current-devel
BuildRequires:	mvn(javax.enterprise:cdi-api)
# javax.inject and jakarta-inject both provide mvn(javax.inject:javax.inject).
# The package name selects the jar CDI 2.0 was built against.
BuildRequires:	javax.inject
BuildRequires:	mvn(org.osgi:osgi.core)
BuildRequires:	mvn(org.osgi:osgi.annotation)
BuildRequires:	mvn(org.osgi:org.osgi.namespace.extender)
BuildRequires:	mvn(org.osgi:org.osgi.namespace.implementation)
BuildSystem:	maven
BuildOption(install):	--file-name %{name}

%description
OSGi CDI Integration 1.0.1. Annotation literals extend
javax.enterprise.util.AnnotationLiteral from CDI 2.0, and the
qualifiers use javax.inject.Qualifier. DTOs extend org.osgi.dto.DTO
from OSGi Core 6 and reference framework service DTOs. The extender
requirement inlines osgi.extender named osgi.cdi at version 1.0, and
the implementation requirement inlines osgi.implementation named
osgi.cdi at version 1.0. The service and annotation packages are
version 1.0.1. The other packages are version 1.0.0. Versioning
annotations are compile-time only. This build targets Java 8.

%prep
%setup -q -c -T
# The builders' rpmuncompress passes a sources jar to tar.
python - %{SOURCE0} <<'PY'
import sys
import zipfile
zipfile.ZipFile(sys.argv[1]).extractall(".")
PY
rm -rf META-INF
cp -p %{SOURCE1} LICENSE
mkdir -p src/main/java
mv org src/main/java/
python - <<'PY'
from pathlib import Path
root = Path("src/main/java")
javas = sorted(path.relative_to(root).as_posix() for path in root.rglob("*.java"))
expected = [
    "org/osgi/service/cdi/CDIConstants.java",
    "org/osgi/service/cdi/ComponentType.java",
    "org/osgi/service/cdi/ConfigurationPolicy.java",
    "org/osgi/service/cdi/MaximumCardinality.java",
    "org/osgi/service/cdi/ReferencePolicy.java",
    "org/osgi/service/cdi/ReferencePolicyOption.java",
    "org/osgi/service/cdi/ServiceScope.java",
    "org/osgi/service/cdi/annotations/Bean.java",
    "org/osgi/service/cdi/annotations/BeanPropertyType.java",
    "org/osgi/service/cdi/annotations/Beans.java",
    "org/osgi/service/cdi/annotations/ComponentProperties.java",
    "org/osgi/service/cdi/annotations/ComponentScoped.java",
    "org/osgi/service/cdi/annotations/FactoryComponent.java",
    "org/osgi/service/cdi/annotations/MinimumCardinality.java",
    "org/osgi/service/cdi/annotations/PID.java",
    "org/osgi/service/cdi/annotations/PIDs.java",
    "org/osgi/service/cdi/annotations/PrototypeRequired.java",
    "org/osgi/service/cdi/annotations/Reference.java",
    "org/osgi/service/cdi/annotations/Reluctant.java",
    "org/osgi/service/cdi/annotations/RequireCDIExtender.java",
    "org/osgi/service/cdi/annotations/RequireCDIImplementation.java",
    "org/osgi/service/cdi/annotations/Service.java",
    "org/osgi/service/cdi/annotations/ServiceInstance.java",
    "org/osgi/service/cdi/annotations/SingleComponent.java",
    "org/osgi/service/cdi/annotations/package-info.java",
    "org/osgi/service/cdi/package-info.java",
    "org/osgi/service/cdi/propertytypes/BeanPropertyException.java",
    "org/osgi/service/cdi/propertytypes/ExportedService.java",
    "org/osgi/service/cdi/propertytypes/ServiceDescription.java",
    "org/osgi/service/cdi/propertytypes/ServiceRanking.java",
    "org/osgi/service/cdi/propertytypes/ServiceVendor.java",
    "org/osgi/service/cdi/propertytypes/package-info.java",
    "org/osgi/service/cdi/reference/BeanServiceObjects.java",
    "org/osgi/service/cdi/reference/BindBeanServiceObjects.java",
    "org/osgi/service/cdi/reference/BindService.java",
    "org/osgi/service/cdi/reference/BindServiceReference.java",
    "org/osgi/service/cdi/reference/package-info.java",
    "org/osgi/service/cdi/runtime/CDIComponentRuntime.java",
    "org/osgi/service/cdi/runtime/dto/ActivationDTO.java",
    "org/osgi/service/cdi/runtime/dto/ComponentDTO.java",
    "org/osgi/service/cdi/runtime/dto/ComponentInstanceDTO.java",
    "org/osgi/service/cdi/runtime/dto/ConfigurationDTO.java",
    "org/osgi/service/cdi/runtime/dto/ContainerDTO.java",
    "org/osgi/service/cdi/runtime/dto/ExtensionDTO.java",
    "org/osgi/service/cdi/runtime/dto/ReferenceDTO.java",
    "org/osgi/service/cdi/runtime/dto/package-info.java",
    "org/osgi/service/cdi/runtime/dto/template/ActivationTemplateDTO.java",
    "org/osgi/service/cdi/runtime/dto/template/ComponentTemplateDTO.java",
    "org/osgi/service/cdi/runtime/dto/template/ConfigurationTemplateDTO.java",
    "org/osgi/service/cdi/runtime/dto/template/ContainerTemplateDTO.java",
    "org/osgi/service/cdi/runtime/dto/template/ExtensionTemplateDTO.java",
    "org/osgi/service/cdi/runtime/dto/template/ReferenceTemplateDTO.java",
    "org/osgi/service/cdi/runtime/dto/template/package-info.java",
    "org/osgi/service/cdi/runtime/package-info.java",
]
if javas != expected:
    raise SystemExit("java files changed")
if list(Path(".").rglob("module-info.java")) or list(Path(".").rglob("*.class")):
    raise SystemExit("unexpected input")
license_text = Path("LICENSE").read_text(encoding="utf-8")
if "Apache License" not in license_text or "Version 2.0" not in license_text:
    raise SystemExit("LICENSE is not Apache 2.0")
header = (root / "org/osgi/service/cdi/CDIConstants.java").read_text(encoding="utf-8")
if "SPDX-License-Identifier: Apache-2.0" not in header or "Licensed under the Apache License, Version 2.0" not in header:
    raise SystemExit("source license header changed")

Path("pom.xml").write_text("""<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0">
  <modelVersion>4.0.0</modelVersion>
  <groupId>org.osgi</groupId>
  <artifactId>org.osgi.service.cdi</artifactId>
  <version>%{version}</version>
  <packaging>jar</packaging>
  <name>OSGi CDI Integration</name>
  <description>OSGi CDI Integration %{version}, packaged without a parent POM.</description>
  <url>https://docs.osgi.org/</url>
  <licenses>
    <license>
      <name>Apache-2.0</name>
      <url>https://www.apache.org/licenses/LICENSE-2.0</url>
    </license>
  </licenses>
  <properties>
    <project.build.sourceEncoding>UTF-8</project.build.sourceEncoding>
    <maven.compiler.release>8</maven.compiler.release>
  </properties>
  <dependencies>
    <dependency>
      <groupId>javax.enterprise</groupId>
      <artifactId>cdi-api</artifactId>
      <version>2.0.SP1</version>
    </dependency>
    <dependency>
      <groupId>javax.inject</groupId>
      <artifactId>javax.inject</artifactId>
      <version>1</version>
    </dependency>
    <dependency>
      <groupId>org.osgi</groupId>
      <artifactId>osgi.core</artifactId>
      <version>6.0.0</version>
    </dependency>
    <dependency>
      <groupId>org.osgi</groupId>
      <artifactId>osgi.annotation</artifactId>
      <version>8.1.0</version>
      <scope>provided</scope>
    </dependency>
    <dependency>
      <groupId>org.osgi</groupId>
      <artifactId>org.osgi.namespace.extender</artifactId>
      <version>1.0.1</version>
      <scope>provided</scope>
    </dependency>
    <dependency>
      <groupId>org.osgi</groupId>
      <artifactId>org.osgi.namespace.implementation</artifactId>
      <version>1.0.0</version>
      <scope>provided</scope>
    </dependency>
  </dependencies>
  <build>
    <plugins>
      <plugin>
        <groupId>org.apache.maven.plugins</groupId>
        <artifactId>maven-compiler-plugin</artifactId>
        <version>3.12.1</version>
        <configuration>
          <release>8</release>
        </configuration>
      </plugin>
      <plugin>
        <groupId>org.apache.maven.plugins</groupId>
        <artifactId>maven-jar-plugin</artifactId>
        <version>3.3.0</version>
        <configuration>
          <archive>
            <manifestEntries>
              <Automatic-Module-Name>org.osgi.service.cdi</Automatic-Module-Name>
              <Specification-Version>1.0</Specification-Version>
              <Implementation-Version>%{version}</Implementation-Version>
            </manifestEntries>
          </archive>
        </configuration>
      </plugin>
    </plugins>
  </build>
</project>
""", encoding="utf-8")
pom = Path("pom.xml").read_text(encoding="utf-8")
for needle in (
    "<artifactId>org.osgi.service.cdi</artifactId>",
    "<artifactId>cdi-api</artifactId>",
    "<artifactId>javax.inject</artifactId>",
    "<artifactId>osgi.core</artifactId>",
    "<artifactId>osgi.annotation</artifactId>",
    "<artifactId>org.osgi.namespace.extender</artifactId>",
    "<artifactId>org.osgi.namespace.implementation</artifactId>",
    "<version>%{version}</version>",
    "<release>8</release>",
    "</project.build.sourceEncoding>",
):
    if needle not in pom:
        raise SystemExit("pom missing " + needle)
if pom.count("<version>1.0.1</version>") != 2 or pom.count("<version>1.0.0</version>") != 1 or pom.count("<version>2.0.SP1</version>") != 1 or pom.count("<version>1</version>") != 1 or pom.count("<version>6.0.0</version>") != 1 or pom.count("<version>8.1.0</version>") != 1 or pom.count("<scope>provided</scope>") != 3:
    raise SystemExit("pom versions changed")
for needle in (
    "junit",
    "SNAPSHOT",
    "<source>",
    "<target>",
    "<parent>",
    "felix",
    "maven-bundle-plugin",
    "<artifactId>org.osgi.framework</artifactId>",
    "<artifactId>org.osgi.dto</artifactId>",
    "<artifactId>org.osgi.resource</artifactId>",
    "<version>1.0</version>",
    "<version>8.0.1</version>",
    "projectbuild.sourceEncoding",
    "<groupId>org.eclipse.ee4j</groupId>",
):
    if needle in pom:
        raise SystemExit("pom still contains " + needle)
PY

%build -a
java --module-path target/org.osgi.service.cdi-%{version}.jar --describe-module org.osgi.service.cdi > module-describe.txt
grep -q '^org\.osgi\.service\.cdi@' module-describe.txt || { cat module-describe.txt; exit 1; }
grep -q ' automatic$' module-describe.txt || { cat module-describe.txt; exit 1; }
python - <<'PY'
import zipfile
from pathlib import Path
jar = Path("target/org.osgi.service.cdi-%{version}.jar")
with zipfile.ZipFile(jar) as zf:
    classes = {name for name in zf.namelist() if name.endswith(".class")}
    required = {
        "org/osgi/service/cdi/CDIConstants.class",
        "org/osgi/service/cdi/ComponentType.class",
        "org/osgi/service/cdi/ConfigurationPolicy.class",
        "org/osgi/service/cdi/MaximumCardinality.class",
        "org/osgi/service/cdi/ReferencePolicy.class",
        "org/osgi/service/cdi/ReferencePolicyOption.class",
        "org/osgi/service/cdi/ServiceScope.class",
        "org/osgi/service/cdi/annotations/Bean.class",
        "org/osgi/service/cdi/annotations/BeanPropertyType$Literal.class",
        "org/osgi/service/cdi/annotations/BeanPropertyType.class",
        "org/osgi/service/cdi/annotations/Beans.class",
        "org/osgi/service/cdi/annotations/ComponentProperties$Literal.class",
        "org/osgi/service/cdi/annotations/ComponentProperties.class",
        "org/osgi/service/cdi/annotations/ComponentScoped$Literal.class",
        "org/osgi/service/cdi/annotations/ComponentScoped.class",
        "org/osgi/service/cdi/annotations/FactoryComponent$Literal.class",
        "org/osgi/service/cdi/annotations/FactoryComponent.class",
        "org/osgi/service/cdi/annotations/MinimumCardinality$Literal.class",
        "org/osgi/service/cdi/annotations/MinimumCardinality.class",
        "org/osgi/service/cdi/annotations/PID$Literal.class",
        "org/osgi/service/cdi/annotations/PID.class",
        "org/osgi/service/cdi/annotations/PIDs$Literal.class",
        "org/osgi/service/cdi/annotations/PIDs.class",
        "org/osgi/service/cdi/annotations/PrototypeRequired$Literal.class",
        "org/osgi/service/cdi/annotations/PrototypeRequired.class",
        "org/osgi/service/cdi/annotations/Reference$Any.class",
        "org/osgi/service/cdi/annotations/Reference$Literal.class",
        "org/osgi/service/cdi/annotations/Reference.class",
        "org/osgi/service/cdi/annotations/Reluctant$Literal.class",
        "org/osgi/service/cdi/annotations/Reluctant.class",
        "org/osgi/service/cdi/annotations/RequireCDIExtender.class",
        "org/osgi/service/cdi/annotations/RequireCDIImplementation.class",
        "org/osgi/service/cdi/annotations/Service$Literal.class",
        "org/osgi/service/cdi/annotations/Service.class",
        "org/osgi/service/cdi/annotations/ServiceInstance$Literal.class",
        "org/osgi/service/cdi/annotations/ServiceInstance.class",
        "org/osgi/service/cdi/annotations/SingleComponent$Literal.class",
        "org/osgi/service/cdi/annotations/SingleComponent.class",
        "org/osgi/service/cdi/annotations/package-info.class",
        "org/osgi/service/cdi/package-info.class",
        "org/osgi/service/cdi/propertytypes/BeanPropertyException.class",
        "org/osgi/service/cdi/propertytypes/ExportedService.class",
        "org/osgi/service/cdi/propertytypes/ServiceDescription.class",
        "org/osgi/service/cdi/propertytypes/ServiceRanking.class",
        "org/osgi/service/cdi/propertytypes/ServiceVendor.class",
        "org/osgi/service/cdi/propertytypes/package-info.class",
        "org/osgi/service/cdi/reference/BeanServiceObjects.class",
        "org/osgi/service/cdi/reference/BindBeanServiceObjects.class",
        "org/osgi/service/cdi/reference/BindService.class",
        "org/osgi/service/cdi/reference/BindServiceReference.class",
        "org/osgi/service/cdi/reference/package-info.class",
        "org/osgi/service/cdi/runtime/CDIComponentRuntime.class",
        "org/osgi/service/cdi/runtime/dto/ActivationDTO.class",
        "org/osgi/service/cdi/runtime/dto/ComponentDTO.class",
        "org/osgi/service/cdi/runtime/dto/ComponentInstanceDTO.class",
        "org/osgi/service/cdi/runtime/dto/ConfigurationDTO.class",
        "org/osgi/service/cdi/runtime/dto/ContainerDTO.class",
        "org/osgi/service/cdi/runtime/dto/ExtensionDTO.class",
        "org/osgi/service/cdi/runtime/dto/ReferenceDTO.class",
        "org/osgi/service/cdi/runtime/dto/package-info.class",
        "org/osgi/service/cdi/runtime/dto/template/ActivationTemplateDTO.class",
        "org/osgi/service/cdi/runtime/dto/template/ComponentTemplateDTO.class",
        "org/osgi/service/cdi/runtime/dto/template/ConfigurationTemplateDTO.class",
        "org/osgi/service/cdi/runtime/dto/template/ContainerTemplateDTO.class",
        "org/osgi/service/cdi/runtime/dto/template/ExtensionTemplateDTO.class",
        "org/osgi/service/cdi/runtime/dto/template/ReferenceTemplateDTO.class",
        "org/osgi/service/cdi/runtime/dto/template/package-info.class",
        "org/osgi/service/cdi/runtime/package-info.class",
    }
    if classes != required:
        raise SystemExit("class set " + " ".join(sorted(classes ^ required)))
    literal = zf.read("org/osgi/service/cdi/annotations/BeanPropertyType$Literal.class")
    if b"javax/enterprise/util/AnnotationLiteral" not in literal:
        raise SystemExit("annotation literal lost AnnotationLiteral")
    props = zf.read("org/osgi/service/cdi/annotations/ComponentProperties.class")
    if b"javax/inject/Qualifier" not in props:
        raise SystemExit("component properties lost Qualifier")
    reference = zf.read("org/osgi/service/cdi/annotations/Reference.class")
    if b"javax/enterprise/util/Nonbinding" not in reference or b"javax/inject/Qualifier" not in reference:
        raise SystemExit("reference lost a CDI type")
    objects = zf.read("org/osgi/service/cdi/reference/BeanServiceObjects.class")
    if b"org/osgi/framework/ServiceReference" not in objects:
        raise SystemExit("bean service objects lost ServiceReference")
    activation = zf.read("org/osgi/service/cdi/runtime/dto/ActivationDTO.class")
    if b"org/osgi/dto/DTO" not in activation or b"org/osgi/framework/dto/ServiceReferenceDTO" not in activation:
        raise SystemExit("activation DTO lost a type")
    runtime = zf.read("org/osgi/service/cdi/runtime/CDIComponentRuntime.class")
    if b"org/osgi/framework/Bundle" not in runtime:
        raise SystemExit("component runtime lost Bundle")
    extender = zf.read("org/osgi/service/cdi/annotations/RequireCDIExtender.class")
    if b"org/osgi/annotation/bundle/Requirement" not in extender or b"osgi.extender" not in extender or b"osgi.cdi" not in extender:
        raise SystemExit("extender requirement lost its name")
    if b"org/osgi/namespace/extender/ExtenderNamespace" in extender or b"1.0.1" in extender or b"1.0.0" in extender:
        raise SystemExit("extender requirement kept a type or the wrong version")
    implementation = zf.read("org/osgi/service/cdi/annotations/RequireCDIImplementation.class")
    if b"org/osgi/annotation/bundle/Requirement" not in implementation or b"osgi.implementation" not in implementation or b"osgi.cdi" not in implementation:
        raise SystemExit("implementation requirement lost its name")
    if b"org/osgi/namespace/implementation/ImplementationNamespace" in implementation or b"osgi.extender" in implementation or b"1.0.1" in implementation or b"1.0.0" in implementation:
        raise SystemExit("implementation requirement kept a type or the wrong version")
    for name in (
        "org/osgi/service/cdi/package-info.class",
        "org/osgi/service/cdi/annotations/package-info.class",
    ):
        data = zf.read(name)
        if b"org/osgi/annotation/versioning/Version" not in data or b"1.0.1" not in data:
            raise SystemExit("package version was not recorded")
    for name in (
        "org/osgi/service/cdi/propertytypes/package-info.class",
        "org/osgi/service/cdi/reference/package-info.class",
        "org/osgi/service/cdi/runtime/package-info.class",
        "org/osgi/service/cdi/runtime/dto/package-info.class",
        "org/osgi/service/cdi/runtime/dto/template/package-info.class",
    ):
        data = zf.read(name)
        if b"org/osgi/annotation/versioning/Version" not in data or b"1.0.0" not in data or b"1.0.1" in data:
            raise SystemExit("package version was not recorded")
    if any(b"org/osgi/namespace/extender/ExtenderNamespace" in zf.read(name) or b"org/osgi/namespace/implementation/ImplementationNamespace" in zf.read(name) for name in classes):
        raise SystemExit("namespace class was not inlined")
PY

%files -f .mfiles
%doc LICENSE
