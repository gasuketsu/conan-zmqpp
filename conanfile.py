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
    options = {"shared": [True, False],
               "zmqpp_libzmq_cmake": [True, False],
               "zmqpp_build_examples": [True, False],
               "zmqpp_build_client": [True, False],
               "zmqpp_build_tests": [True, False]}
    default_options = '''
shared=False
zmqpp_libzmq_cmake=False
zmqpp_build_examples=False
zmqpp_build_client=False
zmqpp_build_tests=False
'''

    def requirements(self):
        self.requires("libzmq/4.1.5@memsharded/stable")

    def source(self):
       self.run("git clone https://github.com/zeromq/zmqpp.git")
       self.run("cd zmqpp && git checkout 4.1.2")
       shutil.move("zmqpp/CMakeLists.txt", "zmqpp/CMakeListsOriginal.cmake")
       shutil.copy("CMakeLists.txt", "zmqpp/CMakeLists.txt")

    def build(self):
        cmake = CMake(self.settings)
        cmake_options = []
        for option_name in self.options.values.fields:
            activated = getattr(self.options, option_name)
            the_option = "%s=" % option_name.upper()
            if option_name == "shared":
                the_option = "ZMQPP_BUILD_SHARED=ON" if activated else "ZMQPP_BUILD_SHARED=OFF"
            else:
                the_option += "ON" if activated else "OFF"
            cmake_options.append(the_option)
        options_zmqpp = " -D".join(cmake_options)
        conf_command = 'cd zmqpp/cmake_build && cmake .. %s -D%s' % (cmake.command_line, options_zmqpp)
        self.output.warn(conf_command)
        self.run("mkdir -p zmqpp/cmake_build")
        self.run(conf_command)
        self.run("cd zmqpp/cmake_build && cmake --build . %s" % cmake.build_config)

    def package(self):
        self.copy("*.hpp", dst="include/zmqpp", src="zmqpp/src/zmqpp")
        self.copy("*.lib", dst="lib", keep_path=False)
        self.copy("*.dll", dst="bin", keep_path=False)
        self.copy("*.so", dst="lib", keep_path=False)
        self.copy("*.a", dst="lib", keep_path=False)

    def package_info(self):
        self.cpp_info.libs = ["zmqpp"]
