from conans import ConanFile, CMake, tools
from conanos.build import config_scheme
import os, shutil

class NvcodecheadersConan(ConanFile):
    name = "nv-codec-headers"
    version = "n8.2.15.6"
    description = "FFmpeg nvidia headers"
    url = "https://github.com/conanos/nv-codec-headers"
    homepage = "https://github.com/FFmpeg/nv-codec-headers"
    license = "GPL-v2+"
    generators = "visual_studio", "gcc"
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False], "fPIC": [True, False]}
    default_options = { 'shared': True, 'fPIC': True }

    _source_subfolder = "source_subfolder"
    _build_subfolder = "build_subfolder"

    def config_options(self):
        if self.settings.os == "Windows":
            del self.options.fPIC

    def configure(self):
        del self.settings.compiler.libcxx

        config_scheme(self)

    def source(self):
        url_ = 'https://github.com/FFmpeg/nv-codec-headers/archive/{version}.tar.gz'
        tools.get(url_.format(version=self.version))
        extracted_dir = self.name + "-" + self.version
        os.rename(extracted_dir, self._source_subfolder)

    def build(self):
        pass
    
    def package(self):
        self.copy("*", dst=os.path.join(self.package_folder,"include"), src=os.path.join(self.build_folder,self._source_subfolder,"include"))
        tools.mkdir(os.path.join(self.package_folder,"lib","pkgconfig"))
        shutil.copy(os.path.join(self.build_folder,self._source_subfolder,"ffnvcodec.pc.in"),
                    os.path.join(self.package_folder,"lib","pkgconfig","ffnvcodec.pc"))
        tools.replace_in_file(os.path.join(self.package_folder,"lib","pkgconfig","ffnvcodec.pc"),"@@PREFIX@@",self.package_folder)

    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)

