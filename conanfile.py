from conans import ConanFile, CMake, tools
import shutil
import os


class ZmqppConan(ConanFile):
    name = "zmqpp"
    description = "0mq 'highlevel' C++ bindings"
    version = "4.1.2"
    license = "MPLv2"
    url = "https://github.com/gasuketsu/conan-zmqpp"
    settings = "os", "compiler", "build_type", "arch"
    generators = "cmake", "txt", "env"
    exports = "CMakeLists.txt"
    options = {"shared": [True, False]}
    default_options = "shared=True"

    def requirements(self):
        self.requires("libzmq/4.1.5@gasuketsu/testing")

    def source(self):
       self.run("git clone https://github.com/zeromq/zmqpp.git")
       self.run("cd zmqpp && git checkout 4.1.2")
       shutil.move("zmqpp/CMakeLists.txt", "zmqpp/CMakeListsOriginal.cmake")
       shutil.copy("CMakeLists.txt", "zmqpp/CMakeLists.txt")

    def build(self):
        cmake = CMake(self.settings)
        cmake_options = ["-DZMQPP_BUILD_CLIENT=ON"]
        shared_option = "ZMQPP_BUILD_STATIC=OFF" if self.options.shared else "ZMQPP_BUILD_SHARED=OFF"
        cmake_options.append(shared_option)
        options_zmqpp = " -D".join(cmake_options)
        conf_command = 'cd zmqpp/cmake_build && cmake .. %s %s' % (cmake.command_line, options_zmqpp)
        self.output.warn(conf_command)
        self.run("mkdir -p zmqpp/cmake_build")
        self.run(conf_command)
        self.run("cd zmqpp/cmake_build && cmake --build . %s" % cmake.build_config)

    def package(self):
        self.copy("*.hpp", dst="include/zmqpp", src="zmqpp/src/zmqpp")
        self.copy("*.lib", dst="lib", src="zmqpp/cmake_build", keep_path=False)
        self.copy("*.dll", dst="bin", src="zmqpp/cmake_build", keep_path=False)
        self.copy("*.so", dst="lib", src="zmqpp/cmake_build", keep_path=False, symlinks=True)
        self.copy("*.a", dst="lib", src="zmqpp/cmake_build", keep_path=False)
        self.copy("*", dst="bin", src="zmqpp/cmake_build/bin", keep_path=False)

    def package_info(self):
        self.cpp_info.libs = ["zmqpp"] if self.options.shared else ["zmqpp-static"]
        self.env_info.path.append(os.path.join(self.package_folder, "bin"))
        self.env_info.LD_LIBRARY_PATH.append(os.path.join(self.package_folder, "lib"))
