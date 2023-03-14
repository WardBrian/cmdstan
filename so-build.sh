echo 'building main'
g++ -std=c++1y -pthread -D_REENTRANT -Wno-sign-compare -Wno-ignored-attributes        -I stan/lib/stan_math/lib/tbb_2020.3/include    -O3 -I src -I stan/src -I stan/lib/rapidjson_1.1.0/ -I lib/CLI11-1.9.1/ -I stan/lib/stan_math/ -I stan/lib/stan_math/lib/eigen_3.4.0 -I stan/lib/stan_math/lib/boost_1.78.0 -I stan/lib/stan_math/lib/sundials_6.1.1/include -I stan/lib/stan_math/lib/sundials_6.1.1/src/sundials    -DBOOST_DISABLE_ASSERTS          -c -o src/cmdstan/main.o src/cmdstan/main.cpp

g++ -std=c++1y -pthread -D_REENTRANT -Wno-sign-compare -Wno-ignored-attributes  -flto src/cmdstan/main.o       -Wl,-L,"/home/brian/Dev/cpp/cmdstan/stan/lib/stan_math/lib/tbb" -Wl,-rpath,"/home/brian/Dev/cpp/cmdstan/stan/lib/stan_math/lib/tbb"     stan/lib/stan_math/lib/sundials_6.1.1/lib/libsundials_nvecserial.a stan/lib/stan_math/lib/sundials_6.1.1/lib/libsundials_cvodes.a stan/lib/stan_math/lib/sundials_6.1.1/lib/libsundials_idas.a stan/lib/stan_math/lib/sundials_6.1.1/lib/libsundials_kinsol.a  stan/lib/stan_math/lib/tbb/libtbb.so.2 -o main


echo 'building SO'
g++ -std=c++1y -pthread -D_REENTRANT -Wno-sign-compare -Wno-ignored-attributes   -ggdb3   -I stan/lib/stan_math/lib/tbb_2020.3/include    -O3 -I src -I stan/src -I stan/lib/rapidjson_1.1.0/ -I lib/CLI11-1.9.1/ -I stan/lib/stan_math/ -I stan/lib/stan_math/lib/eigen_3.4.0 -I stan/lib/stan_math/lib/boost_1.78.0 -I stan/lib/stan_math/lib/sundials_6.1.1/include -I stan/lib/stan_math/lib/sundials_6.1.1/src/sundials    -DBOOST_DISABLE_ASSERTS     -fPIC -fno-plt    -c -Wno-ignored-attributes   -x c++ -o examples/bernoulli/bernoulli.o examples/bernoulli/bernoulli.hpp

g++ -std=c++1y -pthread -D_REENTRANT -Wno-sign-compare -Wno-ignored-attributes -DBOOST_DISABLE_ASSERTS  -shared -fPIC -fno-plt -flto -o examples/bernoulli/bernoulli.so   examples/bernoulli/bernoulli.o   -Wl,-L,"/home/brian/Dev/cpp/cmdstan/stan/lib/stan_math/lib/tbb" -Wl,-rpath,"/home/brian/Dev/cpp/cmdstan/stan/lib/stan_math/lib/tbb"     stan/lib/stan_math/lib/sundials_6.1.1/lib/libsundials_nvecserial.a stan/lib/stan_math/lib/sundials_6.1.1/lib/libsundials_cvodes.a stan/lib/stan_math/lib/sundials_6.1.1/lib/libsundials_idas.a stan/lib/stan_math/lib/sundials_6.1.1/lib/libsundials_kinsol.a  stan/lib/stan_math/lib/tbb/libtbb.so.2
