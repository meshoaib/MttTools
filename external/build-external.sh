#! /bin/bash

# YAML

wget --no-check-certificate https://yaml-cpp.googlecode.com/files/yaml-cpp-0.5.1.tar.gz
tar xf yaml-cpp-0.5.1.tar.gz

cd yaml-cpp-0.5.1
mkdir build
cd build

cmake -DYAML_CPP_BUILD_TOOLS=OFF -DYAML_CPP_BUILD_CONTRIB=OFF -DCMAKE_INSTALL_PREFIX:PATH=../../ ..

make -j4
make install

cd ../..
rm yaml-cpp-0.5.1.tar.gz

# TCLAP
wget http://optimate.dl.sourceforge.net/project/tclap/tclap-1.2.1.tar.gz
tar xf tclap-1.2.1.tar.gz

cd tclap-1.2.1
./configure --prefix=$PWD/../

make -j4
make install

cd ..
rm tclap-1.2.1.tar.gz

# Json cpp
svn checkout svn://svn.code.sf.net/p/jsoncpp/code/trunk jsoncpp-code

cd jsoncpp-code/jsoncpp
mkdir -p ../build/release
cd ../build/release

cmake -DCMAKE_BUILD_TYPE=release -DCMAKE_INSTALL_PREFIX:PATH=$PWD/../../../ -G "Unix Makefiles" ../../jsoncpp
make -j4
make install

cd ../../..
rm -rf jsoncpp-code
