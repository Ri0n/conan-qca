# conan-qca
Conan packages for Qt Cryptographic Architecture

To build with Visual Studio 2019 (compiler version 16)

```
conan create . qca/testing -s compiler="Visual Studio" -s compiler.version=16
```

Or something like this

```
set CONAN_VISUAL_VERSIONS=16   # for cmd
$Env:CONAN_VISUAL_VERSIONS=16  # for PS
python.exe build.py
```
