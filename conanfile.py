import os

from conans import ConanFile, tools, CMake
from conans.tools import replace_in_file

class QcaConan(ConanFile):
    name = "qca"
    description = "Qt Cryptographic Architecture"
    version = "2.2.0"
    license = "LGPL 2.1"
    url = "https://github.com/KDE/qca"
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True]}
    default_options = "shared=True"
    generators = "cmake_find_package"
    requires = "Qt/5.11.0@bincrafters/stable", "OpenSSL/1.0.2o@conan/stable", "cyrus-sasl-sasl2/2.1.26@rion/stable"
    scm = {
        "type": "git",
        "url": "https://github.com/KDE/qca.git",
        "revision": "da4d1d06d4f67104738cb027b215eb41293c85cd" # 2.2.0 + fixes
    }

    def build(self):
        cmake = CMake(self) # it will find the packages by using our auto-generated FindXXX.cmake files
        # next 3 substitutions are required because Conan generates incompatible with original find module
        replace_in_file("FindOpenSSL.cmake", "OpenSSL_", "OPENSSL_")
        replace_in_file("FindOpenSSL.cmake", "OPENSSL_INCLUDES", "OPENSSL_INCLUDE_DIR")
        replace_in_file(os.path.join("plugins", "qca-ossl", "CMakeLists.txt"),
            'OPENSSL_LIBRARIES',
            'OPENSSL_LIBRARIES_TARGETS',
        )
        # and this one is a kind of bug in qca's cmakelists
        replace_in_file("CMakeLists.txt",
            'set(CMAKE_MODULE_PATH "${CMAKE_CURRENT_SOURCE_DIR}/cmake/modules" )',
            'set(CMAKE_MODULE_PATH "${CMAKE_MODULE_PATH};${CMAKE_CURRENT_SOURCE_DIR}/cmake/modules" )',
        )
        cmake.configure()
        cmake.build()
        
    def package(self):
        install_dir = "conan_install"
        self.copy("*.h", dst="include", src="include")
        self.copy("*qca-qt5.dll", dst="bin", keep_path=False)
        self.copy("*qca-qt5.lib", dst="lib", keep_path=False)
        self.copy("lib/*.dll", dst="crypto", keep_path=False)
    
    def package_info(self):
        if self.settings.compiler == "Visual Studio":
            self.cpp_info.libs = ["qca-qt5.lib"]
        else:
            self.cpp_info.libs = ["qca-qt5"]