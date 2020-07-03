import os

from conans import ConanFile, tools, CMake
from conans.tools import replace_in_file

class QcaConan(ConanFile):
    name = "qca"
    description = "Qt Cryptographic Architecture"
    version = "2.3.0.1"
    license = "LGPL 2.1"
    url = "https://github.com/psi-im/qca"
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True]}
    default_options = "shared=True"
    generators = "cmake_find_package"
    requires = "qt/[>=5.5.0]@bincrafters/stable", "openssl/1.1.1g"  # , "cyrus-sasl-sasl2/[>=2.1.27]@rion/stable"

    scm_to_conandata = True
    scm={
        "type": "git",
        "url": "https://github.com/psi-im/qca.git",
        "revision": "ebe945ef67d74952c932f513f51959e875abf8ee" # 2.3.0 + fixes
    }

    def build(self):
        cmake = CMake(self) # it will find the packages by using our auto-generated FindXXX.cmake files
        # next 3 substitutions are required because Conan generates incompatible with original find module
        replace_in_file("FindOpenSSL.cmake", "OpenSSL_", "OPENSSL_")
        replace_in_file("FindOpenSSL.cmake", "OPENSSL_INCLUDES", "OPENSSL_INCLUDE_DIR")
        replace_in_file(os.path.join("plugins", "qca-ossl", "CMakeLists.txt"),
            'OpenSSL::SSL OpenSSL::Crypto',
            'OpenSSL::OpenSSL',
        )
        # and this one is a kind of bug in qca's cmakelists
        replace_in_file("CMakeLists.txt",
            'set(CMAKE_MODULE_PATH "${CMAKE_CURRENT_SOURCE_DIR}/cmake/modules" )',
            'set(CMAKE_MODULE_PATH "${CMAKE_MODULE_PATH};${CMAKE_CURRENT_SOURCE_DIR}/cmake/modules" )',
        )
        # adapt sasl find module
        if os.path.exists("Findcyrus-sasl-sasl2.cmake"):
            os.rename("Findcyrus-sasl-sasl2.cmake", "FindSasl2.cmake")
            replace_in_file("FindSasl2.cmake", "cyrus-sasl-sasl2_", "SASL2_")
            replace_in_file("FindSasl2.cmake", "SASL2_LIBRARIES_TARGETS", "SASL2_LIBRARIES")
            replace_in_file("FindSasl2.cmake", "SASL2_INCLUDE_DIRS", "SASL2_INCLUDE_DIR")
        
        cmake.configure(['-DBUILD_PLUGINS=ossl'])
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