from conans import ConanFile, CMake
import shutil


class ZmqppConan(ConanFile):
    name = "zmqpp"
    description = "0mq 'highlevel' C++ bindings"
    version = "4.1.2"
    license = "MPLv2"
    url = "https://github.com/gasuketsu/conan-zmqpp"
    settings = "os", "compiler", "build_type", "arch"
    generators = "cmake", "txt"
    exports = "CMakeLists.txt"
    options = {"shared": [True, False], "build_client": [True, False]}
    default_options = "shared=False", "build_client=False"

    def requirements(self):
        self.requires("libzmq/[>4.1.0]@memsharded/stable")
        if self.options.build_client:
            self.requires("Boost/[>1.58.0]@lasote/stable")

    def configure(self):
        if self.options.shared:
            self.options["libzmq"].shared = "True"

    def source(self):
        self.run("git clone https://github.com/zeromq/zmqpp.git")
        self.run("cd zmqpp && git checkout %s" % self.version)
        shutil.move("zmqpp/CMakeLists.txt", "zmqpp/CMakeListsOriginal.cmake")
        shutil.copy("CMakeLists.txt", "zmqpp/CMakeLists.txt")

    def build(self):
        cmake = CMake(self)
        opts = {"ZMQPP_BUILD_STATIC": "ON" if not self.options.shared else "OFF",
                "ZMQPP_BUILD_SHARED": "ON" if self.options.shared else "OFF",
                "ZMQPP_BUILD_CLIENT": "ON" if self.options.build_client else "OFF"}
        cmake.configure(defs=opts, source_dir="zmqpp", build_dir="./")
        cmake.build()

    def package(self):
        self.copy("*.hpp", dst="include/zmqpp", src="zmqpp/src/zmqpp")
        self.copy("*.lib", dst="lib", keep_path=False)
        self.copy("*.dll", dst="bin", keep_path=False)
        self.copy("*.so", dst="lib", keep_path=False, symlinks=True)
        self.copy("*.a", dst="lib", keep_path=False)
        self.copy("*", dst="bin", src="bin", keep_path=False)
        self.copy("license*", dst="licenses", src="zmqpp", ignore_case=True, keep_path=False)

    def package_info(self):
        self.cpp_info.libs = ["zmqpp"] if self.options.shared else ["zmqpp-static"]
